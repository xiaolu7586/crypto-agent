---
name: market-info
description: Real-time crypto prices, 24h change, market cap, and Base network gas fees
version: 1.0.0
---

## What this skill does
- **Token prices**: real-time price, 1h/24h/7d change, market cap, volume
- **Gas fees**: current Base network gas price and estimated transaction costs
- **Multi-token**: look up multiple tokens in one request

## Trigger conditions
Use this skill when the user:
- Asks about the price of any token (ETH, BTC, SOL, USDC, etc.)
- Wants to know market trends or price changes
- Asks about gas fees or transaction costs
- Says "how much is...", "what's the price of...", "check gas"

## Workflow

### Get token price
```bash
python3 skills/market-info/scripts/get_price.py ETH
python3 skills/market-info/scripts/get_price.py ETH BTC SOL
```

### Get gas fees
```bash
python3 skills/market-info/scripts/get_gas.py
```

## Output format

### Price display
```
📊 Market Prices

  ETH    $3,745.20   ▲ +2.4% (24h)   ▲ +0.3% (1h)
  BTC   $97,420.00   ▼ -0.8% (24h)   — +0.0% (1h)
  SOL      $185.40   ▲ +5.1% (24h)   ▲ +1.2% (1h)

  Updated: just now
```

### Gas display
```
⛽ Base Network Gas

  Gas price:          0.0012 Gwei
  Token transfer:     ~$0.001
  Token swap:         ~$0.008
```

## Supported tokens
BTC · ETH · SOL · BNB · USDC · USDT · DAI · MATIC · ARB · OP · LINK · UNI · AAVE · MKR · WBTC · cbETH
