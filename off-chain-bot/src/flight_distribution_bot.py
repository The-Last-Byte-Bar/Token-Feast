import time
import os
from dotenv import load_dotenv
from ergo_python_appkit.appkit import *

# Load environment variables
load_dotenv()

def launch_token_flight(node_url, proxy_address, wallet_mnemonic, wallet_password):
    ergo_client = ErgoAppKit(node_url)
    
    while True:
        try:
            current_height = ergo_client.get_current_height()
            unspent_boxes = ergo_client.get_unspent_boxes(proxy_address)
            
            for box in unspent_boxes:
                if is_flight_ready(box, current_height):
                    initiate_flight(ergo_client, box, wallet_mnemonic, wallet_password, current_height)
            
            time.sleep(60)  # Check every minute
        except Exception as e:
            print(f"Flight delay: {e}")
            time.sleep(60)  # Wait a minute before retrying

def is_flight_ready(box, current_height):
    last_flight_height = box.get_registers()[1].value
    distribution_interval = int(os.getenv('DISTRIBUTION_INTERVAL', 10))
    return current_height >= last_flight_height + distribution_interval

def initiate_flight(ergo_client, box, wallet_mnemonic, wallet_password, current_height):
    tokens_per_distribution = int(os.getenv('TOKENS_PER_DISTRIBUTION', 1000))
    
    # Create and sign the transaction
    unsigned_tx = create_distribution_tx(ergo_client, box, tokens_per_distribution, current_height)
    signed_tx = ergo_client.sign_transaction(unsigned_tx, wallet_mnemonic, wallet_password)
    
    # Submit the transaction
    tx_id = ergo_client.send_transaction(signed_tx)
    print(f"Token flight launched! Transaction ID: {tx_id}")

def create_distribution_tx(ergo_client, box, tokens_to_distribute, current_height):
    # Implement the logic to create the unsigned transaction
    # This is a placeholder and needs to be implemented based on your specific requirements
    pass

if __name__ == "__main__":
    NODE_URL = os.getenv('ERGO_NODE_URL')
    PROXY_ADDRESS = os.getenv('PROXY_CONTRACT_ADDRESS')
    WALLET_MNEMONIC = os.getenv('WALLET_MNEMONIC')
    WALLET_PASSWORD = os.getenv('WALLET_PASSWORD')
    
    launch_token_flight(NODE_URL, PROXY_ADDRESS, WALLET_MNEMONIC, WALLET_PASSWORD)