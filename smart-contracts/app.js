import React, { useState } from 'react';

const MintTokenComponent = () => {
  const [walletAddress, setWalletAddress] = useState(null);
  const [txId, setTxId] = useState(null);
  const [error, setError] = useState(null);

  const connectWallet = async () => {
    if (typeof ergoConnector !== 'undefined') {
      try {
        const connected = await ergoConnector.nautilus.connect();
        if (connected) {
          const address = await ergo.get_change_address();
          setWalletAddress(address);
        }
      } catch (err) {
        setError("Failed to connect to Nautilus wallet");
      }
    } else {
      setError("Nautilus wallet is not installed");
    }
  };

  const mintTokens = async () => {
    try {
      // Get UTXOs from Nautilus
      const utxos = await ergo.get_utxos();

      // Prepare the transaction on the backend
      const response = await fetch('http://localhost:8080/prepare-mint-transaction', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          walletAddress,
          utxos: utxos.map(utxo => utxo.boxId),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to prepare transaction');
      }

      const unsignedTx = await response.json();

      // Sign the transaction with Nautilus
      const signedTx = await ergo.sign_tx(unsignedTx);

      // Submit the transaction
      const txId = await ergo.submit_tx(signedTx);

      setTxId(txId);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      {!walletAddress ? (
        <button onClick={connectWallet}>Connect Nautilus Wallet</button>
      ) : (
        <div>
          <p>Connected: {walletAddress}</p>
          <button onClick={mintTokens}>Mint Tokens</button>
        </div>
      )}
      {txId && <p>Transaction submitted: {txId}</p>}
      {error && <p style={{color: 'red'}}>{error}</p>}
    </div>
  );
};

export default MintTokenComponent;