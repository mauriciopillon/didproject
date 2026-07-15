from pathlib import Path
from decimal import Decimal
import json
import subprocess
import time

from bech32 import bech32_encode, convertbits
from eth_account import Account


ROOT_DIR = Path(__file__).resolve().parents[1]
CHAINS_FILE = ROOT_DIR / "chains.json"

FUND_AMOUNT_XRP = Decimal("100")
DENOM = "axrp"
DERIVATION_PATH = "m/44'/60'/0'/0/0"
BECH32_PREFIX = "ethm"
FEE = "20000000000000000axrp"
GAS = "200000"


def load_chains():
    data = json.loads(CHAINS_FILE.read_text(encoding="utf-8"))
    return data["chains"]


def xrp_to_axrp(amount):
    return int(amount * Decimal(10**18))


def eth_hex_to_ethm(address):
    raw = bytes.fromhex(address.removeprefix("0x"))
    data = convertbits(raw, 8, 5)
    return bech32_encode(BECH32_PREFIX, data)


def relayer_address_from_mnemonic(mnemonic):
    Account.enable_unaudited_hdwallet_features()

    account = Account.from_mnemonic(
        mnemonic.strip(),
        account_path=DERIVATION_PATH,
    )

    return eth_hex_to_ethm(account.address)


def run(cmd):
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def fund_relayer(chain):
    relayer_address = relayer_address_from_mnemonic(chain["relayer_mnemonic"])
    amount = f"{xrp_to_axrp(FUND_AMOUNT_XRP)}{DENOM}"
    node = f"tcp://{chain['ip']}:{chain['rpc_port']}"

    print(f"{chain['label']}: funding {relayer_address} com {amount}")

    cmd = [
        "docker",
        "exec",
        chain["service"],
        "/app/bin/exrpd",
        "tx",
        "bank",
        "send",
        "alice",
        relayer_address,
        amount,
        "--home",
        "/app/.exrpd",
        "--chain-id",
        chain["chain_id"],
        "--keyring-backend",
        "test",
        "--node",
        node,
        "--gas",
        GAS,
        "--fees",
        FEE,
        "-y",
    ]

    result = run(cmd)

    if result.stdout.strip():
        print(result.stdout.strip())

    if result.stderr.strip():
        print(result.stderr.strip())

    time.sleep(3)

    query_cmd = [
        "docker",
        "exec",
        chain["service"],
        "/app/bin/exrpd",
        "query",
        "bank",
        "balances",
        relayer_address,
        "--node",
        node,
    ]

    balance = run(query_cmd)

    print(f"{chain['label']}: saldo de {relayer_address}")
    print(balance.stdout.strip())


def main():
    for chain in load_chains():
        fund_relayer(chain)


if __name__ == "__main__":
    main()
