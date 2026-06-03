from src.event_handler import execute_message
from src.config import (
    ARTIFACT_JSON_PATH,
    CONTRACT_ADDRESS,
    EVM_PRIVATE_KEY,
    EVM_RPC_URL,
    GAS_LIMIT,
)


def main() -> None:
    contract_address = CONTRACT_ADDRESS
    command_id = "0xSEU_COMMAND_ID_AQUI"
    source_chain = "xrpl"
    source_address = "rSEU_ENDERECO_XRPL_AQUI"
    payload_hex = ""

    if not contract_address:
        raise ValueError("CONTRACT_ADDRESS is required for execute")

    if not command_id or command_id == "0xSEU_COMMAND_ID_AQUI":
        raise ValueError("Set a real command_id in evm_client/execute.py")

    if not source_address or source_address == "rSEU_ENDERECO_XRPL_AQUI":
        raise ValueError("Set a real source_address in evm_client/execute.py")

    result = execute_message(
        rpc_url=EVM_RPC_URL,
        private_key=EVM_PRIVATE_KEY,
        artifact_json_path=ARTIFACT_JSON_PATH,
        contract_address=contract_address,
        command_id=command_id,
        source_chain=source_chain,
        source_address=source_address,
        payload_hex=payload_hex,
        gas_limit=GAS_LIMIT,
    )

    print(result)


if __name__ == "__main__":
    main()