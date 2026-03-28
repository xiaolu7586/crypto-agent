# Crypto Trader

A full-stack crypto trading agent for the ClawDI platform. Combines OKX wallet infrastructure with 6551 market intelligence to cover the complete trading workflow: research → signal → decide → execute.

## What It Does

| Category | Capabilities |
|----------|-------------|
| **Wallet** | Multi-chain wallet via OKX (20+ chains), Email OTP setup, balance, send |
| **DEX Trading** | Swap execution across 20+ chains, security scan before every trade |
| **CEX Trading** | Spot & futures on Binance, Bybit, OKX, Hyperliquid via 6551 |
| **DeFi** | Deposit/withdraw on Aave, Lido, Compound, and more |
| **Market Data** | Real-time prices, K-lines, gas fees |
| **Research** | Token metadata, holder distribution, trending tokens |
| **Signals** | Smart money, whale, KOL on-chain signals |
| **Meme Tokens** | Pump.fun/meme token scanning, rug pull and bundle detection |
| **Social Intel** | Twitter/X KOL monitoring, real-time push events |
| **News** | Crypto news with AI impact ratings and trading signals |
| **Security** | Token honeypot detection, transaction simulation, approval management |
| **Portfolio** | Multi-chain portfolio tracking and DeFi position overview |

## Setup

### Step 1 — Get your 6551 token
Visit https://6551.io/mcp and get your `OPEN_TOKEN`.

### Step 2 — Start the agent
Send any message. The agent will:
1. Auto-install required tools (`onchainos` + `opentrade`)
2. Guide you through OKX wallet creation (email + OTP, one time only)
3. Ask for your 6551 token on first use of news/Twitter/CEX features

### Step 3 — Start trading
Your wallet is ready. Deposit funds and start trading.

## Data Sources

By default, wallet and trading execution use OKX. Market data, research, and signals also default to OKX but can be switched to 6551:

- **Temporary**: "Use 6551 to check ETH price"
- **Persistent**: "Use 6551 for market data from now on"
- **Switch back**: "Switch back to OKX for market data"

## Security Scan

Security scanning is **enabled by default** for all DEX swaps. To disable:
> "Turn off security scan"

The agent will warn you and ask for confirmation. To re-enable:
> "Enable security scan"

## Supported Chains

Ethereum, Base, BSC, Arbitrum, Solana, XLayer, Polygon, and 15+ more.
Run `onchainos wallet chains` for the full list.

## Skills

Powered by 22 skills from OKX and 6551:

**OKX (13):** okx-agentic-wallet, okx-dex-swap, okx-dex-market, okx-wallet-portfolio, okx-onchain-gateway, okx-security, okx-defi-invest, okx-defi-portfolio, okx-dex-token, okx-dex-signal, okx-dex-trenches, okx-audit-log, okx-x402-payment

**6551 (9):** opennews, opentwitter, opentrade-dex-swap, opentrade-market, opentrade-portfolio, opentrade-token, opentrade-gateway, opentrade-newsliquid, opentrade-wallet

## Disclaimer

This agent is a tool, not a financial advisor. All trading decisions are yours. Crypto markets are volatile — only trade what you can afford to lose.
