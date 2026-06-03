const express = require("express");
const { PORT } = require("./config/environmentConfig");
const { createRecoverySdk, createSenderOptions } = require("./config/axelarConfig");
const { AxelarService } = require("./services/axelarService");
const { BridgeService } = require("./services/bridgeService");

const sdk = createRecoverySdk();
const senderOptions = createSenderOptions();

const axelarService = new AxelarService(sdk, senderOptions);
const bridgeService = new BridgeService(axelarService);

const app = express();
app.use(express.json());

app.get("/health", (_req, res) => {
  res.status(200).json({
    ok: true,
    service: "main-js",
  });
});

app.get("/status/:txHash", async (req, res) => {
  try {
    const { txHash } = req.params;
    const eventIndex =
      req.query.eventIndex !== undefined ? Number(req.query.eventIndex) : undefined;

    const status = await bridgeService.getStatus({
      sourceTxHash: txHash,
      eventIndex,
    });

    const commandId = bridgeService.extractCommandId(status);

    res.status(200).json({
      ok: true,
      commandId,
      status,
    });
  } catch (error) {
    res.status(400).json({
      ok: false,
      error: error.message,
    });
  }
});

app.post("/relay", async (req, res) => {
  try {
    const { sourceTxHash, eventIndex } = req.body || {};

    if (!sourceTxHash) {
      return res.status(400).json({
        ok: false,
        error: "sourceTxHash is required",
      });
    }

    const result = await bridgeService.run({
      sourceTxHash,
      eventIndex,
    });

    return res.status(200).json({
      ok: true,
      commandId: result.commandId,
      result,
    });
  } catch (error) {
    return res.status(500).json({
      ok: false,
      error: error.message,
    });
  }
});

app.listen(PORT, () => {
  console.log(`bridge-js listening on http://localhost:${PORT}`);
});