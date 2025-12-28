# This allows you to create or update a DID
import json
from xrpl.models import DIDSet
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.transaction import submit_and_wait
from xrpl.utils import str_to_hex
from utils.multibase import base58


# connect to the xrpl via a client
print("Connecting to client")
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)
print("connected!")

# Wallet credentials from seed
seed_holder = "sEdTZHgVTQrHJJNRiytkst15mXH6jQM"
wallet_holder = Wallet.from_seed(seed=seed_holder)
address_holder = wallet_holder.address
public_key_holder = wallet_holder.public_key


document = {
    "@context":"https://www.w3.org/TR/did-1.1/#did-documents",
    "id": f"did:xrpl:2:{address_holder}"
}

data = {
    "verificationMethod":[
            {
            "id":"#key-1",
            "type":"Ed25519VerificationKey",
            "pKey":base58(public_key_holder)
        }
    ]
}

# uri = " "

# DID SET transaction
# str_to_hex() converts the inputted string to blockchain understandable hexadecimal
did_set_txn = DIDSet(
    account=wallet_holder.address,
    did_document=str_to_hex(json.dumps(document, ensure_ascii=False, separators=(",", ":"))),
    data=str_to_hex(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    # uri=str_to_hex(uri),
)


# sign, submit the transaction and wait for the response
print("signing and submitting the transaction, awaiting a response \n")
did_set_txn_response = submit_and_wait(
    transaction=did_set_txn,
    client=client, 
    wallet=wallet_holder
)

# Parse response for result
did_set_txn_result = did_set_txn_response.result

# Print result and transaction hash
print(f"Transaction result: {did_set_txn_result["meta"]["TransactionResult"]}")
print(f"Hash: {did_set_txn_result["hash"]}")