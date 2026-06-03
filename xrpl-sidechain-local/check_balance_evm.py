import requests
from decimal import Decimal

# RPC_URL = "http://localhost:8545"  # Chain A
RPC_URL = "http://localhost:9545"  # Chain B

ADDRESS = "0x6f6c82025cfa145dd13b614aa4289ad6ca856e53"

payload = {
    "jsonrpc": "2.0",
    "method": "eth_getBalance",
    "params": [ADDRESS, "latest"],
    "id": 1
}

response = requests.post(RPC_URL, json=payload)
data = response.json()

balance_wei = int(data["result"], 16)
balance_xrp = Decimal(balance_wei) / Decimal(10**18)

print("Address:", ADDRESS)
print("Balance axrp:", balance_wei)
print("Balance XRP:", balance_xrp)