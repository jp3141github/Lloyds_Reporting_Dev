"""
Power BI Script: AAD236 - CIU Look-through (S.06.03.01) Transformer
This script transforms Collective Investment Undertaking data into AAD236 format for Power BI
"""

import pandas as pd
import numpy as np


def transform_aad236(dataset):
    """Transform raw CIU data into AAD236 format"""

    aad236_columns = {
        'Investment_Fund_Code': 'Investment_Fund_Code',
        'Investment_Fund_Code_Type': 'Investment_Fund_Code_Type',
        'C0010_CIU_ID_Code': 'CIU_ID_Code',
        'C0020_CIU_ID_Code_Type': 'CIU_ID_Code_Type',
        'Item_Title': 'Item_Title',
        'Issuer_Group': 'Issuer_Group',
        'Issuer_Group_Code': 'Issuer_Group_Code',
        'Issuer_Group_Code_Type': 'Issuer_Group_Code_Type',
        'External_Rating': 'External_Rating',
        'Rating_Agency': 'Rating_Agency',
        'Duration': 'Duration',
        'CIC': 'CIC',
        'C0030_Underlying_Asset_Category': 'Underlying_Asset_Category',
        'C0040_Country_Issue': 'Country_Issue',
        'C0050_Currency': 'Currency',
        'Total_SII_Amount_Non_FIS': 'Total_SII_Amount_Non_FIS',
        'Total_SII_Amount_FIS': 'Total_SII_Amount_FIS',
        'C0060_Total_Solvency_II_Amount': 'Total_Solvency_II_Amount',
        'Issue_Type': 'Issue_Type',
        'Level_Look_Through': 'Level_Look_Through',
        'Maturity_Date': 'Maturity_Date',
        'Fund_Number': 'Fund_Number',
        'Notional_Amount': 'Notional_Amount',
        'Asset_Liquidity': 'Asset_Liquidity',
        'Trust_Fund_Name': 'Trust_Fund_Name'
    }

    output_df = pd.DataFrame()

    for eiopa_code, source_col in aad236_columns.items():
        if source_col in dataset.columns:
            output_df[eiopa_code] = dataset[source_col]
        else:
            output_df[eiopa_code] = None

    # Validations
    # Level of Look-Through validation (1/2/3/9)
    if 'Level_Look_Through' in output_df.columns:
        output_df['Level_Look_Through'] = output_df['Level_Look_Through'].apply(
            lambda x: x if x in ['1', '2', '3', '9'] else '9'
        )

    # Underlying Asset Category validation
    valid_categories = ['1', '2', '3', '4', '5', '9']
    if 'C0030_Underlying_Asset_Category' in output_df.columns:
        output_df['C0030_Underlying_Asset_Category'] = output_df['C0030_Underlying_Asset_Category'].apply(
            lambda x: x if x in valid_categories else '9'
        )

    # Asset Liquidity validation (1/2/3)
    if 'Asset_Liquidity' in output_df.columns:
        output_df['Asset_Liquidity'] = output_df['Asset_Liquidity'].apply(
            lambda x: x if x in ['1', '2', '3'] else '3'
        )

    # Numeric field conversions
    numeric_fields = [
        'Duration', 'Total_SII_Amount_Non_FIS', 'Total_SII_Amount_FIS',
        'C0060_Total_Solvency_II_Amount', 'Fund_Number', 'Notional_Amount'
    ]

    for field in numeric_fields:
        if field in output_df.columns:
            output_df[field] = pd.to_numeric(output_df[field], errors='coerce')

    # Date fields
    if 'Maturity_Date' in output_df.columns:
        output_df['Maturity_Date'] = pd.to_datetime(output_df['Maturity_Date'], errors='coerce')

    return output_df


# Main execution for Power BI
if __name__ == "__main__":
    result = transform_aad236(dataset)
    print(f"AAD236 Records: {len(result)}")
    print(f"Total Solvency II Amount: {result['C0060_Total_Solvency_II_Amount'].sum():,.2f}")
