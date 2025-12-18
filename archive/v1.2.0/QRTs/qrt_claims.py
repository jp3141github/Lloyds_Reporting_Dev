"""
PRA/BoE QRT Generator - Claims Templates (IR19-20)
===================================================
Actuarial-focused claims development templates for Solvency II reporting.

Templates:
- IR1901: Non-Life Insurance Claims
- IR1902: Non-Life Claim Development - General Liability Sub-classes
- IR2001: Development of the Distribution of the Claims Incurred
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random
from typing import Dict, List

from .qrt_balance_sheet import (
    UNDERTAKINGS, REPORTING_DATE, NON_LIFE_LOB,
    random_amount, random_percentage
)

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


# ============================================================================
# IR1901 - Non-Life Insurance Claims
# ============================================================================

def generate_ir1901_non_life_claims():
    """
    IR1901 - Non-Life Insurance Claims
    Claims triangles and development analysis for non-life insurance.
    """
    data = []

    accident_years = list(range(2014, 2025))  # 11 years of development
    development_years = list(range(0, 11))

    for undertaking in UNDERTAKINGS:
        for lob in NON_LIFE_LOB[:8]:
            ultimate_by_ay = {ay: random_amount(20_000_000, 150_000_000) for ay in accident_years}

            for accident_year in accident_years:
                ultimate = ultimate_by_ay[accident_year]
                max_dev = 2024 - accident_year  # How developed this AY is

                for dev_year in range(min(max_dev + 1, 11)):
                    # Development pattern
                    if dev_year == 0:
                        cum_pct = 0.35
                    elif dev_year == 1:
                        cum_pct = 0.60
                    elif dev_year == 2:
                        cum_pct = 0.75
                    elif dev_year == 3:
                        cum_pct = 0.85
                    elif dev_year == 4:
                        cum_pct = 0.92
                    else:
                        cum_pct = min(1.0, 0.92 + 0.015 * (dev_year - 4))

                    # Add some randomness
                    cum_pct *= np.random.uniform(0.95, 1.05)

                    row = {
                        'LEI': undertaking['lei'],
                        'Undertaking_Name': undertaking['name'],
                        'Reporting_Date': REPORTING_DATE,
                        'Line_Of_Business': lob,
                        'Accident_Year': accident_year,
                        'Development_Year': dev_year,
                        'Calendar_Year': accident_year + dev_year,
                        'Claims_Paid_Cumulative': round(ultimate * cum_pct, 2),
                        'Claims_Paid_Incremental': round(ultimate * (cum_pct - (0 if dev_year == 0 else cum_pct * 0.85)), 2),
                        'Case_Reserves': round(ultimate * (1 - cum_pct) * 0.6, 2),
                        'IBNR': round(ultimate * (1 - cum_pct) * 0.4, 2),
                        'Incurred_Claims': round(ultimate * (cum_pct + (1 - cum_pct) * 0.7), 2),
                        'Ultimate_Claims': round(ultimate, 2),
                        'Reinsurance_Recoveries_Paid': round(ultimate * cum_pct * np.random.uniform(0.15, 0.30), 2),
                        'Reinsurance_Recoveries_Outstanding': round(ultimate * (1 - cum_pct) * np.random.uniform(0.15, 0.30), 2),
                        'Net_Claims_Paid': round(ultimate * cum_pct * np.random.uniform(0.70, 0.85), 2),
                        'Net_Ultimate': round(ultimate * np.random.uniform(0.70, 0.85), 2),
                        'Claim_Count': random.randint(50, 2000),
                        'Average_Claim_Size': round(ultimate * cum_pct / max(1, random.randint(50, 2000)), 2),
                    }
                    data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR1902 - Non-Life Claim Development - General Liability Sub-classes
# ============================================================================

def generate_ir1902_gl_claims_development():
    """
    IR1902 - Non-Life Claim Development - General Liability Sub-classes
    Detailed claims triangles for general liability lines.
    """
    data = []

    gl_subclasses = [
        'Public Liability',
        'Products Liability',
        'Employers Liability',
        'Professional Indemnity',
        'Directors & Officers',
        'Medical Malpractice',
    ]

    accident_years = list(range(2010, 2025))  # 15 years - longer tail

    for undertaking in UNDERTAKINGS:
        for subclass in gl_subclasses:
            ultimate_by_ay = {ay: random_amount(10_000_000, 80_000_000) for ay in accident_years}

            for accident_year in accident_years:
                ultimate = ultimate_by_ay[accident_year]
                max_dev = 2024 - accident_year

                for dev_year in range(min(max_dev + 1, 15)):
                    # Longer-tail development pattern for GL
                    if dev_year == 0:
                        cum_pct = 0.15
                    elif dev_year == 1:
                        cum_pct = 0.30
                    elif dev_year == 2:
                        cum_pct = 0.45
                    elif dev_year == 3:
                        cum_pct = 0.55
                    elif dev_year == 4:
                        cum_pct = 0.65
                    elif dev_year == 5:
                        cum_pct = 0.73
                    elif dev_year == 6:
                        cum_pct = 0.80
                    elif dev_year == 7:
                        cum_pct = 0.85
                    elif dev_year == 8:
                        cum_pct = 0.89
                    elif dev_year == 9:
                        cum_pct = 0.92
                    else:
                        cum_pct = min(1.0, 0.92 + 0.015 * (dev_year - 9))

                    cum_pct *= np.random.uniform(0.93, 1.07)

                    row = {
                        'LEI': undertaking['lei'],
                        'Undertaking_Name': undertaking['name'],
                        'Reporting_Date': REPORTING_DATE,
                        'GL_Subclass': subclass,
                        'Accident_Year': accident_year,
                        'Development_Year': dev_year,
                        'Calendar_Year': accident_year + dev_year,
                        # Gross
                        'Gross_Paid_Cumulative': round(ultimate * cum_pct, 2),
                        'Gross_Paid_Incremental': round(ultimate * cum_pct * 0.15, 2),
                        'Gross_Case_Reserves': round(ultimate * (1 - cum_pct) * 0.5, 2),
                        'Gross_IBNR': round(ultimate * (1 - cum_pct) * 0.5, 2),
                        'Gross_Incurred': round(ultimate * (cum_pct + (1 - cum_pct) * 0.65), 2),
                        'Gross_Ultimate': round(ultimate, 2),
                        # Reinsurance
                        'RI_Paid': round(ultimate * cum_pct * np.random.uniform(0.20, 0.40), 2),
                        'RI_Outstanding': round(ultimate * (1 - cum_pct) * np.random.uniform(0.20, 0.40), 2),
                        # Net
                        'Net_Paid_Cumulative': round(ultimate * cum_pct * np.random.uniform(0.60, 0.80), 2),
                        'Net_Incurred': round(ultimate * (cum_pct + (1 - cum_pct) * 0.65) * np.random.uniform(0.60, 0.80), 2),
                        'Net_Ultimate': round(ultimate * np.random.uniform(0.60, 0.80), 2),
                        # Large Claims
                        'Large_Claims_Count': random.randint(1, 20),
                        'Large_Claims_Amount': round(ultimate * np.random.uniform(0.20, 0.50), 2),
                        'Large_Claims_Threshold': 1_000_000,
                        # Claim Stats
                        'Total_Claim_Count': random.randint(100, 3000),
                        'Open_Claims': random.randint(10, 500),
                        'Closed_Claims': random.randint(90, 2500),
                    }
                    data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2001 - Development of the Distribution of the Claims Incurred
# ============================================================================

def generate_ir2001_claims_distribution():
    """
    IR2001 - Development of the Distribution of the Claims Incurred
    Statistical distribution analysis of claims development.
    """
    data = []

    development_periods = list(range(0, 16))  # 16 development periods
    percentiles = [10, 25, 50, 75, 90, 95, 99]

    for undertaking in UNDERTAKINGS:
        for lob in NON_LIFE_LOB[:6]:
            base_ultimate = random_amount(50_000_000, 300_000_000)

            for dev_period in development_periods:
                # Generate percentile distribution
                mean_pct = 0.30 + 0.05 * dev_period if dev_period < 14 else 1.0
                std_pct = 0.10 * (1 - dev_period / 16)

                percentile_values = {}
                for pct in percentiles:
                    z_score = (pct - 50) / 25  # Approximate z-score
                    percentile_values[f'P{pct}'] = round(
                        base_ultimate * (mean_pct + z_score * std_pct), 2
                    )

                row = {
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Line_Of_Business': lob,
                    'Development_Period': dev_period,
                    'Mean_Claims': round(base_ultimate * mean_pct, 2),
                    'Std_Dev_Claims': round(base_ultimate * std_pct, 2),
                    'CV': round(std_pct / mean_pct if mean_pct > 0 else 0, 4),
                    **percentile_values,
                    'IQR': percentile_values['P75'] - percentile_values['P25'],
                    'Skewness': round(np.random.uniform(-0.5, 1.5), 4),
                    'Kurtosis': round(np.random.uniform(2.5, 5.0), 4),
                    'Number_Of_Simulations': 10000,
                    'Simulation_Method': 'Bootstrap',
                    # Distribution Parameters
                    'Distribution_Type': random.choice(['LogNormal', 'Gamma', 'Weibull']),
                    'Distribution_Param1': round(np.random.uniform(0.5, 2.0), 4),
                    'Distribution_Param2': round(np.random.uniform(0.1, 1.0), 4),
                }
                data.append(row)

    return pd.DataFrame(data)


# Export all functions
__all__ = [
    'generate_ir1901_non_life_claims',
    'generate_ir1902_gl_claims_development',
    'generate_ir2001_claims_distribution',
]
