import json
import os


from .program import run

logging_level = os.environ.get("LOG_LEVEL", "DEBUG")

with open(f"./input/data.json") as file:
    data = json.load(file)

with open(f"./input/params.json") as file:
    params = json.load(file)

response = run(data, params)

print()
print(response.to_json())
