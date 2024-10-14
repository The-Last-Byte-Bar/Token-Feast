const { ErgoAppKit } = require('ergo_appkit_js');

const nodeUrl = 'http://213.239.193.208:9053/';
const explorerUrl = 'https://api.ergoplatform.com/';

const getUnsignedTransaction = async () => {
  const ergoClient = new ErgoAppKit(nodeUrl, explorerUrl);

  // Implement logic to create unsigned transaction
  // This is a placeholder and needs to be implemented based on your specific requirements
  const unsignedTx = await ergoClient.createUnsignedTransaction(/* parameters */);

  return unsignedTx;
};

const submitTransaction = async (signedTx) => {
  const ergoClient = new ErgoAppKit(nodeUrl, explorerUrl);

  // Submit the signed transaction to the network
  const txId = await ergoClient.sendTransaction(signedTx);

  return txId;
};

module.exports = {
  getUnsignedTransaction,
  submitTransaction,
};