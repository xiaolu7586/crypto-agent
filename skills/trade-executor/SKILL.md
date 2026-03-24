---
name: trade-executor
description: Swap tokens on Base network — get quotes and execute trades via 0x Protocol with mandatory confirmation step
version: 1.0.0
---

## What this skill does
Executes token swaps on Base network using 0x Protocol, which routes across all Base DEXes for best price.

**Always two steps: quote first → user confirms → then execute.**

## Trigger conditions
Use this skill when the user:
- Wants to swap, trade, buy, or sell tokens
- Says "swap X for Y", "buy ETH with USDC", "sell my USDC"
- Asks for a price quote before trading

## Workflow

### Step 1 — Get quote
```bash
python3 skills/trade-executor/scripts/get_quote.py <sell_token> <buy_token> <sell_amount>
```
Example:
```bash
python3 skills/trade-executor/scripts/get_quote.py USDC ETH 100
```

### Step 2 — Show confirmation (MANDATORY — never skip)
Display the full swap preview. Wait for explicit "confirm", "yes", or "ok".
If user is unclear or asks questions, answer first — do not execute.

### Step 3 — Execute swap (only after confirmation)
```bash
python3 skills/trade-executor/scripts/execute_swap.py <wallet_id> <address> <sell_token> <buy_token> <sell_amount>
```
Get `wallet_id` and `address` from USER.md.

## Output format

### Swap preview (step 2)
```
📊 Swap Preview

  You pay:      100.00 USDC
  You receive:  ~0.0267 ETH
  Rate:         1 ETH = $3,745
  Price impact: 0.02%
  Gas fee:      ~$0.04
  Route:        Uniswap V3

⚠️  Rates update every 30 seconds. This action cannot be undone.
    Reply "confirm" to execute, or "cancel" to abort.
```

### Swap executed (step 3)
```
✅ Swap Complete

  Sold:     100.00 USDC
  Received: ~0.0267 ETH

  Transaction: https://basescan.org/tx/0xabc...def
```

### Swap failed
```
❌ Swap Failed

  Reason: [error description]

  Your funds are safe — no tokens were moved.
  You can try again or adjust the amount.
```

## Safety rules
See references/swap_safety.md for full guidelines.
- Default slippage: 0.5% (50 bps)
- Warn if price impact > 2%
- Warn if gas fee > 5% of swap value
- Never auto-execute — always require explicit confirmation

## Supported tokens
ETH · WETH · USDC · USDT · DAI · cbETH
