from pydantic import BaseModel, Field

from src.model.execution_status import ExecutionStatus


class Job(BaseModel):
    id: str = Field(examples=["87cb778e-ac43-11ec-b909-0242ac120002"])
    status: ExecutionStatus = Field(examples=["SUCCEEDED"])
    createdAt: str = Field(examples=["2022-04-01 12:00:00"])
    startedAt: str = Field(None, examples=["2022-04-01 12:00:00"])
    endedAt: str = Field(None, examples=["2022-04-01 12:00:00"])

    model_config = {
        "use_enum_values": True
    }
