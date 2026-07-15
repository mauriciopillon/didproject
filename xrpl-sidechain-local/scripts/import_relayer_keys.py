from pathlib import Path
import json
import os
import subprocess


ROOT_DIR = Path(__file__).resolve().parents[1]
CHAINS_FILE = ROOT_DIR / "chains.json"
MNEMONICS_DIR = ROOT_DIR / "relayer" / "hermes" / "mnemonics"

HERMES_CONTAINER = "hermes"
DERIVATION_PATH = "m/44'/60'/0'/0/0"


def load_chains():
    data = json.loads(CHAINS_FILE.read_text(encoding="utf-8"))
    return data["chains"]


def run(cmd):
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def write_mnemonic_file(chain):
    MNEMONICS_DIR.mkdir(parents=True, exist_ok=True)

    key_name = chain["key_name"]
    mnemonic = chain["relayer_mnemonic"].strip()

    path = MNEMONICS_DIR / f"{key_name}.txt"
    path.write_text(mnemonic + "\n", encoding="utf-8")
    os.chmod(path, 0o644)

    print(f"Mnemonic escrito: {path}")


def check_mnemonic_visible_inside_hermes(chain):
    key_name = chain["key_name"]
    expected = chain["relayer_mnemonic"].strip()

    cmd = [
        "docker",
        "exec",
        HERMES_CONTAINER,
        "sh",
        "-lc",
        f"cat /home/hermes/.hermes/mnemonics/{key_name}.txt",
    ]

    result = run(cmd)
    actual = result.stdout.strip()

    if actual != expected:
        raise RuntimeError(
            f"Mnemonic visto pelo Hermes não bate com chains.json para {chain['label']}"
        )


def reset_hermes_keys():
    cmd = [
        "docker",
        "exec",
        "-u",
        "0",
        HERMES_CONTAINER,
        "sh",
        "-lc",
        "rm -rf /home/hermes/.hermes/keys/* && "
        "mkdir -p /home/hermes/.hermes/keys && "
        "chown -R 2000:2000 /home/hermes/.hermes/keys && "
        "chmod -R u+rwX /home/hermes/.hermes/keys",
    ]

    run(cmd)


def import_key(chain):
    key_name = chain["key_name"]
    chain_id = chain["chain_id"]

    print(f"Importando {key_name} em {chain_id}...")

    cmd = [
        "docker",
        "exec",
        HERMES_CONTAINER,
        "hermes",
        "keys",
        "add",
        "--chain",
        chain_id,
        "--mnemonic-file",
        f"/home/hermes/.hermes/mnemonics/{key_name}.txt",
        "--key-name",
        key_name,
        "--hd-path",
        DERIVATION_PATH,
        "--overwrite",
    ]

    result = run(cmd)

    if result.stdout.strip():
        print(result.stdout.strip())

    if result.stderr.strip():
        print(result.stderr.strip())


def list_key(chain):
    cmd = [
        "docker",
        "exec",
        HERMES_CONTAINER,
        "hermes",
        "keys",
        "list",
        "--chain",
        chain["chain_id"],
    ]

    result = run(cmd)

    if result.stdout.strip():
        print(result.stdout.strip())

    if result.stderr.strip():
        print(result.stderr.strip())


def main():
    chains = load_chains()

    for chain in chains:
        write_mnemonic_file(chain)

    for chain in chains:
        check_mnemonic_visible_inside_hermes(chain)

    reset_hermes_keys()

    for chain in chains:
        import_key(chain)
        list_key(chain)
        print()


if __name__ == "__main__":
    main()
