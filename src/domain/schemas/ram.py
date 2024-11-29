# FILE: src/domain/schemas/ram.py
from pydantic import BaseModel

class GetRamResponseSchema(BaseModel):
    total: int
    available: int
    used: int
    percent:float