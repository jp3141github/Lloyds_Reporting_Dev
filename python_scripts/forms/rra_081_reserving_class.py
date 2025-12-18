"""
RRA 081 Reserving Class Information - Power BI Python Script
============================================================

V2.0: Stub processor for form implementation
Form 081 captures reserving class definitions and actuarial groupings.

This script processes and validates RRA 081 Reserving Class Information for Power BI reporting.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional

# Form metadata
FORM_CODE = '081'
FORM_NAME = 'Reserving Class Information'
FORM_VERSION = '2.0'


def process_rra_081(data_source: str = '../../synthetic_data/rra_081_reserving_class.csv') -> pd.DataFrame:
    """
    Process RRA 081 Reserving Class Information data for Power BI

    Form 081 Fields (expected):
    ---------------------------
    - Syndicate_Number: Lloyd's syndicate number
    - Reserving_Class_Code: Internal reserving class code
    - Reserving_Class_Name: Reserving class description
    - SCOB_Codes: Linked SCOB codes (comma separated)
    - Development_Pattern: Short/Medium/Long tail
    - Actuarial_Method: Primary method used
    - Year_of_Account: Applicable YoA
    """

    df = pd.read_csv(data_source)

    # Add calculated fields
    df['SCOB_Count'] = df['SCOB_Codes'].str.split(',').str.len()
    df['Is_Long_Tail'] = df['Development_Pattern'] == 'Long Tail'

    return df


def get_reserving_class_summary(data_source: str = '../../synthetic_data/rra_081_reserving_class.csv') -> pd.DataFrame:
    """Generate reserving class summary"""
    df = process_rra_081(data_source)

    summary = df.groupby(['Development_Pattern', 'Actuarial_Method']).agg({
        'Reserving_Class_Code': 'nunique',
        'Syndicate_Number': 'nunique'
    }).reset_index()

    summary.columns = ['Pattern', 'Method', 'Class_Count', 'Syndicate_Count']
    return summary


def validate_rra_081(data_source: str = '../../synthetic_data/rra_081_reserving_class.csv') -> pd.DataFrame:
    """Validate RRA 081 Reserving Class Information data"""
    df = pd.read_csv(data_source)

    validations = []

    # Check for valid development patterns
    valid_patterns = ['Short Tail', 'Medium Tail', 'Long Tail']
    if 'Development_Pattern' in df.columns:
        invalid_patterns = ~df['Development_Pattern'].isin(valid_patterns)
        validations.append({
            'Rule': 'Valid Development Pattern',
            'Status': 'FAIL' if invalid_patterns.any() else 'PASS',
            'Records_Affected': int(invalid_patterns.sum()),
            'Severity': 'Warning'
        })

    return pd.DataFrame(validations)


if __name__ == "__main__":
    print(f"RRA {FORM_CODE} - {FORM_NAME}")
    print("=" * 60)
    print(f"Version: {FORM_VERSION}")
