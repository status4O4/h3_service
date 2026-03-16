from loguru import logger

from app.config import settings
from app.utils.geometry import parse_polygon, create_bbox


class HexService:
    def __init__(self, uow):
        self.uow = uow
        logger.info("HexService инициализирован")

    def get_hex(self, parent_hex):
        with self.uow as uow:
            data = uow.hex_repo.get_by_parent(parent_hex)
        logger.debug("get_hex: найдено {} ячеек для родителя {}", len(data), parent_hex)
        return [r.to_list() for r in data]

    def avg(self, resolution):
        logger.info("Вызов avg с resolution={}", resolution)
        with self.uow as uow:
            result = uow.hex_repo.aggregate_resolution(resolution)
        logger.info("Вызов avg с resolution={}", resolution)
        return result

    def bbox(self, border):
        data = self._filter_by_polygon(border)
        return [r.to_list() for r in data]

    def bbox_raw(self, border):
        return self._filter_by_polygon(border)

    def _filter_by_polygon(self, border):
        logger.info("Фильтрация по полигону с border={}", border)
        polygon = parse_polygon(border)
        logger.debug("Полигон распарсен с {} вершинами", len(polygon.exterior.coords))

        dataset_bbox = create_bbox(
            settings.CENTER_LON, settings.CENTER_LAT, settings.RADIUS_KM
        )

        if not polygon.intersects(dataset_bbox):
            logger.warning(
                "Входной полигон не пересекается с границами датасета. Возвращается пустой результат."
            )
            return []

        with self.uow as uow:
            result = uow.hex_repo.inside_polygon(polygon)

        logger.debug("Найдено {} ячеек внутри полигона", len(result))
        return result
