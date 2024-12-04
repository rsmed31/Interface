"""This module defines a `MonitorTask` class for monitoring metrics on a host."""
import time
import psutil


class MonitorTask:
    """A class for monitoring metrics."""

    interval: int
    cpu_percent: list[float]
    num_cores: int
    disk_usage: dict

    def __init__(self) -> None:
        """
        Initialize the MonitorTask class.

        Add initialization tasks here like checks
        The monitoring interval is 3 seconds.
        """
        self.interval = 3
        self.num_cores = psutil.cpu_count(logical=False)
        self.cpu_percent = [0] * self.num_cores
        self.disk_usage = {}

    def monitor(self):
        """Continuously monitor and store the result in an attribute."""
        while True:
            self.cpu_percent = psutil.cpu_percent(percpu=True)
            self.update_disk_usage()
            time.sleep(self.interval)
            
    def __str__(self) -> str:
        return f"MonitorTask(interval = {self.interval})"

    def update_disk_usage(self):
        """Fetch disk usage statistics."""
        disk_info = psutil.disk_usage('/')
        self.disk_usage = {
            "total": disk_info.total,
            "used": disk_info.used,
            "free": disk_info.free,
            "percent": disk_info.percent,
        }
    def get_disk_usage(self):
        """Return the latest disk usage stats."""
        if not self.disk_usage:
         self.update_disk_usage()
        return self.disk_usage


