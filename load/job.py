from .handlers import inventory_handler, location_handler, run_handler

import logging
logging.basicConfig(filename="execution.log", filemode="w", format='%(asctime)s %(message)s', level=logging.DEBUG)
logger = logging.info


def main(**raw_data_records):
    # add support for storing raw data in csv
    inventory = {}
    inventory_records = raw_data_records["Inventory"]
    for record in inventory_records:
        inventory_obj = inventory_handler(record, logger)
        if inventory_obj is None:
            logger(f"caught invalid Inventory record: {record} | {inventory_obj}")
            continue
        inventory_name = inventory_obj.name
        inventory[inventory_name] = inventory_obj

    locations = {}
    locations_records = raw_data_records["Location"]
    for record in locations_records:
        location_obj = location_handler(record, logger)
        if location_obj is None:
            logger(f"caught invalid Location record: {record} | {location_obj}")
            continue
        location_name = location_obj.name
        locations[location_name] = location_obj

    runs = []
    run_records = raw_data_records["Run"]
    for record in run_records:
        run_obj = run_handler(record, logger)
        if run_obj is None:
            logger(f"caught invalid Run record: {record} | {run_obj}")
            continue
        runs.append(run_obj)

    return {"Inventory": inventory, "Location": locations, "Run": runs}


if __name__ == "__main__":
    main()