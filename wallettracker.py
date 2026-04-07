import os
import requests
from flask import Flask, jsonify
from flask import request
from dotenv import load_dotenv

load_dotenv()

lista = []
app = Flask(__name__)

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

#Simple function to shorten numbers
def shorten_number(num):
    # Define suffixes for thousands, millions, and billions
    suffixes = ['', 'k', 'M', 'B']

    # Determine the appropriate suffix and divide the number
    suffix_index = 0
    while abs(num) >= 1000 and suffix_index < len(suffixes) - 1:
        num /= 1000.0
        suffix_index += 1

    # Format the number with the suffix
    formatted_num = f'{num:.1f}{suffixes[suffix_index]}'

    return formatted_num

#Function to obtain a token's Market Cap using DexScreener API
def get_marketcap(CA):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{CA}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'pairs' in data and data['pairs']:
            fdv = data['pairs'][0].get('fdv')
            if fdv is not None:
                return shorten_number(fdv)
            else:
                print("Error: 'fdv' key not found in data")
                return 0
        else:
            print("Error: No 'pairs' key found in data")
            return 0
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return 0

#Function to obtain a token's Market Cap using PumpFun API
def get_marketcapPF(CA):
    url = f"https://frontend-api.pump.fun/coins/{CA}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return shorten_number(data["usd_market_cap"])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return 0

@app.route('/webh', methods=['GET', 'POST'])
def webh():

    if request.method == 'POST':
        data = request.json
        lista.append(data)

        if (data[0]['type'] == 'SWAP'):

            desc = data[0]['description'] #Grab the description of the transaction
            tokenCA = data[0]['tokenTransfers'][1]['mint'] #Grab tokenCA from the mint value of token transfers
            wallet = data[0]['feePayer'] #Wallet doing the transaction is the fee payer

            desc_parts = desc.split(' ') #Split description in a vector using the space as separator
            buy_sale_identifier = desc_parts[-1] #Obtain the last word of the desc to check if sale or buy
            wallet_part = desc_parts[0]  #Wallet address is the first postion of the vector created
            desc_parts[0] = f'[({wallet_part[:4]}...{wallet_part[-4:]})](https://solscan.io/account/{wallet})' #Create a string that only shows first and last 4 characters of the wallet and is also a link to solscan

            #Updated description string
            short_desc = ' '.join(desc_parts)

            #If tokenCA is SOL CA, its a sale else a buy
            if buy_sale_identifier == 'SOL':
                transaction_type = 'Sale'
            else:
                transaction_type = 'Buy'


            if transaction_type == 'Buy':
                print(round(data[0]['tokenTransfers'][0]['tokenAmount'], 3))
                MC = get_marketcap(tokenCA)
                if MC != 0:
                    message = {
                        "content": None,
                        "embeds": [
                            {
                            "description": f"🟢 ** BUY**\n{short_desc}\n```{tokenCA}```\n**Market Cap: **{MC} \n**Links:** [Photon](https://photon-sol.tinyastro.io/en/lp/{tokenCA}) | [Trojan](https://t.me/diomedes_trojanbot?start=r-unauth0rized403-{tokenCA}) | [Axiom](https://axiom.trade/t/{tokenCA}/@elonmusk?chain=sol) | [DexScreener](https://dexscreener.com/solana/{tokenCA})",
                            "color": 5697089
                            }
                            ],
                         "username": "Wallet Tracker",
                         "avatar_url": "https://i.imgur.com/WjWkIHW.png",
                         "attachments": []}
                    requests.post(WEBHOOK_URL, json=message)


            else:
                tokenCA = data[0]['tokenTransfers'][0]['mint']
                MC = get_marketcap(tokenCA)
                if MC != 0:
                    message = {
                        "content": None,
                        "embeds": [
                            {
                            "description": f"🔴 ** SALE**\n{short_desc}\n```{tokenCA}```\n**Market Cap: **{MC}\n**Links:** [Photon](https://photon-sol.tinyastro.io/en/lp/{tokenCA}) | [Trojan](https://t.me/diomedes_trojanbot?start=r-unauth0rized403-{tokenCA}) | [Axiom](https://axiom.trade/t/{tokenCA}/@elonmusk?chain=sol) | [DexScreener](https://dexscreener.com/solana/{tokenCA})",
                            "color": 16066086
                            }
                            ],
                         "username": "Wallet Tracker",
                         "avatar_url": "https://i.imgur.com/WjWkIHW.png",
                         "attachments": []}
                    requests.post(WEBHOOK_URL, json=message)


        elif (data[0]['type'] == 'TRANSFER'):

            pumpfunCA = '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P'

            try:
                checkPF = data[0]['instructions'][3]['accounts'][-1] #Pumpfun Web
            except:
                checkPF = None

            if not checkPF or checkPF != pumpfunCA:
                try:
                    checkPF = data[0]['instructions'][2]['programId'] #BullX
                except:
                    checkPF = None
            if (checkPF == pumpfunCA):
                if 'tokenTransfers' in data[0] and data[0]['tokenTransfers']:
                    if data[0]['tokenTransfers'][0].get('mint'):
                        tokenCA = data[0]['tokenTransfers'][0]['mint']

                        tokenQuantity = round(data[0]['tokenTransfers'][0]['tokenAmount'], 3)
                        wallet = data[0]['feePayer']
                        wallet_short = f'[({wallet[:4]}...{wallet[-4:]})](https://solscan.io/account/{wallet})' #Create a string that only shows first and last 4 characters of the wallet and is also a link to solscan

                        desc = data[0]['description']
                        words = desc.split()  # Dividir la cadena en palabras usando espacios como delimitador
                        buy_sale_identifier = words[0]
                        tokenName = words[3]
                        MC = get_marketcapPF(tokenCA)

                        if (buy_sale_identifier != wallet):
                            solanaQuantity = round(abs(data[0]["accountData"][0]["nativeBalanceChange"])/1000000000, 3)

                            message = {
                            "content": None,
                            "embeds": [
                                {
                                "description": f"💊🟢 ** BUY ON PUMP.FUN **\n{wallet_short} swapped {solanaQuantity} SOL for {tokenQuantity} {tokenName} on Pump.fun\n```{tokenCA}```\n**Market Cap: **{MC} \n**Links:** [Photon](https://photon-sol.tinyastro.io/en/lp/{tokenCA}) | [Trojan](https://t.me/diomedes_trojanbot?start={tokenCA}) | [Axiom](https://axiom.trade/t/{tokenCA}/@elonmusk?chain=sol) | [Pump.Fun](https://www.pump.fun/{tokenCA})",
                                "color": 5697089
                                }
                                ],
                             "username": "Wallet Tracker",
                             "avatar_url": "https://i.imgur.com/WjWkIHW.png",
                             "attachments": []}
                            requests.post(WEBHOOK_URL, json=message)
                        else:
                            solanaQuantity = round(abs(data[0]["accountData"][0]["nativeBalanceChange"])/1000000000, 3)

                            message = {
                            "content": None,
                            "embeds": [
                                {
                                "description": f"💊🔴 ** SALE ON PUMP.FUN **\n{wallet_short} swapped {tokenQuantity} {tokenName} for {solanaQuantity} SOL on Pump.fun\n```{tokenCA}```\n**Market Cap: **{MC} \n**Links:** [Photon](https://photon-sol.tinyastro.io/en/lp/{tokenCA}) | [Trojan](https://t.me/diomedes_trojanbot?start={tokenCA}) | [Axiom](https://axiom.trade/t/{tokenCA}/@elonmusk?chain=sol) | [Pump.Fun](https://www.pump.fun/{tokenCA})",
                                "color": 16066086
                                }
                                ],
                             "username": "Wallet Tracker",
                             "avatar_url": "https://i.imgur.com/WjWkIHW.png",
                             "attachments": []}
                            requests.post(WEBHOOK_URL, json=message)

        elif (data[0]['type'] == 'UNKNOWN'):
            tokenCA = data[0]['tokenTransfers'][0]['mint']


            tokenQuantity = round(data[0]['tokenTransfers'][0]['tokenAmount'], 3)
            wallet = data[0]['feePayer']
            wallet_short = f'[({wallet[:4]}...{wallet[-4:]})](https://solscan.io/account/{wallet})' #Create a string that only shows first and last 4 characters of the wallet and is also a link to solscan
            solanaQuantity = abs(data[0]["accountData"][0]["nativeBalanceChange"])/1000000000

            message = {
            "content": None,
            "embeds": [
                  {
                        "description": f"💊🟢 ** BUY ON PUMP.FUN (photon)**\n{wallet_short} swapped {solanaQuantity} SOL for {tokenQuantity} tokens on Pump.fun\n```{tokenCA}```\n**Market Cap: **{MC} \n**Links:** [Photon](https://photon-sol.tinyastro.io/en/lp/{tokenCA}) | [Trojan](https://t.me/diomedes_trojanbot?start={tokenCA}) | [Axiom](https://axiom.trade/t/{tokenCA}/@elonmusk?chain=sol) | [Pump.Fun](https://www.pump.fun/{tokenCA})",
                        "color": 5697089
                        }
                        ],
            "username": "Wallet Tracker",
            "avatar_url": "https://i.imgur.com/WjWkIHW.png",
            "attachments": []}
            requests.post(WEBHOOK_URL, json=message)


        return jsonify({'message': 'POST request received successfully'})
    else:
        #If the request is a GET, return the requests stored in lista
        return jsonify({'message': lista})