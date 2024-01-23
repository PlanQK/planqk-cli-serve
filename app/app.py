import time
from datetime import datetime
import os
from fastapi import BackgroundTasks, FastAPI, HTTPException

from typing import Optional
from app.helpers.date_formatter import format_timestamp
from app.model.execution_input import ExecutionInput
from app.model.execution_status import ExecutionStatus
from app.model.job import Job
from app.user_code_runner import run_user_code
from app.helpers.json import to_json
import uuid
import concurrent.futures

jobs = {}
executions = {}

app = FastAPI(title=__name__)

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
    with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(execute_user_code, params, data)
            executions[key] = future

@app.get('/')
def health_check():
    return ({"status": "Service is up and running"})

@app.post('/')
async def start_execution(input: ExecutionInput, background_tasks: BackgroundTasks):
    job_id=str(uuid.uuid4())

    try:
        background_tasks.add_task(submit_execution, job_id, input.params, input.data)

        job = Job(id = job_id, status = ExecutionStatus.PENDING, createdAt = format_timestamp(time.time()))
        jobs[job_id] = job
        return to_json(job)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get('/{id}')
def get_execution_status(id):
    future = executions.get(id)
    job = jobs.get(id)

    if future is None or job is None :
        raise HTTPException(status_code=404, detail="Execution does not exist")

    if future.done():
        if job:
            job.status = ExecutionStatus.COMPLETED
        else: 
            job = Job(id = id, status = ExecutionStatus.COMPLETED, createdAt = format_timestamp(time.time()))
        
        jobs[id] = job
        return to_json(job)

    jobs[id] = Job(id = id, status = ExecutionStatus.IN_PROGRESS, createdAt = format_timestamp(time.time()))

    return to_json(job)

@app.get('/{id}/result')
def get_result(id):
    future = executions.get(id)
    if future is None:
        raise HTTPException(status_code=404, detail="Execution does not exist")

    if future.done():
        response = future.result()
        return response
    return (f"Current execution status is: {to_json(ExecutionStatus.IN_PROGRESS)}") 

@app.delete('/{id}/cancel')
def get_result(id):
    del jobs[id]
    del executions[id]
