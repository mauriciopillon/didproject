from pathlib import Path
from decimal import Decimal
import json
import subprocess
import time


ROOT_DIR = Path(__file__).resolve().parents[1]
CHAINS_FILE = ROOT_DIR / "chains.json"
LOG_FILE = ROOT_DIR / "tests" / "logfile.jsonl"

### Source
SOURCE_CHAIN = "Chain A"
SOURCE_KEY_NAME = "alice"
SOURCE_COSMOS_ADDRESS = "ethm1dakgyqjulg29m5fmv992g2y66m9g2mjn6hahwg"
SOURCE_CHANNEL = "channel-0"
SOURCE_PORT = "transfer"


### Destination
DESTINATION_CHAIN = "Chain B"
DESTINATION_COSMOS_ADDRESS = "ethm1dakgyqjulg29m5fmv992g2y66m9g2mjn6hahwg"


### Transfer data
DENOM = "axrp"
TRANSFER_AMOUNT = "1"  # em XRP
FEE_AMOUNT = "20000000000000000"
GAS_LIMIT = 400000
TIMEOUT_SECONDS = 1000


def load_chains():
    data = json.loads(CHAINS_FILE.read_text(encoding="utf-8"))
    return data["chains"]


def find_chain(chain_identifier):
    for chain in load_chains():
        values = [
            chain.get("name"),
            chain.get("label"),
            chain.get("service"),
            chain.get("chain_id"),
        ]

        if chain_identifier in values:
            return chain

    raise ValueError(f"Chain não encontrada no chains.json: {chain_identifier}")


def xrp_to_axrp(amount):
    return str(int(Decimal(str(amount)) * Decimal(10**18)))


def get_source_channel(source_chain_data, destination_chain_data):
    if SOURCE_CHANNEL:
        return SOURCE_CHANNEL

    channels = source_chain_data.get("channels", {})
    destination_keys = [
        destination_chain_data.get("label"),
        destination_chain_data.get("name"),
        destination_chain_data.get("service"),
        destination_chain_data.get("chain_id"),
    ]

    for key in destination_keys:
        if key in channels:
            return channels[key]

    raise ValueError(
        f"Canal IBC não encontrado para {source_chain_data['label']} -> {destination_chain_data['label']}"
    )


def run(cmd):
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def parse_json_output(stdout):
    text = stdout.strip()

    if not text:
        return {}

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")

        if start >= 0 and end >= start:
            return json.loads(text[start:end + 1])

        return {"raw_output": text}


def transfer_cross_chain(
    source_chain,
    destination_chain,
    source_cosmos_address,
    destination_cosmos_address,
):
    source_chain_data = find_chain(source_chain)
    destination_chain_data = find_chain(destination_chain)

    source_channel = get_source_channel(source_chain_data, destination_chain_data)
    amount_axrp = xrp_to_axrp(TRANSFER_AMOUNT)
    amount = f"{amount_axrp}{DENOM}"
    fee = f"{FEE_AMOUNT}{DENOM}"
    node = f"tcp://{source_chain_data['ip']}:{source_chain_data['rpc_port']}"
    timeout_timestamp = str(int((time.time() + TIMEOUT_SECONDS) * 1_000_000_000))

    cmd = [
        "docker",
        "exec",
        source_chain_data["service"],
        "/app/bin/exrpd",
        "tx",
        "ibc-transfer",
        "transfer",
        SOURCE_PORT,
        source_channel,
        destination_cosmos_address,
        amount,
        "--from",
        SOURCE_KEY_NAME,
        "--home",
        "/app/.exrpd",
        "--chain-id",
        source_chain_data["chain_id"],
        "--keyring-backend",
        "test",
        "--node",
        node,
        "--gas",
        str(GAS_LIMIT),
        "--fees",
        fee,
        "--packet-timeout-timestamp",
        timeout_timestamp,
        "--output",
        "json",
        "-y",
    ]

    result = run(cmd)

    if result.stderr.strip():
        print(result.stderr.strip())

    response = parse_json_output(result.stdout)

    code = response.get("code", 0)
    tx_hash = response.get("txhash") or response.get("hash")

    output = {
        "Source Chain": source_chain,
        "Source Chain ID": source_chain_data["chain_id"],
        "Destination Chain": destination_chain,
        "Destination Chain ID": destination_chain_data["chain_id"],
        "Source Port": SOURCE_PORT,
        "Source Channel": source_channel,
        "Sender": source_cosmos_address,
        "Sender Key": SOURCE_KEY_NAME,
        "Receiver": destination_cosmos_address,
        "Amount": str(TRANSFER_AMOUNT) + " XRP",
        "Amount axrp": amount_axrp,
        "Code": code,
        "TxHash": tx_hash,
    }

    if "raw_log" in response:
        output["RawLog"] = response["raw_log"]

    if "raw_output" in response:
        output["RawOutput"] = response["raw_output"]

    if code == 0:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

        with LOG_FILE.open("a", encoding="utf-8") as out:
            out.write(json.dumps(output, ensure_ascii=False) + "\n")

    print(json.dumps(output, indent=2, ensure_ascii=False))


transfer_cross_chain(
    source_chain=SOURCE_CHAIN,
    destination_chain=DESTINATION_CHAIN,
    source_cosmos_address=SOURCE_COSMOS_ADDRESS,
    destination_cosmos_address=DESTINATION_COSMOS_ADDRESS,
)
