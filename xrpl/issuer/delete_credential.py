from xrpl.models import CredentialDelete
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.transaction import submit_and_wait
from xrpl.utils import str_to_hex
from dotenv import load_dotenv
import os
load_dotenv()

# connect to the xrpl via a client
print("Connecting to client")
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)
print("connected!")

# Credential type for deletion
credential_type = "Diploma"

# Holder address
holder_address = os.getenv("HOLDER_ADDRESS")

# Issuer Wallet
issuer_seed = os.getenv("ISSUER_SEED")
issuer_wallet = Wallet.from_seed(seed=issuer_seed)
issuer_address = issuer_wallet.address

# Credential Delete transaction | Holder ou Issuer podem deletar
credential_delete_tx = CredentialDelete(
    account=holder_address, # Alvo da credencial
    issuer=issuer_address, # Issuer da credencial
    credential_type=str_to_hex(credential_type) # tipo da credencial
)

# Sign, submit and wait for response
credential_delete_tx_response = submit_and_wait(
    transaction=credential_delete_tx,
    client=client,
    wallet=issuer_wallet
)

credential_delete_tx_result = credential_delete_tx_response.result

print(credential_delete_tx_result["meta"]["TransactionResult"])
print(credential_delete_tx_result["hash"])