from pydantic import BaseModel

'''
Runs columns: dict_keys(['Marketing Name', 'OD Location', 'Current Qty', 'Sown RPT', 'Harvest End RPT', 'Archive?'])
'''

class Run(BaseModel):
    location_name: str
    inventory_name: str
    inventory_planted_cnt: int
    start_date: str
    end_date: str
    is_active: bool
