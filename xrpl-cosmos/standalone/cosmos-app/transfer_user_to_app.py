import os
import json
from utils.make import *
from utils.broadcast import *
from utils.converter import *
from dotenv import load_dotenv
from eth_utils import keccak
from decimal import Decimal


load_dotenv()

CHAIN_ID = os.getenv("CHAIN_ID")

USER_EVM_PRIVATE_KEY = os.getenv("USER_EVM_PRIVATE_KEY").replace("0x", "")
APP_COSMOS_ADDRESS = os.getenv("APP_COSMOS_ADDRESS")

DENOM = os.getenv("DENOM", "axrp")
CONSUME_AMOUNT = "0.1" # em XRP

FEE_AMOUNT = os.getenv("FEE_AMOUNT", "20000000000000000")
GAS_LIMIT = int(os.getenv("GAS_LIMIT", "200000"))

BECH32_PREFIX = "ethm"

MSG_SEND_TYPE_URL = "/cosmos.bank.v1beta1.MsgSend"
ETH_PUBKEY_TYPE_URL = "/ethermint.crypto.v1.ethsecp256k1.PubKey"


def transfer_user_to_app():
    private_key = get_private_key(USER_EVM_PRIVATE_KEY)

    user_cosmos_address = get_user_cosmos_address(private_key)
    pubkey_compressed = get_compressed_pubkey(private_key)

    account_number, sequence = get_account_info(user_cosmos_address)

    msg_send = make_msg_send(
        from_address=user_cosmos_address,
        to_address=APP_COSMOS_ADDRESS,
        amount=str(int(Decimal(str(CONSUME_AMOUNT)) * Decimal(10**18))),
        denom=DENOM,
    )

    msg_any = make_any(MSG_SEND_TYPE_URL, msg_send)

    tx_body = make_tx_body(msg_any)

    pubkey = make_pubkey(pubkey_compressed)
    pubkey_any = make_any(ETH_PUBKEY_TYPE_URL, pubkey)

    signer_info = make_signer_info(pubkey_any, sequence)

    fee = make_fee(
        amount=FEE_AMOUNT,
        denom=DENOM,
        gas_limit=GAS_LIMIT,
    )

    auth_info = make_auth_info(signer_info, fee)

    sign_doc = make_sign_doc(
        body_bytes=tx_body,
        auth_info_bytes=auth_info,
        chain_id=CHAIN_ID,
        account_number=account_number,
    )

    sign_hash = keccak(sign_doc)
    signature = private_key.sign_msg_hash(sign_hash).to_bytes()

    tx_raw = make_tx_raw(
        body_bytes=tx_body,
        auth_info_bytes=auth_info,
        signature=signature,
    )

    response = broadcast_tx(tx_raw)

    output = {
        "User Cosmos Address:": user_cosmos_address,
        "App Cosmos Address:":APP_COSMOS_ADDRESS,
        "Amount:":str(CONSUME_AMOUNT) + "XRP",
        "Code:":response["result"]["code"],
        "TxHash:":response["result"]["hash"]
    }
    if(response["result"]["code"] == 0):
        with open("cosmos-app/logfile.jsonl", "a", encoding="utf-8") as out:
            out.write(json.dumps(output, ensure_ascii=False) + "\n")

    print(output)


transfer_user_to_app()