from pydantic import BaseModel


class Run(BaseModel):
    location_name: str
    inventory_name: str
    inventory_planted_cnt: int
    start_date: str
    end_date: str