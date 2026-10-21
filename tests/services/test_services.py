import app.services as services

def test_empty_string_constraint():
	example_body = {'a': 1, 'b': ''}
	sanitized_body = services.assume_empty_string_is_undeclared(example_body)
	assert 'b' not in sanitized_body
