from datetime import datetime

from .models.Inventory import Inventory
from .models.Location import Location
from .models.Run import Run


def inventory_handler(record):
    name = record["Marketing Name"].strip()
    try:
        spacing = float(record["Plant Spacing"])
    except ValueError:
        spacing = None

    try:
        single_planting_max = int(record["Max Single Planting"])
    except ValueError:
        # if no single_planting_max found then use 0
        single_planting_max = 0

    try:
        dtm = int(record["DTM"])
    except ValueError:
        dtm = None

    try:
        md = int(record["MD"])
    except ValueError:
        md = None

    # build set of months which are in season for inventory item
    month_abbreviations = {"mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb"}
    seasonality = {key.lower() for key in record if key.lower() in month_abbreviations and record.get(key, "") != ""}

    sun_constraint = record["Sun"].strip().lower()
    is_active = record.get("Archived", "") == ""
    return Inventory(
        name=name,
        spacing=spacing,
        single_planting_max=single_planting_max,
        dtm=dtm,
        md=md,
        seasonality=seasonality,
        sun_constraint=sun_constraint,
        is_active=is_active
    )


def location_handler(record):
    name = record["name"].strip().lower()
    sun_constraint = record["sun"].strip().lower()
    try:
        total_area = float(record.get("Aval Area", 0))
    except ValueError:
        # if no total_area found then use 0
        total_area = 0

    return Location(
        name=name,
        sun_constraint=sun_constraint,
        total_area=total_area
    )


def run_handler(record):
    location_name = record.get("OD Location", "").strip().lower()
    inventory_name = record["Marketing Name"].strip().lower()

    try:
        inventory_planted_cnt = int(record.get("Current Qty", 0))
    except ValueError:
        inventory_planted_cnt = 0

    #start_date = datetime.datetime.strptime(record["Sown RPT"].strip(), "%Y-%m-%d")
    #end_date = datetime.datetime.strptime(record["Harvest End RPT"].strip(), "%Y-%m-%d")
    start_date = record["Sown RPT"].strip()
    end_date = record["Harvest End RPT"].strip()
    is_active = record.get("Archive?", "") == ""
    return Run(
        location_name=location_name,
        inventory_name=inventory_name,
        inventory_planted_cnt=inventory_planted_cnt,
        start_date=start_date,
        end_date=end_date,
        is_active=is_active
    )