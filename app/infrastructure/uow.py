from loguru import logger

from app.infrastructure.dataset import generate_dataset
from app.infrastructure.repository import HexRepository


class UnitOfWork:
    _instance = None
    _dataset = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            logger.info("UnitOfWork создаётся впервые")
        else:
            logger.info("UnitOfWork возвращается из кэша (singleton)")
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return

        if self._dataset is None:
            self._dataset = generate_dataset()
            logger.info("Dataset сгенерирован для UnitOfWork")

        self.hex_repo = HexRepository(self._dataset)
        self._initialized = True
        logger.info("UnitOfWork инициализирован с HexRepository")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass
