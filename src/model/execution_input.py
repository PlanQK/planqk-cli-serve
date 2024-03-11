from typing import Dict
from pydantic import BaseModel

class ExecutionInput(BaseModel):
    data: Dict[str, object]
    params: Dict[str, object]
    