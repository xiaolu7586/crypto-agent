#!/usr/bin/env python3
"""
Get a swap quote from 0x Protocol on Base network.

Usage: python3 get_quote.py <sell_token> <buy_token> <sell_amount>
Example: python3 get_quote.py USDC ETH 100
"""
import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("ZERO_X_API_KEY")
if not API_KEY:
    print("ERROR: ZERO_X_API_KEY not set in .env", file=sys.stderr)
    sys.exit(1)

TOKEN_ADDRESSES = {
    "ETH":   "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
    "WETH":  "0x4200000000000000000000000000000000000006",
    "USDC":  "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "USDT":  "0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2",
    "DAI":   "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
    "CBETH": "0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22",
}

TOKEN_DECIMALS = {
    "ETH": 18, "WETH": 18, "USDC": 6, "USDT": 6, "DAI": 18, "CBETH": 18,
}

if len(sys.argv) < 4:
    print("Usage: python3 get_quote.py <sell_token> <buy_token> <sell_amount>", file=sys.stderr)
    sys.exit(1)

sell_token   = sys.argv[1].upper()
buy_token    = sys.argv[2].upper()
sell_amount  = float(sys.argv[3])

for tok in (sell_token, buy_token):
    if tok not in TOKEN_ADDRESSES:
        print(f"ERROR: Unsupported token '{tok}'. Supported: {', '.join(TOKEN_ADDRESSES)}", file=sys.stderr)
        sys.exit(1)

sell_decimals = TOKEN_DECIMALS.get(sell_token, 18)
sell_amount_wei = int(sell_amount * (10 ** sell_decimals))

headers = {"0x-api-key": API_KEY, "0x-version": "v2"}

resp = requests.get(
    "https://api.0x.org/swap/permit2/price",
    headers=headers,
    params={
        "chainId":   "8453",
        "sellToken": TOKEN_ADDRESSES[sell_token],
        "buyToken":  TOKEN_ADDRESSES[buy_token],
        "sellAmount": str(sell_amount_wei),
    },
    timeout=15,
)

if resp.status_code != 200:
    print(f"ERROR: 0x API {resp.status_code} — {resp.text}", file=sys.stderr)
    sys.exit(1)

data = resp.json()
buy_decimals   = TOKEN_DECIMALS.get(buy_token, 18)
buy_amount     = int(data.get("buyAmount", 0)) / (10 ** buy_decimals)
price_impact   = data.get("estimatedPriceImpact", "0")
sources        = [s["name"] for s in data.get("sources", []) if float(s.get("proportion", 0)) > 0]

print(json.dumps({
    "sell":         {"token": sell_token, "amount": sell_amount},
    "buy":          {"token": buy_token,  "amount": round(buy_amount, 8)},
    "rate":         f"1 {sell_token} = {round(buy_amount / sell_amount, 6)} {buy_token}",
    "price_impact": price_impact,
    "gas_estimate": data.get("gas", 0),
    "sources":      sources,
}))
