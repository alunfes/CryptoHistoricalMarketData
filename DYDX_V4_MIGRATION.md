# dYdX v3 to v4 Migration Summary

## Issue
Docker startup was showing dydx version errors because the `dydx3` package is no longer available on PyPI. dYdX has moved from v3 (Ethereum-based) to v4 (Cosmos-based blockchain).

## Changes Made

### 1. Dependency Updates

#### requirements.txt (root)
- Changed: `dydx3==1.0.1` → `dydx-v4-client==1.1.5`

#### app/requirements.txt
- Changed: `dydx3` → `dydx-v4-client`

### 2. API Endpoint Updates

#### ignore/apiendpoints.yaml
Updated dYdX endpoints to v4:
- Ticker API: `https://api.dydx.exchange/v3/markets` → `https://indexer.dydx.trade/v4/perpetualMarkets`
- OHLC API: `https://api.dydx.exchange/v3/candles/` → `https://indexer.dydx.trade/v4/candles/perpetualMarkets/`

### 3. Code Changes

#### app/DataDownLoader.py
- Removed imports:
  - `from dydx3 import Client`
  - `from dydx3.helpers.request_helpers import generate_now_iso`
  - `from web3 import Web3`
  - `from dydx3.constants import *`
- Removed unused `__dydx()` method that used the dydx3 SDK
- The `__download_dydx_ohlcv()` method continues to use direct HTTP calls via aiohttp, which is compatible with both v3 and v4

#### app/test.py
- Removed imports:
  - `from dydx3 import Client`
  - `from dydx3.helpers.request_helpers import generate_now_iso`
  - `from web3 import Web3`
  - `from dydx3.constants import *`
- Updated `dydx()` method to use direct HTTP API calls instead of the dydx3 SDK

#### app/TickerConverter.py
- Updated `__convert_dydx_ticker()` to handle both v3 and v4 API response formats:
  - v4 uses `'ACTIVE'` status instead of `'ONLINE'`
  - v4 uses `'ticker'` field instead of `'market'`
  - Added fallback logic to support both formats

### 4. Documentation Updates

#### README.md
- Updated dYdX API endpoints to v4

#### README_ja.md
- Updated dYdX API endpoints to v4 in all locations:
  - Configuration examples
  - Supported exchanges section
  - Troubleshooting section

#### DOCKER_ENHANCEMENTS_SUMMARY.md
- Updated references from `dydx3` to `dydx-v4-client`

## API Compatibility Notes

### Response Format Compatibility
The v4 API maintains similar response structures to v3 for OHLC data:
- Both use ISO timestamp format in `startedAt` field
- Both include `open`, `high`, `low`, `close` fields
- The `OhlcConverter.__convert_dydx_ohlc()` method works with both versions

### Ticker API Changes
The v4 ticker API has minor differences:
- Status: `'ONLINE'` (v3) → `'ACTIVE'` (v4)
- Market identifier: `'market'` (v3) → `'ticker'` (v4)
- Both changes are handled by the updated `TickerConverter`

### Resolution Values
Both v3 and v4 support the same resolution values:
- `1DAY`, `4HOURS`, `1HOUR`, `30MINS`, `15MINS`, `5MINS`, `1MIN`

## Benefits of Migration

1. **Removes Docker Startup Error**: The `dydx3` package is no longer available, causing installation failures
2. **Future-Proof**: Uses the actively maintained dYdX v4 API
3. **Minimal Code Changes**: Most of the codebase used direct HTTP calls, not the SDK
4. **Backward Compatible**: The converter handles both v3 and v4 response formats

## Testing Recommendations

1. Test ticker download: Verify that `__get_tickers()` correctly fetches dYdX markets
2. Test OHLC download: Verify that `__download_dydx_ohlcv()` correctly fetches candle data
3. Test data conversion: Verify that downloaded data is correctly converted and saved
4. Docker build: Verify that `docker compose build` succeeds without dydx3 errors

## Migration Notes

- The migration focuses on removing SDK dependencies and updating API endpoints
- The core data fetching logic remains unchanged (using aiohttp for direct HTTP calls)
- No changes to data storage format or file structure
- No changes to other exchanges (OKX, Bybit, ApexPro)
