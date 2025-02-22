"""
This module defines a controller class for fetching Logs from a monitoring task.
"""

import os
from domain.models import Log
from pathlib import Path
import apache_log_parser
from typing import List, Dict

log_format = '%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i"'
parser = apache_log_parser.make_parser(log_format)


def log_parser(log_entry):
    parsed_data = parser(log_entry)
    result_log = [
        parsed_data.get("remote_host", ""),  # Extract remote host (IP address)
        parsed_data.get("time_received", ""),
        parsed_data.get("request_method", ""),
        parsed_data.get("request_url", ""),
        parsed_data.get("status", ""),
    ]
    return result_log


def count_log(log_file: Path) -> Dict:
    unique_ips = set()
    cpt_404 = 0
    cpt_200 = 0
    page_visits = {}
    ip_visits = {}  # New dictionary to track IP visits

    try:
        with log_file.open("r") as file:
            for line in file:
                try:
                    log_entry = log_parser(line)
                    ip = log_entry[0]

                    # Check if the IP address is not '127.0.0.1'
                    if ip != "127.0.0.1":
                        status = log_entry[4]
                        request_method = log_entry[2]
                        request_url = log_entry[3]
                        path = request_url.split(" ", 1)[0]

                        if path in ("/", "/?p=1", "/?page_id=2"):
                            if path == "/":
                                path = "Home"
                            elif path == "/?p=1":
                                path = "Sample Page"
                            else:
                                path = "Welcome to Wordpress"

                        # Track page visits
                        page_visits[path] = page_visits.get(path, 0) + 1

                        # Track IP visits
                        if ip not in ip_visits:
                            ip_visits[ip] = []
                        ip_visits[ip].append(path)

                        if request_method == "GET":
                            if status == "404":
                                cpt_404 += 1
                            elif status == "200":
                                cpt_200 += 1
                            unique_ips.add(ip)
                except Exception as e:
                    # Log the error and continue with the next line
                    error_message = f"Error parsing line: {line.strip()}. Error: {e}"
                    with open("erreur.log", "a") as error_file:
                        error_file.write(error_message + "\n")

        return {
            "total_ip": len(unique_ips),
            "good": cpt_200,
            "error": cpt_404,
            "total_pages": page_visits,
            "ip_visits": ip_visits,  # Return IP visits
        }

    except FileNotFoundError as e:
        error_message = f"Le fichier {log_file} n'a pas été trouvé. Erreur : {e}"
        with open("erreur.log", "a") as error_file:
            error_file.write(error_message + "\n")

        return {
            "total_ip": 0,
            "good": 0,
            "error": 0,
            "total_pages": {},
            "ip_visits": {},  # Return empty IP visits
        }
    except Exception as e:
        error_message = (
            f"Une erreur s'est produite lors de la lecture du fichier {log_file}. "
            f"Erreur : {e}"
        )
        with open("erreur.log", "a") as error_file:
            error_file.write(error_message + "\n")

        return {
            "total_ip": 0,
            "good": 0,
            "error": 0,
            "total_pages": {},
            "ip_visits": {},  # Return empty IP visits
        }


def get_last_logs(count: int, log_file: Path) -> List[Dict]:
    try:
        with log_file.open("r") as file:
            lines = file.readlines()
            last_lines = lines[-count:]
            entries = []
            for line in last_lines:
                try:
                    log_entry = log_parser(line)
                    entry = {
                        "ip": log_entry[0],
                        "time": log_entry[1],
                        "request_method": log_entry[2],
                        "request_url": log_entry[3],
                        "status": log_entry[4],
                    }
                    entries.append(entry)
                except Exception as e:
                    error_message = f"Error parsing line: {line.strip()}. Error: {e}"
                    with open("erreur.log", "a") as error_file:
                        error_file.write(error_message + "\n")
            return entries
    except Exception as e:
        # Handle exceptions as needed
        error_message = (
            f"Une erreur s'est produite lors de la lecture du fichier {log_file}. "
            f"Erreur : {e}"
        )
        with open("erreur.log", "a") as error_file:
            error_file.write(error_message + "\n")
        return []


class LogService:

    def __init__(self, log_path: str = None):
        self.log_path = (
            Path(log_path)
            if log_path
            else Path(os.getenv("LOG_PATH", "/var/log/apache2/access.log"))
        )

    async def get_log(self) -> Log:
        result = count_log(self.log_path)
        return Log(
            nbip=result["total_ip"],
            succeed=result["good"],
            failed=result["error"],
            nbwebsites=result["total_pages"],
            ip_visits=result["ip_visits"],  # Include IP visits in the response
        )

    async def get_recent_logs(self, count: int) -> List[Dict]:
        result = get_last_logs(count, self.log_path)
        return result

    def __str__(self):
        return self.__class__.__name__
