import json
from pathlib import Path
from typing import Any


def load_artifact(artifact_json_path: str) -> dict[str, Any]:
    path = Path(artifact_json_path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"Artifact file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        artifact = json.load(file)

    if "abi" not in artifact:
        raise ValueError(f"Artifact has no 'abi': {path}")

    return artifact


def load_abi(artifact_json_path: str) -> list[dict[str, Any]]:
    artifact = load_artifact(artifact_json_path)
    return artifact["abi"]


def load_bytecode(artifact_json_path: str) -> str:
    artifact = load_artifact(artifact_json_path)

    bytecode = artifact.get("bytecode")
    if not isinstance(bytecode, str) or not bytecode.strip():
        raise ValueError(f"Artifact has no usable 'bytecode': {artifact_json_path}")

    return bytecode.strip()