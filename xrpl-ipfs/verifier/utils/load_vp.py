import json
from pathlib import Path

def load_vp(path: str) -> dict:

    vp_str = Path(path).read_text(encoding="utf-8")
    vp = json.loads(vp_str)

    return vp