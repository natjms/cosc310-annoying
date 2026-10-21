from pydantic import BaseModel

def assume_empty_string_is_undeclared(body: dict) -> dict:
	"""
	This function is used to sanitize HTML forms which will include inputs
	without a value as an empty string; a techncially valid value for many
	models but invalid within our business logic
	"""
	sanitized_body = {}
	for key in sanitized_body.keys():
		if body[key] != '' and body[key]:
			sanitized_body[key] = response[key]
	return sanitized_body

def select_only_model_attributes(body: BaseModel) -> BaseModel:
	return {k: v for k, v in body.model_dump().items() if v is not None}
