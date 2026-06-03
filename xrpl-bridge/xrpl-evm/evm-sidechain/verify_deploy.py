import json

from src.event_handler import read_receiver_state
from src.config import ARTIFACT_JSON_PATH, EVM_RPC_URL
from src.web3_client import create_web3, normalize_address


CONTRACT_ADDRESS = "0x39390664541569a26C512968B4c668a21b9868D2"


def print_json(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


def main() -> None:
    if not CONTRACT_ADDRESS or CONTRACT_ADDRESS == "0xSEU_CONTRATO_AQUI":
        raise ValueError("Set a real contract address")

    w3 = create_web3(EVM_RPC_URL)
    contract_address = normalize_address(w3, CONTRACT_ADDRESS)

    code = w3.eth.get_code(contract_address)
    has_code = code != b""

    result = {
        "contract_address": contract_address,
        "rpc_url": EVM_RPC_URL,
        "chain_id": w3.eth.chain_id,
        "latest_block": w3.eth.block_number,
        "has_code": has_code,
        "code_size_bytes": len(code),
    }

    if not has_code:
        result["verified"] = False
        result["reason"] = "No contract bytecode found at this address"
        print_json(result)
        return

    try:
        state = read_receiver_state(
            rpc_url=EVM_RPC_URL,
            artifact_json_path=ARTIFACT_JSON_PATH,
            contract_address=contract_address,
        )

        result["verified"] = True
        result["contract_read_ok"] = True
        result["state"] = state
    except Exception as exc:
        result["verified"] = True
        result["contract_read_ok"] = False
        result["read_error"] = str(exc)

    print_json(result)


if __name__ == "__main__":
    main()