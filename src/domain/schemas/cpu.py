"""
This module defines a data transfer model for a GetCpuResponseSchema.
"""
from pydantic import BaseModel


class GetCpuResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing CPU information.

    Attributes:
        id (int): The ID of the CPU data.
        usage (str): The CPU usage in string format.
    """

    id: int
    usage: str


class GetCpuCoreResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing CPU core information.

    Attributes:
        processor_name (str): The name of the processor.
        number_of_cores (int): The number of CPU cores.
        frequency (float): The frequency of the CPU in MHz.
    """

    processor_name: str
    number_of_cores: int
    frequency: float
