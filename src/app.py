from fastapi import BackgroundTasks, FastAPI
from src.execution_manager import create_execution, delete_execution, get_execution_result, get_execution_status
from src.model.execution_input import ExecutionInput
from src.job_manager import create_job, delete_job, update_job_status
import uuid

app = FastAPI(title=__name__)

@app.get('/')
def health_check():
    return ({"status": "Service is up and running"})

@app.post('/')
async def create(input: ExecutionInput, background_tasks: BackgroundTasks):
    id=str(uuid.uuid4())
    create_execution(id, input, background_tasks)
    return create_job(id)
    

@app.get('/{id}')
def get_status(id):
    isExecutionDone = get_execution_status(id)
    return update_job_status(id, isExecutionDone)

@app.get('/{id}/result')
def get_result(id):
    return get_execution_result(id)

@app.delete('/{id}/cancel')
def delete(id):
    delete_execution(id)
    delete_job(id)
    