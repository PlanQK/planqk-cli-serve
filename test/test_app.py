import os

import pytest
from busypie import wait, SECOND
from fastapi.testclient import TestClient

from src.app import app
from src.model.execution_status import ExecutionStatus

client = TestClient(app)


def has_job_finished(job_id):
    response = client.get(f'/{job_id}')
    job_status = response.json()['status']
    return (job_status == ExecutionStatus.FAILED
            or job_status == ExecutionStatus.SUCCEEDED
            or job_status == ExecutionStatus.CANCELLED)


@pytest.fixture(autouse=True)
def my_setup_and_tear_down():
    os.environ["ENTRY_POINT"] = ""
    del os.environ["ENTRY_POINT"]


def test_health_check():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"status": "Service is up and running"}


def test_create_job_with_string_input():
    input_data = {
        "data": {"test_data": "test_data_value2"},
        "params": {"test_param": "test_param_value2"}
    }
    response = client.post('/', json=input_data)

    assert response.status_code == 201
    assert response.json()['status'] == ExecutionStatus.PENDING
    assert response.json()['id'] is not None


def test_create_job_with_array_input():
    input_data = {
        "data": {"value": ["abc", "dce"]},
        "params": {"value2": ["abc", "dce"]}
    }

    response = client.post('/', json=input_data)

    assert response.status_code == 201
    assert response.json()['status'] == ExecutionStatus.PENDING
    assert response.json()['id'] is not None


def test_get_job_status_when_no_execution():
    response = client.get(f'/123')
    assert response.status_code == 404


def test_get_job_status_with_valid_execution():
    response = client.post('/', json={"data": {}, "params": {}})

    assert response.status_code == 201
    assert response.json()['status'] == ExecutionStatus.PENDING
    job_id = response.json()['id']
    assert job_id is not None

    wait().at_most(2, SECOND).until(lambda: has_job_finished(job_id))

    response = client.get(f'/{job_id}')
    assert response.status_code == 200
    assert response.json()['status'] == ExecutionStatus.SUCCEEDED


def run_exception(**kwargs):
    raise ValueError("This is a custom error message")


def test_get_job_status_with_invalid_execution():
    os.environ["ENTRY_POINT"] = "test.test_app:run_exception"

    response = client.post('/', json={"data": {}, "params": {}})

    assert response.status_code == 201
    assert response.json()['status'] == ExecutionStatus.PENDING
    job_id = response.json()['id']
    assert job_id is not None

    wait().at_most(2, SECOND).until(lambda: has_job_finished(job_id))

    response = client.get(f'/{job_id}')
    assert response.status_code == 200
    assert response.json()['status'] == ExecutionStatus.FAILED


def test_get_job_result_with_valid_execution():
    response = client.post('/', json={"data": {}, "params": {}})

    assert response.status_code == 201
    assert response.json()['status'] == ExecutionStatus.PENDING
    job_id = response.json()['id']
    assert job_id is not None

    wait().at_most(2, SECOND).until(lambda: has_job_finished(job_id))

    response = client.get(f'/{job_id}/result')
    assert response.status_code == 200
    assert response.json()['data'] is not None


def test_get_job_result_with_invalid_execution():
    os.environ["ENTRY_POINT"] = "test.test_app:run_exception"

    response = client.post('/', json={"data": {}, "params": {}})

    assert response.status_code == 201
    assert response.json()['status'] == ExecutionStatus.PENDING
    job_id = response.json()['id']
    assert job_id is not None

    wait().at_most(2, SECOND).until(lambda: has_job_finished(job_id))

    response = client.get(f'/{job_id}/result')
    assert response.status_code == 404
