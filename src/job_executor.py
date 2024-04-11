import os
from concurrent.futures import ThreadPoolExecutor

from fastapi import HTTPException

from src.execute_user_code import execute_user_code
from src.job_state import JobState
from src.model.execution_input import ExecutionInput
from src.model.job import Job


class JobExecutor:
    def __init__(self):
        self.jobs = {}
        self.executor = ThreadPoolExecutor(max_workers=3)

    def create_job(self, job_id: str, execution_input: ExecutionInput) -> None:
        entry_point = os.environ.get("ENTRY_POINT", "user_code.src.program:run")
        future = self.executor.submit(execute_user_code, execution_input.data, execution_input.params, entry_point)

        job = JobState(job_id, future)
        self.jobs[job_id] = job

    def get_job_status(self, job_id: str) -> Job:
        job = self.jobs.get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Not found")

        return job.get_status()

    def get_job_result(self, job_id: str):
        job = self.jobs.get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Not found")

        result = job.get_result()
        if result is None:
            raise HTTPException(status_code=404, detail="Not found")

        return result

    def cancel_job(self, job_id: str):
        job = self.jobs.get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Not found")

        job.cancel()
        return job.get_status()
