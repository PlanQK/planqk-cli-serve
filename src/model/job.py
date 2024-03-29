from pydantic import BaseModel

from src.model.execution_status import ExecutionStatus

class Job(BaseModel):
    id: str
    status: ExecutionStatus
    createdAt: str
    startedAt: str
    endedAt: str = ""

    class Config:  
        use_enum_values = True
    