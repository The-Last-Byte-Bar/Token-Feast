# Token Flight

Welcome to Token Flight, a decentralized application (DApp) that brings the spirit of "The Last Byte Bar" to the blockchain world.

## About

Token Flight is a DApp built on the Ergo blockchain. It mints and distributes "Bar" tokens, inspired by "The Last Byte Bar". The application periodically sends these tokens on "flights" to users, creating a unique distribution mechanism.

## Features

- Minting of "Bar" tokens
- Automated "flight" distribution of tokens every 10 blocks
- Bar-themed user interface with random quotes
- Integration with Nautilus wallet for transactions

## Project Structure

- `smart-contracts/`: Ergo smart contracts for token minting and flight distribution
- `off-chain-bot/`: Python bot for automated token flight distribution
- `frontend/`: React-based web interface with a bar ambiance
- `backend/`: Node.js server for handling token flights
- `config/`: Configuration files
- `scripts/`: Utility scripts for deployment and running the flight bot


"It's always flight o'clock somewhere!" - The Last Byte Bar

# Token Flight Startup Procedure

Follow these steps to start your Token Flight system after running the setup script:

## 1. Configure Environment Variables

1.1. Backend Configuration:
   - Navigate to the `backend` directory
   - Create a `.env` file if it doesn't exist
   - Add the following variables (replace with your actual values):
     ```
     ERGO_NODE_URL=http://213.239.193.208:9053
     ERGO_EXPLORER_URL=https://api.ergoplatform.com
     BACKEND_WALLET_MNEMONIC=your backend wallet mnemonic phrase here
     BACKEND_WALLET_PASSWORD=your backend wallet password here
     PROXY_CONTRACT_ADDRESS=your_proxy_contract_address_here
     PORT=3001
     ```

1.2. Off-chain Bot Configuration:
   - Navigate to the `off-chain-bot` directory
   - Create a `.env` file if it doesn't exist
   - Add the following variables (replace with your actual values):
     ```
     ERGO_NODE_URL=http://213.239.193.208:9053
     BOT_WALLET_MNEMONIC=your bot wallet mnemonic phrase here
     BOT_WALLET_PASSWORD=your bot wallet password here
     PROXY_CONTRACT_ADDRESS=your_proxy_contract_address_here
     DISTRIBUTION_INTERVAL=10
     TOKENS_PER_DISTRIBUTION=1000
     ```

## 2. Start the Backend Server

2.1. Open a new terminal window
2.2. Navigate to the `backend` directory
2.3. Run the following command:
     ```
     npm start
     ```
2.4. Verify that the server starts without errors and is listening on the specified port

## 3. Start the Frontend Development Server

3.1. Open a new terminal window
3.2. Navigate to the `frontend` directory
3.3. Run the following command:
     ```
     npm start
     ```
3.4. Your default web browser should open automatically to `http://localhost:3000`
3.5. Verify that the Token Flight interface loads correctly

## 4. Deploy Smart Contracts (if not already deployed)

4.1. Open a new terminal window
4.2. Navigate to the `smart-contracts` directory
4.3. Run the deployment script:
     ```
     ./deploy_flight_contracts.sh
     ```
4.4. Note the addresses of the deployed contracts and update your `.env` files accordingly

## 5. Start the Off-chain Bot

5.1. Open a new terminal window
5.2. Navigate to the `off-chain-bot` directory
5.3. Activate the virtual environment:
     ```
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```
5.4. Start the bot:
     ```
     python src/flight_distribution_bot.py
     ```
5.5. Verify that the bot starts without errors and begins monitoring for distribution events

## 6. System Verification

6.1. Use the frontend interface to initiate a token minting transaction
6.2. Confirm that the transaction is processed by the backend and submitted to the Ergo blockchain
6.3. Monitor the off-chain bot's output to ensure it detects and processes the distribution events
6.4. Check the recipient's wallet to verify that tokens are being distributed as expected

## 7. Ongoing Monitoring

7.1. Keep all terminal windows open to monitor the logs of each component
7.2. Regularly check the Ergo Explorer to verify transactions and token distributions
7.3. Monitor system resources to ensure all components are running smoothly

## Troubleshooting

- If any component fails to start, check the respective logs for error messages
- Ensure all environment variables are correctly set in the `.env` files
- Verify that the Ergo node is accessible and synchronized
- Check that the wallet mnemonics and passwords are correct and the wallets have sufficient funds for transactions

Remember to secure your system and never share sensitive information like wallet mnemonics or passwords.