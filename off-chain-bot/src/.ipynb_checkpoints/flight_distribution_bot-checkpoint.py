import os
from dotenv import load_dotenv
from ergo_python_appkit.appkit import ErgoAppKit, ErgoTreeTemplate, ErgoContract

load_dotenv()

def distribute_tokens():
    ergo_client = ErgoAppKit(os.getenv('ERGO_NODE_URL'))
    proxy_address = os.getenv('PROXY_CONTRACT_ADDRESS')
    distribution_interval = int(os.getenv('DISTRIBUTION_INTERVAL'))
    tokens_per_distribution = int(os.getenv('TOKENS_PER_DISTRIBUTION'))

    # Get the current height
    current_height = ergo_client.getCurrentHeight()

    # Find the proxy box
    proxy_box = ergo_client.getBoxesByAddress(proxy_address)[0]
    last_flight_height = proxy_box.getRegisters()[1].getValue()

    if current_height >= last_flight_height + distribution_interval:
        # Time for a new distribution
        recipient_address = ErgoTreeTemplate.fromErgoTree(proxy_box.getRegisters()[0].getValue()).toAddress()
        
        input_box = ergo_client.getBoxesById(proxy_box.getId())
        output_box = ergo_client.buildOutBox(
            value=proxy_box.getValue(),
            tokens=[(proxy_box.getTokens()[0].getId(), proxy_box.getTokens()[0].getValue() - tokens_per_distribution)],
            contract=ErgoContract(proxy_address),
            registers=[recipient_address.getErgoTree(), current_height]
        )
        
        distribution_box = ergo_client.buildOutBox(
            value=ergo_client.getMinimumBoxValue(),
            tokens=[(proxy_box.getTokens()[0].getId(), tokens_per_distribution)],
            contract=ErgoContract(recipient_address.toString()),
        )

        unsigned_tx = ergo_client.buildUnsignedTransaction(
            inputs=[input_box],
            outputs=[output_box, distribution_box],
            fee=ergo_client.getMinimumFee(),
            changeAddress=proxy_address
        )

        signed_tx = ergo_client.signTransaction(unsigned_tx)
        tx_id = ergo_client.sendTransaction(signed_tx)
        print(f"Distribution transaction sent: {tx_id}")

if __name__ == "__main__":
    while True:
        distribute_tokens()
        time.sleep(60)  # Check every minute