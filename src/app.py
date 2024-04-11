from typing import List

from fastapi import BackgroundTasks, FastAPI, Path, Query

from src.execution_manager import create_execution, delete_execution, get_execution_result, get_execution_status
from src.model.execution_input import ExecutionInput
from src.model.execution_output import ExecutionOutput
from src.model.health_check import HealthCheck
from src.model.job import Job

app = FastAPI(
    title="Local PlanQK Service",
    version="1.0",
)


@app.get('/',
         tags=["Status API"],
         summary="Health checking endpoint")
def health_check() -> HealthCheck:
    return HealthCheck(status="Service is up and running")


@app.post('/',
          tags=["Service API"],
          summary="Asynchronous execution of the service",
          status_code=201)
async def create(execution_input: ExecutionInput, background_tasks: BackgroundTasks) -> Job:
    return create_execution(execution_input, background_tasks)


@app.get('/{id}',
         tags=["Service API"],
         summary="Check execution status")
def get_status(job_id: str = Path(alias="id", description="The ID of a certain execution")) -> Job:
    return get_execution_status(job_id)


@app.get('/{id}/result',
         tags=["Service API"],
         summary="Get the result of an execution")
def get_result(job_id: str = Path(alias="id", description="The ID of a certain execution")) -> ExecutionOutput:
    return get_execution_result(job_id)


@app.get('/{id}/interim-results',
         tags=["Service API"],
         summary="Get the last or a list of interim results of an execution")
def get_interim_results(
        job_id: str = Path(alias="id", description="The ID of a certain execution"),
        last: bool = Query(
            False, description="Either true or false to show only the last or all interim results"
        )
) -> List[ExecutionOutput] | ExecutionOutput:
    return []


@app.put('/{id}/cancel',
         tags=["Service API"],
         summary="Cancel an execution")
def delete(job_id: str = Path(alias="id", description="The ID of a certain execution")) -> Job:
    delete_execution(job_id)
    return get_execution_status(job_id)
