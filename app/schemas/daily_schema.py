from pydantic import BaseModel
from typing import List

class DailyResponseData(BaseModel):
    date: str
    positive: int
    recovered: int
    deaths: int
    active: int

class DailyResponseMulti(BaseModel):
    ok: bool
    data: List[DailyResponseData]
    message: str

class DailyResponseSingle(BaseModel):
    ok: bool
    data: DailyResponseData
    message: str