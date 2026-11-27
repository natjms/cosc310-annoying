from dotenv import load_dotenv

# reads configuration from .env file,
# sets `os.environ` variables that can be used later
load_dotenv(".env")
load_dotenv(".env.dev", override=True)


# e402 is for module imports at the top;
# they must stay this way for this file however.

import os  # noqa:E402
from contextlib import asynccontextmanager  # noqa:E402
from pathlib import Path  # noqa:E402

from fastapi import FastAPI  # noqa:E402

from app import app  # noqa:E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n\n" + "-" * 10 + "init() status" + "-" * 10)
    print(
        f".env file found: {'YES' if Path('.env').exists() else 'NO!!! missing env!'}"  # noqa:E501,ASYNC240
    )

    data_dir_env = os.getenv("DATA_DIR")
    print(f"value of 'data_dir': {data_dir_env or 'NOT SET'}")

    if data_dir_env:
        data_path = Path(data_dir_env)
        print(
            f"the supposed location: {data_path.resolve()} ({'exists' if data_path.exists() else 'MISSING!'})"  # noqa:E501,ASYNC240
            # e501 is for line too long, async240 is since the path call is blocking
        )
    else:
        print(f"data directory: unresolved")
    print("-" * 10 + "init() finish;" + "-" * 9 + "\n")
    yield


app.router.lifespan_context = lifespan
