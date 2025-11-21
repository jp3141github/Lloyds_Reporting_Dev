"""
Power BI Python Query Script
=============================

This script is designed to be used directly in Power BI's Python script data source.

Instructions for Power BI:
1. Open Power BI Desktop
2. Get Data > More > Other > Python script
3. Copy and paste this entire script
4. Click OK

The script will generate synthetic Lloyd's FSCS data and return a dataset
that can be used for reporting and visualization.
"""

import pandas as pd
import numpy as np
from datetime import date
import random


def generate_fscs_data(num_syndicates=15, reporting_year=2024):
    """
    Generate FSCS data for Power BI consumption.

    This is a self-contained version for Power BI that doesn't rely on external modules.
    """
    np.random.seed(42)
    random.seed(42)

    # Generate syndicate numbers
    syndicates = sorted(random.sample(range(2000, 6000), num_syndicates))

    data = []

    for syndicate in syndicates:
        # Generate GWP for general business (£10M to £500M)
        gwp_general = np.random.lognormal(mean=np.log(150_000_000), sigma=0.5)
        gwp_general = np.clip(gwp_general, 10_000_000, 500_000_000)
        if random.random() < 0.2:
            gwp_general = 0

        # Generate GWP for life business (£1M to £100M)
        gwp_life = np.random.lognormal(mean=np.log(30_000_000), sigma=0.5)
        gwp_life = np.clip(gwp_life, 1_000_000, 100_000_000)
        if random.random() < 0.2:
            gwp_life = 0

        # Generate BEL for general business (1.5-3x GWP)
        bel_general = gwp_general * np.random.uniform(1.5, 3.0) * np.random.uniform(0.8, 1.2)
        if gwp_general == 0:
            bel_general = np.random.uniform(0, 5_000_000)

        # Generate BEL for life business (3-8x GWP)
        bel_life = gwp_life * np.random.uniform(3.0, 8.0) * np.random.uniform(0.8, 1.2)
        if gwp_life == 0:
            bel_life = np.random.uniform(0, 5_000_000)

        data.append({
            'Syndicate_Number': syndicate,
            'Reporting_Year': reporting_year,
            'Reporting_Date': date(reporting_year, 12, 31),
            'Managing_Agent': f"MA_{random.randint(100, 999)}",
            'GWP_General_Business_GBP': round(gwp_general, 2),
            'GWP_Life_Business_GBP': round(gwp_life, 2),
            'GWP_Total_GBP': round(gwp_general + gwp_life, 2),
            'BEL_General_Business_GBP': round(bel_general, 2),
            'BEL_Life_Business_GBP': round(bel_life, 2),
            'BEL_Total_GBP': round(bel_general + bel_life, 2),
            'General_Business_Percentage': round(
                (gwp_general / (gwp_general + gwp_life) * 100) if (gwp_general + gwp_life) > 0 else 0,
                2
            ),
            'Data_Quality_Flag': 'Synthetic',
            'Notes': 'Protected contracts with eligible claimants only'
        })

    return pd.DataFrame(data)


# This is the main execution block that Power BI will run
# Power BI expects a DataFrame to be assigned to a variable for output

# Generate the data
dataset = generate_fscs_data(num_syndicates=15, reporting_year=2024)

# Power BI will automatically detect and use this DataFrame
# You can reference this as 'dataset' in subsequent transformations
print(f"Generated {len(dataset)} syndicate records for FSCS reporting")
