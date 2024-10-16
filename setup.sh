#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Setup smart contracts
echo "Setting up smart contracts..."
cd "$SCRIPT_DIR/smart-contracts"
sbt compile
cd "$SCRIPT_DIR"

# Setup off-chain bot
echo "Setting up off-chain bot..."
cd "$SCRIPT_DIR/off-chain-bot"
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
cd "$SCRIPT_DIR"

# Setup frontend
echo "Setting up frontend..."
cd "$SCRIPT_DIR/frontend"
npm install
cd "$SCRIPT_DIR"

# Setup backend
echo "Setting up backend..."
cd "$SCRIPT_DIR/backend"
npm install
cd "$SCRIPT_DIR"

echo "Setup complete! You can now start each component separately."
echo "To start the frontend: cd frontend && npm start"
echo "To start the backend: cd backend && npm start"
echo "To start the off-chain bot: cd off-chain-bot && source venv/bin/activate && python src/flight_distribution_bot.py"