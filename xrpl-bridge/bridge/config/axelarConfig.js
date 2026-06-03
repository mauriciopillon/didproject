const { AxelarGMPRecoveryAPI, Environment } = require("@axelar-network/axelarjs-sdk");
const { ethers } = require("ethers");
const {
  AXELAR_ENVIRONMENT,
  DESTINATION_RPC_URL,
  DESTINATION_PRIVATE_KEY,
} = require("./environmentConfig");

function mapEnvironment(name) {
  switch (name) {
    case "TESTNET":
      return Environment.TESTNET;
    case "MAINNET":
      return Environment.MAINNET;
    default:
      throw new Error(`Unsupported AXELAR_ENVIRONMENT: ${name}`);
  }
}

function createRecoverySdk() {
  return new AxelarGMPRecoveryAPI({
    environment: mapEnvironment(AXELAR_ENVIRONMENT),
  });
}

function createSenderOptions() {
  const provider = new ethers.providers.JsonRpcProvider(DESTINATION_RPC_URL);

  return {
    provider,
    privateKey: DESTINATION_PRIVATE_KEY,
  };
}

module.exports = {
  createRecoverySdk,
  createSenderOptions,
};