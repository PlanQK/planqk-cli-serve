from pydantic import BaseModel
from typing import Dict, Any

class ResponseHandler(BaseModel):
    result: Dict[str, Any]
    metadata: Dict[str, Any]

    def __init__(self, result, metadata):
        super()
        self.result = result
        self.metadata = metadata
