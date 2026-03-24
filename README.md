# Crypto Trader — ClawDI Agent

An AI-powered crypto trading assistant for [ClawDI](https://www.clawdi.ai/). Manage your wallet, track markets, and execute token swaps on Base network — all through natural conversation.

## What it does

- **Wallet management** — automatic wallet creation on first use, balance tracking, deposits and transfers
- **Market data** — real-time token prices, 24h change, and Base network gas fees
- **Token swaps** — get quotes and execute swaps via 0x Protocol with mandatory confirmation

## Quick Start

### 1. Prerequisites
- A [ClawDI](https://www.clawdi.ai/) account with this agent installed
- Wallet infrastructure credentials (set by platform admin)
- A [0x Protocol API key](https://0x.org/docs/introduction/getting-started) (free tier available)

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start chatting
Open ClawDI and say anything — your wallet is created automatically on first message.

## Skills

| Skill | Description |
|-------|-------------|
| `wallet-manager` | Create wallet, check balance, send tokens, get deposit address |
| `market-info` | Real-time prices, 24h change, gas fees |
| `trade-executor` | Swap token quotes and execution with confirmation |

## Repo Structure

```
crypto-agent/
├── AGENTS.md              # Core system prompt
├── TOOLS.md               # Runtime environment reference
├── SOUL.md                # Behavioral philosophy
├── IDENTITY.md            # Agent persona
├── USER.md                # User profile (wallet address, preferences)
├── HEARTBEAT.md           # Scheduled tasks placeholder
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
└── skills/
    ├── wallet-manager/    # Wallet creation, balance, transfers
    ├── market-info/       # Token prices and gas fees
    └── trade-executor/    # Swap quotes and execution
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PRIVY_APP_ID` | ✅ | Wallet infrastructure App ID |
| `PRIVY_APP_SECRET` | ✅ | Wallet infrastructure App Secret |
| `ZERO_X_API_KEY` | ✅ | [0x Protocol](https://0x.org) API key |
| `BASE_RPC_URL` | Optional | Base RPC (default: mainnet.base.org) |
| `COINGECKO_API_KEY` | Optional | CoinGecko Pro key (free tier works without) |

## Supported Tokens (Base Network)

ETH · USDC · USDT · DAI · WETH · cbETH

## Platform Capabilities Required

The following platform-level features will improve this agent when implemented in ClawDI:

| Feature | Impact |
|---------|--------|
| **Secrets injection** | Users never need to configure `.env` — credentials injected by platform |
| **Skill scanning mandate** | Forces full SKILL.md + references to load before every reply |
| **Workspace file auto-load** | SOUL.md, IDENTITY.md, USER.md injected into context at session start |
| **Runtime metadata** | Current datetime and timezone injected per session |

## Version Roadmap

| Version | Features |
|---------|---------|
| **V1 (current)** | Wallet creation · Balance · Send · Market prices · Token swaps on Base |
| **V2** | AI trade advisor (bull/bear analysis, 5-tier signal) · Portfolio tracker |
| **V3** | Solana support · Price alerts · Conditional orders · DeFi yields (Aave/Morpho) |

## Disclaimer

This agent is for informational and utility purposes only. It is not financial advice. Crypto assets are volatile. Always verify transaction details before confirming. You are solely responsible for your trading decisions.
