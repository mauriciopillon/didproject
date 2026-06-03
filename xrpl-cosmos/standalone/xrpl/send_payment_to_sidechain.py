import os
import json
from eth_abi import encode, decode
from dotenv import load_dotenv
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment, Memo
from xrpl.transaction import submit_and_wait
from xrpl.utils import xrp_to_drops, str_to_hex

load_dotenv()

XRPL_RPC_URL = os.getenv("XRPL_RPC_URL")
XRPL_SEED = os.getenv("XRPL_SEED")
DESTINATION_EVM_ADDRESS = os.getenv("USER_EVM_ADDRESS")
AXELAR_XRPL_GATEWAY = os.getenv("AXELAR_XRPL_GATEWAY")
DESTINATION_CHAIN = os.getenv("DESTINATION_CHAIN")

GAS_FEE_AMOUNT = "3000000"
XRP_AMOUNT = 1
SENDING_AMOUNT = str(
    int(xrp_to_drops(XRP_AMOUNT)) + int(GAS_FEE_AMOUNT)
)


client = JsonRpcClient(XRPL_RPC_URL)
wallet = Wallet.from_seed(XRPL_SEED)


def to_hex_lower(value: str) -> str:
    return value.encode("utf-8").hex()


def memo(memo_type: str, memo_data: str) -> Memo:
    return Memo(
        memo_type=to_hex_lower(memo_type),
        memo_data=to_hex_lower(memo_data),
    )

def memo_bytes(memo_type: str, memo_data: bytes):
    return Memo(
        memo_type=to_hex_lower(memo_type),
        memo_data=memo_data.hex(),
    )

# user_address = "0x32057C923B4CAA6D93CBB10E01639E751ED56A84"
# some_id = "0xB488A46ECF2CFB2A4251564F6E7206FD7AE791ECDBD5C9E902570674EB2C2678"

# payload = encode(
#     ["address", "bytes32"],
#     [
#         user_address,
#         bytes.fromhex(some_id.removeprefix("0x")),
#     ],
# )


def build_interchain_transfer_payment():

    payment = Payment(
        account=wallet.address,
        destination=AXELAR_XRPL_GATEWAY,
        amount=SENDING_AMOUNT, # XRP_AMOUNT + GAS_FEE
        memos=[
            memo("type", "interchain_transfer"),
            memo("destination_address", DESTINATION_EVM_ADDRESS.replace("0x", "")),
            memo("destination_chain", "xrpl-evm"),
            memo("gas_fee_amount", "3000000"),
        ],
    )

    return payment


def send_xrp_to_evm_sidechain():
    payment = build_interchain_transfer_payment()

    response = submit_and_wait(
        transaction=payment,
        client=client,
        wallet=wallet,
    )

    output = {
        "XRPL source address:": wallet.classic_address,
        "Destination EVM address:": DESTINATION_EVM_ADDRESS,
        "XRPL transaction hash:": response.result["hash"],
        "Result:": response.result["meta"]["TransactionResult"]
    }

    print(output)
    with open("xrpl/logfile.jsonl", "a", encoding="utf-8") as out:
        out.write(json.dumps(output, ensure_ascii=False) + "\n")
    return response.result["hash"]


tx_hash = send_xrp_to_evm_sidechain()