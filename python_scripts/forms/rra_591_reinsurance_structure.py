"""
RRA 591 Syndicate Reinsurance Structure - Power BI Python Script
================================================================

V2.0: New form processor added based on Lloyd's RRA V1.6 (March 2025)
Form 591 captures syndicate reinsurance program structure and arrangements.

This script processes and validates RRA 591 Reinsurance Structure data for Power BI reporting.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional

# Form metadata
FORM_CODE = '591'
FORM_NAME = 'Syndicate Reinsurance Structure'
FORM_VERSION = '2.0'


def process_rra_591(data_source: str = '../../synthetic_data/rra_591_reinsurance_structure.csv') -> pd.DataFrame:
    """
    Process RRA 591 Syndicate Reinsurance Structure data for Power BI

    Parameters:
    -----------
    data_source : str
        Path to the reinsurance structure data CSV file

    Returns:
    --------
    pandas.DataFrame
        Processed reinsurance structure data ready for Power BI visualization

    Form 591 Fields (expected):
    ---------------------------
    - Syndicate_Number: Lloyd's syndicate number
    - Year_of_Account: YoA for reinsurance program
    - Program_Type: Type of reinsurance (QS, XOL, Stop Loss, etc.)
    - Reinsurer_Name: Name of reinsurer
    - Reinsurer_Rating: Credit rating of reinsurer
    - Coverage_Layer: Layer description
    - Attachment_Point_GBP: Attachment point in GBP
    - Limit_GBP: Coverage limit in GBP
    - Premium_GBP: Reinsurance premium paid
    - Cession_Rate: Percentage ceded (for proportional)
    - Effective_Date: Coverage start date
    - Expiry_Date: Coverage end date
    - Treaty_Reference: Unique treaty reference
    """

    # Load data
    df = pd.read_csv(data_source)

    # Add calculated fields
    df['Premium_Millions'] = df['Premium_GBP'] / 1_000_000
    df['Limit_Millions'] = df['Limit_GBP'] / 1_000_000
    df['Attachment_Millions'] = df['Attachment_Point_GBP'] / 1_000_000

    # Calculate exhaustion point
    df['Exhaustion_Point_GBP'] = df['Attachment_Point_GBP'] + df['Limit_GBP']
    df['Exhaustion_Millions'] = df['Exhaustion_Point_GBP'] / 1_000_000

    # Rate on line calculation (for XOL)
    df['Rate_On_Line'] = np.where(
        df['Limit_GBP'] > 0,
        df['Premium_GBP'] / df['Limit_GBP'],
        0
    )
    df['Rate_On_Line_Pct'] = df['Rate_On_Line'] * 100

    # Add date calculations
    df['Effective_Date'] = pd.to_datetime(df['Effective_Date'])
    df['Expiry_Date'] = pd.to_datetime(df['Expiry_Date'])
    df['Coverage_Days'] = (df['Expiry_Date'] - df['Effective_Date']).dt.days

    # Add reinsurer quality tier
    rating_tiers = {
        'AAA': 'Tier 1',
        'AA+': 'Tier 1',
        'AA': 'Tier 1',
        'AA-': 'Tier 1',
        'A+': 'Tier 2',
        'A': 'Tier 2',
        'A-': 'Tier 2',
        'BBB+': 'Tier 3',
        'BBB': 'Tier 3',
        'BBB-': 'Tier 3',
    }
    df['Reinsurer_Tier'] = df['Reinsurer_Rating'].map(rating_tiers).fillna('Tier 4')

    # Categorize program type
    proportional_types = ['Quota Share', 'QS', 'Surplus', 'Proportional']
    df['Is_Proportional'] = df['Program_Type'].isin(proportional_types)

    return df


def get_reinsurance_summary(data_source: str = '../../synthetic_data/rra_591_reinsurance_structure.csv') -> pd.DataFrame:
    """
    Generate summary statistics for RRA 591 Reinsurance Structure

    Returns:
    --------
    pandas.DataFrame
        Summary statistics by syndicate and program type
    """

    df = process_rra_591(data_source)

    summary = df.groupby(['Syndicate_Number', 'Program_Type']).agg({
        'Premium_GBP': 'sum',
        'Limit_GBP': 'sum',
        'Treaty_Reference': 'count',
        'Cession_Rate': 'mean'
    }).reset_index()

    summary.columns = ['Syndicate', 'Program_Type', 'Total_Premium', 'Total_Limit', 'Treaty_Count', 'Avg_Cession']
    summary['Total_Premium_M'] = summary['Total_Premium'] / 1_000_000
    summary['Total_Limit_M'] = summary['Total_Limit'] / 1_000_000

    return summary


def get_reinsurer_exposure(data_source: str = '../../synthetic_data/rra_591_reinsurance_structure.csv') -> pd.DataFrame:
    """
    Analyze reinsurer concentration and exposure

    Returns:
    --------
    pandas.DataFrame
        Reinsurer exposure analysis
    """

    df = process_rra_591(data_source)

    exposure = df.groupby(['Reinsurer_Name', 'Reinsurer_Rating', 'Reinsurer_Tier']).agg({
        'Limit_GBP': 'sum',
        'Premium_GBP': 'sum',
        'Syndicate_Number': 'nunique',
        'Treaty_Reference': 'count'
    }).reset_index()

    exposure.columns = ['Reinsurer', 'Rating', 'Tier', 'Total_Limit', 'Total_Premium', 'Syndicates', 'Treaties']
    exposure['Limit_Millions'] = exposure['Total_Limit'] / 1_000_000

    # Calculate concentration percentages
    total_limit = exposure['Total_Limit'].sum()
    exposure['Concentration_Pct'] = (exposure['Total_Limit'] / total_limit * 100).round(2)

    return exposure.sort_values('Total_Limit', ascending=False)


def validate_rra_591(data_source: str = '../../synthetic_data/rra_591_reinsurance_structure.csv') -> pd.DataFrame:
    """
    Validate RRA 591 Reinsurance Structure data

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

    # Check for valid reinsurer ratings
    valid_ratings = ['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-', 'BB+', 'BB', 'NR']
    invalid_ratings = ~df['Reinsurer_Rating'].isin(valid_ratings)
    validations.append({
        'Rule': 'Valid Reinsurer Rating',
        'Status': 'FAIL' if invalid_ratings.any() else 'PASS',
        'Records_Affected': int(invalid_ratings.sum()),
        'Severity': 'Warning'
    })

    # Check attachment < exhaustion
    if 'Attachment_Point_GBP' in df.columns and 'Limit_GBP' in df.columns:
        invalid_layers = df['Limit_GBP'] <= 0
        validations.append({
            'Rule': 'Positive Limit Required',
            'Status': 'FAIL' if invalid_layers.any() else 'PASS',
            'Records_Affected': int(invalid_layers.sum()),
            'Severity': 'Critical'
        })

    # Check dates are valid
    df['Effective_Date'] = pd.to_datetime(df['Effective_Date'], errors='coerce')
    df['Expiry_Date'] = pd.to_datetime(df['Expiry_Date'], errors='coerce')
    invalid_dates = df['Effective_Date'] >= df['Expiry_Date']
    validations.append({
        'Rule': 'Effective Date < Expiry Date',
        'Status': 'FAIL' if invalid_dates.any() else 'PASS',
        'Records_Affected': int(invalid_dates.sum()),
        'Severity': 'Critical'
    })

    # Check cession rate for proportional treaties
    if 'Cession_Rate' in df.columns:
        invalid_cession = (df['Cession_Rate'] < 0) | (df['Cession_Rate'] > 1)
        validations.append({
            'Rule': 'Cession Rate 0-100%',
            'Status': 'FAIL' if invalid_cession.any() else 'PASS',
            'Records_Affected': int(invalid_cession.sum()),
            'Severity': 'Warning'
        })

    return pd.DataFrame(validations)


# For use in Power BI - the 'dataset' variable will be provided by Power BI
# Uncomment the following lines when using in Power BI:
# df = process_rra_591()
# The processed dataframe 'df' will be available for visualization in Power BI


if __name__ == "__main__":
    # Test the functions
    print(f"RRA {FORM_CODE} - {FORM_NAME}")
    print("=" * 60)
    print(f"Version: {FORM_VERSION}")
    print("\nNote: This processor requires synthetic data file:")
    print("  synthetic_data/rra_591_reinsurance_structure.csv")
    print("\nTo generate test data, run:")
    print("  python -m python_scripts.data_generation.generate_unified_lloyds_data --type RRA")
