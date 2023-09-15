from pydantic import BaseModel

class ResponseObj(BaseModel):
    error: bool = False
    message: str = ""
    name: str = ""
    status: bool = False

    def set(self, error: bool, message: str, name: str = "", status: bool = False):
        self.error = error
        self.message = message
        self.name = name
        self.status = status