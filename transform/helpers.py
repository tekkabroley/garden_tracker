import datetime


def date_add_days(date, num):
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
    adjusted_date_obj = date_obj + datetime.timedelta(days=num)
    adjusted_date = datetime.datetime.strftime(adjusted_date_obj, '%Y-%m-%d')
    return adjusted_date

