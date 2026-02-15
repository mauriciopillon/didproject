# This allows you to create or update a DID
import json
from xrpl.models import CredentialCreate
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.transaction import submit_and_wait
from xrpl.utils import str_to_hex


# connect to the xrpl via a client
print("Connecting to client")
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)
print("connected!")

# Issuer credentials from seed
seed_usp = "sEdV8EK8uPMkCRHYcYG8x7jKxqj5mag"
wallet_usp = Wallet.from_seed(seed=seed_usp)
address_usp = wallet_usp.address

# User account
address_user = "rNH4PgbHE4JCoH7PvSjFnrXv18A8qk4nJv"

# Credential type
credential_type = "Diploma"

# Uri data
uri_data = {
            "curso":"Engenharia",
            "ano":"2025",
            
        }

# Credential Create transaction
credential_create_tx = CredentialCreate(
    account=wallet_usp.address, # issuer da credencial
    subject=address_user, # alvo da credencial
    credential_type=str_to_hex(credential_type), # tipo da credencial
    uri=str_to_hex(json.dumps(uri_data, ensure_ascii=False, separators=(",", ":")))   
)

# Sign, submit and wait for response
credential_create_tx_response = submit_and_wait(
    transaction=credential_create_tx,
    client=client,
    wallet=wallet_usp
)

credential_create_tx_result = credential_create_tx_response.result

print(f"Transaction result: {credential_create_tx_result["meta"]["TransactionResult"]}")
print(f"Hash: {credential_create_tx_result["hash"]}")