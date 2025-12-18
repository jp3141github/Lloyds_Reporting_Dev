"""
RRA 293 Outstanding & IBNR by PYoA - Power BI Python Script
===========================================================

V2.0: Stub processor for form implementation
Form 293 captures outstanding claims and IBNR split by Prior Year of Account (PYoA).

This script processes and validates RRA 293 data for Power BI reporting.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional

# Form metadata
FORM_CODE = '293'
FORM_NAME = 'Outstanding & IBNR by PYoA'
FORM_VERSION = '2.0'


def process_rra_293(data_source: str = '../../synthetic_data/rra_293_outstanding_ibnr_pyoa.csv') -> pd.DataFrame:
    """
    Process RRA 293 Outstanding & IBNR by PYoA data for Power BI

    Form 293 Fields (expected):
    ---------------------------
    - Syndicate_Number: Lloyd's syndicate number
    - Year_of_Account: Current YoA
    - Prior_YoA: Prior year of account
    - Class_of_Business: SCOB code
    - Gross_Outstanding_GBP: Gross outstanding claims
    - Gross_IBNR_GBP: Gross IBNR
    - Net_Outstanding_GBP: Net outstanding claims
    - Net_IBNR_GBP: Net IBNR
    - Currency: Original currency
    """

    df = pd.read_csv(data_source)

    # Add calculated fields
    df['Gross_Total_GBP'] = df['Gross_Outstanding_GBP'] + df['Gross_IBNR_GBP']
    df['Net_Total_GBP'] = df['Net_Outstanding_GBP'] + df['Net_IBNR_GBP']
    df['Gross_Total_Millions'] = df['Gross_Total_GBP'] / 1_000_000
    df['Net_Total_Millions'] = df['Net_Total_GBP'] / 1_000_000

    # Calculate RI recovery
    df['RI_Outstanding'] = df['Gross_Outstanding_GBP'] - df['Net_Outstanding_GBP']
    df['RI_IBNR'] = df['Gross_IBNR_GBP'] - df['Net_IBNR_GBP']

    # Age of PYoA
    df['PYoA_Age'] = df['Year_of_Account'] - df['Prior_YoA']

    return df


def get_pyoa_summary(data_source: str = '../../synthetic_data/rra_293_outstanding_ibnr_pyoa.csv') -> pd.DataFrame:
    """Generate summary by PYoA age"""
    df = process_rra_293(data_source)

    summary = df.groupby('PYoA_Age').agg({
        'Gross_Total_GBP': 'sum',
        'Net_Total_GBP': 'sum',
        'Syndicate_Number': 'nunique'
    }).reset_index()

    summary.columns = ['PYoA_Age', 'Gross_Total', 'Net_Total', 'Syndicate_Count']
    summary['Gross_Millions'] = summary['Gross_Total'] / 1_000_000
    return summary


def validate_rra_293(data_source: str = '../../synthetic_data/rra_293_outstanding_ibnr_pyoa.csv') -> pd.DataFrame:
    """Validate RRA 293 data"""
    df = pd.read_csv(data_source)

    validations = []

    # Check Prior YoA <= Current YoA
    if 'Prior_YoA' in df.columns and 'Year_of_Account' in df.columns:
        invalid = df['Prior_YoA'] > df['Year_of_Account']
        validations.append({
            'Rule': 'Prior YoA <= Current YoA',
            'Status': 'FAIL' if invalid.any() else 'PASS',
            'Records_Affected': int(invalid.sum()),
            'Severity': 'Critical'
        })

    # Check Net <= Gross
    invalid_os = df['Net_Outstanding_GBP'] > df['Gross_Outstanding_GBP']
    validations.append({
        'Rule': 'Net Outstanding <= Gross',
        'Status': 'FAIL' if invalid_os.any() else 'PASS',
        'Records_Affected': int(invalid_os.sum()),
        'Severity': 'Warning'
    })

    return pd.DataFrame(validations)


if __name__ == "__main__":
    print(f"RRA {FORM_CODE} - {FORM_NAME}")
    print("=" * 60)
    print(f"Version: {FORM_VERSION}")
