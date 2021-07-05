import transform.filter.filters as filters


def main(location_name, runs):
    runs1 = filters.filter_runs_active(runs)
    runs2 = filters.filter_runs_target_location(runs1, location_name)
    return runs2


if __name__ == "__main__":
    main()