import pytest

from src.execute_user_code import execute_user_code


def run_valid(**kwargs):
    return {"result": True}


def run_exception(**kwargs):
    raise Exception()


def test_execute_user_code_with_valid_response():
    entry_point = "test.test_execute_user_code:run_valid"
    response = execute_user_code({}, {}, entry_point)

    assert response == {"result": True}


def test_execute_user_code_with_exception():
    entry_point = "test.test_execute_user_code:run_exception"

    with pytest.raises(Exception):
        execute_user_code({}, {}, entry_point)


def test_execute_user_code_with_invalid_entry_point():
    entry_point = "test.test_execute_user_code:invalid_entry_point"

    with pytest.raises(Exception):
        execute_user_code({}, {}, entry_point)


def test_execute_user_code_with_null_entry_point():
    with pytest.raises(Exception):
        execute_user_code({}, {}, None)
