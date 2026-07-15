from pathlib import Path
from decimal import Decimal
import json
import subprocess


ROOT_DIR = Path(__file__).resolve().parents[1]
CHAINS_FILE = ROOT_DIR / "chains.json"

CHAIN = "Chain B"
ADDRESS = "ethm1dakgyqjulg29m5fmv992g2y66m9g2mjn6hahwg"


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


def run(cmd):
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def query_balance(chain, address):
    node = f"tcp://{chain['ip']}:{chain['rpc_port']}"

    cmd = [
        "docker",
        "exec",
        chain["service"],
        "/app/bin/exrpd",
        "query",
        "bank",
        "balances",
        address,
        "--node",
        node,
        "--output",
        "json",
    ]

    result = run(cmd)
    return json.loads(result.stdout)


def main():
    chain = find_chain(CHAIN)
    data = query_balance(chain, ADDRESS)

    print("Chain:", chain["label"])
    print("Chain ID:", chain["chain_id"])
    print("Address:", ADDRESS)
    print()

    for balance in data["balances"]:
        denom = balance["denom"]
        amount = int(balance["amount"])

        print("Denom:", denom)
        print("Amount:", amount)

        if denom == "axrp":
            amount_xrp = Decimal(amount) / Decimal(10**18)
            print("Amount XRP:", amount_xrp)

        print()


if __name__ == "__main__":
    main()
