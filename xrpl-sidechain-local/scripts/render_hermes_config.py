from pathlib import Path
import json
import os


ROOT_DIR = Path(__file__).resolve().parents[1]
CHAINS_FILE = ROOT_DIR / "chains.json"
HERMES_DIR = ROOT_DIR / "relayer" / "hermes"
CONFIG_FILE = HERMES_DIR / "config.toml"
MNEMONICS_DIR = HERMES_DIR / "mnemonics"


def load_chains():
    data = json.loads(CHAINS_FILE.read_text(encoding="utf-8"))
    return data["chains"]


def write_mnemonics(chains):
    MNEMONICS_DIR.mkdir(parents=True, exist_ok=True)

    for chain in chains:
        path = MNEMONICS_DIR / f"{chain['key_name']}.txt"
        path.write_text(chain["relayer_mnemonic"].strip() + "\n", encoding="utf-8")
        os.chmod(path, 0o644)


def render_chain(chain):
    chain_id = chain["chain_id"]
    ip = chain["ip"]
    rpc_port = chain["rpc_port"]
    grpc_port = chain["grpc_port"]
    key_name = chain["key_name"]

    return f"""
[[chains]]
id = "{chain_id}"
type = "CosmosSdk"
rpc_addr = "http://{ip}:{rpc_port}"
grpc_addr = "http://{ip}:{grpc_port}"
event_source = {{ mode = "push", url = "ws://{ip}:{rpc_port}/websocket", batch_delay = "500ms" }}
rpc_timeout = "10s"
trusted_node = false
account_prefix = "ethm"
key_name = "{key_name}"
key_store_type = "Test"
address_type = {{ derivation = "ethermint", proto_type = {{ pk_type = "/ethermint.crypto.v1.ethsecp256k1.PubKey" }} }}
store_prefix = "ibc"
default_gas = 400000
max_gas = 2000000
gas_price = {{ price = 0.0, denom = "axrp" }}
gas_multiplier = 1.3
max_msg_num = 30
max_tx_size = 180000
clock_drift = "5s"
max_block_time = "30s"
trusting_period = "12hours"
trust_threshold = {{ numerator = "1", denominator = "3" }}
memo_prefix = "hermes"
"""


def render_config():
    chains = load_chains()

    HERMES_DIR.mkdir(parents=True, exist_ok=True)
    write_mnemonics(chains)

    content = f"""[global]
log_level = "info"

[mode]

[mode.clients]
enabled = true
refresh = true
misbehaviour = true

[mode.connections]
enabled = true

[mode.channels]
enabled = true

[mode.packets]
enabled = true
clear_interval = 100
clear_on_start = true
tx_confirmation = true

[rest]
enabled = false
host = "127.0.0.1"
port = 3000

[telemetry]
enabled = false
host = "127.0.0.1"
port = 3001

{''.join(render_chain(chain) for chain in chains)}
"""

    CONFIG_FILE.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    render_config()
    print(f"Hermes config: {CONFIG_FILE}")
    print(f"Mnemonics: {MNEMONICS_DIR}")
