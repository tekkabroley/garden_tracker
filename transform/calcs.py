from transform.helpers import date_add_days


def location_available_area(target_date, inventory, location, runs):
    available_area_by_date = {}
    end_date = date_add_days(target_date, 364)
    date_ = target_date
    while date_ <= end_date:
        available_area = location.total_area
        for run in runs:
            condition = run.start_date <= date_ <= run.end_date
            if condition:
                planted_cnt = run.inventory_planted_cnt
                plant_name = run.inventory_name
                plant = inventory[plant_name]
                used_area = plant.required_area() * planted_cnt
                available_area -= used_area
        available_area_by_date[date_] = available_area
        date_ = date_add_days(date_, 1)
    return available_area_by_date


def inventory_recommendations(target_date, available_area_map, inventory):
    recommendations = {}
    for plant_name in inventory:
        plant = inventory[plant_name]
        required_duration = plant.required_duration()
        required_end_date = date_add_days(target_date, required_duration)
        available_area_over_range = {date: area for date, area in available_area_map.items()
                                     if target_date <= date <= required_end_date}
        min_available_area = min(available_area_over_range.values())
        required_area = plant.required_area()
        max_num_plantings = int(min_available_area // required_area)
        if max_num_plantings <= 0:
            continue

        if plant.single_planting_max is None:
            num_recommended = max_num_plantings
        elif max_num_plantings < plant.single_planting_max:
            num_recommended = max_num_plantings
        else:
            num_recommended = plant.single_planting_max

        recommendations[plant_name] = num_recommended
    return recommendations
