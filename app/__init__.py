from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .exceptions import MissingValueException
from .api.routes import api_router
from .api.routes.health import router as health_router


"""
A basic Pydantic model corresponding to an error response with a message
"""
class ErrorResponse(BaseModel):
	message: str

app = FastAPI()
app.include_router(health_router)

app.mount('/web', StaticFiles(directory='web/', html=True), name='web')
app.include_router(api_router)

@app.exception_handler(MissingValueException)
def missing_value_handler(_request: Request, e: MissingValueException) -> ErrorResponse:
	return JSONResponse(
		status_code=404,
		content={ 'message': e.message }
	)
