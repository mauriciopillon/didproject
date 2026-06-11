import json
import time
from decimal import Decimal
from eth_utils import keccak

from utils.make import *
from utils.broadcast import *
from utils.converter import *


CHAIN_ID = "xrplevm_1449999-1"

COSMOS_API_URL = "http://localhost:1317"
COSMOS_RPC_URL = "http://localhost:26657"

USER_EVM_PRIVATE_KEY = "D8161FD5FDF4EB216A6556DC639A2543B0ED9ABDBCEB9971FE08CFBA56F588C8"

ALICE_CHAIN_B_COSMOS_ADDRESS = "ethm1dakgyqjulg29m5fmv992g2y66m9g2mjn6hahwg"

SOURCE_PORT = "transfer"
SOURCE_CHANNEL = "channel-2"

DENOM = "axrp"
TRANSFER_AMOUNT = "1"  # em XRP

FEE_AMOUNT = "20000000000000000"
GAS_LIMIT = 400000

TIMEOUT_SECONDS = 1000

IBC_TRANSFER_TYPE_URL = "/ibc.applications.transfer.v1.MsgTransfer"
ETH_PUBKEY_TYPE_URL = "/ethermint.crypto.v1.ethsecp256k1.PubKey"


def transfer_cross_chain():
    private_key = get_private_key(USER_EVM_PRIVATE_KEY.replace("0x", ""))

    alice_chain_a_cosmos_address = get_user_cosmos_address(private_key)
    pubkey_compressed = get_compressed_pubkey(private_key)

    account_number, sequence = get_account_info(alice_chain_a_cosmos_address)

    amount_axrp = str(int(Decimal(str(TRANSFER_AMOUNT)) * Decimal(10**18)))
    timeout_timestamp = int((time.time() + TIMEOUT_SECONDS) * 1_000_000_000)

    msg_transfer = make_msg_transfer(
        source_port=SOURCE_PORT,
        source_channel=SOURCE_CHANNEL,
        sender=alice_chain_a_cosmos_address,
        receiver=ALICE_CHAIN_B_COSMOS_ADDRESS,
        amount=amount_axrp,
        denom=DENOM,
        timeout_timestamp=timeout_timestamp,
    )

    msg_any = make_any(IBC_TRANSFER_TYPE_URL, msg_transfer)

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
        "Source Chain": CHAIN_ID,
        "Source Port": SOURCE_PORT,
        "Source Channel": SOURCE_CHANNEL,
        "Sender Chain A": alice_chain_a_cosmos_address,
        "Receiver Chain B": ALICE_CHAIN_B_COSMOS_ADDRESS,
        "Amount": str(TRANSFER_AMOUNT) + " XRP",
        "Amount axrp": amount_axrp,
        "Code": response["result"]["code"],
        "TxHash": response["result"]["hash"],
    }

    if(response["result"]["code"] == 0):
        with open("tests/logfile.jsonl", "a", encoding="utf-8") as out:
            out.write(json.dumps(output, ensure_ascii=False) + "\n")

    print(json.dumps(output, indent=2, ensure_ascii=False))


transfer_cross_chain()
