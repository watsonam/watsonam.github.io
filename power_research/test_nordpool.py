import pandas as pd
from scrapers.nordpool import scrape_nordpool, scrape_nordpool_volumes


def test_nordpool_17_10_2025():
    expected_data = [
        ("23:00 - 00:00", 78.20),
        ("00:00 - 01:00", 75.98),
        ("01:00 - 02:00", 76.00),
        ("02:00 - 03:00", 74.55),
        ("03:00 - 04:00", 73.79),
        ("04:00 - 05:00", 73.35),
        ("05:00 - 06:00", 87.85),
        ("06:00 - 07:00", 94.28),
        ("07:00 - 08:00", 113.24),
        ("08:00 - 09:00", 109.94),
        ("09:00 - 10:00", 99.00),
        ("10:00 - 11:00", 87.95),
        ("11:00 - 12:00", 83.85),
        ("12:00 - 13:00", 77.35),
        ("13:00 - 14:00", 75.66),
        ("14:00 - 15:00", 75.57),
        ("15:00 - 16:00", 82.74),
        ("16:00 - 17:00", 98.47),
        ("17:00 - 18:00", 115.09),
        ("18:00 - 19:00", 124.50),
        ("19:00 - 20:00", 106.00),
        ("20:00 - 21:00", 88.34),
        ("21:00 - 22:00", 86.15),
        ("22:00 - 23:00", 78.14)
    ]

    df = scrape_nordpool('2025-10-17')

    assert df is not None, "Should return data for 2025-10-17"
    assert len(df) == 24, f"Should have 24 rows, got {len(df)}"

    expected_df = pd.DataFrame(expected_data, columns=['period', 'price'])

    for i, (expected_period, expected_price) in enumerate(expected_data):
        actual_period = df.iloc[i]['period']
        actual_price = df.iloc[i]['price']

        assert actual_period == expected_period, f"Row {i}: expected period '{expected_period}', got '{actual_period}'"
        assert abs(actual_price - expected_price) < 0.01, f"Row {i}: expected price {expected_price}, got {actual_price}"

    min_price = df['price'].min()
    max_price = df['price'].max()
    avg_price = df['price'].mean()

    assert abs(min_price - 73.35) < 0.01, f"Min should be 73.35, got {min_price}"
    assert abs(max_price - 124.50) < 0.01, f"Max should be 124.50, got {max_price}"
    assert abs(avg_price - 89.00) < 0.01, f"Average should be 89.00, got {avg_price}"

    print("✓ All tests passed for 2025-10-17 data")


def test_nordpool_16_10_2025():
    expected_data = [
        ("23:00 - 00:00", 79.59),
        ("00:00 - 01:00", 75.01),
        ("01:00 - 02:00", 73.54),
        ("02:00 - 03:00", 72.02),
        ("03:00 - 04:00", 71.07),
        ("04:00 - 05:00", 72.25),
        ("05:00 - 06:00", 76.08),
        ("06:00 - 07:00", 92.47),
        ("07:00 - 08:00", 108.84),
        ("08:00 - 09:00", 106.19),
        ("09:00 - 10:00", 99.10),
        ("10:00 - 11:00", 81.42),
        ("11:00 - 12:00", 76.71),
        ("12:00 - 13:00", 77.98),
        ("13:00 - 14:00", 77.79),
        ("14:00 - 15:00", 75.22),
        ("15:00 - 16:00", 84.96),
        ("16:00 - 17:00", 106.07),
        ("17:00 - 18:00", 126.64),
        ("18:00 - 19:00", 140.42),
        ("19:00 - 20:00", 122.38),
        ("20:00 - 21:00", 107.56),
        ("21:00 - 22:00", 87.49),
        ("22:00 - 23:00", 77.18)
    ]

    df = scrape_nordpool('2025-10-16')

    assert df is not None, "Should return data for 2025-10-16"
    assert len(df) == 24, f"Should have 24 rows, got {len(df)}"

    for i, (expected_period, expected_price) in enumerate(expected_data):
        actual_period = df.iloc[i]['period']
        actual_price = df.iloc[i]['price']

        assert actual_period == expected_period, f"Row {i}: expected period '{expected_period}', got '{actual_period}'"
        assert abs(actual_price - expected_price) < 0.01, f"Row {i}: expected price {expected_price}, got {actual_price}"

    min_price = df['price'].min()
    max_price = df['price'].max()
    avg_price = df['price'].mean()

    assert abs(min_price - 71.07) < 0.01, f"Min should be 71.07, got {min_price}"
    assert abs(max_price - 140.42) < 0.01, f"Max should be 140.42, got {max_price}"
    assert abs(avg_price - 90.33) < 0.01, f"Average should be 90.33, got {avg_price:.2f}"

    print("✓ All tests passed for 2025-10-16 data")


def test_nordpool_volumes_20_10_2025():
    expected_data = [
        ("23:00 - 00:00", 11777.2, 11092.2),
        ("00:00 - 01:00", 11938.7, 11239.4),
        ("01:00 - 02:00", 11989.4, 10840.9),
        ("02:00 - 03:00", 11951.8, 10633.2),
        ("03:00 - 04:00", 11942.9, 10543.2),
        ("04:00 - 05:00", 11110.2, 10014.0),
        ("05:00 - 06:00", 10765.6, 9381.8),
        ("06:00 - 07:00", 11864.5, 10464.8),
        ("07:00 - 08:00", 14197.5, 12797.8),
        ("08:00 - 09:00", 15482.9, 14083.2),
        ("09:00 - 10:00", 16269.1, 14869.4),
        ("10:00 - 11:00", 16036.7, 14637.0),
        ("11:00 - 12:00", 15972.9, 14573.2),
        ("12:00 - 13:00", 16132.0, 14732.3),
        ("13:00 - 14:00", 15901.0, 14501.3),
        ("14:00 - 15:00", 15478.0, 14078.3),
        ("15:00 - 16:00", 15647.9, 14248.2),
        ("16:00 - 17:00", 16486.2, 15086.5),
        ("17:00 - 18:00", 17775.0, 16375.3),
        ("18:00 - 19:00", 18829.9, 17430.2),
        ("19:00 - 20:00", 18132.7, 16733.0),
        ("20:00 - 21:00", 16556.1, 15156.4),
        ("21:00 - 22:00", 14137.7, 12738.0),
        ("22:00 - 23:00", 13089.5, 11689.8)
    ]

    df = scrape_nordpool_volumes('2025-10-20')

    assert df is not None, "Should return data for 2025-10-20"
    assert len(df) == 24, f"Should have 24 rows, got {len(df)}"

    for i, (expected_period, expected_buy, expected_sell) in enumerate(expected_data):
        actual_period = df.iloc[i]['period']
        actual_buy = df.iloc[i]['buy_volume']
        actual_sell = df.iloc[i]['sell_volume']

        assert actual_period == expected_period, f"Row {i}: expected period '{expected_period}', got '{actual_period}'"
        assert abs(actual_buy - expected_buy) < 0.1, f"Row {i}: expected buy volume {expected_buy}, got {actual_buy}"
        assert abs(actual_sell - expected_sell) < 0.1, f"Row {i}: expected sell volume {expected_sell}, got {actual_sell}"

    buy_total = df['buy_volume'].sum()
    sell_total = df['sell_volume'].sum()

    assert abs(buy_total - 349465.4) < 1.0, f"Buy total should be 349465.4, got {buy_total}"
    assert abs(sell_total - 317939.4) < 1.0, f"Sell total should be 317939.4, got {sell_total}"

    print("✓ All volume tests passed for 2025-10-20 data")


if __name__ == "__main__":
    test_nordpool_17_10_2025()
    test_nordpool_16_10_2025()
    test_nordpool_volumes_20_10_2025()