"""
Power BI Script: AAD233 - Open Derivatives (S.08.01.01) Transformer
This script transforms raw derivatives data into the AAD233 return format for Power BI
"""

import pandas as pd
import numpy as np


def transform_aad233(dataset):
    """Transform raw derivatives data into AAD233 format"""

    aad233_columns = {
        'C0060_Portfolio': 'Portfolio',
        'C0070_Fund_Number': 'Fund_Number',
        'C0080_Derivatives_Unit_Linked': 'Derivatives_Unit_Linked',
        'C0040_Derivative_ID_Code': 'Derivative_ID_Code',
        'C0050_Derivative_ID_Code_Type': 'Derivative_ID_Code_Type',
        'C0260_Counterparty_Name': 'Counterparty_Name',
        'C0270_Counterparty_Code': 'Counterparty_Code',
        'C0280_Type_Counterparty_Code': 'Type_Counterparty_Code',
        'C0290_External_Rating': 'External_Rating',
        'C0300_Nominated_ECAI': 'Nominated_ECAI',
        'C0330_Counterparty_Group': 'Counterparty_Group',
        'C0340_Counterparty_Group_Code': 'Counterparty_Group_Code',
        'C0350_Type_Counterparty_Group_Code': 'Type_Counterparty_Group_Code',
        'C0360_Contract_Name': 'Contract_Name',
        'C0090_Instrument_Underlying': 'Instrument_Underlying',
        'C0370_Currency': 'Currency',
        'C0380_CIC': 'CIC',
        'C0110_Use_Derivative': 'Use_Derivative',
        'C0120_Delta': 'Delta',
        'C0130_Notional_Amount': 'Notional_Amount',
        'C0140_Buyer_Seller': 'Buyer_Seller',
        'C0150_Premium_Paid': 'Premium_Paid',
        'C0160_Premium_Received': 'Premium_Received',
        'C0170_Number_Contracts': 'Number_Contracts',
        'C0180_Contract_Size': 'Contract_Size',
        'C0390_Trigger_Value': 'Trigger_Value',
        'C0400_Unwind_Trigger': 'Unwind_Trigger',
        'C0190_Max_Loss_Unwinding': 'Max_Loss_Unwinding',
        'C0200_Swap_Outflow_Amount': 'Swap_Outflow_Amount',
        'C0210_Swap_Inflow_Amount': 'Swap_Inflow_Amount',
        'C0410_Swap_Delivered_Currency': 'Swap_Delivered_Currency',
        'C0420_Swap_Received_Currency': 'Swap_Received_Currency',
        'C0220_Initial_Date': 'Initial_Date',
        'C0430_Maturity_Date': 'Maturity_Date',
        'C0230_Duration': 'Duration',
        'C0250_Valuation_Method': 'Valuation_Method',
        'Total_SII_Amount_Non_FIS': 'Total_SII_Amount_Non_FIS',
        'Total_SII_Amount_FIS': 'Total_SII_Amount_FIS',
        'C0240_Solvency_II_Value': 'Solvency_II_Value',
        'C0310_Credit_Quality_Step': 'Credit_Quality_Step',
        'C0320_Internal_Rating': 'Internal_Rating',
        'C0100_Type_Code_Underlying': 'Type_Code_Underlying',
        'Trust_Fund_Name': 'Trust_Fund_Name'
    }

    output_df = pd.DataFrame()

    for eiopa_code, source_col in aad233_columns.items():
        if source_col in dataset.columns:
            output_df[eiopa_code] = dataset[source_col]
        else:
            output_df[eiopa_code] = None

    # Validations
    valid_portfolios = ['L', 'NL', 'RF', 'OIF', 'SF', 'G']
    output_df['C0060_Portfolio'] = output_df['C0060_Portfolio'].apply(
        lambda x: x if x in valid_portfolios else 'NL'
    )

    # Use of Derivative validation (MI/MA/EPM)
    output_df['C0110_Use_Derivative'] = output_df['C0110_Use_Derivative'].apply(
        lambda x: x if x in ['MI', 'MA', 'EPM'] else 'MI'
    )

    # Buyer/Seller validation (B/S)
    output_df['C0140_Buyer_Seller'] = output_df['C0140_Buyer_Seller'].apply(
        lambda x: x if x in ['B', 'S'] else 'B'
    )

    # Unwind Trigger validation (B/F/R/N/M/O/NT)
    output_df['C0400_Unwind_Trigger'] = output_df['C0400_Unwind_Trigger'].apply(
        lambda x: x if x in ['B', 'F', 'R', 'N', 'M', 'O', 'NT'] else 'N'
    )

    # Numeric field conversions
    numeric_fields = [
        'C0070_Fund_Number', 'C0120_Delta', 'C0130_Notional_Amount',
        'C0150_Premium_Paid', 'C0160_Premium_Received', 'C0170_Number_Contracts',
        'C0180_Contract_Size', 'C0390_Trigger_Value', 'C0190_Max_Loss_Unwinding',
        'C0200_Swap_Outflow_Amount', 'C0210_Swap_Inflow_Amount',
        'C0230_Duration', 'C0240_Solvency_II_Value', 'C0310_Credit_Quality_Step'
    ]

    for field in numeric_fields:
        if field in output_df.columns:
            output_df[field] = pd.to_numeric(output_df[field], errors='coerce')

    # Date fields
    date_fields = ['C0220_Initial_Date', 'C0430_Maturity_Date']
    for field in date_fields:
        if field in output_df.columns:
            output_df[field] = pd.to_datetime(output_df[field], errors='coerce')

    return output_df


# Main execution for Power BI
if __name__ == "__main__":
    result = transform_aad233(dataset)
    print(f"AAD233 Records: {len(result)}")
    print(f"Total Notional Amount: {result['C0130_Notional_Amount'].sum():,.2f}")
