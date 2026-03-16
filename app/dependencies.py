import h3
from fastapi import HTTPException, Query

from app.infrastructure.uow import UnitOfWork
from app.services.hex_service import HexService


async def get_hex_service() -> HexService:
    return HexService(UnitOfWork())


async def validate_hex(
    parent_hex: str = Query(
        ..., description="Индекс гексагона. Пример: '8a11aa648367fff'"
    ),
) -> str:
    try:
        h3.get_resolution(parent_hex)
        return parent_hex
    except ValueError:
        raise HTTPException(
            status_code=400, detail=f"'{parent_hex}' - не валидный H3 индекс"
        )


async def validate_border(
    border: str = Query(
        ...,
        description="Массив координат lat/lon разделенных запятыми. Пример: '56.0027/38,55.9973/38.0,56/37.9952'",
    ),
):
    pairs = border.split(",")
    if len(pairs) < 3:
        raise HTTPException(
            status_code=400, detail="Полигон должен содержать минимум 3 точки"
        )
    for pair in pairs:
        try:
            lat_str, lon_str = pair.split("/")
            lat = float(lat_str)
            lon = float(lon_str)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Неверный формат координат: {pair}. Должно быть lat/lon",
            )
        if not (-90 <= lat <= 90):
            raise HTTPException(
                status_code=400, detail=f"Широта {lat} вне диапазона [-90, 90]"
            )
        if not (-180 <= lon <= 180):
            raise HTTPException(
                status_code=400, detail=f"Долгота {lon} вне диапазона [-180, 180]"
            )
    return border
