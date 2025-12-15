import pandas as pd
from epexspot import scrape_epexspot


def test_epexspot_2025_12_14():
    """Test EPEX SPOT scraper against known data for 2025-12-14."""

    # Expected data from manual table (2025-12-14)
    expected_data = [
        # 00 - 01 hour
        {"period": "00:00 - 00:30", "low": 12.78, "high": 44.99, "last": 18.29, "weight_avg": 26.93, "volume": 1055.9, "rpd": 26.70, "rpd_hh": 26.93},
        {"period": "00:30 - 01:00", "low": 8.91, "high": 40.78, "last": 19.09, "weight_avg": 18.90, "volume": 917.3, "rpd": 20.29, "rpd_hh": 18.90},
        # 01 - 02 hour
        {"period": "01:00 - 01:30", "low": 8.57, "high": 43.69, "last": 11.61, "weight_avg": 17.49, "volume": 1547.3, "rpd": 18.58, "rpd_hh": 17.49},
        {"period": "01:30 - 02:00", "low": 4.52, "high": 34.84, "last": 22.00, "weight_avg": 18.80, "volume": 1324.8, "rpd": 19.85, "rpd_hh": 18.80},
        # 02 - 03 hour
        {"period": "02:00 - 02:30", "low": 8.97, "high": 55.00, "last": 27.00, "weight_avg": 20.38, "volume": 1363.5, "rpd": 20.73, "rpd_hh": 20.38},
        {"period": "02:30 - 03:00", "low": 11.66, "high": 56.09, "last": 40.00, "weight_avg": 21.89, "volume": 1596.0, "rpd": 22.00, "rpd_hh": 21.89},
        # 03 - 04 hour
        {"period": "03:00 - 03:30", "low": 13.89, "high": 42.13, "last": 24.01, "weight_avg": 22.51, "volume": 1364.5, "rpd": 22.53, "rpd_hh": 22.51},
        {"period": "03:30 - 04:00", "low": 4.81, "high": 40.00, "last": 17.41, "weight_avg": 19.42, "volume": 1407.9, "rpd": 19.91, "rpd_hh": 19.42},
        # 04 - 05 hour
        {"period": "04:00 - 04:30", "low": 5.03, "high": 32.90, "last": 8.93, "weight_avg": 17.26, "volume": 1290.7, "rpd": 16.85, "rpd_hh": 17.26},
        {"period": "04:30 - 05:00", "low": -2.25, "high": 26.99, "last": 4.00, "weight_avg": 11.14, "volume": 1152.2, "rpd": 11.83, "rpd_hh": 11.14},
        # 05 - 06 hour
        {"period": "05:00 - 05:30", "low": 5.00, "high": 23.89, "last": 21.18, "weight_avg": 13.30, "volume": 1349.6, "rpd": 13.55, "rpd_hh": 13.30},
        {"period": "05:30 - 06:00", "low": -45.99, "high": 20.00, "last": 2.53, "weight_avg": 10.52, "volume": 1450.7, "rpd": 11.19, "rpd_hh": 10.52},
        # 06 - 07 hour
        {"period": "06:00 - 06:30", "low": 1.90, "high": 37.82, "last": 21.70, "weight_avg": 15.44, "volume": 1341.2, "rpd": 15.62, "rpd_hh": 15.44},
        {"period": "06:30 - 07:00", "low": 2.69, "high": 37.23, "last": 15.54, "weight_avg": 19.29, "volume": 1464.5, "rpd": 18.81, "rpd_hh": 19.29},
        # 07 - 08 hour
        {"period": "07:00 - 07:30", "low": -24.30, "high": 40.89, "last": 21.81, "weight_avg": 23.17, "volume": 1551.2, "rpd": 22.09, "rpd_hh": 23.17},
        {"period": "07:30 - 08:00", "low": 12.44, "high": 54.99, "last": 50.00, "weight_avg": 32.89, "volume": 1608.8, "rpd": 30.33, "rpd_hh": 32.89},
        # 08 - 09 hour
        {"period": "08:00 - 08:30", "low": -59.10, "high": 59.90, "last": 52.86, "weight_avg": 40.41, "volume": 1775.6, "rpd": 41.49, "rpd_hh": 40.41},
        {"period": "08:30 - 09:00", "low": -38.00, "high": 72.89, "last": 72.50, "weight_avg": 53.05, "volume": 1543.4, "rpd": 52.48, "rpd_hh": 53.05},
        # 09 - 10 hour
        {"period": "09:00 - 09:30", "low": 15.01, "high": 68.68, "last": 58.30, "weight_avg": 51.74, "volume": 1743.2, "rpd": 51.39, "rpd_hh": 51.74},
        {"period": "09:30 - 10:00", "low": 26.01, "high": 82.54, "last": 79.00, "weight_avg": 69.47, "volume": 1741.3, "rpd": 66.85, "rpd_hh": 69.47},
        # 10 - 11 hour
        {"period": "10:00 - 10:30", "low": 10.01, "high": 83.00, "last": 70.62, "weight_avg": 63.97, "volume": 1581.1, "rpd": 62.15, "rpd_hh": 63.97},
        {"period": "10:30 - 11:00", "low": 42.00, "high": 85.09, "last": 79.00, "weight_avg": 73.42, "volume": 1706.6, "rpd": 69.61, "rpd_hh": 73.42},
        # 11 - 12 hour
        {"period": "11:00 - 11:30", "low": 35.10, "high": 72.03, "last": 55.15, "weight_avg": 60.40, "volume": 1891.8, "rpd": 59.55, "rpd_hh": 60.40},
        {"period": "11:30 - 12:00", "low": 26.59, "high": 64.92, "last": 29.98, "weight_avg": 49.40, "volume": 1494.5, "rpd": 51.08, "rpd_hh": 49.40},
        # 12 - 13 hour
        {"period": "12:00 - 12:30", "low": 18.20, "high": 67.19, "last": 29.00, "weight_avg": 42.99, "volume": 1661.7, "rpd": 44.36, "rpd_hh": 42.99},
        {"period": "12:30 - 13:00", "low": 19.19, "high": 59.44, "last": 37.00, "weight_avg": 38.09, "volume": 1532.4, "rpd": 41.01, "rpd_hh": 38.09},
        # 13 - 14 hour
        {"period": "13:00 - 13:30", "low": 27.36, "high": 80.97, "last": 69.84, "weight_avg": 51.65, "volume": 2896.3, "rpd": 50.94, "rpd_hh": 51.65},
        {"period": "13:30 - 14:00", "low": 35.09, "high": 75.23, "last": 73.71, "weight_avg": 50.91, "volume": 2438.3, "rpd": 50.25, "rpd_hh": 50.91},
        # 14 - 15 hour
        {"period": "14:00 - 14:30", "low": 35.44, "high": 74.10, "last": 68.00, "weight_avg": 55.66, "volume": 2248.2, "rpd": 53.88, "rpd_hh": 55.66},
        {"period": "14:30 - 15:00", "low": 40.73, "high": 71.95, "last": 50.00, "weight_avg": 54.63, "volume": 1821.1, "rpd": 52.95, "rpd_hh": 54.63},
        # 15 - 16 hour
        {"period": "15:00 - 15:30", "low": 17.71, "high": 73.79, "last": 63.05, "weight_avg": 59.00, "volume": 2075.2, "rpd": 56.02, "rpd_hh": 59.00},
        {"period": "15:30 - 16:00", "low": 38.37, "high": 73.77, "last": 44.00, "weight_avg": 60.86, "volume": 1758.9, "rpd": 56.86, "rpd_hh": 60.86},
        # 16 - 17 hour
        {"period": "16:00 - 16:30", "low": 37.25, "high": 68.63, "last": 47.05, "weight_avg": 59.75, "volume": 1587.1, "rpd": 62.08, "rpd_hh": 59.75},
        {"period": "16:30 - 17:00", "low": 57.73, "high": 75.99, "last": 72.00, "weight_avg": 68.62, "volume": 1186.7, "rpd": 69.22, "rpd_hh": 68.62},
        # 17 - 18 hour
        {"period": "17:00 - 17:30", "low": 62.00, "high": 78.36, "last": 74.95, "weight_avg": 71.65, "volume": 1537.5, "rpd": 71.49, "rpd_hh": 71.65},
        {"period": "17:30 - 18:00", "low": 73.00, "high": 84.36, "last": 82.00, "weight_avg": 79.36, "volume": 1505.2, "rpd": 77.52, "rpd_hh": 79.36},
        # 18 - 19 hour
        {"period": "18:00 - 18:30", "low": 61.76, "high": 91.77, "last": 87.96, "weight_avg": 80.49, "volume": 1581.5, "rpd": 79.72, "rpd_hh": 80.49},
        {"period": "18:30 - 19:00", "low": 72.48, "high": 94.00, "last": 93.00, "weight_avg": 82.80, "volume": 1707.5, "rpd": 81.53, "rpd_hh": 82.80},
        # 19 - 20 hour
        {"period": "19:00 - 19:30", "low": 74.76, "high": 93.88, "last": 92.00, "weight_avg": 82.84, "volume": 1635.2, "rpd": 81.51, "rpd_hh": 82.84},
        {"period": "19:30 - 20:00", "low": 69.03, "high": 88.00, "last": 77.12, "weight_avg": 75.97, "volume": 1337.4, "rpd": 76.39, "rpd_hh": 75.97},
        # 20 - 21 hour
        {"period": "20:00 - 20:30", "low": 56.10, "high": 92.00, "last": 83.15, "weight_avg": 76.83, "volume": 1322.6, "rpd": 74.46, "rpd_hh": 76.83},
        {"period": "20:30 - 21:00", "low": 46.77, "high": 79.92, "last": 58.40, "weight_avg": 68.87, "volume": 1314.1, "rpd": 68.40, "rpd_hh": 68.87},
        # 21 - 22 hour
        {"period": "21:00 - 21:30", "low": 52.92, "high": 75.40, "last": 66.00, "weight_avg": 67.82, "volume": 1659.7, "rpd": 67.65, "rpd_hh": 67.82},
        {"period": "21:30 - 22:00", "low": 19.78, "high": 72.01, "last": 42.00, "weight_avg": 54.58, "volume": 1415.9, "rpd": 57.40, "rpd_hh": 54.58},
        # 22 - 23 hour
        {"period": "22:00 - 22:30", "low": 45.80, "high": 88.10, "last": 68.57, "weight_avg": 68.69, "volume": 1902.0, "rpd": 67.69, "rpd_hh": 68.69},
        {"period": "22:30 - 23:00", "low": 33.36, "high": 71.00, "last": 47.00, "weight_avg": 54.37, "volume": 1478.2, "rpd": 56.53, "rpd_hh": 54.37},
        # 23 - 24 hour
        {"period": "23:00 - 23:30", "low": 44.02, "high": 84.99, "last": 77.48, "weight_avg": 60.65, "volume": 1820.5, "rpd": 61.22, "rpd_hh": 60.65},
        {"period": "23:30 - 24:00", "low": 46.29, "high": 94.76, "last": 90.00, "weight_avg": 64.41, "volume": 1961.5, "rpd": 64.24, "rpd_hh": 64.41},
    ]

    # Scrape the data
    df = scrape_epexspot('2025-12-14')

    # Verify we got data
    assert df is not None, "Failed to scrape data"

    # Verify we have 48 periods
    assert len(df) == 48, f"Expected 48 periods, got {len(df)}"

    # Verify required columns exist
    required_columns = ['period', 'low_price', 'high_price', 'last_price',
                       'weight_avg_price', 'buy_volume', 'sell_volume', 'volume', 'rpd', 'rpd_hh']
    for col in required_columns:
        assert col in df.columns, f"Missing required column: {col}"

    print("✓ All required columns present (including RPD columns)")

    # Verify each row matches expected data
    for i, expected in enumerate(expected_data):
        actual_row = df.iloc[i]

        # Check period
        assert actual_row['period'] == expected['period'], \
            f"Row {i}: Period mismatch. Expected '{expected['period']}', got '{actual_row['period']}'"

        # Check prices (allow small floating point differences)
        assert abs(actual_row['low_price'] - expected['low']) < 0.01, \
            f"Row {i} ({expected['period']}): Low price mismatch. Expected {expected['low']}, got {actual_row['low_price']}"

        assert abs(actual_row['high_price'] - expected['high']) < 0.01, \
            f"Row {i} ({expected['period']}): High price mismatch. Expected {expected['high']}, got {actual_row['high_price']}"

        assert abs(actual_row['last_price'] - expected['last']) < 0.01, \
            f"Row {i} ({expected['period']}): Last price mismatch. Expected {expected['last']}, got {actual_row['last_price']}"

        assert abs(actual_row['weight_avg_price'] - expected['weight_avg']) < 0.01, \
            f"Row {i} ({expected['period']}): Weight avg price mismatch. Expected {expected['weight_avg']}, got {actual_row['weight_avg_price']}"

        # Check volume
        assert abs(actual_row['volume'] - expected['volume']) < 0.1, \
            f"Row {i} ({expected['period']}): Volume mismatch. Expected {expected['volume']}, got {actual_row['volume']}"

        # Check RPD columns
        assert abs(actual_row['rpd'] - expected['rpd']) < 0.01, \
            f"Row {i} ({expected['period']}): RPD mismatch. Expected {expected['rpd']}, got {actual_row['rpd']}"

        assert abs(actual_row['rpd_hh'] - expected['rpd_hh']) < 0.01, \
            f"Row {i} ({expected['period']}): RPD HH mismatch. Expected {expected['rpd_hh']}, got {actual_row['rpd_hh']}"

    print("✓ All 48 periods validated successfully!")
    print(f"✓ Total volume: {df['volume'].sum():.1f} MWh")
    print(f"✓ Avg weight price: {df['weight_avg_price'].mean():.2f} £/MWh")
    print(f"✓ Price range: {df['weight_avg_price'].min():.2f} - {df['weight_avg_price'].max():.2f} £/MWh")


def test_epexspot_2025_12_15():
    """Test EPEX SPOT scraper for 2025-12-15.

    Note: EPEX SPOT continuous market data updates throughout the day,
    so we validate structure and data types rather than exact values.
    """

    # Sample of expected data structure (values may differ as market is continuous)
    expected_data = [
        # 00 - 01 hour
        {"period": "00:00 - 00:30"}, {"period": "00:30 - 01:00"},
        # 01 - 02 hour
        {"period": "01:00 - 01:30"}, {"period": "01:30 - 02:00"},
        # 02 - 03 hour
        {"period": "02:00 - 02:30"}, {"period": "02:30 - 03:00"},
        # 03 - 04 hour
        {"period": "03:00 - 03:30"}, {"period": "03:30 - 04:00"},
        # 04 - 05 hour
        {"period": "04:00 - 04:30"}, {"period": "04:30 - 05:00"},
        # 05 - 06 hour
        {"period": "05:00 - 05:30"}, {"period": "05:30 - 06:00"},
        # 06 - 07 hour
        {"period": "06:00 - 06:30"}, {"period": "06:30 - 07:00"},
        # 07 - 08 hour
        {"period": "07:00 - 07:30"}, {"period": "07:30 - 08:00"},
        # 08 - 09 hour
        {"period": "08:00 - 08:30"}, {"period": "08:30 - 09:00"},
        # 09 - 10 hour
        {"period": "09:00 - 09:30"}, {"period": "09:30 - 10:00"},
        # 10 - 11 hour
        {"period": "10:00 - 10:30"}, {"period": "10:30 - 11:00"},
        # 11 - 12 hour
        {"period": "11:00 - 11:30"}, {"period": "11:30 - 12:00"},
        # 12 - 13 hour
        {"period": "12:00 - 12:30"}, {"period": "12:30 - 13:00"},
        # 13 - 14 hour
        {"period": "13:00 - 13:30"}, {"period": "13:30 - 14:00"},
        # 14 - 15 hour
        {"period": "14:00 - 14:30"}, {"period": "14:30 - 15:00"},
        # 15 - 16 hour
        {"period": "15:00 - 15:30"}, {"period": "15:30 - 16:00"},
        # 16 - 17 hour
        {"period": "16:00 - 16:30"}, {"period": "16:30 - 17:00"},
        # 17 - 18 hour
        {"period": "17:00 - 17:30"}, {"period": "17:30 - 18:00"},
        # 18 - 19 hour
        {"period": "18:00 - 18:30"}, {"period": "18:30 - 19:00"},
        # 19 - 20 hour
        {"period": "19:00 - 19:30"}, {"period": "19:30 - 20:00"},
        # 20 - 21 hour
        {"period": "20:00 - 20:30"}, {"period": "20:30 - 21:00"},
        # 21 - 22 hour
        {"period": "21:00 - 21:30"}, {"period": "21:30 - 22:00"},
        # 22 - 23 hour
        {"period": "22:00 - 22:30"}, {"period": "22:30 - 23:00"},
        # 23 - 24 hour
        {"period": "23:00 - 23:30"}, {"period": "23:30 - 24:00"},
    ]

    # Scrape the data
    df = scrape_epexspot('2025-12-15')

    # Verify we got data
    assert df is not None, "Failed to scrape data"

    # Verify we have 48 periods
    assert len(df) == 48, f"Expected 48 periods, got {len(df)}"

    # Verify required columns exist
    required_columns = ['period', 'low_price', 'high_price', 'last_price',
                       'weight_avg_price', 'buy_volume', 'sell_volume', 'volume']
    for col in required_columns:
        assert col in df.columns, f"Missing required column: {col}"

    print("✓ All required columns present")

    # Verify each row has correct period format and valid data
    for i in range(48):
        actual_row = df.iloc[i]
        expected = expected_data[i]

        # Check period matches expected format
        assert actual_row['period'] == expected['period'], \
            f"Row {i}: Period mismatch. Expected '{expected['period']}', got '{actual_row['period']}'"

        # Check all numeric values are present and valid
        assert actual_row['high_price'] >= actual_row['low_price'], \
            f"Row {i} ({expected['period']}): High price ({actual_row['high_price']}) < Low price ({actual_row['low_price']})"

        assert actual_row['volume'] > 0, \
            f"Row {i} ({expected['period']}): Invalid volume {actual_row['volume']}"

        # Verify volumes match (buy = sell = total in continuous market)
        assert actual_row['buy_volume'] == actual_row['sell_volume'] == actual_row['volume'], \
            f"Row {i} ({expected['period']}): Volume mismatch - buy:{actual_row['buy_volume']}, sell:{actual_row['sell_volume']}, total:{actual_row['volume']}"

    print("✓ All 48 periods validated successfully!")
    print(f"✓ All periods have correct format and valid data")
    print(f"✓ Total volume: {df['volume'].sum():.1f} MWh")
    print(f"✓ Avg weight price: {df['weight_avg_price'].mean():.2f} £/MWh")
    print(f"✓ Price range: {df['weight_avg_price'].min():.2f} - {df['weight_avg_price'].max():.2f} £/MWh")


if __name__ == "__main__":
    print("="*60)
    print("Testing EPEX SPOT scraper for 2025-12-14")
    print("="*60)
    test_epexspot_2025_12_14()

    print("\n" + "="*60)
    print("Testing EPEX SPOT scraper for 2025-12-15")
    print("="*60)
    test_epexspot_2025_12_15()
