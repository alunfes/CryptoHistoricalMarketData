# Implementation Summary: Incremental OHLCV Data Fetching

## Problem Statement (Japanese)
指定した取引所のすべての銘柄の1m ohlcvを可能な限り取得できるようにする。
取得ずみのデータを確認し、取得ずみのデータがある場合は差分・直近データ以降を取得して追記するようにする。

## Translation
Enable fetching of 1-minute OHLCV data for all symbols on specified exchanges as much as possible.
Check for existing data, and if data already exists, fetch and append differential/recent data after the existing data.

## Solution Implemented

### Core Functionality

#### 1. Existing Data Detection
- Added `DataWriter.get_last_timestamp()` to read the last timestamp from existing CSV files
- Added `DataWriter.file_exists()` to check if data files exist
- Returns `None` if no data exists, enabling initial full download

#### 2. Incremental Download Logic
For each exchange and symbol:
```python
# Check for existing data
last_ts = DataWriter.get_last_timestamp(exchange, base, quote)

# Calculate download start point
if last_ts is not None:
    download_since = last_ts + 60000  # Start 1 minute after last data
else:
    download_since = since_ts  # Use default (e.g., 90 days ago)

# Skip if data is up to date
if download_since >= till_ts:
    print(f'Skipping {exchange}-{symbol}: data is up to date')
    continue
```

#### 3. Data Merging & Deduplication
Modified `DataWriter.write_data()` to:
- Read existing data if file exists
- Concatenate old and new data
- Remove duplicates based on timestamp
- Sort by timestamp
- Save merged data

```python
if os.path.exists(file_path):
    existing_df = pd.read_csv(file_path)
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset=['timestamp'], keep='last')
    combined_df = combined_df.sort_values('timestamp').reset_index(drop=True)
    combined_df.to_csv(file_path, index=False)
```

#### 4. Remove Download Limits
Removed all counter-based limits that were stopping after downloading just a few symbols:
- OKX: was limited to 1 symbol → now processes all
- Bybit: was limited to 3 symbols → now processes all
- dYdX: was limited to 10 symbols → now processes all
- ApexPro: was limited to 2 symbols → now processes all

### Files Modified

#### 1. `app/DataWriter.py`
**Added methods:**
- `get_last_timestamp(exchange, base, quote)` - Gets last timestamp from existing file
- `file_exists(exchange, base, quote)` - Checks if file exists

**Modified method:**
- `write_data()` - Now appends to existing files with deduplication

#### 2. `app/DataDownLoader.py`
**Modified methods:**
- `__start_okx_ohlcv_download()` - Added incremental logic, removed limit
- `__start_bybit_ohlcv_download()` - Added incremental logic, removed limit
- `__start_dydx_ohlcv_download()` - Added incremental logic, removed limit
- `__start_apexpro_ohlcv_download()` - Added incremental logic, removed limit
- All `__download_*_ohlcv()` methods - Enhanced logging

#### 3. `app/OhlcConverter.py`
**Fixed:**
- `__convert_dydx_ohlc()` - Changed timestamp conversion from seconds to milliseconds for consistency

### Test Coverage

#### Unit Tests (`test_incremental_download.py`)
- ✓ `test_get_last_timestamp()` - Verify reading last timestamp
- ✓ `test_file_exists()` - Verify file existence checking
- ✓ `test_append_data()` - Verify data appending
- ✓ `test_duplicate_handling()` - Verify duplicate removal

#### Integration Tests (`test_full_workflow.py`)
- ✓ Initial download scenario (no existing data)
- ✓ Incremental download scenario (existing data)
- ✓ Skip scenario (data is up to date)
- ✓ Gap in data scenario

### Behavior Changes

#### Before Implementation:
```
Run 1: Download limited symbols (1-10 symbols per exchange)
Run 2: Re-download same data, overwrite files
Result: Wasted bandwidth, limited symbol coverage
```

#### After Implementation:
```
Run 1: Download ALL symbols from 90 days ago
Run 2: Check each file, download only new data since last timestamp
Run 3: Skip symbols that are up to date
Result: Efficient, complete coverage, no wasted downloads
```

### Example Workflow

#### First Run
```
Downloading target tickers...
Download Ticker Done for dydx, num tickers=37

Started ohlc download process...
Downloaded dydx-BTC-USD (BTC-USD): 129600 records
Downloaded dydx-ETH-USD (ETH-USD): 129600 records
Downloaded dydx-LINK-USD (LINK-USD): 129600 records
... (continues for all 37 symbols)
```

#### Second Run (1 hour later)
```
Downloading target tickers...
Download Ticker Done for dydx, num tickers=37

Started ohlc download process...
Updated dydx-BTC-USD (BTC-USD): 60 records
Updated dydx-ETH-USD (ETH-USD): 60 records
Updated dydx-LINK-USD (LINK-USD): 60 records
... (continues for all 37 symbols)
```

#### Third Run (immediately after)
```
Downloading target tickers...
Download Ticker Done for dydx, num tickers=37

Started ohlc download process...
Skipping dydx-BTC-USD: data is up to date
Skipping dydx-ETH-USD: data is up to date
Skipping dydx-LINK-USD: data is up to date
... (continues for all 37 symbols)
```

### Technical Details

#### Timestamp Handling
- All timestamps stored in **milliseconds** (Unix epoch)
- Consistent across all exchanges (OKX, Bybit, dYdX, ApexPro)
- Increment by 60000ms (1 minute) to avoid duplicate downloads

#### File Format
- CSV format: `{exchange}-{base}-{quote}.csv`
- Columns: timestamp, open, high, low, close
- Sorted by timestamp in ascending order
- No duplicates

#### Thread Safety
- OHLCData uses threading locks for concurrent access
- DataWriter methods are thread-safe

### Performance Benefits

1. **Bandwidth Savings**: Only downloads new data
2. **Time Savings**: Skips up-to-date symbols
3. **Completeness**: Processes all available symbols
4. **Reliability**: Handles edge cases (duplicates, gaps, errors)
5. **Maintainability**: Clear logging and error messages

### Configuration

No configuration changes required. Uses existing `params.yaml`:

```yaml
exchanges: ['bybit', 'okx', 'dydx', 'apexpro']
since_num_days_before: 90  # Only used for initial downloads
ohlcv_data_interval:
  okx: '1m'
  bybit: 1
  dydx: '1MIN'
  apexpro: 1
```

### Compatibility

- ✓ Backward compatible - works with existing data files
- ✓ No breaking changes to API or file formats
- ✓ Transparent to existing code
- ✓ Can be run repeatedly without issues

## Summary

The implementation successfully addresses both requirements:

1. ✅ **すべての銘柄の1m ohlcvを可能な限り取得** - All artificial limits removed, downloads all available symbols
2. ✅ **取得ずみのデータを確認し、差分・直近データ以降を取得して追記** - Checks existing data, downloads and appends only incremental data

The solution is efficient, reliable, and ready for production use.
