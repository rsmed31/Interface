from pydantic import BaseModel
from .cpu import GetCpuResponseSchema, GetCpuCoreResponseSchema
from .log import GetLogResponseSchema


class ExceptionResponseSchema(BaseModel):
    error: str


__all__ = [
    "GetCpuResponseSchema",
    "GetCpuCoreResponseSchema",
    "ExceptionResponseSchema",
    "GetLogResponseSchema",
]
