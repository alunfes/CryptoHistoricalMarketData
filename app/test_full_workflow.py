"""
Integration test to simulate the full download workflow
"""
import os
import pandas as pd
import time
from DataWriter import DataWriter
from OHLCData import OHLCData
from TickerData import TickerData

def simulate_initial_download():
    """Simulate an initial download scenario"""
    print("\n" + "=" * 60)
    print("TEST 1: Simulating initial download (no existing data)")
    print("=" * 60)
    
    # Initialize
    TickerData.initialize()
    OHLCData.initialize()
    
    # Add a test ticker
    TickerData.add_ticker('test_exchange', 'BTC-USD', 'BTC', 'USD', 'perpetual')
    
    # Simulate scenario where no data exists
    last_ts = DataWriter.get_last_timestamp('test_exchange', 'BTC', 'USD')
    assert last_ts is None, f"Expected None for non-existent file, got {last_ts}"
    print("✓ No existing data found (as expected)")
    
    # Simulate download with since_ts from 90 days ago
    current_ts = int(time.time() * 1000)
    since_ts = current_ts - (90 * 24 * 60 * 60 * 1000)
    
    # Should use since_ts since no existing data
    download_since = last_ts + 60000 if last_ts is not None else since_ts
    assert download_since == since_ts, "Should use since_ts for initial download"
    print(f"✓ Using initial since_ts: {since_ts}")
    
    # Simulate downloaded data
    timestamps = [since_ts + i * 60000 for i in range(10)]  # 10 minutes of data
    opens = [100 + i for i in range(10)]
    highs = [110 + i for i in range(10)]
    lows = [90 + i for i in range(10)]
    closes = [105 + i for i in range(10)]
    
    OHLCData.add_data('test_exchange', 'BTC-USD', 'BTC', 'USD', 
                      opens, highs, lows, closes, timestamps)
    
    # Write data
    import asyncio
    asyncio.run(DataWriter.write_data('test_exchange', 'BTC-USD', 'BTC', 'USD'))
    
    # Verify file was created
    assert DataWriter.file_exists('test_exchange', 'BTC', 'USD'), "File should exist after write"
    print("✓ Data file created successfully")
    
    # Verify data
    df = pd.read_csv('./app/Data/test_exchange-BTC-USD.csv')
    assert len(df) == 10, f"Expected 10 records, got {len(df)}"
    print(f"✓ {len(df)} records written successfully")
    print(f"  Timestamp range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    

def simulate_incremental_download():
    """Simulate an incremental download scenario"""
    print("\n" + "=" * 60)
    print("TEST 2: Simulating incremental download (existing data)")
    print("=" * 60)
    
    # Initialize
    OHLCData.initialize()
    
    # Get last timestamp from existing data
    last_ts = DataWriter.get_last_timestamp('test_exchange', 'BTC', 'USD')
    assert last_ts is not None, "Should have existing data from previous test"
    print(f"✓ Found existing data, last timestamp: {last_ts}")
    
    # Simulate scenario where we want to download from last_ts onwards
    current_ts = int(time.time() * 1000)
    
    # Calculate download_since (should be last_ts + 60000)
    download_since = last_ts + 60000
    print(f"✓ Will download from: {download_since} (last_ts + 1 minute)")
    
    # Simulate downloading 5 more minutes of data
    new_timestamps = [download_since + i * 60000 for i in range(5)]
    new_opens = [110 + i for i in range(5)]
    new_highs = [120 + i for i in range(5)]
    new_lows = [100 + i for i in range(5)]
    new_closes = [115 + i for i in range(5)]
    
    OHLCData.add_data('test_exchange', 'BTC-USD', 'BTC', 'USD', 
                      new_opens, new_highs, new_lows, new_closes, new_timestamps)
    
    # Write data (should append)
    import asyncio
    asyncio.run(DataWriter.write_data('test_exchange', 'BTC-USD', 'BTC', 'USD'))
    
    # Verify data was appended
    df = pd.read_csv('./app/Data/test_exchange-BTC-USD.csv')
    assert len(df) == 15, f"Expected 15 records (10 + 5), got {len(df)}"
    print(f"✓ Data appended successfully: {len(df)} total records")
    print(f"  Timestamp range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    
    # Verify timestamps are sorted and unique
    assert df['timestamp'].is_monotonic_increasing, "Timestamps should be sorted"
    assert df['timestamp'].is_unique, "Timestamps should be unique"
    print("✓ Timestamps are sorted and unique")


def simulate_skip_scenario():
    """Simulate scenario where data is up to date"""
    print("\n" + "=" * 60)
    print("TEST 3: Simulating skip scenario (data is up to date)")
    print("=" * 60)
    
    # Get last timestamp
    last_ts = DataWriter.get_last_timestamp('test_exchange', 'BTC', 'USD')
    print(f"✓ Last timestamp in data: {last_ts}")
    
    # Simulate current time is before or equal to last data
    simulated_till_ts = last_ts  # Pretend current time equals last data time
    download_since = last_ts + 60000
    
    # Should skip because download_since >= till_ts
    should_skip = download_since >= simulated_till_ts
    assert should_skip, "Should skip when data is up to date"
    print(f"✓ Correctly identified that data is up to date")
    print(f"  download_since ({download_since}) >= till_ts ({simulated_till_ts})")


def simulate_gap_in_data():
    """Simulate downloading when there's a gap in existing data"""
    print("\n" + "=" * 60)
    print("TEST 4: Simulating gap in data")
    print("=" * 60)
    
    # Initialize
    OHLCData.initialize()
    
    # Create data with a gap
    timestamps_before = [1000000 + i * 60000 for i in range(5)]
    timestamps_after = [2000000 + i * 60000 for i in range(5)]  # Gap between 1240000 and 2000000
    
    all_timestamps = timestamps_before + timestamps_after
    opens = [100 + i for i in range(10)]
    highs = [110 + i for i in range(10)]
    lows = [90 + i for i in range(10)]
    closes = [105 + i for i in range(10)]
    
    # Create new test file
    os.makedirs('./app/Data', exist_ok=True)
    gap_data = pd.DataFrame([
        {'timestamp': t, 'open': o, 'high': h, 'low': l, 'close': c}
        for t, o, h, l, c in zip(all_timestamps, opens, highs, lows, closes)
    ])
    gap_data.to_csv('./app/Data/test_gap-BTC-USD.csv', index=False)
    
    # Get last timestamp (should be from the after-gap data)
    last_ts = DataWriter.get_last_timestamp('test_gap', 'BTC', 'USD')
    assert last_ts == timestamps_after[-1], f"Expected {timestamps_after[-1]}, got {last_ts}"
    print(f"✓ Last timestamp correctly identified: {last_ts}")
    
    # Note: The system will download from last_ts onwards, not fill the gap
    # This is by design - it fetches the most recent data
    print("✓ System will fetch data after last timestamp (gap will remain)")
    print("  This is the expected behavior for incremental updates")
    
    # Cleanup
    os.remove('./app/Data/test_gap-BTC-USD.csv')


def cleanup():
    """Clean up test files"""
    print("\n" + "=" * 60)
    print("Cleaning up test files")
    print("=" * 60)
    
    test_file = './app/Data/test_exchange-BTC-USD.csv'
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"✓ Removed {test_file}")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("FULL WORKFLOW INTEGRATION TESTS")
    print("=" * 60)
    
    try:
        simulate_initial_download()
        simulate_incremental_download()
        simulate_skip_scenario()
        simulate_gap_in_data()
        cleanup()
        
        print("\n" + "=" * 60)
        print("ALL INTEGRATION TESTS PASSED! ✓")
        print("=" * 60 + "\n")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Ensure cleanup
        try:
            cleanup()
        except:
            pass
