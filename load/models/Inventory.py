from pydantic import BaseModel


class Inventory(BaseModel):
    name: str
    required_duration: int
    required_area: float
    single_planting_max: int
