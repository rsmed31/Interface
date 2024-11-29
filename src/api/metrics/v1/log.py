"""
This module defines API routes for handling CPU-related data.
"""
from fastapi import APIRouter, Request # type: ignore
from domain.schemas import (
    ExceptionResponseSchema,
    GetLogResponseSchema,
)
from domain.services import LogService

log_router = APIRouter()


@log_router.get(
    "",
    response_model=GetLogResponseSchema,
    # response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_log(request: Request) -> GetLogResponseSchema:
    """
    Route to get a list of Log data.

    Args:
        request (Request): The incoming request.

    Returns:
        List[GetLogResponseSchema]: A list of Log data as per the response model.
    """
    return await LogService().get_log()


