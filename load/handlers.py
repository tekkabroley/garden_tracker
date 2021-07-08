from .models.Inventory import Inventory
from .models.Location import Location
from .models.Run import Run


# Add logging for execptions

def inventory_handler(record):
    name = record["Marketing Name"].strip().lower()
    try:
        spacing = float(record["Plant Spacing"])
    except ValueError:
        return

    try:
        single_planting_max = int(record["Max Single Planting"])
    except ValueError:
        single_planting_max = None

    try:
        dtm = int(record["DTM"])
    except ValueError:
        return

    try:
        md = int(record["MD"])
    except ValueError:
        return

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
        return

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
        return

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