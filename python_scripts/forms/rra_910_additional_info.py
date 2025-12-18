"""
RRA 910 Additional Information - Power BI Python Script
=======================================================

V2.0: Stub processor for form implementation
Form 910 captures additional information and notes for the RRA submission.

This script processes and validates RRA 910 Additional Information for Power BI reporting.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional

# Form metadata
FORM_CODE = '910'
FORM_NAME = 'Additional Information'
FORM_VERSION = '2.0'


def process_rra_910(data_source: str = '../../synthetic_data/rra_910_additional_info.csv') -> pd.DataFrame:
    """
    Process RRA 910 Additional Information data for Power BI

    Form 910 Fields (expected):
    ---------------------------
    - Syndicate_Number: Lloyd's syndicate number
    - Year_of_Account: YoA
    - Section: Section reference (e.g., Section A, Section B)
    - Question_Number: Question reference number
    - Question_Text: The question or topic
    - Response: Free text response
    - Supporting_Reference: Document/table references
    - Response_Date: Date of response
    """

    df = pd.read_csv(data_source)

    # Add calculated fields
    df['Response_Length'] = df['Response'].str.len()
    df['Has_Reference'] = df['Supporting_Reference'].notna()
    df['Response_Date'] = pd.to_datetime(df['Response_Date'])

    return df


def get_additional_info_summary(data_source: str = '../../synthetic_data/rra_910_additional_info.csv') -> pd.DataFrame:
    """Generate summary by section"""
    df = process_rra_910(data_source)

    summary = df.groupby('Section').agg({
        'Question_Number': 'count',
        'Response_Length': 'mean',
        'Has_Reference': 'sum'
    }).reset_index()

    summary.columns = ['Section', 'Question_Count', 'Avg_Response_Length', 'With_References']
    return summary


def validate_rra_910(data_source: str = '../../synthetic_data/rra_910_additional_info.csv') -> pd.DataFrame:
    """Validate RRA 910 Additional Information data"""
    df = pd.read_csv(data_source)

    validations = []

    # Check for empty responses
    empty_responses = df['Response'].isnull() | (df['Response'].str.strip() == '')
    validations.append({
        'Rule': 'Response Required',
        'Status': 'FAIL' if empty_responses.any() else 'PASS',
        'Records_Affected': int(empty_responses.sum()),
        'Severity': 'Warning'
    })

    # Check syndicate number present
    if df['Syndicate_Number'].isnull().any():
        validations.append({
            'Rule': 'Syndicate Number Required',
            'Status': 'FAIL',
            'Records_Affected': int(df['Syndicate_Number'].isnull().sum()),
            'Severity': 'Critical'
        })
    else:
        validations.append({
            'Rule': 'Syndicate Number Required',
            'Status': 'PASS',
            'Records_Affected': 0,
            'Severity': 'Critical'
        })

    return pd.DataFrame(validations)


if __name__ == "__main__":
    print(f"RRA {FORM_CODE} - {FORM_NAME}")
    print("=" * 60)
    print(f"Version: {FORM_VERSION}")
