from .models.Inventory import Inventory
from .models.Location import Location
from .models.Run import Run

from datetime import datetime


def inventory_handler(record, logger):
    name = record["Marketing Name"].strip().lower()
    try:
        spacing = float(record["Plant Spacing"])
        single_planting_max = int(record["Max Single Planting"])
        dtm = int(record["DTM"])
        md = int(record["MD"])
    except KeyError as ke:
        logger(f"KeyError {ke} | {record}")
        return
    except ValueError as ve:
        logger(f"ValueError {ve} | {record}")
        return

    # build set of months which are in season for inventory item
    month_abbreviations = {"mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb"}
    seasonality = {key.strip().lower() for key in record if key.strip().lower() in month_abbreviations
                   and record.get(key, "") != ""}

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


def location_handler(record, logger):
    try:
        name = record["name"].strip().lower()
        sun_constraint = record["sun"].strip().lower()
        total_area = float(record.get("Aval Area", 0))
    except KeyError as ke:
        logger(f"KeyError {ke} | {record}")
        return
    except ValueError as ve:
        logger(f"ValueError {ve} | {record}")
        return

    return Location(
        name=name,
        sun_constraint=sun_constraint,
        total_area=total_area
    )


def run_handler(record, logger):
    try:
        location_name = record["OD Location"].strip().lower()
        inventory_name = record["Marketing Name"].strip().lower()
        inventory_planted_cnt = int(record.get("Current Qty", 0))

        start_date = record["Sown RPT"].strip()
        datetime.strptime(start_date, "%Y-%m-%d")  # validate that start_date is formatted correctly

        end_date = record["Harvest End RPT"].strip()
        datetime.strptime(end_date, "%Y-%m-%d")  # validate that end_date is formatted correctly
    except KeyError as ke:
        logger(f"KeyError {ke} | {record}")
        return
    except ValueError as ve:
        logger(f"ValueError {ve} | {record}")
        return

    is_active = record.get("Archive?", "") == ""
    return Run(
        location_name=location_name,
        inventory_name=inventory_name,
        inventory_planted_cnt=inventory_planted_cnt,
        start_date=start_date,
        end_date=end_date,
        is_active=is_active
    )