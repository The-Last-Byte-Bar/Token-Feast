# Ergo Token Distribution Bot

This project implements an automated token distribution system on the Ergo blockchain. It includes a minting setup and a distribution bot that periodically sends tokens to a list of specified recipient addresses.

## Features

- Token minting with customizable parameters
- Proxy contract creation for secure token holding
- Automated token distribution to multiple recipients
- Configurable distribution rounds and frequency

## Recent Updates

1. **Even Distribution per Round**: The distribution logic has been updated to evenly split the tokens per round among all recipient addresses.
2. **ERG Allocation**: The minting process now ensures that the proxy contract receives enough ERG to cover all rounds of token distribution.
3. **Configuration Validation**: Added checks to ensure that the `tokens_per_round` is divisible by the number of recipient wallets.

## Setup

1. Clone this repository
2. Install the required dependencies (list them here or refer to a requirements.txt file)
3. Set up your configuration file (see `config_example.json` for reference)

## Usage

### Minting Setup

Run the minting setup script to create the proxy contract and mint tokens:

```
python minting_setup.py <path_to_config.json>
```

This will create a proxy contract, mint the specified amount of tokens, and save the necessary information for the distribution bot.

### Distribution Bot

After the minting setup is complete, run the distribution bot:

```
python distribution_bot.py <path_to_config.json>
```

The bot will automatically distribute tokens to the specified recipient addresses at the configured intervals.

## Configuration

Create a `config.json` file with the following structure:

```json
{
  "node_url": "https://node-url.example",
  "network_type": "MAINNET",
  "explorer_url": "https://explorer-url.example",
  "api_key": "your-api-key",
  "minter_address": "address_of_the_minter",
  "node_address": "address_of_the_node",
  "token_name": "Your Token Name",
  "token_description": "Description of your token",
  "token_total_amount": 1000000,
  "token_decimals": 0,
  "recipient_wallets": ["address1", "address2", "address3"],
  "tokens_per_round": 1000,
  "blocks_between_dispense": 720
}
```

Ensure that `token_total_amount` is divisible by `tokens_per_round`, and `tokens_per_round` is divisible by the number of recipient wallets.

## Files

- `minting_setup.py`: Sets up the proxy contract and mints tokens
- `distribution_bot.py`: Runs the automated token distribution
- `config.py`: Handles configuration loading and validation
- `token_minting.py`: Contains the token minting logic
- `proxy_contract.py`: Handles the creation of the proxy contract

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Specify your license here]
