from .handlers import inventory_handler, location_handler, run_handler


def main(**raw_data_records):
    # add support for storing raw data in csv
    # Create list of Ivnetory objects
    inventory = {}
    inventory_records = raw_data_records["Inventory"]
    for record in inventory_records:
        inventory_obj = inventory_handler(record)
        if inventory_obj is None:
            continue
        inventory_name = inventory_obj.name
        inventory[inventory_name] = inventory_obj

    locations = {}
    locations_records = raw_data_records["Location"]
    for record in locations_records:
        location_obj = location_handler(record)
        if location_obj is None:
            continue
        location_name = location_obj.name
        locations[location_name] = location_obj

    runs = []
    run_records = raw_data_records["Run"]
    for record in run_records:
        run_obj = run_handler(record)
        if run_obj is None:
            continue
        runs.append(run_obj)

    return {"Inventory": inventory, "Location": locations, "Run": runs}


if __name__ == "__main__":
    main()