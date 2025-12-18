"""
RRA 391 IELR - Power BI Python Script
=====================================

V2.0: Stub processor for form implementation
Form 391 captures Initial Expected Loss Ratios (IELR) used for reserving.

This script processes and validates RRA 391 IELR data for Power BI reporting.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional

# Form metadata
FORM_CODE = '391'
FORM_NAME = 'IELR'
FORM_VERSION = '2.0'


def process_rra_391(data_source: str = '../../synthetic_data/rra_391_ielr.csv') -> pd.DataFrame:
    """
    Process RRA 391 IELR data for Power BI

    Form 391 Fields (expected):
    ---------------------------
    - Syndicate_Number: Lloyd's syndicate number
    - Year_of_Account: YoA
    - Class_of_Business: SCOB code
    - Reserving_Class: Reserving class code
    - Initial_ELR: Initial expected loss ratio (%)
    - Current_ELR: Current expected loss ratio (%)
    - Gross_Premium_GBP: Gross written premium
    - Selected_Ultimate_GBP: Selected ultimate claims
    - Method: Selection method
    """

    df = pd.read_csv(data_source)

    # Add calculated fields
    df['Premium_Millions'] = df['Gross_Premium_GBP'] / 1_000_000
    df['Ultimate_Millions'] = df['Selected_Ultimate_GBP'] / 1_000_000

    # Implied loss ratio from selected ultimate
    df['Implied_LR'] = np.where(
        df['Gross_Premium_GBP'] > 0,
        df['Selected_Ultimate_GBP'] / df['Gross_Premium_GBP'] * 100,
        0
    )

    # ELR change
    df['ELR_Change'] = df['Current_ELR'] - df['Initial_ELR']
    df['ELR_Change_Pct'] = np.where(
        df['Initial_ELR'] > 0,
        df['ELR_Change'] / df['Initial_ELR'] * 100,
        0
    )

    return df


def get_ielr_summary(data_source: str = '../../synthetic_data/rra_391_ielr.csv') -> pd.DataFrame:
    """Generate IELR summary by class"""
    df = process_rra_391(data_source)

    summary = df.groupby('Class_of_Business').agg({
        'Initial_ELR': 'mean',
        'Current_ELR': 'mean',
        'Gross_Premium_GBP': 'sum',
        'Selected_Ultimate_GBP': 'sum'
    }).reset_index()

    summary.columns = ['Class', 'Avg_Initial_ELR', 'Avg_Current_ELR', 'Total_Premium', 'Total_Ultimate']
    summary['Premium_M'] = summary['Total_Premium'] / 1_000_000
    summary['Ultimate_M'] = summary['Total_Ultimate'] / 1_000_000
    summary['Aggregate_LR'] = summary['Total_Ultimate'] / summary['Total_Premium'] * 100
    return summary


def validate_rra_391(data_source: str = '../../synthetic_data/rra_391_ielr.csv') -> pd.DataFrame:
    """Validate RRA 391 IELR data"""
    df = pd.read_csv(data_source)

    validations = []

    # Check ELR in reasonable range (0-200%)
    if 'Initial_ELR' in df.columns:
        invalid = (df['Initial_ELR'] < 0) | (df['Initial_ELR'] > 200)
        validations.append({
            'Rule': 'Initial ELR 0-200%',
            'Status': 'FAIL' if invalid.any() else 'PASS',
            'Records_Affected': int(invalid.sum()),
            'Severity': 'Warning'
        })

    if 'Current_ELR' in df.columns:
        invalid = (df['Current_ELR'] < 0) | (df['Current_ELR'] > 200)
        validations.append({
            'Rule': 'Current ELR 0-200%',
            'Status': 'FAIL' if invalid.any() else 'PASS',
            'Records_Affected': int(invalid.sum()),
            'Severity': 'Warning'
        })

    return pd.DataFrame(validations)


if __name__ == "__main__":
    print(f"RRA {FORM_CODE} - {FORM_NAME}")
    print("=" * 60)
    print(f"Version: {FORM_VERSION}")
