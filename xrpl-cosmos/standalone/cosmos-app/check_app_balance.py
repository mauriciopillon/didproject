import os
import requests
from dotenv import load_dotenv


load_dotenv()

COSMOS_API_URL = os.getenv("COSMOS_API_URL").rstrip("/")
APP_COSMOS_ADDRESS = os.getenv("APP_COSMOS_ADDRESS")
DENOM = os.getenv("DENOM", "axrp")

def get_balance(address):
    url = f"{COSMOS_API_URL}/cosmos/bank/v1beta1/balances/{address}"

    response = requests.get(url)
    data = response.json()

    for coin in data.get("balances", []):
        if coin.get("denom") == DENOM:
            return coin.get("amount")

    return "0"


balance = int(get_balance(APP_COSMOS_ADDRESS))

print("App Cosmos Address:", APP_COSMOS_ADDRESS)
print("Balance AXRP:", balance)
print("Balance XRP:", balance/10**18)