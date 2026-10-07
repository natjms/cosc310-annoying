import json
import os
import atexit
import threading
from collections.abc import Hashable, Iterable
from itertools import islice
from typing import Any, Literal, TextIO, overload

from pydantic import BaseModel, TypeAdapter
from ulid import ULID

class UniqueError(Exception):
    pass

DEFAULT_WAL_COMMIT_INTERVAL = 60 * 60

Id = ULID

type Name = str

type Value = object

type ValueKey = Hashable

type Dump = dict[Name, Value]

def freeze(value: Value) -> ValueKey:
    if isinstance(value, list):
        return tuple(freeze(v) for v in value)
    if isinstance(value, dict):
        return frozenset((k, freeze(v)) for k, v in value.items())
    return value

class Index(dict[ValueKey, dict[Id, Dump]]):
    def _put(self, vkey: ValueKey, id: Id, item: Dump) -> None:
        if not vkey in self: self[vkey] = {}
        self[vkey][id] = item

    def put(self, vkey: ValueKey, id: Id, item: Dump) -> None:
        if isinstance(vkey, tuple):
            for sub_vkey in vkey: self._put(sub_vkey, id, item)
        else:
            self._put(vkey, id, item)

    def _remove(self, vkey: ValueKey, id: Id) -> None:
        if not vkey in self: return
        leaf = self[vkey]
        if not id in leaf: return
        del leaf[id]
        if not leaf: del self[vkey]

    def remove(self, vkey: ValueKey, id: Id) -> None:
        if isinstance(vkey, tuple):
            for sub_vkey in vkey: self._remove(sub_vkey, id)
        else:
            self._remove(vkey, id)

    def _slice_one(self, vkey: ValueKey) -> dict[Id, Dump] | None:
        return self.get(vkey, None)

    def _slice_many(self, vkeys: Iterable[ValueKey]) -> dict[Id, Dump] | None:
        slices = [self._slice_one(vkey) for vkey in vkeys]
        if not slices or not all(slices): return None
        smallest, *others = sorted(slices, key=len) # type: ignore
        return {
            id: dump
            for id, dump in smallest.items()
            if all(id in other for other in others)
        } or None

    def slice(self, vkey: ValueKey) -> dict[Id, Dump] | None:
        if isinstance(vkey, tuple):
            return self._slice_many(vkey)
        else:
            return self._slice_one(vkey)

class Repo[T: BaseModel]:
    name: str
    model: type[T]

    _lock: threading.Lock

    _id: dict[Id, Dump]
    _indices: dict[Name, Index]

    _adapters: dict[Name, TypeAdapter]

    _path_dir: str
    _path_data: str
    _path_temp: str
    _path_wal: str

    _wal: TextIO | None
    _wal_commit_stop: threading.Event
    _wal_commit_thread: threading.Thread | None
    _wal_commit_interval: int

    def __init__(
        self,
        name: str,
        model: type[T],
        indexed_fields: Iterable[Name],
        wal_commit_interval: int = DEFAULT_WAL_COMMIT_INTERVAL
    ):
        if not isinstance(name, str) or not name.isalnum():
            raise ValueError("name must be an alphanumeric string")
        if not isinstance(model, type) or not issubclass(model, BaseModel):
            raise TypeError("model must be a subclass of BaseModel")

        id_field = model.model_fields.get('id', None)
        if id_field is None or id_field.annotation != ULID:
            raise TypeError(f"model {model.__name__} must have an 'id' field of type ULID")

        indexed_fields = list(indexed_fields)

        for field in indexed_fields:
            if field not in model.model_fields:
                raise ValueError(f"indexed field {field!r} is not a field of model {model.__name__}")

        if len(set(indexed_fields)) != len(indexed_fields):
            raise ValueError("indexed_fields must be unique")
        if 'id' in indexed_fields:
            raise ValueError("indexed_fields must not contain 'id'")

        if type(wal_commit_interval) is not int or wal_commit_interval < 0:
            raise ValueError("wal_commit_interval must be a non-negative integer of seconds, 0 to disable")

        self.name = name
        self.model = model

        self._lock = threading.Lock()

        self._id = {}
        self._indices = { field: Index() for field in indexed_fields }

        self._adapters = {
            field: TypeAdapter(info.rebuild_annotation())
            for field, info in model.model_fields.items()
        }

        data_dir = os.getenv('DATA_DIR', os.getcwd())

        self._path_dir = data_dir
        self._path_data = os.path.join(data_dir, f"{name}.json")
        self._path_temp = os.path.join(data_dir, f"{name}.json.tmp")
        self._path_wal = os.path.join(data_dir, f"{name}.wal.json")

        self._wal = None
        self._wal_commit_stop = threading.Event()
        self._wal_commit_thread = None
        self._wal_commit_interval = wal_commit_interval

        self._replay_file(self._path_data, required=True)
        self._replay_file(self._path_wal, required=False)

        atexit.register(self._shutdown)

        if self._wal_commit_interval > 0:
            self._wal_commit_thread = threading.Thread(
                target=self._wal_commit_loop,
                name=f"repo-{name}-commit",
                daemon=True,
            )
            self._wal_commit_thread.start()

    def _to_dump(self, instance: T, mode: Literal['json', 'python'] = 'json') -> Dump:
        if isinstance(instance, self.model):
            return instance.model_dump(mode=mode)
        else:
            raise TypeError(f"expected instance of model {self.model.__name__}, got type {type(instance)}")

    def _from_dump(self, dump: Dump) -> T:
        return self.model.model_validate(dump)

    def _get(self, id: Id) -> Dump | None:
        return self._id.get(id, None)

    def _replay(self, line: str) -> None:
        try:
            new = json.loads(line)

            id = ULID.parse(new['id'])

            old = self._get(id)

            if '__deleted__' in new:
                if old is None:
                    raise ValueError(f"cannot delete {id!r} because it does not exist")

                del self._id[id]

                for field, index in self._indices.items():
                    index.remove(freeze(old[field]), id)

            else:
                self._id[id] = new

                for field, index in self._indices.items():
                    new_vkey = freeze(new[field])
                    if old is not None:
                        old_vkey = freeze(old[field])
                        if old_vkey != new_vkey:
                            index.remove(old_vkey, id)
                    index.put(new_vkey, id, new)

        except Exception as e:
            print(f"repo {self.name} failed to replay line:\n\t{line}\nbecause: {e}")

    def _replay_file(self, path: str, required: bool) -> None:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                for line in file:
                    self._replay(line)
        except FileNotFoundError:
            if required:
                print(f"repo {self.name} failed to replay file: {path!r} not found")

    def _wal_write(self, dump: Dump) -> None:
        # caller must hold self._lock

        line = json.dumps(dump, ensure_ascii=True, separators=(',', ':'))

        if self._wal is None:
            self._wal = open(self._path_wal, 'a', encoding='utf-8')

        self._wal.write(line + '\n')
        self._wal.flush()
        os.fsync(self._wal.fileno())

    def _wal_commit(self) -> None:
        # caller must hold self._lock

        # write all rows to the temp file, and flush + sync it
        with open(self._path_temp, 'w', encoding='utf-8') as file:
            for dump in self._id.values():
                file.write(json.dumps(dump, ensure_ascii=True, separators=(',', ':')) + '\n')
            file.flush()
            os.fsync(file.fileno())

        # close the wal before swapping,
        # nobody should be writing to it anyway 'cause of the lock
        if self._wal is not None:
            self._wal.close()
            self._wal = None

        # atomically swap the temp file over the data file
        os.replace(self._path_temp, self._path_data)

        # sync the directory so the rename itself is durable
        # works on my machine!
        try:
            dir_fd = os.open(self._path_dir, os.O_RDONLY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        except OSError:
            pass

        # the data file now contains everything, the wal is redundant
        try:
            os.remove(self._path_wal)
        except FileNotFoundError:
            pass

    def _try_wal_commit(self, reason: str) -> None:
        # the timeout avoids hanging forever if a thread died holding the lock
        if not self._lock.acquire(timeout=5):
            print(f"repo {self.name} failed to commit {reason}: could not acquire lock")
            return
        try:
            # nothing to do if there is no wal, meaning no changes since the last commit
            if self._wal is None and not os.path.exists(self._path_wal): return
            self._wal_commit()
        except Exception as e:
            print(f"repo {self.name} failed to commit {reason}: {e}")
        finally:
            self._lock.release()

    def _wal_commit_loop(self) -> None:
        interval = self._wal_commit_interval
        # wait returns true once the stop event is set, ending the loop
        while not self._wal_commit_stop.wait(interval):
            self._try_wal_commit("on timer")

    def _shutdown(self) -> None:
        # stop the timer to avoid racing with the loop
        self._wal_commit_stop.set()
        self._try_wal_commit("on exit")

    def _upsert(self, patch: Dump, /, can_create: bool, can_update: bool) -> T:
        for field in patch:
            if field not in self.model.model_fields:
                raise ValueError(f"field {self.name}[{field!r}] is not a field of model {self.model.__name__}")

        id = patch.get('id', None)
        if not id:
            if not can_create:
                raise ValueError("id is required, but was not set or provided")
            id = Id()
        elif not isinstance(id, Id):
            try:
                id = Id.parse(id)
            except (TypeError, ValueError) as e:
                raise ValueError(f"id must be a ULID, got {id!r}") from e

        with self._lock:

            old = self._get(id)
            if old is not None and not can_update:
                raise ValueError(f"{self.name}.id={id} already exists, cannot create")
            if old is None and not can_create:
                raise ValueError(f"{self.name}.id={id} does not exist, cannot update")

            instance = self._from_dump((old or {}) | patch | { 'id': id })

            new = self._to_dump(instance)

            self._id[id] = new

            for field, index in self._indices.items():
                new_vkey = freeze(new[field])
                if old is not None:
                    old_vkey = freeze(old[field])
                    if old_vkey != new_vkey:
                        index.remove(old_vkey, id)
                index.put(new_vkey, id, new)

            self._wal_write(new)

            return instance

    def _delete(self, id: Id) -> bool:
        if not isinstance(id, Id):
            try:
                id = Id.parse(id)
            except (TypeError, ValueError) as e:
                raise ValueError(f"id must be a ULID, got {id!r}") from e

        with self._lock:

            dump = self._get(id)
            if not dump: return False

            del self._id[id]

            for field, index in self._indices.items():
                vkey = freeze(dump[field])
                index.remove(vkey, id)

            self._wal_write({ 'id': str(id), '__deleted__': True })

            return True

    def _adapt(self, field: Name, value: Value) -> Value:
        adapter = self._adapters[field]
        value = adapter.validate_python(value)
        value = adapter.dump_python(value, mode='json')
        return value

    def _index_slice(self, field: Name, value: Value) -> dict[Id, Dump] | None:
        vkey = freeze(self._adapt(field, value))
        return self._indices[field].slice(vkey)

    def _index_slices(self, slices: dict[Name, Value]) -> Iterable[Dump]:
        for field in slices:
            if field not in self._indices and field != 'id':
                raise ValueError(f"field {self.name}[{field!r}] is not indexed")

        required_id: Id | None = None

        if 'id' in slices:
            id = slices.pop('id')
            if not isinstance(id, Id):
                try:
                    id = Id.parse(id)
                except (TypeError, ValueError) as e:
                    raise ValueError(f"id must be a ULID, got {id!r}") from e
            if id not in self._id:
                return ()
            if not slices:
                return (self._id[id],)
            required_id = id
        else:
            if not slices:
                return self._id.values()

        slices_iter = iter(slices.items())

        first_field, first_value = next(slices_iter)
        first_slice = self._index_slice(first_field, first_value)

        if not first_slice:
            return ()

        if required_id is not None:
            if required_id not in first_slice:
                return ()
            else:
                first_slice = { required_id: first_slice[required_id] }

        if len(slices) == 1:
            return first_slice.values()

        matching_ids = set(first_slice)

        for field, value in slices_iter:
            slice = self._index_slice(field, value)
            if not slice: return ()
            matching_ids.intersection_update(slice)
            if not matching_ids: return ()

        return (self._id[id] for id in matching_ids)

    def _query(self, query: dict[str, Any]) -> list[T]:
        slices = query.copy()

        skip = slices.pop('_skip', 0)
        limit = slices.pop('_limit', 0)
        order_by = slices.pop('_order_by', None)
        order_desc = slices.pop('_order_desc', False)

        if skip is None: skip = 0
        elif type(skip) is not int or skip < 0:
            raise ValueError(f"_skip must be a non-negative integer, got {skip!r}")

        if limit is None: limit = 0
        elif type(limit) is not int or limit < 0:
            raise ValueError(f"_limit must be a non-negative integer, got {limit!r}")

        if order_desc is None: order_desc = False
        elif type(order_desc) is not bool:
            raise ValueError(f"_order_desc must be a boolean, got {order_desc!r}")

        if order_by is not None and (
            not isinstance(order_by, str) or \
            order_by not in self.model.model_fields
        ):
            raise ValueError(f"_order_by must be a field of model {self.model.__name__}, got {order_by!r}")

        with self._lock:
            rows = list(self._index_slices(slices))

        if order_by is not None:
            def key(row):
                v = row[order_by]
                return (v is None, v)
            rows = sorted(rows, key=key, reverse=order_desc) # type: ignore

        stop = None if limit == 0 else skip + limit

        return [
            self._from_dump(row)
            for row in islice(rows, skip, stop)
        ]

    @overload
    def create(self, instance: T, /) -> T: ...
    @overload
    def create(self, /, **kwargs: Any) -> T: ...
    def create(self, instance: T | None = None, /, **kwargs: Any) -> T:
        dump = self._to_dump(instance, 'python') if instance is not None else kwargs
        return self._upsert(dump, True, False)

    @overload
    def update(self, instance: T, /) -> T: ...
    @overload
    def update(self, /, **kwargs: Any) -> T: ...
    def update(self, instance: T | None = None, /, **kwargs: Any) -> T:
        dump = self._to_dump(instance, 'python') if instance is not None else kwargs
        return self._upsert(dump, False, True)

    def upsert(self, instance: T) -> T:
        return self._upsert(self._to_dump(instance, 'python'), True, True)

    def delete(self, id: Id) -> bool:
        return self._delete(id)

    def select(self, /, **query: Any) -> list[T]:
        return self._query(query)

    def unique(self, /, **query: Any) -> T:
        results = self._query(query)
        if len(results) < 1:
            raise UniqueError(f"no row found in {self.name} for query: {query!r}")
        if len(results) > 1:
            raise UniqueError(f"multiple rows found in {self.name} for query: {query!r}")
        return results[0]

class User(BaseModel):
    id: Id
    name: str
    age: int
    follows: list[Id] = []

class Post(BaseModel):
    id: Id
    author_id: Id
    content: str
    tags: list[str]

users = Repo('users', User, indexed_fields=['name', 'age', 'follows'])
posts = Repo('posts', Post, indexed_fields=['author_id', 'tags'])

"""
# create myself:
lua = users.create(name='luavixen', age=22)
# note that the ID is generated automatically

# also create my girlfriend:
iris = users.create(User(id=Id(), name='iris', age=21, follows=[lua.id]))

# well obviously i follow her:
users.update(id=lua.id, follows=[iris.id])

# and john is here too:
john = users.create(name='john', age=20)

# john follows everyone:
users.update(id=john.id, follows=[iris.id, lua.id])

# let's print everyone who follows me:
print("these users follow lua:")
for user in users.select(follows=[lua.id]):
    print(f"  - {user.name}")

# ok let's get posting
posts.create(author_id=lua.id, content='wow... what a cool website', tags=['hello', 'website'])
posts.create(author_id=iris.id, content='just joined lol hi', tags=['hello', 'launch'])
posts.create(author_id=john.id, content='first day gang', tags=['launch', 'hello'])
posts.create(author_id=lua.id, content='posting works lets gooo', tags=['website', 'launch'])
posts.create(author_id=iris.id, content='ok this is kinda cute', tags=['website', 'vibes'])
posts.create(author_id=john.id, content='who up eating lunch rn. at the website launch', tags=['lunch', 'launch', 'wow'])

# what posts are tagged with 'website'?
print("posts tagged with 'website':")
for post in posts.select(tags=['website']):
    print(f"  - {users.unique(id=post.author_id).name} says {post.content!r}")

# delete posts tagged with 'hello' i HATE saying hello
for post in posts.select(tags=['hello']):
    posts.delete(id=post.id)

# ok print all posts
print("all posts, after deleting 'hello' posts:")
for post in posts.select():
    print(f"  - {users.unique(id=post.author_id).name} says {post.content!r}")

# find a unique post with the tags 'launch' and 'website'
print("unique post with tags 'launch' and 'website':")
post = posts.unique(tags=['launch', 'website'])
print(f"  - {users.unique(id=post.author_id).name} says {post.content!r} with tags {post.tags!r}")
"""

for user in users.select():
    print(user)

for post in posts.select():
    print(post)

posts.create(author_id=users.unique(name='luavixen').id, content='wawa', tags=['fox noises'])
