#!/usr/bin/env bash
set -e

HOMEDIR="/app/.exrpd"
CHAINID="xrplevm_1450000-1"

if [ ! -f "$HOMEDIR/config/genesis.json" ]; then
  echo "Chain B ainda não inicializada. Criando genesis..."
  exec bash /app/local-node-b.sh
fi

echo "Chain B já inicializada. Subindo estado existente..."

exec /app/bin/exrpd start \
  --metrics \
  --log_level info \
  --json-rpc.api eth,txpool,personal,net,debug,web3 \
  --home "$HOMEDIR" \
  --chain-id "$CHAINID"