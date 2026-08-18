import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMCIsImV4cCI6MTc4NzY3OTg4NX0.An07G6stXGdm_EuUi4FEzFdGd3ErADJTAz3xIFmSfl0"
}

requisicao = requests.get("http://127.0.0.1:8000/docs/auth/refresh", headers=headers)
print(requisicao)
print(requisicao.json())