import pandas as pd
import requests
import urllib3
import os
import pickle
from datetime import datetime, timedelta
from io import StringIO
from typing import Optional

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_actual_demand() -> Optional[pd.DataFrame]:
    response = requests.get(
        'https://data.elexon.co.uk/bmrs/api/v1/datasets/INDO',
        params={'format': 'csv'},
        headers={'accept': 'text/plain'},
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        return pd.read_csv(StringIO(response.text))
    return None


def get_generation_mix() -> Optional[pd.DataFrame]:
    response = requests.get(
        'https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH',
        params={'format': 'csv'},
        headers={'accept': 'text/plain'},
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        return pd.read_csv(StringIO(response.text))
    return None


def get_demand_outturn_stream(settlement_date_from: str, settlement_date_to: Optional[str] = None) -> Optional[pd.DataFrame]:
    if settlement_date_to is None:
        settlement_date_to = settlement_date_from
    response = requests.get(
        'https://data.elexon.co.uk/bmrs/api/v1/demand/outturn/stream',
        params={
            'settlementDateFrom': settlement_date_from,
            'settlementDateTo': settlement_date_to
        },
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        data = response.json()
        df = pd.DataFrame(data)
        if 'settlementPeriod' in df.columns:
            df['hour'] = ((df['settlementPeriod'] - 1) // 2).astype(int)
        return df
    return None


def aggregate_demand_to_hourly(df: pd.DataFrame) -> pd.DataFrame:
    hourly_df = df.groupby(['settlementDate', 'hour']).agg({
        'initialDemandOutturn': ['mean', 'max', 'min']
    }).round(2)
    hourly_df.columns = ['avg_demand_mw', 'max_demand_mw', 'min_demand_mw']
    hourly_df = hourly_df.reset_index()
    hourly_df['period'] = hourly_df['hour'].apply(
        lambda h: f"{h:02d}:00 - {(h+1)%24:02d}:00"
    )
    return hourly_df.sort_values(['settlementDate', 'hour']).reset_index(drop=True)


def get_actual_total_load(settlement_date: str) -> Optional[pd.DataFrame]:
    response = requests.get(
        'https://data.elexon.co.uk/bmrs/api/v1/demand/actual/total',
        params={
            'from': settlement_date,
            'to': settlement_date,
            'settlementPeriodFrom': 1,
            'settlementPeriodTo': 48
        },
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        data = response.json()
        df = pd.DataFrame(data['data'])
        if 'settlementPeriod' in df.columns:
            df['hour'] = ((df['settlementPeriod'] - 1) // 2).astype(int)
        return df
    return None


def get_bid_offer_data(settlement_date: str, settlement_period: int) -> Optional[pd.DataFrame]:
    response = requests.get(
        'https://data.elexon.co.uk/bmrs/api/v1/balancing/bid-offer/all',
        params={
            'settlementDate': settlement_date,
            'settlementPeriod': settlement_period
        },
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        data = response.json()
        df = pd.DataFrame(data['data'])
        return df
    return None


def get_apx_market_index(settlement_date_from: str, settlement_date_to: Optional[str] = None) -> Optional[pd.DataFrame]:
    if settlement_date_to is None:
        settlement_date_to = settlement_date_from
    from_timestamp = f"{settlement_date_from}T00:00Z"
    to_timestamp = f"{settlement_date_to}T00:00Z"
    response = requests.get(
        'https://data.elexon.co.uk/bmrs/api/v1/balancing/pricing/market-index',
        params={
            'from': from_timestamp,
            'to': to_timestamp,
            'dataProviders': 'APXMIDP'
        },
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        data = response.json()
        df = pd.DataFrame(data['data'])
        if 'settlementPeriod' in df.columns:
            df['hour'] = ((df['settlementPeriod'] - 1) // 2).astype(int)
        return df
    return None


def get_generation_by_fuel(settlement_date_from: str, settlement_date_to: Optional[str] = None) -> Optional[pd.DataFrame]:
    if settlement_date_to is None:
        settlement_date_to = settlement_date_from

    cache_dir = '../cache'
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = f'{cache_dir}/generation_fuel_{settlement_date_from}_{settlement_date_to}.pkl'

    if os.path.exists(cache_file):
        print(f"Loading from cache: {cache_file}")
        return pickle.load(open(cache_file, 'rb'))

    max_retries = 3
    for attempt in range(max_retries):
        response = requests.get(
            'https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH',
            params={
                'settlementDateFrom': settlement_date_from,
                'settlementDateTo': settlement_date_to
            },
            verify=False,
            timeout=30
        )
        if response.status_code == 200 and response.text.strip():
            data = response.json()
            df = pd.DataFrame(data['data'])
            pickle.dump(df, open(cache_file, 'wb'))
            print(f"Cached data: {cache_file}")
            return df
        elif attempt < max_retries - 1:
            print(f"Request failed, retrying... ({attempt + 1}/{max_retries})")
    return None


def get_market_index_data(from_date: str, to_date: Optional[str] = None,
                         settlement_period_from: Optional[int] = None,
                         settlement_period_to: Optional[int] = None) -> Optional[pd.DataFrame]:
    if to_date is None:
        to_date = from_date
    from_timestamp = f"{from_date}T00:00Z"
    to_timestamp = f"{to_date}T00:00Z"
    params = {
        'from': from_timestamp,
        'to': to_timestamp
    }
    if settlement_period_from is not None:
        params['settlementPeriodFrom'] = settlement_period_from
    if settlement_period_to is not None:
        params['settlementPeriodTo'] = settlement_period_to
    response = requests.get(
        'https://data.elexon.co.uk/bmrs/api/v1/balancing/pricing/market-index',
        params=params,
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        data = response.json()
        return pd.DataFrame(data['data'])
    return None