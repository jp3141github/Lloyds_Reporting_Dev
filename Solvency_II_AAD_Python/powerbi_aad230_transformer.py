"""
Power BI Script: AAD230 - List of Assets (S.06.02.01) Transformer
This script transforms raw asset data into the AAD230 return format for Power BI

Usage in Power BI:
1. Import your asset data as 'dataset'
2. Run this script as a Python transformation
3. The output will be the formatted AAD230 table
"""

import pandas as pd
import numpy as np


def transform_aad230(dataset):
    """
    Transform raw asset data into AAD230 format

    Parameters:
    -----------
    dataset : pandas.DataFrame
        Input dataframe with raw asset data

    Returns:
    --------
    pandas.DataFrame
        Formatted AAD230 output table
    """

    # Define the AAD230 schema based on Solvency II specifications
    aad230_columns = {
        'C0060_Portfolio': 'Portfolio',
        'C0070_Fund_Number': 'Fund_Number',
        'C0090_Asset_Held_Unit_Linked': 'Asset_Held_Unit_Linked',
        'C0040_Asset_ID_Code': 'Asset_ID_Code',
        'C0050_Asset_ID_Code_Type': 'Asset_ID_Code_Type',
        'C0100_Asset_Pledged_Collateral': 'Asset_Pledged_Collateral',
        'C0190_Item_Title': 'Item_Title',
        'C0200_Issuer_Name': 'Issuer_Name',
        'C0210_Issuer_Code': 'Issuer_Code',
        'C0220_Type_Issuer_Code': 'Type_Issuer_Code',
        'C0230_Issuer_Sector': 'Issuer_Sector',
        'C0240_Issuer_Group': 'Issuer_Group',
        'C0250_Issuer_Group_Code': 'Issuer_Group_Code',
        'C0260_Type_Issuer_Group_Code': 'Type_Issuer_Group_Code',
        'C0270_Issuer_Country': 'Issuer_Country',
        'C0110_Country_Custody': 'Country_Custody',
        'C0280_Currency': 'Currency',
        'C0290_CIC': 'CIC',
        'C0310_Holdings_Related_Undertakings': 'Holdings_Related_Undertakings',
        'C0320_External_Rating': 'External_Rating',
        'C0330_Nominated_ECAI': 'Nominated_ECAI',
        'C0360_Duration': 'Duration',
        'C0130_Quantity': 'Quantity',
        'C0140_Par_Amount': 'Par_Amount',
        'C0370_Unit_Solvency_II_Price': 'Unit_Solvency_II_Price',
        'C0380_Unit_Pct_Par_Amount_Price': 'Unit_Pct_Par_Amount_Price',
        'C0150_Valuation_Method': 'Valuation_Method',
        'C0160_Acquisition_Value': 'Acquisition_Value',
        'C0170_Total_Solvency_II_Amount': 'Total_Solvency_II_Amount',
        'C0390_Maturity_Date': 'Maturity_Date',
        'C0180_Accrued_Interest': 'Accrued_Interest',
        'C0180_Market_Value_Non_FIS': 'Market_Value_Non_FIS',
        'C0180_Market_Value_FIS': 'Market_Value_FIS',
        'C0080_Matching_Portfolio_Numbers': 'Matching_Portfolio_Numbers',
        'C0120_Custodian': 'Custodian',
        'C0300_Infrastructure_Investment': 'Infrastructure_Investment',
        'C0340_Credit_Quality_Step': 'Credit_Quality_Step',
        'C0350_Internal_Rating': 'Internal_Rating',
        'C0292_SCR_Calc_Approach_CIU': 'SCR_Calc_Approach_CIU',
        'Asset_Liquidity': 'Asset_Liquidity',
        'Fund_Redemption_Frequency': 'Fund_Redemption_Frequency',
        'Trust_Fund_Name': 'Trust_Fund_Name'
    }

    # Create output dataframe with mapped columns
    output_df = pd.DataFrame()

    for eiopa_code, source_col in aad230_columns.items():
        if source_col in dataset.columns:
            output_df[eiopa_code] = dataset[source_col]
        else:
            # Initialize missing columns with None/NaN
            output_df[eiopa_code] = None

    # Apply data validations and transformations

    # Portfolio validation (should be L, NL, RF, OIF, SF, or G)
    valid_portfolios = ['L', 'NL', 'RF', 'OIF', 'SF', 'G']
    output_df['C0060_Portfolio'] = output_df['C0060_Portfolio'].apply(
        lambda x: x if x in valid_portfolios else 'NL'
    )

    # Asset Held Unit Linked validation (Y/N)
    output_df['C0090_Asset_Held_Unit_Linked'] = output_df['C0090_Asset_Held_Unit_Linked'].apply(
        lambda x: x if x in ['Y', 'N'] else 'N'
    )

    # Asset Pledged Collateral validation (Y/N)
    output_df['C0100_Asset_Pledged_Collateral'] = output_df['C0100_Asset_Pledged_Collateral'].apply(
        lambda x: x if x in ['Y', 'N'] else 'N'
    )

    # Holdings Related Undertakings validation (Y/N)
    output_df['C0310_Holdings_Related_Undertakings'] = output_df['C0310_Holdings_Related_Undertakings'].apply(
        lambda x: x if x in ['Y', 'N'] else 'N'
    )

    # Infrastructure Investment validation (Y/N)
    output_df['C0300_Infrastructure_Investment'] = output_df['C0300_Infrastructure_Investment'].apply(
        lambda x: x if x in ['Y', 'N'] else 'N'
    )

    # Numeric field validations
    numeric_fields = [
        'C0070_Fund_Number', 'C0360_Duration', 'C0130_Quantity',
        'C0140_Par_Amount', 'C0370_Unit_Solvency_II_Price',
        'C0380_Unit_Pct_Par_Amount_Price', 'C0160_Acquisition_Value',
        'C0170_Total_Solvency_II_Amount', 'C0180_Accrued_Interest',
        'C0180_Market_Value_Non_FIS', 'C0180_Market_Value_FIS',
        'C0080_Matching_Portfolio_Numbers', 'C0340_Credit_Quality_Step'
    ]

    for field in numeric_fields:
        if field in output_df.columns:
            output_df[field] = pd.to_numeric(output_df[field], errors='coerce')

    # Date field formatting
    date_fields = ['C0390_Maturity_Date']
    for field in date_fields:
        if field in output_df.columns:
            output_df[field] = pd.to_datetime(output_df[field], errors='coerce')

    # Calculate Total Solvency II Amount if missing
    if 'C0170_Total_Solvency_II_Amount' in output_df.columns:
        mask = output_df['C0170_Total_Solvency_II_Amount'].isna()
        if mask.any():
            output_df.loc[mask, 'C0170_Total_Solvency_II_Amount'] = (
                output_df.loc[mask, 'C0130_Quantity'] *
                output_df.loc[mask, 'C0370_Unit_Solvency_II_Price']
            )

    return output_df


def validate_aad230(df):
    """
    Validate AAD230 data against business rules

    Parameters:
    -----------
    df : pandas.DataFrame
        AAD230 formatted dataframe

    Returns:
    --------
    dict
        Dictionary containing validation results and error messages
    """

    validation_results = {
        'is_valid': True,
        'errors': [],
        'warnings': []
    }

    # Check for duplicate Asset IDs
    duplicate_ids = df[df.duplicated(subset=['C0040_Asset_ID_Code'], keep=False)]
    if not duplicate_ids.empty:
        validation_results['errors'].append(
            f"Duplicate Asset ID Codes found: {duplicate_ids['C0040_Asset_ID_Code'].unique()}"
        )
        validation_results['is_valid'] = False

    # Check for required fields
    required_fields = ['C0040_Asset_ID_Code', 'C0050_Asset_ID_Code_Type',
                      'C0170_Total_Solvency_II_Amount']

    for field in required_fields:
        if field in df.columns:
            null_count = df[field].isna().sum()
            if null_count > 0:
                validation_results['errors'].append(
                    f"Required field {field} has {null_count} null values"
                )
                validation_results['is_valid'] = False

    # Check Fund Number for RF portfolio
    rf_mask = df['C0060_Portfolio'] == 'RF'
    rf_no_fund = df[rf_mask & df['C0070_Fund_Number'].isna()]
    if not rf_no_fund.empty:
        validation_results['warnings'].append(
            f"RF Portfolio entries without Fund Number: {len(rf_no_fund)} records"
        )

    # Check for negative values in amount fields
    amount_fields = ['C0170_Total_Solvency_II_Amount', 'C0160_Acquisition_Value']
    for field in amount_fields:
        if field in df.columns:
            negative_count = (df[field] < 0).sum()
            if negative_count > 0:
                validation_results['warnings'].append(
                    f"Field {field} has {negative_count} negative values"
                )

    return validation_results


def add_summary_statistics(df):
    """
    Add summary statistics for reporting

    Parameters:
    -----------
    df : pandas.DataFrame
        AAD230 formatted dataframe

    Returns:
    --------
    dict
        Dictionary containing summary statistics
    """

    summary = {
        'total_records': len(df),
        'total_solvency_ii_amount': df['C0170_Total_Solvency_II_Amount'].sum(),
        'total_acquisition_value': df['C0160_Acquisition_Value'].sum(),
        'by_portfolio': df.groupby('C0060_Portfolio')['C0170_Total_Solvency_II_Amount'].sum().to_dict(),
        'by_cic': df.groupby('C0290_CIC')['C0170_Total_Solvency_II_Amount'].sum().to_dict(),
        'by_currency': df.groupby('C0280_Currency')['C0170_Total_Solvency_II_Amount'].sum().to_dict(),
        'unique_issuers': df['C0200_Issuer_Name'].nunique(),
        'unique_currencies': df['C0280_Currency'].nunique()
    }

    return summary


# Main execution for Power BI
if __name__ == "__main__":
    # This section runs when used in Power BI
    # Power BI provides the 'dataset' variable automatically

    # Transform the data
    result = transform_aad230(dataset)

    # Validate the output
    validation = validate_aad230(result)

    # Print validation results for Power BI query diagnostics
    if not validation['is_valid']:
        print("VALIDATION ERRORS:")
        for error in validation['errors']:
            print(f"  - {error}")

    if validation['warnings']:
        print("VALIDATION WARNINGS:")
        for warning in validation['warnings']:
            print(f"  - {warning}")

    # Generate summary statistics
    summary = add_summary_statistics(result)
    print(f"\nSummary Statistics:")
    print(f"  Total Records: {summary['total_records']}")
    print(f"  Total Solvency II Amount: {summary['total_solvency_ii_amount']:,.2f}")
    print(f"  Unique Issuers: {summary['unique_issuers']}")
    print(f"  Unique Currencies: {summary['unique_currencies']}")

    # The 'result' variable is automatically returned to Power BI
