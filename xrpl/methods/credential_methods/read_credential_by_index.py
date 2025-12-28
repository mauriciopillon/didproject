from xrpl.clients import JsonRpcClient
from xrpl.models.requests import LedgerEntry

credential_index = "381526BBF3B4F7A2F925A27572A2E8461FBB44F6713C342AAFDAC365572D819C"

client = JsonRpcClient("https://s.altnet.rippletest.net:51234")
req = LedgerEntry(index=credential_index)
resp = client.request(req)

credential = resp.result["node"]  

print("Issuer :", credential["Issuer"])
print("Subject :", credential["Subject"])
print("Flags :", credential["Flags"])
print("Index :", credential["index"])
print("Type:", bytes.fromhex(credential["CredentialType"]).decode('utf-8'))
print("URI :", bytes.fromhex(credential["URI"]).decode('utf-8'))