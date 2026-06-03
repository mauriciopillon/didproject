# Inicialização das chains A e B:
```
docker compose up -d --build
```
### Para verificar o funcionamento dos containers,  `docker logs -f xrplevm-a` e, em um segundo terminal `docker logs -f xrplevm-b`.

## Verificação dos endpoints:
### Chain A
#### RPC Cosmos
```
curl http://localhost:26657/status
```
#### RPC EVM
```
curl -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
  http://localhost:8545
```
### Chain B
#### RPC Cosmos
```
curl http://localhost:36657/status
```
#### RPC EVM
```
curl -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
  http://localhost:9545
```