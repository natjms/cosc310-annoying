"""
A generic exception to be raised by when the user expected something but
nothing was found. For example, if the user requested a restaurant by ID and
the ID is valid, but no such restaurant exists.
"""
class MissingValueException(Exception):
	def __init__(self, message):
		super().__init__(self, message)

		# NOTE: if the message property is not explicitly declared here, the
		# Python interpreter may complain that MissingValueException does not
		# have such a property
		self.message = message

"""
An exception that indicates something conflicts with something else. For example,
only one user can have a given username. If you attempt to create a second user
with the same username, that may be well described by this exception
"""
class ResourceConflictException(Exception):
	def __init__(self, message):
		super().__init__(self, message)
		self.message = message
