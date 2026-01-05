from utils.load_vp import load_vp
from utils.verify_xrpl_credential import verify_xrpl_credential
from xrpl.clients import JsonRpcClient

JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)

vp_path = "holder/verifiable_presentations/diploma_vp.json"

vp = load_vp(vp_path)

try:
    credential = verify_xrpl_credential(vp=vp, client=client)

    # Print credential
    print("\nIssuer :", credential["Issuer"])
    print("Subject :", credential["Subject"])
    print("Flags :", credential["Flags"])
    print("Index :", credential["index"])
    print("Type:", bytes.fromhex(credential["CredentialType"]).decode('utf-8'))
    print("URI :", bytes.fromhex(credential["URI"]).decode('utf-8'))
    
except Exception as e:
    print(f"{e}")