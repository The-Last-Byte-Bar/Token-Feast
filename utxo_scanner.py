# utxo_scanner.py
import logging
from ergo_python_appkit.appkit import ErgoAppKit
from org.ergoplatform.appkit import Address
from typing import List, Dict

logger = logging.getLogger(__name__)

def scan_proxy_utxos(appKit: ErgoAppKit, proxy_address: str, token_id: str) -> List[Dict]:
    unspent_boxes = appKit.getUnspentBoxes(proxy_address)
    
    utxos = []
    for box in unspent_boxes:
        box_tokens = {token.getId().toString(): token.getValue() for token in box.getTokens()}
        if token_id in box_tokens:
            utxos.append({
                "box_id": box.getId().toString(),
                "value": box.getValue(),
                "tokens": box_tokens
            })
    
    logger.info(f"Found {len(utxos)} UTXOs in proxy contract")
    return utxos