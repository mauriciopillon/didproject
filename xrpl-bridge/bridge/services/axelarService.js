class AxelarService {
  constructor(sdk, senderOptions) {
    this.sdk = sdk;
    this.senderOptions = senderOptions;
  }

  normalizeTxHash(txHash) {
    const clean = String(txHash || "").trim();
    if (!clean) {
      throw new Error("sourceTxHash is required");
    }

    return clean.startsWith("0x") ? clean : `0x${clean}`;
  }

  async queryStatus(sourceTxHash, eventIndex) {
    const txHash = this.normalizeTxHash(sourceTxHash);

    if (eventIndex === undefined || eventIndex === null) {
      return this.sdk.queryTransactionStatus(txHash);
    }

    return this.sdk.queryTransactionStatus(txHash, Number(eventIndex));
  }

  async manualRelay(sourceTxHash) {
    const txHash = this.normalizeTxHash(sourceTxHash);
    return this.sdk.manualRelayToDestChain(txHash, this.senderOptions);
  }

  async execute(sourceTxHash) {
    const txHash = this.normalizeTxHash(sourceTxHash);
    return this.sdk.execute(txHash, this.senderOptions);
  }
}

module.exports = {
  AxelarService,
};