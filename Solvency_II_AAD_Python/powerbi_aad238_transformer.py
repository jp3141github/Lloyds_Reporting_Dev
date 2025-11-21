"""
Power BI Script: AAD238 - Property (S.11.01.01) Transformer
This script transforms raw property data into AAD238 format for Power BI
"""

import pandas as pd
import numpy as np


def transform_aad238(dataset):
    """Transform raw property data into AAD238 format"""

    aad238_columns = {
        'Property_ID': 'Property_ID',
        'Portfolio': 'Portfolio',
        'Fund_Number': 'Fund_Number',
        'Property_Type': 'Property_Type',
        'Country': 'Country',
        'Currency': 'Currency',
        'Purchase_Date': 'Purchase_Date',
        'Purchase_Price': 'Purchase_Price',
        'Valuation_Date': 'Valuation_Date',
        'Current_Valuation': 'Current_Valuation',
        'Rental_Income_Annual': 'Rental_Income_Annual',
        'Occupancy_Rate': 'Occupancy_Rate',
        'Valuation_Method': 'Valuation_Method',
        'Total_Solvency_II_Amount': 'Total_Solvency_II_Amount',
        'Asset_Liquidity': 'Asset_Liquidity',
        'Trust_Fund_Name': 'Trust_Fund_Name'
    }

    output_df = pd.DataFrame()

    for eiopa_code, source_col in aad238_columns.items():
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

    # Valuation Method validation (1=Quoted in active market, 2=Mark-to-model)
    if 'Valuation_Method' in output_df.columns:
        output_df['Valuation_Method'] = output_df['Valuation_Method'].apply(
            lambda x: x if x in ['1', '2'] else '2'
        )

    # Asset Liquidity validation (1/2/3) - Property is typically 2 or 3
    if 'Asset_Liquidity' in output_df.columns:
        output_df['Asset_Liquidity'] = output_df['Asset_Liquidity'].apply(
            lambda x: x if x in ['1', '2', '3'] else '3'
        )

    # Numeric field conversions
    numeric_fields = [
        'Fund_Number', 'Purchase_Price', 'Current_Valuation',
        'Rental_Income_Annual', 'Occupancy_Rate', 'Total_Solvency_II_Amount'
    ]

    for field in numeric_fields:
        if field in output_df.columns:
            output_df[field] = pd.to_numeric(output_df[field], errors='coerce')

    # Date fields
    date_fields = ['Purchase_Date', 'Valuation_Date']
    for field in date_fields:
        if field in output_df.columns:
            output_df[field] = pd.to_datetime(output_df[field], errors='coerce')

    # Calculate additional metrics
    if 'Current_Valuation' in output_df.columns and 'Rental_Income_Annual' in output_df.columns:
        # Rental Yield (%)
        output_df['Rental_Yield'] = (output_df['Rental_Income_Annual'] /
                                      output_df['Current_Valuation'] * 100).round(2)

    if 'Current_Valuation' in output_df.columns and 'Purchase_Price' in output_df.columns:
        # Capital Appreciation (%)
        output_df['Capital_Appreciation'] = ((output_df['Current_Valuation'] -
                                              output_df['Purchase_Price']) /
                                             output_df['Purchase_Price'] * 100).round(2)

    return output_df


# Main execution for Power BI
if __name__ == "__main__":
    result = transform_aad238(dataset)
    print(f"AAD238 Records: {len(result)}")
    print(f"Total Property Valuation: {result['Current_Valuation'].sum():,.2f}")
    print(f"Total Annual Rental Income: {result['Rental_Income_Annual'].sum():,.2f}")
    if 'Rental_Yield' in result.columns:
        print(f"Average Rental Yield: {result['Rental_Yield'].mean():.2f}%")
    if 'Occupancy_Rate' in result.columns:
        print(f"Average Occupancy Rate: {result['Occupancy_Rate'].mean():.2f}%")
