from fastapi import APIRouter
from typing import Optional

from ..services import monthly_service
from ..schemas import monthly_schema
from ..utils import constant


router = APIRouter(
    prefix="/monthly",
    tags=["monthly"]
)

@router.get("/", response_model=monthly_schema.MonthlyResponseMulti)
async def monthly_multi(since: Optional[str] = constant.EARLIEST_YEAR_MONTH_CASE, upto: Optional[str] = constant.LATEST_YEAR_MONTH_CASE):
    return monthly_service.monthly_multi(since, upto)
    
@router.get("/{year}", response_model=monthly_schema.MonthlyResponseMulti)
async def monthly_year_multi(year: str, since: Optional[str] = None, upto: Optional[str] = None):
    return monthly_service.monthly_year_multi(year, since, upto)

@router.get("/{year}/{month}", response_model=monthly_schema.MonthlyResponseSingle)
async def monthly_year_month_single(year: str, month: str):
    return monthly_service.monthly_year_month_single(year, month)
