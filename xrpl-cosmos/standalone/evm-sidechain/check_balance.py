import os
import requests
from dotenv import load_dotenv

load_dotenv()

EVM_RPC_URL = os.getenv("EVM_RPC_URL")
EVM_ADDRESS = os.getenv("USER_EVM_ADDRESS")


def get_evm_balance(address):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1,
    }

    response = requests.post(EVM_RPC_URL, json=payload)
    result = response.json()["result"]

    balance_wei = int(result, 16)
    balance_xrp = balance_wei / 10**18

    print("Address:", address)
    print("Balance:", balance_xrp, "XRP")
    print("Balance wei:", balance_wei)

    return balance_xrp


get_evm_balance(EVM_ADDRESS)