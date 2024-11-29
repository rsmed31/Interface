"""
This module defines a data model for CPU information.
"""
from pydantic import BaseModel # type: ignore


# Log data model
class Log(BaseModel):
    """
    Pydantic data model for representing Log information.

    Attributes:
        nbip (int)
        failed (int)
        succed (int)
        nbwebsites (dict)
    """
    nbip: int # Number of IP addresses
    failed: int # Number of failed requests
    succeed: int # Number of successful requests
    nbwebsites: dict # Number of visits per website
