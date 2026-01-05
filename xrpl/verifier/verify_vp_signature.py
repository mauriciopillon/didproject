from utils.load_vp import load_vp
from utils.verify_vp_signature import verify_vp_signature
from xrpl.clients import JsonRpcClient

JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)

vp_path = "holder/verifiable_presentations/diploma_vp.json"

vp = load_vp(vp_path)

try:
    verify_vp_signature(vp=vp, client=client)
except Exception as e:
    print(f"{e}")