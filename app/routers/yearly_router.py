from fastapi import APIRouter
from typing import Optional

from ..services import yearly_service
from ..schemas import yearly_schema
from ..utils import constant




router = APIRouter(
    prefix="/yearly",
    tags=["yearly"]
)

@router.get("/", response_model=yearly_schema.YearlyResponseMulti)
async def yearly_multi(since: Optional[int] = int(constant.EARLIEST_YEAR_CASE), upto: Optional[int] = int(constant.LATEST_YEAR_CASE)):
    return yearly_service.yearly_multi(since, upto)

@router.get("/{year}", response_model=yearly_schema.YearlyResponseSingle)
async def yearly_single(year: str):
    return yearly_service.yearly_single(year)