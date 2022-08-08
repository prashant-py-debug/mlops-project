import json

import requests

payload = json.dumps({"AT_1": 1.44, "AT_2": -0.144})
headers = {"Content-Type": "application/json"}


URL = "http://localhost:8000/prediction"
response = requests.request("POST", URL, headers=headers, data=payload)

expected = -1.0

actual = response.json

assert expected == actual
