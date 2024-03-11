import json
from fastapi.testclient import TestClient

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.app import app
from src.model.execution_status import ExecutionStatus
from src.model.job import Job

client = TestClient(app)

def test_health_check():
    response = client.get('/')
    assert response.status_code == 201
    assert response.json() == {"status": "Service is up and running"}

def test_create_with_string_dict_input_data():
    input_data = {
        "data": {"test_data": "test_data_value2"},
        "params": {"test_param": "test_param_value2"}
    }
    response = client.post('/', data=json.dumps(input_data))

    assert response.status_code == 200
    assert response.json()['status'] == ExecutionStatus.PENDING
    
def test_create_with_object_dict_input_data():    
    input_data = {
        "data": {"value" : ["abc", "dce"]},
        "params": {"value2" : ["abc", "dce"]},
    }
    
    response = client.post('/', data=json.dumps(input_data))

    assert response.status_code == 200
    assert response.json()['status'] == ExecutionStatus.PENDING
