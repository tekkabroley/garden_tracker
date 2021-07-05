from extract.job import main as run_extract
from load.job import main as run_load
from cli import main as run_cli
from transform.filter.apply_inventory_filters import main as apply_inventory_filters
from transform.filter.apply_run_filters import main as apply_run_filters



def main():
    user_input = run_cli()
    target_location = user_input["target_location"]
    target_date = user_input["target_date"]

    print("----- extracting data from google sheets -----")
    raw_data = run_extract()

    print("----- building data objects from raw data -----")
    data_objs = run_load(**raw_data)
    locations = data_objs["Location"]

    print("----- applying filters -----")
    location = locations[target_location]
    inventory = apply_inventory_filters(location.sun_constraint, target_date, data_objs["Inventory"])
    runs = apply_run_filters(location.name, data_objs["Run"])

    print("----- completed -----")



if __name__ == "__main__":
    main()