#!/usr/bin/env python3
"""
Execute a token swap on Base using 0x Protocol quote + Privy wallet signing.

Usage: python3 execute_swap.py <wallet_id> <wallet_address> <sell_token> <buy_token> <sell_amount> [slippage_bps]
Example: python3 execute_swap.py wallet_abc 0x3a7F... USDC ETH 100 50
"""
import os
import sys
import json
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

PRIVY_APP_ID    = os.environ.get("PRIVY_APP_ID")
PRIVY_APP_SECRET = os.environ.get("PRIVY_APP_SECRET")
ZERO_X_API_KEY  = os.environ.get("ZERO_X_API_KEY")

if not all([PRIVY_APP_ID, PRIVY_APP_SECRET, ZERO_X_API_KEY]):
    print("ERROR: Missing PRIVY_APP_ID, PRIVY_APP_SECRET, or ZERO_X_API_KEY in .env", file=sys.stderr)
    sys.exit(1)

if len(sys.argv) < 6:
    print("Usage: python3 execute_swap.py <wallet_id> <wallet_address> <sell_token> <buy_token> <sell_amount> [slippage_bps]", file=sys.stderr)
    sys.exit(1)

wallet_id      = sys.argv[1]
wallet_address = sys.argv[2]
sell_token     = sys.argv[3].upper()
buy_token      = sys.argv[4].upper()
sell_amount    = float(sys.argv[5])
slippage_bps   = int(sys.argv[6]) if len(sys.argv) > 6 else 50

TOKEN_ADDRESSES = {
    "ETH":   "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
    "WETH":  "0x4200000000000000000000000000000000000006",
    "USDC":  "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "USDT":  "0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2",
    "DAI":   "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
    "CBETH": "0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22",
}
TOKEN_DECIMALS = {"ETH": 18, "WETH": 18, "USDC": 6, "USDT": 6, "DAI": 18, "CBETH": 18}

privy_creds = base64.b64encode(f"{PRIVY_APP_ID}:{PRIVY_APP_SECRET}".encode()).decode()
privy_headers = {
    "Authorization": f"Basic {privy_creds}",
    "privy-app-id": PRIVY_APP_ID,
    "Content-Type": "application/json",
}
zerox_headers = {"0x-api-key": ZERO_X_API_KEY, "0x-version": "v2"}

sell_decimals  = TOKEN_DECIMALS.get(sell_token, 18)
sell_amount_wei = int(sell_amount * (10 ** sell_decimals))

# Step 1: Get firm quote
quote_resp = requests.get(
    "https://api.0x.org/swap/permit2/quote",
    headers=zerox_headers,
    params={
        "chainId":    "8453",
        "sellToken":  TOKEN_ADDRESSES[sell_token],
        "buyToken":   TOKEN_ADDRESSES[buy_token],
        "sellAmount": str(sell_amount_wei),
        "taker":      wallet_address,
        "slippageBps": str(slippage_bps),
    },
    timeout=15,
)

if quote_resp.status_code != 200:
    print(f"ERROR: Quote failed: {quote_resp.text}", file=sys.stderr)
    sys.exit(1)

quote = quote_resp.json()

# Step 2: Sign permit2 if required
permit2 = quote.get("permit2")
if permit2 and permit2.get("eip712"):
    sign_resp = requests.post(
        f"https://api.privy.io/v1/wallets/{wallet_id}/rpc",
        headers=privy_headers,
        json={
            "method": "eth_signTypedData_v4",
            "caip2": "eip155:8453",
            "params": {"typed_data": permit2["eip712"]},
        },
        timeout=30,
    )
    if sign_resp.status_code != 200:
        print(f"ERROR: Signing failed: {sign_resp.text}", file=sys.stderr)
        sys.exit(1)

# Step 3: Submit transaction
tx = quote["transaction"]
send_resp = requests.post(
    f"https://api.privy.io/v1/wallets/{wallet_id}/rpc",
    headers=privy_headers,
    json={
        "method": "eth_sendTransaction",
        "caip2": "eip155:8453",
        "params": {
            "transaction": {
                "to":       tx["to"],
                "data":     tx["data"],
                "value":    hex(int(tx.get("value", 0))),
                "gasLimit": hex(int(tx.get("gas", 200000))),
            }
        },
    },
    timeout=60,
)

if send_resp.status_code != 200:
    print(f"ERROR: Transaction failed: {send_resp.text}", file=sys.stderr)
    sys.exit(1)

tx_hash     = send_resp.json().get("data", {}).get("hash", "")
buy_decimals = TOKEN_DECIMALS.get(buy_token, 18)
buy_amount   = int(quote.get("buyAmount", 0)) / (10 ** buy_decimals)

print(json.dumps({
    "status":   "submitted",
    "tx_hash":  tx_hash,
    "sell":     {"token": sell_token, "amount": sell_amount},
    "buy":      {"token": buy_token,  "amount": round(buy_amount, 8)},
    "explorer": f"https://basescan.org/tx/{tx_hash}",
}))
