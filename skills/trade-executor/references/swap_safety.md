# Swap Safety Guidelines

## Confirmation Protocol
Every swap requires explicit user confirmation before execution:
- Show full quote: amounts, rate, price impact, gas fee, route
- Wait for "confirm", "yes", "ok", or equivalent
- Treat anything ambiguous as NO — ask again
- Never auto-execute based on prior messages in the conversation

## Risk Thresholds
| Metric | Warn User | Refuse Without Explicit Override |
|--------|-----------|----------------------------------|
| Price impact | > 1% | > 5% |
| Gas cost / swap value | > 5% | > 20% |
| Slippage tolerance | Default: 0.5% | Max: 3% |

## What to Always Show in Quote
1. Exact amount being sold (with token symbol)
2. Estimated amount to receive (prefix with "~")
3. Exchange rate (e.g., 1 ETH = $3,745)
4. Price impact percentage
5. Estimated gas fee in USD
6. DEX routing (e.g., "Uniswap V3 100%")

## Error Handling
| Error | Response |
|-------|---------|
| Insufficient balance | Show current balance, suggest smaller amount |
| Slippage exceeded | Suggest retrying or increasing slippage slightly |
| Quote expired | Fetch fresh quote automatically, show for re-confirmation |
| Network error | Reassure funds are safe, suggest retry |
| Transaction reverted | Explain reason, funds are safe |

## Network Safety
- All swaps are on Base mainnet (Chain ID: 8453) only
- Never send to a contract address without user acknowledgment
- Remind users: Base addresses look like Ethereum addresses (0x...) but are a different network
