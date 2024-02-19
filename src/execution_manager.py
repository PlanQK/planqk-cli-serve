import os
from fastapi import BackgroundTasks
from src.TaskExecutor import TaskExecutor
from src.helpers.date_formatter import format_timestamp
from src.model.execution_input import ExecutionInput
from typing import Optional
from fastapi import HTTPException
from src.model.execution_status import ExecutionStatus
from src.user_code_runner import run_user_code
from src.job_manager import create_job, delete_job, update_job_by_status
import uuid

executor = TaskExecutor()

def update_job(key, future):
    if not future :
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

def execute_user_code(input_data: Optional[dict], input_params: Optional[dict]) -> any:
    entry_point = os.environ.get("ENTRY_POINT", "user_code.src.program:run")

    if input_data is None:
        input_data = dict()
    if input_params is None:
        input_params = dict()
    entry_point_arguments = {"kwargs": {
        "data": input_data,
        "params": input_params,
    }}
    try:
        return run_user_code(entry_point=entry_point, entry_point_arguments=entry_point_arguments)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

def submit_execution(key, params, data):
    executor.submit(execute_user_code, params, data, key, lambda f: update_job(key, f))

def create_execution(input: ExecutionInput, background_tasks: BackgroundTasks):
    id=str(uuid.uuid4())
    background_tasks.add_task(submit_execution, id, input.params, input.data)
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
