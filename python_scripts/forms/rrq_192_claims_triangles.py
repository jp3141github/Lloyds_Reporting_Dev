"""
RRQ 192 Claims Triangles Summary - Power BI Python Script
=========================================================

V2.0: New form processor added based on Lloyd's RRQ Instructions V1.6 (March 2025)
Form 192 provides summary claims triangle data for quarterly monitoring.

This script processes and validates RRQ 192 Claims Triangles Summary data for Power BI reporting.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Form metadata
FORM_CODE = '192'
FORM_NAME = 'Claims Triangles Summary'
FORM_VERSION = '2.0'


def process_rrq_192(data_source: str = '../../synthetic_data/rrq_192_claims_triangles.csv') -> pd.DataFrame:
    """
    Process RRQ 192 Claims Triangles Summary data for Power BI

    Parameters:
    -----------
    data_source : str
        Path to the claims triangles summary data CSV file

    Returns:
    --------
    pandas.DataFrame
        Processed claims triangles summary data ready for Power BI visualization

    Form 192 Fields (expected):
    ---------------------------
    - Syndicate_Number: Lloyd's syndicate number
    - Year_of_Account: Year of account
    - Triangle_Type: Type (Paid, Incurred, Case)
    - Basis: Gross/Net
    - Class_of_Business: Lloyd's SCOB code
    - Currency: Reporting currency
    - Dev_Year_0 to Dev_Year_10: Development year columns
    - Ultimate_Estimate: Current ultimate estimate
    - Selected_IBNR: Selected IBNR amount
    - Method: Actuarial method used
    - Reporting_Period: Quarter end date
    """

    # Load data
    df = pd.read_csv(data_source)

    # Identify development year columns
    dev_cols = [col for col in df.columns if col.startswith('Dev_Year_')]

    # Calculate latest diagonal value
    def get_latest_diagonal(row):
        for col in reversed(dev_cols):
            if pd.notna(row[col]) and row[col] != 0:
                return row[col]
        return 0

    df['Latest_Diagonal'] = df.apply(get_latest_diagonal, axis=1)
    df['Latest_Diagonal_M'] = df['Latest_Diagonal'] / 1_000_000

    # Add calculated fields
    df['Ultimate_Millions'] = df['Ultimate_Estimate'] / 1_000_000
    df['IBNR_Millions'] = df['Selected_IBNR'] / 1_000_000

    # Calculate IBNR as percentage of ultimate
    df['IBNR_Pct_Ultimate'] = np.where(
        df['Ultimate_Estimate'] > 0,
        df['Selected_IBNR'] / df['Ultimate_Estimate'] * 100,
        0
    )

    # Calculate development to ultimate
    df['Dev_to_Ultimate'] = np.where(
        df['Latest_Diagonal'] > 0,
        df['Ultimate_Estimate'] / df['Latest_Diagonal'],
        1
    )

    # Parse reporting period
    df['Reporting_Period'] = pd.to_datetime(df['Reporting_Period'])
    df['Report_Quarter'] = df['Reporting_Period'].dt.quarter
    df['Report_Year'] = df['Reporting_Period'].dt.year

    # Add maturity classification
    def classify_maturity(row):
        # Count non-null development years
        dev_count = sum(1 for col in dev_cols if pd.notna(row[col]) and row[col] != 0)
        if dev_count <= 2:
            return 'Immature'
        elif dev_count <= 5:
            return 'Developing'
        else:
            return 'Mature'

    df['Maturity'] = df.apply(classify_maturity, axis=1)

    return df


def get_triangle_summary_by_method(data_source: str = '../../synthetic_data/rrq_192_claims_triangles.csv') -> pd.DataFrame:
    """
    Summarize triangles by actuarial method

    Returns:
    --------
    pandas.DataFrame
        Summary statistics by method
    """

    df = process_rrq_192(data_source)

    summary = df.groupby(['Method', 'Basis']).agg({
        'Ultimate_Estimate': 'sum',
        'Selected_IBNR': 'sum',
        'Syndicate_Number': 'nunique',
        'Year_of_Account': 'nunique'
    }).reset_index()

    summary.columns = ['Method', 'Basis', 'Total_Ultimate', 'Total_IBNR', 'Syndicates', 'YoA_Count']
    summary['Ultimate_Millions'] = summary['Total_Ultimate'] / 1_000_000
    summary['IBNR_Millions'] = summary['Total_IBNR'] / 1_000_000

    return summary


def get_development_pattern_analysis(
    data_source: str = '../../synthetic_data/rrq_192_claims_triangles.csv',
    triangle_type: str = 'Paid',
    basis: str = 'Gross'
) -> pd.DataFrame:
    """
    Analyze development patterns from triangle data

    Parameters:
    -----------
    data_source : str
        Path to data file
    triangle_type : str
        Filter by triangle type (Paid, Incurred, Case)
    basis : str
        Filter by basis (Gross, Net)

    Returns:
    --------
    pandas.DataFrame
        Development pattern analysis
    """

    df = process_rrq_192(data_source)

    # Filter
    mask = (df['Triangle_Type'] == triangle_type) & (df['Basis'] == basis)
    filtered = df[mask].copy()

    # Identify development columns
    dev_cols = [col for col in df.columns if col.startswith('Dev_Year_')]

    # Calculate average development pattern
    pattern = []
    for i, col in enumerate(dev_cols):
        if col in filtered.columns:
            values = filtered[col].dropna()
            if len(values) > 0:
                pattern.append({
                    'Development_Year': i,
                    'Column': col,
                    'Average_Value': values.mean(),
                    'Count': len(values),
                    'Std_Dev': values.std()
                })

    return pd.DataFrame(pattern)


def compare_gross_net_triangles(data_source: str = '../../synthetic_data/rrq_192_claims_triangles.csv') -> pd.DataFrame:
    """
    Compare gross vs net triangle results

    Returns:
    --------
    pandas.DataFrame
        Comparison of gross and net ultimates
    """

    df = process_rrq_192(data_source)

    # Get gross and net summaries
    gross = df[df['Basis'] == 'Gross'].groupby(['Syndicate_Number', 'Year_of_Account', 'Triangle_Type']).agg({
        'Ultimate_Estimate': 'sum',
        'Selected_IBNR': 'sum'
    }).reset_index()
    gross.columns = ['Syndicate', 'YoA', 'Type', 'Gross_Ultimate', 'Gross_IBNR']

    net = df[df['Basis'] == 'Net'].groupby(['Syndicate_Number', 'Year_of_Account', 'Triangle_Type']).agg({
        'Ultimate_Estimate': 'sum',
        'Selected_IBNR': 'sum'
    }).reset_index()
    net.columns = ['Syndicate', 'YoA', 'Type', 'Net_Ultimate', 'Net_IBNR']

    # Merge
    comparison = gross.merge(net, on=['Syndicate', 'YoA', 'Type'], how='outer')

    # Calculate RI recovery
    comparison['RI_Ultimate'] = comparison['Gross_Ultimate'] - comparison['Net_Ultimate']
    comparison['RI_IBNR'] = comparison['Gross_IBNR'] - comparison['Net_IBNR']
    comparison['RI_Recovery_Pct'] = np.where(
        comparison['Gross_Ultimate'] > 0,
        comparison['RI_Ultimate'] / comparison['Gross_Ultimate'] * 100,
        0
    )

    return comparison


def validate_rrq_192(data_source: str = '../../synthetic_data/rrq_192_claims_triangles.csv') -> pd.DataFrame:
    """
    Validate RRQ 192 Claims Triangles Summary data

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

    # Check valid triangle types
    valid_types = ['Paid', 'Incurred', 'Case']
    if 'Triangle_Type' in df.columns:
        invalid_types = ~df['Triangle_Type'].isin(valid_types)
        validations.append({
            'Rule': 'Valid Triangle Type',
            'Status': 'FAIL' if invalid_types.any() else 'PASS',
            'Records_Affected': int(invalid_types.sum()),
            'Severity': 'Warning'
        })

    # Check valid basis
    valid_basis = ['Gross', 'Net']
    if 'Basis' in df.columns:
        invalid_basis = ~df['Basis'].isin(valid_basis)
        validations.append({
            'Rule': 'Valid Basis (Gross/Net)',
            'Status': 'FAIL' if invalid_basis.any() else 'PASS',
            'Records_Affected': int(invalid_basis.sum()),
            'Severity': 'Warning'
        })

    # Check ultimate >= latest diagonal
    dev_cols = [col for col in df.columns if col.startswith('Dev_Year_')]
    if dev_cols and 'Ultimate_Estimate' in df.columns:
        def get_latest(row):
            for col in reversed(dev_cols):
                if pd.notna(row[col]) and row[col] != 0:
                    return row[col]
            return 0

        df['_latest'] = df.apply(get_latest, axis=1)
        ultimate_less_than_diagonal = df['Ultimate_Estimate'] < df['_latest'] * 0.99  # 1% tolerance
        validations.append({
            'Rule': 'Ultimate >= Latest Diagonal',
            'Status': 'FAIL' if ultimate_less_than_diagonal.any() else 'PASS',
            'Records_Affected': int(ultimate_less_than_diagonal.sum()),
            'Severity': 'Warning'
        })

    # Check IBNR is non-negative for most cases
    if 'Selected_IBNR' in df.columns:
        negative_ibnr = df['Selected_IBNR'] < 0
        validations.append({
            'Rule': 'IBNR Non-Negative',
            'Status': 'FAIL' if negative_ibnr.any() else 'PASS',
            'Records_Affected': int(negative_ibnr.sum()),
            'Severity': 'Warning'
        })

    return pd.DataFrame(validations)


# For use in Power BI - the 'dataset' variable will be provided by Power BI
# Uncomment the following lines when using in Power BI:
# df = process_rrq_192()
# The processed dataframe 'df' will be available for visualization in Power BI


if __name__ == "__main__":
    # Test the functions
    print(f"RRQ {FORM_CODE} - {FORM_NAME}")
    print("=" * 60)
    print(f"Version: {FORM_VERSION}")
    print("\nNote: This processor requires synthetic data file:")
    print("  synthetic_data/rrq_192_claims_triangles.csv")
    print("\nTo generate test data, run:")
    print("  python -m python_scripts.data_generation.generate_unified_lloyds_data --type RRQ")
