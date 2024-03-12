from fastapi.testclient import TestClient

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.app import app
from src.model.execution_status import ExecutionStatus

client = TestClient(app)

def set_entry_point(entry_point):
    os.environ["ENTRY_POINT"] = entry_point
    
def test_health_check():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"status": "Service is up and running"}

def test_create_with_string_input_data():
    input_data = {
        "data": {"test_data": "test_data_value2"},
        "params": {"test_param": "test_param_value2"}
    }
    response = client.post('/', json=input_data)

    assert response.status_code == 200
    assert response.json()['status'] == ExecutionStatus.PENDING
    assert response.json()['id'] is not None
    
def test_create_with_object_input_data():    
    input_data = {
        "data": {"value" : ["abc", "dce"]},
        "params": {"value2" : ["abc", "dce"]}
    }
    
    response = client.post('/', json=input_data)

    assert response.status_code == 200
    assert response.json()['status'] == ExecutionStatus.PENDING
    assert response.json()['id'] is not None

def test_create_with_invalid_input_data():    
    input_data = {
    }
    
    response = client.post('/', json=input_data)

    assert response.status_code == 422
    
def test_get_status_throw_404_when_missing_execution():
    # given
    set_entry_point("test/user_code.valid.src.program:run")

    # when
    response = client.get(f'/123')
    # then
    assert response.status_code == 404

def test_get_status_with_valid_execution():
    # given
    set_entry_point("test/user_code.valid.src.program:run")

    input_data = {
        "data": {},
        "params": {}
    }

    response = client.post('/', json=input_data)

    assert response.status_code == 200
    assert response.json()['status'] == ExecutionStatus.PENDING
    id = response.json()['id']
    assert id is not None
    # when
    response = client.get(f'/{id}')
    # then
    assert response.status_code == 200
    assert response.json()['status'] == ExecutionStatus.SUCCEEDED or response.json()['status'] == ExecutionStatus.RUNNING

def test_get_status_with_invalid_execution():
    # given
    set_entry_point("test/user_code.invalid.src.program:run")

    input_data = {
        "data": {},
        "params": {}
    }

    response = client.post('/', json=input_data)

    assert response.status_code == 200
    assert response.json()['status'] == ExecutionStatus.PENDING
    id = response.json()['id']
    assert id is not None
    # when
    response = client.get(f'/{id}')
    # then
    assert response.status_code == 200
    assert response.json()['status'] == ExecutionStatus.FAILED or response.json()['status'] == ExecutionStatus.RUNNING

def test_get_result_throw_404_when_missing_execution():
    # given
    set_entry_point("test/user_code.valid.src.program:run")

    # when
    response = client.get(f'/123/result')
    # then
    assert response.status_code == 404
    
def test_get_result_of_valid_execution():
    # given
    set_entry_point("test/user_code.valid.src.program:run")

    input_data = {
        "data": {},
        "params": {}
    }

    response = client.post('/', json=input_data)

    assert response.status_code == 200
    assert response.json()['status'] == ExecutionStatus.PENDING
    id = response.json()['id']
    assert id is not None
    # when
    response = client.get(f'/{id}/result')
    # then
    assert response.status_code == 200
    assert response.json()['result'] is not None

def test_get_result_of_invalid_execution():
    # given
    set_entry_point("test/user_code.invalid.src.program:run")

    input_data= {
        "data": {},
        "params": {}
    }

    response = client.post('/', json=input_data)

    assert response.status_code == 200
    assert response.json()['status'] == ExecutionStatus.PENDING
    id = response.json()['id']
    assert id is not None
    # when
    response = client.get(f'/{id}/result')
    # then
    assert response.status_code == 500

def test_delete_execution():
    # given
    set_entry_point("test/user_code.valid.src.program:run")

    input_data = {
        "data": {},
        "params": {}
    }

    response = client.post('/', json=input_data)

    assert response.status_code == 200
    assert response.json()['status'] == ExecutionStatus.PENDING
    id = response.json()['id']
    assert id is not None
    
    response = client.get(f'/{id}')
    assert response.status_code == 200
    assert response.json()['status'] == ExecutionStatus.RUNNING or response.json()['status'] == ExecutionStatus.SUCCEEDED
    
    # when
    response = client.delete(f'/{id}/cancel')
    
    # then
    response = client.get(f'/{id}')
    assert response.status_code == 404
    
def test_delete_execution_throw_404_when_missing_execution():
    # given
    set_entry_point("test/user_code.valid.src.program:run")

    # when
    response = client.delete('/123/cancel')
    # then
    assert response.status_code == 404
    

def test_delete_execution_with_wrong_id():
    # given
    set_entry_point("test/user_code.valid.src.program:run")

    # when
    response = client.delete('/123/cancel')
    
    # then
    assert response.status_code == 404
    
def test_get_interim_result():
    # given
    set_entry_point("test/user_code.valid.src.program:run")

    response = client.get(f'/{id}/interim-results')
    
    assert response.json() == []
