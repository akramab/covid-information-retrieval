import re

from fastapi import HTTPException, status
from typing import Optional
from ..utils import constant, utility_functions
from ..repository import covid_data_repository

def daily_multi(since: Optional[str] = constant.EARLIEST_DATE_CASE, upto: Optional[str] = constant.LATEST_DATE_CASE):
    if (not re.search(utility_functions.regex_date_query_generator("DATE"), since) or not re.search(utility_functions.regex_date_query_generator("DATE"), upto)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameter error! SINCE and UPTO must be a valid date in the format of 'YYYY.MM.DD'. Valid values for YYYY are the value of integers between " + constant.EARLIEST_YEAR_CASE + " and " + constant.LATEST_YEAR_CASE)

    response_body = utility_functions.create_multi_REST_response()

    formatted_since = "-".join((since.split(".")))
    formatted_upto = "-".join((upto.split(".")))

    response_body["data"] = covid_data_repository.find_data_by_dates(formatted_since, formatted_upto)

    return response_body

def daily_multi_year(year: str,since: Optional[str] = None, upto: Optional[str] = None):
    if((not year.isnumeric()) or (int(year) < int(constant.EARLIEST_YEAR_CASE)) or (int(year) > int(constant.LATEST_YEAR_CASE))):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "the provided YEAR must be an integer value between " + constant.EARLIEST_YEAR_CASE + " and " + constant.LATEST_YEAR_CASE + "!"
        )

    response_body = utility_functions.create_multi_REST_response()

    formatted_since = ""
    formatted_upto = ""
    if (since and upto):
        formatted_since = "-".join((since.split(".")))
        formatted_upto = "-".join((upto.split(".")))

    elif (not since and upto):
        if year == constant.EARLIEST_YEAR_CASE:
            formatted_since = "-".join((constant.EARLIEST_DATE_CASE.split(".")))
        else:
            formatted_since = year + "-01-01"
        formatted_upto = "-".join((upto.split(".")))
    
    elif (since and not upto):
        if year == constant.LATEST_YEAR_CASE:
            formatted_upto = "-".join((constant.LATEST_DATE_CASE.split(".")))
        else:
            formatted_upto = year + "-12-31"
        formatted_since = "-".join((since.split(".")))
    else:
        formatted_since = year + "-01-01"
        formatted_upto = year + "-12-31"

    response_body["data"] = covid_data_repository.find_data_by_dates(formatted_since, formatted_upto)

    return response_body

def daily_multi_year_month(year: str, month: str, since: Optional[str] = None, upto: Optional[str] = None):
    if((not year.isnumeric()) or (int(year) < int(constant.EARLIEST_YEAR_CASE)) or (int(year) > int(constant.LATEST_YEAR_CASE))):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "the provided YEAR must be an integer value between " + constant.EARLIEST_YEAR_CASE + " and " + constant.LATEST_YEAR_CASE + "!"
        )
    if((not month.isnumeric()) or (int(month) < 1) or (int(month) > 12)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "the provided MONTH must be an integer value between 1 and 12!"
        )

    response_body = utility_functions.create_multi_REST_response()

    formatted_since = ""
    formatted_upto = ""

    if(since and upto):
        formatted_since = "-".join((since.split(".")))
        formatted_upto = "-".join((upto.split(".")))
    elif(not since and upto):
        formatted_since = year + "-" + month + "-01"
        formatted_upto = "-".join((upto.split(".")))
    elif(since and not upto):
        formatted_since = "-".join((since.split(".")))
        formatted_upto = year + "-" + month + utility_functions.string_formatted_day(year, month)
    else:
        formatted_since = year + "-" + month + "-01"
        formatted_upto = year + "-" + month + utility_functions.string_formatted_day(year, month)
    
    response_body["data"] = covid_data_repository.find_data_by_dates(formatted_since, formatted_upto)

    return response_body

def daily_multi_year_month_date(year: str, month: str, date: str):
    if((not year.isnumeric()) or (int(year) < int(constant.EARLIEST_YEAR_CASE)) or (int(year) > int(constant.LATEST_YEAR_CASE))):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "the provided YEAR must be an integer value between " + constant.EARLIEST_YEAR_CASE + " and " + constant.LATEST_YEAR_CASE + "!"
        )
    if((not month.isnumeric()) or (int(month) < 1) or (int(month) > 12)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "the provided MONTH must be an integer value between 1 and 12!"
        )
    if((not date.isnumeric()) or (int(date) < 1) or (int(date) > 31)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "the provided DATE must be an integer value between 1 and 31!"
        )

    response_body = utility_functions.create_single_REST_response()
    formatted_date = year + "-" + month + "-" + date

    response_body["data"] = covid_data_repository.find_data_by_dates(formatted_date, formatted_date)[0]

    return response_body