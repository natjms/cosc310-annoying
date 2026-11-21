from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .exceptions import MissingValueError
from .routes import router

"""
A basic Pydantic model corresponding to an error response with a message
"""


class ErrorResponse(BaseModel):
    message: str


app = FastAPI()

app.mount("/web", StaticFiles(directory="web/", html=True), name="web")
app.include_router(router)


@app.exception_handler(MissingValueError)
def missing_value_handler(_request: Request, e: MissingValueError) -> ErrorResponse:
    return JSONResponse(status_code=404, content={"message": e.message})
