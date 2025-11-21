"""
SAO Addendum Return - 100 Movements and Actual vs Expected Analysis Data Generator
===================================================================================
This script generates synthetic Lloyd's of London data for the 100 Movements and AvE analysis table.
Compatible with Power BI as a Python data source.

Usage in Power BI:
1. Get Data > More > Python script
2. Copy and paste this script
3. Select the 'movements_ave' table

Author: Claude
Date: 2025-11-21
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(123)

def generate_movements_ave_data(num_classes=10):
    """
    Generate synthetic Movements and Actual vs Expected Analysis data.

    This creates data for the top 10 largest classes by total net reserves,
    with analysis by underwriting year.

    Parameters:
    -----------
    num_classes : int
        Number of reserving classes to generate (default 10, as per instructions)

    Returns:
    --------
    pandas.DataFrame
        Synthetic Movements and AvE analysis data
    """

    # Define reserving classes (top 10 by reserves)
    reserving_classes = [
        'Property Treaty', 'Casualty XL', 'Marine Hull', 'Aviation',
        'Energy Offshore', 'Professional Indemnity', 'D&O US',
        'Cyber', 'Motor', 'Property Direct'
    ][:num_classes]

    # Define Lloyd's Lines of Business
    lloyds_lobs = [
        'Property Treaty', 'Casualty Treaty', 'Marine Hull', 'Aviation',
        'Energy Offshore', 'Professional Indemnity', 'D&O',
        'Cyber', 'Motor', 'Property Direct'
    ][:num_classes]

    # Underwriting years to analyze
    underwriting_years = [2023, 2024, 2025]
    year_labels = ['2023 & Prior', '2024', '2025']

    data = []

    for class_idx, (res_class, lob) in enumerate(zip(reserving_classes, lloyds_lobs)):
        for uw_year, uw_label in zip(underwriting_years, year_labels):
            # Reporting year indicator (1 for current year, 0 for prior years)
            is_reporting_year = 1 if uw_year == 2025 else 0

            # Ultimate Premium (£000s) - decreases for older years
            if uw_year == 2023:
                base_premium = np.random.uniform(5000, 15000)
            elif uw_year == 2024:
                base_premium = np.random.uniform(15000, 30000)
            else:  # 2025
                base_premium = np.random.uniform(20000, 50000)

            ultimate_premium = round(base_premium * (1 + np.random.normal(0, 0.1)), 0)

            # Initial Expected Loss Ratio (IELR) - typically 50-75%
            ielr = round(np.random.uniform(50, 75), 1)

            # Ultimate Loss Ratio (ULR) - varies around IELR
            ulr = round(ielr + np.random.normal(0, 5), 1)

            # Actual vs Expected as % of ultimate premium
            # Positive = movement in excess of expectations
            # More volatility for older years due to development
            if uw_year == 2023:
                ave_pct = round(np.random.normal(2, 5), 1)
            elif uw_year == 2024:
                ave_pct = round(np.random.normal(0, 3), 1)
            else:  # 2025
                ave_pct = round(np.random.normal(-1, 2), 1)

            # Reserves at 2024 YE (£000s)
            reserves_2024ye = round(ultimate_premium * ulr / 100 * np.random.uniform(0.3, 0.8), 0)

            # Reserves at 2025 YE (£000s)
            reserves_2025ye = round(ultimate_premium * ulr / 100 * np.random.uniform(0.2, 0.7), 0)

            # Syndicate estimate at 2025 YE (may differ from Signing Actuary)
            syndicate_estimate_2025ye = round(reserves_2025ye * (1 + np.random.normal(0, 0.05)), 0)

            record = {
                'Class ID': f'{class_idx + 1:02d}',
                'Reserving Class': res_class,
                "Lloyd's Line of Business": lob,
                'Underwriting Year': uw_label,
                'Reporting Year?': is_reporting_year,
                'Ultimate Premium (£000s)': int(ultimate_premium),
                'Actual vs Expected as % of ultimate premium': ave_pct,
                'Initial Expected Loss Ratio (IELR) (%)': ielr,
                'Ultimate Loss Ratio (ULR) (%)': ulr,
                'Reserves 2024YE (£000s)': int(reserves_2024ye),
                'Reserves 2025YE (£000s)': int(reserves_2025ye),
                'Syndicate Estimate - 2025YE (£000s)': int(syndicate_estimate_2025ye)
            }

            data.append(record)

    df = pd.DataFrame(data)

    # Sort by Class ID and Underwriting Year
    df = df.sort_values(['Class ID', 'Underwriting Year'])
    df = df.reset_index(drop=True)

    return df


def generate_summary_data(movements_ave_df):
    """
    Generate summary data for all classes combined.

    Parameters:
    -----------
    movements_ave_df : pandas.DataFrame
        The main movements and AvE analysis data

    Returns:
    --------
    pandas.DataFrame
        Summary statistics
    """

    summary_data = []

    for uw_year in ['2023 & Prior', '2024', '2025']:
        year_data = movements_ave_df[movements_ave_df['Underwriting Year'] == uw_year]

        summary = {
            'Metric': f'Total - {uw_year}',
            'Ultimate Premium (£000s)': int(year_data['Ultimate Premium (£000s)'].sum()),
            'Reserves 2024YE (£000s)': int(year_data['Reserves 2024YE (£000s)'].sum()),
            'Reserves 2025YE (£000s)': int(year_data['Reserves 2025YE (£000s)'].sum()),
            'Syndicate Estimate - 2025YE (£000s)': int(year_data['Syndicate Estimate - 2025YE (£000s)'].sum()),
            'Avg ULR (%)': round(year_data['Ultimate Loss Ratio (ULR) (%)'].mean(), 1),
            'Avg AvE (%)': round(year_data['Actual vs Expected as % of ultimate premium'].mean(), 1)
        }

        summary_data.append(summary)

    # Grand total
    grand_total = {
        'Metric': 'Grand Total',
        'Ultimate Premium (£000s)': int(movements_ave_df['Ultimate Premium (£000s)'].sum()),
        'Reserves 2024YE (£000s)': int(movements_ave_df['Reserves 2024YE (£000s)'].sum()),
        'Reserves 2025YE (£000s)': int(movements_ave_df['Reserves 2025YE (£000s)'].sum()),
        'Syndicate Estimate - 2025YE (£000s)': int(movements_ave_df['Syndicate Estimate - 2025YE (£000s)'].sum()),
        'Avg ULR (%)': round(movements_ave_df['Ultimate Loss Ratio (ULR) (%)'].mean(), 1),
        'Avg AvE (%)': round(movements_ave_df['Actual vs Expected as % of ultimate premium'].mean(), 1)
    }
    summary_data.append(grand_total)

    return pd.DataFrame(summary_data)


# Generate the data
movements_ave = generate_movements_ave_data(num_classes=10)
movements_ave_summary = generate_summary_data(movements_ave)

# Display summary statistics
print("=" * 80)
print("SAO Addendum Return - 100 Movements and AvE Analysis Summary")
print("=" * 80)
print(f"Total Classes: {movements_ave['Reserving Class'].nunique()}")
print(f"Total Records: {len(movements_ave)}")
print(f"Total Ultimate Premium: £{movements_ave['Ultimate Premium (£000s)'].sum():,.0f}k")
print(f"Total Reserves (2025YE): £{movements_ave['Reserves 2025YE (£000s)'].sum():,.0f}k")
print("=" * 80)
print("\nSummary by Underwriting Year:")
print(movements_ave_summary.to_string(index=False))
print("\n" + "=" * 80)
print("\nFirst 15 records:")
print(movements_ave.head(15).to_string(index=False))
print("\n")

# These tables will be available in Power BI
# Power BI will automatically detect the 'movements_ave' and 'movements_ave_summary' dataframes
