from functools import lru_cache

import h3
from loguru import logger

from app.config import settings
from app.domain.models import HexRecord
from app.utils.geometry import compute_ring_size


@lru_cache(maxsize=1)
def generate_dataset() -> tuple[HexRecord, ...]:
    logger.info(
        "Начало генерации датасета | center=({}, {}) | resolution={} | radius={}km",
        settings.CENTER_LAT,
        settings.CENTER_LON,
        settings.DATASET_RESOLUTION,
        settings.RADIUS_KM,
    )

    center = h3.latlng_to_cell(
        settings.CENTER_LAT,
        settings.CENTER_LON,
        settings.DATASET_RESOLUTION,
    )

    max_ring_size = compute_ring_size(settings.RADIUS_KM, settings.DATASET_RESOLUTION)
    cells = h3.grid_disk(center, max_ring_size)

    logger.debug("Получено {} ячеек из grid_disk", len(cells))

    dataset: list[HexRecord] = []
    skipped = 0

    for cell in cells:
        lat, lon = h3.cell_to_latlng(cell)

        distance = h3.great_circle_distance(
            (settings.CENTER_LAT, settings.CENTER_LON),
            (lat, lon),
            unit="km",
        )

        if distance > settings.RADIUS_KM:
            skipped += 1
            continue

        h3_int = h3.str_to_int(cell)

        level = ((h3_int // 512) % 74) - 120
        level = max(-120, min(level, -47))

        cell_id = ((h3_int // 512) % 100) + 1
        cell_id = max(1, min(cell_id, 100))

        dataset.append(
            HexRecord(
                h3_index=cell,
                level=level,
                cell_id=cell_id,
            )
        )

    logger.info(
        "Датасет сгенерирован | итоговых={} | отброшено={}",
        len(dataset),
        skipped,
    )

    return tuple(dataset)
