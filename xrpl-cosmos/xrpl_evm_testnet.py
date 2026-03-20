import requests
import os
from dotenv import load_dotenv
load_dotenv()

EVM_RPC_URL = "https://rpc.testnet.xrplevm.org"
EVM_ADDRESS = os.getenv("EVM_ADDRESS")

def evm_rpc_call(method, params=None, rpc_url=EVM_RPC_URL):
    if params is None:
        params = []

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }

    response = requests.post(rpc_url, json=payload, timeout=20)
    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise RuntimeError(f"EVM RPC error: {data['error']}")

    return data["result"]


def get_latest_evm_block_number(rpc_url=EVM_RPC_URL):
    result = evm_rpc_call("eth_blockNumber", rpc_url=rpc_url)
    return int(result, 16)


def get_evm_balance(address, rpc_url=EVM_RPC_URL):
    result = evm_rpc_call("eth_getBalance", [address, "latest"], rpc_url=rpc_url)

    return {
        "address": address,
        "balance_hex": result,
        "balance_wei": int(result, 16),
    }


def test_latest_evm_block(rpc_url=EVM_RPC_URL):
    block_number = get_latest_evm_block_number(rpc_url)
    print("Latest EVM block number:", block_number)
    return block_number


def test_evm_balance(address, rpc_url=EVM_RPC_URL):
    balance = get_evm_balance(address, rpc_url)
    print("EVM balance:")
    print(balance)
    return balance

test_evm_balance(EVM_ADDRESS)
test_latest_evm_block()