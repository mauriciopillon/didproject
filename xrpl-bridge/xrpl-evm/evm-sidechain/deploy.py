from src.event_handler import deploy_receiver
from src.config import (
    ARTIFACT_JSON_PATH,
    AXELAR_GATEWAY_ADDRESS,
    EVM_PRIVATE_KEY,
    EVM_RPC_URL,
    GAS_LIMIT,
)


def main() -> None:
    # Ajustar aqui se quiser sobrescrever algo do .env
    rpc_url = EVM_RPC_URL
    private_key = EVM_PRIVATE_KEY
    artifact_json_path = ARTIFACT_JSON_PATH
    gateway_address = AXELAR_GATEWAY_ADDRESS
    gas_limit = GAS_LIMIT

    if not gateway_address:
        raise ValueError("AXELAR_GATEWAY_ADDRESS is required for deploy")

    result = deploy_receiver(
        rpc_url=rpc_url,
        private_key=private_key,
        artifact_json_path=artifact_json_path,
        gateway_address=gateway_address,
        gas_limit=gas_limit,
    )

    print(result)


if __name__ == "__main__":
    main()