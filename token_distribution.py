import logging
from ergo_python_appkit.appkit import ErgoAppKit
from org.ergoplatform.appkit import Address
from typing import List, Dict

logger = logging.getLogger(__name__)

ERG_TO_NANOERG = 1e9
NANOERG_PER_RECIPIENT = int(0.001 * ERG_TO_NANOERG)
MIN_BOX_VALUE = int(0.001 * ERG_TO_NANOERG)
FEE = int(0.001 * ERG_TO_NANOERG)

def distribute_tokens(appKit: ErgoAppKit, utxos: List[Dict], token_id: str, recipient_addresses: List[str], tokens_per_round: int, proxy_contract) -> None:
    total_available_erg = sum(utxo['value'] for utxo in utxos)
    total_available_tokens = sum(utxo['tokens'].get(token_id, 0) for utxo in utxos)

    logger.info(f"Total available ERG: {total_available_erg/ERG_TO_NANOERG:.9f}")
    logger.info(f"Total available tokens: {total_available_tokens}")

    # Ensure we have enough tokens for at least one round
    if total_available_tokens < tokens_per_round:
        logger.warning(f"Not enough tokens for a full round. Available: {total_available_tokens}, Required: {tokens_per_round}")
        return

    # Calculate tokens per recipient for this round
    num_recipients = len(recipient_addresses)
    tokens_per_recipient = tokens_per_round // num_recipients
    
    if tokens_per_recipient == 0:
        logger.warning(f"Not enough tokens to distribute to all recipients. Tokens per round: {tokens_per_round}, Recipients: {num_recipients}")
        return

    # Recalculate the actual number of tokens to distribute this round
    tokens_to_distribute = tokens_per_recipient * num_recipients

    # Calculate ERG requirements
    erg_per_recipient = NANOERG_PER_RECIPIENT + MIN_BOX_VALUE
    total_erg_needed = (erg_per_recipient * num_recipients) + FEE + MIN_BOX_VALUE  # Include change box

    if total_available_erg < total_erg_needed:
        logger.warning(f"Not enough ERG for distribution. Available: {total_available_erg/ERG_TO_NANOERG:.9f}, Needed: {total_erg_needed/ERG_TO_NANOERG:.9f}")
        return

    logger.info(f"Distributing {tokens_to_distribute} tokens to {num_recipients} recipients")
    logger.info(f"Tokens per recipient: {tokens_per_recipient}")
    logger.info(f"ERG per recipient: {erg_per_recipient/ERG_TO_NANOERG:.9f}")

    input_boxes = []
    for utxo in utxos:
        boxes = appKit.getBoxesById([utxo['box_id']])
        if boxes:
            input_boxes.append(boxes[0])
        else:
            logger.warning(f"Box with id {utxo['box_id']} not found")

    if not input_boxes:
        logger.error("No valid input boxes found")
        return

    outputs = []
    total_erg_used = 0
    total_tokens_used = 0

    for recipient in recipient_addresses:
        output = appKit.buildOutBox(
            value=erg_per_recipient,
            tokens={token_id: tokens_per_recipient},
            registers=None,
            contract=appKit.contractFromAddress(recipient)
        )
        outputs.append(output)
        total_erg_used += erg_per_recipient
        total_tokens_used += tokens_per_recipient

    total_erg_used += FEE
    change_value = total_available_erg - total_erg_used
    change_tokens = total_available_tokens - total_tokens_used

    logger.info(f"Total ERG to be used: {total_erg_used/ERG_TO_NANOERG:.9f}")
    logger.info(f"Total tokens to be distributed: {total_tokens_used}")
    logger.info(f"Change ERG: {change_value/ERG_TO_NANOERG:.9f}")
    logger.info(f"Change tokens: {change_tokens}")

    if change_value > 0 or change_tokens > 0:
        change_output = appKit.buildOutBox(
            value=max(change_value, MIN_BOX_VALUE),
            tokens={token_id: change_tokens} if change_tokens > 0 else None,
            registers=None,
            contract=proxy_contract
        )
        outputs.append(change_output)

    try:
        unsigned_tx = appKit.buildUnsignedTransaction(
            inputs=input_boxes,
            outputs=outputs,
            fee=FEE,
            sendChangeTo=proxy_contract.toAddress()
        )
        signed_tx = appKit.signTransactionWithNode(unsigned_tx)
        tx_id = appKit.sendTransaction(signed_tx)
        logger.info(f"Tokens distributed to {num_recipients} recipients. Transaction ID: {tx_id}")
        logger.info(f"Distributed {total_tokens_used} tokens with {total_erg_used/ERG_TO_NANOERG:.9f} ERG")
    except Exception as e:
        logger.error(f"Failed to build or send transaction: {str(e)}")
        logger.info(f"Inputs: {[box.getId().toString() for box in input_boxes]}")
        logger.info(f"Outputs: {[output.getValue() for output in outputs]}")