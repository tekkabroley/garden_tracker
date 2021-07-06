from pydantic import BaseModel


class Inventory(BaseModel):
    name: str
    spacing: float
    single_planting_max: int = None
    sun_constraint: str
    dtm: int
    md: int
    seasonality: set
    is_active: bool

    def required_duration(self):
        return self.dtm + self.md

    def required_area(self):
        return self.spacing ** 2
