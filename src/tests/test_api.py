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
            "percent": 40.0
        }
        self.ram_usage = {
            "total": 16777216,
            "available": 8388608,
            "used": 8388608,
            "percent": 50.0
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
            with open(log_file_path, 'r') as file:
                return file.readlines()
        return []


@pytest.fixture
def test_app():
    """Create a test application with mocked monitor"""
    app = create_app()
    app.state.monitortask = MonitorTaskFake()
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
    """Test CPU usage endpoint"""
    response = client.get("/metrics/v1/cpu/usage")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 0, "usage": "10"},
        {"id": 1, "usage": "12"}
    ]


def test_get_cpu_core(client):
    """Test CPU core endpoint"""
    response = client.get("/metrics/v1/cpu/core")
    assert response.status_code == 200
    assert response.json() == {
        "processor_name": "Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz",
        "number_of_cores": 2,
        "frequency": 1800.0
    }


def test_get_disk_usage(client):
    """Test disk usage endpoint"""
    response = client.get("/metrics/v1/disk/usage")
    assert response.status_code == 200
    assert response.json() == {
        "total": 250790436864,
        "used": 100316192768,
        "free": 150474244096,
        "percent": 40.0
    }

def test_get_ram_usage(client):
    """Test RAM usage endpoint"""
    response = client.get("/metrics/v1/ram/usage")
    assert response.status_code == 200
    assert response.json()=={
        "total": 16777216,
            "available": 8388608,
            "used": 8388608,
            "percent": 50.0
    }

def test_get_log_data(client):
    """Test log data endpoint"""
    response = client.get("/metrics/v1/log/logs")
    assert response.status_code == 200
    assert response.json() == {
        "nbip": 5,
        "failed": 7,
        "succeed": 20,
        "nbwebsites": {
            "Home": 6,
            "/page1": 6,
            "/page2": 8,
            "/page3": 7
        },
        "ip_visits": {
            "192.168.1.10": ["Home", "/page1", "/page3", "Home", "Home", "/page1"],
            "10.0.0.1": ["/page2", "/page1", "/page3", "/page2", "/page1", "/page2"],
            "172.16.0.1": ["/page2", "Home", "/page3", "/page1", "Home"],
            "203.0.113.1": ["/page2", "/page3", "/page1", "/page3", "/page2"],
            "198.51.100.1": ["/page2", "Home", "/page3", "/page2", "/page3"]
        }
    }

def test_get_recent_logs_with_correct_data(client):
    """Test recent logs endpoint with correct data"""
    response = client.get("/metrics/v1/log/logs/recent")
    assert response.status_code == 200
    assert len(response.json()) == 5  
    assert response.json() == [
        {
            "ip": "172.16.0.1",
            "time": "[08/Jan/2020:11:15:43 +0000]",
            "request_method": "GET",
            "request_url": "/",
            "status": "200"
        },
        {
            "ip": "203.0.113.1",
            "time": "[08/Jan/2020:13:50:11 +0000]",
            "request_method": "GET",
            "request_url": "/page2",
            "status": "200"
        },
        {
            "ip": "198.51.100.1",
            "time": "[09/Jan/2020:07:40:50 +0000]",
            "request_method": "GET",
            "request_url": "/page3",
            "status": "404"
        },
        {
            "ip": "192.168.1.10",
            "time": "[09/Jan/2020:09:25:25 +0000]",
            "request_method": "GET",
            "request_url": "/page1",
            "status": "200"
        },
        {
            "ip": "10.0.0.1",
            "time": "[09/Jan/2020:12:12:49 +0000]",
            "request_method": "GET",
            "request_url": "/page2",
            "status": "200"
        }
    ]

def test_get_connected_users(client):
    """Test the connected users endpoint"""
    response = client.get("/metrics/v1/users/connected")
    assert response.status_code == 200
    assert response.json() == ["user1", "user2", "user3"]
