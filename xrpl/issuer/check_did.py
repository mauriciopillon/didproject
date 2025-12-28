from xrpl.models import LedgerEntry
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet

# connect to the xrpl via a client
print("Connecting to client")
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)
print("connected!")


# User wallet
seed_user = "sEdTZHgVTQrHJJNRiytkst15mXH6jQM"
wallet_user = Wallet.from_seed(seed=seed_user)
address_user = wallet_user.address

# Issuer wallet
seed_usp = "sEdV8EK8uPMkCRHYcYG8x7jKxqj5mag"
wallet_usp = Wallet.from_seed(seed=seed_usp)
address_usp = wallet_usp.address


# build the request for the account's DID
req = LedgerEntry(ledger_index="validated", did=address_user)

# submit request and awaiting result
print("submitting request \n")
response = client.request(req)
result = response.result

# parse result
if "index" in result and "Account" in result["node"]:
    print(f'DID index: {result["node"]["index"]}')
    # print(f'DID Document HEX: {result["node"]["DIDDocument"]}')
    print(f'DID Document Raw: {bytes.fromhex(result["node"]["DIDDocument"]).decode("utf-8")}')
    # print(f'Data: {result["node"]["Data"]}')
    print(f'Data Raw: {bytes.fromhex(result["node"]["Data"]).decode("utf-8")}')
    # print(f'URI: {result["node"]["URI"]}')
    # print(f'URI Raw: {bytes.fromhex(result["node"]["URI"]).decode("utf-8")}')

else:
    print("No DID found for this account")
