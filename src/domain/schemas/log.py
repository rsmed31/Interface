"""
This module defines a data transfer model for a GetLogResponseSchema.
"""
from pydantic import BaseModel # type: ignore


class GetLogResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing Log information.

    Attributes:
        nbip (int)
        failed (int)
        succeed (int)
        nbwebsites (dict)
    """
    nbip: int # Number of IP addresses
    failed: int # Number of failed requests
    succeed: int # Number of successful requests
    nbwebsites: dict # Number of visits per website

