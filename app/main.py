from dotenv import load_dotenv

# reads configuration from .env file,
# sets `os.environ` variables that can be used later
load_dotenv(".env")
load_dotenv(".env.dev", override=True)

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app import app  # noqa:E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n\n" + "-" * 10 + "init() status" + "-" * 10)
    print(
        f".env file found: {'YES' if Path('.env').exists() else 'NO!!! missing env!'}"
    )

    data_dir_env = os.getenv("DATA_DIR")
    print(f"value of 'data_dir': {data_dir_env or 'NOT SET'}")

    if data_dir_env:
        data_path = Path(data_dir_env)
        print(
            f"the supposed location: {data_path.resolve()} ({'exists' if data_path.exists() else 'MISSING!'})"
        )
    else:
        print(f"data directory: unresolved")
    print("-" * 10 + "init() finish;" + "-" * 9 + "\n")
    yield


app.router.lifespan_context = lifespan
