"""
SAO Addendum Return - 090 Specific IBNR Data Generator
======================================================
This script generates synthetic Lloyd's of London data for the 090 Specific IBNR table.
Compatible with Power BI as a Python data source.

Usage in Power BI:
1. Get Data > More > Python script
2. Copy and paste this script
3. Select the 'specific_ibnr' table

Author: Claude
Date: 2025-11-21
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)

def generate_specific_ibnr_data(num_records=50):
    """
    Generate synthetic Specific IBNR data for Lloyd's SAO Addendum Return.

    Parameters:
    -----------
    num_records : int
        Number of records to generate

    Returns:
    --------
    pandas.DataFrame
        Synthetic Specific IBNR data
    """

    # Define Lloyd's CAT codes (Natural catastrophes)
    cat_codes = [
        '22E', '21E', '23E', '24E', '25E',  # Historic CAT events
        '26E', '27E', '28E', '29E', '30E',
        'Non Nat-Cat'  # Non-natural catastrophe events
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

    # Underwriting years (Lloyd's reporting typically covers multiple years)
    underwriting_years = list(range(2010, 2026))

    data = []

    for _ in range(num_records):
        cat_code = np.random.choice(cat_codes)
        reserving_class = np.random.choice(reserving_classes)

        # Map reserving class to appropriate Lloyd's LoB
        lob_index = reserving_classes.index(reserving_class) % len(lloyds_lobs)
        lloyds_lob = lloyds_lobs[lob_index]

        # Generate random underwriting year (more recent years more likely)
        uw_year = np.random.choice(underwriting_years, p=_get_year_weights(underwriting_years))

        # Number of losses (typically 1-5 for specific IBNR)
        num_losses = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.15, 0.07, 0.03])

        # Gross IBNR (£000s) - range from £1,000k to £50,000k (i.e., £1m to £50m gross)
        # Using lognormal distribution: mean=log(10000), sigma=0.8 gives good range
        gross_ibnr = np.random.lognormal(mean=np.log(10000), sigma=0.8)
        gross_ibnr = max(1000, round(gross_ibnr, 0))

        # Net IBNR (70-95% of gross, accounting for reinsurance)
        net_percentage = np.random.uniform(0.70, 0.95)
        net_ibnr = round(gross_ibnr * net_percentage, 0)

        # Generate comment for some records
        comments = [
            'Reserved using underlying cedant exposure and loss advice plus assumption on limits losses',
            'Based on industry loss estimates and exposure analysis',
            'Derived from actuarial model with management adjustments',
            'Estimated based on similar historical events',
            'Reserve includes uncertainty loading for emerging claims',
            'Subject to significant uncertainty due to limited data',
            ''  # Some entries have no comment
        ]
        comment = np.random.choice(comments, p=[0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.10])

        record = {
            'Reserving Class': reserving_class,
            "Lloyd's Cat Code": cat_code,
            "Lloyd's Line of Business": lloyds_lob,
            'Number of losses': int(num_losses),
            'Underwriting Year': int(uw_year),
            'Gross IBNR (£000s)': int(gross_ibnr),
            'Net IBNR (£000s)': int(net_ibnr),
            'Comment (optional)': comment if comment else np.nan
        }

        data.append(record)

    df = pd.DataFrame(data)

    # Sort by Underwriting Year and Reserving Class
    df = df.sort_values(['Underwriting Year', 'Reserving Class'], ascending=[False, True])
    df = df.reset_index(drop=True)

    return df


def _get_year_weights(years):
    """
    Generate probability weights favoring more recent underwriting years.

    Parameters:
    -----------
    years : list
        List of underwriting years

    Returns:
    --------
    numpy.array
        Normalized probability weights
    """
    n = len(years)
    # Exponential decay - more recent years have higher probability
    weights = np.exp(np.linspace(-2, 0, n))
    return weights / weights.sum()


# Generate the data
specific_ibnr = generate_specific_ibnr_data(num_records=50)

# Display summary statistics
print("=" * 80)
print("SAO Addendum Return - 090 Specific IBNR Summary")
print("=" * 80)
print(f"Total Records: {len(specific_ibnr)}")
print(f"Total Gross IBNR: £{specific_ibnr['Gross IBNR (£000s)'].sum():,.0f}k")
print(f"Total Net IBNR: £{specific_ibnr['Net IBNR (£000s)'].sum():,.0f}k")
print(f"Underwriting Years: {specific_ibnr['Underwriting Year'].min()} - {specific_ibnr['Underwriting Year'].max()}")
cat_code_col = "Lloyd's Cat Code"
num_cat = specific_ibnr[specific_ibnr[cat_code_col] != 'Non Nat-Cat'].shape[0]
num_non_cat = specific_ibnr[specific_ibnr[cat_code_col] == 'Non Nat-Cat'].shape[0]
print(f"Number of CAT Events: {num_cat}")
print(f"Number of Non Nat-Cat Events: {num_non_cat}")
print("=" * 80)
print("\nFirst 10 records:")
print(specific_ibnr.head(10).to_string(index=False))
print("\n")

# This table will be available in Power BI
# Power BI will automatically detect the 'specific_ibnr' dataframe
