from fastapi import HTTPException
from src.model.execution_status import ExecutionStatus
from src.helpers.date_formatter import format_timestamp
from src.model.job import Job
import time

jobs = {}

def create_job(job_id):
    job = Job(id = job_id, status = ExecutionStatus.PENDING, createdAt = format_timestamp(time.time()), startedAt = format_timestamp(time.time()))
    jobs[job_id] = job
    return job

def update_job_by_status(id, status: ExecutionStatus):
    job = jobs.get(id)
    if not job:
        raise HTTPException(status_code=404, detail="Execution does not exist")
    
    job.status = status

    if not status == ExecutionStatus.RUNNING:
        job.endedAt = format_timestamp(time.time())

    jobs[id] = job
    return job

def delete_job(id):
    if not jobs.get(id):
        raise HTTPException(status_code=404, detail="Execution does not exist")
    del jobs[id]
