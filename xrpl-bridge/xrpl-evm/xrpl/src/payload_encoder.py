import json
from typing import Any

from eth_abi import encode
from web3 import Web3
from xrpl.models.transactions import Memo


def utf8_to_hex(text: str) -> str:
    return text.encode("utf-8").hex()


def strip_0x(value: str) -> str:
    return value[2:] if value.startswith("0x") else value


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def build_event_message(event_type: str, event_data: dict[str, Any]) -> str:
    return canonical_json(
        {
            "event_type": event_type,
            "event_data": event_data,
        }
    )


def encode_payload_from_message(message: str) -> bytes:
    # Compatível com um receiver Solidity que faz:
    # string memory message = abi.decode(payload, (string));
    return encode(["string"], [message])


def get_payload_hash_hex(payload: bytes) -> str:
    return Web3.keccak(payload).hex()


def build_axelar_memos(
    destination_chain: str,
    destination_address: str,
    call_type: str,
    payload: bytes,
    include_payload_memo: bool,
) -> list[Memo]:
    payload_hash_hex = strip_0x(get_payload_hash_hex(payload))

    memos = [
        Memo(
            memo_type=utf8_to_hex("type"),
            memo_data=utf8_to_hex(call_type),
        ),
        Memo(
            memo_type=utf8_to_hex("destination_chain"),
            memo_data=utf8_to_hex(destination_chain),
        ),
        Memo(
            memo_type=utf8_to_hex("destination_address"),
            memo_data=utf8_to_hex(destination_address),
        ),
        Memo(
            memo_type=utf8_to_hex("payload_hash"),
            memo_data=payload_hash_hex,
        ),
    ]

    if include_payload_memo:
        memos.append(
            Memo(
                memo_type=utf8_to_hex("payload"),
                memo_data=payload.hex(),
            )
        )

    return memos