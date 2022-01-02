import httpx

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class EntryResponseData(BaseModel):
    total_positive: int
    total_recovered: int
    total_deaths: int
    total_active: int
    new_positive: int
    new_recovered: int
    new_deaths: int
    new_active: int

class EntryResponse(BaseModel):
    ok: bool
    data: EntryResponseData
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

@app.get("/", response_model=EntryResponse)
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

@app.get("/test")
async def test():
    r = httpx.get("https://data.covid19.go.id/public/api/update.json")
    return r.json()