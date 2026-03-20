from eth_account import Account
from bech32 import bech32_encode, convertbits


def generate_private_key_hex():
    account = Account.create()
    return account.key.hex()


def get_evm_address(private_key_hex):
    account = Account.from_key(private_key_hex)
    return account.address


def evm_to_cosmos_address(evm_address, hrp="ethm"):
    evm_hex = evm_address.lower().replace("0x", "")
    address_bytes = bytes.fromhex(evm_hex)
    bech32_data = convertbits(address_bytes, 8, 5, True)
    return bech32_encode(hrp, bech32_data)


def generate_xrpl_evm_account():
    private_key_hex = generate_private_key_hex()
    evm_address = get_evm_address(private_key_hex)
    cosmos_address = evm_to_cosmos_address(evm_address, hrp="ethm")

    return {
        "private_key_hex": private_key_hex,
        "evm_address": evm_address,
        "cosmos_address": cosmos_address,
    }

account_data = generate_xrpl_evm_account()

print("Private key:", account_data["private_key_hex"])
print("EVM address:", account_data["evm_address"])
print("Cosmos address:", account_data["cosmos_address"])