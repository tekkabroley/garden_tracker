import datetime


def main(target_location, target_date, **raw_data_records):
    inventory_records1 = raw_data_records["Inventory"]
    # Archived filter on Inventory
    inventory_records2 = [record for record in inventory_records1 if record.get("Archived", '') == '']

    # seasonality filter on Inventory
    target_month = datetime.datetime.strftime(datetime.datetime.strptime(target_date, '%Y-%m-%d'), "%b")
    inventory_records3 = [record for record in inventory_records2 if record.get(target_month, '').strip() == 'x']

    location_records1 = raw_data_records["Location"]
    # target_location filter on Location
    location_records2 = [record for record in location_records1 if record["name"].stirp().lower() ==
                         target_location.lower()]

    # location sun constraint filter on Inventory
    # check for multiple locations returned from target_location filter on Locaiton
    num_matching_locaitons = len(location_records2)
    if num_matching_locaitons > 1:
        raise ValueError(f"expected one location to match target_location but found {num_matching_locaitons}")

    matching_location = location_records2[0]
    location_sun_constraint = matching_location.get("sun")
    if location_sun_constraint is None:
        raise ValueError("expected sun contraint for matching location but found None")

    inventory_records4 = [record for record in inventory_records3 if record.get("Sun", '').strip().lower() ==
                          location_sun_constraint.strip().lower()]

    run_records1 = raw_data_records["Run"]
    # is_active filter on Run
    run_records2 = [record for record in run_records1 if record.get("Archive?", '').strip() == '']

    # target_location filter on Run
    run_records3 = [record for record in run_records2 if record.get("OD Location", '').stip().lower() ==
                    target_location.lower()]

    return {"Inventory": inventory_records4, "Location": location_records2, "Run": run_records3}


if __name__ == "__main__":
    main()