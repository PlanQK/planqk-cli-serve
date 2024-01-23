import base64
import json


def json_to_dict(value: str, base64_encoded: bool) -> dict:
    if value is None:
        return {}
    decoded_value = value
    if base64_encoded:
        try:
            decoded_value = base64.urlsafe_b64decode(value).decode("utf-8")
        except Exception as e:
            raise ValueError(f"Error decoding Base64 string: {e}")
    try:
        return json.loads(decoded_value)
    except Exception as e:
        raise ValueError(f"Error parsing JSON string: {e}")

def to_json(obj: any):
    return json.dumps(obj, default=lambda o: getattr(o, "__dict__", str(o)), sort_keys=True, indent=2)
