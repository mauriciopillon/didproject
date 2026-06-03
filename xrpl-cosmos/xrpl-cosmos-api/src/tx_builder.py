import os
from dotenv import load_dotenv
from web3 import Web3
from decimal import Decimal

load_dotenv()


ITS_CONTRACT_ADDRESS = os.getenv("ITS_CONTRACT_ADDRESS")
XRP_TOKEN_ID = os.getenv("XRP_TOKEN_ID")

DESTINATION_CHAIN = os.getenv("DESTINATION_CHAIN", "xrpl")
DESTINATION_XRPL_ADDRESS = os.getenv("DESTINATION_XRPL_ADDRESS")

GAS_VALUE_WEI = os.getenv("GAS_VALUE_WEI")


def build_transaction(w3, amount, receiver, sender):

    receiver = os.getenv(receiver.upper()+ "_XRPL_ADDRESS")
    sender = os.getenv(sender.upper()+"_EVM_ADDRESS")

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

    its = w3.eth.contract(
    address=Web3.to_checksum_address(ITS_CONTRACT_ADDRESS),
    abi=ITS_ABI,
    )

    token_id_bytes = Web3.to_bytes(hexstr=XRP_TOKEN_ID)
    destination_bytes = receiver.encode("utf-8") 
    metadata = b""

    tx_value = int(Decimal(str(amount)) * Decimal(10**18))
    tx_gas_value = int(Decimal(str(GAS_VALUE_WEI)) * Decimal(10**18))

    tx = its.functions.interchainTransfer(
        token_id_bytes,
        DESTINATION_CHAIN,
        destination_bytes,
        tx_value,
        metadata,
        tx_gas_value,
    ).build_transaction({
        "from": sender,
        "value": tx_value + tx_gas_value,
        "nonce": w3.eth.get_transaction_count(sender),
        "gas": 900000,
        "gasPrice": w3.eth.gas_price,
        "chainId": w3.eth.chain_id,
    })

    return tx