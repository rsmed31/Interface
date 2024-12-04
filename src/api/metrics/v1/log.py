"""
This module defines API routes for handling log-related data.
"""
from fastapi import APIRouter, Request
from domain.schemas import (
    ExceptionResponseSchema,
    GetLogResponseSchema,
)
from domain.services import LogService

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
