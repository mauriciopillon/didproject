import os
from web3 import Web3
from src.tx_builder import build_transaction
from src.tx_signer import sign_transaction
from src.tx_sender import send_transaction
from dotenv import load_dotenv

load_dotenv()

EVM_RPC_URL = os.getenv("EVM_RPC_URL")

w3 = Web3(Web3.HTTPProvider(EVM_RPC_URL))

def create_transaction(body):
    tx = build_transaction(w3=w3, amount=body.amount, receiver=body.receiver, sender=body.sender)
    
    signed_tx = sign_transaction(w3=w3, tx=tx, pkey= os.getenv(body.sender.upper()+"_EVM_PRIVATE_KEY"))
    
    tx_hash = send_transaction(w3=w3, signed_tx=signed_tx)

    return{ "tx_hash":tx_hash }