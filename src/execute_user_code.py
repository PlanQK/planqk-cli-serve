import traceback
from typing import Optional, Any

from loguru import logger

from src.user_code_runner import run_user_code


def execute_user_code(input_data: Optional[dict], input_params: Optional[dict], entry_point: str) -> Any:
    if input_data is None:
        input_data = dict()
    if input_params is None:
        input_params = dict()
    entry_point_arguments = {"kwargs": {
        "data": input_data,
        "params": input_params,
    }}

    try:
        return run_user_code(entry_point=entry_point, entry_point_arguments=entry_point_arguments)
    except Exception as e:
        logger.error(f"Error executing user code: {e}")
        traceback.print_exc()
        raise e
