from pydantic import BaseModel

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