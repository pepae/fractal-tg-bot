# README for DAO Proposal Notification Telegram Bot

## Overview

This Telegram Bot is designed to monitor DAO (Decentralized Autonomous Organization) proposals on the Ethereum blockchain and notify a specified Telegram chat whenever a new proposal is initialized. It leverages the Ethereum blockchain and Web3 technology to listen for specific events emitted by a smart contract and then uses the Telegram Bot API to send notifications.

## Features

- Monitors DAO proposals through Ethereum smart contract events.
- Sends notifications to a Telegram chat with details of new proposals, including proposal ID, voting end block, and a link to view the proposal on the Fractal frontend.
- Configurable settings for different environments (development and production) and contract addresses.

## Quick Start

### Prerequisites

- Python 3.6 or later.
- A Telegram Bot Token (obtained by creating a bot with @BotFather on Telegram).
- An Infura Project ID for Ethereum blockchain access.
- The smart contract address that emits the proposal events.
- The smart contract ABI.

### Installation

1. **Clone the repository:**

   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install required Python packages:**

   ```
   pip install web3 requests configparser
   ```

3. **Configure the bot:**

   Rename `config.ini.example` to `config.ini` and update it with your settings:

   - `[web3]` section: Infura URL with your project ID.
   - `[etherscan]` section: API URL and the contract address for ABI fetching.
   - `[dao]` section: Addresses for event monitoring and frontend display.
   - `[telegram]` section: Bot token and chat ID where notifications will be sent.
   - `[links]` section: Base URLs for proposal links and environment setting.

### Running the Bot

Execute the script to start monitoring DAO proposals:

```
python fractaltg.py
```

## Documentation

### Configuration (`config.ini`)

- **`[web3]`**:
  - `infura_url`: The full Infura URL, including the project ID, for Ethereum network access.
- **`[etherscan]`**:
  - `api_url`: The Etherscan API URL for fetching the smart contract ABI.
  - `contract_address`: The contract address used for ABI fetching.
- **`[dao]`**:
  - `event_monitoring_contract_address`: The smart contract address that emits the proposal events to monitor.
  - `frontend_display_contract_address`: The contract address used in constructing the frontend proposal link.
- **`[telegram]`**:
  - `bot_token`: Your Telegram Bot token.
  - `chat_id`: The chat ID where the bot will send notifications.
- **`[links]`**:
  - `dev_base_url`: Base URL for the development environment of the Fractal frontend.
  - `non_dev_base_url`: Base URL for the production environment of the Fractal frontend.
  - `environment`: Specifies the environment to use (`dev` or `non_dev`).

### Script (`fractaltg.py`)

The main Python script that initializes the Web3 connection, listens for the `ProposalInitialized` event from the specified smart contract, and sends a Telegram message with the proposal details and link.

### Functions

- **`send_telegram_message(proposal_id, voting_end_block)`**:
  Constructs and sends the message with proposal details to the configured Telegram chat.

- **`monitor_new_proposals(event_filter, poll_interval)`**:
  Continuously checks for new entries in the event filter and calls `send_telegram_message` for each new proposal detected.

### Main Execution Flow

1. Load and parse configuration from `config.ini`.
2. Establish a Web3 connection using the provided Infura URL.
3. Fetch the contract ABI from Etherscan and initialize the contract object for event monitoring.
4. Create an event filter for the `ProposalInitialized` event.
5. Enter a loop to monitor for and handle new proposals, sending notifications as configured.

## Troubleshooting

- Ensure all dependencies are installed and the Python version is compatible.
- Verify the correctness of all configurations in `config.ini`, including the Infura URL, contract addresses, and Telegram bot settings.
- Check the Ethereum network status and your Infura project's usage limits if the script fails to connect or monitor events.

For further assistance, consult the Web3 and Telegram Bot API documentation or seek help from relevant development communities.
