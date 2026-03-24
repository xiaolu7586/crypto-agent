# Tools & Runtime Reference

## Runtime Environment
- Platform: ClawDI / OpenClaw
- Script execution: `python3` (direct — not uv)
- Working directory: agent workspace root
- Install dependencies: `pip install -r requirements.txt -q`

## Environment Variables
Copy `.env.example` to `.env` and fill in your values.

| Variable | Required | Description |
|----------|----------|-------------|
| `PRIVY_APP_ID` | ✅ | Wallet infrastructure App ID |
| `PRIVY_APP_SECRET` | ✅ | Wallet infrastructure App Secret |
| `ZERO_X_API_KEY` | ✅ | 0x Protocol API key for swaps |
| `BASE_RPC_URL` | Optional | Base RPC endpoint (default: mainnet.base.org) |
| `COINGECKO_API_KEY` | Optional | CoinGecko Pro key (free tier works without) |

## Network
| Network | Chain ID | Explorer |
|---------|----------|---------|
| Base Mainnet | 8453 | https://basescan.org |

## Supported Tokens (Base)
| Token | Type | Contract |
|-------|------|---------|
| ETH | Native gas token | — |
| USDC | Stablecoin | 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 |
| USDT | Stablecoin | 0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2 |
| DAI | Stablecoin | 0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb |
| WETH | Wrapped ETH | 0x4200000000000000000000000000000000000006 |
| cbETH | Liquid staking | 0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22 |

## Script Reference
| Script | Arguments | Output |
|--------|-----------|--------|
| `skills/wallet-manager/scripts/create_wallet.py` | none | `{wallet_id, address, chain, network}` |
| `skills/wallet-manager/scripts/get_balance.py` | `<address>` | `{address, network, balances}` |
| `skills/wallet-manager/scripts/send_token.py` | `<wallet_id> <to> <token> <amount>` | `{status, tx_hash, explorer}` |
| `skills/market-info/scripts/get_price.py` | `<TOKEN> [...]` | `{symbol: {price, change_24h, ...}}` |
| `skills/market-info/scripts/get_gas.py` | none | `{gas_price_gwei, estimated_costs}` |
| `skills/trade-executor/scripts/get_quote.py` | `<sell> <buy> <amount>` | `{sell, buy, rate, price_impact, gas}` |
| `skills/trade-executor/scripts/execute_swap.py` | `<wallet_id> <addr> <sell> <buy> <amount>` | `{status, tx_hash, explorer}` |

## Platform Capabilities Required
The following platform-level features will improve this agent when implemented in ClawDI:

| Feature | Description |
|---------|-------------|
| **Secrets injection** | Platform injects `PRIVY_APP_ID`, `PRIVY_APP_SECRET`, `ZERO_X_API_KEY` automatically — users never need to configure `.env` |
| **Skill scanning mandate** | Platform forces full SKILL.md + references to load before every reply |
| **Workspace file auto-load** | SOUL.md, IDENTITY.md, USER.md auto-injected into context at session start |
| **Runtime metadata** | Current datetime, timezone, model name injected per session |
