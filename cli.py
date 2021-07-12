import re
from datetime import datetime


def get_target_location():
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

    Please enter the number or name of target location: """
    # input for target location
    target_location = None
    target_location_ = input(user_location_prompt).strip().lower()
    if re.match('^[0-9]{1}', target_location_) is not None:
        location_code = target_location_[0]
        if location_code == '1':
            target_location = "around greenhouse"
        elif location_code == '2':
            target_location = "back bed left"
        elif location_code == '3':
            target_location = "back bed right"
        elif location_code == '4':
            target_location = "front bed right"
        elif location_code == '5':
            target_location = "ground level bed"
        elif location_code == '6':
            target_location = "trellis beds"
        elif location_code == '7':
            target_location = "west bed middle"
        elif location_code == '8':
            target_location = "west bed north"
        elif location_code == '9':
            target_location = "west bed south"
    else:
        target_location = target_location_

    return target_location


def validate_location(location):
    """ validate that location is one of the expected values for a location"""
    locations = {
        "around greenhouse",
        "back bed left",
        "back bed right",
        "front bed right",
        "ground level bed",
        "trellis beds",
        "west bed middle",
        "west bed north",
        "west bed south"
    }
    return location in locations


def get_target_date():
    # input for target date
    user_date_prompt = "Please specify target date in format YYYY-mm-dd or press ENTER to use today's date: "
    target_date = input(user_date_prompt).strip()
    if target_date == '':
        target_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    return target_date


def validate_date(date):
    """ validate that date conforms to YYYY-mm-dd """
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def main():
    # USER PROMPT
    target_location = get_target_location()
    target_date = get_target_date()

    if not validate_location(target_location):
        print(f"{target_location} is an invalid location.")
        return main()

    if not validate_date(target_date):
        print(f"{target_date} is an invalid date. date needs to in format YYYY-mm-dd.")
        return main()

    return {"target_location": target_location, "target_date": target_date}


if __name__ == "__main__":
    main()