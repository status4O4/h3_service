from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    CENTER_LAT: float = 56.0
    CENTER_LON: float = 38.0

    RADIUS_KM: float = 7.0

    DATASET_RESOLUTION: int = 12

    LEVEL_MOD: int = 74
    LEVEL_OFFSET: int = -120

    CELL_ID_MOD: int = 100
    CELL_ID_OFFSET: int = 1

    LOG_LEVEL: str = "DEBUG"
    LOG_FORMAT_STDOUT: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    LOG_FILE_PATH: Path = Path("logs/app.log")
    LOG_ROTATION: str = "10 MB"
    LOG_RETENTION: str = "10 days"
    LOG_COMPRESSION: str = "zip"


settings = Settings()
