from pydantic import BaseModel

from app.model.execution_status import ExecutionStatus

class Job(BaseModel):
    id: str
    status: ExecutionStatus
    createdAt: float
