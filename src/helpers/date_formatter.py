from datetime import datetime

from fastapi import HTTPException


def format_timestamp(timestamp: float | None):
    if timestamp is None:
        return None
    try:
        timestamp_datetime = datetime.fromtimestamp(timestamp)
        return timestamp_datetime.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error formatting timestamp: {str(e)}")
