from extract.job import main as run_extract
from load.job import main as run_load
from cli import main as run_cli
from transform.apply_filters import main as run_filters



def main():
    user_input = run_cli()
    target_location = user_input["target_location"]
    target_date = user_input["target_date"]

    print("----- extracting data from google sheets -----")
    raw_data = run_extract()

    print("----- building data objects from raw data -----")
    data_objs = run_load(**raw_data)

    print("----- applying filters -----")
    filtered_objs = run_filters(target_location, target_date, **data_objs)

    print("----- completed -----")



if __name__ == "__main__":
    main()