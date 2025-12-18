"""
RRA 020 Exchange Rates - Power BI Python Script
===============================================

V2.0: Stub processor for form implementation
Form 020 contains exchange rates used for currency conversion in Lloyd's reporting.

This script processes and validates RRA 020 Exchange Rates data for Power BI reporting.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional

# Form metadata
FORM_CODE = '020'
FORM_NAME = 'Exchange Rates'
FORM_VERSION = '2.0'


def process_rra_020(data_source: str = '../../synthetic_data/rra_020_exchange_rates.csv') -> pd.DataFrame:
    """
    Process RRA 020 Exchange Rates data for Power BI

    Parameters:
    -----------
    data_source : str
        Path to the exchange rates data CSV file

    Returns:
    --------
    pandas.DataFrame
        Processed exchange rates data ready for Power BI visualization

    Form 020 Fields (expected):
    ---------------------------
    - Currency_Code: ISO currency code
    - Currency_Name: Full currency name
    - Rate_Type: Type of rate (Spot, Average, Closing)
    - Exchange_Rate: Rate against GBP
    - Effective_Date: Date rate is effective
    - Source: Rate source (Lloyd's, BoE, etc.)
    """

    df = pd.read_csv(data_source)

    # Add calculated fields
    df['Inverse_Rate'] = 1 / df['Exchange_Rate']
    df['Effective_Date'] = pd.to_datetime(df['Effective_Date'])
    df['Rate_Month'] = df['Effective_Date'].dt.to_period('M').astype(str)

    return df


def get_exchange_rate_summary(data_source: str = '../../synthetic_data/rra_020_exchange_rates.csv') -> pd.DataFrame:
    """Generate summary of exchange rates by currency"""
    df = process_rra_020(data_source)

    summary = df.groupby('Currency_Code').agg({
        'Exchange_Rate': ['mean', 'min', 'max', 'std'],
        'Effective_Date': ['min', 'max']
    }).reset_index()

    summary.columns = ['Currency', 'Avg_Rate', 'Min_Rate', 'Max_Rate', 'Std_Dev', 'First_Date', 'Last_Date']
    return summary


def validate_rra_020(data_source: str = '../../synthetic_data/rra_020_exchange_rates.csv') -> pd.DataFrame:
    """Validate RRA 020 Exchange Rates data"""
    df = pd.read_csv(data_source)

    validations = []

    # Check for missing currency codes
    validations.append({
        'Rule': 'Currency Code Required',
        'Status': 'FAIL' if df['Currency_Code'].isnull().any() else 'PASS',
        'Records_Affected': int(df['Currency_Code'].isnull().sum()),
        'Severity': 'Critical'
    })

    # Check rates are positive
    if 'Exchange_Rate' in df.columns:
        invalid_rates = df['Exchange_Rate'] <= 0
        validations.append({
            'Rule': 'Exchange Rate > 0',
            'Status': 'FAIL' if invalid_rates.any() else 'PASS',
            'Records_Affected': int(invalid_rates.sum()),
            'Severity': 'Critical'
        })

    return pd.DataFrame(validations)


if __name__ == "__main__":
    print(f"RRA {FORM_CODE} - {FORM_NAME}")
    print("=" * 60)
    print(f"Version: {FORM_VERSION}")
    print("\nNote: This processor requires synthetic data file:")
    print(f"  synthetic_data/rra_{FORM_CODE}_exchange_rates.csv")
