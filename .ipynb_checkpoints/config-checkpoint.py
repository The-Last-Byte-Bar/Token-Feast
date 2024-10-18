# config.py
import json
from dataclasses import dataclass
from typing import List

@dataclass
class Config:
    node_url: str
    explorer_url: str
    api_key: str
    network_type: str
    node_address: str
    minter_address: str
    recipient_wallets: List[str]
    token_name: str
    token_description: str
    token_total_amount: int
    token_decimals: int
    tokens_per_round: int
    blocks_between_dispense: int

def load_config(file_path: str) -> Config:
    with open(file_path, 'r') as config_file:
        config_data = json.load(config_file)
    
    return Config(
        node_url=config_data['node']['nodeApi']['apiUrl'],
        explorer_url=config_data['node']['explorer_url'],
        api_key=config_data['node']['nodeApi']['apiKey'],
        network_type=config_data['node']['networkType'],
        node_address=config_data['node']['nodeAddress'],
        minter_address=config_data['parameters']['minterAddr'],
        recipient_wallets=config_data['parameters']['recipientWallets'],
        token_name=config_data['token']['name'],
        token_description=config_data['token']['description'],
        token_total_amount=config_data['token']['totalAmount'],
        token_decimals=config_data['token']['decimals'],
        tokens_per_round=config_data['distribution']['tokensPerRound'],
        blocks_between_dispense=config_data['distribution']['blocksBetweenDispense']
    )

def validate_config(config: Config) -> None:
    if not all([config.node_url, config.explorer_url, config.api_key, config.network_type,
                config.node_address, config.minter_address, config.recipient_wallets,
                config.token_name, config.token_description, config.token_total_amount,
                config.token_decimals, config.tokens_per_round, config.blocks_between_dispense]):
        raise ValueError("All configuration fields must be filled")
    
    if not isinstance(config.recipient_wallets, list) or len(config.recipient_wallets) == 0:
        raise ValueError("recipient_wallets must be a non-empty list")
    
    if config.token_total_amount <= 0 or config.tokens_per_round <= 0:
        raise ValueError("Token amounts must be positive")
    
    if config.blocks_between_dispense <= 0:
        raise ValueError("blocks_between_dispense must be positive")
