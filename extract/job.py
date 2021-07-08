from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import json

# add support for storing raw data in csv
# import datetime
# from pathlib import Path
# import csv

from extract.gsheets_extraction_tools import build_gsheets_ranges, map_raw_data_to_columns, map_columnar_data_to_records


def main():
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # CSV STORAGE PARAMETERS
    # today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    #  csv_storage_dir = f"csv/{today}"
    # Path(f"csv/{today}").mkdir(parents=True, exist_ok=True)

    # ACCESS GOOGLE SHEETS
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    # get sheet column parameters
    sheet_parameters_path = "./extract/google_sheets_config.json"
    with open(sheet_parameters_path, 'r') as column_params:
        sheet_parameters = json.load(column_params)

    # target gsheets sheet id
    spreadsheet_id = sheet_parameters["sheet_id"]

    # EXTRACT INVENTORY
    # fetch Inventory data
    inventory_config = sheet_parameters["Inventory"]
    inventory_columns = inventory_config["columns"]
    inventory_is_column_name_included = inventory_config["is_column_name_included"]
    inventory_start_row = inventory_config["start_row"]

    # build gsheets ranges for each column
    inventory_column_ranges = build_gsheets_ranges("Inventory", inventory_start_row, inventory_columns)

    # extract from Inventory sheet
    inventory_results = sheet.values().batchGet(spreadsheetId=spreadsheet_id, ranges=inventory_column_ranges,
                                                majorDimension='COLUMNS').execute()
    inventory_result_ranges = inventory_results.get("valueRanges", [])

    # process raw inventory data
    inventory_columnar_data = map_raw_data_to_columns(inventory_result_ranges,
                                                      is_column_header_included=inventory_is_column_name_included)

    # map inventory columnar data to records
    inventory_records = map_columnar_data_to_records(inventory_columnar_data)

    # define path for storing inventory csv file from exract
    # inventory_file_name = "inventory.csv"
    # inventory_file_path = csv_storage_dir + '/' + inventory_file_name

    # get list of inventory column headers
    # inventory_column_headers = list(inventory_columnar_data.keys())
    # print("inventory_column_headers", inventory_column_headers)

    # Write Inventory to CSV
    '''with open(inventory_file_path, 'w') as inventory_outfile:
        csvwriter = csv.DictWriter(inventory_outfile, fieldnames=inventory_column_headers)
        csvwriter.writerows(inventory_records_all)'''

    # EXTRACT LOCAITONS
    # fetch Locations data
    locations_config = sheet_parameters["Locations"]
    locations_columns = locations_config["columns"]
    location_is_column_name_included = locations_config["is_column_name_included"]
    locations_start_row = locations_config["start_row"]

    # build gsheets ranges for each column
    locations_column_ranges = build_gsheets_ranges("Locations", locations_start_row, locations_columns)

    # extract from Locations sheet
    locaitons_results = sheet.values().batchGet(spreadsheetId=spreadsheet_id, ranges=locations_column_ranges,
                                                majorDimension='COLUMNS').execute()
    locations_result_ranges = locaitons_results.get("valueRanges", [])

    # process raw locations data
    locations_columnar_data = map_raw_data_to_columns(locations_result_ranges,
                                                      is_column_header_included=location_is_column_name_included)

    # map locations columnar data to records
    locations_records_ = map_columnar_data_to_records(locations_columnar_data)
    # filter out extranious data from bottom of file
    locations_records = [record for record in locations_records_ if len(record) > 1]

    # define path for storing locations csv file from extract
    # locations_file_name = "locations.csv"
    # locations_file_path = csv_storage_dir + '/' + locations_file_name

    # get list of locations column headers
    # locations_column_headers = list(locations_columnar_data.keys())
    # print("locations_column_headers", locations_column_headers)

    # Write Locations to CSV
    '''with open(locations_file_path, 'w') as locations_outfile:
        csvwriter = csv.DictWriter(locations_outfile, fieldnames=locations_column_headers)
        csvwriter.writerows(locations_records)'''

    # EXTRACT RUNS
    # fetch Runs data from Plants tab
    plants_config = sheet_parameters["Plants"]
    plants_columns = plants_config["columns"]
    plants_is_column_name_included = plants_config["is_column_name_included"]
    plants_start_row = plants_config["start_row"]

    # build gsheets ranges for each column
    plants_column_ranges = build_gsheets_ranges("Plants", plants_start_row, plants_columns)

    # extract from Plants sheet
    run_results = sheet.values().batchGet(spreadsheetId=spreadsheet_id, ranges=plants_column_ranges,
                                             majorDimension='COLUMNS').execute()
    run_result_ranges = run_results.get("valueRanges", [])

    run_columnar_data = map_raw_data_to_columns(run_result_ranges,
                                                   is_column_header_included=plants_is_column_name_included)

    run_records = map_columnar_data_to_records(run_columnar_data)
    # handle this filtering in the load step
    # active_runs_records = [record for record in run_records if record["Archive?"] == '']

    # define path for storing runs csv file from extract
    # runs_file_name = "runs.csv"
    # runs_file_path = csv_storage_dir + '/' + runs_file_name

    # get list of runs column headers
    # runs_column_headers = list(run_columnar_data.keys())
    # print("runs_column_headers", runs_column_headers)

    # Write Runs to CSV
    '''with open(runs_file_path, 'w') as runs_outfile:
        csvwriter = csv.DictWriter(runs_outfile, fieldnames=runs_column_headers)
        csvwriter.writerows(run_records)'''

    # Add filter on requested location dims and runs

    return {"Inventory": inventory_records, "Location": locations_records, "Run": run_records}


if __name__ == "__main__":
    main()