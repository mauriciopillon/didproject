import os
from dotenv import load_dotenv
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountInfo
from xrpl.utils import drops_to_xrp

load_dotenv()

XRPL_RPC_URL = os.getenv("XRPL_RPC_URL")
XRPL_ACCOUNT = os.getenv("XRPL_ADDRESS")

client = JsonRpcClient(XRPL_RPC_URL)

req = AccountInfo(
    account=XRPL_ACCOUNT,
    ledger_index="validated",
)

response = client.request(req)
account_data = response.result["account_data"]

balance_drops = account_data["Balance"]
balance_xrp = drops_to_xrp(balance_drops)

print("Account:", XRPL_ACCOUNT)
print("Balance XRP:", balance_xrp)