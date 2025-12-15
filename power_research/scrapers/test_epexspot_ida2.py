import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from epexspot import scrape_epexspot_auction


def test_epexspot_ida2_2025_12_14():
    """Test EPEX SPOT GB-IDA2 auction scraper against known data for 2025-12-14."""

    # Expected data for all 24 periods (12:00-24:00)
    expected_data = [
        {"period": "12:00 - 12:30", "buy_volume": 135.0, "sell_volume": 42.3, "volume": 135.0, "price": 52.40},
        {"period": "12:30 - 13:00", "buy_volume": 127.5, "sell_volume": 50.0, "volume": 127.5, "price": 52.30},
        {"period": "13:00 - 13:30", "buy_volume": 156.6, "sell_volume": 24.7, "volume": 156.6, "price": 49.31},
        {"period": "13:30 - 14:00", "buy_volume": 180.2, "sell_volume": 23.5, "volume": 180.2, "price": 49.31},
        {"period": "14:00 - 14:30", "buy_volume": 208.8, "sell_volume": 22.9, "volume": 208.8, "price": 49.86},
        {"period": "14:30 - 15:00", "buy_volume": 217.9, "sell_volume": 19.4, "volume": 217.9, "price": 50.00},
        {"period": "15:00 - 15:30", "buy_volume": 202.5, "sell_volume": 51.1, "volume": 202.5, "price": 51.00},
        {"period": "15:30 - 16:00", "buy_volume": 206.6, "sell_volume": 41.7, "volume": 206.6, "price": 56.00},
        {"period": "16:00 - 16:30", "buy_volume": 231.4, "sell_volume": 62.3, "volume": 231.4, "price": 52.00},
        {"period": "16:30 - 17:00", "buy_volume": 219.8, "sell_volume": 32.2, "volume": 219.8, "price": 68.94},
        {"period": "17:00 - 17:30", "buy_volume": 238.5, "sell_volume": 27.0, "volume": 238.5, "price": 68.00},
        {"period": "17:30 - 18:00", "buy_volume": 277.9, "sell_volume": 67.7, "volume": 277.9, "price": 79.60},
        {"period": "18:00 - 18:30", "buy_volume": 194.2, "sell_volume": 66.0, "volume": 194.2, "price": 80.00},
        {"period": "18:30 - 19:00", "buy_volume": 212.2, "sell_volume": 88.8, "volume": 212.2, "price": 82.80},
        {"period": "19:00 - 19:30", "buy_volume": 164.2, "sell_volume": 116.0, "volume": 164.2, "price": 84.00},
        {"period": "19:30 - 20:00", "buy_volume": 118.7, "sell_volume": 103.3, "volume": 118.7, "price": 80.06},
        {"period": "20:00 - 20:30", "buy_volume": 161.8, "sell_volume": 162.0, "volume": 162.0, "price": 73.33},
        {"period": "20:30 - 21:00", "buy_volume": 170.8, "sell_volume": 191.0, "volume": 191.0, "price": 72.58},
        {"period": "21:00 - 21:30", "buy_volume": 195.1, "sell_volume": 200.3, "volume": 200.3, "price": 76.00},
        {"period": "21:30 - 22:00", "buy_volume": 136.7, "sell_volume": 202.7, "volume": 202.7, "price": 72.42},
        {"period": "22:00 - 22:30", "buy_volume": 130.6, "sell_volume": 257.2, "volume": 257.2, "price": 76.00},
        {"period": "22:30 - 23:00", "buy_volume": 85.8, "sell_volume": 222.8, "volume": 222.8, "price": 68.00},
        {"period": "23:00 - 23:30", "buy_volume": 96.2, "sell_volume": 246.7, "volume": 246.7, "price": 71.50},
        {"period": "23:30 - 24:00", "buy_volume": 41.6, "sell_volume": 200.6, "volume": 200.6, "price": 62.00},
    ]

    # Expected summary data
    expected_baseload = 65.73
    # Note: Peakload is not published for GB-IDA2

    print("Testing EPEX SPOT GB-IDA2 auction scraper for 2025-12-14...")
    df = scrape_epexspot_auction('2025-12-14', auction='GB-IDA2')

    if df is None:
        print("❌ FAILED: scrape_epexspot_auction returned None")
        return False

    # Check number of periods
    if len(df) != 24:
        print(f"❌ FAILED: Expected 24 periods, got {len(df)}")
        return False
    print(f"✓ Correct number of periods: {len(df)}")

    # Check columns
    expected_columns = {'period', 'buy_volume', 'sell_volume', 'volume', 'price'}
    actual_columns = set(df.columns)
    if actual_columns != expected_columns:
        print(f"❌ FAILED: Column mismatch. Expected {expected_columns}, got {actual_columns}")
        return False
    print(f"✓ Correct columns: {', '.join(df.columns)}")

    # Check summary data (baseload price)
    if not hasattr(df, 'attrs'):
        print("❌ FAILED: DataFrame missing 'attrs' attribute")
        return False

    if 'baseload_price' not in df.attrs:
        print("❌ FAILED: Missing baseload_price in attrs")
        return False

    if abs(df.attrs['baseload_price'] - expected_baseload) > 0.01:
        print(f"❌ FAILED: Baseload price mismatch. Expected {expected_baseload}, got {df.attrs['baseload_price']}")
        return False
    print(f"✓ Correct baseload price: {df.attrs['baseload_price']}")

    # Peakload should not be present for GB-IDA2
    if 'peakload_price' in df.attrs:
        print(f"⚠ Warning: Peakload price found (not typically published for IDA2): {df.attrs['peakload_price']}")

    # Check each period's data
    errors = []
    for i, expected in enumerate(expected_data):
        actual = df.iloc[i]

        # Check period
        if actual['period'] != expected['period']:
            errors.append(f"Period {i}: Expected period '{expected['period']}', got '{actual['period']}'")

        # Check volumes and price (allow 0.01 tolerance for floating point)
        for field in ['buy_volume', 'sell_volume', 'volume', 'price']:
            if abs(actual[field] - expected[field]) > 0.01:
                errors.append(f"Period {expected['period']}: {field} mismatch. Expected {expected[field]}, got {actual[field]}")

    if errors:
        print(f"❌ FAILED: {len(errors)} data validation errors:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
        return False

    print("✓ All 24 periods validated successfully")

    # Show summary statistics
    print("\n" + "="*60)
    print("VALIDATION SUMMARY:")
    print("="*60)
    print(f"Date: 2025-12-14")
    print(f"Auction: GB-IDA2")
    print(f"Periods: {len(df)} (12:00-24:00)")
    print(f"Baseload Price: {df.attrs['baseload_price']:.2f} £/MWh")
    print(f"Peakload Price: Not published for IDA2")
    print(f"Price Range: {df['price'].min():.2f} to {df['price'].max():.2f} £/MWh")
    print(f"Total Volume: {df['volume'].sum():.1f} MWh")
    print("="*60)
    print("✅ ALL TESTS PASSED!")

    return True


if __name__ == "__main__":
    success = test_epexspot_ida2_2025_12_14()
    sys.exit(0 if success else 1)
