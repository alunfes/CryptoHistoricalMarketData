# Incremental OHLCV Data Download Feature

## Overview

This implementation adds incremental download capability to the CryptoHistoricalMarketData application, allowing it to:

1. **Check for existing data** before downloading
2. **Download only new/missing data** since the last timestamp
3. **Append incremental data** to existing files without duplicates
4. **Process all available symbols** for each exchange (removed artificial limits)

## Key Changes

### 1. DataWriter Enhancements (`app/DataWriter.py`)

#### New Methods

- **`get_last_timestamp(exchange, base, quote)`**
  - Returns the most recent timestamp from an existing data file
  - Returns `None` if the file doesn't exist
  - Handles errors gracefully when reading files

- **`file_exists(exchange, base, quote)`**
  - Checks if a data file exists for the given exchange/symbol pair
  - Used for logging purposes (showing "Updated" vs "Downloaded")

#### Modified Method

- **`write_data(exchange, symbol, base, quote)`**
  - Now checks if a file already exists before writing
  - If file exists: appends new data, removes duplicates, and sorts by timestamp
  - If file doesn't exist: creates the file with the new data
  - Automatically creates the Data directory if it doesn't exist

### 2. DataDownLoader Modifications (`app/DataDownLoader.py`)

#### All Exchange Download Methods Updated

For each exchange (`okx`, `bybit`, `dydx`, `apexpro`), the `__start_*_ohlcv_download` methods now:

1. **Check for existing data**:
   ```python
   last_ts = DataWriter.get_last_timestamp(exchange, base, quote)
   ```

2. **Calculate download start time**:
   ```python
   download_since = last_ts + 60000 if last_ts is not None else since_ts
   ```
   - If data exists: starts from last timestamp + 1 minute (60000 ms)
   - If no data: uses the original `since_ts` (e.g., 90 days ago)

3. **Skip if data is up to date**:
   ```python
   if download_since >= till_ts:
       print(f'Skipping {exchange}-{symbol}: data is up to date')
       continue
   ```

4. **Process all symbols**: Removed counter limits that were stopping after a few symbols

#### Enhanced Logging

All download methods now show:
- "Updated" for existing files being updated with new data
- "Downloaded" for new files being created
- "No new data" when API returns empty results
- "Skipping" when data is already up to date

### 3. Timestamp Consistency Fix (`app/OhlcConverter.py`)

- Fixed dYdX timestamp conversion to use milliseconds consistently
- All exchanges now store timestamps in milliseconds for uniformity

## Usage

The changes are transparent to users. Simply run the application as before:

```bash
python app/main.py
```

### First Run (No Existing Data)
- Downloads data from `since_num_days_before` (configured in `params.yaml`, default 90 days)
- Creates CSV files for each symbol in `./app/Data/`

### Subsequent Runs (Existing Data)
- Checks each symbol's existing data file
- Downloads only data from the last timestamp onwards
- Appends new data to existing files
- Skips symbols that are already up to date

## Configuration

No new configuration is needed. The existing `params.yaml` settings still apply:

```yaml
exchanges: ['bybit', 'okx', 'dydx', 'apexpro']
since_num_days_before: 90  # Used only for initial downloads
ohlcv_data_interval:
  okx: '1m'
  bybit: 1
  dydx: '1MIN'
  apexpro: 1
```

## Data File Format

Data files remain in CSV format with the following columns:
- `timestamp` - Unix timestamp in milliseconds
- `open` - Opening price
- `high` - Highest price
- `low` - Lowest price
- `close` - Closing price

File naming convention: `{exchange}-{base}-{quote}.csv`

Example: `bybit-BTC-USDT.csv`, `dydx-ETH-USD.csv`

## Benefits

1. **Efficiency**: Only downloads new data, saving bandwidth and API calls
2. **Continuity**: Maintains historical data without re-downloading
3. **Scalability**: Processes all symbols without manual limits
4. **Reliability**: Handles duplicates and maintains sorted timestamps
5. **Transparency**: Clear logging shows what's being updated vs downloaded

## Testing

Comprehensive test suites are included:

- `test_incremental_download.py` - Unit tests for core functionality
- `test_full_workflow.py` - Integration tests simulating real-world scenarios

Run tests:
```bash
cd app
python3 test_incremental_download.py
python3 test_full_workflow.py
```

## Edge Cases Handled

1. **No existing data**: Downloads from `since_num_days_before`
2. **Partial data**: Downloads from last timestamp onwards
3. **Up-to-date data**: Skips download to avoid unnecessary API calls
4. **Duplicate timestamps**: Automatically removed during append
5. **Gaps in data**: System downloads from last timestamp (doesn't fill gaps)
6. **Corrupted files**: Gracefully falls back to overwriting

## Technical Details

### Timestamp Management
- All timestamps stored in milliseconds
- Incremental downloads start at `last_timestamp + 60000` (1 minute after last data)
- Prevents overlap and duplicate data points

### Data Merging
- Uses pandas `concat` to combine old and new data
- `drop_duplicates` removes any overlapping timestamps
- `sort_values` ensures chronological order
- `reset_index` maintains clean DataFrame structure

### Thread Safety
- All OHLCData operations use threading locks
- DataWriter methods are class methods for safe concurrent access

## Future Enhancements

Possible improvements for future versions:
- Gap detection and filling
- Data validation and integrity checks
- Compression for large historical datasets
- Database backend option for better performance
- Retry logic for failed downloads
- Progress bars for long-running downloads
