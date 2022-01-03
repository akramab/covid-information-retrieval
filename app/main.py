import httpx

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI()

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


@app.get("/test")
async def test():
    r = httpx.get("https://data.covid19.go.id/public/api/update.json")
    return r.json()