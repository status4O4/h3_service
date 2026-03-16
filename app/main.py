from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.api.routes import router
from app.infrastructure.uow import UnitOfWork
from app.utils.logger import setup_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    logger.info("Application started")
    UnitOfWork()
    yield

    logger.info("Application stopped")


app = FastAPI(lifespan=lifespan)

app.include_router(router)
