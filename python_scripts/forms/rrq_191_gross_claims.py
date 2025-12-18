"""
RRQ 191 Gross Claims Development - Power BI Python Script
=========================================================

V2.0: New form processor added based on Lloyd's RRQ Instructions V1.6 (March 2025)
Form 191 captures gross claims development triangles for quarterly reporting.

This script processes and validates RRQ 191 Gross Claims Development data for Power BI reporting.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Form metadata
FORM_CODE = '191'
FORM_NAME = 'Gross Claims Development'
FORM_VERSION = '2.0'


def process_rrq_191(data_source: str = '../../synthetic_data/rrq_191_gross_claims.csv') -> pd.DataFrame:
    """
    Process RRQ 191 Gross Claims Development data for Power BI

    Parameters:
    -----------
    data_source : str
        Path to the gross claims development data CSV file

    Returns:
    --------
    pandas.DataFrame
        Processed gross claims development data ready for Power BI visualization

    Form 191 Fields (expected):
    ---------------------------
    - Syndicate_Number: Lloyd's syndicate number
    - Year_of_Account: Year of account
    - Development_Year: Development year (0, 1, 2, ...)
    - Class_of_Business: Lloyd's SCOB code
    - Currency: Original currency
    - Gross_Paid_Claims: Cumulative gross paid claims
    - Gross_Case_Reserves: Gross case reserves at development point
    - Gross_IBNR: Gross IBNR at development point
    - Gross_Incurred: Total gross incurred (Paid + Case + IBNR)
    - Reporting_Period: Quarter end date
    """

    # Load data
    df = pd.read_csv(data_source)

    # Add calculated fields
    df['Gross_Paid_Millions'] = df['Gross_Paid_Claims'] / 1_000_000
    df['Gross_Incurred_Millions'] = df['Gross_Incurred'] / 1_000_000
    df['Gross_OS_Millions'] = (df['Gross_Case_Reserves'] + df['Gross_IBNR']) / 1_000_000

    # Calculate development ratios
    df['Paid_to_Incurred_Ratio'] = np.where(
        df['Gross_Incurred'] > 0,
        df['Gross_Paid_Claims'] / df['Gross_Incurred'],
        0
    )
    df['IBNR_to_Incurred_Ratio'] = np.where(
        df['Gross_Incurred'] > 0,
        df['Gross_IBNR'] / df['Gross_Incurred'],
        0
    )

    # Add calendar year
    df['Calendar_Year'] = df['Year_of_Account'] + df['Development_Year']

    # Parse reporting period
    df['Reporting_Period'] = pd.to_datetime(df['Reporting_Period'])
    df['Report_Quarter'] = df['Reporting_Period'].dt.quarter
    df['Report_Year'] = df['Reporting_Period'].dt.year

    return df


def create_gross_development_triangle(
    data_source: str = '../../synthetic_data/rrq_191_gross_claims.csv',
    syndicate: Optional[int] = None,
    class_of_business: Optional[str] = None,
    metric: str = 'Gross_Incurred'
) -> pd.DataFrame:
    """
    Create a development triangle from the gross claims data

    Parameters:
    -----------
    data_source : str
        Path to data file
    syndicate : int, optional
        Filter to specific syndicate
    class_of_business : str, optional
        Filter to specific SCOB
    metric : str
        Column to use for triangle values (default: Gross_Incurred)

    Returns:
    --------
    pandas.DataFrame
        Development triangle with YoA as rows, Dev Year as columns
    """

    df = process_rrq_191(data_source)

    # Apply filters
    if syndicate:
        df = df[df['Syndicate_Number'] == syndicate]
    if class_of_business:
        df = df[df['Class_of_Business'] == class_of_business]

    # Aggregate if needed
    agg_df = df.groupby(['Year_of_Account', 'Development_Year'])[metric].sum().reset_index()

    # Pivot to triangle format
    triangle = agg_df.pivot(
        index='Year_of_Account',
        columns='Development_Year',
        values=metric
    )

    return triangle


def calculate_gross_development_factors(
    data_source: str = '../../synthetic_data/rrq_191_gross_claims.csv',
    syndicate: Optional[int] = None
) -> pd.DataFrame:
    """
    Calculate age-to-age development factors from gross claims triangle

    Returns:
    --------
    pandas.DataFrame
        Development factors by development year
    """

    triangle = create_gross_development_triangle(data_source, syndicate)

    factors = []
    for col_idx in range(len(triangle.columns) - 1):
        col_current = triangle.columns[col_idx]
        col_next = triangle.columns[col_idx + 1]

        # Calculate weighted average factor
        mask = triangle[col_next].notna() & (triangle[col_current] > 0)
        if mask.any():
            factor = (triangle.loc[mask, col_next].sum() /
                     triangle.loc[mask, col_current].sum())
            factors.append({
                'From_Dev_Year': col_current,
                'To_Dev_Year': col_next,
                'Development_Factor': factor,
                'YoA_Count': mask.sum()
            })

    return pd.DataFrame(factors)


def get_gross_claims_summary(data_source: str = '../../synthetic_data/rrq_191_gross_claims.csv') -> pd.DataFrame:
    """
    Generate summary statistics for RRQ 191 Gross Claims Development

    Returns:
    --------
    pandas.DataFrame
        Summary by syndicate and year of account
    """

    df = process_rrq_191(data_source)

    # Get latest development year for each YoA
    latest = df.loc[df.groupby(['Syndicate_Number', 'Year_of_Account'])['Development_Year'].idxmax()]

    summary = latest.groupby('Syndicate_Number').agg({
        'Gross_Paid_Claims': 'sum',
        'Gross_Incurred': 'sum',
        'Gross_IBNR': 'sum',
        'Year_of_Account': 'nunique'
    }).reset_index()

    summary.columns = ['Syndicate', 'Total_Paid', 'Total_Incurred', 'Total_IBNR', 'YoA_Count']
    summary['Paid_Millions'] = summary['Total_Paid'] / 1_000_000
    summary['Incurred_Millions'] = summary['Total_Incurred'] / 1_000_000
    summary['IBNR_Millions'] = summary['Total_IBNR'] / 1_000_000

    return summary


def validate_rrq_191(data_source: str = '../../synthetic_data/rrq_191_gross_claims.csv') -> pd.DataFrame:
    """
    Validate RRQ 191 Gross Claims Development data

    Returns:
    --------
    pandas.DataFrame
        Validation results
    """

    df = pd.read_csv(data_source)

    validations = []

    # Check for missing syndicate numbers
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

    # Check gross incurred = paid + case + IBNR
    if all(col in df.columns for col in ['Gross_Paid_Claims', 'Gross_Case_Reserves', 'Gross_IBNR', 'Gross_Incurred']):
        calculated = df['Gross_Paid_Claims'] + df['Gross_Case_Reserves'] + df['Gross_IBNR']
        tolerance = 0.01  # 1% tolerance for rounding
        mismatch = abs(df['Gross_Incurred'] - calculated) > (df['Gross_Incurred'].abs() * tolerance)
        validations.append({
            'Rule': 'Incurred = Paid + Case + IBNR',
            'Status': 'FAIL' if mismatch.any() else 'PASS',
            'Records_Affected': int(mismatch.sum()),
            'Severity': 'Critical'
        })

    # Check for negative values
    for col in ['Gross_Paid_Claims', 'Gross_Case_Reserves', 'Gross_Incurred']:
        if col in df.columns:
            negative = df[col] < 0
            validations.append({
                'Rule': f'{col} Non-Negative',
                'Status': 'FAIL' if negative.any() else 'PASS',
                'Records_Affected': int(negative.sum()),
                'Severity': 'Warning'
            })

    # Check development year is non-negative integer
    if 'Development_Year' in df.columns:
        invalid_dev = (df['Development_Year'] < 0) | (df['Development_Year'] != df['Development_Year'].astype(int))
        validations.append({
            'Rule': 'Valid Development Year',
            'Status': 'FAIL' if invalid_dev.any() else 'PASS',
            'Records_Affected': int(invalid_dev.sum()),
            'Severity': 'Critical'
        })

    return pd.DataFrame(validations)


# For use in Power BI - the 'dataset' variable will be provided by Power BI
# Uncomment the following lines when using in Power BI:
# df = process_rrq_191()
# The processed dataframe 'df' will be available for visualization in Power BI


if __name__ == "__main__":
    # Test the functions
    print(f"RRQ {FORM_CODE} - {FORM_NAME}")
    print("=" * 60)
    print(f"Version: {FORM_VERSION}")
    print("\nNote: This processor requires synthetic data file:")
    print("  synthetic_data/rrq_191_gross_claims.csv")
    print("\nTo generate test data, run:")
    print("  python -m python_scripts.data_generation.generate_unified_lloyds_data --type RRQ")
