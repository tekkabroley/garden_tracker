import json
import os

from gsheets import Sheets

from gsheets_extraction_tools import map_raw_data_to_columns, map_columnar_data_to_records
from validation import validate_num_rows_is_equal


# path to google sheets api client secrets
secrets = "client_secret.json"

# local storage location for access keys and tokens
sheets = Sheets.from_files(secrets, '~/storage.json')

# garden tracker main spreadsheet url
url = os.environ["sheet_url"]

# create sheets object from spreadsheet found at url
s = sheets.get(url)

# get sheet column parameters
sheet_column_parameters_path = "gsheet_column_parameters.json"
with open(sheet_column_parameters_path, 'r') as column_params:
    sheet_column_parameters = json.load(column_params)

# fetch inventory data
inventory = s.find("Inventory")
inventory_column_parameters = sheet_column_parameters["Inventory"]
inventory_columns = inventory_column_parameters["columns"]
inventory_is_column_name_included = inventory_column_parameters["is_column_name_included"]
inventory_start_row = inventory_column_parameters["start_row"]

# extract from inventory sheet
inventory_columnar_data = map_raw_data_to_columns(inventory, inventory_start_row, inventory_is_column_name_included,
                                                  inventory_columns)

# validate that all columns have the same number of rows
inventory_columns_have_equal_num_rows = validate_num_rows_is_equal(inventory_columnar_data)

if inventory_columns_have_equal_num_rows is False:
    raise ValueError("not all columns have the same number of rows in inventory_columnar_data")

# map inventory columnar data to records
inventory_records = map_columnar_data_to_records(inventory_columnar_data)
for row in inventory_records:
    print(row)



