import base58
import json
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountObjects

def resolve_did_object_for_account(account: str, client: JsonRpcClient) -> dict:
    
    resp = client.request(AccountObjects(account=account))
    if resp.status != "success":
        raise RuntimeError(f"Erro ao buscar conta: {resp.result}")
    
    for obj in resp.result.get("account_objects", []):
        if obj.get("LedgerEntryType") == "DID":
            return obj
    raise RuntimeError("Nenhum objeto DID encontrado")


def get_holder_pubkey_from_did(holder_did: str, vm_id: str, client: JsonRpcClient) -> bytes:
    
    # Address a partir de did:xrpl:2:<address>
    parts = holder_did.split(":")
    if len(parts) != 4 or parts[0] != "did" or parts[1] != "xrpl":
        raise ValueError(f"DID inválido: {holder_did}")
    account = parts[-1]
    
    # Buscar ledger object DID da conta
    did_obj = resolve_did_object_for_account(account, client)

    # Campo DIDDocument
    did_document_hex = did_obj["DIDDocument"]
    did_document_str = bytes.fromhex(did_document_hex).decode("utf-8")
    did_document = json.loads(did_document_str)

    if did_document.get("id") != holder_did:
        raise ValueError("id do DIDDocument não bate com o holder_did")
    
    # Campo Data
    data_hex = did_obj.get("Data")
    if not data_hex:
        raise ValueError("Campo Data ausente no DID")
    data_str = bytes.fromhex(data_hex).decode("utf-8")
    data = json.loads(data_str)

    vm_list = data.get("verificationMethod", [])
    if not vm_list:
        raise ValueError("Nenhum verificationMethod encontrado")

    # vm_id = "did:xrpl:2:<addr>#key-1"
    if "#" in vm_id:
        suffix = "#" + vm_id.split("#", 1)[1]  # "#key-1"
    else:
        suffix = vm_id

    for vm in vm_list:
        if vm.get("id") == suffix:
            pkey_b58 = vm.get("pKey")[1:]
            if not pkey_b58:
                raise ValueError("verificationMethod encontrado, mas sem pKey")
            pubkey_bytes = base58.b58decode(pkey_b58)
            if len(pubkey_bytes) != 32:
                raise ValueError(f"Public key Ed25519 deve ter 32 bytes, recebi {len(pubkey_bytes)}")
            return pubkey_bytes
    
    raise ValueError(f"verificationMethod {vm_id} não encontrado no Data do DID")