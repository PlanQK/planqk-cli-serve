from typing import Dict
from pydantic import BaseModel

class ExecutionInput(BaseModel):
    data: Dict[str, str]
    params: Dict[str, str]
    