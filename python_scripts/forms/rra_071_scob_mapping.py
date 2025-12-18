"""
RRA 071 SCOB Mapping - Power BI Python Script
=============================================

V2.0: Stub processor for form implementation
Form 071 maps Syndicate Classes of Business (SCOB) to Solvency II lines of business.

This script processes and validates RRA 071 SCOB Mapping data for Power BI reporting.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional

# Form metadata
FORM_CODE = '071'
FORM_NAME = 'SCOB Mapping'
FORM_VERSION = '2.0'


def process_rra_071(data_source: str = '../../synthetic_data/rra_071_scob_mapping.csv') -> pd.DataFrame:
    """
    Process RRA 071 SCOB Mapping data for Power BI

    Form 071 Fields (expected):
    ---------------------------
    - Syndicate_Number: Lloyd's syndicate number
    - SCOB_Code: Lloyd's SCOB code (e.g., A1, M1, P1)
    - SCOB_Description: SCOB description
    - SII_LOB_Code: Solvency II line of business code
    - SII_LOB_Description: Solvency II LOB description
    - Allocation_Percentage: Percentage allocation to SII LOB
    - Year_of_Account: Applicable YoA
    """

    df = pd.read_csv(data_source)

    # Add calculated fields
    df['Is_Full_Allocation'] = df['Allocation_Percentage'] == 100
    df['Allocation_Decimal'] = df['Allocation_Percentage'] / 100

    return df


def get_scob_summary(data_source: str = '../../synthetic_data/rra_071_scob_mapping.csv') -> pd.DataFrame:
    """Generate SCOB mapping summary"""
    df = process_rra_071(data_source)

    summary = df.groupby(['SCOB_Code', 'SCOB_Description']).agg({
        'SII_LOB_Code': 'nunique',
        'Syndicate_Number': 'nunique',
        'Allocation_Percentage': 'mean'
    }).reset_index()

    summary.columns = ['SCOB_Code', 'Description', 'SII_LOB_Count', 'Syndicate_Count', 'Avg_Allocation']
    return summary


def validate_rra_071(data_source: str = '../../synthetic_data/rra_071_scob_mapping.csv') -> pd.DataFrame:
    """Validate RRA 071 SCOB Mapping data"""
    df = pd.read_csv(data_source)

    validations = []

    # Check allocation percentages sum to 100 per SCOB/Syndicate
    grouped = df.groupby(['Syndicate_Number', 'SCOB_Code'])['Allocation_Percentage'].sum()
    invalid_allocations = abs(grouped - 100) > 0.01
    validations.append({
        'Rule': 'Allocations Sum to 100%',
        'Status': 'FAIL' if invalid_allocations.any() else 'PASS',
        'Records_Affected': int(invalid_allocations.sum()),
        'Severity': 'Critical'
    })

    return pd.DataFrame(validations)


if __name__ == "__main__":
    print(f"RRA {FORM_CODE} - {FORM_NAME}")
    print("=" * 60)
    print(f"Version: {FORM_VERSION}")
