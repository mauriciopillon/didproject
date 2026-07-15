#!/usr/bin/env bash
set -e

cd /app

HOMEDIR="/app/.exrpd"
CHAINID="$CHAIN_ID"
LOCAL_NODE_SCRIPT="/tmp/local-node-${MONIKER}.sh"
NETWORK_PATCH_SCRIPT="/tmp/network-patch-${MONIKER}.sh"

write_network_patch() {
  cat > "$NETWORK_PATCH_SCRIPT" <<'PATCH'
echo "Configurando rede da chain em ${IP}"

sed -i "s|^proxy_app = .*|proxy_app = \"tcp://${IP}:26658\"|" "$CONFIG"

sed -i "/^\[rpc\]/,/^\[/ s|^laddr = .*|laddr = \"tcp://${IP}:${RPC_PORT}\"|" "$CONFIG"
sed -i "/^\[rpc\]/,/^\[/ s|^grpc_laddr = .*|grpc_laddr = \"\"|" "$CONFIG"
sed -i "/^\[rpc\]/,/^\[/ s|^pprof_laddr = .*|pprof_laddr = \"\"|" "$CONFIG"

sed -i "/^\[p2p\]/,/^\[/ s|^laddr = .*|laddr = \"tcp://${IP}:26656\"|" "$CONFIG"
sed -i "/^\[p2p\]/,/^\[/ s|^external_address = .*|external_address = \"${IP}:26656\"|" "$CONFIG"

sed -i "/^\[instrumentation\]/,/^\[/ s|^prometheus = .*|prometheus = false|" "$CONFIG"

sed -i "/^\[api\]/,/^\[/ s|^enable = .*|enable = true|" "$APP_TOML"
sed -i "/^\[api\]/,/^\[/ s|^address = .*|address = \"tcp://${IP}:${REST_PORT}\"|" "$APP_TOML"

sed -i "/^\[grpc\]/,/^\[/ s|^enable = .*|enable = true|" "$APP_TOML"
sed -i "/^\[grpc\]/,/^\[/ s|^address = .*|address = \"${IP}:${GRPC_PORT}\"|" "$APP_TOML"

sed -i "/^\[grpc-web\]/,/^\[/ s|^enable = .*|enable = false|" "$APP_TOML"

sed -i "/^\[json-rpc\]/,/^\[/ s|^enable = .*|enable = true|" "$APP_TOML"
sed -i "/^\[json-rpc\]/,/^\[/ s|^address = .*|address = \"${IP}:${EVM_RPC_PORT}\"|" "$APP_TOML"
sed -i "/^\[json-rpc\]/,/^\[/ s|^ws-address = .*|ws-address = \"${IP}:${EVM_WS_PORT}\"|" "$APP_TOML"
sed -i "/^\[json-rpc\]/,/^\[/ s|^api = .*|api = \"eth,txpool,personal,net,debug,web3\"|" "$APP_TOML"
sed -i "/^\[json-rpc\]/,/^\[/ s|^metrics-address = .*|metrics-address = \"127.0.0.1:0\"|" "$APP_TOML"

sed -i "/^\[rosetta\]/,/^\[/ s|^enable = .*|enable = false|" "$APP_TOML"
PATCH
}

inject_network_patch() {
  write_network_patch

  awk -v patch="$NETWORK_PATCH_SCRIPT" '
    /^bin\/exrpd start[[:space:]]*\\/ && inserted == 0 {
      while ((getline line < patch) > 0) print line
      close(patch)
      inserted = 1
    }
    { print }
  ' "$LOCAL_NODE_SCRIPT" > "${LOCAL_NODE_SCRIPT}.tmp"

  mv "${LOCAL_NODE_SCRIPT}.tmp" "$LOCAL_NODE_SCRIPT"
  chmod +x "$LOCAL_NODE_SCRIPT"
}

patch_existing_configs() {
  CONFIG="$HOMEDIR/config/config.toml"
  APP_TOML="$HOMEDIR/config/app.toml"

  write_network_patch
  bash "$NETWORK_PATCH_SCRIPT"
}

if [ ! -f "$HOMEDIR/config/genesis.json" ]; then
  echo "$CHAIN_LABEL ainda não inicializada. Criando genesis com chain-id $CHAINID..."

  cp /app/local-node.sh "$LOCAL_NODE_SCRIPT"

  sed -i "s/^CHAINID=.*/CHAINID=\"$CHAINID\"/" "$LOCAL_NODE_SCRIPT"
  sed -i "s/^MONIKER=.*/MONIKER=\"$MONIKER\"/" "$LOCAL_NODE_SCRIPT"

  sed -i '/^[[:space:]]*--metrics[[:space:]]/d' "$LOCAL_NODE_SCRIPT"

  inject_network_patch

  exec bash "$LOCAL_NODE_SCRIPT"
fi

echo "$CHAIN_LABEL já inicializada. Subindo estado existente com chain-id $CHAINID..."

patch_existing_configs

exec /app/bin/exrpd start \
  --log_level info \
  --json-rpc.api eth,txpool,personal,net,debug,web3 \
  --home "$HOMEDIR" \
  --chain-id "$CHAINID"
