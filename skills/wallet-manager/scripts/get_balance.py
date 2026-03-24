#!/usr/bin/env python3
"""
Get wallet balance (ETH + common ERC20 tokens) on Base network.

Usage: python3 get_balance.py <wallet_address>
"""
import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_RPC = os.environ.get("BASE_RPC_URL", "https://mainnet.base.org")

TOKENS = {
    "USDC":  "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "USDT":  "0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2",
    "DAI":   "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
    "WETH":  "0x4200000000000000000000000000000000000006",
    "cbETH": "0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22",
}

TOKEN_DECIMALS = {
    "USDC": 6, "USDT": 6, "DAI": 18, "WETH": 18, "cbETH": 18,
}

ERC20_BALANCE_OF = "0x70a08231"  # balanceOf(address) selector

def rpc(method, params):
    resp = requests.post(
        BASE_RPC,
        json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params},
        timeout=15,
    )
    resp.raise_for_status()
    result = resp.json()
    if "error" in result:
        raise ValueError(result["error"])
    return result["result"]

if len(sys.argv) < 2:
    print("Usage: python3 get_balance.py <wallet_address>", file=sys.stderr)
    sys.exit(1)

address = sys.argv[1].lower()
padded = address[2:].zfill(64) if address.startswith("0x") else address.zfill(64)

# ETH balance
eth_hex = rpc("eth_getBalance", [address, "latest"])
eth_balance = int(eth_hex, 16) / 1e18

balances = {"ETH": round(eth_balance, 6)}

# ERC20 balances
for symbol, contract in TOKENS.items():
    try:
        data = ERC20_BALANCE_OF + padded
        result = rpc("eth_call", [{"to": contract, "data": data}, "latest"])
        raw = int(result, 16)
        decimals = TOKEN_DECIMALS.get(symbol, 18)
        bal = raw / (10 ** decimals)
        if bal > 0:
            balances[symbol] = round(bal, 6)
    except Exception:
        continue

# Get ETH price for USD conversion
try:
    price_resp = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids": "ethereum", "vs_currencies": "usd"},
        timeout=10,
    )
    eth_usd = price_resp.json().get("ethereum", {}).get("usd", 0)
except Exception:
    eth_usd = 0

print(json.dumps({
    "address": address,
    "network": "Base",
    "balances": balances,
    "eth_price_usd": eth_usd,
}))
