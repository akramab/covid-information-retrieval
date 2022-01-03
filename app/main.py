from fastapi import FastAPI
from .routers import entrypoint_router, yearly_router, monthly_router, daily_router

app = FastAPI()

app.include_router(entrypoint_router.router)
app.include_router(yearly_router.router)
app.include_router(monthly_router.router)
app.include_router(daily_router.router)