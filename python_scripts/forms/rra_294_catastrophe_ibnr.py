"""
RRA 294 Catastrophe IBNR - Power BI Python Script
=================================================

V2.0: Stub processor for form implementation
Form 294 captures IBNR specifically related to catastrophe events.

This script processes and validates RRA 294 Catastrophe IBNR data for Power BI reporting.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional

# Form metadata
FORM_CODE = '294'
FORM_NAME = 'Catastrophe IBNR'
FORM_VERSION = '2.0'


def process_rra_294(data_source: str = '../../synthetic_data/rra_294_catastrophe_ibnr.csv') -> pd.DataFrame:
    """
    Process RRA 294 Catastrophe IBNR data for Power BI

    Form 294 Fields (expected):
    ---------------------------
    - Syndicate_Number: Lloyd's syndicate number
    - Year_of_Account: YoA of exposure
    - Event_Code: Lloyd's event code
    - Event_Name: Catastrophe event name
    - Event_Date: Date of catastrophe
    - Gross_IBNR_GBP: Gross catastrophe IBNR
    - Net_IBNR_GBP: Net catastrophe IBNR
    - Expected_Recovery_GBP: Expected RI recovery
    - Confidence_Level: Confidence in estimate (High/Medium/Low)
    """

    df = pd.read_csv(data_source)

    # Add calculated fields
    df['Gross_IBNR_Millions'] = df['Gross_IBNR_GBP'] / 1_000_000
    df['Net_IBNR_Millions'] = df['Net_IBNR_GBP'] / 1_000_000
    df['RI_IBNR'] = df['Gross_IBNR_GBP'] - df['Net_IBNR_GBP']
    df['RI_Recovery_Pct'] = np.where(
        df['Gross_IBNR_GBP'] > 0,
        df['RI_IBNR'] / df['Gross_IBNR_GBP'] * 100,
        0
    )

    df['Event_Date'] = pd.to_datetime(df['Event_Date'])
    df['Event_Year'] = df['Event_Date'].dt.year

    return df


def get_catastrophe_summary(data_source: str = '../../synthetic_data/rra_294_catastrophe_ibnr.csv') -> pd.DataFrame:
    """Generate catastrophe IBNR summary by event"""
    df = process_rra_294(data_source)

    summary = df.groupby(['Event_Code', 'Event_Name']).agg({
        'Gross_IBNR_GBP': 'sum',
        'Net_IBNR_GBP': 'sum',
        'Syndicate_Number': 'nunique'
    }).reset_index()

    summary.columns = ['Event_Code', 'Event_Name', 'Gross_IBNR', 'Net_IBNR', 'Syndicate_Count']
    summary['Gross_Millions'] = summary['Gross_IBNR'] / 1_000_000
    return summary.sort_values('Gross_IBNR', ascending=False)


def validate_rra_294(data_source: str = '../../synthetic_data/rra_294_catastrophe_ibnr.csv') -> pd.DataFrame:
    """Validate RRA 294 Catastrophe IBNR data"""
    df = pd.read_csv(data_source)

    validations = []

    # Check Net <= Gross
    invalid = df['Net_IBNR_GBP'] > df['Gross_IBNR_GBP']
    validations.append({
        'Rule': 'Net IBNR <= Gross IBNR',
        'Status': 'FAIL' if invalid.any() else 'PASS',
        'Records_Affected': int(invalid.sum()),
        'Severity': 'Warning'
    })

    # Check confidence levels
    valid_levels = ['High', 'Medium', 'Low']
    if 'Confidence_Level' in df.columns:
        invalid_conf = ~df['Confidence_Level'].isin(valid_levels)
        validations.append({
            'Rule': 'Valid Confidence Level',
            'Status': 'FAIL' if invalid_conf.any() else 'PASS',
            'Records_Affected': int(invalid_conf.sum()),
            'Severity': 'Warning'
        })

    return pd.DataFrame(validations)


if __name__ == "__main__":
    print(f"RRA {FORM_CODE} - {FORM_NAME}")
    print("=" * 60)
    print(f"Version: {FORM_VERSION}")
