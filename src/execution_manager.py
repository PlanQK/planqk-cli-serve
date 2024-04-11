import os
import traceback
import uuid
from typing import Optional

from fastapi import HTTPException
from loguru import logger

from src.TaskExecutor import TaskExecutor
from src.execute_user_code import execute_user_code
from src.job_manager import create_job, delete_job, update_job_by_status
from src.model.execution_input import ExecutionInput
from src.model.execution_status import ExecutionStatus
from src.user_code_runner import run_user_code

executor = TaskExecutor()


def update_job(key, future):
    if not future:
        raise HTTPException(status_code=404, detail="Execution does not exist")

    if not future.done():
        executionStatus = ExecutionStatus.RUNNING
    elif future.cancelled():
        executionStatus = ExecutionStatus.CANCELLED
    elif future.exception() is not None:
        executionStatus = ExecutionStatus.FAILED
    else:
        executionStatus = ExecutionStatus.SUCCEEDED

    return update_job_by_status(key, executionStatus)


def create_execution(input: ExecutionInput):
    id = str(uuid.uuid4())
    entry_point = os.environ.get("ENTRY_POINT", "user_code.src.program:run")
    executor.submit(execute_user_code, input.data, input.params, entry_point, id, lambda f: update_job(id, f))
    return create_job(id)


def get_execution_status(id):
    future = executor.get(id)
    return update_job(id, future)


def get_execution_result(id):
    future = executor.get(id)
    if future is None:
        raise HTTPException(status_code=404, detail="Execution does not exist")

    if future.done():
        response = future.result()
        return response
    return (f"Current execution status is: {ExecutionStatus.RUNNING}")


def delete_execution(id):
    delete_job(id)
    executor.delete(id)
