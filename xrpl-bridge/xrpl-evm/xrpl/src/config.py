from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

def require_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or not str(value).strip():
        raise ValueError(f"Missing required environment variable: {name}")
    return str(value).strip()


BASE_DIR = Path(__file__).resolve().parent
PYTHON_APP_DIR = BASE_DIR.parent
LOGFILE = os.getenv(
    "LOGFILE_PATH",
    str((PYTHON_APP_DIR / "logfile.jsonl").resolve()),
).strip()

XRPL_RPC_URL = os.getenv("XRPL_RPC_URL").strip()
XRPL_SEED = require_env("XRPL_SEED")

AXELAR_XRPL_GATEWAY_ADDRESS = require_env("AXELAR_XRPL_GATEWAY_ADDRESS")
DESTINATION_CHAIN = require_env("DESTINATION_CHAIN")
DESTINATION_CONTRACT_ADDRESS = require_env("DESTINATION_CONTRACT_ADDRESS")

CALL_TYPE = os.getenv("CALL_TYPE", "call_contract").strip()
AMOUNT_DROPS = os.getenv("AMOUNT_DROPS", "1").strip()

BRIDGE_SERVICE_URL = os.getenv("BRIDGE_SERVICE_URL", "").strip()

INCLUDE_PAYLOAD_MEMO = os.getenv("INCLUDE_PAYLOAD_MEMO", "true").strip().lower() in {
    "1",
    "true",
    "yes",
    "y",
}