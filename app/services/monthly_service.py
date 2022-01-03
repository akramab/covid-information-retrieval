import re

from fastapi import HTTPException, status
from typing import Optional
from ..utils import constant, utility_functions
from ..repository import covid_data_repository

def monthly_multi(since: Optional[str] = constant.EARLIEST_YEAR_MONTH_CASE, upto: Optional[str] = constant.LATEST_YEAR_MONTH_CASE):
    if (not re.search(utility_functions.regex_date_query_generator("MONTH"), since) or not re.search(utility_functions.regex_date_query_generator("MONTH"), upto)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameter error! SINCE and UPTO must be a valid date in the format of 'YYYY.MM'. Valid values for YYYY are the value of integers between " + constant.EARLIEST_YEAR_CASE + " and " + constant.LATEST_YEAR_CASE)


    response_body = utility_functions.create_multi_REST_response()
    since_year_month = since.split(".")
    upto_year_month = upto.split(".")

    for year in range(int(since_year_month[0]), int(upto_year_month[0]) + 1, 1):
        
        if(year < int(upto_year_month[0]) and year == int(since_year_month[0])):
            for month in range(int(since_year_month[1]), 12 + 1, 1):
                response_body["data"].append(covid_data_repository.find_data_by_year_month(year, month))
        elif(year < int(upto_year_month[0])):
            for month in range(1, 12 + 1, 1):
                response_body["data"].append(covid_data_repository.find_data_by_year_month(year, month))
        elif(year == int(upto_year_month[0]) and year == int(since_year_month[0])):
            for month in range(int(since_year_month[1]), int(upto_year_month[1]) + 1, 1):
                response_body["data"].append(covid_data_repository.find_data_by_year_month(year, month))
        else:
            for month in range(1, int(upto_year_month[1]) + 1, 1):
                response_body["data"].append(covid_data_repository.find_data_by_year_month(year, month))

    return response_body
    
def monthly_year_multi(year: str, since: Optional[str] = None, upto: Optional[str] = None):
    if((not year.isnumeric()) or (int(year) < int(constant.EARLIEST_YEAR_CASE)) or (int(year) > int(constant.LATEST_YEAR_CASE))):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "the provided YEAR must be an integer value between " + constant.EARLIEST_YEAR_CASE + " and " + constant.LATEST_YEAR_CASE + "!"
            )

    response_body = utility_functions.create_multi_REST_response()

    since_year_month = ""
    if since:
        since_year_month = (since.split("."))
    elif (year == constant.EARLIEST_YEAR_CASE):
        since_year_month = ((constant.EARLIEST_YEAR_MONTH_CASE).split("."))
    else:
        since_year_month = ((year + ".01").split("."))
    

    upto_year_month = ""
    if upto:
        upto_year_month = (upto.split("."))
    elif (year == constant.LATEST_YEAR_CASE):
        upto_year_month = ((constant.LATEST_YEAR_MONTH_CASE).split("."))
    else:
        upto_year_month = ((year + ".12").split("."))
    
    if (since_year_month[0] != year or upto_year_month[0] != year):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameter error! year in SINCE or UPTO must match with the provided YEAR!"
        )
    
    if (int(since_year_month[1]) > int(upto_year_month[1])):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameter error! month in SINCE must be lower or equal to month in UPTO!" 
        )
    
    if (int(since_year_month[1]) < 1 or int(since_year_month[1]) > 12 or int(upto_year_month[1]) > 12):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameter error! Invalid month value in SINCE or UPTO!"
        )

    for month in range(int(since_year_month[1]), int(upto_year_month[1]) + 1, 1):
        response_body["data"].append(covid_data_repository.find_data_by_year_month(year, month))
    
    return response_body

def monthly_year_month_single(year: str, month: str):
    if(not year.isnumeric() or not month.isnumeric()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="YEAR and MONTH must be an integer!"
        )

    if(int(year) < int(constant.EARLIEST_YEAR_CASE) or int(year) > int(constant.LATEST_YEAR_CASE)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid YEAR value! YEAR must be an integer with a value between " + constant.EARLIEST_YEAR_CASE + " and " + constant.LATEST_YEAR_CASE + "!"
        )
    
    if(int(month) < 1 or int(month) > 12):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid MONTH value! MONTH must be an integer with a value between 1 and 12!"
        )

    response_body = utility_functions.create_single_REST_response()

    response_body["data"] = covid_data_repository.find_data_by_year_month(year, month)

    return response_body