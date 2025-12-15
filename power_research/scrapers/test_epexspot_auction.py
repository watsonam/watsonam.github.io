import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from epexspot import scrape_epexspot_auction


def test_epexspot_auction_2025_12_14():
    """Test EPEX SPOT auction scraper against known data for 2025-12-14."""

    # Expected data for all 48 periods
    expected_data = [
        {"period": "00:00 - 00:30", "buy_volume": 486.0, "sell_volume": 132.2, "volume": 486.0, "price": 40.35},
        {"period": "00:30 - 01:00", "buy_volume": 497.2, "sell_volume": 179.1, "volume": 497.2, "price": 31.43},
        {"period": "01:00 - 01:30", "buy_volume": 529.1, "sell_volume": 254.4, "volume": 529.1, "price": 5.80},
        {"period": "01:30 - 02:00", "buy_volume": 565.7, "sell_volume": 204.3, "volume": 565.7, "price": 16.00},
        {"period": "02:00 - 02:30", "buy_volume": 447.4, "sell_volume": 172.8, "volume": 447.4, "price": 18.45},
        {"period": "02:30 - 03:00", "buy_volume": 505.9, "sell_volume": 224.3, "volume": 505.9, "price": 9.89},
        {"period": "03:00 - 03:30", "buy_volume": 462.1, "sell_volume": 180.6, "volume": 462.1, "price": 16.00},
        {"period": "03:30 - 04:00", "buy_volume": 511.9, "sell_volume": 221.1, "volume": 511.9, "price": 10.77},
        {"period": "04:00 - 04:30", "buy_volume": 485.3, "sell_volume": 191.9, "volume": 485.3, "price": 8.34},
        {"period": "04:30 - 05:00", "buy_volume": 523.6, "sell_volume": 192.2, "volume": 523.6, "price": 9.21},
        {"period": "05:00 - 05:30", "buy_volume": 531.5, "sell_volume": 195.6, "volume": 531.5, "price": 15.36},
        {"period": "05:30 - 06:00", "buy_volume": 518.8, "sell_volume": 193.0, "volume": 518.8, "price": 12.00},
        {"period": "06:00 - 06:30", "buy_volume": 532.9, "sell_volume": 220.7, "volume": 532.9, "price": 9.72},
        {"period": "06:30 - 07:00", "buy_volume": 460.4, "sell_volume": 206.9, "volume": 460.4, "price": 4.00},
        {"period": "07:00 - 07:30", "buy_volume": 509.7, "sell_volume": 172.3, "volume": 509.7, "price": -1.04},
        {"period": "07:30 - 08:00", "buy_volume": 556.8, "sell_volume": 173.6, "volume": 556.8, "price": 4.00},
        {"period": "08:00 - 08:30", "buy_volume": 549.6, "sell_volume": 204.6, "volume": 549.6, "price": -1.05},
        {"period": "08:30 - 09:00", "buy_volume": 556.2, "sell_volume": 156.9, "volume": 556.2, "price": 20.00},
        {"period": "09:00 - 09:30", "buy_volume": 550.4, "sell_volume": 157.5, "volume": 550.4, "price": 24.24},
        {"period": "09:30 - 10:00", "buy_volume": 604.5, "sell_volume": 155.6, "volume": 604.5, "price": 53.00},
        {"period": "10:00 - 10:30", "buy_volume": 546.9, "sell_volume": 241.1, "volume": 546.9, "price": 48.00},
        {"period": "10:30 - 11:00", "buy_volume": 517.6, "sell_volume": 245.0, "volume": 517.6, "price": 52.06},
        {"period": "11:00 - 11:30", "buy_volume": 405.2, "sell_volume": 217.5, "volume": 405.2, "price": 49.29},
        {"period": "11:30 - 12:00", "buy_volume": 379.6, "sell_volume": 228.7, "volume": 379.6, "price": 49.31},
        {"period": "12:00 - 12:30", "buy_volume": 437.1, "sell_volume": 242.4, "volume": 437.1, "price": 50.41},
        {"period": "12:30 - 13:00", "buy_volume": 427.8, "sell_volume": 275.6, "volume": 427.8, "price": 50.26},
        {"period": "13:00 - 13:30", "buy_volume": 315.9, "sell_volume": 287.9, "volume": 315.9, "price": 47.04},
        {"period": "13:30 - 14:00", "buy_volume": 285.4, "sell_volume": 282.0, "volume": 285.4, "price": 48.95},
        {"period": "14:00 - 14:30", "buy_volume": 384.7, "sell_volume": 274.5, "volume": 384.7, "price": 52.00},
        {"period": "14:30 - 15:00", "buy_volume": 355.9, "sell_volume": 266.1, "volume": 355.9, "price": 53.01},
        {"period": "15:00 - 15:30", "buy_volume": 385.7, "sell_volume": 269.9, "volume": 385.7, "price": 59.24},
        {"period": "15:30 - 16:00", "buy_volume": 401.7, "sell_volume": 337.9, "volume": 401.7, "price": 61.73},
        {"period": "16:00 - 16:30", "buy_volume": 430.1, "sell_volume": 264.7, "volume": 430.1, "price": 56.00},
        {"period": "16:30 - 17:00", "buy_volume": 341.5, "sell_volume": 239.0, "volume": 341.5, "price": 68.00},
        {"period": "17:00 - 17:30", "buy_volume": 391.4, "sell_volume": 242.0, "volume": 391.4, "price": 68.10},
        {"period": "17:30 - 18:00", "buy_volume": 292.0, "sell_volume": 290.8, "volume": 292.0, "price": 76.70},
        {"period": "18:00 - 18:30", "buy_volume": 627.4, "sell_volume": 444.9, "volume": 627.4, "price": 75.30},
        {"period": "18:30 - 19:00", "buy_volume": 486.5, "sell_volume": 418.1, "volume": 486.5, "price": 76.00},
        {"period": "19:00 - 19:30", "buy_volume": 389.2, "sell_volume": 415.3, "volume": 415.3, "price": 75.60},
        {"period": "19:30 - 20:00", "buy_volume": 306.1, "sell_volume": 475.3, "volume": 475.3, "price": 73.99},
        {"period": "20:00 - 20:30", "buy_volume": 222.3, "sell_volume": 561.8, "volume": 561.8, "price": 70.00},
        {"period": "20:30 - 21:00", "buy_volume": 176.9, "sell_volume": 615.4, "volume": 615.4, "price": 62.80},
        {"period": "21:00 - 21:30", "buy_volume": 190.2, "sell_volume": 742.5, "volume": 742.5, "price": 68.00},
        {"period": "21:30 - 22:00", "buy_volume": 178.6, "sell_volume": 746.4, "volume": 746.4, "price": 62.99},
        {"period": "22:00 - 22:30", "buy_volume": 178.3, "sell_volume": 740.8, "volume": 740.8, "price": 68.09},
        {"period": "22:30 - 23:00", "buy_volume": 153.0, "sell_volume": 779.4, "volume": 779.4, "price": 52.04},
        {"period": "23:00 - 23:30", "buy_volume": 234.9, "sell_volume": 803.1, "volume": 803.1, "price": 56.54},
        {"period": "23:30 - 24:00", "buy_volume": 303.8, "sell_volume": 891.2, "volume": 891.2, "price": 45.00},
    ]

    # Expected summary data
    expected_baseload = 41.31
    expected_peakload = 53.63

    print("Testing EPEX SPOT auction scraper for 2025-12-14...")
    df = scrape_epexspot_auction('2025-12-14', auction='GB-IDA1')

    if df is None:
        print("❌ FAILED: scrape_epexspot_auction returned None")
        return False

    # Check number of periods
    if len(df) != 48:
        print(f"❌ FAILED: Expected 48 periods, got {len(df)}")
        return False
    print(f"✓ Correct number of periods: {len(df)}")

    # Check columns
    expected_columns = {'period', 'buy_volume', 'sell_volume', 'volume', 'price'}
    actual_columns = set(df.columns)
    if actual_columns != expected_columns:
        print(f"❌ FAILED: Column mismatch. Expected {expected_columns}, got {actual_columns}")
        return False
    print(f"✓ Correct columns: {', '.join(df.columns)}")

    # Check summary data (baseload and peakload prices)
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

    if 'peakload_price' not in df.attrs:
        print("❌ FAILED: Missing peakload_price in attrs")
        return False

    if abs(df.attrs['peakload_price'] - expected_peakload) > 0.01:
        print(f"❌ FAILED: Peakload price mismatch. Expected {expected_peakload}, got {df.attrs['peakload_price']}")
        return False
    print(f"✓ Correct peakload price: {df.attrs['peakload_price']}")

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

    print("✓ All 48 periods validated successfully")

    # Show summary statistics
    print("\n" + "="*60)
    print("VALIDATION SUMMARY:")
    print("="*60)
    print(f"Date: 2025-12-14")
    print(f"Auction: GB-IDA1")
    print(f"Periods: {len(df)}")
    print(f"Baseload Price: {df.attrs['baseload_price']:.2f} £/MWh")
    print(f"Peakload Price: {df.attrs['peakload_price']:.2f} £/MWh")
    print(f"Price Range: {df['price'].min():.2f} to {df['price'].max():.2f} £/MWh")
    print(f"Total Volume: {df['volume'].sum():.1f} MWh")
    print("="*60)
    print("✅ ALL TESTS PASSED!")

    return True


if __name__ == "__main__":
    success = test_epexspot_auction_2025_12_14()
    sys.exit(0 if success else 1)
