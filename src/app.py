from fastapi import BackgroundTasks, FastAPI
from src.execution_manager import create_execution, delete_execution, get_execution_result, get_execution_status
from src.model.execution_input import ExecutionInput
from src.model.job import Job
import json

with open('src/statics/api-spec.json', 'r') as json_file:
    api_spec = json.load(json_file)

app = FastAPI(
  title="Local PlanQK Service",
  version="1.0",
)

@app.get('/', summary="Health checking endpoint", tags=["Status API"], responses=api_spec['paths']['/']['get']['responses'])
def health_check():
    return ({"status": "Service is up and running"})

@app.post('/', summary="Asynchronous execution of the service", tags=["Service API"], responses=api_spec['paths']['/']['post']['responses'])
async def create(input: ExecutionInput, background_tasks: BackgroundTasks) -> Job:
    return create_execution(input, background_tasks)

@app.get('/{id}', summary="Check execution status", tags=["Service API"], responses=api_spec['paths']['/{id}']['get']['responses'])
def get_status(id) -> Job:
    return get_execution_status(id)

@app.get('/{id}/result', summary="Get the result of an execution", tags=["Service API"], responses=api_spec['paths']['/{id}/result']['get']['responses'])
def get_result(id):
    return get_execution_result(id)

@app.get('/{id}/interim-results', summary="Get the last or a list of interim results of an execution", tags=["Service API"], responses=api_spec['paths']['/{id}/interim-results']['get']['responses'])
def get_interim_results(id):
    return []

@app.put('/{id}/cancel', summary="Cancel an execution", tags=["Service API"], responses=api_spec['paths']['/{id}/cancel']['put']['responses'])
def delete(id):
    delete_execution(id)
