import time
import calendar

from . import constant

def create_single_REST_response():
    return {
        "ok": True,
        "data": {},
        "message": "success"
    }

def create_multi_REST_response():
    return {
        "ok": True,
        "data": [],
        "message": "success"
    }

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

def regex_date_query_generator(type):
    regex_string = "("
    for year in range(int(constant.EARLIEST_YEAR_CASE), int(constant.LATEST_YEAR_CASE) + 1, 1):
        if year == int(constant.LATEST_YEAR_CASE):
            regex_string += str(year) + ").("
        else:
            regex_string += str(year) + "|"
    
    for month in range(1, 12 + 1, 1):
        if month == 12:
            regex_string += str(month) + ")"
        elif month >= 10:
            regex_string += str(month) + "|" 
        else:
            regex_string += "0" + str(month) + "|"
    
    if type == "DATE":
        regex_string += ".("
        for day in range(1, 31 + 1, 1):
            if day == 31:
                regex_string += str(day) + ")"
            elif day >= 10:
                regex_string += str(day) + "|"
            else:
                regex_string += "0" + str(day) + "|"
    
    return regex_string