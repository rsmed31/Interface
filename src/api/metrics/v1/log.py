"""
This module defines API routes for handling log-related data.
"""
from fastapi import APIRouter, Request
from domain.schemas import (
    ExceptionResponseSchema,
    GetLogResponseSchema,
)
from domain.services import LogService
from domain.schemas.logentry import LogEntrySchema
from typing import List

log_router = APIRouter()

@log_router.get(
    "/logs",
    response_model=GetLogResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_log(request: Request) -> GetLogResponseSchema:
    """
    Route to get log data.

    Args:
        request (Request): The incoming request.

    Returns:
        GetLogResponseSchema: Log data as per the response model.
    """
    return await LogService().get_log()

@log_router.get(
    "/logs/recent",
    response_model=List[LogEntrySchema],
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_recent_logs(request: Request) -> List[LogEntrySchema]:
    """
    Route to get the last 5 log entries.

    Args:
        request (Request): The incoming request.

    Returns:
        List[LogEntrySchema]: A list of the last 5 log entries.
    """
    return await LogService().get_recent_logs(5)