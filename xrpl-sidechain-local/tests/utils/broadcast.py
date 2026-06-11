import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

COSMOS_API_URL = ("http://localhost:1317").rstrip("/")
COSMOS_RPC_URL = ("http://localhost:26657").rstrip("/")


def get_account_info(address):
    url = f"{COSMOS_API_URL}/cosmos/auth/v1beta1/accounts/{address}"

    response = requests.get(url)
    data = response.json()

    account = data["account"]

    if "base_account" in account:
        account = account["base_account"]

    account_number = int(account["account_number"])
    sequence = int(account["sequence"])

    return account_number, sequence


def broadcast_tx(tx_raw_bytes):
    tx_hex = "0x" + tx_raw_bytes.hex()

    url = f"{COSMOS_RPC_URL}/broadcast_tx_sync"

    response = requests.get(
        url,
        params={"tx": tx_hex},
    )

    return response.json()