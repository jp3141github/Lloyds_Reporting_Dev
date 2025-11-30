"""
Power BI Script: AAD235 - Income/Gains and Losses (S.09.01.01) Transformer
This script transforms raw income data into the AAD235 return format for Power BI
"""

import pandas as pd
import numpy as np


def transform_aad235(dataset):
    """Transform raw income/gains data into AAD235 format"""

    aad235_columns = {
        'C0040_Asset_Category': 'Asset_Category',
        'C0070_Dividends': 'Dividends',
        'C0080_Interest': 'Interest',
        'C0090_Rent': 'Rent',
        'C0100_Net_Gains_Losses': 'Net_Gains_Losses',
        'C0110_Unrealised_Gains_Losses': 'Unrealised_Gains_Losses',
        'C0050_Portfolio': 'Portfolio',
        'C0060_Asset_Held_Unit_Linked': 'Asset_Held_Unit_Linked',
        'Fund_Number': 'Fund_Number'
    }

    output_df = pd.DataFrame()

    for eiopa_code, source_col in aad235_columns.items():
        if source_col in dataset.columns:
            output_df[eiopa_code] = dataset[source_col]
        else:
            output_df[eiopa_code] = None

    # Validations
    valid_portfolios = ['L', 'NL', 'RF', 'OIF', 'SF', 'G']
    if 'C0050_Portfolio' in output_df.columns:
        output_df['C0050_Portfolio'] = output_df['C0050_Portfolio'].apply(
            lambda x: x if x in valid_portfolios else 'NL'
        )

    # Asset Held Unit Linked validation (Y/N)
    if 'C0060_Asset_Held_Unit_Linked' in output_df.columns:
        output_df['C0060_Asset_Held_Unit_Linked'] = output_df['C0060_Asset_Held_Unit_Linked'].apply(
            lambda x: x if x in ['Y', 'N'] else 'N'
        )

    # Numeric field conversions
    numeric_fields = [
        'C0070_Dividends', 'C0080_Interest', 'C0090_Rent',
        'C0100_Net_Gains_Losses', 'C0110_Unrealised_Gains_Losses', 'Fund_Number'
    ]

    for field in numeric_fields:
        if field in output_df.columns:
            output_df[field] = pd.to_numeric(output_df[field], errors='coerce')

    # Aggregate by Asset Category if multiple records exist
    if len(output_df) > 0:
        agg_dict = {
            'C0070_Dividends': 'sum',
            'C0080_Interest': 'sum',
            'C0090_Rent': 'sum',
            'C0100_Net_Gains_Losses': 'sum',
            'C0110_Unrealised_Gains_Losses': 'sum'
        }

        group_cols = ['C0040_Asset_Category']
        if 'C0050_Portfolio' in output_df.columns:
            group_cols.append('C0050_Portfolio')

        output_df = output_df.groupby(group_cols, as_index=False).agg(agg_dict)

    return output_df


# Main execution for Power BI
if __name__ == "__main__":
    result = transform_aad235(dataset)
    print(f"AAD235 Records: {len(result)}")
    total_income = (result['C0070_Dividends'].sum() +
                   result['C0080_Interest'].sum() +
                   result['C0090_Rent'].sum())
    print(f"Total Income: {total_income:,.2f}")
    print(f"Net Gains/Losses: {result['C0100_Net_Gains_Losses'].sum():,.2f}")
