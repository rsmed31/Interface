from fastapi import APIRouter, Request
from typing import List

user_router = APIRouter()

@user_router.get("/connected", response_model=List[str])
async def get_connected_users(request: Request) -> List[str]:
    """
    Route to get connected users.

    Args:
        request (Request): The incoming request.

    Returns:
        List[str]: List of connected users.
    """
    return request.app.state.monitortask.get_connected_users()