from pydantic import BaseModel
from typing import List

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