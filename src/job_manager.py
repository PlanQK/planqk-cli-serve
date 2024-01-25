from src.model.execution_status import ExecutionStatus
from src.helpers.date_formatter import format_timestamp
from src.model.job import Job
import time

jobs = {}

def create_job(job_id):
    job = Job(id = job_id, status = ExecutionStatus.PENDING, createdAt = format_timestamp(time.time()))
    jobs[job_id] = job
    return job

def update_job_status(id, isDone):
    job = jobs.get(id)

    if isDone:
        if job:
            job.status = ExecutionStatus.COMPLETED
        else: 
            job = Job(id = id, status = ExecutionStatus.COMPLETED, createdAt = format_timestamp(time.time()))
    elif not isDone and job:
        job.status = ExecutionStatus.IN_PROGRESS

    jobs[id] = job
    return job

def delete_job(id):
    del jobs[id]
