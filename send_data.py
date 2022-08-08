import os
import json
import requests
import pandas as pd


DATA_PATH = os.getenv("data_path", "banana/banana.csv")
URL = os.getenv("url", "http://localhost:8000/prediction")


def send_requests():
    """sends continuous requests to api"""

    data = pd.read_csv(DATA_PATH)
    headers = {"Content-Type": "application/json"}

    for i in range(len(data)):
        at_1 = data.iloc[i, 0]
        at_2 = data.iloc[i, 1]
        payload = json.dumps({"AT_1": at_1, "AT_2": at_2})

        response = requests.request("POST", URL, headers=headers, data=payload)
        print(response)


if __name__ == "__main__":
    send_requests()
