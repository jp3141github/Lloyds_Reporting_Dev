"""
RRA 292 Net Premium and IBNR Form - Power BI Python Script
This script processes RRA 292 Net Premium and IBNR estimates (after reinsurance)
"""

import pandas as pd
import numpy as np


def process_rra_292(data_source='../../synthetic_data/rra_292_net_premium_ibnr.csv'):
    """
    Process RRA 292 Net Premium and IBNR data for Power BI

    Parameters:
    -----------
    data_source : str
        Path to the data CSV file

    Returns:
    --------
    pandas.DataFrame
        Processed data ready for Power BI visualization
    """

    # Load data
    df = pd.read_csv(data_source)

    # Calculate total incurred (net)
    df['Total_Incurred_Net'] = (
        df['Paid_Claims_Net'] +
        df['Case_Reserves_Net'] +
        df['IBNR_Best_Estimate_Net']
    )

    # Calculate reserve ratios
    df['Case_Reserve_Ratio'] = np.where(
        df['Total_Incurred_Net'] > 0,
        df['Case_Reserves_Net'] / df['Total_Incurred_Net'],
        0
    )

    df['IBNR_Ratio'] = np.where(
        df['Total_Incurred_Net'] > 0,
        df['IBNR_Best_Estimate_Net'] / df['Total_Incurred_Net'],
        0
    )

    df['Paid_Ratio'] = np.where(
        df['Total_Incurred_Net'] > 0,
        df['Paid_Claims_Net'] / df['Total_Incurred_Net'],
        0
    )

    # Calculate IBNR range (net)
    df['IBNR_Range_Net'] = df['IBNR_High_Net'] - df['IBNR_Low_Net']
    df['IBNR_Range_Pct'] = np.where(
        df['IBNR_Best_Estimate_Net'] > 0,
        df['IBNR_Range_Net'] / df['IBNR_Best_Estimate_Net'],
        0
    )

    # Calculate variance from best estimate
    df['IBNR_High_Variance'] = df['IBNR_High_Net'] - df['IBNR_Best_Estimate_Net']
    df['IBNR_Low_Variance'] = df['IBNR_Best_Estimate_Net'] - df['IBNR_Low_Net']

    # Calculate ultimate loss and loss ratio (net)
    df['Ultimate_Loss_Net'] = df['Total_Incurred_Net']
    df['Earned_Premium_Ratio'] = np.where(
        df['Net_Written_Premium'] > 0,
        df['Net_Earned_Premium'] / df['Net_Written_Premium'],
        0
    )

    # Calculate loss ratio metrics (net)
    df['Loss_Ratio_Incurred_Net'] = np.where(
        df['Net_Earned_Premium'] > 0,
        df['Total_Incurred_Net'] / df['Net_Earned_Premium'],
        0
    )

    df['Loss_Ratio_Paid_Net'] = np.where(
        df['Net_Earned_Premium'] > 0,
        df['Paid_Claims_Net'] / df['Net_Earned_Premium'],
        0
    )

    # Add year age
    df['Year_Age'] = 2024 - df['Year_of_Account']

    # Maturity indicators
    df['Is_Mature'] = df['Year_Age'] >= 3
    df['Maturity_Level'] = pd.cut(
        df['Year_Age'],
        bins=[-1, 1, 3, 5, 100],
        labels=['Immature', 'Developing', 'Mature', 'Very Mature']
    )

    return df


def get_ri_recovery_analysis(data_source='../../synthetic_data/rra_292_net_premium_ibnr.csv',
                             gross_data_source='../../synthetic_data/rra_291_gross_premium_ibnr.csv'):
    """
    Analyze reinsurance recoveries by comparing net to gross

    Returns:
    --------
    pandas.DataFrame
        RI recovery analysis
    """

    df_net = process_rra_292(data_source)
    df_gross = pd.read_csv(gross_data_source)

    # Merge on key dimensions
    df_merged = df_net.merge(
        df_gross[['Syndicate_Number', 'Year_of_Account', 'LOB_Code',
                  'Gross_Written_Premium', 'Gross_Earned_Premium',
                  'Paid_Claims_Gross', 'Case_Reserves_Gross', 'IBNR_Best_Estimate']],
        on=['Syndicate_Number', 'Year_of_Account', 'LOB_Code'],
        how='left',
        suffixes=('_Net', '_Gross')
    )

    # Calculate RI recoveries
    df_merged['RI_Written_Premium'] = df_merged['Gross_Written_Premium'] - df_merged['Net_Written_Premium']
    df_merged['RI_Earned_Premium'] = df_merged['Gross_Earned_Premium'] - df_merged['Net_Earned_Premium']
    df_merged['RI_Paid_Recovery'] = df_merged['Paid_Claims_Gross'] - df_merged['Paid_Claims_Net']
    df_merged['RI_Case_Reserve_Recovery'] = df_merged['Case_Reserves_Gross'] - df_merged['Case_Reserves_Net']
    df_merged['RI_IBNR_Recovery'] = df_merged['IBNR_Best_Estimate'] - df_merged['IBNR_Best_Estimate_Net']

    # Calculate RI ratios
    df_merged['RI_Cession_Ratio'] = np.where(
        df_merged['Gross_Written_Premium'] > 0,
        df_merged['RI_Written_Premium'] / df_merged['Gross_Written_Premium'],
        0
    )

    df_merged['RI_Recovery_Ratio'] = np.where(
        df_merged['Paid_Claims_Gross'] > 0,
        df_merged['RI_Paid_Recovery'] / df_merged['Paid_Claims_Gross'],
        0
    )

    return df_merged


def get_net_summary_by_yoa(data_source='../../synthetic_data/rra_292_net_premium_ibnr.csv'):
    """
    Generate Net Premium and IBNR summary by Year of Account

    Returns:
    --------
    pandas.DataFrame
        Summary by Year of Account
    """

    df = process_rra_292(data_source)

    summary = df.groupby('Year_of_Account').agg({
        'Net_Written_Premium': 'sum',
        'Net_Earned_Premium': 'sum',
        'Paid_Claims_Net': 'sum',
        'Case_Reserves_Net': 'sum',
        'IBNR_Best_Estimate_Net': 'sum',
        'IBNR_High_Net': 'sum',
        'IBNR_Low_Net': 'sum',
        'Total_Incurred_Net': 'sum',
        'Ultimate_Loss_Ratio': 'mean'
    }).reset_index()

    # Calculate aggregated metrics
    summary['Loss_Ratio_Net'] = np.where(
        summary['Net_Earned_Premium'] > 0,
        summary['Total_Incurred_Net'] / summary['Net_Earned_Premium'],
        0
    )

    summary['IBNR_to_Premium_Ratio'] = np.where(
        summary['Net_Earned_Premium'] > 0,
        summary['IBNR_Best_Estimate_Net'] / summary['Net_Earned_Premium'],
        0
    )

    # Add year age
    summary['Year_Age'] = 2024 - summary['Year_of_Account']

    # Convert to millions
    for col in ['Net_Written_Premium', 'Net_Earned_Premium', 'Paid_Claims_Net',
                'Case_Reserves_Net', 'IBNR_Best_Estimate_Net', 'IBNR_High_Net',
                'IBNR_Low_Net', 'Total_Incurred_Net']:
        summary[f'{col}_M'] = summary[col] / 1000000
        summary = summary.drop(columns=[col])

    summary = summary.round(2)

    return summary


def get_net_summary_by_lob(data_source='../../synthetic_data/rra_292_net_premium_ibnr.csv'):
    """
    Generate Net Premium and IBNR summary by Line of Business

    Returns:
    --------
    pandas.DataFrame
        Summary by LOB
    """

    df = process_rra_292(data_source)

    summary = df.groupby('LOB_Code').agg({
        'Net_Written_Premium': 'sum',
        'Net_Earned_Premium': 'sum',
        'Paid_Claims_Net': 'sum',
        'Case_Reserves_Net': 'sum',
        'IBNR_Best_Estimate_Net': 'sum',
        'IBNR_High_Net': 'sum',
        'IBNR_Low_Net': 'sum',
        'Total_Incurred_Net': 'sum',
        'Ultimate_Loss_Ratio': 'mean',
        'IBNR_Ratio': 'mean'
    }).reset_index()

    # Calculate aggregated metrics
    summary['Loss_Ratio_Net'] = np.where(
        summary['Net_Earned_Premium'] > 0,
        summary['Total_Incurred_Net'] / summary['Net_Earned_Premium'],
        0
    )

    # Convert to millions
    for col in ['Net_Written_Premium', 'Net_Earned_Premium', 'Paid_Claims_Net',
                'Case_Reserves_Net', 'IBNR_Best_Estimate_Net', 'IBNR_High_Net',
                'IBNR_Low_Net', 'Total_Incurred_Net']:
        summary[f'{col}_M'] = summary[col] / 1000000
        summary = summary.drop(columns=[col])

    summary = summary.round(2)

    return summary


def compare_net_vs_gross(net_data_source='../../synthetic_data/rra_292_net_premium_ibnr.csv',
                         gross_data_source='../../synthetic_data/rra_291_gross_premium_ibnr.csv'):
    """
    Compare net (Form 292) vs gross (Form 291) metrics

    Returns:
    --------
    pandas.DataFrame
        Comparison analysis
    """

    df_net = process_rra_292(net_data_source)
    df_gross = pd.read_csv(gross_data_source)

    # Aggregate both
    net_agg = df_net.groupby(['Year_of_Account', 'LOB_Code']).agg({
        'Net_Earned_Premium': 'sum',
        'Total_Incurred_Net': 'sum'
    }).reset_index()

    gross_agg = df_gross.groupby(['Year_of_Account', 'LOB_Code']).agg({
        'Gross_Earned_Premium': 'sum',
        'Paid_Claims_Gross': 'sum',
        'Case_Reserves_Gross': 'sum',
        'IBNR_Best_Estimate': 'sum'
    }).reset_index()

    gross_agg['Total_Incurred_Gross'] = (
        gross_agg['Paid_Claims_Gross'] +
        gross_agg['Case_Reserves_Gross'] +
        gross_agg['IBNR_Best_Estimate']
    )

    # Merge
    comparison = net_agg.merge(
        gross_agg,
        on=['Year_of_Account', 'LOB_Code'],
        how='outer'
    )

    # Calculate RI impact
    comparison['RI_Premium_Ceded'] = comparison['Gross_Earned_Premium'] - comparison['Net_Earned_Premium']
    comparison['RI_Claims_Recovered'] = comparison['Total_Incurred_Gross'] - comparison['Total_Incurred_Net']

    comparison['Net_Retention_Ratio'] = np.where(
        comparison['Gross_Earned_Premium'] > 0,
        comparison['Net_Earned_Premium'] / comparison['Gross_Earned_Premium'],
        0
    )

    comparison['RI_Loss_Ratio_Benefit'] = np.where(
        comparison['Gross_Earned_Premium'] > 0,
        (comparison['Total_Incurred_Gross'] / comparison['Gross_Earned_Premium']) -
        (comparison['Total_Incurred_Net'] / comparison['Net_Earned_Premium']),
        0
    )

    return comparison


# For use in Power BI
# df = process_rra_292()


if __name__ == "__main__":
    # Test the functions
    print("Processing RRA 292 Net Premium and IBNR Data...")

    try:
        df = process_rra_292()
        print(f"\nProcessed {len(df)} records")

        print("\n" + "="*80)
        print("Net Premium and IBNR Summary by Year of Account:")
        print("="*80)
        print(get_net_summary_by_yoa())

        print("\n" + "="*80)
        print("Net Premium and IBNR Summary by Line of Business:")
        print("="*80)
        print(get_net_summary_by_lob())

        print("\n" + "="*80)
        print("RI Recovery Analysis (Sample):")
        print("="*80)
        ri_analysis = get_ri_recovery_analysis()
        print(ri_analysis[['Year_of_Account', 'LOB_Code', 'RI_Cession_Ratio',
                           'RI_Recovery_Ratio']].head(10))
    except FileNotFoundError:
        print("Note: Synthetic data file not found. Generate with generate_synthetic_lloyds_data.py")
