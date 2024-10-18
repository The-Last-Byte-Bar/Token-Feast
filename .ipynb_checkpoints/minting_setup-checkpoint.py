# minting_setup.py
import asyncio
import logging
import sys
import json
from ergo_python_appkit.appkit import ErgoAppKit
from config import load_config, validate_config
from proxy_contract import create_proxy_contract
from token_minting import mint_tokens_to_proxy
from org.ergoplatform.appkit import Address, ErgoTreeTemplate

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    if len(sys.argv) < 2:
        print("Usage: python minting_setup.py <path_to_config.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    config = load_config(config_path)
    validate_config(config)

    appKit = ErgoAppKit(config.node_url, config.network_type, config.explorer_url, config.api_key)

    # Create proxy contract
    current_height = appKit._ergoClient.execute(lambda ctx: ctx.getHeight())
    unlock_height = current_height + 1
    proxy_contract = create_proxy_contract(appKit, config.recipient_wallets, unlock_height, config.node_address)
    proxy_address = Address.fromErgoTree(proxy_contract, appKit._networkType).toString()
    logger.info(f"Proxy contract address: {proxy_address}")

    # Mint tokens
    token_id = mint_tokens_to_proxy(appKit, config, proxy_contract)
    logger.info(f"Tokens minted. Token ID: {token_id}")

    # Save important information for the bot
    bot_info = {
        "proxy_contract_address": proxy_address,
        "token_id": token_id,
        "recipient_wallets": config.recipient_wallets,
        "tokens_per_round": config.tokens_per_round,
        "blocks_between_dispense": config.blocks_between_dispense
    }

    with open("bot_info.json", "w") as f:
        json.dump(bot_info, f, indent=2)
    
    logger.info("Bot information saved to bot_info.json")

if __name__ == "__main__":
    asyncio.run(main())