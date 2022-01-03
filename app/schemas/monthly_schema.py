from pydantic import BaseModel
from typing import List

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