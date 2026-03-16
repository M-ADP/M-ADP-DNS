import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import api_router as router
from src.common.config.settings import get_app_config, load_all_configs
from src.core.db import create_all_tables
from src.core.exceptions import register_exception_handlers

logging.basicConfig(level=logging.INFO)

load_all_configs()
config = get_app_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield


app = FastAPI(
    title=config.app_name,
    version=config.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors.allow_origins,
    allow_methods=config.cors.allow_methods,
    allow_credentials=config.cors.allow_credentials,
    allow_headers=config.cors.allow_headers,
)

register_exception_handlers(app)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8001, reload=True, reload_excludes=[".venv"])
