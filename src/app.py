from fastapi import BackgroundTasks, FastAPI
from src.execution_manager import create_execution, delete_execution, get_execution_result, get_execution_status, submit_execution
from src.model.execution_input import ExecutionInput

app = FastAPI(title=__name__)

@app.get('/')
def health_check():
    return ({"status": "Service is up and running"})

@app.post('/')
async def create(input: ExecutionInput, background_tasks: BackgroundTasks):
    return create_execution(input, background_tasks)

@app.get('/{id}')
def get_status(id):
    return get_execution_status(id)

@app.get('/{id}/result')
def get_result(id):
    return get_execution_result(id)

@app.delete('/{id}/cancel')
def delete(id):
    delete_execution(id)
    