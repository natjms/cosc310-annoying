import sys
import threading
import pytest
from pydantic import BaseModel, ValidationError
from app.repositories.repo import Id, Repo, UniqueError

class Item(BaseModel):
	id: Id
	name: str
	n: int
	tags: list[str] = []
	score: int | None = None # not indexed

@pytest.fixture
def repo():
	return Repo('items', Item, indexed_fields=['name', 'n', 'tags'], in_memory=True)

def names(items):
	return sorted(i.name for i in items)

# construction

@pytest.mark.parametrize('kwargs, error', [
	(dict(name='bad name!', model=Item, indexed_fields=[]), ValueError),
	(dict(name='items', model=dict, indexed_fields=[]), TypeError),
	(dict(name='items', model=Item, indexed_fields=['nope']), ValueError),
	(dict(name='items', model=Item, indexed_fields=['n', 'n']), ValueError),
	(dict(name='items', model=Item, indexed_fields=['id']), ValueError),
])
def test_init_rejects_bad_config(kwargs, error):
	with pytest.raises(error):
		Repo(**kwargs)

def test_init_requires_ulid_id():
	class NoId(BaseModel):
		name: str
	with pytest.raises(TypeError):
		Repo('noid', NoId, [])

# create / read

def test_create_generates_id(repo):
	item = repo.create(name='a', n=1)
	assert isinstance(item.id, Id)
	assert repo.unique(id=item.id) == item

def test_create_from_instance_keeps_id(repo):
	item = Item(id=Id(), name='a', n=1)
	assert repo.create(item).id == item.id

def test_create_duplicate_id_fails(repo):
	item = repo.create(name='a', n=1)
	with pytest.raises(ValueError):
		repo.create(item)

def test_create_invalid_data_stores_nothing(repo):
	with pytest.raises(ValidationError):
		repo.create(name='a', n='not a number')
	assert repo.select() == []

def test_create_rejects_wrong_model(repo):
	class Other(BaseModel):
		id: Id
	with pytest.raises(TypeError):
		repo.create(Other(id=Id()))

def test_returned_instances_are_copies(repo):
	item = repo.create(name='a', n=1, tags=['x'])
	item.tags.append('y')
	repo.unique(id=item.id).tags.append('z')
	assert repo.unique(id=item.id).tags == ['x']

# update / upsert

def test_update_patches_fields(repo):
	item = repo.create(name='a', n=1, tags=['x'])
	updated = repo.update(id=item.id, n=2)
	assert (updated.name, updated.n, updated.tags) == ('a', 2, ['x'])
	assert repo.unique(id=item.id) == updated

@pytest.mark.parametrize('method', ['create', 'update'])
def test_unknown_field_fails(repo, method):
	item = repo.create(name='a', n=1)
	with pytest.raises(ValueError):
		getattr(repo, method)(id=item.id, scroe=5)

def test_update_accepts_string_id(repo):
	item = repo.create(name='a', n=1)
	assert repo.update(id=str(item.id), n=2).n == 2

def test_update_moves_index_entries(repo):
	item = repo.create(name='a', n=1, tags=['x', 'y'])
	repo.update(id=item.id, name='b', tags=['y', 'z'])
	assert repo.select(name='a') == []
	assert repo.select(tags=['x']) == []
	assert names(repo.select(name='b')) == ['b']
	assert names(repo.select(tags=['y', 'z'])) == ['b']

def test_update_refreshes_unchanged_index_entries(repo):
	item = repo.create(name='a', n=1)
	repo.update(id=item.id, n=2)
	assert repo.unique(name='a').n == 2

@pytest.mark.parametrize('kwargs', [{}, {'id': Id()}, {'id': 'not-a-ulid'}])
def test_update_bad_id_fails(repo, kwargs):
	with pytest.raises(ValueError):
		repo.update(**kwargs, n=1)

def test_update_invalid_data_changes_nothing(repo):
	item = repo.create(name='a', n=1)
	with pytest.raises(ValidationError):
		repo.update(id=item.id, n='nope')
	assert repo.unique(n=1) == item

def test_upsert_creates_then_updates(repo):
	item = Item(id=Id(), name='a', n=1)
	repo.upsert(item)
	repo.upsert(item.model_copy(update={'n': 2}))
	assert [i.n for i in repo.select()] == [2]

def test_update_from_instance(repo):
	item = repo.create(name='a', n=1)
	repo.update(item.model_copy(update={'name': 'b'}))
	assert names(repo.select()) == ['b']
	with pytest.raises(ValueError):
		repo.update(Item(id=Id(), name='c', n=1))

# delete

def test_delete(repo):
	item = repo.create(name='a', n=1, tags=['x'])
	assert repo.delete(item.id) is True
	assert repo.delete(item.id) is False
	assert repo.select() == []
	assert repo.select(name='a') == []
	assert repo.select(tags=['x']) == []

@pytest.mark.parametrize('remove', [
	lambda repo, item: repo.delete(item.id),
	lambda repo, item: repo.update(id=item.id, tags=['z']),
])
def test_duplicate_list_values_leave_no_stale_index(repo, remove):
	item = repo.create(name='a', n=1, tags=['x', 'x', 'y'])
	remove(repo, item)
	assert repo.select(tags=['x']) == []
	assert repo.select(tags=['y']) == []

def test_delete_bad_id_fails(repo):
	with pytest.raises(ValueError):
		repo.delete('not-a-ulid')

# querying

@pytest.fixture
def filled(repo):
	repo.create(name='a', n=3, tags=['x', 'y'])
	repo.create(name='b', n=1, tags=['y'])
	repo.create(name='c', n=2, tags=['x', 'z'])
	repo.create(name='d', n=1)
	return repo

@pytest.mark.parametrize('query, expected', [
	({}, ['a', 'b', 'c', 'd']),
	({'n': 1}, ['b', 'd']),
	({'n': '1'}, ['b', 'd']), # query values are coerced by the field type
	({'n': 1, 'name': 'b'}, ['b']),
	({'n': 1, 'name': 'a'}, []),
	({'tags': ['x']}, ['a', 'c']),
	({'tags': ['x', 'y']}, ['a']), # list queries match rows containing all values
	({'tags': ['y', 'z']}, []),
	({'tags': ['nope']}, []),
	({'name': 'nope'}, []),
])
def test_select(filled, query, expected):
	assert names(filled.select(**query)) == expected

def test_select_by_id(filled):
	a = filled.unique(name='a')
	assert filled.select(id=a.id) == [a]
	assert filled.select(id=a.id, n=3) == [a]
	assert filled.select(id=a.id, n=1) == []
	assert filled.select(id=Id()) == []
	assert filled.select(id=str(a.id)) == [a]
	with pytest.raises(ValueError):
		filled.select(id='not-a-ulid')

@pytest.mark.parametrize('query', [{'score': 1}, {'id': Id(), 'score': 1}])
def test_select_unindexed_field_fails(filled, query):
	with pytest.raises(ValueError):
		filled.select(**query)

def test_select_invalid_value_fails(filled):
	with pytest.raises(ValidationError):
		filled.select(n='not a number')

def test_order_skip_limit(filled):
	def order(**q): return [i.name for i in filled.select(_order_by='name', **q)]
	assert order() == ['a', 'b', 'c', 'd']
	assert order(_order_desc=True) == ['d', 'c', 'b', 'a']
	assert order(_skip=1, _limit=2) == ['b', 'c']
	assert order(_skip=3, _limit=5) == ['d']
	assert order(_skip=10) == []
	assert [i.n for i in filled.select(_order_by='n')] == [1, 1, 2, 3]

def test_order_by_optional_field(filled):
	filled.update(id=filled.unique(name='a').id, score=2)
	filled.update(id=filled.unique(name='c').id, score=1)
	assert [i.score for i in filled.select(_order_by='score')] == [1, 2, None, None]
	assert [i.score for i in filled.select(_order_by='score', _order_desc=True)] == [None, None, 2, 1]

@pytest.mark.parametrize('query', [
	{'_skip': -1}, {'_limit': -1}, {'_limit': 1.5},
	{'_order_desc': 'yes'}, {'_order_by': 'nope'},
])
def test_bad_query_options_fail(filled, query):
	with pytest.raises(ValueError):
		filled.select(**query)

def test_unique(filled):
	assert filled.unique(name='a').n == 3
	with pytest.raises(UniqueError):
		filled.unique(name='nope')
	with pytest.raises(UniqueError):
		filled.unique(n=1)

# concurrency

@pytest.mark.parametrize('query', [{}, {'n': 1}, {'n': 1, 'name': 'a'}])
def test_select_during_concurrent_writes(repo, query):
	done = threading.Event()

	def churn():
		while not done.is_set():
			ids = [repo.create(name='a', n=1).id for _ in range(20)]
			for id in ids: repo.delete(id)

	old_interval = sys.getswitchinterval()
	sys.setswitchinterval(1e-6) # switch threads constantly to cause races
	writer = threading.Thread(target=churn)
	writer.start()
	try:
		for _ in range(500):
			repo.select(**query)
	finally:
		done.set()
		writer.join()
		sys.setswitchinterval(old_interval)
