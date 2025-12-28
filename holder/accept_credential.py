# This allows you to create or update a DID
from xrpl.models import CredentialAccept
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
# rNH4PgbHE4JCoH7PvSjFnrXv18A8qk4nJv

seed = "sEdV8EK8uPMkCRHYcYG8x7jKxqj5mag"
wallet_usp = Wallet.from_seed(seed=seed)

# Issuer account
address_usp = "rL7oLd4KDXcCfjPcCWpLF7WGATxPG7gcVp"

# Credential Create transaction
credential_accept_tx = CredentialAccept(
    account=wallet_holder.address, # alvo da credencial
    issuer=address_usp, # issuer da credencial
    credential_type=str_to_hex("Diploma") # tipo da credencial
)

# Sign, submit and wait for response
credential_accept_tx_response = submit_and_wait(
    transaction=credential_accept_tx,
    client=client,
    wallet=wallet_holder
)

credential_accept_tx_result = credential_accept_tx_response.result

print(f"Transaction result: {credential_accept_tx_result["meta"]["TransactionResult"]}")
print(f"Hash: {credential_accept_tx_result["hash"]}")