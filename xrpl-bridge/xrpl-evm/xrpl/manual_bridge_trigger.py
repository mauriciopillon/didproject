import requests

response = requests.post(
    "http://localhost:3000/relay",
    json={"sourceTxHash": " "},
)

print(response.status_code)
print(response.json())