from typing import Any

from xrpl.clients import JsonRpcClient
from xrpl.models.transactions import Payment
from xrpl.transaction import submit_and_wait
from xrpl.wallet import Wallet

from bridge_services import post_to_bridge

from config import (
    AMOUNT_DROPS,
    AXELAR_XRPL_GATEWAY_ADDRESS,
    BRIDGE_SERVICE_URL,
    CALL_TYPE,
    DESTINATION_CHAIN,
    DESTINATION_CONTRACT_ADDRESS,
    INCLUDE_PAYLOAD_MEMO,
    LOGFILE,
    XRPL_RPC_URL,
    XRPL_SEED,
)

from src.logfile import append_logfile

from payload_encoder import (
    build_axelar_memos,
    build_event_message,
    encode_payload_from_message,
    get_payload_hash_hex,
)


def extract_tx_hash(submit_result: Any) -> str:
    result = getattr(submit_result, "result", {}) or {}

    tx_hash = result.get("hash")
    if tx_hash:
        return tx_hash

    tx_json = result.get("tx_json", {}) or {}
    tx_hash = tx_json.get("hash")
    if tx_hash:
        return tx_hash

    raise ValueError("Could not extract transaction hash from XRPL response")


def build_payment(payload: bytes) -> Payment:
    memos = build_axelar_memos(
        destination_chain=DESTINATION_CHAIN,
        destination_address=DESTINATION_CONTRACT_ADDRESS,
        call_type=CALL_TYPE,
        payload=payload,
        include_payload_memo=INCLUDE_PAYLOAD_MEMO,
    )

    wallet = Wallet.from_seed(XRPL_SEED)

    return Payment(
        account=wallet.address,
        destination=AXELAR_XRPL_GATEWAY_ADDRESS,
        amount=AMOUNT_DROPS,
        memos=memos,
    )


def send_event_to_evm(event_type: str, event_data: dict[str, Any]) -> dict[str, Any]:
    client = JsonRpcClient(XRPL_RPC_URL)
    wallet = Wallet.from_seed(XRPL_SEED)

    message = build_event_message(event_type=event_type, event_data=event_data)
    payload = encode_payload_from_message(message)
    payload_hash = get_payload_hash_hex(payload)

    payment = build_payment(payload=payload)
    submit_result = submit_and_wait(payment, client, wallet)
    tx_hash = extract_tx_hash(submit_result)

    xrpl_result = getattr(submit_result, "result", {}) or {}

    logfile_entry = {
        "source_tx_hash": tx_hash,
        "xrpl_rpc_url": XRPL_RPC_URL,
        "sender_address": wallet.address,
        "gateway_address": AXELAR_XRPL_GATEWAY_ADDRESS,
        "destination_chain": DESTINATION_CHAIN,
        "destination_contract_address": DESTINATION_CONTRACT_ADDRESS,
        "call_type": CALL_TYPE,
        "amount_drops": AMOUNT_DROPS,
        "event_type": event_type,
        "event_data": event_data,
        "message": message,
        "payload_hex": payload.hex(),
        "payload_hash": payload_hash,
        "include_payload_memo": INCLUDE_PAYLOAD_MEMO,
        "xrpl_result": xrpl_result,
    }

    append_logfile(logfile_entry, LOGFILE)
    bridge_response = post_to_bridge(BRIDGE_SERVICE_URL, tx_hash)

    return {
        "source_tx_hash": tx_hash,
        "payload_hash": payload_hash,
        "payload_hex": payload.hex(),
        "message": message,
        "bridge_response": bridge_response,
        "xrpl_result": xrpl_result,
    }