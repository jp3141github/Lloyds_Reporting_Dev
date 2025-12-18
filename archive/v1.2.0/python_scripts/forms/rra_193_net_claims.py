"""
RRA 193 Net Claims Form - Power BI Python Script
This script processes and analyzes RRA 193 Net Claims development triangles
"""

import pandas as pd
import numpy as np


def process_rra_193(data_source='../../synthetic_data/rra_193_net_claims.csv'):
    """
    Process RRA 193 Net Claims data for Power BI

    Parameters:
    -----------
    data_source : str
        Path to the net claims data CSV file

    Returns:
    --------
    pandas.DataFrame
        Processed claims data ready for Power BI visualization
    """

    # Load data
    df = pd.read_csv(data_source)

    # Calculate key metrics
    df['Incurred_Claims'] = df['Cumulative_Paid_Claims'] + df['Case_Reserves'] + df['IBNR_Reserve']
    df['Loss_Ratio_Net'] = np.where(
        df['Net_Premium_Written'] > 0,
        df['Total_Incurred'] / df['Net_Premium_Written'],
        0
    )
    df['Loss_Ratio_Gross'] = np.where(
        df['Gross_Premium_Written'] > 0,
        df['Total_Incurred'] / df['Gross_Premium_Written'],
        0
    )

    # Calculate development factors (year-over-year)
    df = df.sort_values(['Syndicate_Number', 'Year_of_Account', 'LOB_Code', 'Development_Year'])

    # Calculate paid development
    df['Prior_Cumulative_Paid'] = df.groupby(
        ['Syndicate_Number', 'Year_of_Account', 'LOB_Code']
    )['Cumulative_Paid_Claims'].shift(1)

    df['Paid_Development_Factor'] = np.where(
        df['Prior_Cumulative_Paid'] > 0,
        df['Cumulative_Paid_Claims'] / df['Prior_Cumulative_Paid'],
        np.nan
    )

    # Calculate incurred development
    df['Prior_Total_Incurred'] = df.groupby(
        ['Syndicate_Number', 'Year_of_Account', 'LOB_Code']
    )['Total_Incurred'].shift(1)

    df['Incurred_Development_Factor'] = np.where(
        df['Prior_Total_Incurred'] > 0,
        df['Total_Incurred'] / df['Prior_Total_Incurred'],
        np.nan
    )

    # Calculate reserve ratios
    df['Case_Reserve_Ratio'] = np.where(
        df['Total_Incurred'] > 0,
        df['Case_Reserves'] / df['Total_Incurred'],
        0
    )

    df['IBNR_Ratio'] = np.where(
        df['Total_Incurred'] > 0,
        df['IBNR_Reserve'] / df['Total_Incurred'],
        0
    )

    df['Paid_Ratio'] = np.where(
        df['Total_Incurred'] > 0,
        df['Cumulative_Paid_Claims'] / df['Total_Incurred'],
        0
    )

    # Calculate claims closure rate
    df['Claims_Closure_Rate'] = np.where(
        df['Number_of_Claims'] > 0,
        df['Number_of_Claims_Closed'] / df['Number_of_Claims'],
        0
    )

    # Add maturity indicators
    df['Maturity_Years'] = df['Development_Year']
    df['Is_Mature'] = df['Development_Year'] >= 3

    # Calculate average claim amounts
    df['Average_Paid_Per_Claim'] = np.where(
        df['Number_of_Claims_Closed'] > 0,
        df['Cumulative_Paid_Claims'] / df['Number_of_Claims_Closed'],
        0
    )

    df['Average_Incurred_Per_Claim'] = np.where(
        df['Number_of_Claims'] > 0,
        df['Total_Incurred'] / df['Number_of_Claims'],
        0
    )

    return df


def create_development_triangle(data_source='../../synthetic_data/rra_193_net_claims.csv',
                                metric='Total_Incurred',
                                syndicate=None,
                                lob_code=None):
    """
    Create a development triangle for a specific metric

    Parameters:
    -----------
    data_source : str
        Path to the data file
    metric : str
        Metric to display ('Total_Incurred', 'Cumulative_Paid_Claims', etc.)
    syndicate : int, optional
        Filter for specific syndicate
    lob_code : str, optional
        Filter for specific line of business

    Returns:
    --------
    pandas.DataFrame
        Development triangle
    """

    df = pd.read_csv(data_source)

    # Apply filters
    if syndicate:
        df = df[df['Syndicate_Number'] == syndicate]
    if lob_code:
        df = df[df['LOB_Code'] == lob_code]

    # Pivot to create triangle
    triangle = df.pivot_table(
        values=metric,
        index='Year_of_Account',
        columns='Development_Year',
        aggfunc='sum',
        fill_value=0
    )

    return triangle


def calculate_chain_ladder(data_source='../../synthetic_data/rra_193_net_claims.csv',
                           syndicate=None,
                           lob_code=None):
    """
    Calculate chain ladder development factors

    Parameters:
    -----------
    data_source : str
        Path to the data file
    syndicate : int, optional
        Filter for specific syndicate
    lob_code : str, optional
        Filter for specific line of business

    Returns:
    --------
    pandas.DataFrame
        Development factors by development year
    """

    df = process_rra_193(data_source)

    # Apply filters
    if syndicate:
        df = df[df['Syndicate_Number'] == syndicate]
    if lob_code:
        df = df[df['LOB_Code'] == lob_code]

    # Calculate average development factors
    dev_factors = df.groupby('Development_Year').agg({
        'Paid_Development_Factor': ['mean', 'median', 'std', 'count'],
        'Incurred_Development_Factor': ['mean', 'median', 'std', 'count']
    }).reset_index()

    dev_factors.columns = ['_'.join(col).strip('_') for col in dev_factors.columns.values]

    # Rename for clarity
    dev_factors = dev_factors.rename(columns={
        'Development_Year': 'Development_Year',
        'Paid_Development_Factor_mean': 'Paid_LDF_Mean',
        'Paid_Development_Factor_median': 'Paid_LDF_Median',
        'Paid_Development_Factor_std': 'Paid_LDF_StdDev',
        'Paid_Development_Factor_count': 'Paid_Sample_Size',
        'Incurred_Development_Factor_mean': 'Incurred_LDF_Mean',
        'Incurred_Development_Factor_median': 'Incurred_LDF_Median',
        'Incurred_Development_Factor_std': 'Incurred_LDF_StdDev',
        'Incurred_Development_Factor_count': 'Incurred_Sample_Size'
    })

    return dev_factors


def get_claims_summary_by_yoa(data_source='../../synthetic_data/rra_193_net_claims.csv'):
    """
    Generate claims summary by Year of Account

    Returns:
    --------
    pandas.DataFrame
        Summary by Year of Account
    """

    df = process_rra_193(data_source)

    # Get latest development year for each YoA
    latest = df.sort_values('Development_Year').groupby(
        ['Syndicate_Number', 'Year_of_Account', 'LOB_Code']
    ).tail(1)

    summary = latest.groupby('Year_of_Account').agg({
        'Gross_Premium_Written': 'sum',
        'Net_Premium_Written': 'sum',
        'Cumulative_Paid_Claims': 'sum',
        'Case_Reserves': 'sum',
        'IBNR_Reserve': 'sum',
        'Total_Incurred': 'sum',
        'Number_of_Claims': 'sum',
        'Number_of_Claims_Closed': 'sum'
    }).reset_index()

    summary['Net_Loss_Ratio'] = np.where(
        summary['Net_Premium_Written'] > 0,
        summary['Total_Incurred'] / summary['Net_Premium_Written'],
        0
    )

    summary['Claims_Closure_Rate'] = np.where(
        summary['Number_of_Claims'] > 0,
        summary['Number_of_Claims_Closed'] / summary['Number_of_Claims'],
        0
    )

    # Convert to millions for readability
    for col in ['Gross_Premium_Written', 'Net_Premium_Written', 'Cumulative_Paid_Claims',
                'Case_Reserves', 'IBNR_Reserve', 'Total_Incurred']:
        summary[f'{col}_M'] = summary[col] / 1000000
        summary = summary.drop(columns=[col])

    return summary


def get_claims_summary_by_lob(data_source='../../synthetic_data/rra_193_net_claims.csv'):
    """
    Generate claims summary by Line of Business

    Returns:
    --------
    pandas.DataFrame
        Summary by LOB
    """

    df = process_rra_193(data_source)

    # Get latest development year for each combination
    latest = df.sort_values('Development_Year').groupby(
        ['Syndicate_Number', 'Year_of_Account', 'LOB_Code']
    ).tail(1)

    summary = latest.groupby('LOB_Code').agg({
        'Gross_Premium_Written': 'sum',
        'Net_Premium_Written': 'sum',
        'Cumulative_Paid_Claims': 'sum',
        'Case_Reserves': 'sum',
        'IBNR_Reserve': 'sum',
        'Total_Incurred': 'sum',
        'Number_of_Claims': 'sum',
        'Loss_Ratio_Net': 'mean'
    }).reset_index()

    summary['Average_Claim_Size'] = np.where(
        summary['Number_of_Claims'] > 0,
        summary['Total_Incurred'] / summary['Number_of_Claims'],
        0
    )

    # Convert to millions
    for col in ['Gross_Premium_Written', 'Net_Premium_Written', 'Cumulative_Paid_Claims',
                'Case_Reserves', 'IBNR_Reserve', 'Total_Incurred', 'Average_Claim_Size']:
        summary[f'{col}_M'] = summary[col] / 1000000
        summary = summary.drop(columns=[col])

    summary = summary.round(2)

    return summary


# For use in Power BI
# df = process_rra_193()


if __name__ == "__main__":
    # Test the functions
    print("Processing RRA 193 Net Claims Data...")
    df = process_rra_193()
    print(f"\nProcessed {len(df)} records")

    print("\n" + "="*80)
    print("Claims Summary by Year of Account:")
    print("="*80)
    print(get_claims_summary_by_yoa())

    print("\n" + "="*80)
    print("Claims Summary by Line of Business:")
    print("="*80)
    print(get_claims_summary_by_lob())

    print("\n" + "="*80)
    print("Chain Ladder Development Factors:")
    print("="*80)
    print(calculate_chain_ladder())
