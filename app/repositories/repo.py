"""Thread-safe in-memory relational database abstraction with persistence to disk and write-ahead logging.

Here's a comprehensive set of doctests that show how to use `Repo`,
including all the CRUD operations and foreign key usage:

>>> class User(BaseModel):
...     id: Id
...     name: str
...     age: int
...     tags: list[str] = []

>>> class Post(BaseModel):
...     id: Id
...     author_id: Id  # foreign key User.id
...     content: str

Create/load repositories by calling the constructor with the name & model class:

>>> users = Repo('users', User, indexed_fields=['name', 'age', 'tags'], in_memory=True)
>>> posts = Repo('posts', Post, indexed_fields=['author_id'], fulltext_fields=['content'], in_memory=True)

Create some users:

>>> a = users.create(name='ada', age=30, tags=['admin', 'dev'])        # id is generated if omitted
>>> b = users.create(User(id=Id(), name='bob', age=25, tags=['dev']))  # can pass a model instance
>>> c = users.create(name='cy', age=30)                                # defaults used for missing fields

Update a user's age, partial patch, by `id`:

>>> new_b = users.update(id=b.id, age=26)
>>> (new_b.name, new_b.age)
('bob', 26)
>>> new_b is b
False

Note that `new_b` is a copy, not the same instance as `b`.
The repository always copies model instances, storing them as decomposed `Dump`s.
This means that mutations to the original or returned instances do not affect the stored data.

Find a single unique user by `id` or other indexed field:

>>> ada = users.unique(name='ada')
>>> ada == a    and ada is not a
True

>>> foo = users.unique(age=30)
Traceback (most recent call last):
app.repositories.repo.UniqueError: multiple rows found in users for query: {'age': 30}

>>> bar = users.unique(id=Id())
Traceback (most recent call last):
app.repositories.repo.UniqueError: no row found in users for query: {'id': ...}

Upsert full instances, creating or replacing as needed:

>>> new_c = users.upsert(c.model_copy(update={'tags': ['ops']}))
>>> new_c.tags
['ops']

>>> j = users.upsert(User(id=Id(), name='john', age=32))
>>> j == users.unique(id=j.id)
True

Delete a user by `id`:

>>> was_deleted = users.delete(id=j.id)
>>> was_deleted
True
>>> users.delete(id=j.id)  # already deleted
False

This is just a utility function for the upcoming select examples:

>>> def names(users: list[User]) -> list[str]:
...     return [u.name for u in users]

Select, equality on indexed fields, multiple fields are ANDed:

>>> rows = users.select(age=30)
>>> names(rows)
['ada', 'cy']

>>> rows = users.select(age=30, tags=['dev'])
>>> names(rows)
['ada']

List fields match by their elements, multiple values are ANDed:

>>> names( users.select(tags=['dev']) )
['ada', 'bob']

>>> names( users.select(tags=['dev', 'admin']) )
['ada']

Query values are coerced to the field's type automagically!
E.g. `str -> int` or `str -> ULID`:

>>> names( users.select(age='26', id=str(b.id)) )
['bob']

Ordering and pagination is supported via `_order_by`, `_order_desc`, `_skip`, `_limit`.
Default order is by `id`, which contains creation time.

Here's a complex query, get the oldest two users, skipping the oldest, ordered by age:

>>> rows = users.select(_order_by='age', _order_desc=True, _skip=1, _limit=2)
>>> names(rows)
['cy', 'bob']

Hrm. Let's add back John, and also give Ada a birthday, and try again:

>>> _ = users.create(j)
>>> _ = users.update(id=a.id, age=a.age + 1)

>>> rows = users.select(_order_by='age', _order_desc=True, _skip=1, _limit=2)
>>> names(rows)
['ada', 'cy']

And now, without the limit or the skip:

>>> rows = users.select(_order_by='age', _order_desc=True)
>>> names(rows)
['john', 'ada', 'cy', 'bob']

Without any query, select returns all rows, ordered by `id` (creation time):

>>> names( users.select() )
['ada', 'bob', 'cy', 'john']

Unlike `unique`, `select` returns all matching rows, not just the first one. It can also return nothing!

>>> users.select(tags=['manager'])
[]

Now, let's create some posts, with foreign keys linking them to their authors:

>>> def create_post(author: User, content: str) -> Post:
...     return posts.create(author_id=author.id, content=content)

>>> def contents(posts: list[Post]) -> list[str]:
...     return [post.content for post in posts]

>>> _ = create_post(a, 'hello world')
>>> _ = create_post(a, 'my second post')
>>> _ = create_post(c, 'hello from cy')

One-to-many query, a user's posts:

>>> rows = posts.select(author_id=a.id, _limit=10, _order_desc=True)
>>> contents(rows)
['my second post', 'hello world']

Many-to-one query, a post's author:

>>> for post in posts.select():
...     author = users.unique(id=post.author_id)
...     print(f'{author.name}: {post.content}')
ada: hello world
ada: my second post
cy: hello from cy

Let's use fulltext search to find posts by content:

>>> rows = posts.select(content='hello')
>>> contents(rows)
['hello world', 'hello from cy']

Oh! Cy wants to edit his hello post:

>>> p = posts.unique(author_id=c.id, content='hello from cy')
>>> _ = posts.update(id=p.id, content='hello from cy. it takes just a second to post!')

Check how fulltext search matches "second post", including how the closer match comes first:
>>> rows = posts.select(content='second post')
>>> contents(rows)
['my second post', 'hello from cy. it takes just a second to post!']

Ada wants to delete all her data, so let's oblige.
Note that you can only delete by ID:

>>> a = users.unique(name='ada')
>>> for p in posts.select(author_id=a.id):
...     _ = posts.delete(id=p.id)
>>> users.delete(id=a.id)
True

As you can see, she's been deleted:

>>> users.select(id=a.id)
[]
>>> posts.select(author_id=a.id)
[]

And let's make sure fulltext search lost Ada's post:

>>> rows = posts.select(content='hello')
>>> contents(rows)
['hello from cy. it takes just a second to post!']

Finally, in-memory databases support `delete_all`, used for testing:

>>> posts.delete_all()
>>> posts.select()
[]
"""

from abc import ABC, abstractmethod
import os
import atexit
import threading
from io import FileIO
import json
from itertools import islice
from collections.abc import Hashable, Iterable
from typing import Any, Final, Literal, overload, override

from pydantic import BaseModel, TypeAdapter
from pocketsearch import Blob, PocketSearch, Schema, Text
from ulid import ULID

class UniqueError(Exception):
    """Raised when a unique constraint is violated."""

DEFAULT_WAL_COMMIT_INTERVAL: Final[int] = 60 * 60
"""The default WAL commit interval, in seconds."""

Id = ULID
"""The type of the `id` primary key field, always a `ULID`.

This is not a type alias, just a normal constant,
to allow for `Id()` construction and `isinstance(x, Id)` checks.
Changing the ID type also requires minor changes to `Repo`'s implementation.
"""

type Name = str
"""Represents the name of a field of a `Dump` or a `BaseModel` instance."""

type Value = object
"""Represents the value of a field of a `Dump` or a `BaseModel` instance."""

type ValueKey = Hashable
"""Represents a hashable value.

When a `Dump` contains a `Value` that is a `list`/`set`/`dict`,
it is converted to a `ValueKey` by recursively `freeze()`ing its elements.
These `ValueKey`s used by `Index` to index complex/nested `Value`s.

`Index` will flatten out the first level of a `list`/`set`/`dict`,
which allows for partial matching e.g. searching for a post by tag,
but it does not flatten beyond the first level, allowing for e.g. full dictionaries to be matched against.
"""

type Dump = dict[Name, Value]
"""Represents a `Dump` instance, a dictionary of `Name` to `Value` pairs.

Instead of storing model instances directly, or storing JSON strings,
we pick a middle ground: dump the model instance using `model_dump(mode='json')` and store that,
converting it to JSON when de/serializing, and converting it back to `BaseModel` instances when querying.
"""

def freeze(value: Value) -> ValueKey:
    """Freezes a `Value` into a `ValueKey` by recursively `freeze()`ing it and its elements.

    `freeze()` converts:
        * `list` to `tuple`
        * `set` to `frozenset`
        * `dict` to `frozenset` of `(key, value)` pairs
        * all other values are left as-is
    """
    # represent lists as tuples, freeze elements
    if isinstance(value, list):
        return tuple(freeze(v) for v in value)
    # represent sets as frozensets, freeze elements
    if isinstance(value, set):
        return frozenset(freeze(v) for v in value)
    # represent dicts as frozensets of (key, value) pairs, freeze values
    if isinstance(value, dict):
        return frozenset((k, freeze(v)) for k, v in value.items())
    # all other values are left as-is
    return value

class Index(ABC):
    """Represents an index over a specific field of `Dump` values for `Repo`."""

    @abstractmethod
    def slice(self, vkey: ValueKey) -> dict[Id, Dump] | None: ...

    @abstractmethod
    def put(self, vkey: ValueKey, id: Id, item: Dump) -> None: ...

    @abstractmethod
    def remove(self, vkey: ValueKey, id: Id) -> None: ...

    @abstractmethod
    def clear(self) -> None: ...

class HashIndex(dict[ValueKey, dict[Id, Dump]], Index):
    """Provides a dict-backed implementation of `Index`.

    Given all rows in the repository, and the field to index, the `HashIndex`
    is interested in the set of all unique values for the field, e.g.
    `set([ row[field] for row in repo ])`. We've implemented `HashIndex` as a
    nested dictionary: it maps each unique field value to a sub-dictionary of
    `Id -> Dump` pairs, where each `Id`/`Dump` represents one of the rows that
    has that unique value in the indexed field. All mutation functions in
    `Repo` work very carefully to ensure this representation is accurate.

    Additionally, the `HashIndex` adds an additional rule for
    `tuple`/`frozenset`s (and `list`/`set`/`dict`, which are frozen into
    `tuple`/`frozenset`), where the first level of the container is flattened.
    Instead of the entire container being treated as one unique value that the
    given `Id`/`Dump` has, the container's values are all treated as seperate
    `ValueKey`s, allowing queries to partial-match against a container's
    content. This special querying functionality is implemented in
    `_slice_many`.
    """

    def _put(self, vkey: ValueKey, id: Id, item: Dump) -> None:
        """Adds the given `Id`/`Dump` pair to the `HashIndex` under the given `ValueKey`."""
        if not vkey in self: self[vkey] = {}
        self[vkey][id] = item

    @override
    def put(self, vkey: ValueKey, id: Id, item: Dump) -> None:
        """Adds the given `Id`/`Dump` pair to the `HashIndex` under the given `ValueKey`,
           flattening `tuple`/`frozenset` values.
        """
        if isinstance(vkey, (tuple, frozenset)):
            for sub_vkey in vkey: self._put(sub_vkey, id, item)
        else:
            self._put(vkey, id, item)

    def _remove(self, vkey: ValueKey, id: Id) -> None:
        """Removes the given `Id`/`Dump` pair from the `HashIndex` under the given `ValueKey`."""
        if not vkey in self: return
        leaf = self[vkey]
        if not id in leaf: return
        del leaf[id]
        if not leaf: del self[vkey]

    @override
    def remove(self, vkey: ValueKey, id: Id) -> None:
        """Removes the given `Id`/`Dump` pair from the `HashIndex` under the given `ValueKey`,
           flattening `tuple`/`frozenset` values.
        """
        if isinstance(vkey, (tuple, frozenset)):
            for sub_vkey in vkey: self._remove(sub_vkey, id)
        else:
            self._remove(vkey, id)

    def _slice_one(self, vkey: ValueKey) -> dict[Id, Dump] | None:
        """Returns the slice of the `HashIndex` under the given `ValueKey`."""
        return self.get(vkey, None)

    def _slice_many(self, vkeys: Iterable[ValueKey]) -> dict[Id, Dump] | None:
        """Returns the intersection of the `HashIndex` slices under the given `ValueKey` values."""
        # we want the intersection, collect all slices
        slices = [self._slice_one(vkey) for vkey in vkeys]
        if not slices or not all(slices): return None
        # find the smallest slice and use it as the basis for the intersection
        smallest, *others = sorted(slices, key=len) # type: ignore
        return {
            id: dump
            for id, dump in smallest.items()
            if all(id in other for other in others)
            # all other slices must contain this id
        } or None
        # return None if the intersection is empty

    @override
    def slice(self, vkey: ValueKey) -> dict[Id, Dump] | None:
        """Returns the slice of the `HashIndex` under the given `ValueKey`,
           or performs an intersection of multiple slices if the `ValueKey` is a `tuple`/`frozenset`.
        """
        if isinstance(vkey, (tuple, frozenset)):
            return self._slice_many(vkey)
        else:
            return self._slice_one(vkey)

FTS_MAX_RESULTS = 100

def vkey_to_search(vkey: ValueKey) -> str:
    if isinstance(vkey, (tuple, frozenset)):
        return " ".join(str(v) for v in vkey)
    else:
        return str(vkey)

class FTSSchema(Schema):
    ulid = Blob(is_id_field=True)
    text = Text(index=True)

class FTSIndex(PocketSearch, Index):
    """Provides a full-text search implementation of `Index`, powered by PocketSearch.

    PocketSearch uses Python's built-in SQLite database support, and the FTS5
    extension for full-text search: https://sqlite.org/fts5.html. The SQLite
    database is in-memory, and I store `Id`/`Dump`s as `ulid BLOB, text TEXT`
    where the `text` field is computed from the `ValueKey` using
    `vkey_to_search`. Note that PocketSearch defaults to only returning 10
    results, but I've adjusted it to up to 100 results in `slice`. Ideally
    these should be most-to-least relevant.

    This `Index` doesn't actually store the `Dump` values, so instead it takes
    the `Repo`'s `_id` dict in the constructor to look up `Dump`s by `Id`
    as-needed.
    """

    def __init__(self, id: dict[Id, Dump]):
        super().__init__(schema=FTSSchema) # type: ignore
        self._id = id

    @override
    def put(self, vkey: ValueKey, id: Id, item: Dump) -> None:
        self.insert_or_update(ulid=id.bytes, text=vkey_to_search(vkey))

    @override
    def remove(self, vkey: ValueKey, id: Id) -> None:
        if d := self.search(ulid=id.bytes)[0]:
            self.delete(rowid=d.id) # type: ignore

    @override
    def clear(self) -> None:
        self.delete_all()

    @override
    def slice(self, vkey: ValueKey) -> dict[Id, Dump] | None:
        return {
            (i := ULID(d.ulid)): self._id[i]
            for d in self.search(text=vkey_to_search(vkey))[0:FTS_MAX_RESULTS] # type: ignore
        }

class Repo[T: BaseModel]:
    name: str
    """Name of the repository."""
    model: type[T]
    """Type of the model stored in the repository."""

    _lock: threading.RLock

    _id: dict[Id, Dump]
    _indices: dict[Name, Index]
    _fulltext: set[Name]

    _adapters: dict[Name, TypeAdapter]

    _in_memory: bool

    _path_dir: str
    _path_data: str
    _path_temp: str
    _path_wal: str

    _wal: FileIO | None
    _wal_failed: bool
    _wal_commit_stop: threading.Event
    _wal_commit_thread: threading.Thread | None
    _wal_commit_interval: int

    _dir_fd: int | None

    _shutdown_hook: Any

    def __init__(
        self,
        name: str,
        model: type[T],
        indexed_fields: Iterable[Name],
        fulltext_fields: Iterable[Name] = (),
        in_memory: bool = False,
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
        fulltext_fields = list(fulltext_fields)
        all_fields = indexed_fields + fulltext_fields

        for field in all_fields:
            if field not in model.model_fields:
                raise ValueError(f"indexed field {field!r} is not a field of model {model.__name__}")

        if len(set(all_fields)) != len(all_fields):
            raise ValueError("indexed fields must be unique")
        if 'id' in all_fields:
            raise ValueError("indexed fields must not contain 'id'")

        if type(wal_commit_interval) is not int or wal_commit_interval < 0:
            raise ValueError("wal_commit_interval must be a non-negative integer of seconds, 0 to disable")

        self.name = name
        self.model = model

        self._lock = threading.RLock()

        self._id = {}
        self._indices = {field: HashIndex() for field in indexed_fields} | \
                        {field: FTSIndex(self._id) for field in fulltext_fields} # type: ignore
        self._fulltext = set(fulltext_fields)

        # adapters are used for select()/unique() to convert query values to the model's type
        # this allows you to e.g. pass one type (e.g. str) and have it converted to the model's type (e.g. int)
        self._adapters = {
            field: TypeAdapter(info.rebuild_annotation())
            for field, info in model.model_fields.items()
        }

        self._in_memory = in_memory

        data_dir = os.getenv('DATA_DIR', os.getcwd())
        if data_dir == ':memory:':
            self._in_memory = True

        self._path_dir = data_dir
        self._path_data = os.path.join(data_dir, f"{name}.json")
        self._path_temp = os.path.join(data_dir, f"{name}.json.tmp")
        self._path_wal = os.path.join(data_dir, f"{name}.wal.json")

        self._wal = None
        self._wal_failed = False
        self._wal_commit_stop = threading.Event()
        self._wal_commit_thread = None
        self._wal_commit_interval = wal_commit_interval

        if not self._in_memory:
            try:
                self._dir_fd = os.open(data_dir, os.O_RDONLY)
            except (OSError, NotImplementedError):
                self._dir_fd = None

            # register the shutdown handler to commit WAL on exit
            self._shutdown_hook = atexit.register(self._shutdown)

            # start the WAL commit loop, if the interval is positive
            if self._wal_commit_interval > 0:
                self._wal_commit_thread = threading.Thread(
                    target=self._wal_commit_loop,
                    name=f"repo-{name}-commit",
                    daemon=True,
                )
                self._wal_commit_thread.start()

            # replay the data and WAL files to recover state
            with self._lock:
                self._replay_file(self._path_data, allow_torn_tail=False)
                if self._replay_file(self._path_wal, allow_torn_tail=True):
                    self._wal_commit()

    def _dump2model(self, dump: Dump) -> T:
        return self.model.model_validate(dump, by_name=True)

    def _model2dump(self, instance: T, mode: Literal['json', 'python'] = 'json') -> Dump:
        if isinstance(instance, self.model):
            return instance.model_dump(mode=mode, exclude_computed_fields=True)
        else:
            raise TypeError(f"expected instance of model {self.model.__name__}, got type {type(instance)}")

    def _apply_put(self, id: Id, new: Dump) -> None: # must hold _lock
        old = self._id.get(id)
        self._id[id] = new
        for field, index in self._indices.items():
            new_vkey = freeze(new[field])
            if old is not None:
                old_vkey = freeze(old[field])
                if old_vkey != new_vkey:
                    index.remove(old_vkey, id)
            index.put(new_vkey, id, new)

    def _apply_delete(self, id: Id) -> bool: # must hold _lock
        old = self._id.pop(id, None)
        if old is None: return False
        for field, index in self._indices.items():
            index.remove(freeze(old[field]), id)
        return True

    def _replay_line(self, line: str) -> None: # must hold _lock
        row = json.loads(line)
        id = Id.parse(row['id'])
        if row.get('__deleted__'):
            # a missing row is fine here, replaying an old WAL must be idempotent
            self._apply_delete(id)
        else:
            self._apply_put(id, self._model2dump(self._dump2model(row)))

    def _replay_file(self, path: str, allow_torn_tail: bool) -> bool: # must hold _lock
        try:
            file = open(path, 'r', encoding='utf-8')
        except FileNotFoundError:
            return False
        with file:
            bad: tuple[int, Exception] | None = None
            line = ''
            for lineno, line in enumerate(file, 1):
                if bad is not None:
                    raise ValueError(f"{path} line {bad[0]}: {bad[1]!r}") from bad[1]
                try:
                    self._replay_line(line)
                except Exception as e:
                    bad = (lineno, e)
            if bad is not None:
                # only a final line with no newline can be a write cut off by a crash
                if not allow_torn_tail or line.endswith('\n'):
                    raise ValueError(f"{path} line {bad[0]}: {bad[1]!r}") from bad[1]
                print(f"repo {self.name} ignoring torn last line of {path}")
        return True

    def _dump2bytes(self, dump: Dump) -> bytes:
        return (json.dumps(dump, ensure_ascii=True, separators=(',', ':')) + '\n').encode('ascii')

    def _fsync_dir(self) -> None:
        if self._dir_fd is not None:
            try:
                os.fsync(self._dir_fd)
            except OSError:
                pass

    def _wal_write(self, dump: Dump) -> None: # must hold _lock
        if self._in_memory:
            return
        if self._wal_failed:
            raise RuntimeError(f"repo {self.name} refused write after a WAL write failed")
        bytes = self._dump2bytes(dump)
        try:
            if self._wal is None:
                # unbuffered, if the write fails it needs to fail now, not later
                self._wal = open(self._path_wal, 'ab', buffering=0)
                self._fsync_dir()
            if self._wal.write(bytes) != len(bytes):
                raise OSError(f"short write to {self._path_wal}")
            os.fsync(self._wal.fileno())
        except BaseException:
            self._wal_failed = True
            raise

    def _wal_commit(self) -> None: # must hold _lock
        if self._in_memory:
            return
        # write all rows to the temp file
        with open(self._path_temp, 'wb') as file:
            for dump in self._id.values():
                bytes = self._dump2bytes(dump)
                if file.write(bytes) != len(bytes):
                    raise OSError(f"short write to {self._path_temp}")
            file.flush()
            os.fsync(file.fileno())
        # close the wal before swapping
        if self._wal is not None:
            self._wal.close()
            self._wal = None
        # atomically swap the temp file over the data file
        os.replace(self._path_temp, self._path_data)
        # the data file now contains everything, the wal is redundant
        try: os.remove(self._path_wal)
        except FileNotFoundError: pass
        # sync the directory so the rename & delete are durable
        self._fsync_dir()
        # wal is good now!
        self._wal_failed = False

    def _try_wal_commit(self, reason: str) -> None: # aquires _lock
        # the timeout avoids hanging forever if a thread died holding the lock
        if not self._lock.acquire(timeout=5):
            print(f"repo {self.name} failed to commit {reason}: could not acquire lock")
            return
        try:
            # nothing to do if there is no wal meaning no changes since the last commit
            if (
                self._wal is None \
                and not self._wal_failed \
                and not os.path.exists(self._path_wal)
            ): return
            # if any of the above conditions are not met, commit the wal
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
        if self._shutdown_hook is not None:
            atexit.unregister(self._shutdown_hook)
            self._shutdown_hook = None

    def close(self) -> None:
        self._shutdown()

    def __enter__(self) -> 'Repo[T]':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def _upsert(self, patch: Dump, /, can_create: bool, can_update: bool) -> T: # aquires _lock
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

            old = self._id.get(id)
            if old is not None and not can_update:
                raise ValueError(f"{self.name}.id={id} already exists, cannot create")
            if old is None and not can_create:
                raise ValueError(f"{self.name}.id={id} does not exist, cannot update")

            instance = self._dump2model((old or {}) | patch | { 'id': id })

            new = self._model2dump(instance)

            self._wal_write(new)
            self._apply_put(id, new)

            return instance

    def _delete(self, id: Id) -> bool: # aquires _lock
        if not isinstance(id, Id):
            try:
                id = Id.parse(id)
            except (TypeError, ValueError) as e:
                raise ValueError(f"id must be a ULID, got {id!r}") from e

        with self._lock:
            if id not in self._id: return False
            self._wal_write({ 'id': str(id), '__deleted__': True })
            return self._apply_delete(id)

    def _delete_all(self) -> None: # aquires _lock
        if not self._in_memory:
            raise NotImplementedError("delete_all on-disk repo")

        with self._lock:
            self._id.clear()
            for index in self._indices.values():
                index.clear()

    def _adapt(self, field: Name, value: Value) -> Value:
        adapter = self._adapters[field]
        value = adapter.validate_python(value)
        value = adapter.dump_python(value, mode='json')
        return value

    def _index_slice(self, field: Name, value: Value) -> dict[Id, Dump] | None: # must hold _lock
        vkey = freeze(self._adapt(field, value))
        return self._indices[field].slice(vkey)

    def _index_slices(self, slices: dict[Name, Value]) -> Iterable[Dump]: # must hold _lock
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

    def _query(self, query: dict[str, Any]) -> list[T]: # aquires _lock
        slices = query.copy()

        skip = slices.pop('_skip', 0)
        limit = slices.pop('_limit', None)
        order_by = slices.pop('_order_by', None)
        order_desc = slices.pop('_order_desc', False)

        if type(skip) is not int or skip < 0:
            raise ValueError(f"_skip must be a non-negative integer, got {skip!r}")

        if limit is not None and (type(limit) is not int or limit < 0):
            raise ValueError(f"_limit must be a non-negative integer, got {limit!r}")

        if type(order_desc) is not bool:
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
            rows.sort(key=key, reverse=order_desc) # type: ignore
        elif self._fulltext.isdisjoint(slices):
            rows.sort(key=lambda row: row['id'], reverse=order_desc) # type: ignore

        stop = None if limit is None else skip + limit

        return [
            self._dump2model(row)
            for row in islice(rows, skip, stop)
        ]

    @overload
    def create(self, instance: T, /) -> T: ...
    @overload
    def create(self, /, **kwargs: Any) -> T: ...
    def create(self, instance: T | None = None, /, **kwargs: Any) -> T:
        dump = self._model2dump(instance, 'python') if instance is not None else kwargs
        return self._upsert(dump, True, False)

    @overload
    def update(self, instance: T, /) -> T: ...
    @overload
    def update(self, /, **kwargs: Any) -> T: ...
    def update(self, instance: T | None = None, /, **kwargs: Any) -> T:
        dump = self._model2dump(instance, 'python') if instance is not None else kwargs
        return self._upsert(dump, False, True)

    def upsert(self, instance: T) -> T:
        return self._upsert(self._model2dump(instance, 'python'), True, True)

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

    def delete_all(self) -> None:
        self._delete_all()
