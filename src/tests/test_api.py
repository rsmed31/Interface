"""This module defines tests for the API endpoints"""

import pytest
from fastapi.testclient import TestClient
from domain.services.logservice import count_log, LogService
from server import create_app
from monitor import MonitorTask
import os


class MonitorTaskFake(MonitorTask):
    """Mock monitor with deterministic test values"""

    def __init__(self):
        """Initialize with fake data"""
        self.interval = 0
        self.num_cores = 2
        self.cpu_percent = ["10", "12"]
        self.disk_usage = {
            "total": 250790436864,
            "used": 100316192768,
            "free": 150474244096,
            "percent": 40.0,
        }
        self.ram_usage = {
            "total": 16777216,
            "available": 8388608,
            "used": 8388608,
            "percent": 50.0,
        }
        self.processor_name = "Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz"
        self.cpu_frequency = 1800.0
        self.logservice = LogService("src/logs/wordpress.log")

    def monitor(self):
        """Mock monitor method"""
        pass

    def get_disk_usage(self):
        """Return fake disk stats"""
        return self.disk_usage

    def get_processor_name(self) -> str:
        """Return fake processor name"""
        return self.processor_name

    def get_cpu_frequency(self) -> float:
        """Return fake CPU frequency"""
        return self.cpu_frequency

    def get_connected_users(self):
        # Return mock connected users
        return ["user1", "user2", "user3"]

    def get_log_data(self):
        """Return log data from logs/wordpress.log"""
        log_file_path = os.path.abspath("src/logs/wordpress.log")
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


