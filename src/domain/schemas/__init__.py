from pydantic import BaseModel
from .cpu import GetCpuResponseSchema, GetCpuCoreResponseSchema
from .log import GetLogResponseSchema
from .logentry import LogEntrySchema


class ExceptionResponseSchema(BaseModel):
    error: str


__all__ = [
    "GetCpuResponseSchema",
    "GetCpuCoreResponseSchema",
    "ExceptionResponseSchema",
    "GetLogResponseSchema",
    "LogEntrySchema",
]
