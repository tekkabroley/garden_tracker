from .models.Inventory import Inventory
from .models.Location import Location
from .models.Run import Run


def inventory_handler(record):
    name = record["Marketing Name"].strip()
    spacing = float(record["Plant Spacing"])
    required_area = spacing ** 2
    single_planting_max = int(record["Max Single Planting"])
    required_duration = int(record["DTM"]) + int(record["MD"])
    return Inventory(
        name=name,
        required_duration=required_duration,
        required_area=required_area,
        single_planting_max=single_planting_max
    )


def location_handler(record):
    name = record["name"].strip()
    sun_constraint = record["sun"].strip()
    total_area = float(record["Aval Area"])
    return Location(
        name=name,
        sun_constraint=sun_constraint,
        total_area=total_area
    )


def run_handler(record):
    location_name = record["OD Location"].strip()
    inventory_name = record["Marketing Name"].strip()
    inventory_planted_cnt = int(record["Current Qty"])
    start_date = record["Sown RPT"].strip()
    end_date = record["Harvest End RPT"].strip()
    return Run(
        location_name=location_name,
        inventory_name=inventory_name,
        inventory_planted_cnt=inventory_planted_cnt,
        start_date=start_date,
        end_date=end_date
    )