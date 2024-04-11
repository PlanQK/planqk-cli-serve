from pydantic import BaseModel, Field

from src.model.execution_status import ExecutionStatus


class Job(BaseModel):
    id: str = Field(examples=["87cb778e-ac43-11ec-b909-0242ac120002"])
    status: ExecutionStatus = Field(examples=["SUCCEEDED"])
    created_at: str = Field(examples=["2022-04-01 12:00:00"])
    started_at: str = Field(None, examples=["2022-04-01 12:00:00"])
    ended_at: str = Field(None, examples=["2022-04-01 12:00:00"])

    model_config = {
        "use_enum_values": True
    }
