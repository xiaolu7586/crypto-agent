---
name: wallet-manager
description: Manage your crypto wallet on Base network — check balance, send tokens, and get your deposit address
version: 1.0.0
---

## What this skill does
- **First-time setup**: automatically creates your wallet on first use
- **Balance check**: view ETH and token balances in real time
- **Deposit**: get your wallet address to receive crypto
- **Send**: transfer ETH or tokens to any Base address

## Trigger conditions
Use this skill when the user:
- Asks about their wallet, balance, or address
- Wants to send or receive crypto
- Is using the agent for the first time (auto-trigger wallet creation)
- Asks how to fund their wallet

## Workflow

### Step 1 — Check if wallet exists
Read USER.md. If `Base address: (not set)`, run wallet creation first.

### Step 2 — Create wallet (first time only)
```bash
python3 skills/wallet-manager/scripts/create_wallet.py
```
Save the returned `wallet_id` and `address` to USER.md immediately.

### Step 3 — Check balance
```bash
python3 skills/wallet-manager/scripts/get_balance.py <address>
```

### Step 4 — Send tokens (requires explicit confirmation)
Show transfer preview first. Wait for user confirmation, then:
```bash
python3 skills/wallet-manager/scripts/send_token.py <wallet_id> <to_address> <token> <amount>
```

## Output format

### Wallet created
```
✅ Your wallet is ready

  Address:  0x3a7F...c4B9
  Network:  Base (Ethereum L2)
  Balance:  0 ETH

⚠️  Use this address for Base network only.
    Do not send assets from other networks without bridging first.

💡 To fund your wallet, send ETH or USDC to the address above.
```

### Balance display
```
💼 Your Wallet — Base Network

  ETH:    0.0450  ($84.20)
  USDC:   120.00

  Address: 0x3a7F...c4B9
```

### Send confirmation
```
📤 Send Preview

  Token:    50 USDC
  To:       0xRecipient...
  Network:  Base
  Gas fee:  ~$0.02

⚠️  This cannot be undone. Reply "confirm" to send.
```

### Send success
```
✅ Sent

  50 USDC → 0xRecipient...
  Transaction: https://basescan.org/tx/0xabc...
```

## Notes
- Wallet is created once and persists in USER.md
- Network: Base mainnet only (Chain ID: 8453)
- Supported tokens: ETH, USDC, USDT, DAI, WETH, cbETH
