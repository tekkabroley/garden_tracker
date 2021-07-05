from pydantic import BaseModel

'''
Locations columns: dict_keys(['name', 'sun', 'Aval Area'])



'''
class Location(BaseModel):
    name: str
    sun_constraint: str
    total_area: float
