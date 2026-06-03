from typing import Any

from web3 import Web3


def strip_0x(value: str) -> str:
    return value[2:] if value.startswith("0x") else value


def create_web3(rpc_url: str) -> Web3:
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    if not w3.is_connected():
        raise ConnectionError(f"Could not connect to EVM RPC: {rpc_url}")

    return w3


def get_account(w3: Web3, private_key: str):
    return w3.eth.account.from_key(private_key)


def normalize_address(w3: Web3, address: str) -> str:
    return w3.to_checksum_address(address)


def normalize_bytes32(hex_value: str) -> bytes:
    clean = strip_0x(hex_value).strip()

    if not clean:
        raise ValueError("command_id cannot be empty")

    if len(clean) > 64:
        raise ValueError("command_id is longer than 32 bytes")

    padded = clean.rjust(64, "0")
    return bytes.fromhex(padded)


def normalize_hex_bytes(hex_value: str) -> bytes:
    clean = strip_0x(hex_value).strip()
    if len(clean) % 2 != 0:
        clean = "0" + clean
    return bytes.fromhex(clean)


def build_base_transaction(w3: Web3, sender_address: str) -> dict[str, Any]:
    return {
        "from": sender_address,
        "nonce": w3.eth.get_transaction_count(sender_address, "pending"),
        "chainId": w3.eth.chain_id,
        "gasPrice": w3.eth.gas_price,
    }


def sign_send_and_wait(w3: Web3, tx: dict[str, Any], private_key: str) -> dict[str, Any]:
    signed = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return {
        "tx_hash": w3.to_hex(tx_hash),
        "receipt": dict(receipt),
    }