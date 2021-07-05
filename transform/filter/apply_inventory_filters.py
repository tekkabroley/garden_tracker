import transform.filter.filters as filters


def main(location_sun_constraint, target_date, inventory):
    inventory1 = filters.filter_inventory_active(inventory)
    inventory2 = filters.filter_inventory_seasonality(inventory1, target_date)
    inventory3 = filters.filter_inventory_sun_constraint(inventory2, location_sun_constraint)
    return inventory3


if __name__ == "__main__":
    main()