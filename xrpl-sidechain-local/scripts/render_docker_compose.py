from pathlib import Path
import json


ROOT_DIR = Path(__file__).resolve().parents[1]
CHAINS_FILE = ROOT_DIR / "chains.json"
OUTPUT_FILE = ROOT_DIR / "docker-compose.yaml"

MACVLAN_NAME = "xrplevm_macvlan"
MACVLAN_SUBNET = "10.10.20.0/24"
MACVLAN_GATEWAY = "10.10.20.1"
MACVLAN_PARENT = "enp0s31f6"
HERMES_IP = "10.10.20.250"
HERMES_KEYS_VOLUME = "hermes-keys"


def load_chains():
    data = json.loads(CHAINS_FILE.read_text(encoding="utf-8"))
    return data["chains"]


def volume_name(chain):
    return chain.get("volume", f"{chain['service']}-data")


def render_chain_service(chain):
    return f"""  {chain["service"]}:
    image: xrplevm-local:dev
    build: *xrplevm-build
    container_name: {chain["service"]}
    command: ["/usr/local/bin/start-persistent.sh"]
    environment:
      CHAIN_ID: {json.dumps(str(chain["chain_id"]))}
      MONIKER: {json.dumps(str(chain["moniker"]))}
      CHAIN_LABEL: {json.dumps(str(chain["label"]))}
      IP: {json.dumps(str(chain["ip"]))}
      RPC_PORT: {json.dumps(str(chain["rpc_port"]))}
      REST_PORT: {json.dumps(str(chain["rest_port"]))}
      GRPC_PORT: {json.dumps(str(chain["grpc_port"]))}
      EVM_RPC_PORT: {json.dumps(str(chain["evm_rpc_port"]))}
      EVM_WS_PORT: {json.dumps(str(chain["evm_ws_port"]))}
      KEY_NAME: {json.dumps(str(chain["key_name"]))}
    networks:
      {MACVLAN_NAME}:
        ipv4_address: {chain["ip"]}
    volumes:
      - {volume_name(chain)}:/app/.exrpd
"""


def render_compose():
    chains = load_chains()

    services = "\n".join(
        render_chain_service(chain)
        for chain in chains
    )

    chain_depends_on = "\n".join(
        f"      {chain['service']}:\n        condition: service_started"
        for chain in chains
    )

    volumes = "\n".join(
        f"  {volume_name(chain)}:" for chain in chains
    )

    content = f"""x-xrplevm-build: &xrplevm-build
  context: .
  dockerfile: Dockerfile

services:
{services}
  hermes-init:
    image: informalsystems/hermes:1.13.1
    container_name: hermes-init
    entrypoint: ["sh", "-lc"]
    command: "mkdir -p /keys && chown -R 2000:2000 /keys && chmod -R u+rwX /keys"
    volumes:
      - {HERMES_KEYS_VOLUME}:/keys
    network_mode: none

  hermes:
    image: informalsystems/hermes:1.13.1
    container_name: hermes
    entrypoint: ["sleep"]
    command: ["infinity"]
    volumes:
      - ./relayer/hermes/config.toml:/home/hermes/.hermes/config.toml:ro
      - ./relayer/hermes/mnemonics:/home/hermes/.hermes/mnemonics:ro
      - {HERMES_KEYS_VOLUME}:/home/hermes/.hermes/keys
    depends_on:
      hermes-init:
        condition: service_completed_successfully
{chain_depends_on}
    networks:
      {MACVLAN_NAME}:
        ipv4_address: {HERMES_IP}

networks:
  {MACVLAN_NAME}:
    name: {MACVLAN_NAME}
    driver: macvlan
    driver_opts:
      parent: {MACVLAN_PARENT}
    ipam:
      config:
        - subnet: {MACVLAN_SUBNET}
          gateway: {MACVLAN_GATEWAY}

volumes:
{volumes}
  {HERMES_KEYS_VOLUME}:
"""

    OUTPUT_FILE.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    render_compose()
    print(f"Compose: {OUTPUT_FILE}")
