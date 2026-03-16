from loguru import logger
from app.config import settings
import sys


def setup_logger() -> None:
    logger.remove()

    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT_STDOUT,
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )

    logger.add(
        settings.LOG_FILE_PATH,
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        compression=settings.LOG_COMPRESSION,
        level=settings.LOG_LEVEL,
    )
