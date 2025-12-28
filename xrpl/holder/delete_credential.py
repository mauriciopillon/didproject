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

# holder credentials from seed
seed_holder = "sEdTZHgVTQrHJJNRiytkst15mXH6jQM"
wallet_holder = Wallet.from_seed(seed=seed_holder)
address_holder = wallet_holder.address

# Issuer account
address_usp = "rL7oLd4KDXcCfjPcCWpLF7WGATxPG7gcVp"

# Credential Delete transaction | holder ou Issuer podem deletar
credential_delete_tx = CredentialDelete(
    account=wallet_holder.address, # issuer da credencial
    issuer=address_usp, # alvo da credencial
    credential_type=str_to_hex("Diploma 2") # tipo da credencial
)

# Sign, submit and wait for response
credential_delete_tx_response = submit_and_wait(
    transaction=credential_delete_tx,
    client=client,
    wallet=wallet_holder
)

credential_delete_tx_result = credential_delete_tx_response.result

print(credential_delete_tx_result["meta"]["TransactionResult"])
print(credential_delete_tx_result["hash"])