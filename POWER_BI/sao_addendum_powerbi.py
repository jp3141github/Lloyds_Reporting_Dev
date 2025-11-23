"""
SAO Addendum Return Data Generator for Power BI
================================================
Generates SAO (Signing Actuary Opinion) Addendum Return data for Lloyd's syndicates.
Compatible with Power BI as a Python data source.

Tables Generated:
- specific_ibnr: 090 Specific IBNR data
- movements_ave: 100 Movements and Actual vs Expected Analysis
- movements_ave_summary: 100 Summary statistics

Usage in Power BI:
1. Get Data > More > Python script
2. Copy and paste this script
3. Select the tables you need from the list
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


def _get_year_weights(years):
    """Generate probability weights favoring more recent underwriting years."""
    n = len(years)
    weights = np.exp(np.linspace(-2, 0, n))
    return weights / weights.sum()


def generate_specific_ibnr_data(num_records=50):
    """
    Generate synthetic Specific IBNR data for Lloyd's SAO Addendum Return (Form 090).
    """
    # Define Lloyd's CAT codes
    cat_codes = [
        '22E', '21E', '23E', '24E', '25E',
        '26E', '27E', '28E', '29E', '30E',
        'Non Nat-Cat'
    ]

    # Define reserving classes
    reserving_classes = [
        'Prop Cat XL', 'Marine Hull', 'Aviation', 'Energy', 'Casualty',
        'D&O US', 'D&O UK', 'Professional Indemnity', 'Cyber',
        'Motor', 'Property Treaty', 'Property Direct', 'Marine Cargo',
        'Terrorism', 'Political Risk', 'Credit & Bond', 'Accident & Health'
    ]

    # Define Lloyd's Lines of Business
    lloyds_lobs = [
        'Property Cat XL', 'Marine Hull', 'Aviation', 'Energy Offshore',
        'Casualty Treaty', 'D&O', 'Professional Indemnity', 'Cyber',
        'Motor', 'Property Treaty', 'Property Direct', 'Marine Cargo',
        'Terrorism', 'Political Risk', 'Credit & Surety', 'Accident & Health'
    ]

    underwriting_years = list(range(2010, 2026))

    data = []

    for _ in range(num_records):
        cat_code = np.random.choice(cat_codes)
        reserving_class = np.random.choice(reserving_classes)

        lob_index = reserving_classes.index(reserving_class) % len(lloyds_lobs)
        lloyds_lob = lloyds_lobs[lob_index]

        uw_year = np.random.choice(underwriting_years, p=_get_year_weights(underwriting_years))
        num_losses = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.15, 0.07, 0.03])

        gross_ibnr = np.random.lognormal(mean=np.log(10000), sigma=0.8)
        gross_ibnr = max(1000, round(gross_ibnr, 0))

        net_percentage = np.random.uniform(0.70, 0.95)
        net_ibnr = round(gross_ibnr * net_percentage, 0)

        comments = [
            'Reserved using underlying cedant exposure and loss advice plus assumption on limits losses',
            'Based on industry loss estimates and exposure analysis',
            'Derived from actuarial model with management adjustments',
            'Estimated based on similar historical events',
            'Reserve includes uncertainty loading for emerging claims',
            'Subject to significant uncertainty due to limited data',
            ''
        ]
        comment = np.random.choice(comments, p=[0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.10])

        record = {
            'Reserving Class': reserving_class,
            'Lloyds Cat Code': cat_code,
            'Lloyds Line of Business': lloyds_lob,
            'Number of losses': int(num_losses),
            'Underwriting Year': int(uw_year),
            'Gross IBNR (GBP 000s)': int(gross_ibnr),
            'Net IBNR (GBP 000s)': int(net_ibnr),
            'Comment': comment if comment else np.nan
        }

        data.append(record)

    df = pd.DataFrame(data)
    df = df.sort_values(['Underwriting Year', 'Reserving Class'], ascending=[False, True])
    df = df.reset_index(drop=True)

    return df


def generate_movements_ave_data(num_classes=10):
    """
    Generate synthetic Movements and Actual vs Expected Analysis data (Form 100).
    """
    reserving_classes = [
        'Property Treaty', 'Casualty XL', 'Marine Hull', 'Aviation',
        'Energy Offshore', 'Professional Indemnity', 'D&O US',
        'Cyber', 'Motor', 'Property Direct'
    ][:num_classes]

    lloyds_lobs = [
        'Property Treaty', 'Casualty Treaty', 'Marine Hull', 'Aviation',
        'Energy Offshore', 'Professional Indemnity', 'D&O',
        'Cyber', 'Motor', 'Property Direct'
    ][:num_classes]

    underwriting_years = [2023, 2024, 2025]
    year_labels = ['2023 & Prior', '2024', '2025']

    data = []

    for class_idx, (res_class, lob) in enumerate(zip(reserving_classes, lloyds_lobs)):
        for uw_year, uw_label in zip(underwriting_years, year_labels):
            is_reporting_year = 1 if uw_year == 2025 else 0

            if uw_year == 2023:
                base_premium = np.random.uniform(5000, 15000)
            elif uw_year == 2024:
                base_premium = np.random.uniform(15000, 30000)
            else:
                base_premium = np.random.uniform(20000, 50000)

            ultimate_premium = round(base_premium * (1 + np.random.normal(0, 0.1)), 0)
            ielr = round(np.random.uniform(50, 75), 1)
            ulr = round(ielr + np.random.normal(0, 5), 1)

            if uw_year == 2023:
                ave_pct = round(np.random.normal(2, 5), 1)
            elif uw_year == 2024:
                ave_pct = round(np.random.normal(0, 3), 1)
            else:
                ave_pct = round(np.random.normal(-1, 2), 1)

            reserves_2024ye = round(ultimate_premium * ulr / 100 * np.random.uniform(0.3, 0.8), 0)
            reserves_2025ye = round(ultimate_premium * ulr / 100 * np.random.uniform(0.2, 0.7), 0)
            syndicate_estimate_2025ye = round(reserves_2025ye * (1 + np.random.normal(0, 0.05)), 0)

            record = {
                'Class ID': f'{class_idx + 1:02d}',
                'Reserving Class': res_class,
                'Lloyds Line of Business': lob,
                'Underwriting Year': uw_label,
                'Reporting Year Flag': is_reporting_year,
                'Ultimate Premium (GBP 000s)': int(ultimate_premium),
                'Actual vs Expected Pct': ave_pct,
                'Initial Expected Loss Ratio Pct': ielr,
                'Ultimate Loss Ratio Pct': ulr,
                'Reserves 2024YE (GBP 000s)': int(reserves_2024ye),
                'Reserves 2025YE (GBP 000s)': int(reserves_2025ye),
                'Syndicate Estimate 2025YE (GBP 000s)': int(syndicate_estimate_2025ye)
            }

            data.append(record)

    df = pd.DataFrame(data)
    df = df.sort_values(['Class ID', 'Underwriting Year'])
    df = df.reset_index(drop=True)

    return df


def generate_movements_ave_summary(movements_ave_df):
    """Generate summary data for movements and AvE analysis."""
    summary_data = []

    for uw_year in ['2023 & Prior', '2024', '2025']:
        year_data = movements_ave_df[movements_ave_df['Underwriting Year'] == uw_year]

        summary = {
            'Metric': f'Total - {uw_year}',
            'Ultimate Premium (GBP 000s)': int(year_data['Ultimate Premium (GBP 000s)'].sum()),
            'Reserves 2024YE (GBP 000s)': int(year_data['Reserves 2024YE (GBP 000s)'].sum()),
            'Reserves 2025YE (GBP 000s)': int(year_data['Reserves 2025YE (GBP 000s)'].sum()),
            'Syndicate Estimate 2025YE (GBP 000s)': int(year_data['Syndicate Estimate 2025YE (GBP 000s)'].sum()),
            'Avg ULR Pct': round(year_data['Ultimate Loss Ratio Pct'].mean(), 1),
            'Avg AvE Pct': round(year_data['Actual vs Expected Pct'].mean(), 1)
        }

        summary_data.append(summary)

    grand_total = {
        'Metric': 'Grand Total',
        'Ultimate Premium (GBP 000s)': int(movements_ave_df['Ultimate Premium (GBP 000s)'].sum()),
        'Reserves 2024YE (GBP 000s)': int(movements_ave_df['Reserves 2024YE (GBP 000s)'].sum()),
        'Reserves 2025YE (GBP 000s)': int(movements_ave_df['Reserves 2025YE (GBP 000s)'].sum()),
        'Syndicate Estimate 2025YE (GBP 000s)': int(movements_ave_df['Syndicate Estimate 2025YE (GBP 000s)'].sum()),
        'Avg ULR Pct': round(movements_ave_df['Ultimate Loss Ratio Pct'].mean(), 1),
        'Avg AvE Pct': round(movements_ave_df['Actual vs Expected Pct'].mean(), 1)
    }
    summary_data.append(grand_total)

    return pd.DataFrame(summary_data)


# =============================================================================
# GENERATE ALL TABLES FOR POWER BI
# =============================================================================
print("Generating SAO Addendum Data for Power BI...")
print("=" * 60)

# Generate SAO Addendum tables (these will be available in Power BI)
specific_ibnr = generate_specific_ibnr_data(num_records=50)
movements_ave = generate_movements_ave_data(num_classes=10)
movements_ave_summary = generate_movements_ave_summary(movements_ave)

print(f"specific_ibnr (Form 090): {len(specific_ibnr)} records")
print(f"movements_ave (Form 100): {len(movements_ave)} records")
print(f"movements_ave_summary (Form 100 Summary): {len(movements_ave_summary)} records")
print("=" * 60)
print(f"Total Gross IBNR: GBP {specific_ibnr['Gross IBNR (GBP 000s)'].sum():,.0f}k")
print(f"Total Net IBNR: GBP {specific_ibnr['Net IBNR (GBP 000s)'].sum():,.0f}k")
print(f"Total Ultimate Premium: GBP {movements_ave['Ultimate Premium (GBP 000s)'].sum():,.0f}k")
print("=" * 60)
print("SAO Addendum data generated successfully!")
