import requests
import time
import pandas as pd

def get_api_key(scan):
    with open(f"{scan}_api.txt", "r") as api_file:
        return api_file.read().strip()

def get_owned_token_ids(wallet_address, contract_address, scan):
    api_key = get_api_key(scan)
    base_urls = {
        "bsc": "https://api.bscscan.com/api?module=account&action=tokennfttx&contractaddress={contract_address}&address={wallet_address}&page=1&offset=20&sort=desc&apikey={api_key}",
        "poly": "https://api.polygonscan.com/api?module=account&action=tokennfttx&contractaddress={contract_address}&address={wallet_address}&page=1&offset=20&sort=desc&apikey={api_key}",
        "eth": "https://api.etherscan.com/api?module=account&action=tokennfttx&contractaddress={contract_address}&address={wallet_address}&tag=latest&apikey={api_key}"
    }
    url = base_urls[scan].format(contract_address=contract_address, wallet_address=wallet_address, api_key=api_key)
    
    response = requests.get(url)
    data = response.json()
    
    if "result" in data:
        # Ethereum response
        if isinstance(data["result"], list):
            token_transactions = data["result"]
            token_ids = [tx.get("tokenID") for tx in token_transactions]
            return token_ids
    return []

# Reads the wallet addresses from wallets.txt
wallet_addresses = []
with open("wallets.txt", "r") as file:
    wallet_addresses = [line.strip() for line in file]

contract_address = ""  # Insert contract address of NFT collection or Token you want to check ownership

scan = "eth"  # "poly" "eth" "bsc" Choose the scan

results = []

for wallet_address in wallet_addresses:
    owned_token_ids = get_owned_token_ids(wallet_address, contract_address, scan)
    
    if owned_token_ids:
        print(f"{wallet_address} owns tokens with the following IDs on {scan.capitalize()}: {', '.join(map(str, owned_token_ids))}")
        results.append([wallet_address, ', '.join(map(str, owned_token_ids))])
    else:
        print(f"{wallet_address} does not own tokens from the specified contract on {scan.capitalize()}.")
        results.append([wallet_address, "No tokens"])

    time.sleep(5)  # 5 second time out, that's the default rate limit for the Free plan for these scanners' APIs.

# Creates EXCEL
df = pd.DataFrame(results, columns=["Wallet Address", f"Owned Token IDs on {scan.capitalize()}"])

# Save excel with respective name of your chosen scan "bsc.xlsx" "eth.xlsx" "poly.xlsx"
df.to_excel(f"Token_Ownership_{scan.capitalize()}.xlsx", index=False)
