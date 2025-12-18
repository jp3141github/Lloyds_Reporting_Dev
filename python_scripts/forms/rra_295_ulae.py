"""
RRA 295 ULAE - Power BI Python Script
=====================================

V2.0: Stub processor for form implementation
Form 295 captures Unallocated Loss Adjustment Expenses (ULAE).

This script processes and validates RRA 295 ULAE data for Power BI reporting.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional

# Form metadata
FORM_CODE = '295'
FORM_NAME = 'ULAE'
FORM_VERSION = '2.0'


def process_rra_295(data_source: str = '../../synthetic_data/rra_295_ulae.csv') -> pd.DataFrame:
    """
    Process RRA 295 ULAE data for Power BI

    Form 295 Fields (expected):
    ---------------------------
    - Syndicate_Number: Lloyd's syndicate number
    - Year_of_Account: YoA
    - ULAE_Category: Category (Internal/External)
    - Expense_Type: Type of expense
    - Gross_ULAE_GBP: Gross ULAE amount
    - Net_ULAE_GBP: Net ULAE amount
    - Allocation_Method: Method used for allocation
    - Basis_Premium_GBP: Premium base for ratio calculation
    """

    df = pd.read_csv(data_source)

    # Add calculated fields
    df['Gross_ULAE_Millions'] = df['Gross_ULAE_GBP'] / 1_000_000
    df['Net_ULAE_Millions'] = df['Net_ULAE_GBP'] / 1_000_000

    # ULAE ratio
    df['ULAE_Ratio'] = np.where(
        df['Basis_Premium_GBP'] > 0,
        df['Gross_ULAE_GBP'] / df['Basis_Premium_GBP'] * 100,
        0
    )

    df['Is_Internal'] = df['ULAE_Category'] == 'Internal'

    return df


def get_ulae_summary(data_source: str = '../../synthetic_data/rra_295_ulae.csv') -> pd.DataFrame:
    """Generate ULAE summary by category"""
    df = process_rra_295(data_source)

    summary = df.groupby('ULAE_Category').agg({
        'Gross_ULAE_GBP': 'sum',
        'Net_ULAE_GBP': 'sum',
        'Syndicate_Number': 'nunique'
    }).reset_index()

    summary.columns = ['Category', 'Gross_ULAE', 'Net_ULAE', 'Syndicate_Count']
    summary['Gross_Millions'] = summary['Gross_ULAE'] / 1_000_000
    return summary


def validate_rra_295(data_source: str = '../../synthetic_data/rra_295_ulae.csv') -> pd.DataFrame:
    """Validate RRA 295 ULAE data"""
    df = pd.read_csv(data_source)

    validations = []

    # Check ULAE is non-negative
    invalid = df['Gross_ULAE_GBP'] < 0
    validations.append({
        'Rule': 'Gross ULAE Non-Negative',
        'Status': 'FAIL' if invalid.any() else 'PASS',
        'Records_Affected': int(invalid.sum()),
        'Severity': 'Warning'
    })

    # Check valid categories
    valid_cats = ['Internal', 'External']
    if 'ULAE_Category' in df.columns:
        invalid_cat = ~df['ULAE_Category'].isin(valid_cats)
        validations.append({
            'Rule': 'Valid ULAE Category',
            'Status': 'FAIL' if invalid_cat.any() else 'PASS',
            'Records_Affected': int(invalid_cat.sum()),
            'Severity': 'Warning'
        })

    return pd.DataFrame(validations)


if __name__ == "__main__":
    print(f"RRA {FORM_CODE} - {FORM_NAME}")
    print("=" * 60)
    print(f"Version: {FORM_VERSION}")
