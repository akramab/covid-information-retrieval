from fastapi import APIRouter

from ..schemas import entrypoint_schema
from ..services import entrypoint_service
from ..utils import constant, utility_functions


router = APIRouter(
    prefix="",
    tags=["entrypoint"]
)

@router.get("/", response_model=entrypoint_schema.EntrypointResponse)
async def index():
    return entrypoint_service.index()