#!/usr/bin/env python3
"""
Create a new server wallet via wallet infrastructure API.
Outputs wallet_id and address as JSON.

Usage: python3 create_wallet.py
"""
import os
import sys
import json
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.environ.get("PRIVY_APP_ID")
APP_SECRET = os.environ.get("PRIVY_APP_SECRET")

if not APP_ID or not APP_SECRET:
    print("ERROR: PRIVY_APP_ID and PRIVY_APP_SECRET must be set in .env", file=sys.stderr)
    sys.exit(1)

credentials = base64.b64encode(f"{APP_ID}:{APP_SECRET}".encode()).decode()

headers = {
    "Authorization": f"Basic {credentials}",
    "privy-app-id": APP_ID,
    "Content-Type": "application/json",
}

response = requests.post(
    "https://api.privy.io/v1/wallets",
    headers=headers,
    json={"chain_type": "ethereum"},
    timeout=30,
)

if response.status_code == 200:
    data = response.json()
    print(json.dumps({
        "wallet_id": data["id"],
        "address": data["address"],
        "chain": "Base (Ethereum L2)",
        "network": "eip155:8453",
    }))
else:
    print(f"ERROR: {response.status_code} — {response.text}", file=sys.stderr)
    sys.exit(1)
