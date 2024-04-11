import logging
import os
import sys
import time
import uuid
from typing import List

from fastapi import FastAPI, Path, Query, BackgroundTasks
from loguru import logger

from src.helpers.date_formatter import format_timestamp
from src.helpers.logging import LogHandler
from src.job_executor import JobExecutor
from src.model.execution_input import ExecutionInput
from src.model.execution_output import ExecutionOutput
from src.model.execution_status import ExecutionStatus
from src.model.health_check import HealthCheck
from src.model.job import Job

app = FastAPI(
    title="Local PlanQK Service",
    version="1.0",
)

logging_level = os.environ.get("LOG_LEVEL", "DEBUG")
logging.getLogger().handlers = [LogHandler()]
logging.getLogger().setLevel(logging_level)
logger.configure(handlers=[{"sink": sys.stdout, "level": logging_level}])

job_executor = JobExecutor()


@app.get('/',
         tags=["Status API"],
         summary="Health checking endpoint")
def health_check() -> HealthCheck:
    return HealthCheck(status="Service is up and running")


@app.post('/',
          tags=["Service API"],
          summary="Asynchronous execution of the service",
          status_code=201)
async def create_job(execution_input: ExecutionInput, background_tasks: BackgroundTasks) -> Job:
    job_id = str(uuid.uuid4())
    background_tasks.add_task(job_executor.create_job, job_id, execution_input)
    return Job(id=job_id, status=ExecutionStatus.PENDING, created_at=format_timestamp(time.time()))


@app.get('/{id}',
         tags=["Service API"],
         summary="Check execution status")
def get_job_status(job_id: str = Path(alias="id", description="The ID of a certain execution")) -> Job:
    return job_executor.get_job_status(job_id)


@app.get('/{id}/result',
         tags=["Service API"],
         summary="Get the result of an execution")
def get_job_result(job_id: str = Path(alias="id", description="The ID of a certain execution")) -> ExecutionOutput:
    return job_executor.get_job_result(job_id)


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
def cancel_job(job_id: str = Path(alias="id", description="The ID of a certain execution")) -> Job:
    return job_executor.cancel_job(job_id)
