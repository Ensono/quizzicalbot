from pydantic import BaseModel, model_validator
import base64
import datetime
import hashlib

class Document(BaseModel):

    id: str = ""
    path: str
    filename: str
    title: str
    url: str = ""
    content: str
    chunk_id: str = ""
    last_updated: str = ""

    @model_validator(mode="after")
    def validate_last_updated(cls, values):

        # Create an id for the document based on the path and filename
        hasher = hashlib.sha256()
        hasher.update(f"{values.path}/{values.filename}".encode("utf-8"))
        values.id = hasher.hexdigest()

        # Set the last_updated value if not set
        if values.last_updated == "":
            values.last_updated = datetime.datetime.utcnow().isoformat()

        return values

    def resolve_content(self, encoding):
        if encoding == "base64":
            self.content = base64.b64decode(self.content).decode("utf-8")
