// File: scripts/deploy_flight_contracts.sh
#!/bin/bash

cd "$(dirname "$0")/.."

echo "Compiling and running MintBarToken..."
sbt "runMain tokenflight.MintBarToken"

echo "Compiling and running FlightProxyContract..."
sbt "runMain tokenflight.FlightProxyContract"

echo "Deployment completed."