import json
from typing import Any

from web3 import Web3

from src.artifact_loader import load_abi, load_bytecode
from src.web3_client import (
    build_base_transaction,
    create_web3,
    get_account,
    normalize_address,
    normalize_bytes32,
    normalize_hex_bytes,
    sign_send_and_wait,
)


def get_contract_factory(
    rpc_url: str,
    artifact_json_path: str,
):
    w3 = create_web3(rpc_url)
    abi = load_abi(artifact_json_path)
    bytecode = load_bytecode(artifact_json_path)

    contract_factory = w3.eth.contract(abi=abi, bytecode=bytecode)
    return w3, contract_factory


def get_contract(
    rpc_url: str,
    artifact_json_path: str,
    contract_address: str,
):
    w3 = create_web3(rpc_url)
    abi = load_abi(artifact_json_path)

    contract = w3.eth.contract(
        address=normalize_address(w3, contract_address),
        abi=abi,
    )
    return w3, contract


def deploy_receiver(
    rpc_url: str,
    private_key: str,
    artifact_json_path: str,
    gateway_address: str,
    gas_limit: int,
) -> dict[str, Any]:
    w3, contract_factory = get_contract_factory(rpc_url, artifact_json_path)
    account = get_account(w3, private_key)

    tx = contract_factory.constructor(
        normalize_address(w3, gateway_address)
    ).build_transaction(
        {
            **build_base_transaction(w3, account.address),
            "gas": gas_limit,
        }
    )

    result = sign_send_and_wait(w3, tx, private_key)
    receipt = result["receipt"]

    output = {
        "deployer_address": account.address,
        "tx_hash": result["tx_hash"],
        "contract_address": receipt.get("contractAddress"),
        "block_number": receipt.get("blockNumber"),
        "status": receipt.get("status"),
        "gas_used": receipt.get("gasUsed"),
    }

    with open("evm-sidechain/deploy_log.jsonl", "a", encoding="utf-8") as out:
        out.write(json.dumps(output, ensure_ascii=False) + "\n")

    return output


def execute_message(
    rpc_url: str,
    private_key: str,
    artifact_json_path: str,
    contract_address: str,
    command_id: str,
    source_chain: str,
    source_address: str,
    payload_hex: str,
    gas_limit: int,
) -> dict[str, Any]:
    w3, contract = get_contract(rpc_url, artifact_json_path, contract_address)
    account = get_account(w3, private_key)

    command_id_bytes = normalize_bytes32(command_id)
    payload_bytes = normalize_hex_bytes(payload_hex)

    tx = contract.functions.execute(
        command_id_bytes,
        source_chain,
        source_address,
        payload_bytes,
    ).build_transaction(
        {
            **build_base_transaction(w3, account.address),
            "gas": gas_limit,
        }
    )

    result = sign_send_and_wait(w3, tx, private_key)
    receipt = result["receipt"]

    return {
        "executor_address": account.address,
        "tx_hash": result["tx_hash"],
        "contract_address": normalize_address(w3, contract_address),
        "block_number": receipt.get("blockNumber"),
        "status": receipt.get("status"),
        "gas_used": receipt.get("gasUsed"),
    }


def try_parse_json(text: str) -> Any:
    try:
        return json.loads(text)
    except Exception:
        return text


def read_receiver_state(
    rpc_url: str,
    artifact_json_path: str,
    contract_address: str,
) -> dict[str, Any]:
    w3, contract = get_contract(rpc_url, artifact_json_path, contract_address)

    last_command_id = contract.functions.lastCommandId().call()
    last_source_chain = contract.functions.lastSourceChain().call()
    last_source_address = contract.functions.lastSourceAddress().call()
    last_message = contract.functions.lastMessage().call()

    return {
        "contract_address": normalize_address(w3, contract_address),
        "last_command_id": Web3.to_hex(last_command_id),
        "last_source_chain": last_source_chain,
        "last_source_address": last_source_address,
        "last_message": last_message,
        "last_message_parsed": try_parse_json(last_message),
    }