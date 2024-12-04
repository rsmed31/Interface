"""This module defines tests for the API endpoints"""
import pytest
from fastapi.testclient import TestClient
from server import create_app
from monitor import MonitorTask


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

    def monitor(self):
        """Mock monitor method"""
        pass

    def get_disk_usage(self):
        """Return fake disk stats"""
        return self.disk_usage


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
    assert response.json() == {"number": 2}


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
    
