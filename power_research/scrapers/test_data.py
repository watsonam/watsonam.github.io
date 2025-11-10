import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from elexon import get_generation_by_fuel, get_market_index_data


def test_get_generation_by_fuel():
    """Test get_generation_by_fuel function returns expected data structure"""
    df = get_generation_by_fuel('2025-10-17', '2025-10-17')

    assert df is not None, "Function should return data"
    assert isinstance(df, pd.DataFrame), "Should return DataFrame"

    expected_columns = ['dataset', 'publishTime', 'startTime', 'settlementDate',
                       'settlementPeriod', 'fuelType', 'generation']

    for col in expected_columns:
        assert col in df.columns, f"Missing column: {col}"

    assert 'FUELHH' in df['dataset'].values, "Dataset should contain FUELHH"

    fuel_types = df['fuelType'].unique()
    expected_fuel_types = ['BIOMASS', 'CCGT', 'COAL', 'INTELEC']
    for fuel in expected_fuel_types:
        assert fuel in fuel_types, f"Missing fuel type: {fuel}"

    assert all(df['settlementPeriod'].between(1, 48)), "Settlement periods should be 1-48"
    assert df['generation'].notna().all(), "Generation should not have null values"

    print(f"Test passed! Retrieved {len(df)} records with {len(fuel_types)} fuel types")
    return True


def test_get_market_index_data():
    """Test get_market_index_data function returns expected data structure"""
    df = get_market_index_data('2022-09-26')

    assert df is not None, "Function should return data"
    assert isinstance(df, pd.DataFrame), "Should return DataFrame"

    expected_columns = ['startTime', 'dataProvider', 'settlementDate', 'settlementPeriod', 'price', 'volume']
    for col in expected_columns:
        assert col in df.columns, f"Missing column: {col}"

    data_providers = df['dataProvider'].unique()
    expected_providers = ['N2EXMIDP', 'APXMIDP']
    for provider in expected_providers:
        assert provider in data_providers, f"Missing data provider: {provider}"

    assert all(df['settlementPeriod'].between(1, 48)), "Settlement periods should be 1-48"
    assert df['price'].notna().all(), "Price should not have null values"
    assert df['volume'].notna().all(), "Volume should not have null values"

    print(f"Test passed! Retrieved {len(df)} records from {len(data_providers)} providers")
    return True


def get_test_data_2024_10_17():
    """Returns test data for 2024-10-17"""
    data = [
        {"period": "23:00 - 00:00", "price": 78.20},
        {"period": "00:00 - 01:00", "price": 75.98},
        {"period": "01:00 - 02:00", "price": 76.00},
        {"period": "02:00 - 03:00", "price": 74.55},
        {"period": "03:00 - 04:00", "price": 73.79},
        {"period": "04:00 - 05:00", "price": 73.35},
        {"period": "05:00 - 06:00", "price": 87.85},
        {"period": "06:00 - 07:00", "price": 94.28},
        {"period": "07:00 - 08:00", "price": 113.24},
        {"period": "08:00 - 09:00", "price": 109.94},
        {"period": "09:00 - 10:00", "price": 99.00},
        {"period": "10:00 - 11:00", "price": 87.95},
        {"period": "11:00 - 12:00", "price": 83.85},
        {"period": "12:00 - 13:00", "price": 77.35},
        {"period": "13:00 - 14:00", "price": 75.66},
        {"period": "14:00 - 15:00", "price": 75.57},
        {"period": "15:00 - 16:00", "price": 82.74},
        {"period": "16:00 - 17:00", "price": 98.47},
        {"period": "17:00 - 18:00", "price": 115.09},
        {"period": "18:00 - 19:00", "price": 124.50},
        {"period": "19:00 - 20:00", "price": 106.00},
        {"period": "20:00 - 21:00", "price": 88.34},
        {"period": "21:00 - 22:00", "price": 86.15},
        {"period": "22:00 - 23:00", "price": 78.14}
    ]
    return pd.DataFrame(data)


def get_test_data_2024_10_16():
    """Returns test data for 2024-10-16"""
    data = [
        {"period": "23:00 - 00:00", "price": 79.59},
        {"period": "00:00 - 01:00", "price": 75.01},
        {"period": "01:00 - 02:00", "price": 73.54},
        {"period": "02:00 - 03:00", "price": 72.02},
        {"period": "03:00 - 04:00", "price": 71.07},
        {"period": "04:00 - 05:00", "price": 72.25},
        {"period": "05:00 - 06:00", "price": 76.08},
        {"period": "06:00 - 07:00", "price": 92.47},
        {"period": "07:00 - 08:00", "price": 108.84},
        {"period": "08:00 - 09:00", "price": 106.19},
        {"period": "09:00 - 10:00", "price": 99.10},
        {"period": "10:00 - 11:00", "price": 81.42},
        {"period": "11:00 - 12:00", "price": 76.71},
        {"period": "12:00 - 13:00", "price": 77.98},
        {"period": "13:00 - 14:00", "price": 77.79},
        {"period": "14:00 - 15:00", "price": 75.22},
        {"period": "15:00 - 16:00", "price": 84.96},
        {"period": "16:00 - 17:00", "price": 106.07},
        {"period": "17:00 - 18:00", "price": 126.64},
        {"period": "18:00 - 19:00", "price": 140.42},
        {"period": "19:00 - 20:00", "price": 122.38},
        {"period": "20:00 - 21:00", "price": 107.56},
        {"period": "21:00 - 22:00", "price": 87.49},
        {"period": "22:00 - 23:00", "price": 77.18}
    ]
    return pd.DataFrame(data)