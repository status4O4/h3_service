from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response

from app.api.schemas import HexResponse, AvgResponse, BboxResponse
from app.dependencies import get_hex_service, validate_border, validate_hex
from app.utils.kml import generate_kml

router = APIRouter()


@router.get("/hex", response_model=HexResponse)
async def hex_endpoint(
    parent_hex: str = Depends(validate_hex), service=Depends(get_hex_service)
):
    return service.get_hex(parent_hex)


@router.get("/avg", response_model=AvgResponse)
async def avg_endpoint(
    resolution: int = Query(..., ge=0, le=12, description="H3 разрешение от 0 до 12"),
    service=Depends(get_hex_service),
):
    return service.avg(resolution)


@router.get("/bbox", response_model=BboxResponse)
async def bbox_endpoint(
    border: str = Depends(validate_border), service=Depends(get_hex_service)
):
    return service.bbox(border)


@router.get("/bbox_kml")
async def bbox_kml(
    border: str = Depends(validate_border), service=Depends(get_hex_service)
):
    records = service.bbox_raw(border)

    kml = generate_kml(records)

    return Response(
        content=kml,
        media_type="application/vnd.google-earth.kml+xml",
        headers={"Content-Disposition": "attachment; filename=hexagons.kml"},
    )
