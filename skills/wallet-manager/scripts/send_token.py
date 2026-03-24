#!/usr/bin/env python3
"""
Send ETH or ERC20 tokens from wallet to another address on Base.

Usage: python3 send_token.py <wallet_id> <to_address> <token> <amount>
Example: python3 send_token.py wallet_abc123 0xRecipient... USDC 50
"""
import os
import sys
import json
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

PRIVY_APP_ID = os.environ.get("PRIVY_APP_ID")
PRIVY_APP_SECRET = os.environ.get("PRIVY_APP_SECRET")
BASE_RPC = os.environ.get("BASE_RPC_URL", "https://mainnet.base.org")

if not PRIVY_APP_ID or not PRIVY_APP_SECRET:
    print("ERROR: PRIVY_APP_ID and PRIVY_APP_SECRET must be set in .env", file=sys.stderr)
    sys.exit(1)

if len(sys.argv) < 5:
    print("Usage: python3 send_token.py <wallet_id> <to_address> <token> <amount>", file=sys.stderr)
    sys.exit(1)

wallet_id   = sys.argv[1]
to_address  = sys.argv[2]
token       = sys.argv[3].upper()
amount      = float(sys.argv[4])

TOKEN_ADDRESSES = {
    "USDC":  "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "USDT":  "0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2",
    "DAI":   "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
    "WETH":  "0x4200000000000000000000000000000000000006",
    "cbETH": "0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22",
}
TOKEN_DECIMALS = {"USDC": 6, "USDT": 6, "DAI": 18, "WETH": 18, "cbETH": 18}

privy_creds = base64.b64encode(f"{PRIVY_APP_ID}:{PRIVY_APP_SECRET}".encode()).decode()
headers = {
    "Authorization": f"Basic {privy_creds}",
    "privy-app-id": PRIVY_APP_ID,
    "Content-Type": "application/json",
}

if token == "ETH":
    value_wei = int(amount * 1e18)
    tx_params = {
        "to": to_address,
        "value": hex(value_wei),
        "data": "0x",
        "gasLimit": hex(21000),
    }
else:
    if token not in TOKEN_ADDRESSES:
        print(f"ERROR: Unsupported token '{token}'. Supported: ETH, {', '.join(TOKEN_ADDRESSES.keys())}", file=sys.stderr)
        sys.exit(1)

    decimals = TOKEN_DECIMALS.get(token, 18)
    amount_wei = int(amount * (10 ** decimals))
    to_padded = to_address[2:].lower().zfill(64)
    amount_hex = hex(amount_wei)[2:].zfill(64)
    data = "0xa9059cbb" + to_padded + amount_hex  # transfer(address,uint256)

    tx_params = {
        "to": TOKEN_ADDRESSES[token],
        "value": "0x0",
        "data": data,
        "gasLimit": hex(65000),
    }

resp = requests.post(
    f"https://api.privy.io/v1/wallets/{wallet_id}/rpc",
    headers=headers,
    json={
        "method": "eth_sendTransaction",
        "caip2": "eip155:8453",
        "params": {"transaction": tx_params},
    },
    timeout=30,
)

if resp.status_code != 200:
    print(f"ERROR: {resp.status_code} — {resp.text}", file=sys.stderr)
    sys.exit(1)

tx_hash = resp.json().get("data", {}).get("hash", "")
print(json.dumps({
    "status": "submitted",
    "tx_hash": tx_hash,
    "token": token,
    "amount": amount,
    "to": to_address,
    "explorer": f"https://basescan.org/tx/{tx_hash}",
}))
