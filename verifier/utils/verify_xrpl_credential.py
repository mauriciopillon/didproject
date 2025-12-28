from xrpl.clients import JsonRpcClient
from xrpl.models.requests import LedgerEntry

LSF_ACCEPTED = 0x00010000

def verify_xrpl_credential(vp: dict, client: JsonRpcClient, require_accepted: bool = True) -> dict:
    
    xcred = vp.get("xrplCredential")
    if not xcred:
        raise ValueError("VP não possui campo xrplCredential")

    ref = xcred.get("xrplCredentialRef")
    if not ref:
        raise ValueError("xrplCredential não possui xrplCredentialRef")

    network_id = ref.get("network_id")
    issuer_account = ref.get("issuer")
    subject_account = ref.get("subject")
    credential_type = ref.get("credential_type")
    index = ref.get("index")

    if network_id != 2:
        raise ValueError(f"network_id inesperado ({network_id})")
    if not issuer_account or not subject_account or not credential_type or not index:
        raise ValueError("xrplCredentialRef incompleto")

    # CredentialType para hex
    credential_type_hex = credential_type.encode("utf-8").hex().upper()

    # Buscar a Credential pelo index
    resp = client.request(LedgerEntry(index=index))
    if resp.status != "success":
        raise RuntimeError(f"Erro ao buscar Credential pelo index: {resp.result}")
    
    node = resp.result.get("node")
    if not node:
        raise RuntimeError("LedgerEntry não retornou campo 'node'")

    if node.get("LedgerEntryType") != "Credential":
        raise ValueError("LedgerEntryType não é 'Credential'")

    # Checar Issuer, Subject, CredentialType
    if node.get("Issuer") != issuer_account:
        raise ValueError("Issuer da Credential no ledger não bate com xrplCredentialRef")
    if node.get("Subject") != subject_account:
        raise ValueError("Subject da Credential no ledger não bate com xrplCredentialRef")
    if node.get("CredentialType") != credential_type_hex:
        raise ValueError("CredentialType da Credential no ledger não bate com credential_type da VP")

    # Checar Flag accepted
    flags = node.get("Flags", 0)
    if require_accepted and not (flags & LSF_ACCEPTED):
        raise ValueError("Credential encontrada, mas não aceita (lsfAccepted)")
    
    print("XRPL Credential confirmada.")

    return node