from scrapers.elexon import analyze_balancing_costs_simple, get_acceptances_with_prices
import pandas as pd

def compare_approaches():
    print("=== COMPARING BOTH APPROACHES FOR 2025-11-20 (FULL DAY) ===\n")

    # Test both approaches
    date = '2025-11-20'

    print("1. COMPLEX APPROACH (Direct Join):")
    print("=" * 50)

    df_complex = get_acceptances_with_prices(date)

    if df_complex is not None and len(df_complex) > 0:
        print(f"✓ Merged data: {len(df_complex)} records")
        print(f"Max offer: £{df_complex['offer'].max():.2f}/MWh")
        print(f"Mean offer: £{df_complex['offer'].mean():.2f}/MWh")

        print("\nTop 5 highest offer prices:")
        top_offers = df_complex.nlargest(5, 'offer')[['bmUnit', 'offer', 'bid']]
        print(top_offers.to_string(index=False))

        expensive_count = len(df_complex[df_complex['offer'] > 1000])
        print(f"\nOffers > £1000/MWh: {expensive_count}")
    else:
        print("✗ No data from complex approach")

    print("\n" + "=" * 60 + "\n")

    print("2. SIMPLE APPROACH (Three-Step Analysis):")
    print("=" * 50)

    summary_df = analyze_balancing_costs_simple(date)  # Now returns DataFrame

    if summary_df is not None:
        print(f"✓ DISBSAD Summary:")
        max_price = summary_df['buyPriceMaximum'].max()
        avg_price = summary_df['buyPriceAverage'].mean()
        total_volume = summary_df['buyVolumeTotal'].sum()
        print(f"  Max buy price: £{max_price:.2f}/MWh")
        print(f"  Avg buy price: £{avg_price:.2f}/MWh")
        print(f"  Total volume: {total_volume:.1f} MWh")

        print(f"\nAll periods with balancing activity:")
        active_periods = summary_df[summary_df['buyVolumeTotal'] > 0]
        if len(active_periods) > 0:
            print(active_periods[['settlementPeriod', 'buyPriceMaximum', 'buyVolumeTotal', 'acceptance_count']].to_string(index=False))
        else:
            print("No periods with balancing volume")
    else:
        print("✗ No summary data available")

    print("\n" + "=" * 60 + "\n")
    print("COMPARISON SUMMARY:")
    print("=" * 20)

    if df_complex is not None and len(df_complex) > 0:
        complex_max = df_complex['offer'].max()
        complex_records = len(df_complex)
    else:
        complex_max = 0
        complex_records = 0

    if summary_df is not None and len(summary_df) > 0:
        simple_max = summary_df['buyPriceMaximum'].max()
        simple_volume = summary_df['buyVolumeTotal'].sum()
    else:
        simple_max = 0
        simple_volume = 0

    print(f"Complex approach: {complex_records} records, max offer £{complex_max:.2f}/MWh")
    print(f"Simple approach: max buy price £{simple_max:.2f}/MWh, total volume {simple_volume:.1f} MWh")

    if complex_max > 0 and simple_max > 0:
        print("✓ Both approaches found balancing activity")
    elif complex_max > 0 and simple_max == 0:
        print("! Complex found activity, simple didn't - check period alignment")
    elif complex_max == 0 and simple_max > 0:
        print("! Simple found activity, complex didn't - possible join issues")
    else:
        print("- No significant balancing activity detected by either approach")

if __name__ == '__main__':
    compare_approaches()