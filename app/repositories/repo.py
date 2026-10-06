from copy import deepcopy
from itertools import islice
from typing import Any, Hashable, Iterable, overload
from pydantic import BaseModel
from ulid import ULID

class UniqueError(Exception):
    pass

type Id = str
type Field = str
type Value = Any
type ValueKey = Hashable
type Dump = dict[Field, Value]

def generate_id() -> Id:
    return str(ULID())

def recursive_hash(obj: Any) -> int:
    try: return obj.__hash__()
    except TypeError: pass

    try:
        hash = 0
        if isinstance(obj, dict):
            for key, value in obj.items():
                hash ^= recursive_hash(key) ^ recursive_hash(value)
        else:
            for element in obj:
                hash ^= recursive_hash(element)
        return hash
    except TypeError: pass

    return id(obj)

class HashableRef:
    __slots__ = ('obj', 'hash')

    def __init__(self, obj: object):
        self.obj = obj
        self.hash = recursive_hash(obj)

    def __hash__(self) -> int:
        return self.hash

    def __eq__(self, other: object) -> bool:
        return isinstance(other, HashableRef) \
            and self.hash == other.hash \
            and self.obj == other.obj

def askey(obj: object, copy: bool = False) -> ValueKey:
    try:
        _ = obj.__hash__() << 0
        return obj
    except TypeError:
        if copy: obj = deepcopy(obj)
        return HashableRef(obj)

class Index(dict[ValueKey, dict[Id, Dump]]):
    def all(self) -> Iterable[Dump]:
        for slice in self.values():
            yield from slice.values()

    def has(self, vkey: ValueKey, id: Id | None = None) -> bool:
        return vkey in self and (id is None or id in self[vkey])

    def find(self, vkey: ValueKey, id: Id) -> Dump | None:
        return self[vkey][id] if self.has(vkey, id) else None

    def put(self, vkey: ValueKey, id: Id, item: Dump) -> None:
        if not vkey in self: self[vkey] = {}
        self[vkey][id] = item

    def remove(self, vkey: ValueKey, id: Id) -> bool:
        if not vkey in self: return False
        leaf = self[vkey]
        if not id in leaf: return False
        del leaf[id]
        if not leaf: del self[vkey]
        return True

class Repo[T: BaseModel]:
    name: str
    model: type[T]

    _id: Index
    _indicies: dict[Field, Index]

    def __init__(self, name: str, model: type[T], indexed_fields: Iterable[Field]):
        if not isinstance(name, str) or not name.isalnum() or not name:
            raise ValueError(f"name must be a non-empty alphanumeric string, got {name}")

        if not isinstance(model, type) or not issubclass(model, BaseModel):
            raise TypeError(f"model must be a subclass of BaseModel, got {model}")

        id_field = model.model_fields.get('id', None)
        if id_field is None or not (
            id_field.annotation is None or
            issubclass(id_field.annotation, str)
        ):
            raise TypeError(f"model {model.__name__} must have an 'id' field of type str")

        indexed_fields = list(indexed_fields)

        for field in indexed_fields:
            if field not in model.model_fields:
                raise ValueError(f"indexed field {field} is not a valid field of {model.__name__}")

        if len(set(indexed_fields)) != len(indexed_fields):
            raise ValueError("indexed_fields must be unique")

        if 'id' in indexed_fields:
            raise ValueError("indexed_fields must not contain 'id'")

        self.name = name
        self.model = model

        self._id = Index()
        self._indicies = {}

        for field in indexed_fields:
            self._indicies[field] = Index()

        self._indicies['id'] = self._id

    def _todump(self, instance: T) -> Dump:
        if isinstance(instance, self.model):
            return instance.model_dump(mode='json')
        else:
            raise TypeError(f"instance {instance} is not of type {self.model}")

    def _fromdump(self, dump: Dump) -> T:
        return self.model.model_validate(dump)

    def _get(self, id: Id) -> Dump | None:
        return self._id.find(id, id)

    def _upsert(self, new_dump: Dump, /, can_create: bool, can_update: bool) -> T:
        assert can_create or can_update

        id = new_dump.get('id', None)

        if not id:
            if can_create:
                id = new_dump['id'] = generate_id()
            else:
                raise ValueError("id is required, but was not set or provided")
        elif type(id) is not str:
            raise ValueError(f"id must be a string, got {id}")

        old_dump = self._get(id)

        if old_dump:
            if not can_update:
                raise ValueError(f"{self.name}.id={id} already exists, cannot create")
            for k, v in old_dump.items():
                if k not in new_dump or new_dump[k] is None:
                    new_dump[k] = v
        elif not can_create:
            raise ValueError(f"{self.name}.id={id} does not exist, cannot update")

        instance = self._fromdump(new_dump)

        if old_dump:
            for field, index in self._indicies.items():
                old_value = old_dump[field]
                new_value = new_dump[field]
                if old_value is not new_value:
                    index.remove(askey(old_value), id)
                index.put(askey(new_value, copy=True), id, new_dump)
        else:
            for field, index in self._indicies.items():
                new_value = new_dump[field]
                index.put(askey(new_value, copy=True), id, new_dump)

        return instance

    def _delete(self, id: Id) -> bool:
        dump = self._get(id)
        if not dump: return False

        for field, index in self._indicies.items():
            value = dump[field]
            index.remove(askey(value), id)

        return True

    def _index_slice(self, field: Field, value: Value) -> dict[Id, Dump] | None:
        return self._indicies[field].get(askey(value), None)

    def _query_rows(self, filters: dict[Field, Value]) -> Iterable[Dump]:
        for field in filters:
            if field not in self._indicies:
                raise ValueError(f"field {self.name}.{field} is not indexed")

        if not filters:
            return self._id.all()

        filters_iter = iter(filters.items())

        first_field, first_value = next(filters_iter)
        first_slice = self._index_slice(first_field, first_value)

        if first_slice is None:
            return ()

        if len(filters) == 1:
            return first_slice.values()

        matching_ids = set(first_slice)

        for field, value in filters_iter:
            slice = self._index_slice(field, value)
            if slice is None: return ()
            matching_ids.intersection_update(slice)

        return (
            dump
            for id, dump in first_slice.items()
            if id in matching_ids
        )

    def _query(self, query: dict[str, Any]) -> list[T]:
        # don't mutate the caller's query
        filters = query.copy()

        skip = filters.pop('_skip', 0)
        limit = filters.pop('_limit', None)
        order_by = filters.pop('_order_by', None)
        order_desc = filters.pop('_order_desc', False)

        if type(skip) is not int or skip < 0:
            raise ValueError(f"_skip must be a non-negative integer, got {skip}")

        if limit is not None and (type(limit) is not int or limit < 0):
            raise ValueError(f"_limit must be a non-negative integer or None, got {limit}")

        if type(order_desc) is not bool:
            raise ValueError(f"_order_desc must be a boolean, got {order_desc}")

        if order_by is not None and (
            not isinstance(order_by, str)
            or order_by not in self.model.model_fields
        ):
            raise ValueError(f"_order_by must be a field on {self.model.__name__}, got {order_by}")

        rows = self._query_rows(filters)

        if order_by is not None:
            rows = sorted(
                rows,
                key=lambda row: row[order_by],
                reverse=order_desc,
            )

        stop = None if limit is None else skip + limit

        return [
            self._fromdump(row)
            for row in islice(rows, skip, stop)
        ]

    @overload
    def create(self, instance: T, /) -> T: ...
    @overload
    def create(self, /, **kwargs: Any) -> T: ...
    def create(self, instance: T | None = None, /, **kwargs: Any) -> T:
        dump = self._todump(instance) if instance is not None else kwargs
        return self._upsert(dump, True, False)

    @overload
    def update(self, instance: T, /) -> T: ...
    @overload
    def update(self, /, **kwargs: Any) -> T: ...
    def update(self, instance: T | None = None, /, **kwargs: Any) -> T:
        dump = self._todump(instance) if instance is not None else kwargs
        return self._upsert(dump, False, True)

    def upsert(self, instance: T) -> T:
        return self._upsert(self._todump(instance), True, True)

    def delete(self, id: Id) -> bool:
        return self._delete(id)

    def select(self, /, **query: Any) -> list[T]:
        return self._query(query)

    def unique(self, /, **query: Any) -> T:
        results = self._query(query)
        if len(results) < 1:
            raise UniqueError(f"no result found in {self.name} for query: {query}")
        if len(results) > 1:
            raise UniqueError(f"multiple results found in {self.name} for query: {query}")
        return results[0]

class User(BaseModel):
    id: str
    name: str
    age: int
    friends: list[str]

repo = Repo('users', User, ['name', 'age', 'friends'])

lua = repo.create(name='Lua', age=21, friends=['Iris', 'Jo'])
jo = repo.create(id='jo', name='Jo', age=23, friends=['Lua', 'Iris'])
iris = User(id='iris', name='Iris', age=21, friends=['Jo', 'Lua'])

repo.create(iris)
repo.update(id=lua.id, age=22)

for user in repo.select():
    print(user)

print("this user is 22:", repo.select(age=22))
print("this user is friends with jo and lua:", repo.select(friends=['Jo', 'Lua']))
