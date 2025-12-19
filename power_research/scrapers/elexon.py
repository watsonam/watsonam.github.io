import pandas as pd
import requests
import urllib3
import os
import pickle
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path
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


def get_balancing_acceptances(from_date: str, to_date: str | None = None,
                             bm_unit: str | None = None,
                             settlement_period_from: int | None = None,
                             settlement_period_to: int | None = None) -> pd.DataFrame | None:
    """This endpoint provides the bid-offer acceptance data (BOALF) for a requested BMU."""
    if to_date is None:
        to_date = from_date
    from_timestamp = f"{from_date}T00:00Z"
    to_timestamp = f"{to_date}T00:00Z"
    params = {
        'from': from_timestamp,
        'to': to_timestamp
    }
    if bm_unit is not None:
        params['bmUnit'] = bm_unit
    if settlement_period_from is not None:
        params['settlementPeriodFrom'] = settlement_period_from
    if settlement_period_to is not None:
        params['settlementPeriodTo'] = settlement_period_to
    response = requests.get(
        'https://data.elexon.co.uk/bmrs/api/v1/balancing/acceptances',
        params=params,
        headers={'accept': 'text/plain'},
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        data = response.json()
        return pd.DataFrame(data['data'])
    return None


def get_balancing_physical(from_date: str, to_date: str | None = None,
                          bm_unit: str | None = None,
                          settlement_period_from: int | None = None,
                          settlement_period_to: int | None = None,
                          datasets: list[str] | None = None) -> pd.DataFrame | None:
    """This endpoint provides the physical data for a requested BMU."""
    if to_date is None:
        to_date = from_date
    from_timestamp = f"{from_date}T00:00Z"
    to_timestamp = f"{to_date}T00:00Z"
    params = {
        'from': from_timestamp,
        'to': to_timestamp
    }
    if bm_unit is not None:
        params['bmUnit'] = bm_unit
    if settlement_period_from is not None:
        params['settlementPeriodFrom'] = settlement_period_from
    if settlement_period_to is not None:
        params['settlementPeriodTo'] = settlement_period_to
    if datasets is not None:
        params['dataset'] = datasets
    response = requests.get(
        'https://data.elexon.co.uk/bmrs/api/v1/balancing/physical',
        params=params,
        headers={'accept': 'text/plain'},
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        data = response.json()
        return pd.DataFrame(data['data'])
    return None


def get_balancing_dynamic(bm_unit: str | None = None,
                         snapshot_at: str | None = None,
                         until: str | None = None,
                         snapshot_at_settlement_period: int | None = None,
                         until_settlement_period: int | None = None,
                         datasets: list[str] | None = None) -> pd.DataFrame | None:
    """This endpoint provides the dynamic data for a requested BMU, excluding physical rate data."""
    params = {}
    if bm_unit is not None:
        params['bmUnit'] = bm_unit
    if snapshot_at is not None:
        params['snapshotAt'] = f"{snapshot_at}T00:00Z" if 'T' not in snapshot_at else snapshot_at
    if until is not None:
        params['until'] = f"{until}T00:00Z" if 'T' not in until else until
    if snapshot_at_settlement_period is not None:
        params['snapshotAtSettlementPeriod'] = snapshot_at_settlement_period
    if until_settlement_period is not None:
        params['untilSettlementPeriod'] = until_settlement_period
    if datasets is not None:
        params['dataset'] = datasets
    response = requests.get(
        'https://data.elexon.co.uk/bmrs/api/v1/balancing/dynamic',
        params=params,
        headers={'accept': 'text/plain'},
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        data = response.json()
        return pd.DataFrame(data['data'])
    return None


def get_balancing_bid_offer(from_date: str, to_date: str | None = None,
                           bm_unit: str | None = None,
                           settlement_period_from: int | None = None,
                           settlement_period_to: int | None = None) -> pd.DataFrame | None:
    """This endpoint provides the bid-offer data for a requested BMU."""
    if to_date is None:
        to_date = from_date
    from_timestamp = f"{from_date}T00:00Z"
    to_timestamp = f"{to_date}T00:00Z"
    params = {
        'from': from_timestamp,
        'to': to_timestamp
    }
    if bm_unit is not None:
        params['bmUnit'] = bm_unit
    if settlement_period_from is not None:
        params['settlementPeriodFrom'] = settlement_period_from
    if settlement_period_to is not None:
        params['settlementPeriodTo'] = settlement_period_to
    response = requests.get(
        'https://data.elexon.co.uk/bmrs/api/v1/balancing/bid-offer',
        params=params,
        headers={'accept': 'text/plain'},
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        data = response.json()
        return pd.DataFrame(data['data'])
    return None


def get_balancing_acceptances_all(settlement_date: str, settlement_period: int) -> pd.DataFrame | None:
    """This endpoint provides the bid-offer acceptance data (BOALF) for multiple or all BMUs."""
    params = {
        'settlementDate': settlement_date,
        'settlementPeriod': settlement_period
    }
    response = requests.get(
        'https://data.elexon.co.uk/bmrs/api/v1/balancing/acceptances/all',
        params=params,
        headers={'accept': 'text/plain'},
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        data = response.json()
        return pd.DataFrame(data['data'])
    return None


def get_balancing_bid_offer_all(settlement_date: str, settlement_period: int) -> pd.DataFrame | None:
    """This endpoint provides market-wide bid-offer data for all BMUs or a requested set of multiple BMUs."""
    params = {
        'settlementDate': settlement_date,
        'settlementPeriod': settlement_period
    }
    response = requests.get(
        'https://data.elexon.co.uk/bmrs/api/v1/balancing/bid-offer/all',
        params=params,
        headers={'accept': 'text/plain'},
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        data = response.json()
        return pd.DataFrame(data['data'])
    return None


def get_balancing_nonbm_volumes(from_date: str, to_date: str | None = None,
                               settlement_period_from: int | None = None,
                               settlement_period_to: int | None = None) -> pd.DataFrame | None:
    """This endpoint provides balancing services volume data received from NGESO."""
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
        'https://data.elexon.co.uk/bmrs/api/v1/balancing/nonbm/volumes',
        params=params,
        headers={'accept': 'text/plain'},
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        data = response.json()
        return pd.DataFrame(data['data'])
    return None


def get_balancing_nonbm_disbsad_details(settlement_date: str, settlement_period: int) -> pd.DataFrame | None:
    """This endpoint provides disaggregated balancing services adjustment data for a single settlement period."""
    params = {
        'settlementDate': settlement_date,
        'settlementPeriod': settlement_period
    }
    response = requests.get(
        'https://data.elexon.co.uk/bmrs/api/v1/balancing/nonbm/disbsad/details',
        params=params,
        headers={'accept': 'text/plain'},
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        data = response.json()
        return pd.DataFrame(data['data'])
    return None


def get_balancing_nonbm_disbsad_summary(from_date: str, to_date: str | None = None) -> pd.DataFrame | None:
    """This endpoint provides disaggregated balancing services adjustment data batched by settlement period."""
    if to_date is None:
        to_date = from_date
    from_timestamp = f"{from_date}T00:00Z"
    to_timestamp = f"{to_date}T00:00Z"
    params = {
        'from': from_timestamp,
        'to': to_timestamp
    }
    response = requests.get(
        'https://data.elexon.co.uk/bmrs/api/v1/balancing/nonbm/disbsad/summary',
        params=params,
        headers={'accept': 'text/plain'},
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        data = response.json()
        return pd.DataFrame(data['data'])
    return None


def get_balancing_acceptances_all_day(settlement_date: str) -> pd.DataFrame | None:
    """Get acceptances for all BMUs across all settlement periods (1-48) for a single day."""
    all_data = []
    for period in range(1, 49):
        df = get_balancing_acceptances_all(settlement_date, period)
        if df is not None and not df.empty:
            all_data.append(df)

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return None


def get_acceptances_with_prices(settlement_date: str) -> pd.DataFrame | None:
    """Join acceptances with bid-offer data to get actual prices paid."""
    acceptances_df = get_balancing_acceptances_all_day(settlement_date)
    if acceptances_df is None:
        return None

    all_bid_offers = []
    settlement_periods = acceptances_df['settlementPeriodFrom'].unique()

    for period in sorted(settlement_periods):
        bid_offer_df = get_balancing_bid_offer_all(settlement_date, period)
        if bid_offer_df is not None:
            all_bid_offers.append(bid_offer_df)

    if not all_bid_offers:
        return None

    bid_offers_df = pd.concat(all_bid_offers, ignore_index=True)

    merged_df = pd.merge(
        acceptances_df,
        bid_offers_df,
        on=['bmUnit', 'settlementDate'],
        how='inner',
        suffixes=('_acceptance', '_bid_offer')
    )

    merged_df = merged_df[
        (merged_df['settlementPeriodFrom'] >= merged_df['settlementPeriod']) &
        (merged_df['settlementPeriodTo'] <= merged_df['settlementPeriod'])
    ]

    return merged_df


def get_bm_units_reference() -> pd.DataFrame | None:
    """Get BMU reference data including fuel types and other metadata."""
    response = requests.get(
        'https://data.elexon.co.uk/bmrs/api/v1/reference/bmunits/all',
        headers={'accept': 'text/plain'},
        verify=False
    )
    if response.status_code == 200 and response.text.strip():
        data = response.json()
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif 'data' in data:
            return pd.DataFrame(data['data'])
        else:
            return pd.DataFrame(data)
    return None


def get_acceptances_with_fuel_types(settlement_date: str) -> pd.DataFrame | None:
    """Get acceptances with prices and fuel types for comprehensive analysis."""
    # Get acceptances with prices
    df_balancing = get_acceptances_with_prices(settlement_date)
    if df_balancing is None:
        return None

    # Get BMU reference data
    bmu_ref = get_bm_units_reference()
    if bmu_ref is None:
        return df_balancing

    # Merge to add fuel types
    merged_df = df_balancing.merge(
        bmu_ref[['elexonBmUnit', 'fuelType', 'bmUnitType', 'bmUnitName', 'leadPartyName']],
        left_on='bmUnit',
        right_on='elexonBmUnit',
        how='left'
    )

    return merged_df


def analyze_balancing_costs_simple(settlement_date: str, period_start: int = 1, period_end: int = 48, use_cache: bool = True) -> pd.DataFrame | None:
    """Create summary DataFrame of balancing costs with DISBSAD, acceptances, and bid-offers."""

    # Check cache first
    if use_cache:
        cache_dir = 'data/cache'
        os.makedirs(cache_dir, exist_ok=True)
        cache_file = f"{cache_dir}/balancing_costs_simple_{settlement_date}_{period_start}_{period_end}.pkl"

        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Cache read error for {settlement_date}: {e}")

    disbsad_df = get_balancing_nonbm_disbsad_summary(settlement_date, settlement_date)
    if disbsad_df is None or len(disbsad_df) == 0 or 'settlementPeriod' not in disbsad_df.columns:
        return None

    target_periods = disbsad_df[
        (disbsad_df['settlementPeriod'] >= period_start) &
        (disbsad_df['settlementPeriod'] <= period_end)
    ].copy()

    acceptances_df = get_balancing_acceptances_all_day(settlement_date)
    if acceptances_df is None:
        return target_periods

    target_acceptances = acceptances_df[
        (acceptances_df['settlementPeriodFrom'] >= period_start) &
        (acceptances_df['settlementPeriodTo'] <= period_end)
    ].copy()

    # Group acceptances by settlement period for summary
    period_summary = target_acceptances.groupby('settlementPeriodFrom').agg({
        'acceptanceNumber': 'count',
        'bmUnit': 'nunique',
        'levelFrom': ['sum', 'mean'],
        'levelTo': ['sum', 'mean']
    }).reset_index()

    period_summary.columns = [
        'settlementPeriod', 'acceptance_count', 'unique_bmus_called',
        'total_level_from', 'avg_level_from', 'total_level_to', 'avg_level_to'
    ]

    # Merge with DISBSAD data
    summary_df = target_periods.merge(
        period_summary,
        on='settlementPeriod',
        how='left'
    )

    # Fill NaN values for periods with no acceptances
    summary_df = summary_df.fillna(0)

    # Save to cache
    if use_cache:
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(summary_df, f)
        except Exception as e:
            print(f"Cache write error for {settlement_date}: {e}")

    return summary_df


def get_top_called_bmus_with_prices(settlement_date: str, period_start: int = 1, period_end: int = 48, top_n: int = 10) -> pd.DataFrame | None:
    """Get the top called BMUs with their offer price statistics."""

    # Get all acceptances for the day
    acceptances_df = get_balancing_acceptances_all_day(settlement_date)
    if acceptances_df is None:
        return None

    # Filter acceptances to target periods
    target_acceptances = acceptances_df[
        (acceptances_df['settlementPeriodFrom'] >= period_start) &
        (acceptances_df['settlementPeriodTo'] <= period_end)
    ].copy()

    if len(target_acceptances) == 0:
        return None

    # Group acceptances by BMU to see who was called most
    bmu_calls = target_acceptances.groupby('bmUnit').agg({
        'acceptanceNumber': 'count',
        'settlementPeriodFrom': ['min', 'max'],
        'levelFrom': 'sum',
        'levelTo': 'sum'
    }).reset_index()

    bmu_calls.columns = ['bmUnit', 'call_count', 'first_period', 'last_period', 'total_level_from', 'total_level_to']
    bmu_calls = bmu_calls.sort_values('call_count', ascending=False).head(top_n)

    # Get bid-offer data for target periods
    all_bid_offers = []
    for period in range(period_start, period_end + 1):
        bid_offer_df = get_balancing_bid_offer_all(settlement_date, period)
        if bid_offer_df is not None:
            all_bid_offers.append(bid_offer_df)

    if not all_bid_offers:
        return bmu_calls

    bid_offers_df = pd.concat(all_bid_offers, ignore_index=True)

    # Get bid-offer data for the top called BMUs
    top_bmus = bmu_calls['bmUnit'].tolist()
    top_bmu_offers = bid_offers_df[bid_offers_df['bmUnit'].isin(top_bmus)].copy()

    # Summary stats by BMU
    offer_stats = top_bmu_offers.groupby('bmUnit')['offer'].agg(['min', 'max', 'mean', 'count']).reset_index()
    offer_stats.columns = ['bmUnit', 'offer_min', 'offer_max', 'offer_mean', 'offer_count']

    # Merge call counts with offer stats
    result_df = bmu_calls.merge(offer_stats, on='bmUnit', how='left')

    return result_df


def save_elexon_history(days_back: int = 3, data_dir: str = "power_research/data/elexon") -> int:
    base_path = Path(data_dir)
    base_path.mkdir(parents=True, exist_ok=True)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    current_date = start_date
    success_count = 0

    print(f"Saving Elexon data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        print(f"Processing {date_str}")

        demand_file = base_path / f"{date_str}_demand_outturn.csv"
        if not demand_file.exists():
            demand_df = get_demand_outturn_stream(date_str)
            if demand_df is not None and not demand_df.empty:
                demand_df.to_csv(demand_file, index=False)
                print(f"  ✓ Saved demand outturn data: {len(demand_df)} rows")
            else:
                print(f"  ✗ No demand outturn data available")
        else:
            print(f"  Skipping demand outturn - already exists")

        balancing_file = base_path / f"{date_str}_balancing_costs.csv"
        if not balancing_file.exists():
            balancing_df = analyze_balancing_costs_simple(date_str)
            if balancing_df is not None and not balancing_df.empty:
                balancing_df.to_csv(balancing_file, index=False)
                print(f"  ✓ Saved balancing costs data: {len(balancing_df)} rows")
            else:
                print(f"  ✗ No balancing costs data available")
        else:
            print(f"  Skipping balancing costs - already exists")

        acceptances_file = base_path / f"{date_str}_acceptances.csv"
        if not acceptances_file.exists():
            acceptances_df = get_acceptances_with_fuel_types(date_str)
            if acceptances_df is not None and not acceptances_df.empty:
                acceptances_df.to_csv(acceptances_file, index=False)
                print(f"  ✓ Saved acceptances data: {len(acceptances_df)} rows")
                success_count += 1
            else:
                print(f"  ✗ No acceptances data available")
        else:
            print(f"  Skipping acceptances - already exists")

        current_date += timedelta(days=1)

    print(f"Completed: {success_count} days processed")
    return success_count


if __name__ == "__main__":
    save_elexon_history(days_back=3)
