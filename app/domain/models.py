from pydantic import BaseModel, Field


class HexRecord(BaseModel):
    h3_index: str = Field(..., description="H3 index")
    level: int = Field(..., ge=-120, le=-47)
    cell_id: int = Field(..., ge=1, le=100)

    def to_list(self):
        return [self.h3_index, self.level, self.cell_id]
