import time
import calendar

def is_date_greater_than(date1, date2):
    formatted_date1 = time.strptime(date1, "%Y-%m-%d")
    formatted_date2 = time.strptime(date2, "%Y-%m-%d")

    return formatted_date1 >= formatted_date2

def is_date_lower_than(date1, date2):
    formatted_date1 = time.strptime(date1, "%Y-%m-%d")
    formatted_date2 = time.strptime(date2, "%Y-%m-%d")

    return formatted_date1 <= formatted_date2


def string_formatted_day(year, month):
    day = calendar.monthrange(int(year), int(month))

    formatted_day = "-" + str(day[1])

    return formatted_day