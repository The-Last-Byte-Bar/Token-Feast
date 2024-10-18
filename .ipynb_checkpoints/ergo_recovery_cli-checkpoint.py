import argparse
import json
import logging
from ergo_python_appkit.appkit import ErgoAppKit
from org.ergoplatform.appkit import Address, ErgoValue, Constants

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        return json.load(config_file)

def recover_erg(appKit, proxy_address, node_address):
    unspent_boxes = appKit.boxesToSpend(proxy_address, 0)
    
    if not unspent_boxes:
        logger.info("No unspent boxes found in the proxy contract")
        return
    
    total_erg = sum(box.getValue() for box in unspent_boxes)
    total_tokens = {}
    
    for box in unspent_boxes:
        for token in box.getTokens():
            token_id = token.getId().toString()
            token_amount = token.getValue()
            if token_id in total_tokens:
                total_tokens[token_id] += token_amount
            else:
                total_tokens[token_id] = token_amount
    
    output = appKit.buildOutBox(
        value=total_erg - int(1e6),  # Subtract fee
        tokens=total_tokens,
        registers=None,
        contract=appKit.contractFromAddress(node_address)
    )
    
    unsigned_tx = appKit.buildUnsignedTransaction(
        inputs=unspent_boxes,
        outputs=[output],
        fee=int(1e6),
        sendChangeTo=Address.create(node_address).getErgoAddress()
    )
    signed_tx = appKit.signTransactionWithNode(unsigned_tx)
    
    tx_id = appKit.sendTransaction(signed_tx)
    logger.info(f"ERG and tokens recovered to node wallet. Transaction ID: {tx_id}")
    logger.info(f"Recovered {total_erg/1e9:.9f} ERG and {total_tokens} tokens")

def main():
    parser = argparse.ArgumentParser(description="Ergo Recovery CLI Tool")
    parser.add_argument("--config", default="ergo.json", help="Path to the configuration file")
    parser.add_argument("--proxy", required=True, help="Proxy contract address to recover from")
    args = parser.parse_args()

    config = load_config(args.config)
    
    node_url = config['node']['nodeApi']['apiUrl']
    explorer_url = config['node']['explorer_url']
    api_key = config['node']['nodeApi']['apiKey']
    node_address = config['node']['nodeAddress']
    
    appKit = ErgoAppKit(node_url, config['node']['networkType'], explorer_url, api_key)
    
    logger.info(f"Attempting to recover funds from proxy address: {args.proxy}")
    recover_erg(appKit, args.proxy, node_address)

if __name__ == "__main__":
    main()