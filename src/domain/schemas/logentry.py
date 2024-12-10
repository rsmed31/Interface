from pydantic import BaseModel

class LogEntrySchema(BaseModel):
    ip: str
    time: str
    request_method: str
    request_url: str
    status: str