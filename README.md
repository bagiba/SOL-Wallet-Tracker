# Solana Wallet Tracker

This script allows users to receive real-time transaction alerts for specific Solana wallets directly in a Discord text channel. It sets up a receiver that listens for transaction data and formats it into rich Discord embeds, complete with market cap information and quick links to various trading platforms (Photon, Trojan, Axiom, DexScreener, Pump.fun).

## Prerequisites

This project relies on **Helius Enhanced WebSockets** to capture and send the real-time on-chain transaction data to this application. 

You must configure Helius to point to the `/webh` endpoint of this running application. For instructions on how to set this up, please refer to the official documentation:
[Helius Enhanced WebSockets Documentation](https://www.helius.dev/docs/enhanced-websockets)

## Features

- **Real-Time Alerts:** Receive instant notifications for Swaps, Transfers, and Pump.fun trades.
- **Discord Integration:** Formatted messages via Discord Webhooks.
- **Market Cap Fetching:** Automatically retrieves token market caps using DexScreener and Pump.fun APIs.
- **Trade Details:** Displays whether the transaction was a Buy or Sale, the SOL amount, and the token quantity.
- **Quick Links:** Provides direct links to chart tools and trading bots for the transacted token.

## Setup Instructions

1. **Clone the repository** (if you haven't already).

2. **Install the required dependencies:**
   Make sure you have Python installed. Run the following command to install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables:**
   - Create a file named `.env` in the root directory of the project.
   - Add your Discord Webhook URL to the `.env` file like this:
     ```env
     WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url_here
     ```

4. **Run the application:**
   ```bash
   python wallettracker.py
   ```
   *(Note: For external services to reach your local machine during development, you will need to expose your local server to the internet using a tool like ngrok or localtunnel.)*

## How it Works

Once the server is running and your Helius configuration is set up, Helius will send transaction data to your `/webh` endpoint. The script parses this data, determines the type of transaction (Swap, Transfer, etc.), fetches additional token data (like Market Cap), and then formats and sends a POST request to your designated Discord Webhook URL.
