from collections import defaultdict

import h3
import numpy as np
from loguru import logger
from shapely.geometry import Polygon
from shapely.prepared import prep

from app.domain.models import HexRecord


class HexRepository:
    def __init__(self, dataset: tuple[HexRecord, ...]):
        self.dataset = dataset

        self._parent_cache = defaultdict(list)
        self._resolution_cache = defaultdict(list)

        logger.debug("HexRepository инициализирует _dataset_map")
        self._dataset_map = {rec.h3_index: rec for rec in dataset}

        logger.debug("HexRepository инициализирует _parent_cache")
        for rec in self.dataset:
            max_res = h3.get_resolution(rec.h3_index)
            for res in range(max_res + 1):
                parent = h3.cell_to_parent(rec.h3_index, res)
                self._parent_cache[(parent, res)].append(rec)

        logger.info("HexRepository инициализирован с {} ячейками", len(dataset))

    def get_by_parent(self, parent_hex: str) -> list[HexRecord]:
        parent_res = h3.get_resolution(parent_hex)
        logger.debug(
            "Поиск ячеек с родителем {} (resolution={})", parent_hex, parent_res
        )

        result = self._parent_cache.get((parent_hex, parent_res), [])

        logger.info("Найдено {} ячеек для родителя {}", len(result), parent_hex)
        return result

    def aggregate_resolution(self, resolution: int):
        logger.debug("Агрегация датасета до resolution={}", resolution)

        if resolution in self._resolution_cache:
            logger.info("Возвращаем результат из кэша для resolution={}", resolution)
            return self._resolution_cache[resolution]

        groups = defaultdict(list)

        for (parent, res), records in self._parent_cache.items():
            if res != resolution:
                continue
            for rec in records:
                key = (parent, rec.cell_id)
                groups[key].append(rec.level)

        logger.debug("Создано {} групп для агрегации", len(groups))

        result = []

        for (parent, cell_id), values in groups.items():
            med = int(np.median(values))
            result.append([parent, med, cell_id])

        self._resolution_cache[resolution] = result
        logger.info("Агрегация завершена, итоговых записей: {}", len(result))
        return result

    def inside_polygon(self, polygon: Polygon):
        logger.debug(
            "Фильтрация ячеек внутри полигона с {} вершинами",
            len(polygon.exterior.coords),
        )

        resolution = h3.get_resolution(self.dataset[0].h3_index)

        coords = [(lat, lon) for lon, lat in polygon.exterior.coords]
        poly = h3.LatLngPoly(coords)

        candidate_cells = set(h3.polygon_to_cells(poly, resolution))

        prepared = prep(polygon)

        result = []

        for h3_index in candidate_cells:
            rec = self._dataset_map.get(h3_index, None)
            if not rec:
                continue

            boundary = h3.cell_to_boundary(h3_index)
            hex_poly = Polygon((lon, lat) for lat, lon in boundary)

            if prepared.contains(hex_poly):
                result.append(rec)

        logger.info("Найдено {} ячеек внутри полигона", len(result))
        return result
