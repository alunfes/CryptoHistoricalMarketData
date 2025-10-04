"""
Test script to verify incremental download functionality
"""
import os
import pandas as pd
import tempfile
import shutil
from DataWriter import DataWriter
from OHLCData import OHLCData

def test_get_last_timestamp():
    """Test getting last timestamp from existing file"""
    print("Testing get_last_timestamp()...")
    
    # Create a temporary test file
    test_data = pd.DataFrame([
        {'timestamp': 1000000, 'open': 100, 'high': 110, 'low': 90, 'close': 105},
        {'timestamp': 2000000, 'open': 105, 'high': 115, 'low': 95, 'close': 110},
        {'timestamp': 3000000, 'open': 110, 'high': 120, 'low': 100, 'close': 115},
    ])
    
    # Create test directory
    os.makedirs('./app/Data', exist_ok=True)
    test_file = './app/Data/test-BTC-USD.csv'
    test_data.to_csv(test_file, index=False)
    
    # Test getting last timestamp
    last_ts = DataWriter.get_last_timestamp('test', 'BTC', 'USD')
    assert last_ts == 3000000, f"Expected 3000000, got {last_ts}"
    print(f"✓ Last timestamp correctly retrieved: {last_ts}")
    
    # Test non-existent file
    last_ts_none = DataWriter.get_last_timestamp('test', 'ETH', 'USD')
    assert last_ts_none is None, f"Expected None, got {last_ts_none}"
    print("✓ Non-existent file returns None")
    
    # Cleanup
    os.remove(test_file)
    print("✓ test_get_last_timestamp passed\n")


def test_file_exists():
    """Test file_exists method"""
    print("Testing file_exists()...")
    
    # Create test file
    os.makedirs('./app/Data', exist_ok=True)
    test_file = './app/Data/test-BTC-USD.csv'
    pd.DataFrame({'timestamp': [1000000]}).to_csv(test_file, index=False)
    
    # Test existing file
    exists = DataWriter.file_exists('test', 'BTC', 'USD')
    assert exists == True, f"Expected True, got {exists}"
    print("✓ Existing file detected correctly")
    
    # Test non-existent file
    not_exists = DataWriter.file_exists('test', 'ETH', 'USD')
    assert not_exists == False, f"Expected False, got {not_exists}"
    print("✓ Non-existent file detected correctly")
    
    # Cleanup
    os.remove(test_file)
    print("✓ test_file_exists passed\n")


def test_append_data():
    """Test appending new data to existing file"""
    print("Testing data append functionality...")
    
    # Create initial data
    initial_data = pd.DataFrame([
        {'timestamp': 1000000, 'open': 100, 'high': 110, 'low': 90, 'close': 105},
        {'timestamp': 2000000, 'open': 105, 'high': 115, 'low': 95, 'close': 110},
    ])
    
    os.makedirs('./app/Data', exist_ok=True)
    test_file = './app/Data/test-BTC-USD.csv'
    initial_data.to_csv(test_file, index=False)
    
    # Simulate new data being added to OHLCData
    OHLCData.initialize()
    new_timestamps = [3000000, 4000000]
    new_opens = [110, 115]
    new_highs = [120, 125]
    new_lows = [100, 105]
    new_closes = [115, 120]
    
    OHLCData.add_data('test', 'BTC-USD', 'BTC', 'USD', 
                      new_opens, new_highs, new_lows, new_closes, new_timestamps)
    
    # Import asyncio to run async write_data
    import asyncio
    asyncio.run(DataWriter.write_data('test', 'BTC-USD', 'BTC', 'USD'))
    
    # Read combined data
    combined = pd.read_csv(test_file)
    
    # Verify data was appended and sorted
    assert len(combined) == 4, f"Expected 4 rows, got {len(combined)}"
    assert combined['timestamp'].iloc[0] == 1000000, "First timestamp incorrect"
    assert combined['timestamp'].iloc[-1] == 4000000, "Last timestamp incorrect"
    assert combined['timestamp'].is_monotonic_increasing, "Timestamps not sorted"
    
    print(f"✓ Data correctly appended: {len(combined)} total records")
    print(f"✓ Timestamps sorted: {list(combined['timestamp'])}")
    
    # Cleanup
    os.remove(test_file)
    print("✓ test_append_data passed\n")


def test_duplicate_handling():
    """Test handling of duplicate timestamps"""
    print("Testing duplicate timestamp handling...")
    
    # Create initial data with some timestamps
    initial_data = pd.DataFrame([
        {'timestamp': 1000000, 'open': 100, 'high': 110, 'low': 90, 'close': 105},
        {'timestamp': 2000000, 'open': 105, 'high': 115, 'low': 95, 'close': 110},
        {'timestamp': 3000000, 'open': 110, 'high': 120, 'low': 100, 'close': 115},
    ])
    
    os.makedirs('./app/Data', exist_ok=True)
    test_file = './app/Data/test-BTC-USD.csv'
    initial_data.to_csv(test_file, index=False)
    
    # Simulate overlapping data
    OHLCData.initialize()
    new_timestamps = [2000000, 3000000, 4000000]  # 2 duplicates
    new_opens = [105, 110, 115]
    new_highs = [115, 120, 125]
    new_lows = [95, 100, 105]
    new_closes = [110, 115, 120]
    
    OHLCData.add_data('test', 'BTC-USD', 'BTC', 'USD', 
                      new_opens, new_highs, new_lows, new_closes, new_timestamps)
    
    import asyncio
    asyncio.run(DataWriter.write_data('test', 'BTC-USD', 'BTC', 'USD'))
    
    # Read combined data
    combined = pd.read_csv(test_file)
    
    # Verify duplicates were removed
    assert len(combined) == 4, f"Expected 4 unique rows, got {len(combined)}"
    assert combined['timestamp'].is_unique, "Timestamps are not unique"
    assert combined['timestamp'].is_monotonic_increasing, "Timestamps not sorted"
    
    print(f"✓ Duplicates correctly handled: {len(combined)} unique records")
    print(f"✓ Timestamps: {list(combined['timestamp'])}")
    
    # Cleanup
    os.remove(test_file)
    print("✓ test_duplicate_handling passed\n")


if __name__ == '__main__':
    print("=" * 60)
    print("Running incremental download tests")
    print("=" * 60 + "\n")
    
    try:
        test_get_last_timestamp()
        test_file_exists()
        test_append_data()
        test_duplicate_handling()
        
        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
