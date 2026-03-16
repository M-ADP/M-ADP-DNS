import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import router
from src.common.config.settings import get_app_config, load_all_configs
from src.core.db import create_all_tables
from src.core.exceptions import register_exception_handlers

logging.basicConfig(level=logging.INFO)

load_all_configs()
config = get_app_config()

app = FastAPI(
    title=config.app_name,
    version=config.app_version,
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


@app.on_event("startup")
async def on_startup() -> None:
    await create_all_tables()
