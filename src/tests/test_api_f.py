# FILE: tests/test_api_f.py

import pytest
from fastapi.testclient import TestClient
from server import create_app
from domain.services.logservice import LogService
from monitor import MonitorTask
import os


class MonitorTaskFake(MonitorTask):
    """Mock monitor with deterministic test values"""

    def __init__(self):
        self.cpu_percent = [-1]  # Invalid CPU percent as a list
        self.logservice = LogService("src/logs/wordpressStatic.log")

    def monitor(self):
        """Mock monitor method"""
        pass

    def get_cpu_usage(self):
        return self.cpu_percent  # Return the list directly

    def get_ram_usage(self):
        return {
            "total": -1,
            "available": -1,
            "used": -1,
            "percent": -1,
        }  # Invalid RAM usage

    def get_disk_usage(self):
        return {
            "total": -1,
            "used": -1,
            "free": -1,
            "percent": -1,
        }  # Invalid disk usage

    def get_connected_users(self):
        return ["invalid_user"]  # Invalid user data

    def get_log_data(self):
        """Return log data from wordpressStatic.log"""
        log_file_path = os.path.abspath("src/logs/wordpressStatic.log")
        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as file:
                return file.readlines()
        return []


@pytest.fixture
def test_app():
    """Create a test application with mocked monitor"""
    app = create_app()
    app.state.monitortask = MonitorTaskFake()
    return app



