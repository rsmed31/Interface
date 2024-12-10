"""
This module defines the schema for log-related data.
"""
from pydantic import BaseModel
from typing import Dict, List



class GetLogResponseSchema(BaseModel):
    """
    Pydantic schema for representing log response data.

    Attributes:
        nbip (int): Number of unique IP addresses.
        failed (int): Number of failed requests.
        succeed (int): Number of successful requests.
        nbwebsites (Dict[str, int]): Number of visits per website.
        ip_visits (Dict[str, List[str]]): IP visits.
    """
    nbip: int
    failed: int
    succeed: int
    nbwebsites: Dict[str, int]
    ip_visits: Dict[str, List[str]]

