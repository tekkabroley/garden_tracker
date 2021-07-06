from pydantic import BaseModel


class Location(BaseModel):
    name: str
    sun_constraint: str
    total_area: float
