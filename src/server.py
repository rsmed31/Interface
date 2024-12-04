"""
This module contains a FastAPI application with various routes and middleware.

It initializes the FastAPI app, sets up routers, event listeners, and exception handlers, and
creates a monitoring thread for fetching metrics.
"""
import threading
from typing import List
from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api import router
from api.default.default import default_router
from core.exceptions import CustomException
from core.config import get_config
from monitor import MonitorTask
from contextlib import asynccontextmanager
import asyncio

def init_routers(fastapi: FastAPI) -> None:
    """
    Initialize API routers and include them in the FastAPI application.

    Args:
        fastapi (FastAPI): The FastAPI application to add routers to.
    """
    # Add default route (version, healthcheck)
    fastapi.include_router(default_router)
    # Add domain routes
    fastapi.include_router(router)

def init_listeners(fastapi: FastAPI) -> None:
    """
    Initialize event listeners and exception handlers for the FastAPI application.

    Args:
        fastapi (FastAPI): The FastAPI application to set up event listeners and handlers for.
    """
    # Exception handler
    @fastapi.exception_handler(CustomException)
    async def custom_exception_handler(_request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )

    # Start monitoring thread
    @fastapi.on_event("startup")
    async def start_monitoring():
        try:
            monitor_task = MonitorTask()
            threading.Thread(target=monitor_task.monitor, daemon=True).start()
            fastapi.state.monitortask = monitor_task
        except Exception as e:
            logger.error(f"Failed to start monitoring task: {e}")

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application.
    """
    config = get_config()
    app = FastAPI(
        title=config.title,
        description=config.description,
        version=config.version,
        debug=config.debug,
        middleware=[
            Middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]),
        ],
    )

    init_routers(app)
    init_listeners(app)

    return app

app = create_app()
