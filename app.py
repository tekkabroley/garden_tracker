from extract.job import main as run_extract
from load.job import main as run_load
from cli import main as run_cli
from transform.filter.apply_inventory_filters import main as apply_inventory_filters
from transform.filter.apply_run_filters import main as apply_run_filters
from transform.calcs import location_available_area, inventory_recommendations
from view import print_recommendations



def main():
    user_input = run_cli()
    target_location = user_input["target_location"]
    target_date = user_input["target_date"]

    print("----- extracting data from google sheets -----")
    raw_data = run_extract()

    print("\n----- building data objects from raw data -----")
    data_objs = run_load(**raw_data)
    locations = data_objs["Location"]
    inventory_all = data_objs["Inventory"]

    print("\n----- applying filters -----")
    location = locations[target_location]
    inventory = apply_inventory_filters(location.sun_constraint, target_date, inventory_all)
    runs = apply_run_filters(location.name, data_objs["Run"])

    print("\n----- calculating recommendations -----\n")
    location_available_area_map = location_available_area(target_date, inventory_all, location, runs)
    recommendations = inventory_recommendations(target_date, location_available_area_map, inventory)

    print_recommendations(target_location, target_date, recommendations)

    print("\n----- completed -----")


if __name__ == "__main__":
    main()