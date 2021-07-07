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

            Please enter the number or name of target location:
        """
    # input for target location
    target_location = None
    target_location_ = input(user_location_prompt).strip().lower()
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
        target_location = target_location_

    return target_location.strip().lower()


def get_target_date():
    # input for target date
    user_date_prompt = "Please specify target date in format YYYY-mm-dd or press ENTER to use today's date: "
    target_date = input(user_date_prompt).strip()
    if target_date == '':
        target_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    return target_date


def main():
    # USER PROMPT
    target_location = get_target_location()
    target_date = get_target_date()

    return {"target_location": target_location, "target_date": target_date}


if __name__ == "__main__":
    main()