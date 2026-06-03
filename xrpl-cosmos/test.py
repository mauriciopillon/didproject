import httpx

body = {
    "amount": "0.1",
    "receiver": "Bob",
    "sender": "Alice"
}

response = httpx.post("http://localhost:8001/forward", json=body)

print(response.status_code)
print(response.json())