import json
from datetime import datetime, timezone
from utils.jws import jws

private_key = "ED2A4E34EDC84003058AA334B3AC701484BFE53C433C4AAAEF56EFA4CAE4C905CE"
holder_address = "rNH4PgbHE4JCoH7PvSjFnrXv18A8qk4nJv"
issuer_address = "rL7oLd4KDXcCfjPcCWpLF7WGATxPG7gcVp"
credential_index = "381526BBF3B4F7A2F925A27572A2E8461FBB44F6713C342AAFDAC365572D819C"

VP_Data = {
    "@context":"https://www.w3.org/TR/vc-data-model-2.0/#verifiable-presentations",

    "type": ["VerifiablePresentation", "XRPLDegreeVP"],
    "holder": f"did:xrpl:2:{holder_address}",      

    "xrplCredential":{
        "@context": "https://xrpl.org/docs/references/protocol/ledger-data/ledger-entry-types/credential",                    
        "type": ["XRPLCredential","XRPLDegreeCredential"],
        "issuer":f"did:xrpl:2:{issuer_address}",
        "xrplCredentialRef": {
            "network_id": 2,
            "issuer": issuer_address,            
            "subject": holder_address,         
            "credential_type": "Diploma",
            "index": credential_index          
        }  
    },    
}

proof = {
        "type":"Ed25519Signature",
        "created":datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "proofPurpose":"authentication",
        "verificationMethod":f"did:xrpl:2:{holder_address}#key-1",
        "jws":jws(VP_Data, private_key)
    }

VP_Data["proof"] = proof

with open("holder/verifiable_presentations/diploma_vp.json","w",encoding="utf-8") as f:
    json.dump(VP_Data, f, indent=4, ensure_ascii=False)