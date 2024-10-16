import './App.css';
import React, { useState, useEffect } from 'react';
import { ErgoProvider, SubmitTx, useErgo } from 'ergo-react-components'; // You'll need to install this package

function App() {
  const [walletAddress, setWalletAddress] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [proxyAddress, setProxyAddress] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [txId, setTxId] = useState(null);
  const { ergo } = useErgo();

  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    if (typeof window.ergoConnector !== 'undefined') {
      const isConnected = await window.ergoConnector.nautilus.connect();
      setIsConnected(isConnected);
      if (isConnected) {
        const address = await window.ergo.get_change_address();
        setWalletAddress(address);
      }
    }
  };

  const connectWallet = async () => {
    if (typeof window.ergoConnector !== 'undefined') {
      try {
        const connected = await window.ergoConnector.nautilus.connect();
        setIsConnected(connected);
        if (connected) {
          const address = await window.ergo.get_change_address();
          setWalletAddress(address);
        }
      } catch (error) {
        console.error("Error connecting to Nautilus wallet:", error);
        setError("Failed to connect to wallet");
      }
    } else {
      setError("Nautilus wallet is not installed");
    }
  };

  const disconnectWallet = async () => {
    if (isConnected) {
      await window.ergoConnector.nautilus.disconnect();
      setIsConnected(false);
      setWalletAddress(null);
    }
  };

  const mintTokensAndCreateProxy = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const height = await ergo.get_current_height();
      const utxos = await ergo.get_utxos();

      // Step 1: Get the unsigned transaction from the backend
      const response = await fetch('http://localhost:3001/create-minting-tx', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ walletAddress, height, utxos }),
      });
      const { unsignedTx } = await response.json();

      // Step 2: Sign the transaction with Nautilus
      const signedTx = await ergo.sign_tx(unsignedTx);

      // Step 3: Submit the signed transaction
      const txId = await ergo.submit_tx(signedTx);

      setTxId(txId);
      setProxyAddress(unsignedTx.outputs[0].address); // Assuming the first output is the proxy address
      setIsLoading(false);
    } catch (error) {
      console.error("Error minting tokens:", error);
      setError("Failed to mint tokens and create proxy");
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="vaporwave-background"></div>
      <div className="content">
        <header className="App-header">
          <h1 className="neon-text">Token Flight</h1>
        </header>
        <main>
          <div className="vaporwave-box">
            {!isConnected ? (
              <button className="vaporwave-button" onClick={connectWallet}>Connect Nautilus Wallet</button>
            ) : (
              <div className="wallet-info">
                <p className="connected-text">Connected: <span className="address">{walletAddress}</span></p>
                <button className="vaporwave-button" onClick={disconnectWallet}>Disconnect Wallet</button>
                <button className="vaporwave-button" onClick={mintTokensAndCreateProxy} disabled={isLoading}>
                  {isLoading ? 'Processing...' : 'Mint Tokens and Create Proxy'}
                </button>
                {txId && <p className="tx-text">Transaction ID: <span className="address">{txId}</span></p>}
                {proxyAddress && <p className="proxy-text">Proxy Address: <span className="address">{proxyAddress}</span></p>}
              </div>
            )}
            {error && <p className="error-text">{error}</p>}
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;