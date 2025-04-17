import requests

for i in range(100):
    res = requests.get("http://localhost:5050/tasks")
    print(f"{i+1}/100 -> Status: {res.status_code}")
