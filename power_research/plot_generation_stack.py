import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import pandas as pd
import matplotlib.pyplot as plt
from scrapers.elexon import get_generation_by_fuel

# NOTE: The renewables outturn values are underestimated in this report because they exclude embedded generation 
# and wind farms which do not have Operational Meters. As of 2025, NESO estimates this representation of wind farms 
# with Operational Meters to be approximately 82%.

category_colors = {
    'Nuclear': '#2b4c85',
    'Hydro (non-PS)': '#00a0b0',
    'Wind': '#4a9eff',
    'Biomass': '#8b4a9c',
    'CCGT': '#b85450',
    'OCGT': '#90ee90',
    'Coal': '#333333',
    'Oil': '#7a7a7a',
    'Other': '#ff8c42',
    'Pumped Storage': '#006080',
    'Interconnectors': '#70c1b3'
}

def prepare_generation_data(settlement_date: str) -> pd.DataFrame | None:
    fuel_generation = get_generation_by_fuel(settlement_date)
    if fuel_generation is None:
        return None
    fuel_mapping = {'BIOMASS': 'Biomass', 'CCGT': 'CCGT', 'COAL': 'Coal', 'NUCLEAR': 'Nuclear', 'NPSHYD': 'Hydro (non-PS)', 'OCGT': 'OCGT', 'OIL': 'Oil', 'OTHER': 'Other', 'PS': 'Pumped Storage', 'WIND': 'Wind'}
    interconnector_mapping = {'INTELEC': 'Eleclink (INTELEC)', 'INTEW': 'Ireland (East-West)', 'INTFR': 'France (IFA)', 'INTGRNL': 'Ireland (Greenlink)', 'INTIFA2': 'France (IFA2)', 'INTIRL': 'Northern Ireland (Moyle)', 'INTNED': 'Netherlands (BritNed)', 'INTNEM': 'Belgium (Nemolink)', 'INTNSL': 'North Sea Link (INTNSL)', 'INTVKL': 'Denmark (Viking link)'}
    fuel_generation['fuel_category'] = fuel_generation['fuelType'].map(fuel_mapping)
    fuel_generation.loc[fuel_generation['fuelType'].isin(interconnector_mapping.keys()), 'fuel_category'] = 'Interconnectors'
    return fuel_generation.groupby(['settlementPeriod', 'fuel_category'])['generation'].sum().unstack(fill_value=0)

def create_generation_stack_chart(settlement_date: str) -> None:
    pivot_df = prepare_generation_data(settlement_date)
    if pivot_df is None:
        print(f"No data available for {settlement_date}")
        return
    generation_order = [
        'Nuclear', 'Hydro (non-PS)', 'Wind', 'Biomass', 'CCGT',
        'OCGT', 'Coal', 'Oil', 'Other', 'Pumped Storage', 'Interconnectors'
    ]
    plt.figure(figsize=(15, 8))
    bottom_pos = pd.Series([0] * len(pivot_df.index), index=pivot_df.index)
    bottom_neg = pd.Series([0] * len(pivot_df.index), index=pivot_df.index)
    label_positions = [5, 10, 15, 20, 25, 30, 35, 40, 45, 12, 27]
    for i, category in enumerate(generation_order):
        if category in pivot_df.columns:
            values = pivot_df[category]
            color = category_colors.get(category, '#888888')

            positive_vals = values.clip(lower=0)
            negative_vals = values.clip(upper=0)

            if positive_vals.sum() > 0:
                plt.fill_between(pivot_df.index, bottom_pos, bottom_pos + positive_vals,
                                label=category, color=color, alpha=0.85)
                avg_val = positive_vals.mean()
                if avg_val > 200 and i < len(label_positions):
                    label_settlement = label_positions[i]
                    if label_settlement <= len(positive_vals):
                        idx = label_settlement - 1
                        y_pos = bottom_pos.iloc[idx] + positive_vals.iloc[idx]/2
                        plt.text(label_settlement, y_pos, category,
                                ha='center', va='center', fontsize=9, rotation=90,
                                color='white', weight='bold')
                bottom_pos += positive_vals

            if negative_vals.sum() < 0:
                plt.fill_between(pivot_df.index, bottom_neg, bottom_neg + negative_vals,
                                color=color, alpha=0.85)
                avg_val = abs(negative_vals.mean())
                if avg_val > 200 and i < len(label_positions):
                    label_settlement = label_positions[i]
                    if label_settlement <= len(negative_vals):
                        idx = label_settlement - 1
                        y_pos = bottom_neg.iloc[idx] + negative_vals.iloc[idx]/2
                        plt.text(label_settlement, y_pos, category,
                                ha='center', va='center', fontsize=9, rotation=90,
                                color='white', weight='bold')
                bottom_neg += negative_vals

    plt.xlabel('Settlement Period')
    plt.ylabel('Generation (MW)')
    plt.title(f'UK Electricity Generation by Fuel Type - {settlement_date}')
    plt.grid(True, alpha=0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def create_percentage_stack_chart(settlement_date: str) -> None:
    pivot_df = prepare_generation_data(settlement_date)
    if pivot_df is None:
        print(f"No data available for {settlement_date}")
        return
    positive_df = pivot_df.clip(lower=0)
    totals = positive_df.sum(axis=1)
    percentage_df = positive_df.div(totals, axis=0) * 100
    generation_order = [
        'Nuclear', 'Hydro (non-PS)', 'Wind', 'Biomass', 'CCGT',
        'OCGT', 'Coal', 'Oil', 'Other', 'Pumped Storage', 'Interconnectors'
    ]
    available_categories = [cat for cat in generation_order if cat in percentage_df.columns]
    plt.figure(figsize=(15, 8))
    plt.bar(percentage_df.index, percentage_df[available_categories[0]],
             color=category_colors.get(available_categories[0], '#888888'),
             label=available_categories[0], alpha=0.85)
    bottom = percentage_df[available_categories[0]]
    for category in available_categories[1:]:
        plt.bar(percentage_df.index, percentage_df[category], bottom=bottom,
                color=category_colors.get(category, '#888888'), label=category, alpha=0.85)
        bottom += percentage_df[category]
    plt.xlabel('Settlement Period')
    plt.ylabel('Percentage (%)')
    plt.title(f'UK Electricity Generation by Fuel Type (%) - {settlement_date}')
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3, axis='y')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_ccgt_vs_price(settlement_date: str, apx_data: pd.DataFrame) -> None:
    pivot_df = prepare_generation_data(settlement_date)
    if pivot_df is None:
        print(f"No data available for {settlement_date}")
        return

    fig, ax1 = plt.subplots(figsize=(12, 6))

    for category in ['CCGT']:
        values = pivot_df[category]
        color = category_colors.get(category, '#888888')
        ax1.plot(pivot_df.index, values, color=color, label=category)
    ax1.set_xlabel('Settlement Period')
    ax1.set_ylabel('Generation (MW)')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    apx_data_sorted = apx_data.sort_values('settlementPeriod')
    ax2 = ax1.twinx()
    ax2.plot(apx_data_sorted['settlementPeriod'], apx_data_sorted['price'], linewidth=2, label='Price')
    ax2.set_ylabel('Price (£/MWh)')
    ax2.tick_params(axis='y')
    ax1.legend(bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    plt.show()

def plot_price_volume_comparison(settlement_date: str, nord_pool_df: pd.DataFrame, nord_pool_volumes_df: pd.DataFrame, apx_data: pd.DataFrame) -> None:
    fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(20, 8))
    color = 'tab:red'
    color_sell = 'tab:green'
    ax1.set_xlabel('Hour')
    ax1.set_ylabel('Price (GBP/MWh)', color=color)
    ax1.plot(range(len(nord_pool_df)), nord_pool_df['price'], marker='o', color=color, label='Price', linewidth=2)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Volume (MWh)', color='black')
    ax2.plot(range(len(nord_pool_volumes_df)), nord_pool_volumes_df['sell_volume'], marker='s', color=color_sell, label='Sell Volume', linewidth=2, alpha=0.7)
    ax2.tick_params(axis='y', labelcolor='black')

    ax1.set_xticks(range(len(nord_pool_df)))
    ax1.set_xticklabels(nord_pool_df['period'], rotation=45, ha='right')
    ax1.set_title(f'Nordpool UK Day-Ahead Auction Prices and Trading Volumes {settlement_date}', fontsize=12, pad=15)
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    color_price = 'tab:red'
    color_volume = 'tab:purple'

    ax3.set_xlabel('Settlement Period')
    ax3.set_ylabel('Price (GBP/MWh)', color=color_price)
    apx_data_sorted = apx_data.sort_values('settlementPeriod')
    ax3.plot(apx_data_sorted['settlementPeriod'], apx_data_sorted['price'], marker='o', color=color_price, label='Price', linewidth=2)
    ax3.tick_params(axis='y', labelcolor=color_price)
    ax3.grid(True, alpha=0.3)

    ax4 = ax3.twinx()
    ax4.set_ylabel('Volume (MWh)', color=color_volume)
    ax4.plot(apx_data_sorted['settlementPeriod'], apx_data_sorted['volume'], marker='s', color=color_volume, label='Volume', linewidth=2, alpha=0.7)
    ax4.tick_params(axis='y', labelcolor=color_volume)

    ax3.set_title(f'APX Data 30 min Day Ahead Auction Prices: {settlement_date}', fontsize=12, pad=15)
    ax3.legend(loc='upper left')
    ax4.legend(loc='upper right')

    plt.tight_layout()
    plt.show()

def plot_nordpool_price_volume(settlement_date: str, nord_pool_df: pd.DataFrame, nord_pool_volumes_df: pd.DataFrame) -> None:
    fig, ax1 = plt.subplots(figsize=(12, 6))
    color = 'tab:red'
    color_sell = 'tab:green'

    ax1.set_xlabel('Hour')
    ax1.set_ylabel('Price (GBP/MWh)', color=color)
    ax1.plot(range(len(nord_pool_df)), nord_pool_df['price'], marker='o', color=color, label='Price', linewidth=2)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Volume (MWh)', color='black')
    ax2.plot(range(len(nord_pool_volumes_df)), nord_pool_volumes_df['sell_volume'], marker='s', color=color_sell, label='Sell Volume', linewidth=2, alpha=0.7)
    ax2.tick_params(axis='y', labelcolor='black')

    ax1.set_xticks(range(len(nord_pool_df)))
    ax1.set_xticklabels(nord_pool_df['period'], rotation=45, ha='right')
    ax1.set_title(f'Nordpool UK Day-Ahead Auction Prices and Trading Volumes {settlement_date}', fontsize=12, pad=15)
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.tight_layout()
    plt.show()

def plot_nordpool_comparison(settlement_dates: list[str], nord_pool_data_dict: dict[str, tuple[pd.DataFrame, pd.DataFrame]]) -> None:
    num_dates = len(settlement_dates)
    cols = min(3, num_dates)
    rows = (num_dates + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
    if num_dates == 1:
        axes = [axes]
    elif rows == 1:
        axes = axes.reshape(1, -1)

    color = 'tab:red'
    color_sell = 'tab:green'

    for i, date in enumerate(settlement_dates):
        row = i // cols
        col = i % cols
        ax1 = axes[row, col] if rows > 1 else axes[col]

        nord_pool_df, nord_pool_volumes_df = nord_pool_data_dict[date]

        ax1.set_xlabel('Hour')
        ax1.set_ylabel('Price (GBP/MWh)', color=color)
        ax1.plot(range(len(nord_pool_df)), nord_pool_df['price'], marker='o', color=color, label='Price', linewidth=2)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True, alpha=0.3)

        ax2 = ax1.twinx()
        ax2.set_ylabel('Volume (MWh)', color='black')
        ax2.plot(range(len(nord_pool_volumes_df)), nord_pool_volumes_df['sell_volume'], marker='s', color=color_sell, label='Sell Volume', linewidth=2, alpha=0.7)
        ax2.tick_params(axis='y', labelcolor='black')

        ax1.set_xticks(range(len(nord_pool_df)))
        ax1.set_xticklabels(nord_pool_df['period'], rotation=45, ha='right')
        ax1.set_title(f'NordPool {date}', fontsize=10)

        if i == 0:
            ax1.legend(loc='upper left')
            ax2.legend(loc='upper right')

    for i in range(num_dates, rows * cols):
        row = i // cols
        col = i % cols
        if rows > 1:
            fig.delaxes(axes[row, col])
        else:
            fig.delaxes(axes[col])

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # create_generation_stack_chart('2025-10-17')
    create_percentage_stack_chart('2025-10-17')