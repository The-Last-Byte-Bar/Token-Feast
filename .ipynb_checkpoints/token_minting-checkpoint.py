import logging
from ergo_python_appkit.appkit import ErgoAppKit
from org.ergoplatform.appkit import Address
from config import Config
import math

ERG_TO_NANOERG = 1e9
NANOERG_PER_RECIPIENT = int(0.001 * ERG_TO_NANOERG)
FEE = int(0.001 * ERG_TO_NANOERG)
MIN_BOX_VALUE = int(0.001 * ERG_TO_NANOERG)

logger = logging.getLogger(__name__)

def mint_tokens_to_proxy(appKit: ErgoAppKit, config: Config, proxy_contract: bytes) -> str:
    # Calculate the total number of distribution rounds
    total_rounds = math.ceil(config.token_total_amount / config.tokens_per_round)
    
    # Calculate the ERG needed for one round of distribution
    num_recipients = len(config.recipient_wallets)
    erg_per_round = (NANOERG_PER_RECIPIENT + MIN_BOX_VALUE) * num_recipients + FEE

    # Calculate the total ERG needed for all rounds
    total_erg_for_distribution = erg_per_round * total_rounds

    # Add a buffer for the final change box
    erg_amount = total_erg_for_distribution + MIN_BOX_VALUE

    logger.info(f"Calculated total ERG needed for all distributions: {erg_amount/ERG_TO_NANOERG:.9f} ERG")
    logger.info(f"Number of distribution rounds: {total_rounds}")
    logger.info(f"Tokens per round: {config.tokens_per_round}")
    logger.info(f"Number of recipients: {num_recipients}")
    logger.info(f"Tokens per recipient per round: {config.tokens_per_round // num_recipients}")

    # We need to send erg_amount to the proxy, plus an additional FEE for this transaction
    total_erg_needed = erg_amount + FEE

    unspent_boxes = appKit.boxesToSpend(config.minter_address, total_erg_needed)
    
    token_id = unspent_boxes[0].getId().toString()
    
    mint_output = appKit.mintToken(
        value=erg_amount,  # This is the amount that goes to the proxy
        tokenId=token_id,
        tokenName=config.token_name,
        tokenDesc=config.token_description,
        mintAmount=config.token_total_amount,
        decimals=config.token_decimals,
        contract=appKit.contractFromTree(proxy_contract)
    )
    
    unsigned_tx = appKit.buildUnsignedTransaction(
        inputs=unspent_boxes,
        outputs=[mint_output],
        fee=FEE,
        sendChangeTo=Address.create(config.minter_address).getErgoAddress()
    )
    signed_tx = appKit.signTransactionWithNode(unsigned_tx)
    tx_id = appKit.sendTransaction(signed_tx)
    logger.info(f"Minting transaction sent. Transaction ID: {tx_id}")
    logger.info(f"Minted {config.token_total_amount} tokens with {erg_amount/ERG_TO_NANOERG:.9f} ERG locked in proxy contract")
    logger.info(f"Total ERG spent (including transaction fee): {total_erg_needed/ERG_TO_NANOERG:.9f} ERG")
    return token_id