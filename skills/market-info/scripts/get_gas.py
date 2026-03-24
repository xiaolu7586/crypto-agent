#!/usr/bin/env python3
"""
Get current gas price on Base network with estimated transaction costs.

Usage: python3 get_gas.py
"""
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_RPC = os.environ.get("BASE_RPC_URL", "https://mainnet.base.org")

def rpc(method, params=None):
    resp = requests.post(
        BASE_RPC,
        json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params or []},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["result"]

gas_hex  = rpc("eth_gasPrice")
gas_wei  = int(gas_hex, 16)
gas_gwei = gas_wei / 1e9

try:
    price_resp = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids": "ethereum", "vs_currencies": "usd"},
        timeout=10,
    )
    eth_usd = price_resp.json().get("ethereum", {}).get("usd", 0)
except Exception:
    eth_usd = 0

TRANSFER_GAS = 21_000
SWAP_GAS     = 150_000
ERC20_GAS    = 65_000

def cost_usd(gas_limit):
    return round((gas_wei * gas_limit / 1e18) * eth_usd, 5)

print(json.dumps({
    "network":       "Base",
    "gas_price_gwei": round(gas_gwei, 4),
    "eth_price_usd": eth_usd,
    "estimated_costs": {
        "eth_transfer":   f"~${cost_usd(TRANSFER_GAS):.4f}",
        "erc20_transfer": f"~${cost_usd(ERC20_GAS):.4f}",
        "token_swap":     f"~${cost_usd(SWAP_GAS):.4f}",
    },
}))
