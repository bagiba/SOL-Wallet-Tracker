import requests
from flask import Flask, jsonify
from flask import request

lista = []
app = Flask(__name__)

wallet_owners = {
    'CCrWZFb6shfU9bQz8pZ61VwRn9wccCViNajq67vUkaMP': 'shadow4',
    'G4rUK4eyvsU3ay1QafN6VZsrwmgmrBhgDR91N1YjG1eQ': 'shadow3',
    '2HWT2KLLdN2wxYTqdSuko5SBzg2SEJASgV4GE2tD7TML': 'catolic',
    'DwKdQS91C9r3ue2viJsYtcFmTGDjzV91zzQqNVgDrEvb': 'unrevel',
    'B9ZyBmeXuGp2H5o6qUyYGpkVaco7s37Rd1mxA8vVeycV': 'sol7 3',
    '9HJTeX467VZNKn5nv8VjXAxtwnbKmi8LfjUSieVDbNxt': 'roxo',
    '2xPraXZPQ3GirTcJsybKqmEZeAqdD6kLr3gw64FxgRZt': 'yog-ray',
    '6Y1wJPh5XFUoT15KpJ16kjHvQ1VJ6sK2Y3zMBmsoPQZB': 'feed-bot',
    'AbA3qBmz317YdqoqQgUYRdoHN6qvxL4ksGNyEhTmjxcz': 'shadow5',
    '8ei7KS5tdHc8uoYtk4pCyJ17RYsr5ZXK9nnQVeRpDbks': 'dam1ah',
    '8h2YPugtbBj4UH8Kw1bn5WfEfkhCfmEcgSNn6iz4JB46': 'oversol',
    '62Ne7d7yH1cHJ7Q76BrCe7zTj6QZz8VZCBWiKwqURJTe': 'cipher',
    '62femS3raYXBmq2qQPw8SQ36FyrsMmu6GWcnUx1wcBX': 'reed-commie',
    '2mjdduwGWqVSuPhHaLruQnjeEKACDxoE7fYm5Jq1ycJL': 'feed1',
    '5J2tN3rnrh79k17qmvzQJrMPBzb6uAuG1f9gJD8qt5Tq': 'loli2',
    'CqsdTGRW5BcuM4h6tES38c6qVctHTGNuoWDndnLZ4J5D': 'loli3',
    '3ZKc3pVLEG4sNQBxd8Nt4Ssa8EjFNNTpioPmfJmVSGgy': 'shadow2',
    'ATTosnuUE7FHpr37uCPZVnFvfW1kRoayhtr3uy4bYJNU': 'shadow',
    'EzxYyXGBj6Z12bqBLSM3YkknZ2WmR2BVRBBe88WjBYL2': 'awp1',
    'AWNtFkwDDPg5XaAi5PFb4U4KjZxHTJBT987JmqdTyJ7D': 'ram1',
    '4TdH5Re1U623TX7RWuqcvrU1xLygo2Mi4qPfSV5yvSDb': 'ram2',
    'BeRrqafrVPJP53dqTA4ozmD9L7wJFBSYA8zBmPLrjR3X': 'ram3',
    '571zfemzBm9psKaDxZN5ufEZtYNxK5omVmVCmuHe2isa': 'ram4',
    '9nrRN7pBM3Fdtm3wEHaTbf9adhMyBhPEAQHXBRdDzVxa': 'ram-challenge',
    '4oJEYjoJcrRKo3z4G8uj9EMoWyivcqdWmGFBun57RHk4': 'loli4',
    '6P7oK8vL742GH6v4PFzCYVXCGKYhvZQULXy293gPd6JU': 'SUSSY',
    'GaXcwvwKP3CnVXLU5eGqr3V96FrzWThm96uJVTJfAQiT': 'sober-pump',
    'F4TT3XTfw3JPX2poy4ndfDcJp7rAFk9ho2Dux6fQgeRQ': 'sober-main',
    '4dgTz5PH6LnWDzKGqYbh4wq4ngw6idBfobc3oAhwW15m': 'sober-alt',
    'Eiek9LhnodFo5B52uWSdip2RW7PdRmLyMf3B375FTRv2': 'sober-alt2',
    '5c9AXCPXKgdH5SBdXa5qnqSc53etZgc7mFiXkaWrsD9': 'sober-alt3',
    'CxjVWRsuhufyR2Y1K9vassq6RKxKLQbnVTX9S9KCxDKg': 'sober-alt4',
    '3MUXjjNgfUDsiEyGTKKiMMYRZhYT2coSgw8WXT6RwJft': 'dam1ah-2',
    '4Be9CvxqHW6BYiRAxW9Q3xu1ycTMWaL5z8NX4HR3ha7t': 'drawline',
    '2mC9EDWDuMn9PoXXnSmwMbHpEvowGKD9kVaBMKq2ENeQ': 'choco2',
    'HKtzTLqANw5JjCSipquBSg5j1bUBdobAYfbBJtfvjpZW': 'shadow6',
    '5LPVe89zDbhfpunvowczLzz8tucjQNNRSAnS8bP2uzSM': 'resolvent',
    '6cvJDbtNTuPXoWugwjkgG4DQFWtUppcEtN3wRxYrdi8p': 'sol7-4',
    'gW2YZ1NFgmBSAMBJ2dAQK7dMKbvFE4CojyzrDKPzXYa': 'choco3',
    '3puC5MWSCN3VerMjwiQh5E33RnTgpyVmx8w4wx46UWBY': 'choco4',
    '5LR8fjTuwUi8qGapkdtm1wZduZsC8i8MpUH6AoZVaoou': 'choco5',
    'GV7CfgWVCgCTfQmRfEg3r8D9BLZf3tgtxvN32hitQbXz': 'shadow7',
    'HAmFnVktrp7VRTh3bvkfcmxkTpH48GK3iv5VLYFpGwVv': 'michimillionaire'
}

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

def get_marketcap(CA):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{CA}"

    # Make the API request
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        fdv = data['pairs'][0]['fdv']
        return(shorten_number(fdv))
    else:
        print(f"Error: {response.status_code} - {response.text}")


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        lista.append(data)

        desc = data[0]['description']
        tokenCA = data[0]['tokenTransfers'][1]['mint']
        wallet = data[0]['feePayer']

        wallet_owner = wallet_owners.get(wallet, 'Unknown')

        desc_parts = desc.split(' ')
        wallet_part = desc_parts[0]  # Assuming wallet address is the first part of the description
        desc_parts[0] = f'[({wallet_part[:4]}...{wallet_part[-4:]})](https://solscan.io/account/{wallet})'

        # Updated description string
        short_desc = ' '.join(desc_parts)

        if tokenCA == 'So11111111111111111111111111111111111111112':
            transaction_type = 'Sale'
        else:
            transaction_type = 'Buy'


        # URL Discord Webhook
        webhook_url = 'https://discord.com/api/webhooks/'
        if transaction_type == 'Buy':
            MC = get_marketcap(tokenCA)
            message = {
        "content": None,
        "embeds": [
            {
            "description": f"🟢 ** BUY**\n**{wallet_owner}** {short_desc}\n```{tokenCA}```\n**Market Cap: **{MC} \n**Links:** [Photon](https://photon-sol.tinyastro.io/en/lp/{tokenCA}) | [Trojan](https://t.me/diomedes_trojanbot?start={tokenCA}) | [DexScreener](https://dexscreener.com/solana/{tokenCA})",
            "color": 5697089
            }
            ],
         "username": "Wallet Tracker",
         "avatar_url": "https://i.imgur.com/WjWkIHW.png",
         "attachments": []}

        else:
            tokenCA = data[0]['tokenTransfers'][0]['mint']
            MC = get_marketcap(tokenCA)
            message = {
        "content": None,
        "embeds": [
            {
            "description": f"🔴 ** SALE**\n**{wallet_owner}** {short_desc}\n```{tokenCA}```\n**Market Cap: **{MC}\n**Links:** [Photon](https://photon-sol.tinyastro.io/en/lp/{tokenCA}) | [Trojan](https://t.me/diomedes_trojanbot?start={tokenCA}) | [DexScreener](https://dexscreener.com/solana/{tokenCA})",
            "color": 16066086
            }
            ],
         "username": "Wallet Tracker",
         "avatar_url": "https://i.imgur.com/WjWkIHW.png",
         "attachments": []}

            # Enviar la solicitud POST al webhook de Discord
        response = requests.post(webhook_url, json=message)
        print(response.text)
        print(data)


        return jsonify({'message': 'POST request received successfully'})
    else:
        return jsonify({'message': lista})
