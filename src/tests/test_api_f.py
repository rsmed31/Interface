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
    app.state.logservice = LogService(log_path="src/logs/wordpressStatic.log")
    return app


@pytest.fixture
def client(test_app):
    """Create a test client"""
    return TestClient(test_app)


def test_health(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200


def test_get_cpu_usage(client):
    """Test CPU usage endpoint with incorrect data"""
    response = client.get("/metrics/v1/cpu/usage")
    assert response.status_code == 200
    assert response.json() == [{"id": 0, "usage": "-1"}]


def test_get_ram_usage(client):
    """Test RAM usage endpoint with incorrect data"""
    response = client.get("/metrics/v1/ram/usage")
    assert response.status_code == 200
    assert response.json() == {"total": -1, "available": -1, "used": -1, "percent": -1}


def test_get_disk_usage(client):
    """Test disk usage endpoint with incorrect data"""
    response = client.get("/metrics/v1/disk/usage")
    assert response.status_code == 200
    assert response.json() == {"total": -1, "used": -1, "free": -1, "percent": -1}


def test_get_connected_users(client):
    """Test the connected users endpoint with incorrect data"""
    response = client.get("/metrics/v1/users/connected")
    assert response.status_code == 200
    assert response.json() == ["invalid_user"]


def test_get_log_data(client):
    """Test log data endpoint"""
    response = client.get("/metrics/v1/log/logs")
    assert response.status_code == 200
    assert response.json() == {
        "nbip": 5,
        "failed": 6,
        "succeed": 18,
        "nbwebsites": {"Home": 5, "/page1": 6, "/page3": 6, "/page2": 7, "": 1},
        "ip_visits": {
            "192.168.1.10": ["Home", "/page1", "/page3", "Home", "/page1"],
            "10.0.0.1": ["/page2", "/page1", "/page3", "/page2", "/page1", "/page2"],
            "172.16.0.1": ["/page2", "Home", "/page3", "/page1", "Home"],
            "203.0.113.1": ["/page3", "/page1", "", "/page2"],
            "198.51.100.1": ["/page2", "Home", "/page3", "/page2", "/page3"],
        },
    }


def test_get_recent_logs_with_incorrect_data(client):
    """Test recent logs endpoint with incorrect data"""
    valid_logs = [
        {
            "ip": "172.16.0.1",
            "time": "[08/Jan/2020:11:15:43 +0000]",
            "request_method": "GET",
            "request_url": "/",
            "status": "200",
        },
        {
            "ip": "203.0.113.1",
            "time": "[08/Jan/2020:13:50:11 +0000]",
            "request_method": "GET",
            "request_url": "/page2",
            "status": "200",
        },
        {
            "ip": "198.51.100.1",
            "time": "[09/Jan/2020:07:40:50 +0000]",
            "request_method": "GET",
            "request_url": "/page3",
            "status": "404",
        },
        {
            "ip": "192.168.1.10",
            "time": "[09/Jan/2020:09:25:25 +0000]",
            "request_method": "GET",
            "request_url": "/page1",
            "status": "200",
        },
        {
            "ip": "10.0.0.1",
            "time": "[09/Jan/2020:12:12:49 +0000]",
            "request_method": "GET",
            "request_url": "/page2",
            "status": "200",
        },
    ]
    response = client.get("/metrics/v1/log/logs/recent")
    assert response.status_code == 200
    assert response.json() == valid_logs
