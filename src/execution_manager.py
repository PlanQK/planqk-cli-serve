import os
from fastapi import BackgroundTasks
from src.model.execution_input import ExecutionInput
from typing import Optional
from fastapi import HTTPException
from src.model.execution_status import ExecutionStatus
from src.user_code_runner import run_user_code
import concurrent.futures

executions = {}

def submit_execution(key, params, data):
    with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(execute_user_code, params, data)
            executions[key] = future

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

def create_execution(execution_id, input: ExecutionInput, background_tasks: BackgroundTasks):
    background_tasks.add_task(submit_execution, execution_id, input.params, input.data)

def get_execution_status(id):
    future = executions.get(id)

    if future is None :
        raise HTTPException(status_code=404, detail="Execution does not exist")
    
    return future.done()

def get_execution_result(id):
    future = executions.get(id)
    if future is None:
        raise HTTPException(status_code=404, detail="Execution does not exist")

    if future.done():
        response = future.result()
        return response
    return (f"Current execution status is: {ExecutionStatus.IN_PROGRESS}")

def delete_execution(id):
    del executions[id]
