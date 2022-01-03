import httpx
import re

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict, List, Optional
from .utils import constant, utility_functions
from .schemas import entrypoint_schema
from .schemas import yearly_schema
from .schemas import monthly_schema
from .schemas import daily_schema



app = FastAPI()

covid_data_JSON = {}
with httpx.Client() as client:
    covid_data_JSON = client.get("https://data.covid19.go.id/public/api/update.json").json()

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

def find_data_by_year(year):
    httpx_response_JSON = httpx.get("https://data.covid19.go.id/public/api/update.json").json()
    year = str(year)

    result = {
        "year": year,
        "positive": 0,
        "recovered": 0,
        "deaths": 0,
        "active": 0
    }
    
    for daily_data in httpx_response_JSON["update"]["harian"]:
        if (year in daily_data["key_as_string"]):
            result["positive"] += daily_data["jumlah_positif"]["value"]
            result["recovered"] += daily_data["jumlah_sembuh"]["value"]
            result["deaths"] += daily_data["jumlah_meninggal"]["value"]
            result["active"] += daily_data["jumlah_dirawat"]["value"]
    
    return result

def find_data_by_year_month(year, month):
    httpx_response_JSON = covid_data_JSON
    month = (str(int(month))) if (int(month) >= 10) else ("0" + str(int(month)))

    year_month = str(year) + "-" + month

    result = {
        "month": year_month,
        "positive": 0,
        "recovered": 0,
        "deaths": 0,
        "active": 0
    }
    
    for daily_data in httpx_response_JSON["update"]["harian"]:
        if (year_month in daily_data["key_as_string"]):
            result["positive"] += daily_data["jumlah_positif"]["value"]
            result["recovered"] += daily_data["jumlah_sembuh"]["value"]
            result["deaths"] += daily_data["jumlah_meninggal"]["value"]
            result["active"] += daily_data["jumlah_dirawat"]["value"]
    
    return result

def find_data_by_year_month_date(year, month, date):
    httpx_response_JSON = covid_data_JSON
    month = (str(int(month))) if (int(month) >= 10) else ("0" + str(int(month)))
    date= (str(int(date))) if (int(date) >= 10) else ("0" + str(int(date)))

    year_month_date = str(year) + "-" + month + "-" + date

    result = {
        "date": year_month_date,
        "positive": 0,
        "recovered": 0,
        "deaths": 0,
        "active": 0
    }

    for daily_data in httpx_response_JSON["update"]["harian"]:
        if (year_month_date in daily_data["key_as_string"]):
            result["positive"] += daily_data["jumlah_positif"]["value"]
            result["recovered"] += daily_data["jumlah_sembuh"]["value"]
            result["deaths"] += daily_data["jumlah_meninggal"]["value"]
            result["active"] += daily_data["jumlah_dirawat"]["value"]
    
    return result

def find_data_by_dates(since, upto):
    httpx_response_JSON = covid_data_JSON
    result = []

    for daily_data in httpx_response_JSON["update"]["harian"]:
        if((utility_functions.is_date_greater_than(daily_data["key_as_string"][0:10], since)) and (utility_functions.is_date_lower_than(daily_data["key_as_string"][0:10], upto))):
            result.append({
                "date": daily_data["key_as_string"][0:10],
                "positive": daily_data["jumlah_positif"]["value"],
                "recovered": daily_data["jumlah_sembuh"]["value"],
                "deaths": daily_data["jumlah_meninggal"]["value"],
                "active": daily_data["jumlah_dirawat"]["value"]
            })
    
    return result

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
    
    
        



@app.get("/", response_model=entrypoint_schema.EntrypointResponse)
async def index():
    httpx_response_JSON = httpx.get("https://data.covid19.go.id/public/api/update.json").json()
    response_body = create_single_REST_response()

    response_body["data"] = {
        "total_positive": httpx_response_JSON["update"]["total"]["jumlah_positif"],
        "total_recovered": httpx_response_JSON["update"]["total"]["jumlah_sembuh"],
        "total_deaths": httpx_response_JSON["update"]["total"]["jumlah_meninggal"],
        "total_active": httpx_response_JSON["update"]["total"]["jumlah_dirawat"],
        "new_positive": httpx_response_JSON["update"]["penambahan"]["jumlah_positif"],
        "new_recovered": httpx_response_JSON["update"]["penambahan"]["jumlah_sembuh"],
        "new_deaths": httpx_response_JSON["update"]["penambahan"]["jumlah_meninggal"],
        "new_active": httpx_response_JSON["update"]["penambahan"]["jumlah_dirawat"]
    }
    return response_body

@app.get("/yearly", response_model=yearly_schema.YearlyResponseMulti)
async def yearly_multi(since: Optional[int] = int(constant.EARLIEST_YEAR_CASE), upto: Optional[int] = int(constant.LATEST_YEAR_CASE)):
    response_body = create_multi_REST_response()

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
        response_body["data"].append(find_data_by_year(year))

    return response_body

@app.get("/yearly/{year}", response_model=yearly_schema.YearlyResponseSingle)
async def yearly_single(year: str):
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

    response_body = create_single_REST_response()
    response_body["data"] = find_data_by_year(year)

    return response_body

@app.get("/monthly", response_model=monthly_schema.MonthlyResponseMulti)
async def monthly_multi(since: Optional[str] = constant.EARLIEST_YEAR_MONTH_CASE, upto: Optional[str] = constant.LATEST_YEAR_MONTH_CASE):

    if (not re.search(regex_date_query_generator("MONTH"), since) or not re.search(regex_date_query_generator("MONTH"), upto)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameter error! SINCE and UPTO must be a valid date in the format of 'YYYY.MM'. Valid values for YYYY are the value of integers between " + constant.EARLIEST_YEAR_CASE + " and " + constant.LATEST_YEAR_CASE)


    response_body = create_multi_REST_response()
    since_year_month = since.split(".")
    upto_year_month = upto.split(".")

    for year in range(int(since_year_month[0]), int(upto_year_month[0]) + 1, 1):
        
        if(year < int(upto_year_month[0]) and year == int(since_year_month[0])):
            for month in range(int(since_year_month[1]), 12 + 1, 1):
                response_body["data"].append(find_data_by_year_month(year, month))
        elif(year < int(upto_year_month[0])):
            for month in range(1, 12 + 1, 1):
                response_body["data"].append(find_data_by_year_month(year, month))
        elif(year == int(upto_year_month[0]) and year == int(since_year_month[0])):
            for month in range(int(since_year_month[1]), int(upto_year_month[1]) + 1, 1):
                response_body["data"].append(find_data_by_year_month(year, month))
        else:
            for month in range(1, int(upto_year_month[1]) + 1, 1):
                response_body["data"].append(find_data_by_year_month(year, month))

    return response_body
    
@app.get("/monthly/{year}", response_model=monthly_schema.MonthlyResponseMulti)
async def monthly_year_multi(year: str, since: Optional[str] = None, upto: Optional[str] = None):
    if((not year.isnumeric()) or (int(year) < int(constant.EARLIEST_YEAR_CASE)) or (int(year) > int(constant.LATEST_YEAR_CASE))):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "the provided YEAR must be an integer value between " + constant.EARLIEST_YEAR_CASE + " and " + constant.LATEST_YEAR_CASE + "!"
            )

    response_body = create_multi_REST_response()

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
        response_body["data"].append(find_data_by_year_month(year, month))
    
    return response_body

@app.get("/monthly/{year}/{month}", response_model=monthly_schema.MonthlyResponseSingle)
async def monthly_year_month_single(year: str, month: str):
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

    response_body = create_single_REST_response()

    response_body["data"] = find_data_by_year_month(year, month)

    return response_body

@app.get("/daily", response_model=daily_schema.DailyResponseMulti)
async def daily_multi(since: Optional[str] = constant.EARLIEST_DATE_CASE, upto: Optional[str] = constant.LATEST_DATE_CASE):
    if (not re.search(regex_date_query_generator("DATE"), since) or not re.search(regex_date_query_generator("DATE"), upto)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameter error! SINCE and UPTO must be a valid date in the format of 'YYYY.MM.DD'. Valid values for YYYY are the value of integers between " + constant.EARLIEST_YEAR_CASE + " and " + constant.LATEST_YEAR_CASE)

    response_body = create_multi_REST_response()

    formatted_since = "-".join((since.split(".")))
    formatted_upto = "-".join((upto.split(".")))

    response_body["data"] = find_data_by_dates(formatted_since, formatted_upto)

    return response_body

@app.get("/daily/{year}", response_model=daily_schema.DailyResponseMulti)
async def daily_multi_year(year: str,since: Optional[str] = None, upto: Optional[str] = None):
    if((not year.isnumeric()) or (int(year) < int(constant.EARLIEST_YEAR_CASE)) or (int(year) > int(constant.LATEST_YEAR_CASE))):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "the provided YEAR must be an integer value between " + constant.EARLIEST_YEAR_CASE + " and " + constant.LATEST_YEAR_CASE + "!"
        )

    response_body = create_multi_REST_response()

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

    response_body["data"] = find_data_by_dates(formatted_since, formatted_upto)

    return response_body

@app.get("/daily/{year}/{month}", response_model=daily_schema.DailyResponseMulti)
async def daily_multi_year_month(year: str, month: str, since: Optional[str] = None, upto: Optional[str] = None):
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

    response_body = create_multi_REST_response()

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
    
    response_body["data"] = find_data_by_dates(formatted_since, formatted_upto)

    return response_body

@app.get("/daily/{year}/{month}/{date}", response_model=daily_schema.DailyResponseSingle)
async def daily_multi_year_month_date(year: str, month: str, date: str):
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

    response_body = create_single_REST_response()
    formatted_date = year + "-" + month + "-" + date

    response_body["data"] = find_data_by_dates(formatted_date, formatted_date)[0]

    return response_body