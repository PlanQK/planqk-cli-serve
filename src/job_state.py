import time
from concurrent.futures import Future

from src.helpers.date_formatter import format_timestamp
from src.model.execution_output import ExecutionOutput
from src.model.execution_status import ExecutionStatus
from src.model.job import Job


class JobState:
    def __init__(self, job_id: str, future: Future):
        self.job_id = job_id
        self.created_at = time.time()
        self.started_at = time.time()
        self.ended_at = None
        self.future = future
        self.future.add_done_callback(lambda f: self.__set_ended_at())

    def has_finished(self):
        return self.future.done()

    def get_status(self) -> Job:
        if self.future.exception() is not None:
            status = ExecutionStatus.FAILED
        elif self.future.cancelled():
            status = ExecutionStatus.CANCELLED
        elif self.future.done():
            status = ExecutionStatus.SUCCEEDED
        else:
            status = ExecutionStatus.RUNNING

        return Job(
            id=self.job_id,
            status=status,
            created_at=format_timestamp(self.created_at),
            started_at=format_timestamp(self.started_at),
            ended_at=format_timestamp(self.ended_at),
        )

    def get_result(self) -> ExecutionOutput | None:
        if self.future.exception() is not None:
            return None

        if self.has_finished():
            return self.future.result()
        return None

    def cancel(self):
        self.future.cancel()

    def __set_ended_at(self):
        self.ended_at = time.time()
