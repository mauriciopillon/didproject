FROM golang:1.23.8

RUN apt update && apt install -y \
    git \
    make \
    jq \
    curl \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone https://github.com/xrplevm/node.git .

RUN make build

RUN cp local-node.sh local-node-a.sh && \
    cp local-node.sh local-node-b.sh && \
    sed -i '/^[[:space:]]*make build[[:space:]]*$/d' local-node-a.sh local-node-b.sh && \
    sed -i 's/MONIKER="localnet"/MONIKER="xrplevm-a"/' local-node-a.sh && \
    sed -i 's/MONIKER="localnet"/MONIKER="xrplevm-b"/' local-node-b.sh && \
    sed -i 's/CHAINID="xrplevm_1449999-1"/CHAINID="xrplevm_1450000-1"/' local-node-b.sh && \
    sed -i 's#unbonding_time"]="60s"#unbonding_time"]="86400s"#g' local-node-a.sh local-node-b.sh && \
    chmod +x local-node-a.sh local-node-b.sh

RUN sed -i '/bin\/exrpd start \\/i\
sed -i '\''s#laddr = "tcp://127.0.0.1:26657"#laddr = "tcp://0.0.0.0:26657"#g'\'' "$CONFIG"\n\
sed -i '\''s#address = "127.0.0.1:8545"#address = "0.0.0.0:8545"#g'\'' "$APP_TOML"\n\
sed -i '\''s#ws-address = "127.0.0.1:8546"#ws-address = "0.0.0.0:8546"#g'\'' "$APP_TOML"\n\
sed -i '\''s#address = "tcp://localhost:1317"#address = "tcp://0.0.0.0:1317"#g'\'' "$APP_TOML"\n\
sed -i '\''s#address = "localhost:9090"#address = "0.0.0.0:9090"#g'\'' "$APP_TOML"' local-node-a.sh local-node-b.sh

COPY scripts/start-persistent-a.sh /usr/local/bin/start-persistent-a.sh
COPY scripts/start-persistent-b.sh /usr/local/bin/start-persistent-b.sh

RUN chmod +x /usr/local/bin/start-persistent-a.sh \
    /usr/local/bin/start-persistent-b.sh

EXPOSE 26656 26657 1317 9090 8545 8546