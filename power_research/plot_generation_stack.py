import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import pandas as pd
import matplotlib.pyplot as plt
from scrapers.elexon import get_generation_by_fuel

# NOTE: The renewables outturn values are underestimated in this report because they exclude embedded generation 
# and wind farms which do not have Operational Meters. As of 2025, NESO estimates this representation of wind farms 
# with Operational Meters to be approximately 82%.


def create_generation_stack_chart(settlement_date: str) -> None:
    fuel_generation = get_generation_by_fuel(settlement_date)

    if fuel_generation is None:
        print(f"No data available for {settlement_date}")
        return

    fuel_mapping = {'BIOMASS': 'Biomass', 'CCGT': 'CCGT', 'COAL': 'Coal', 'NUCLEAR': 'Nuclear', 'NPSHYD': 'Hydro (non-PS)', 'OCGT': 'OCGT', 'OIL': 'Oil', 'OTHER': 'Other', 'PS': 'Pumped Storage', 'WIND': 'Wind'}
    interconnector_mapping = {'INTELEC': 'Eleclink (INTELEC)', 'INTEW': 'Ireland (East-West)', 'INTFR': 'France (IFA)', 'INTGRNL': 'Ireland (Greenlink)', 'INTIFA2': 'France (IFA2)', 'INTIRL': 'Northern Ireland (Moyle)', 'INTNED': 'Netherlands (BritNed)', 'INTNEM': 'Belgium (Nemolink)', 'INTNSL': 'North Sea Link (INTNSL)', 'INTVKL': 'Denmark (Viking link)'}
    fuel_generation['fuel_category'] = fuel_generation['fuelType'].map(fuel_mapping); fuel_generation.loc[fuel_generation['fuelType'].isin(interconnector_mapping.keys()), 'fuel_category'] = 'Interconnectors'
    pivot_df = fuel_generation.groupby(['settlementPeriod', 'fuel_category'])['generation'].sum().unstack(fill_value=0)
    category_colors = {'Nuclear': '#2b4c85', 'Hydro (non-PS)': '#00a0b0', 'Wind': '#4a9eff', 'Biomass': '#8b4a9c', 'CCGT': '#b85450', 'OCGT': '#90ee90', 'Coal': '#333333', 'Oil': '#7a7a7a', 'Other': '#ff8c42', 'Pumped Storage': '#006080', 'Interconnectors': '#70c1b3'}
    generation_order = ['Nuclear', 'Hydro (non-PS)', 'Wind', 'Biomass', 'CCGT', 'OCGT', 'Coal', 'Oil', 'Other', 'Pumped Storage', 'Interconnectors']
    plt.figure(figsize=(15, 8))
    bottom_pos = pd.Series([0] * len(pivot_df.index), index=pivot_df.index); bottom_neg = pd.Series([0] * len(pivot_df.index), index=pivot_df.index)
    label_positions = [5, 10, 15, 20, 25, 30, 35, 40, 45, 12, 27]
    for i, category in enumerate(generation_order):
        if category in pivot_df.columns:
            values = pivot_df[category]
            color = category_colors.get(category, '#888888')

            positive_vals = values.clip(lower=0); negative_vals = values.clip(upper=0)

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

    plt.xlabel('Settlement Period'); plt.ylabel('Generation (MW)'); plt.title(f'UK Electricity Generation by Fuel Type - {settlement_date}'); 
    plt.grid(True, alpha=0.3); plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left'); plt.tight_layout(); 
    plt.show()

def create_percentage_stack_chart(settlement_date: str) -> None:
    fuel_generation = get_generation_by_fuel(settlement_date)
    if fuel_generation is None:
        print(f"No data available for {settlement_date}")
        return
    fuel_mapping = {'BIOMASS': 'Biomass', 'CCGT': 'CCGT', 'COAL': 'Coal', 'NUCLEAR': 'Nuclear', 'NPSHYD': 'Hydro (non-PS)', 'OCGT': 'OCGT', 'OIL': 'Oil', 'OTHER': 'Other', 'PS': 'Pumped Storage', 'WIND': 'Wind'}
    interconnector_mapping = {'INTELEC': 'Eleclink (INTELEC)', 'INTEW': 'Ireland (East-West)', 'INTFR': 'France (IFA)', 'INTGRNL': 'Ireland (Greenlink)', 'INTIFA2': 'France (IFA2)', 'INTIRL': 'Northern Ireland (Moyle)', 'INTNED': 'Netherlands (BritNed)', 'INTNEM': 'Belgium (Nemolink)', 'INTNSL': 'North Sea Link (INTNSL)', 'INTVKL': 'Denmark (Viking link)'}
    fuel_generation['fuel_category'] = fuel_generation['fuelType'].map(fuel_mapping)
    fuel_generation.loc[fuel_generation['fuelType'].isin(interconnector_mapping.keys()), 'fuel_category'] = 'Interconnectors'
    pivot_df = fuel_generation.groupby(['settlementPeriod', 'fuel_category'])['generation'].sum().unstack(fill_value=0)
    positive_df = pivot_df.clip(lower=0)
    totals = positive_df.sum(axis=1)
    percentage_df = positive_df.div(totals, axis=0) * 100
    category_colors = {'Nuclear': '#2b4c85', 'Hydro (non-PS)': '#00a0b0', 'Wind': '#4a9eff', 'Biomass': '#8b4a9c', 'CCGT': '#b85450', 'OCGT': '#90ee90', 'Coal': '#333333', 'Oil': '#7a7a7a', 'Other': '#ff8c42', 'Pumped Storage': '#006080', 'Interconnectors': '#70c1b3'}
    generation_order = ['Nuclear', 'Hydro (non-PS)', 'Wind', 'Biomass', 'CCGT', 'OCGT', 'Coal', 'Oil', 'Other', 'Pumped Storage', 'Interconnectors']
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

if __name__ == "__main__":
    # create_generation_stack_chart('2025-10-17')
    create_percentage_stack_chart('2025-10-17')