import React from 'react';
import { ergoConnector } from '@vechain/ergo-connector';

const LaunchButton = () => {
  const handleLaunch = async () => {
    if (typeof ergoConnector !== 'undefined') {
      try {
        const connected = await ergoConnector.nautilus.connect();
        if (connected) {
          const unsignedTx = await fetchUnsignedTransaction();
          const signedTx = await ergoConnector.nautilus.signTx(unsignedTx);
          const txId = await submitTransaction(signedTx);
          alert(`Token flight launched! Transaction ID: ${txId}`);
        } else {
          alert('Failed to connect to Nautilus wallet');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Check the console for details.');
      }
    } else {
      alert('Nautilus wallet is not installed');
    }
  };

  const fetchUnsignedTransaction = async () => {
    // Fetch unsigned transaction from your backend
    const response = await fetch('/api/unsignedTransaction');
    return response.json();
  };

  const submitTransaction = async (signedTx) => {
    // Submit signed transaction to your backend
    const response = await fetch('/api/submitTransaction', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(signedTx),
    });
    return response.text();
  };

  return (
    <button onClick={handleLaunch} className="launch-button">
      Launch Token Flight
    </button>
  );
};

export default LaunchButton;
