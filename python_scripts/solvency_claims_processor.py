"""
Solvency II Pillar 3 - Risk and Claim Reporting
Step B Claims Template Processor for Power BI

This script processes Lloyd's of London claims data and transforms it
into the format required for RRA (Reserve Return Annual) forms.

Usage in Power BI:
1. Use 'Get Data' -> 'Python script'
2. Copy this script or reference the file
3. Specify the input data source
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional


def validate_claim_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and clean the claims data.

    Args:
        df: Input claims dataframe

    Returns:
        Validated and cleaned dataframe
    """
    required_columns = [
        'Syndicate Number',
        'Claim Reference',
        'UMR',
        'Risk Code',
        'Year of Account',
        'Original Currency',
        'Claim status at beginning of period',
        'Claim status at end of period',
        'Outstanding Claims Amount as at beginning of period',
        'Paid to Date Amount',
        'Paid in Year amount',
        'Outstanding Claim amount as at end of period'
    ]

    # Check for required columns
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        print(f"Warning: Missing columns: {missing_cols}")

    # Convert numeric columns
    numeric_cols = [
        'Outstanding Claims Amount as at beginning of period',
        'Paid to Date Amount',
        'Paid in Year amount',
        'Outstanding Claim amount as at end of period'
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Convert Year of Account to integer
    if 'Year of Account' in df.columns:
        df['Year of Account'] = pd.to_numeric(df['Year of Account'], errors='coerce').fillna(0).astype(int)

    return df


def calculate_incurred_amounts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total incurred amounts for claims.

    Args:
        df: Claims dataframe

    Returns:
        Dataframe with calculated incurred amounts
    """
    df = df.copy()

    # Total Incurred = Paid to Date + Outstanding at end of period
    df['Total Incurred as at end of period'] = (
        df['Paid to Date Amount'] +
        df['Outstanding Claim amount as at end of period']
    )

    # Movement in year = Outstanding at end - Outstanding at beginning + Paid in year
    df['Movement in Year'] = (
        df['Outstanding Claim amount as at end of period'] -
        df['Outstanding Claims Amount as at beginning of period'] +
        df['Paid in Year amount']
    )

    # Reserve movement
    df['Reserve Movement'] = (
        df['Outstanding Claim amount as at end of period'] -
        df['Outstanding Claims Amount as at beginning of period']
    )

    return df


def aggregate_by_syndicate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate claims data by syndicate and year of account.

    Args:
        df: Claims dataframe with calculated amounts

    Returns:
        Aggregated dataframe by syndicate
    """
    agg_dict = {
        'Claim Reference': 'count',
        'Outstanding Claims Amount as at beginning of period': 'sum',
        'Paid to Date Amount': 'sum',
        'Paid in Year amount': 'sum',
        'Outstanding Claim amount as at end of period': 'sum',
        'Total Incurred as at end of period': 'sum',
        'Movement in Year': 'sum',
        'Reserve Movement': 'sum'
    }

    grouped = df.groupby([
        'Syndicate Number',
        'Year of Account'
    ]).agg(agg_dict).reset_index()

    # Rename count column
    grouped.rename(columns={'Claim Reference': 'Number of Claims'}, inplace=True)

    return grouped


def aggregate_by_risk_code(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate claims data by risk code and year of account.

    Args:
        df: Claims dataframe with calculated amounts

    Returns:
        Aggregated dataframe by risk code
    """
    agg_dict = {
        'Claim Reference': 'count',
        'Outstanding Claims Amount as at beginning of period': 'sum',
        'Paid to Date Amount': 'sum',
        'Paid in Year amount': 'sum',
        'Outstanding Claim amount as at end of period': 'sum',
        'Total Incurred as at end of period': 'sum',
        'Movement in Year': 'sum',
        'Reserve Movement': 'sum'
    }

    grouped = df.groupby([
        'Syndicate Number',
        'Year of Account',
        'Risk Code'
    ]).agg(agg_dict).reset_index()

    grouped.rename(columns={'Claim Reference': 'Number of Claims'}, inplace=True)

    return grouped


def aggregate_by_claim_status(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate claims data by claim status.

    Args:
        df: Claims dataframe with calculated amounts

    Returns:
        Aggregated dataframe by claim status
    """
    agg_dict = {
        'Claim Reference': 'count',
        'Outstanding Claims Amount as at beginning of period': 'sum',
        'Paid to Date Amount': 'sum',
        'Paid in Year amount': 'sum',
        'Outstanding Claim amount as at end of period': 'sum',
        'Total Incurred as at end of period': 'sum',
        'Movement in Year': 'sum',
        'Reserve Movement': 'sum'
    }

    grouped = df.groupby([
        'Syndicate Number',
        'Year of Account',
        'Claim status at end of period'
    ]).agg(agg_dict).reset_index()

    grouped.rename(columns={'Claim Reference': 'Number of Claims'}, inplace=True)

    return grouped


def create_summary_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create overall summary report for all syndicates.

    Args:
        df: Claims dataframe with calculated amounts

    Returns:
        Summary report dataframe
    """
    agg_dict = {
        'Claim Reference': 'count',
        'Syndicate Number': 'nunique',
        'Outstanding Claims Amount as at beginning of period': 'sum',
        'Paid to Date Amount': 'sum',
        'Paid in Year amount': 'sum',
        'Outstanding Claim amount as at end of period': 'sum',
        'Total Incurred as at end of period': 'sum',
        'Movement in Year': 'sum',
        'Reserve Movement': 'sum'
    }

    summary = df.agg(agg_dict).to_frame().T
    summary.rename(columns={
        'Claim Reference': 'Total Number of Claims',
        'Syndicate Number': 'Number of Syndicates'
    }, inplace=True)

    return summary


def process_claims_data(input_file: str, sheet_name: str = 'input Sheet') -> Dict[str, pd.DataFrame]:
    """
    Main processing function for claims data.

    Args:
        input_file: Path to the Excel input file
        sheet_name: Name of the sheet containing claims data

    Returns:
        Dictionary containing all output tables
    """
    # Read the data
    df = pd.read_excel(input_file, sheet_name=sheet_name)

    # Validate and clean
    df = validate_claim_data(df)

    # Calculate derived amounts
    df = calculate_incurred_amounts(df)

    # Create different aggregations
    output_tables = {
        'detailed_claims': df,
        'by_syndicate': aggregate_by_syndicate(df),
        'by_risk_code': aggregate_by_risk_code(df),
        'by_claim_status': aggregate_by_claim_status(df),
        'summary': create_summary_report(df)
    }

    return output_tables


def export_to_excel(output_tables: Dict[str, pd.DataFrame], output_file: str):
    """
    Export all output tables to a single Excel file with multiple sheets.

    Args:
        output_tables: Dictionary of dataframes to export
        output_file: Path to the output Excel file
    """
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for sheet_name, df in output_tables.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Output exported to: {output_file}")


# Power BI Integration Example
def powerbi_transform(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform function specifically designed for Power BI.
    This function expects the input dataframe to be loaded in Power BI.

    Args:
        input_df: Input claims dataframe from Power BI

    Returns:
        Transformed dataframe ready for visualization
    """
    # Validate and clean
    df = validate_claim_data(input_df)

    # Calculate derived amounts
    df = calculate_incurred_amounts(df)

    return df


# Main execution example
if __name__ == "__main__":
    # Example usage
    # Replace with your actual file path
    input_file = "path/to/your/claims_data.xlsx"

    # Process the data
    output_tables = process_claims_data(input_file)

    # Display summary statistics
    print("\n=== Summary Report ===")
    print(output_tables['summary'])

    print("\n=== By Syndicate ===")
    print(output_tables['by_syndicate'])

    print("\n=== By Risk Code ===")
    print(output_tables['by_risk_code'])

    print("\n=== By Claim Status ===")
    print(output_tables['by_claim_status'])

    # Export to Excel
    export_to_excel(output_tables, "claims_output.xlsx")
