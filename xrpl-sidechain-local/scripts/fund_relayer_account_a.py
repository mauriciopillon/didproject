from decimal import Decimal
from web3 import Web3

RPC_URL = "http://localhost:8545"

ALICE_PRIVATE_KEY = "0xD8161FD5FDF4EB216A6556DC639A2543B0ED9ABDBCEB9971FE08CFBA56F588C8"
RELAYER_EVM_ADDRESS = "0xd01D6027860c2E2e37295d3dE4B5a5f46F68d52f"

AMOUNT_XRP = Decimal("100")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

alice = w3.eth.account.from_key(ALICE_PRIVATE_KEY)

amount_wei = int(AMOUNT_XRP * Decimal(10**18))

tx = {
    "from": alice.address,
    "to": Web3.to_checksum_address(RELAYER_EVM_ADDRESS),
    "value": amount_wei,
    "nonce": w3.eth.get_transaction_count(alice.address),
    "gas": 21000,
    "gasPrice": w3.eth.gas_price,
    "chainId": w3.eth.chain_id,
}

signed_tx = alice.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

print("Tx hash:", tx_hash.hex())

print("Chain A")
print("From:", alice.address)
print("To:", RELAYER_EVM_ADDRESS)
print("Amount XRP:", AMOUNT_XRP)

receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Status:", receipt.status)
print("Block:", receipt.blockNumber)