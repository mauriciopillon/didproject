import json
from urllib import error, request
from typing import Any


def post_to_bridge(bridge_service_url: str, source_tx_hash: str) -> dict[str, Any] | None:
    if not bridge_service_url.strip():
        return None

    body = json.dumps({"sourceTxHash": source_tx_hash}).encode("utf-8")

    req = request.Request(
        url=bridge_service_url.rstrip("/") + "/relay",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=15) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        return {
            "ok": False,
            "status": exc.code,
            "error": raw,
        }
    except Exception as exc:
        return {
            "ok": False,
            "error": str(exc),
        }