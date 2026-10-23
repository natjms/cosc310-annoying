def coerce_empty_string_to_none(value: str) -> str:
	"""
	This validator is used to sanitize HTML forms which will include inputs
	without a value as an empty string; a techncially valid value for many
	models may be invalid in business logic
	"""
	return value if value != '' else None

def nonempty_string(value: str) -> str:
	if value == '':
		raise ValueError('Required text field cannot be empty')
	return value

def positive_float(value: float) -> float:
	if value < 0:
		raise ValueError('Given numeric value must not be less than zero')
	return value
