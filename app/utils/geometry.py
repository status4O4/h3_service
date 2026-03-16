import math

import h3
from shapely.geometry import Polygon, box


def parse_polygon(border: str) -> Polygon:
    coords = []

    for p in border.split(","):
        lat, lon = map(float, p.split("/"))
        coords.append((lon, lat))
    return Polygon(coords)


def compute_ring_size(radius_km: float, resolution: int) -> int:
    edge = h3.average_hexagon_edge_length(resolution, unit="km")
    hex_spacing = edge * 2 / math.sqrt(3)
    n = math.ceil(radius_km / hex_spacing)
    return n


def create_bbox(c_lon: float, c_lat: float, radius_km: float) -> Polygon:
    return box(
        c_lon - radius_km / 111,
        c_lat - radius_km / 111,
        c_lon + radius_km / 111,
        c_lat + radius_km / 111,
    )
