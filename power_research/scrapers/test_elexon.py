from elexon import get_balancing_acceptances, get_balancing_physical, get_balancing_dynamic, get_balancing_bid_offer, get_balancing_acceptances_all, get_balancing_bid_offer_all, get_balancing_nonbm_volumes, get_balancing_nonbm_disbsad_details, get_balancing_nonbm_disbsad_summary, get_balancing_acceptances_all_day, analyze_balancing_costs_simple, get_acceptances_with_prices, get_acceptances_with_fuel_types, get_top_called_bmus_with_prices
import pandas as pd
import pickle
import os
from datetime import datetime, timedelta

def test_get_balancing_acceptances():
    print("Testing get_balancing_acceptances function")
    df = get_balancing_acceptances('2022-10-03', '2022-10-06', 'T_MILWW-1')

    if df is not None:
        print(f"✓ Got {len(df)} rows")
        print(f"Columns: {df.columns.tolist()}")
        expected_cols = ['settlementDate', 'bmUnit', 'acceptanceNumber']
        for col in expected_cols:
            if col in df.columns:
                print(f"✓ {col} found")
            else:
                print(f"✗ {col} missing")
        print("Acceptances test passed")
    else:
        print("✗ No acceptances data returned")

def test_get_balancing_physical():
    print("\nTesting get_balancing_physical function")
    df = get_balancing_physical('2022-09-22', '2022-09-23', '2__HFLEX001', datasets=['PN', 'MILS'])

    if df is not None:
        print(f"✓ Got {len(df)} rows")
        print(f"Columns: {df.columns.tolist()}")
        expected_cols = ['dataset', 'settlementDate', 'bmUnit']
        for col in expected_cols:
            if col in df.columns:
                print(f"✓ {col} found")
            else:
                print(f"✗ {col} missing")
        print("Physical test passed")
    else:
        print("✗ No physical data returned")

def test_get_balancing_dynamic():
    print("\nTesting get_balancing_dynamic function")
    df = get_balancing_dynamic(
        bm_unit='2__HFLEX001',
        snapshot_at='2022-08-23T00:00Z',
        until='2022-08-24T00:00Z',
        snapshot_at_settlement_period=2,
        until_settlement_period=2,
        datasets=['SEL', 'MNZT', 'MDP']
    )

    if df is not None:
        print(f"✓ Got {len(df)} rows")
        print(f"Columns: {df.columns.tolist()}")
        expected_cols = ['dataset', 'bmUnit', 'value']
        for col in expected_cols:
            if col in df.columns:
                print(f"✓ {col} found")
            else:
                print(f"✗ {col} missing")
        print("Dynamic test passed")
    else:
        print("✗ No dynamic data returned")

def test_get_balancing_bid_offer():
    print("\nTesting get_balancing_bid_offer function")
    df = get_balancing_bid_offer('2022-09-22', '2022-09-23', '2__HFLEX001')

    if df is not None:
        print(f"✓ Got {len(df)} rows")
        print(f"Columns: {df.columns.tolist()}")
        expected_cols = ['settlementDate', 'bmUnit', 'bid', 'offer']
        for col in expected_cols:
            if col in df.columns:
                print(f"✓ {col} found")
            else:
                print(f"✗ {col} missing")
        print("Bid-offer test passed")
    else:
        print("✗ No bid-offer data returned")

def test_get_balancing_acceptances_all():
    print("\nTesting get_balancing_acceptances_all function")
    df = get_balancing_acceptances_all('2023-01-24', 39)

    if df is not None:
        print(f"✓ Got {len(df)} rows")
        print(f"Columns: {df.columns.tolist()}")
        expected_cols = ['settlementDate', 'bmUnit', 'acceptanceNumber']
        for col in expected_cols:
            if col in df.columns:
                print(f"✓ {col} found")
            else:
                print(f"✗ {col} missing")
        print("Acceptances-all test passed")
    else:
        print("✗ No acceptances-all data returned")

def test_get_balancing_bid_offer_all():
    print("\nTesting get_balancing_bid_offer_all function")
    df = get_balancing_bid_offer_all('2022-09-22', 1)

    if df is not None:
        print(f"✓ Got {len(df)} rows")
        print(f"Columns: {df.columns.tolist()}")
        expected_cols = ['settlementDate', 'bmUnit', 'bid', 'offer']
        for col in expected_cols:
            if col in df.columns:
                print(f"✓ {col} found")
            else:
                print(f"✗ {col} missing")
        print("Bid-offer-all test passed")
    else:
        print("✗ No bid-offer-all data returned")

def test_get_balancing_nonbm_volumes():
    print("\nTesting get_balancing_nonbm_volumes function")
    df = get_balancing_nonbm_volumes('2022-08-12', '2022-08-13')

    if df is not None:
        print(f"✓ Got {len(df)} rows")
        print(f"Columns: {df.columns.tolist()}")
        expected_cols = ['settlementDate', 'bmUnit', 'bmUnitApplicableBalancingServicesVolume']
        for col in expected_cols:
            if col in df.columns:
                print(f"✓ {col} found")
            else:
                print(f"✗ {col} missing")
        print("Non-BM volumes test passed")
    else:
        print("✗ No non-BM volumes data returned")

def test_get_balancing_nonbm_disbsad_details():
    print("\nTesting get_balancing_nonbm_disbsad_details function")
    df = get_balancing_nonbm_disbsad_details('2022-10-26', 3)

    if df is not None:
        print(f"✓ Got {len(df)} rows")
        print(f"Columns: {df.columns.tolist()}")
        expected_cols = ['settlementDate', 'cost', 'volume', 'price', 'partyId']
        for col in expected_cols:
            if col in df.columns:
                print(f"✓ {col} found")
            else:
                print(f"✗ {col} missing")
        print("DISBSAD details test passed")
    else:
        print("✗ No DISBSAD details data returned")

def test_get_balancing_nonbm_disbsad_summary():
    print("\nTesting get_balancing_nonbm_disbsad_summary function")
    df = get_balancing_nonbm_disbsad_summary('2022-09-20', '2022-09-27')

    if df is not None:
        print(f"✓ Got {len(df)} rows")
        print(f"Columns: {df.columns.tolist()}")
        expected_cols = ['settlementDate', 'buyActionCount', 'sellActionCount', 'netVolume']
        for col in expected_cols:
            if col in df.columns:
                print(f"✓ {col} found")
            else:
                print(f"✗ {col} missing")
        print("DISBSAD summary test passed")
    else:
        print("✗ No DISBSAD summary data returned")

def test_get_balancing_acceptances_all_day():
    print("\nTesting get_balancing_acceptances_all_day function")
    df = get_balancing_acceptances_all_day('2023-01-24')

    if df is not None:
        print(f"✓ Got {len(df)} rows")
        print(f"Unique settlement periods: {sorted(df['settlementPeriodFrom'].unique())[:10]}...")
        expected_cols = ['settlementDate', 'bmUnit', 'acceptanceNumber']
        for col in expected_cols:
            if col in df.columns:
                print(f"✓ {col} found")
            else:
                print(f"✗ {col} missing")
        print("Acceptances-all-day test passed")
    else:
        print("✗ No acceptances-all-day data returned")

def test_analyze_balancing_costs_simple():
    print("\nTesting analyze_balancing_costs_simple function")
    df = analyze_balancing_costs_simple('2025-11-20')

    if df is not None:
        print(f"✓ Got {len(df)} periods summary")
        if len(df) > 0:
            print(f"✓ Max buy price: £{df['buyPriceMaximum'].max():.2f}/MWh")
        print("Summary analysis test passed")
    else:
        print("✗ No summary data returned")

def test_get_acceptances_with_prices():
    print("\nTesting get_acceptances_with_prices function")
    df = get_acceptances_with_prices('2025-11-20')

    if df is not None:
        print(f"✓ Got {len(df)} merged records")
        print(f"✓ Max offer: £{df['offer'].max():.2f}/MWh")
        print("Complex analysis test passed")
    else:
        print("✗ No merged data returned")

def test_get_acceptances_with_fuel_types():
    print("\nTesting get_acceptances_with_fuel_types function")
    df = get_acceptances_with_fuel_types('2025-11-20')

    if df is not None:
        print(f"✓ Got {len(df)} records with fuel types")
        fuel_types = df['fuelType'].value_counts()
        print(f"✓ Fuel types: {fuel_types.head().to_dict()}")
        print("Fuel type mapping test passed")
    else:
        print("✗ No fuel type data returned")

def test_get_top_called_bmus_with_prices():
    print("\nTesting get_top_called_bmus_with_prices function")
    df = get_top_called_bmus_with_prices('2025-11-20')

    if df is not None:
        print(f"✓ Got {len(df)} top called BMUs")
        print(f"✓ Most called: {df.iloc[0]['bmUnit']} ({df.iloc[0]['call_count']} calls)")
        print("Top BMUs test passed")
    else:
        print("✗ No top BMU data returned")

def test_90_day_analysis():
    print("\n=== RUNNING 90-DAY BALANCING COSTS ANALYSIS ===")

    # Calculate date range: 90 days before today (2025-11-22)
    end_date = datetime(2025, 11, 21)  # Yesterday
    start_date = end_date - timedelta(days=89)  # 90 days total

    print(f"Analyzing from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

    results = []
    successful = 0
    failed = 0

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')

        try:
            df = analyze_balancing_costs_simple(date_str, use_cache=True)
            if df is not None and len(df) > 0:
                # Add date column for consolidation
                df['analysis_date'] = date_str
                results.append(df)
                successful += 1

                # Print progress every 10 days
                if successful % 10 == 0:
                    print(f"✓ Processed {successful} days successfully...")
            else:
                failed += 1

        except Exception as e:
            print(f"✗ Error processing {date_str}: {e}")
            failed += 1

        current_date += timedelta(days=1)

    print(f"\nCompleted: {successful} successful, {failed} failed")

    if results:
        # Combine all results
        combined_df = pd.concat(results, ignore_index=True)
        print(f"✓ Combined dataset: {len(combined_df)} total periods across {len(results)} days")

        # Save combined results
        os.makedirs('data', exist_ok=True)

        # Save as pickle
        pickle_file = 'data/balancing_costs_90_days.pkl'
        with open(pickle_file, 'wb') as f:
            pickle.dump(combined_df, f)
        print(f"✓ Saved combined results to {pickle_file}")

        # Save as CSV for easy viewing
        csv_file = 'data/balancing_costs_90_days.csv'
        combined_df.to_csv(csv_file, index=False)
        print(f"✓ Saved combined results to {csv_file}")

        # Show summary statistics
        print("\n=== SUMMARY STATISTICS ===")
        active_periods = combined_df[combined_df['buyVolumeTotal'] > 0]
        print(f"Periods with balancing activity: {len(active_periods)}")
        if len(active_periods) > 0:
            print(f"Max buy price: £{active_periods['buyPriceMaximum'].max():.2f}/MWh")
            print(f"Average buy price: £{active_periods['buyPriceMaximum'].mean():.2f}/MWh")
            print(f"Total balancing volume: {active_periods['buyVolumeTotal'].sum():.1f} MWh")

            # Top 5 most expensive periods
            top_expensive = active_periods.nlargest(5, 'buyPriceMaximum')
            print("\nTop 5 most expensive periods:")
            print(top_expensive[['analysis_date', 'settlementPeriod', 'buyPriceMaximum', 'buyVolumeTotal']].to_string(index=False))
    else:
        print("✗ No data collected for 90-day period")

if __name__ == '__main__':
    test_get_balancing_acceptances()
    test_get_balancing_physical()
    test_get_balancing_dynamic()
    test_get_balancing_bid_offer()
    test_get_balancing_acceptances_all()
    test_get_balancing_bid_offer_all()
    test_get_balancing_nonbm_volumes()
    test_get_balancing_nonbm_disbsad_details()
    test_get_balancing_nonbm_disbsad_summary()
    test_get_balancing_acceptances_all_day()
    test_analyze_balancing_costs_simple()
    test_get_acceptances_with_prices()
    test_get_acceptances_with_fuel_types()
    test_get_top_called_bmus_with_prices()
    test_90_day_analysis()
    print("\nAll Elexon tests completed")