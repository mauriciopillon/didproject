import base64
import json
from .resolve_did import get_holder_pubkey_from_did
from nacl.signing import VerifyKey
from nacl.encoding import RawEncoder
from xrpl.clients import JsonRpcClient


def b64url_decode(s: str) -> bytes:
    padding = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + padding)


def verify_vp_signature(vp: dict, client: JsonRpcClient) -> None:
    
    proof = vp.get("proof")
    if not proof:
        raise ValueError("VP não possui campo 'proof'")

    jws = proof.get("jws")
    vm_id = proof.get("verificationMethod")

    if not jws or not vm_id:
        raise ValueError("Proof sem jws ou verificationMethod")

    # Decompor JWS
    try:
        header_b64, payload_b64, sig_b64 = jws.split(".")
    except ValueError:
        raise ValueError("JWS incorreto")

    # validar header.alg == "EdDSA"
    header_bytes = b64url_decode(header_b64)
    header = json.loads(header_bytes.decode("utf-8"))
    if header.get("alg") != "EdDSA":
        raise ValueError(f"Algoritmo JWS inesperado: {header.get('alg')}")

    # Recriar VP sem proof e serializar
    vp_no_proof = dict(vp)
    vp_no_proof.pop("proof", None)

    vp_payload = json.dumps(
        vp_no_proof,
        separators=(",", ":"),
        sort_keys=True
    ).encode("utf-8")

    expected_payload_b64 = base64.urlsafe_b64encode(vp_payload).rstrip(b"=").decode("ascii")
    if payload_b64 != expected_payload_b64:
        raise ValueError("Payload do JWS não corresponde a VP")

    # Resolver DID do holder e obter public key
    holder_did = vp.get("holder")
    if not holder_did:
        raise ValueError("VP não possui holder")

    pubkey_bytes = get_holder_pubkey_from_did(holder_did, vm_id, client)

    #  Verificar assinatura Ed25519
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature = b64url_decode(sig_b64)

    vk = VerifyKey(pubkey_bytes, encoder=RawEncoder)
    try:
        vk.verify(signing_input, signature)
    except Exception as e:
        raise ValueError(f"Assinatura da VP inválida: {e}")
    
    print("Assinatura da VP confirmada.")