from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import json
import os

from gsheets_extraction_tools import map_raw_data_to_columns, map_columnar_data_to_records, build_gsheets_ranges


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def main():
    """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
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

    # target gsheets sheet id
    spreadsheet_id = os.environ["sheet_id"]

    # Call the Sheets API
    sheet = service.spreadsheets()

    # get sheet column parameters
    sheet_column_parameters_path = "gsheet_column_parameters.json"
    with open(sheet_column_parameters_path, 'r') as column_params:
        sheet_column_parameters = json.load(column_params)

    # EXTRACT Inventory
    # fetch Inventory data
    inventory_config = sheet_column_parameters["Inventory"]
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
    print(f"returned {len(inventory_records)} records from Inventory")

    # EXTRACT Locations
    # fetch Locations data
    locations_config = sheet_column_parameters["Locations"]
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
    locations_records = map_columnar_data_to_records(locations_columnar_data)
    print(f"returned {len(locations_records)} records from Locations")

    # EXTRACT Plants
    # fetch Plants data
    plants_config = sheet_column_parameters["Plants"]
    plants_columns = plants_config["columns"]
    plants_is_column_name_included = plants_config["is_column_name_included"]
    plants_start_row = plants_config["start_row"]

    # build gsheets ranges for each column
    plants_column_ranges = build_gsheets_ranges("Plants", plants_start_row, plants_columns)
    
    # extract from Plants sheet
    plants_results = sheet.values().batchGet(spreadsheetId=spreadsheet_id, ranges=plants_column_ranges,
                                     majorDimension='COLUMNS').execute()
    plants_result_ranges = plants_results.get("valueRanges", [])

    plants_columnar_data = map_raw_data_to_columns(plants_result_ranges,
                                                   is_column_header_included=plants_is_column_name_included)
    
    plants_records = map_columnar_data_to_records(plants_columnar_data)
    print(f"returned {len(plants_records)} records from Plants")



if __name__ == "__main__":
    main()