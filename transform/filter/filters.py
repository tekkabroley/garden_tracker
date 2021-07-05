from datetime import datetime


def filter_inventory_active(inventory):
    # Archived filter on Inventory
    inventory_ = {plant_name: model for plant_name, model in inventory.items() if model.is_active}
    return inventory_


def filter_inventory_seasonality(inventory, target_date):
    # seasonality filter on Inventory
    target_month = datetime.strftime(datetime.strptime(target_date, '%Y-%m-%d'), "%b").lower()
    inventory_ = {plant_name: model for plant_name, model in inventory.items() if target_month in model.seasonality}
    return inventory_


def get_target_location(locations, target_location):
    location = locations[target_location]
    return location


def filter_inventory_sun_constraint(inventory, location_sun_constraint):
    inventory_ = {plant_name: model for plant_name, model in inventory.items()
                  if model.sun_constraint == location_sun_constraint}
    return inventory_


def filter_runs_active(runs):
    # is_active filter on Run
    runs_ = [run for run in runs if run.is_active]
    return runs_


def filter_runs_target_location(runs, target_location):
    # target_location filter on Run
    runs_ = [run for run in runs if run.location_name == target_location]
    return runs_
