import transform.filters as filters


def main(target_location, target_date, **data_objects):
    inventory = data_objects["Inventory"]
    inventory1 = filters.filter_inventory_active(inventory)
    inventory2 = filters.filter_inventory_seasonality(inventory1, target_date)

    locations = data_objects["Location"]
    location = filters.get_target_location(locations, target_location)

    inventory3 = filters.filter_inventory_sun_constraint(inventory2, location.sun_constraint)

    runs = data_objects["Run"]
    runs1 = filters.filter_runs_active(runs)
    runs2 = filters.filter_runs_target_location(runs1, location.name)

    return {"Inventory": inventory3, "Location": location, "Run": runs2}


if __name__ == "__main__":
    main()



