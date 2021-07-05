from pydantic import BaseModel

'''
Inventory columns: dict_keys(['Marketing Name', 'Plant Spacing', 'Max Single Planting', 'Sun', 'DTM', 'MD', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Archived'])



'''
class Inventory(BaseModel):
    name: str
    #required_duration: int
    #required_area: float
    spacing: float = None
    single_planting_max: int
    sun_constraint: str
    dtm: int = None
    md: int = None
    seasonality: set
    is_active: bool
