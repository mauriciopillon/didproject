const {
  POLL_INTERVAL_MS,
  MAX_POLLS,
} = require("../config/env");

const STATUS = {
  DEST_GATEWAY_APPROVED: "destination_gateway_approved",
  DEST_EXECUTED: "destination_executed",
  EXPRESS_EXECUTED: "express_executed",
  DEST_EXECUTE_ERROR: "error",
  UNKNOWN_ERROR: "unknown_error",
  CANNOT_FETCH_STATUS: "cannot_fetch_status",
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

class BridgeService {
  constructor(axelarService) {
    this.axelarService = axelarService;
  }

  isExecuted(status) {
    return status === STATUS.DEST_EXECUTED || status === STATUS.EXPRESS_EXECUTED;
  }

  isApproved(status) {
    return status === STATUS.DEST_GATEWAY_APPROVED;
  }

  isFatal(status) {
    return (
      status === STATUS.DEST_EXECUTE_ERROR ||
      status === STATUS.UNKNOWN_ERROR ||
      status === STATUS.CANNOT_FETCH_STATUS
    );
  }

  extractCommandId(statusObject) {
    if (!statusObject || typeof statusObject !== "object") {
      return null;
    }

    return (
      statusObject.commandId ||
      statusObject.commandID ||
      statusObject.command_id ||
      statusObject?.call?.commandId ||
      statusObject?.approved?.commandId ||
      statusObject?.execution?.commandId ||
      null
    );
  }

  attachCommandId(result, ...objects) {
    if (result.commandId) {
      return;
    }

    for (const obj of objects) {
      const maybe = this.extractCommandId(obj);
      if (maybe) {
        result.commandId = maybe;
        return;
      }
    }
  }

  async getStatus({ sourceTxHash, eventIndex }) {
    return this.axelarService.queryStatus(sourceTxHash, eventIndex);
  }

  async run({ sourceTxHash, eventIndex }) {
    const result = {
      sourceTxHash,
      eventIndex,
      commandId: null,
      initialStatus: null,
      relayResponse: null,
      executeResponse: null,
      finalStatus: null,
      polls: [],
    };

    const initial = await this.axelarService.queryStatus(sourceTxHash, eventIndex);
    result.initialStatus = initial;
    this.attachCommandId(result, initial);

    if (this.isExecuted(initial.status)) {
      result.finalStatus = initial;
      this.attachCommandId(result, initial);
      return result;
    }

    if (!this.isApproved(initial.status)) {
      const relayResponse = await this.axelarService.manualRelay(sourceTxHash);
      result.relayResponse = relayResponse;
      this.attachCommandId(result, relayResponse);

      const relaySucceeded =
        relayResponse &&
        (relayResponse.success === true || relayResponse.success === "success");

      if (!relaySucceeded) {
        throw new Error(
          `manualRelayToDestChain failed: ${relayResponse?.error || "unknown error"}`
        );
      }
    }

    let executeTriggered = false;

    for (let i = 0; i < MAX_POLLS; i += 1) {
      const status = await this.axelarService.queryStatus(sourceTxHash, eventIndex);
      result.polls.push(status);
      this.attachCommandId(result, status);

      if (this.isExecuted(status.status)) {
        result.finalStatus = status;
        this.attachCommandId(result, status);
        return result;
      }

      if (this.isFatal(status.status)) {
        throw new Error(
          `Axelar transaction entered fatal state: ${status.status}`
        );
      }

      if (this.isApproved(status.status) && !executeTriggered) {
        const executeResponse = await this.axelarService.execute(sourceTxHash);
        result.executeResponse = executeResponse;
        this.attachCommandId(result, executeResponse);
        executeTriggered = true;

        const executeSucceeded =
          executeResponse &&
          (executeResponse.success === true || executeResponse.success === "success");

        if (!executeSucceeded) {
          throw new Error(
            `execute failed: ${executeResponse?.error || "unknown error"}`
          );
        }
      }

      await sleep(POLL_INTERVAL_MS);
    }

    const lastStatus = await this.axelarService.queryStatus(sourceTxHash, eventIndex);
    result.finalStatus = lastStatus;
    this.attachCommandId(result, lastStatus);

    throw new Error(
      `Timeout waiting for destination execution. Last known status: ${lastStatus.status}`
    );
  }
}

module.exports = {
  BridgeService,
};