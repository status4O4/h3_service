from typing import List, Tuple

from pydantic import RootModel

HexItem = Tuple[str, int, int]


class BaseHexResponse(RootModel[List[HexItem]]):
    pass


class HexResponse(BaseHexResponse):
    pass


class AvgResponse(BaseHexResponse):
    pass


class BboxResponse(BaseHexResponse):
    pass
