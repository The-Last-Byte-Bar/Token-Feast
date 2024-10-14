#!/bin/bash

# Setup smart contracts
echo "Setting up smart contracts..."
cd smart-contracts
sbt compile
cd ..

# Setup off-chain bot
echo "Setting up off-chain bot..."
cd off-chain-bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

# Setup frontend
echo "Setting up frontend..."
cd frontend
npm install
cd ..

# Setup backend
echo "Setting up backend..."
cd backend
npm install
cd ..

echo "Setup complete! You can now start each component separately."
echo "To start the frontend: cd frontend && npm start"
echo "To start the backend: cd backend && npm start"
echo "To start the off-chain bot: cd off-chain-bot && source venv/bin/activate && python src/flight_distribution_bot.py"