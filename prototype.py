from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import json
import os
import datetime
import re

from gsheets_extraction_tools import map_raw_data_to_columns, map_columnar_data_to_records, build_gsheets_ranges

import logging

today = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
logging.basicConfig(filename=f'{today}.log', level=logging.DEBUG)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def main():
    # USER PROMPT
    # input for target location
    user_location_prompt = """
    1. Around Greenhouse
    2. Back Bed Left
    3. Back Bed Right
    4. Front Bed Right
    5. Ground Level Bed
    6. Trellis Beds
    7. West Bed Middle
    8. West Bed North
    9. West Bed South
    
    Please enter the number or name of target location:
    """

    # input for target date
    target_location_ = input(user_location_prompt).strip()
    target_location = None
    if re.match('^[0-9]{1}', target_location_) is not None:
        location_code = target_location_[0]
        if location_code == '1':
            target_location = "Around Greenhouse"
        elif location_code == '2':
            target_location = "Back Bed Left"
        elif location_code == '3':
            target_location = "Back Bed Right"
        elif location_code == '4':
            target_location = "Front Bed Right"
        elif location_code == '5':
            target_location = "Ground Level Bed"
        elif location_code == '6':
            target_location = "Trellis Beds"
        elif location_code == '7':
            target_location = "West Bed Middle"
        elif location_code == '8':
            target_location = "West Bed North"
        elif location_code == '9':
            target_location = "West Bed South"
        else:
            raise ValueError(f"Expected numeric value associated to location prompt but found: {target_location_}")
    else:
        target_location = target_location_

    user_date_prompt = "Please specify target date in format YYYY-mm-dd or press ENTER to use today's date: "
    target_date = input(user_date_prompt).strip()
    if target_date == '':
        target_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

    # DATA EXTRACTION START
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
    sheet_parameters_path = "gsheet_column_parameters.json"
    with open(sheet_parameters_path, 'r') as column_params:
        sheet_parameters = json.load(column_params)

    # target gsheets sheet id
    spreadsheet_id = sheet_parameters["sheet_id"]

    # EXTRACT Inventory
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
    inventory_records_all = map_columnar_data_to_records(inventory_columnar_data)
    inventory_records = [record for record in inventory_records_all if record.get("Archived", '') == '']
    #print(f"returned {len(inventory_records)} records from Inventory")  # DEBUG
    #print(f"Inventory columns: {inventory_records[0].keys()}")  # DEBUGå

    # specific inventory dims sliced by plant name
    inventory_attribute_map = {}
    for record in inventory_records:
        plant_name = record["Marketing Name"].strip()
        plant_sun_constraint = record["Sun"].strip()
        # or would it be better to simply pass on inventory which isn't defined for these areas?
        try:
            required_area = float(record["Plant Spacing"]) ** 2
        except ValueError:
            required_area = None

        try:
            max_single_planting = int(record["Max Single Planting"])
        except ValueError:
            max_single_planting = None

        required_duration = int(record["DTM"]) + int(record["MD"])
        inventory_attribute_map[plant_name] = {
            "required_area": required_area,
            "max_single_planting": max_single_planting,
            "Sun": plant_sun_constraint,
            "required_duration": required_duration
        }

    # EXTRACT Locations
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
    locations_records = map_columnar_data_to_records(locations_columnar_data)[:-1]  # temp workaround for data cleaning
    #print(f"returned {len(locations_records)} records from Locations")  # DEBUG
    #print(f"Locations columns: {locations_records[0].keys()}")  # DEBUG

    # specific location dims sliced by plant name
    location_attribute_map = {}
    for record in locations_records:
        location_name = record["name"].strip()
        try:
            total_area = float(record["Aval Area"])
        except ValueError:
            total_area = None
        except KeyError:
            total_area = None
        location_sun_constraint = record.get("sun").strip()

        location_attribute_map[location_name] = {
            "total_area": total_area,
            "sun": location_sun_constraint
        }
    #for attrib in location_attribute_map:
    #    print("loc", attrib, location_attribute_map[attrib]["sun"])

    # EXTRACT Plants
    # fetch Plants data
    plants_config = sheet_parameters["Plants"]
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
    active_runs_records = [record for record in plants_records if record["Archive?"] == '']
    #print(f"returned {len(active_runs_records)} records from Plants")  # DEBUG
    #print(f"Runs columns: {active_runs_records[0].keys()}")  # DEBUG


    # FILTER INVENTORY ON LOCATION SUN CONSTRAINT
    target_locaiton_attributes = location_attribute_map.get(target_location)
    if target_locaiton_attributes is None:
        raise KeyError(f"{target_location} not found in location_attribute_map")

    location_sun_constraint = target_locaiton_attributes.get("sun").lower()
    if location_sun_constraint is None:
        raise ValueError("expected locaiton_sun_constraint but found None")

    #sun_constraint_match = [plant for plant in inventory_records
    #                        if plant["Sun"].lower() == location_sun_constraint]
    sun_constraint_match = []
    for record in inventory_records:
        sun_contraint = record["Sun"].lower()
        if sun_contraint == location_sun_constraint:
            sun_constraint_match.append(record)

    #print("sun_constraint_match", sun_constraint_match)
    # why is the total area fetched here? appears to be dead code
    #location_total_area = target_locaiton_attributes.get("total_area")
    #if location_total_area is None:
    #    raise ValueError("expected location_total_area but found None")


    # FILTER INVENTORY ON SEASONALITY
    # convert target_date to 3 letter month code
    target_month = datetime.datetime.strftime(datetime.datetime.strptime(target_date, '%Y-%m-%d'), "%b")
    seasonality_constraint_match = []
    for record in sun_constraint_match:
        is_in_season = record.get(target_month, '').strip() == 'x'
        if is_in_season:
            seasonality_constraint_match.append(record)


    #seasonality_constraint_match = [plant for plant in sun_constraint_match if plant[target_month].strip() == 'x']
    #seasonality_constraint_match = [record["Marketing Name"] for record in sun_constraint_match
    #                                if record[target_month].strip() == 'x']
    #print(f"num records after seasonality filter: {len(seasonality_constraint_match)}")

    filtered_inventory_attribute_map = {}
    for record in seasonality_constraint_match:
        plant_name = record["Marketing Name"]
        plant_sun_constraint = record["Sun"]
        # or would it be better to simply pass on inventory which isn't defined for these areas?
        try:
            required_area = float(record["Plant Spacing"]) ** 2
        except ValueError:
            required_area = None

        try:
            max_single_planting = int(record["Max Single Planting"])
        except ValueError:
            max_single_planting = None

        required_duration = int(record["DTM"]) + int(record["MD"])
        filtered_inventory_attribute_map[plant_name] = {
            "required_area": required_area,
            "max_single_planting": max_single_planting,
            "Sun": plant_sun_constraint,
            "required_duration": required_duration
        }

    # CALC FOR AVAILABLE AREA IN LOCATION
    # calculate the total area used in a location per date over a range
    # join active_runs_records with inventory_records
    # join the location_records to get the total area for a given location
    runs_inventory_locations_join = active_runs_records.copy()
    for run in runs_inventory_locations_join:
        del run["Archive?"]
        plant_name = run["Marketing Name"]
        plant_inventory_attributes = inventory_attribute_map.get(plant_name)
        if plant_inventory_attributes is None:
            #print(f"unable to find inventory dimensions for {plant_name}")
            logging.debug(f"unable to find inventory dimensions for {plant_name}")
            continue

        required_duration = plant_inventory_attributes["required_duration"]
        required_area = plant_inventory_attributes["required_area"]
        max_single_planting = plant_inventory_attributes["max_single_planting"]

        location_name = run["OD Location"]
        location_attributes = location_attribute_map.get(location_name)
        if location_attributes is None:
            #print(f"unable to find location dimensions for {location_name}")
            logging.debug(f"unable to find location dimensions for {location_name}")
            continue
        location_total_area = location_attributes["total_area"]

        run.update({"required_duration": required_duration, "required_area": required_area,
                    "max_single_planting": max_single_planting, "location_total_area": location_total_area})


    # what is the required date range needed for area calc?
    range_end_date_obj = datetime.datetime.strptime(target_date, '%Y-%m-%d') + datetime.timedelta(days=364)

    # create date range from target to max
    working_date_range = [target_date]
    work_date_obj = datetime.datetime.strptime(target_date, '%Y-%m-%d')
    while work_date_obj <= range_end_date_obj:
        work_date_obj = work_date_obj + datetime.timedelta(days=1)
        work_date = datetime.datetime.strftime(work_date_obj, '%Y-%m-%d')
        working_date_range.append(work_date)

    # fitler on the target location
    run_inventory = [record for record in runs_inventory_locations_join
                     if record["OD Location"].lower() == target_location.lower()]

    # for each date between target_date and max_harvest_date calculate the available area for location
    available_area_by_date = {}  # {ds: avail_area}
    for date in working_date_range:
        used_area = 0
        for record in run_inventory:
            start_date = record["Sown RPT"]
            end_date = record["Harvest End RPT"]
            try:
                plant_quantity = int(record["Current Qty"])
            except ValueError:
                continue
            except KeyError:
                print(f"unable to find Current Qty for record {record}")
                continue

            if start_date <= date and date <= end_date:
                used_area += record["required_area"] * plant_quantity

        available_area = location_attribute_map[target_location]["total_area"] - used_area
        available_area_by_date[date] = available_area

    # for each plant in inventory check if required area is available during expected duraiton
    viable_plants = []
    target_date_available_area = available_area_by_date[target_date]
    for plant_name in filtered_inventory_attribute_map:
        required_area = filtered_inventory_attribute_map[plant_name]["required_area"]
        required_duration = filtered_inventory_attribute_map[plant_name]["required_duration"]
        if required_area is None or required_duration is None:
            continue
        plant_duration_end_date = datetime.datetime.strftime(datetime.datetime.strptime(target_date, '%Y-%m-%d') +
                                                             datetime.timedelta(days=required_duration), '%Y-%m-%d')
        is_plant_viable = True
        for date in available_area_by_date:
            if target_date <= date and date <= plant_duration_end_date:
                available_area = available_area_by_date[date]
                condition = available_area >= required_area
                if condition is False:
                    is_plant_viable = False
                    break
        if is_plant_viable is True:
            plant_inventory_attributes = inventory_attribute_map[plant_name]
            plant_required_area = plant_inventory_attributes["required_area"]
            plant_max_single_planting = plant_inventory_attributes["max_single_planting"]
            quantity = int(target_date_available_area // plant_required_area)
            if quantity <= plant_max_single_planting:
                viable_plants.append((plant_name, quantity))
            else:
                viable_plants.append((plant_name, plant_max_single_planting))
        else:
            continue


    # USER OUTPUT
    print('\n')
    print(f"{target_location} available area on {target_date}: {round(target_date_available_area, 2)} sqft")
    if not viable_plants:
        print("No recommendation")
    else:
        print("Recommended Plant Name, Quantity")
        for plant_name, qty in viable_plants:
            print(plant_name, qty)


if __name__ == "__main__":
    main()