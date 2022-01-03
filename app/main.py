import httpx

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI()

covid_data_JSON = {}
with httpx.Client() as client:
    covid_data_JSON = client.get("https://data.covid19.go.id/public/api/update.json").json()

class EntrypointResponseData(BaseModel):
    total_positive: int
    total_recovered: int
    total_deaths: int
    total_active: int
    new_positive: int
    new_recovered: int
    new_deaths: int
    new_active: int

class EntrypointResponse(BaseModel):
    ok: bool
    data: EntrypointResponseData
    message: str

class YearlyResponseData(BaseModel):
    year: str
    positive: int
    recovered: int
    deaths: int
    active: int

class YearlyResponseMulti(BaseModel):
    ok: bool
    data: List[YearlyResponseData]
    message: str

class YearlyResponseSingle(BaseModel):
    ok: bool
    data: YearlyResponseData
    message: str

class MonthlyResponseData(BaseModel):
    month: str
    positive: int
    recovered: int
    deaths: int
    active: int

class MonthlyResponseMulti(BaseModel):
    ok: bool
    data: List[MonthlyResponseData]
    message: str

class MonthlyResponseSingle(BaseModel):
    ok: bool
    data: MonthlyResponseData
    message: str

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

@app.get("/", response_model=EntrypointResponse)
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

@app.get("/yearly", response_model=YearlyResponseMulti)
async def yearly_multi(since: Optional[int] = 2020, upto: Optional[int] = 2022):
    response_body = create_multi_REST_response()

    for year in range(since, upto+1, 1):
        response_body["data"].append(find_data_by_year(year))

    return response_body

@app.get("/yearly/{year}", response_model=YearlyResponseSingle)
async def yearly_single(year: str):
    response_body = create_single_REST_response()
    response_body["data"] = find_data_by_year(year)

    return response_body

@app.get("/monthly", response_model=MonthlyResponseMulti)
async def monthly_multiple(since: Optional[str] = "2020.03", upto: Optional[str] = "2022.01"):
    response_body = create_multi_REST_response()
    since_year_month = since.split(".")
    upto_year_month = upto.split(".")

    for year in range(int(since_year_month[0]), int(upto_year_month[0]) + 1, 1):
        print("year = ", year)
        
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
    
@app.get("/monthly/{year}", response_model=MonthlyResponseMulti)
async def monthly_year_multiple(year: str, since: Optional[str] = None, upto: Optional[str] = None):
    response_body = create_multi_REST_response()

    since_year_month = ""
    if since:
        since_year_month = (since.split("."))
    elif (year == "2020"):
        since_year_month = (("2020.03").split("."))
    else:
        since_year_month = ((year + ".01").split("."))
    

    upto_year_month = ""
    if upto:
        upto_year_month = (upto.split("."))
    elif (year == "2022"):
        upto_year_month = (("2022.01").split("."))
    else:
        upto_year_month = ((year + ".12").split("."))

    for month in range(int(since_year_month[1]), int(upto_year_month[1]) + 1, 1):
        response_body["data"].append(find_data_by_year_month(year, month))
    
    return response_body

@app.get("/monthly/{year}/{month}", response_model=MonthlyResponseSingle)
async def monthly_year_month_single(year: str, month: str):
    response_body = create_single_REST_response()

    response_body["data"] = find_data_by_year_month(year, month)

    return response_body


@app.get("/test")
async def test():
    r = httpx.get("https://data.covid19.go.id/public/api/update.json")
    return r.json()