"""This module defines a `MonitorTask` class for monitoring metrics on a host."""

import time
import psutil
import platform
import os
from domain.services.logservice import LogService


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
        self.ram_usage = {}
        self.logservice = LogService(
            log_path=os.getenv("LOG_PATH", "/var/log/apache2/access.log")
        )

    def monitor(self):
        """Continuously monitor and store the result in an attribute."""
        while True:
            self.cpu_percent = psutil.cpu_percent(percpu=True)
            self.update_disk_usage()
            self.update_ram_usage()
            time.sleep(self.interval)

    def __str__(self) -> str:
        return f"MonitorTask(interval = {self.interval})"

    def update_disk_usage(self):
        """Fetch disk usage statistics."""
        disk_info = psutil.disk_usage("/")
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

    def update_ram_usage(self):
        """Fetch RAM usage statistics."""
        ram_info = psutil.virtual_memory()
        self.ram_usage = {
            "total": ram_info.total,
            "available": ram_info.available,
            "used": ram_info.used,
            "percent": ram_info.percent,
        }

    def get_ram_usage(self):
        """Return the latest RAM usage stats."""
        if not hasattr(self, "ram_usage"):
            self.update_ram_usage()
        return self.ram_usage

    def get_processor_name(self) -> str:
        """Fetch the processor name."""
        return platform.processor()

    def get_cpu_frequency(self) -> float:
        """Fetch the CPU frequency in MHz."""
        return psutil.cpu_freq().current

    def get_connected_users(self):
        """Return connected users using psutil.users()."""
        connected_users = []
        for user in psutil.users():
            user_info = (
                f"{user.name} {user.terminal} {user.host or ''} "
                f"{time.strftime('%Y-%m-%d %H:%M', time.localtime(user.started))}"
            )
            connected_users.append(user_info)
        return connected_users
