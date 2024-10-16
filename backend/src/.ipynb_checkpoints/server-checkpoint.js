import express from 'express';
import cors from 'cors';
import { ErgoAddress, OutputBuilder, TransactionBuilder } from '@fleet-sdk/core';
import { getErgoClient } from './ergoClient';

const app = express();
app.use(cors());
app.use(express.json());

app.post('/create-minting-tx', async (req, res) => {
  try {
    const { walletAddress, height, utxos } = req.body;
    const ergoClient = await getErgoClient();

    const proxyContract = ergoClient.contractFromAddress(process.env.PROXY_CONTRACT_ADDRESS);
    const recipientAddress = ErgoAddress.fromBase58(walletAddress);
    const tokenAmount = BigInt(1000000); // 1 million tokens

    const unsignedTx = new TransactionBuilder(height)
      .from(utxos)
      .to(
        new OutputBuilder(BigInt(1000000), proxyContract.ergoTree)
          .mintToken({
            amount: tokenAmount,
            name: 'Bar Token',
            description: 'The Last Byte Bar Token',
            decimals: 0,
          })
          .setAdditionalRegisters({
            R4: recipientAddress.ergoTree,
            R5: height, // Set the initial flight height
          })
      )
      .sendChangeTo(recipientAddress)
      .payMinFee()
      .build();

    res.json({ unsignedTx: unsignedTx.toEIP12Object() });
  } catch (error) {
    console.error('Error creating minting transaction:', error);
    res.status(500).json({ error: 'Failed to create minting transaction' });
  }
});

app.listen(3001, () => console.log('Server running on port 3001'));