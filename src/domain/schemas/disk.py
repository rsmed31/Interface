from pydantic import BaseModel

class GetDiskResponseSchema(BaseModel):
    total: int
    used: int
    free: int
    percent: float
