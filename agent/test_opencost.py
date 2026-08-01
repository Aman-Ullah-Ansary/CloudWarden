import requests
import json

url = "http://localhost:9091/model/allocation"

params = {
    "window": "today"
}

response = requests.get(url, params=params)

print("Status Code:", response.status_code)

try:
    data = response.json()
    print(json.dumps(data, indent=2))
except Exception:
    print(response.text)