# This allows you to create or update a DID
from xrpl.models import CredentialDelete
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.transaction import submit_and_wait
from xrpl.utils import str_to_hex


# connect to the xrpl via a client
print("Connecting to client")
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)
print("connected!")

# User credentials from seed
seed_user = "sEdTZHgVTQrHJJNRiytkst15mXH6jQM"
wallet_user = Wallet.from_seed(seed=seed_user)
address_user = wallet_user.address

# Issuer account
address_usp = "rL7oLd4KDXcCfjPcCWpLF7WGATxPG7gcVp"

# Credential Delete transaction | User ou Issuer podem deletar
credential_delete_tx = CredentialDelete(
    account=wallet_user.address, # issuer da credencial
    issuer=address_usp, # alvo da credencial
    credential_type=str_to_hex("Diploma") # tipo da credencial
)

# Sign, submit and wait for response
credential_delete_tx_response = submit_and_wait(
    transaction=credential_delete_tx,
    client=client,
    wallet=wallet_user
)

credential_delete_tx_result = credential_delete_tx_response.result

print(credential_delete_tx_result["meta"]["TransactionResult"])
print(credential_delete_tx_result["hash"])