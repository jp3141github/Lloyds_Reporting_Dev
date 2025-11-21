"""
RRA 010 Control Form - Power BI Python Script
This script processes and validates RRA 010 Control data for Power BI reporting
"""

import pandas as pd
import numpy as np
from datetime import datetime

def process_rra_010(data_source='../../synthetic_data/rra_010_control.csv'):
    """
    Process RRA 010 Control data for Power BI

    Parameters:
    -----------
    data_source : str
        Path to the control data CSV file

    Returns:
    --------
    pandas.DataFrame
        Processed control data ready for Power BI visualization
    """

    # Load data
    df = pd.read_csv(data_source)

    # Add calculated fields
    df['Capacity_Millions'] = df['Capacity_GBP'] / 1000000
    df['YoA_Range'] = df['Final_Pure_YoA'] - df['First_Pure_YoA'] + 1
    df['Is_Active'] = df['Status'].isin(['Submitted', 'Approved'])

    # Add submission year
    df['Submission_Year'] = pd.to_datetime(df['Submission_Date']).dt.year

    # Calculate days since submission
    df['Days_Since_Submission'] = (
        datetime.now() - pd.to_datetime(df['Submission_Date'])
    ).dt.days

    # Add status priority for sorting
    status_priority = {'Draft': 1, 'Submitted': 2, 'Approved': 3}
    df['Status_Priority'] = df['Status'].map(status_priority)

    return df


def get_control_summary(data_source='../../synthetic_data/rra_010_control.csv'):
    """
    Generate summary statistics for RRA 010 Control

    Returns:
    --------
    pandas.DataFrame
        Summary statistics
    """

    df = process_rra_010(data_source)

    summary = pd.DataFrame({
        'Metric': [
            'Total Syndicates',
            'Total Capacity (GBP M)',
            'Average Capacity (GBP M)',
            'Syndicates Submitted',
            'Syndicates Approved',
            'Average YoA Range'
        ],
        'Value': [
            len(df),
            df['Capacity_GBP'].sum() / 1000000,
            df['Capacity_GBP'].mean() / 1000000,
            (df['Status'] == 'Submitted').sum(),
            (df['Status'] == 'Approved').sum(),
            df['YoA_Range'].mean()
        ]
    })

    summary['Value'] = summary['Value'].round(2)

    return summary


def validate_rra_010(data_source='../../synthetic_data/rra_010_control.csv'):
    """
    Validate RRA 010 Control data

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
            'Records_Affected': df['Syndicate_Number'].isnull().sum()
        })
    else:
        validations.append({
            'Rule': 'Syndicate Number Required',
            'Status': 'PASS',
            'Records_Affected': 0
        })

    # Check for valid email addresses
    invalid_emails = ~df['Contact_Email'].str.contains('@', na=False)
    validations.append({
        'Rule': 'Valid Email Address',
        'Status': 'FAIL' if invalid_emails.any() else 'PASS',
        'Records_Affected': invalid_emails.sum()
    })

    # Check that First YoA <= Final YoA
    invalid_yoa = df['First_Pure_YoA'] > df['Final_Pure_YoA']
    validations.append({
        'Rule': 'First YoA <= Final YoA',
        'Status': 'FAIL' if invalid_yoa.any() else 'PASS',
        'Records_Affected': invalid_yoa.sum()
    })

    # Check capacity is positive
    invalid_capacity = df['Capacity_GBP'] <= 0
    validations.append({
        'Rule': 'Capacity > 0',
        'Status': 'FAIL' if invalid_capacity.any() else 'PASS',
        'Records_Affected': invalid_capacity.sum()
    })

    return pd.DataFrame(validations)


# For use in Power BI - the 'dataset' variable will be provided by Power BI
# Uncomment the following lines when using in Power BI:
# df = process_rra_010()
# The processed dataframe 'df' will be available for visualization in Power BI


if __name__ == "__main__":
    # Test the functions
    print("Processing RRA 010 Control Data...")
    df = process_rra_010()
    print(f"\nProcessed {len(df)} records")
    print("\nSample data:")
    print(df.head())

    print("\n" + "="*60)
    print("Control Summary:")
    print("="*60)
    print(get_control_summary())

    print("\n" + "="*60)
    print("Validation Results:")
    print("="*60)
    print(validate_rra_010())
