from typing import Dict, Any, Optional

from pydantic import BaseModel, Field


class ExecutionInput(BaseModel):
    data: Optional[Dict[str, Any]] = Field(None)
    params: Optional[Dict[str, Any]] = Field(None)
