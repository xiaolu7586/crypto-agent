---
name: okx-cex
description: "Use this skill when the user asks to check their OKX exchange balance, place a spot order, cancel an order, view open orders, check positions, view trade history, set leverage, or any operation on their OKX exchange (CEX) account. Trigger on phrases like 'my OKX balance', 'buy BTC on OKX', 'place a limit order', 'cancel my order', 'check my positions', 'open orders', 'trade history', 'set leverage', '我的OKX余额', '挂单', '撤单', '查持仓', '交易记录'. Do NOT use for DEX swaps or on-chain operations (use okx-dex-swap or onchainos instead)."
license: MIT
metadata:
  author: clawdi
  version: "1.0.0"
  homepage: "https://www.okx.com/docs-v5/en/"
---

# OKX CEX Account

Direct OKX REST API integration for centralized exchange operations — balance, spot orders, positions, and trade history.

## Pre-flight: Load Credentials

Before any operation, read credentials from USER.md:

```bash
OKX_API_KEY=$(grep "API Key:" USER.md | awk '{print $NF}')
OKX_API_SECRET=$(grep "API Secret:" USER.md | awk '{print $NF}')
OKX_PASSPHRASE=$(grep "API Passphrase:" USER.md | awk '{print $NF}')
```

If any credential is empty, tell the user: "Your OKX exchange account is not connected yet. Please say 'connect my OKX account' to set it up."

## Signing Helper

All OKX API calls require HMAC-SHA256 authentication. Use this Python snippet before each request:

```python
import hmac, hashlib, base64, datetime

def okx_sign(secret, timestamp, method, path, body=""):
    msg = timestamp + method + path + body
    sig = base64.b64encode(
        hmac.new(secret.encode(), msg.encode(), hashlib.sha256).digest()
    ).decode()
    return sig

ts = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
sign = okx_sign("$OKX_API_SECRET", ts, "GET", "/api/v5/account/balance")
print(f"{ts}|{sign}")
```

Then use the output in curl headers:
```bash
OKX_BASE="https://www.okx.com"
-H "OK-ACCESS-KEY: $OKX_API_KEY"
-H "OK-ACCESS-SIGN: <sign>"
-H "OK-ACCESS-TIMESTAMP: <ts>"
-H "OK-ACCESS-PASSPHRASE: $OKX_PASSPHRASE"
-H "Content-Type: application/json"
```

## Command Index

| # | Operation | Method | Path |
|---|---|---|---|
| 1 | Check account balance | GET | `/api/v5/account/balance` |
| 2 | Place spot order | POST | `/api/v5/trade/order` |
| 3 | Cancel order | DELETE | `/api/v5/trade/order` |
| 4 | View open orders | GET | `/api/v5/trade/orders-pending` |
| 5 | View order history | GET | `/api/v5/trade/orders-history` |
| 6 | Check positions | GET | `/api/v5/account/positions` |
| 7 | Get ticker price | GET | `/api/v5/market/ticker?instId=<PAIR>` |

## Operations

### 1. Check Account Balance

```bash
TS=$(python3 -c "import datetime; print(datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z'))")
SIGN=$(python3 -c "
import hmac,hashlib,base64
ts='$TS'; secret='$OKX_API_SECRET'
msg=ts+'GET'+'/api/v5/account/balance'
print(base64.b64encode(hmac.new(secret.encode(),msg.encode(),hashlib.sha256).digest()).decode())
")
curl -s "$OKX_BASE/api/v5/account/balance" \
  -H "OK-ACCESS-KEY: $OKX_API_KEY" \
  -H "OK-ACCESS-SIGN: $SIGN" \
  -H "OK-ACCESS-TIMESTAMP: $TS" \
  -H "OK-ACCESS-PASSPHRASE: $OKX_PASSPHRASE" \
  -H "Content-Type: application/json"
```

Display: show each currency with total, available, and frozen balance. Skip zero balances.

### 2. Place Spot Order

Parameters needed from user:
- `instId`: trading pair, e.g. `BTC-USDT`
- `side`: `buy` or `sell`
- `ordType`: `market` or `limit`
- `sz`: quantity
- `px`: price (limit orders only)

```bash
BODY='{"instId":"BTC-USDT","tdMode":"cash","side":"buy","ordType":"limit","sz":"0.001","px":"60000"}'
TS=$(python3 -c "import datetime; print(datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z'))")
SIGN=$(python3 -c "
import hmac,hashlib,base64
ts='$TS'; secret='$OKX_API_SECRET'
body='$BODY'
msg=ts+'POST'+'/api/v5/trade/order'+body
print(base64.b64encode(hmac.new(secret.encode(),msg.encode(),hashlib.sha256).digest()).decode())
")
curl -s -X POST "$OKX_BASE/api/v5/trade/order" \
  -H "OK-ACCESS-KEY: $OKX_API_KEY" \
  -H "OK-ACCESS-SIGN: $SIGN" \
  -H "OK-ACCESS-TIMESTAMP: $TS" \
  -H "OK-ACCESS-PASSPHRASE: $OKX_PASSPHRASE" \
  -H "Content-Type: application/json" \
  -d "$BODY"
```

Always confirm with user before placing: show pair, side, amount, price. Wait for explicit confirmation.

### 3. Cancel Order

Parameters: `instId` and `ordId`

```bash
BODY='{"instId":"BTC-USDT","ordId":"<orderId>"}'
TS=$(python3 -c "import datetime; print(datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z'))")
SIGN=$(python3 -c "
import hmac,hashlib,base64
ts='$TS'; secret='$OKX_API_SECRET'
body='$BODY'
msg=ts+'DELETE'+'/api/v5/trade/order'+body
print(base64.b64encode(hmac.new(secret.encode(),msg.encode(),hashlib.sha256).digest()).decode())
")
curl -s -X DELETE "$OKX_BASE/api/v5/trade/order" \
  -H "OK-ACCESS-KEY: $OKX_API_KEY" \
  -H "OK-ACCESS-SIGN: $SIGN" \
  -H "OK-ACCESS-TIMESTAMP: $TS" \
  -H "OK-ACCESS-PASSPHRASE: $OKX_PASSPHRASE" \
  -H "Content-Type: application/json" \
  -d "$BODY"
```

### 4. View Open Orders

```bash
TS=$(python3 -c "import datetime; print(datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z'))")
SIGN=$(python3 -c "
import hmac,hashlib,base64
ts='$TS'; secret='$OKX_API_SECRET'
msg=ts+'GET'+'/api/v5/trade/orders-pending'
print(base64.b64encode(hmac.new(secret.encode(),msg.encode(),hashlib.sha256).digest()).decode())
")
curl -s "$OKX_BASE/api/v5/trade/orders-pending" \
  -H "OK-ACCESS-KEY: $OKX_API_KEY" \
  -H "OK-ACCESS-SIGN: $SIGN" \
  -H "OK-ACCESS-TIMESTAMP: $TS" \
  -H "OK-ACCESS-PASSPHRASE: $OKX_PASSPHRASE" \
  -H "Content-Type: application/json"
```

### 5. View Order History

```bash
TS=$(python3 -c "import datetime; print(datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z'))")
SIGN=$(python3 -c "
import hmac,hashlib,base64
ts='$TS'; secret='$OKX_API_SECRET'
path='/api/v5/trade/orders-history?instType=SPOT'
msg=ts+'GET'+path
print(base64.b64encode(hmac.new(secret.encode(),msg.encode(),hashlib.sha256).digest()).decode())
")
curl -s "$OKX_BASE/api/v5/trade/orders-history?instType=SPOT" \
  -H "OK-ACCESS-KEY: $OKX_API_KEY" \
  -H "OK-ACCESS-SIGN: $SIGN" \
  -H "OK-ACCESS-TIMESTAMP: $TS" \
  -H "OK-ACCESS-PASSPHRASE: $OKX_PASSPHRASE" \
  -H "Content-Type: application/json"
```

### 6. Check Positions

```bash
TS=$(python3 -c "import datetime; print(datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z'))")
SIGN=$(python3 -c "
import hmac,hashlib,base64
ts='$TS'; secret='$OKX_API_SECRET'
msg=ts+'GET'+'/api/v5/account/positions'
print(base64.b64encode(hmac.new(secret.encode(),msg.encode(),hashlib.sha256).digest()).decode())
")
curl -s "$OKX_BASE/api/v5/account/positions" \
  -H "OK-ACCESS-KEY: $OKX_API_KEY" \
  -H "OK-ACCESS-SIGN: $SIGN" \
  -H "OK-ACCESS-TIMESTAMP: $TS" \
  -H "OK-ACCESS-PASSPHRASE: $OKX_PASSPHRASE" \
  -H "Content-Type: application/json"
```

## Error Handling

| Error code | Meaning | Action |
|---|---|---|
| `50111` | Invalid API Key | Ask user to verify credentials in USER.md |
| `50113` | Invalid signature | Retry once; if fails, ask user to reconnect |
| `51000` | Parameter error | Check instId format (e.g. BTC-USDT not BTC/USDT) |
| `51008` | Insufficient balance | Show current balance, ask user to adjust amount |

On any auth error (5011x): tell user "Your OKX API credentials may be invalid or expired. Please reconnect via 'connect my OKX account'."

## Display Rules

- Always show amounts with currency symbol
- For orders: show pair, side (Buy/Sell), type, amount, price, status
- For balance: only show non-zero currencies
- Never expose raw API credentials in responses
- Confirm before any write operation (place/cancel order)
