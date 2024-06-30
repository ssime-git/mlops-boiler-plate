import requests
from requests.auth import HTTPBasicAuth
import json

url = "http://localhost:8080/api/v1/dags/ci_pipeline/dagRuns"
payload = {
    "dag_run_id": "remotely-triggered",
}
headers = {
    'Content-Type': 'application/json',
}
auth = HTTPBasicAuth('airflow', 'airflow')

response = requests.post(url, headers=headers, data=json.dumps(payload), auth=auth)

if response.status_code == 200:
    print("POST request successful!")
    print("Response:", response.json())
else:
    print("Failed to make POST request")
    print("Status code:", response.status_code)
    print("Response:", response.text)