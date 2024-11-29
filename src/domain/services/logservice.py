"""
This module defines a controller class for fetching Logs from a monitoring task.
"""
from domain.models import Log
from urllib.parse import urlparse
import apache_log_parser # type: ignore

log_format = '%v %h %l %u %t "%m %r" %>s %b "%{Referer}i" "%{User-Agent}i"'
parser = apache_log_parser.make_parser(log_format)

def log_parser(log_entry):
    parsed_data = parser(log_entry)
    result_log = [
        parsed_data.get('remote_host', ''),
        parsed_data.get('time_received', ''),
        parsed_data.get('method', ''),
        parsed_data.get('request_first_line', ''),
        parsed_data.get('status', ''),
    ]
    return result_log

def count_log(log_file):
    unique_ips = set()
    cpt_404 = 0
    cpt_200 = 0
    page_visits = {}

    try:
        with open(log_file, 'r') as file:
            for line in file:
                log_entry = log_parser(line)
                ip = log_entry[0]

                # Check if the IP address is not '127.0.0.1'
                if ip != '127.0.0.1':
                    status = log_entry[4]
                    request_method = log_entry[2]
                    request_url = log_entry[3]
                    path = request_url.split(' ', 1)[0]

                    if path == "/" or path == "/?p=1" or path == "/?page_id=2":
                        if path == "/":
                            path = "Home"
                        elif path == "/?p=1":
                            path = "Sample Page"
                        else:
                            path = "Welcome to Wordpress"

                        page_visits[path] = page_visits.get(path, 0) + 1
                        if request_method == 'GET':
                            if status == '404':
                                cpt_404 += 1
                            elif status == '200':
                                cpt_200 += 1
                            unique_ips.add(ip)

        return {'total_ip': len(unique_ips), 'good': cpt_200, 'error': cpt_404, 'total_pages': page_visits}

    except FileNotFoundError as e:
        error_message = f"Le fichier {log_file} n'a pas été trouvé. Erreur : {e}"

        with open('erreur.log', 'a') as error_file:
            error_file.write(error_message + '\n')

        return {'total_ip': 0, 'good': 0, 'error': 0, 'total_pages': {}}


class LogService:

    def __init__(self):
        ...

    async def get_log(self) -> Log:
        result = count_log("/var/log/apache2/other_vhosts_access.log")
        return Log(
            nbip=result['total_ip'],
            succeed=result['good'],
            failed=result['error'],
            nbwebsites=result['total_pages'])

    def __str__(self):
        return self.__class__.__name__
