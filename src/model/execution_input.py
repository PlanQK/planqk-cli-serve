from typing import Dict, Any, Optional

from pydantic import BaseModel


class ExecutionInput(BaseModel):
    data: Optional[Dict[str, Any]]
    params: Optional[Dict[str, Any]]
