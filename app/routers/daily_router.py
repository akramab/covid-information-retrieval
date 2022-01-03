from fastapi import APIRouter
from typing import Optional

from ..services import daily_service
from ..schemas import daily_schema
from ..utils import constant

router = APIRouter(
    prefix="/daily",
    tags=["daily"]
)


@router.get("/", response_model=daily_schema.DailyResponseMulti)
async def daily_multi(since: Optional[str] = constant.EARLIEST_DATE_CASE, upto: Optional[str] = constant.LATEST_DATE_CASE):
    return daily_service.daily_multi(since, upto)

@router.get("/{year}", response_model=daily_schema.DailyResponseMulti)
async def daily_multi_year(year: str,since: Optional[str] = None, upto: Optional[str] = None):
    return daily_service.daily_multi_year(year, since, upto)

@router.get("/{year}/{month}", response_model=daily_schema.DailyResponseMulti)
async def daily_multi_year_month(year: str, month: str, since: Optional[str] = None, upto: Optional[str] = None):
    return daily_service.daily_multi_year_month(year, month, since, upto)
   
@router.get("/{year}/{month}/{date}", response_model=daily_schema.DailyResponseSingle)
async def daily_multi_year_month_date(year: str, month: str, date: str):
    return daily_service.daily_multi_year_month_date(year, month, date)
