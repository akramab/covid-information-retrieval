from fastapi import HTTPException, status
from typing import Optional
from ..utils import constant, utility_functions
from ..repository import covid_data_repository

def yearly_multi(since: Optional[int] = int(constant.EARLIEST_YEAR_CASE), upto: Optional[int] = int(constant.LATEST_YEAR_CASE)):
    response_body = utility_functions.create_multi_REST_response()

    if(since < int(constant.EARLIEST_YEAR_CASE) or upto > int(constant.LATEST_YEAR_CASE)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameters error! SINCE must be higher or equal than " + constant.EARLIEST_YEAR_CASE +" and UPTO can't be higher than " + constant.LATEST_YEAR_CASE +"!"
        )

    if(since > upto):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameters error! SINCE can't be a higher value than UPTO!")

    for year in range(since, upto+1, 1):
        response_body["data"].append(covid_data_repository.find_data_by_year(year))

    return response_body

def yearly_single(year: str):
    if(not year.isnumeric()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Value error! the provided YEAR must be an integer! with a value between " + constant.EARLIEST_YEAR_CASE +" and " + constant.LATEST_YEAR_CASE +"!"
        )

    if(int(year) < int(constant.EARLIEST_YEAR_CASE) or int(year) > int(constant.LATEST_YEAR_CASE)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Value error! the provided YEAR must be higher or equal than " + constant.EARLIEST_YEAR_CASE +" and can't be higher than " + constant.LATEST_YEAR_CASE +"!"
        )

    response_body = utility_functions.create_single_REST_response()
    response_body["data"] = covid_data_repository.find_data_by_year(year)

    return response_body