"""
RRA 091 LPT Data - Power BI Python Script
=========================================

V2.0: Stub processor for form implementation
Form 091 captures Loss Portfolio Transfer (LPT) and Adverse Development Cover (ADC) data.

This script processes and validates RRA 091 LPT Data for Power BI reporting.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional

# Form metadata
FORM_CODE = '091'
FORM_NAME = 'LPT Data'
FORM_VERSION = '2.0'


def process_rra_091(data_source: str = '../../synthetic_data/rra_091_lpt_data.csv') -> pd.DataFrame:
    """
    Process RRA 091 LPT Data for Power BI

    Form 091 Fields (expected):
    ---------------------------
    - Syndicate_Number: Lloyd's syndicate number
    - Transaction_Type: LPT, ADC, or similar
    - Counterparty: Name of reinsurer/cedant
    - Effective_Date: Transaction effective date
    - Years_of_Account: YoAs covered (comma separated)
    - Gross_Reserves_Transferred_GBP: Gross reserves amount
    - Net_Premium_GBP: Premium paid/received
    - Cover_Limit_GBP: Maximum cover limit
    - Retention_GBP: Retention amount
    """

    df = pd.read_csv(data_source)

    # Add calculated fields
    df['Reserves_Millions'] = df['Gross_Reserves_Transferred_GBP'] / 1_000_000
    df['Premium_Millions'] = df['Net_Premium_GBP'] / 1_000_000
    df['Premium_to_Reserves_Ratio'] = np.where(
        df['Gross_Reserves_Transferred_GBP'] > 0,
        df['Net_Premium_GBP'] / df['Gross_Reserves_Transferred_GBP'],
        0
    )

    df['Effective_Date'] = pd.to_datetime(df['Effective_Date'])
    df['YoA_Count'] = df['Years_of_Account'].str.split(',').str.len()

    return df


def get_lpt_summary(data_source: str = '../../synthetic_data/rra_091_lpt_data.csv') -> pd.DataFrame:
    """Generate LPT summary by transaction type"""
    df = process_rra_091(data_source)

    summary = df.groupby('Transaction_Type').agg({
        'Gross_Reserves_Transferred_GBP': 'sum',
        'Net_Premium_GBP': 'sum',
        'Syndicate_Number': 'nunique'
    }).reset_index()

    summary.columns = ['Type', 'Total_Reserves', 'Total_Premium', 'Syndicate_Count']
    summary['Reserves_M'] = summary['Total_Reserves'] / 1_000_000
    return summary


def validate_rra_091(data_source: str = '../../synthetic_data/rra_091_lpt_data.csv') -> pd.DataFrame:
    """Validate RRA 091 LPT Data"""
    df = pd.read_csv(data_source)

    validations = []

    # Check transaction types
    valid_types = ['LPT', 'ADC', 'RITC', 'Other']
    if 'Transaction_Type' in df.columns:
        invalid = ~df['Transaction_Type'].isin(valid_types)
        validations.append({
            'Rule': 'Valid Transaction Type',
            'Status': 'FAIL' if invalid.any() else 'PASS',
            'Records_Affected': int(invalid.sum()),
            'Severity': 'Warning'
        })

    return pd.DataFrame(validations)


if __name__ == "__main__":
    print(f"RRA {FORM_CODE} - {FORM_NAME}")
    print("=" * 60)
    print(f"Version: {FORM_VERSION}")
