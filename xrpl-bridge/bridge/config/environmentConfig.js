const path = require("path");
const dotenv = require("dotenv");

dotenv.config({ path: path.resolve(process.cwd(), ".env") });

function required(name) {
  const value = process.env[name];
  if (!value || !value.trim()) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value.trim();
}

function optionalInt(name, fallback) {
  const raw = process.env[name];
  if (!raw || !raw.trim()) return fallback;

  const parsed = Number(raw);
  if (!Number.isInteger(parsed) || parsed <= 0) {
    throw new Error(`Environment variable ${name} must be a positive integer`);
  }

  return parsed;
}

module.exports = {
  PORT: optionalInt("PORT", 3000),
  AXELAR_ENVIRONMENT: (process.env.AXELAR_ENVIRONMENT || "TESTNET").trim().toUpperCase(),
  DESTINATION_RPC_URL: required("DESTINATION_RPC_URL"),
  DESTINATION_PRIVATE_KEY: required("DESTINATION_PRIVATE_KEY"),
  POLL_INTERVAL_MS: optionalInt("POLL_INTERVAL_MS", 8000),
  MAX_POLLS: optionalInt("MAX_POLLS", 30),
};