import configparser
import logging
import requests
import json
import time
from web3 import Web3

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Initialize Web3 connection using the Infura URL from config file
infura_url = config['web3']['infura_url']
w3 = Web3(Web3.HTTPProvider(infura_url))
logging.info("Web3 connection initialized")

# Etherscan API URL and event monitoring contract address from config
etherscan_api_url = f"{config['etherscan']['api_url']}?module=contract&action=getabi&address={config['dao']['event_monitoring_contract_address']}&format=raw"

# Fetch the ABI
response = requests.get(etherscan_api_url)
if response.status_code == 200:
    dao_contract_abi = response.text
    logging.info("Successfully fetched contract ABI")
else:
    logging.error("Failed to fetch ABI")
    exit(1)

# Convert the ABI from string to JSON
dao_contract_abi = json.loads(dao_contract_abi)

# Event monitoring contract address from config
event_monitoring_contract_address = config['dao']['event_monitoring_contract_address']

# Convert to checksum address for the event monitoring contract
checksum_address = Web3.to_checksum_address(event_monitoring_contract_address)
logging.info(f"Checksum address for event monitoring: {checksum_address}")

# Initialize DAO Contract for event monitoring
dao_contract = w3.eth.contract(address=checksum_address, abi=dao_contract_abi)
logging.info("DAO contract for event monitoring initialized")

# Frontend display contract address from config
frontend_display_contract_address = config['dao']['frontend_display_contract_address']

# Load link format from config
environment = config['links']['environment'].strip()
base_url_key = f"{environment}_base_url"
base_url = config['links'][base_url_key].strip() + frontend_display_contract_address + "/proposals/"

# Function to Send Telegram Message with Proposal Link
def send_telegram_message(proposal_id, voting_end_block):
    proposal_link = base_url + str(proposal_id)
    message = f"New DAO Proposal Initialized:\nID: {proposal_id}\nVoting End Block: {voting_end_block}\nProposal Link: {proposal_link}"
    url = f"https://api.telegram.org/bot{config['telegram']['bot_token']}/sendMessage"
    data = {"chat_id": config['telegram']['chat_id'], "text": message}
    response = requests.post(url, data=data)
    logging.info(f"Telegram response: {response.text}")

# Monitor New Proposals
def monitor_new_proposals(event_filter, poll_interval):
    while True:
        try:
            for event in event_filter.get_new_entries():
                proposal_id = event.args.proposalId
                voting_end_block = event.args.votingEndBlock
                send_telegram_message(proposal_id, voting_end_block)  # Updated function call
            time.sleep(poll_interval)
        except Exception as e:
            logging.error(f"Error in monitoring proposals: {str(e)}")

# Main Function
if __name__ == "__main__":
    proposal_initialized_filter = dao_contract.events.ProposalInitialized.create_filter(fromBlock="latest")
    logging.info("ProposalInitialized event filter created")
    poll_interval = 10  # Can be made configurable too
    monitor_new_proposals(proposal_initialized_filter, poll_interval)
