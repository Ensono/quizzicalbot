from pydantic import BaseModel

class ResponseObj(BaseModel):
    error: bool = False
    message: str = ""
    name: str = ""
    status: bool = False
    duration: float = 0.0