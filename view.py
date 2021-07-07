

def print_recommendations(location_name, target_date, recommendations):
    location_name_ = location_name.capitalize()
    recommendations_ = sorted(recommendations.items(), key=lambda tup: tup[0])
    if len(recommendations) == 0:
        print(f"No recommendations for {location_name_} on {target_date}")
    else:
        print(f"Recommendations for {location_name_} on {target_date}")
        for inventory_name, cnt in recommendations_:
            print(f"{inventory_name.capitalize()} | {cnt}")