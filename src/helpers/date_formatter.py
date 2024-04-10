from datetime import datetime

from fastapi import HTTPException


def format_timestamp(timestamp_float):
    try:
        timestamp_datetime = datetime.fromtimestamp(timestamp_float)
        return timestamp_datetime.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error formatting timestamp: {str(e)}")
