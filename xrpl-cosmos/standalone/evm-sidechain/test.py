import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv(override=True)

EVM_RPC_URL = os.getenv("EVM_RPC_URL")
ITS_CONTRACT_ADDRESS = os.getenv("ITS_CONTRACT_ADDRESS")
XRP_TOKEN_ID = os.getenv("XRP_TOKEN_ID")

ITS_ABI = [
    {
        "type": "function",
        "name": "tokenManagerAddress",
        "stateMutability": "view",
        "inputs": [{"name": "tokenId", "type": "bytes32"}],
        "outputs": [{"name": "", "type": "address"}],
    },
    {
        "type": "function",
        "name": "registeredTokenAddress",
        "stateMutability": "view",
        "inputs": [{"name": "tokenId", "type": "bytes32"}],
        "outputs": [{"name": "", "type": "address"}],
    },
    {
        "type": "function",
        "name": "tokenHandler",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [{"name": "", "type": "address"}],
    },
]

w3 = Web3(Web3.HTTPProvider(EVM_RPC_URL))

its = w3.eth.contract(
    address=Web3.to_checksum_address(ITS_CONTRACT_ADDRESS),
    abi=ITS_ABI,
)

print("Chain ID:", w3.eth.chain_id)
print("ITS:", ITS_CONTRACT_ADDRESS)
print("ITS code length:", len(w3.eth.get_code(Web3.to_checksum_address(ITS_CONTRACT_ADDRESS))))

token_manager = its.functions.tokenManagerAddress(XRP_TOKEN_ID).call()
token_manager_code = w3.eth.get_code(Web3.to_checksum_address(token_manager))

print("Token ID:", XRP_TOKEN_ID)
print("TokenManager:", token_manager)
print("TokenManager code length:", len(token_manager_code))

if len(token_manager_code) == 0:
    print("TokenManager NÃO existe para esse tokenId no ITS novo.")
    raise SystemExit

token_address = its.functions.registeredTokenAddress(XRP_TOKEN_ID).call()
token_handler = its.functions.tokenHandler().call()

print("Registered token:", token_address)
print("TokenHandler:", token_handler)