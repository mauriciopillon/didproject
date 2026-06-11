#!/usr/bin/env bash
set -e

HOMEDIR="/app/.exrpd"
CHAINID="xrplevm_1449999-1"

if [ ! -f "$HOMEDIR/config/genesis.json" ]; then
  echo "Chain A ainda não inicializada. Criando genesis..."
  exec bash /app/local-node-a.sh
fi

echo "Chain A já inicializada. Subindo estado existente..."

exec /app/bin/exrpd start \
  --metrics \
  --log_level info \
  --json-rpc.api eth,txpool,personal,net,debug,web3 \
  --home "$HOMEDIR" \
  --chain-id "$CHAINID"