import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def require_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or not str(value).strip():
        raise ValueError(f"Missing required environment variable: {name}")
    return str(value).strip()


def optional_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default

    parsed = int(raw)
    if parsed <= 0:
        raise ValueError(f"Environment variable {name} must be a positive integer")
    return parsed



EVM_RPC_URL = require_env("EVM_RPC_URL")
EVM_PRIVATE_KEY = require_env("EVM_PRIVATE_KEY")

ARTIFACT_JSON_PATH = require_env("ARTIFACT_JSON_PATH")
AXELAR_GATEWAY_ADDRESS = os.getenv("AXELAR_GATEWAY_ADDRESS", "").strip()
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "").strip()

BASE_DIR = Path(__file__).resolve().parent
PYTHON_APP_DIR = BASE_DIR.parent
LOGFILE_PATH = os.getenv(
    "LOGFILE_PATH",
    str((PYTHON_APP_DIR / "logfile.jsonl").resolve()),
).strip()

GAS_LIMIT = optional_int("GAS_LIMIT", 3_000_000)