const express = require('express');
const router = express.Router();
const { getUnsignedTransaction, submitTransaction } = require('../services/ergoService');

router.get('/unsignedTransaction', async (req, res) => {
  try {
    const unsignedTx = await getUnsignedTransaction();
    res.json(unsignedTx);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create unsigned transaction' });
  }
});

router.post('/submitTransaction', async (req, res) => {
  try {
    const signedTx = req.body;
    const txId = await submitTransaction(signedTx);
    res.json({ txId });
  } catch (error) {
    res.status(500).json({ error: 'Failed to submit transaction' });
  }
});

module.exports = router;