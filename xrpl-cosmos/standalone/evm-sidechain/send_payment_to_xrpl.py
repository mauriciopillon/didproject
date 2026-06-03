import os
from dotenv import load_dotenv
from web3 import Web3
from decimal import Decimal

from xrpl.core.addresscodec import decode_classic_address

load_dotenv()

EVM_RPC_URL = os.getenv("EVM_RPC_URL")
USER_EVM_PRIVATE_KEY = os.getenv("USER_EVM_PRIVATE_KEY")

ITS_CONTRACT_ADDRESS = os.getenv("ITS_CONTRACT_ADDRESS")
XRP_TOKEN_ID = os.getenv("XRP_TOKEN_ID")

DESTINATION_CHAIN = os.getenv("DESTINATION_CHAIN", "xrpl")
DESTINATION_XRPL_ADDRESS = os.getenv("DESTINATION_XRPL_ADDRESS")

AMOUNT_RAW = 0.1
GAS_VALUE_WEI = 0.1


ITS_ABI = [
    {
        "type": "function",
        "name": "interchainTransfer",
        "stateMutability": "payable",
        "inputs": [
            {"name": "tokenId", "type": "bytes32"},
            {"name": "destinationChain", "type": "string"},
            {"name": "destinationAddress", "type": "bytes"},
            {"name": "amount", "type": "uint256"},
            {"name": "metadata", "type": "bytes"},
            {"name": "gasValue", "type": "uint256"},
        ],
        "outputs": [],
    }
]


w3 = Web3(Web3.HTTPProvider(EVM_RPC_URL))

account = w3.eth.account.from_key(USER_EVM_PRIVATE_KEY)

its = w3.eth.contract(
    address=Web3.to_checksum_address(ITS_CONTRACT_ADDRESS),
    abi=ITS_ABI,
)

token_id_bytes = Web3.to_bytes(hexstr=XRP_TOKEN_ID)
destination_bytes = DESTINATION_XRPL_ADDRESS.encode("utf-8")
metadata = b""

print("From EVM:", account.address)
print("ITS:", ITS_CONTRACT_ADDRESS)
print("Token ID:", XRP_TOKEN_ID)
print("Destination chain:", DESTINATION_CHAIN)
print("Destination bytes:", "0x" + destination_bytes.hex())
print("Amount:", AMOUNT_RAW)
print("Gas value:", GAS_VALUE_WEI)
print("Native balance:", w3.eth.get_balance(account.address))


TX_AMOUNT_RAW = int(Decimal(str(AMOUNT_RAW)) * Decimal(10**18))
TX_GAS_VALUE_WEI = int(Decimal(str(GAS_VALUE_WEI)) * Decimal(10**18))
TX_VALUE = TX_AMOUNT_RAW+TX_GAS_VALUE_WEI


tx = its.functions.interchainTransfer(
    token_id_bytes,
    DESTINATION_CHAIN,
    destination_bytes,
    TX_AMOUNT_RAW,
    metadata,
    TX_GAS_VALUE_WEI,
).build_transaction({
    "from": account.address,
    "value": TX_VALUE,
    "nonce": w3.eth.get_transaction_count(account.address),
    "gas": 900000,
    "gasPrice": w3.eth.gas_price,
    "chainId": w3.eth.chain_id,
})

signed_tx = w3.eth.account.sign_transaction(tx, USER_EVM_PRIVATE_KEY)
raw_tx = getattr(signed_tx, "raw_transaction", signed_tx.raw_transaction)

tx_hash = w3.eth.send_raw_transaction(raw_tx)

print("EVM tx hash:", tx_hash.hex())

receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Status:", receipt.status)
print("Gas used:", receipt.gasUsed)