"""
Power BI Script: AAD237 - Loans and Mortgages (S.10.01.01) Transformer
This script transforms raw loans/mortgages data into AAD237 format for Power BI
"""

import pandas as pd
import numpy as np


def transform_aad237(dataset):
    """Transform raw loans and mortgages data into AAD237 format"""

    aad237_columns = {
        'Loan_ID': 'Loan_ID',
        'Loan_Type': 'Loan_Type',
        'Portfolio': 'Portfolio',
        'Fund_Number': 'Fund_Number',
        'Counterparty_Name': 'Counterparty_Name',
        'Counterparty_Code': 'Counterparty_Code',
        'Type_Counterparty_Code': 'Type_Counterparty_Code',
        'Country': 'Country',
        'Currency': 'Currency',
        'Original_Amount': 'Original_Amount',
        'Outstanding_Amount': 'Outstanding_Amount',
        'Interest_Rate': 'Interest_Rate',
        'Acquisition_Date': 'Acquisition_Date',
        'Maturity_Date': 'Maturity_Date',
        'Duration': 'Duration',
        'Collateral_Value': 'Collateral_Value',
        'Valuation_Method': 'Valuation_Method',
        'Total_Solvency_II_Amount': 'Total_Solvency_II_Amount',
        'Credit_Quality_Step': 'Credit_Quality_Step',
        'Internal_Rating': 'Internal_Rating',
        'Asset_Liquidity': 'Asset_Liquidity'
    }

    output_df = pd.DataFrame()

    for eiopa_code, source_col in aad237_columns.items():
        if source_col in dataset.columns:
            output_df[eiopa_code] = dataset[source_col]
        else:
            output_df[eiopa_code] = None

    # Validations
    valid_portfolios = ['L', 'NL', 'RF', 'OIF', 'SF', 'G']
    if 'Portfolio' in output_df.columns:
        output_df['Portfolio'] = output_df['Portfolio'].apply(
            lambda x: x if x in valid_portfolios else 'NL'
        )

    # Loan Type validation (1=Mortgages, 2=Loans on policies, 3=Policy loans, 4=Other loans)
    valid_loan_types = ['1', '2', '3', '4']
    if 'Loan_Type' in output_df.columns:
        output_df['Loan_Type'] = output_df['Loan_Type'].apply(
            lambda x: x if x in valid_loan_types else '4'
        )

    # Valuation Method validation (1=Quoted in active market, 2=Mark-to-model)
    if 'Valuation_Method' in output_df.columns:
        output_df['Valuation_Method'] = output_df['Valuation_Method'].apply(
            lambda x: x if x in ['1', '2'] else '2'
        )

    # Asset Liquidity validation (1/2/3)
    if 'Asset_Liquidity' in output_df.columns:
        output_df['Asset_Liquidity'] = output_df['Asset_Liquidity'].apply(
            lambda x: x if x in ['1', '2', '3'] else '3'
        )

    # Numeric field conversions
    numeric_fields = [
        'Fund_Number', 'Original_Amount', 'Outstanding_Amount',
        'Interest_Rate', 'Duration', 'Collateral_Value',
        'Total_Solvency_II_Amount', 'Credit_Quality_Step'
    ]

    for field in numeric_fields:
        if field in output_df.columns:
            output_df[field] = pd.to_numeric(output_df[field], errors='coerce')

    # Date fields
    date_fields = ['Acquisition_Date', 'Maturity_Date']
    for field in date_fields:
        if field in output_df.columns:
            output_df[field] = pd.to_datetime(output_df[field], errors='coerce')

    # Calculate Loan-to-Value ratio
    if 'Outstanding_Amount' in output_df.columns and 'Collateral_Value' in output_df.columns:
        output_df['LTV_Ratio'] = (output_df['Outstanding_Amount'] /
                                   output_df['Collateral_Value'] * 100).round(2)

    return output_df


# Main execution for Power BI
if __name__ == "__main__":
    result = transform_aad237(dataset)
    print(f"AAD237 Records: {len(result)}")
    print(f"Total Outstanding Amount: {result['Outstanding_Amount'].sum():,.2f}")
    print(f"Total Solvency II Amount: {result['Total_Solvency_II_Amount'].sum():,.2f}")
    if 'LTV_Ratio' in result.columns:
        print(f"Average LTV Ratio: {result['LTV_Ratio'].mean():.2f}%")
