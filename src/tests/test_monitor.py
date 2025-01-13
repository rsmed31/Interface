import pytest
from monitor import MonitorTask
import psutil
import threading
import time
from unittest.mock import patch, Mock


@pytest.fixture
def mock_cpu_freq():
    with patch('psutil.cpu_freq', return_value=Mock(current=2500.0)) as mock:
        yield mock

@pytest.fixture
def mock_users():
    """Mock connected users data"""
    mock_data = [
        Mock(name='user1', terminal='pts/0', host='localhost', started=time.time()),
        Mock(name='user2', terminal='pts/1', host='remote', started=time.time())
    ]
    with patch('psutil.users', return_value=mock_data) as mock:
        yield mock

def test_monitor_task_init():
    """Test MonitorTask initialization"""
    monitor = MonitorTask()
    assert monitor.interval == 3
    assert monitor.num_cores == psutil.cpu_count(logical=False)
    assert len(monitor.cpu_percent) == monitor.num_cores
    assert isinstance(monitor.disk_usage, dict)
    assert isinstance(monitor.ram_usage, dict)

def test_update_disk_usage():
    """Test disk usage update"""
    monitor = MonitorTask()
    monitor.update_disk_usage()
    assert "total" in monitor.disk_usage
    assert "used" in monitor.disk_usage
    assert "free" in monitor.disk_usage
    assert "percent" in monitor.disk_usage
    
def test_update_ram_usage():
    """Test RAM usage update"""
    monitor = MonitorTask()
    monitor.update_ram_usage()
    assert "total" in monitor.ram_usage
    assert "available" in monitor.ram_usage
    assert "used" in monitor.ram_usage
    assert "percent" in monitor.ram_usage

def test_get_ram_usage():
    """Test RAM usage getter"""
    monitor = MonitorTask()
    # First ensure RAM usage is initialized
    monitor.update_ram_usage()
    ram_stats = monitor.get_ram_usage()
    
    # Test dictionary structure
    assert isinstance(ram_stats, dict)
    required_keys = ["total", "available", "used", "percent"]
    for key in required_keys:
        assert key in ram_stats, f"Missing key: {key}"
    
    # Test value types
    assert isinstance(ram_stats["total"], int)
    assert isinstance(ram_stats["available"], int) 
    assert isinstance(ram_stats["used"], int)
    assert isinstance(ram_stats["percent"], float)
    
    # Test logical constraints
    assert ram_stats["total"] > 0
    assert ram_stats["available"] >= 0
    assert ram_stats["used"] >= 0
    assert 0 <= ram_stats["percent"] <= 100
    
def test_get_disk_usage():
    """Test disk usage getter"""
    monitor = MonitorTask()
    disk_stats = monitor.get_disk_usage()
    assert isinstance(disk_stats, dict)
    assert all(key in disk_stats for key in ["total", "used", "free", "percent"])

def test_get_processor_name():
    """Test processor name getter"""
    mock_processor = "Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz"
    
    with patch('cpuinfo.get_cpu_info', return_value={"brand_raw": mock_processor}):
        monitor = MonitorTask()
        processor_name = monitor.get_processor_name()
        assert isinstance(processor_name, str)
        assert processor_name == mock_processor

def test_get_cpu_frequency(mock_cpu_freq):
    """Test CPU frequency getter"""
    monitor = MonitorTask()
    frequency = monitor.get_cpu_frequency()
    assert isinstance(frequency, float)
    assert frequency == 2500.0

def test_get_connected_users(mock_users):
    """Test connected users getter"""
    monitor = MonitorTask()
    users = monitor.get_connected_users()
    assert isinstance(users, list)
    assert len(users) == 2
    for user in users:
        assert isinstance(user, str)

def test_monitor_string_representation():
    """Test string representation"""
    monitor = MonitorTask()
    assert str(monitor) == f"MonitorTask(interval = {monitor.interval})"