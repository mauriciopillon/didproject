import requests
import os
from dotenv import load_dotenv
load_dotenv()

COSMOS_API_URL = "http://cosmos-api.testnet.xrplevm.org"
COSMOS_RPC_URL = "https://cosmos-rpc.testnet.xrplevm.org"

COSMOS_ADDRESS = os.getenv("COSMOS_ADDRESS")

def cosmos_get(path, api_url=COSMOS_API_URL):
    url = f"{api_url.rstrip('/')}{path}"
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.json()


def cosmos_rpc_get(path, rpc_url=COSMOS_RPC_URL):
    url = f"{rpc_url.rstrip('/')}{path}"
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.json()


def get_latest_cosmos_block(api_url=COSMOS_API_URL):
    data = cosmos_get("/cosmos/base/tendermint/v1beta1/blocks/latest", api_url)

    header = data.get("block", {}).get("header", {})

    return {
        "height": header.get("height"),
        "chain_id": header.get("chain_id"),
        "time": header.get("time"),
        "proposer_address": header.get("proposer_address"),
        "raw": data,
    }


def get_cosmos_balance(address, api_url=COSMOS_API_URL):
    data = cosmos_get(f"/cosmos/bank/v1beta1/balances/{address}", api_url)

    return {
        "address": address,
        "balances": data.get("balances", []),
        "pagination": data.get("pagination", {}),
        "raw": data,
    }


def test_latest_cosmos_block(api_url=COSMOS_API_URL):
    block_data = get_latest_cosmos_block(api_url)
    print("Latest Cosmos block:")
    print(block_data)
    return block_data


def test_cosmos_balance(address, api_url=COSMOS_API_URL):
    balance_data = get_cosmos_balance(address, api_url)
    print("Cosmos balance:")
    print(balance_data)
    return balance_data


def test_cosmos_rpc_status(rpc_url=COSMOS_RPC_URL):
    status = cosmos_rpc_get("/status", rpc_url)
    print("Cosmos RPC status:")
    print(status)
    return status

test_cosmos_balance(COSMOS_ADDRESS)
test_cosmos_rpc_status()
test_latest_cosmos_block