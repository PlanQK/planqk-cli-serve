from pydantic import BaseModel, Extra


class ExecutionOutput(BaseModel):
    model_config = {
        "extra": Extra.allow
    }
