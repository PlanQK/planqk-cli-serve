from pydantic import BaseModel


class HealthCheck(BaseModel):
    status: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "Service is up and running",
                }
            ]
        }
    }
