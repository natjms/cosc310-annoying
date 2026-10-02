from dotenv import load_dotenv

# reads configuration from .env file,
# sets `os.environ` variables that can be used later
load_dotenv()

from fastapi import FastAPI

from .api.routes import api_router

app = FastAPI()

app.include_router(api_router)
