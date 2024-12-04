from pydantic import BaseModel

class Log(BaseModel):
    """
    Pydantic data model for representing Log information.

    Attributes:
        nbip (int): Number of IP addresses
        failed (int): Number of failed requests
        succeed (int): Number of successful requests
        nbwebsites (dict): Number of visits per website
        ip_visits (dict): Mapping of IP addresses to visited pages
    """
    nbip: int
    failed: int
    succeed: int
    nbwebsites: dict
    ip_visits: dict  # New attribute to track IP visits