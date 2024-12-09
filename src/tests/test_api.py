"""This module defines tests for the API endpoints"""
import pytest
from fastapi.testclient import TestClient
from domain.services.logservice import count_log, log_parser
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
        self.processor_name = "Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz"
        self.cpu_frequency = 1800.0

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
    

LOG = (
    '192.168.240.50 - - [08/Dec/2023:08:55:20 +0000] "GET / HTTP/1.0" '
    '200 15075 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"'
)

result_log = ['192.168.240.50','[08/Dec/2023:08:55:20 +0000]','GET', '/ HTTP/1.0','200']

def test_parsing():
    """
    Test case for parsing a log using `log_parser`.

    This function tests the `log_parser` function by passing a log message
    (`LOG`) and checks if the returned result matches the `result_log`.

    Raises:
        AssertionError: If the parsed result does not match the expected result.
    """
    result = log_parser(LOG)
    print(result)
    print(result_log)
    assert result == result_log

def test_count_log() :
    """
    Test case for counting logs in a file.

    This function tests the `count_log` function by providing a file path
    and asserts the counts of unique IPs, successful requests, failed requests,
    and page visit counts against expected values.

    Raises:
        AssertionError: If the counts of IPs, successful requests, failed requests,
                        or page visits do not match the expected values.
    """
    result = count_log("src/logs/wordpress.log")
    assert result['total_ip'] == 5
    assert result['good'] == 20
    assert result['error'] == 7
    assert result['total_pages'], {
                'Home' : 6,
                '/page1': 6,
                '/page2': 8,
                '/page3': 7
            }

