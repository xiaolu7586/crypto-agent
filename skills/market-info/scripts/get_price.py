#!/usr/bin/env python3
"""
Get real-time token prices from CoinGecko.

Usage: python3 get_price.py <TOKEN> [TOKEN2 ...]
Example: python3 get_price.py ETH BTC SOL
"""
import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("COINGECKO_API_KEY", "")

SYMBOL_TO_ID = {
    "BTC":   "bitcoin",
    "ETH":   "ethereum",
    "SOL":   "solana",
    "BNB":   "binancecoin",
    "USDC":  "usd-coin",
    "USDT":  "tether",
    "DAI":   "dai",
    "MATIC": "matic-network",
    "ARB":   "arbitrum",
    "OP":    "optimism",
    "LINK":  "chainlink",
    "UNI":   "uniswap",
    "AAVE":  "aave",
    "MKR":   "maker",
    "WBTC":  "wrapped-bitcoin",
    "CBETH": "coinbase-wrapped-staked-eth",
    "WETH":  "weth",
}

if len(sys.argv) < 2:
    print("Usage: python3 get_price.py <TOKEN> [TOKEN2 ...]", file=sys.stderr)
    sys.exit(1)

symbols = [s.upper() for s in sys.argv[1:]]
coin_ids, symbol_map = [], {}

for sym in symbols:
    cid = SYMBOL_TO_ID.get(sym)
    if cid:
        coin_ids.append(cid)
        symbol_map[cid] = sym
    else:
        print(f"WARNING: Unknown symbol '{sym}' — skipping", file=sys.stderr)

if not coin_ids:
    print("ERROR: No valid token symbols provided", file=sys.stderr)
    sys.exit(1)

base_url = "https://pro-api.coingecko.com/api/v3" if API_KEY else "https://api.coingecko.com/api/v3"
headers  = {"x-cg-pro-api-key": API_KEY} if API_KEY else {}

resp = requests.get(
    f"{base_url}/coins/markets",
    headers=headers,
    params={
        "vs_currency": "usd",
        "ids": ",".join(coin_ids),
        "order": "market_cap_desc",
        "per_page": 50,
        "price_change_percentage": "1h,24h,7d",
    },
    timeout=15,
)

if resp.status_code != 200:
    print(f"ERROR: CoinGecko API {resp.status_code} — {resp.text}", file=sys.stderr)
    sys.exit(1)

results = {}
for coin in resp.json():
    sym = symbol_map.get(coin["id"], coin["symbol"].upper())
    results[sym] = {
        "price_usd":   coin["current_price"],
        "change_1h":   round(coin.get("price_change_percentage_1h_in_currency")  or 0, 2),
        "change_24h":  round(coin.get("price_change_percentage_24h_in_currency") or 0, 2),
        "change_7d":   round(coin.get("price_change_percentage_7d_in_currency")  or 0, 2),
        "market_cap":  coin.get("market_cap"),
        "volume_24h":  coin.get("total_volume"),
    }

print(json.dumps(results))
