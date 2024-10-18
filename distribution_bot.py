# distribution_bot.py
import asyncio
import logging
import sys
import json
from ergo_python_appkit.appkit import ErgoAppKit
from config import load_config
from utxo_scanner import scan_proxy_utxos
from token_distribution import distribute_tokens
from org.ergoplatform.appkit import Address

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    if len(sys.argv) < 2:
        print("Usage: python distribution_bot.py <path_to_config.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    config = load_config(config_path)

    # Load bot information
    with open("bot_info.json", "r") as f:
        bot_info = json.load(f)

    proxy_address = bot_info["proxy_contract_address"]
    token_id = bot_info["token_id"]
    recipient_wallets = bot_info["recipient_wallets"]
    tokens_per_round = bot_info["tokens_per_round"]
    blocks_between_dispense = bot_info["blocks_between_dispense"]

    appKit = ErgoAppKit(config.node_url, config.network_type, config.explorer_url, config.api_key)

    # Get the proxy contract from the address
    proxy_contract = appKit.contractFromAddress(proxy_address)

    while True:
        try:
            utxos = scan_proxy_utxos(appKit, proxy_address, token_id)
            logger.info(f"Scanned UTXOs: {utxos}")
            if utxos:
                try:
                    logger.info(f"Attempting to distribute {tokens_per_round} tokens to {len(recipient_wallets)} recipients")
                    distribute_tokens(appKit, utxos, token_id, recipient_wallets, tokens_per_round, proxy_contract)
                except ValueError as ve:
                    logger.warning(f"Failed to distribute tokens: {str(ve)}")
                except Exception as e:
                    logger.error(f"Error during token distribution: {str(e)}")
                    logger.exception("Full stack trace:")
            else:
                logger.info("No UTXOs available for distribution")
            await asyncio.sleep(blocks_between_dispense * 120)  # Assuming 2 minutes per block
        except Exception as e:
            logger.error(f"Error during UTXO scanning: {str(e)}")
            logger.exception("Full stack trace:")
            await asyncio.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    asyncio.run(main())