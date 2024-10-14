#!/bin/bash

# Compile the contracts
cd smart-contracts
sbt compile

# Deploy MintBarToken contract
sbt "runMain MintBarToken"

# Deploy FlightProxyContract
# Note: This step might require additional parameters or setup
sbt "runMain FlightProxyContract"

echo "Contracts deployed successfully!"