from src.event_handler import read_receiver_state
from src.config import (
    ARTIFACT_JSON_PATH,
    CONTRACT_ADDRESS,
    EVM_RPC_URL,
)


def main() -> None:
    contract_address = CONTRACT_ADDRESS

    if not contract_address:
        raise ValueError("CONTRACT_ADDRESS is required for read")

    result = read_receiver_state(
        rpc_url=EVM_RPC_URL,
        artifact_json_path=ARTIFACT_JSON_PATH,
        contract_address=contract_address,
    )

    print(result)


if __name__ == "__main__":
    main()