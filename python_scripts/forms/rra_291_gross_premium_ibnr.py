"""
RRA 291 Gross Premium and IBNR Form - Power BI Python Script
This script processes RRA 291 Gross Premium and IBNR estimates
"""

import pandas as pd
import numpy as np


def process_rra_291(data_source='../../synthetic_data/rra_291_gross_premium_ibnr.csv'):
    """
    Process RRA 291 Gross Premium and IBNR data for Power BI

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

    # Calculate total incurred
    df['Total_Incurred_Gross'] = (
        df['Paid_Claims_Gross'] +
        df['Case_Reserves_Gross'] +
        df['IBNR_Best_Estimate']
    )

    # Calculate reserve ratios
    df['Case_Reserve_Ratio'] = np.where(
        df['Total_Incurred_Gross'] > 0,
        df['Case_Reserves_Gross'] / df['Total_Incurred_Gross'],
        0
    )

    df['IBNR_Ratio'] = np.where(
        df['Total_Incurred_Gross'] > 0,
        df['IBNR_Best_Estimate'] / df['Total_Incurred_Gross'],
        0
    )

    df['Paid_Ratio'] = np.where(
        df['Total_Incurred_Gross'] > 0,
        df['Paid_Claims_Gross'] / df['Total_Incurred_Gross'],
        0
    )

    # Calculate IBNR range
    df['IBNR_Range'] = df['IBNR_High'] - df['IBNR_Low']
    df['IBNR_Range_Pct'] = np.where(
        df['IBNR_Best_Estimate'] > 0,
        df['IBNR_Range'] / df['IBNR_Best_Estimate'],
        0
    )

    # Calculate variance from best estimate
    df['IBNR_High_Variance'] = df['IBNR_High'] - df['IBNR_Best_Estimate']
    df['IBNR_Low_Variance'] = df['IBNR_Best_Estimate'] - df['IBNR_Low']

    # Calculate ultimate loss and loss ratio
    df['Ultimate_Loss'] = df['Total_Incurred_Gross']
    df['Earned_Premium_Ratio'] = np.where(
        df['Gross_Written_Premium'] > 0,
        df['Gross_Earned_Premium'] / df['Gross_Written_Premium'],
        0
    )

    # Calculate loss ratio metrics
    df['Loss_Ratio_Incurred'] = np.where(
        df['Gross_Earned_Premium'] > 0,
        df['Total_Incurred_Gross'] / df['Gross_Earned_Premium'],
        0
    )

    df['Loss_Ratio_Paid'] = np.where(
        df['Gross_Earned_Premium'] > 0,
        df['Paid_Claims_Gross'] / df['Gross_Earned_Premium'],
        0
    )

    # Add year age (assuming current year is 2024)
    df['Year_Age'] = 2024 - df['Year_of_Account']

    # Maturity indicators
    df['Is_Mature'] = df['Year_Age'] >= 3
    df['Maturity_Level'] = pd.cut(
        df['Year_Age'],
        bins=[-1, 1, 3, 5, 100],
        labels=['Immature', 'Developing', 'Mature', 'Very Mature']
    )

    return df


def get_ibnr_summary_by_yoa(data_source='../../synthetic_data/rra_291_gross_premium_ibnr.csv'):
    """
    Generate IBNR summary by Year of Account

    Returns:
    --------
    pandas.DataFrame
        Summary by Year of Account
    """

    df = process_rra_291(data_source)

    summary = df.groupby('Year_of_Account').agg({
        'Gross_Written_Premium': 'sum',
        'Gross_Earned_Premium': 'sum',
        'Paid_Claims_Gross': 'sum',
        'Case_Reserves_Gross': 'sum',
        'IBNR_Best_Estimate': 'sum',
        'IBNR_High': 'sum',
        'IBNR_Low': 'sum',
        'Total_Incurred_Gross': 'sum',
        'Ultimate_Loss_Ratio': 'mean'
    }).reset_index()

    # Calculate aggregated metrics
    summary['Loss_Ratio'] = np.where(
        summary['Gross_Earned_Premium'] > 0,
        summary['Total_Incurred_Gross'] / summary['Gross_Earned_Premium'],
        0
    )

    summary['IBNR_to_Premium_Ratio'] = np.where(
        summary['Gross_Earned_Premium'] > 0,
        summary['IBNR_Best_Estimate'] / summary['Gross_Earned_Premium'],
        0
    )

    # Add year age
    summary['Year_Age'] = 2024 - summary['Year_of_Account']

    # Convert to millions
    for col in ['Gross_Written_Premium', 'Gross_Earned_Premium', 'Paid_Claims_Gross',
                'Case_Reserves_Gross', 'IBNR_Best_Estimate', 'IBNR_High', 'IBNR_Low',
                'Total_Incurred_Gross']:
        summary[f'{col}_M'] = summary[col] / 1000000
        summary = summary.drop(columns=[col])

    summary = summary.round(2)

    return summary


def get_ibnr_summary_by_lob(data_source='../../synthetic_data/rra_291_gross_premium_ibnr.csv'):
    """
    Generate IBNR summary by Line of Business

    Returns:
    --------
    pandas.DataFrame
        Summary by LOB
    """

    df = process_rra_291(data_source)

    summary = df.groupby('LOB_Code').agg({
        'Gross_Written_Premium': 'sum',
        'Gross_Earned_Premium': 'sum',
        'Paid_Claims_Gross': 'sum',
        'Case_Reserves_Gross': 'sum',
        'IBNR_Best_Estimate': 'sum',
        'IBNR_High': 'sum',
        'IBNR_Low': 'sum',
        'Total_Incurred_Gross': 'sum',
        'Ultimate_Loss_Ratio': 'mean',
        'IBNR_Ratio': 'mean'
    }).reset_index()

    # Calculate aggregated metrics
    summary['Loss_Ratio'] = np.where(
        summary['Gross_Earned_Premium'] > 0,
        summary['Total_Incurred_Gross'] / summary['Gross_Earned_Premium'],
        0
    )

    # Convert to millions
    for col in ['Gross_Written_Premium', 'Gross_Earned_Premium', 'Paid_Claims_Gross',
                'Case_Reserves_Gross', 'IBNR_Best_Estimate', 'IBNR_High', 'IBNR_Low',
                'Total_Incurred_Gross']:
        summary[f'{col}_M'] = summary[col] / 1000000
        summary = summary.drop(columns=[col])

    summary = summary.round(2)

    return summary


def get_ibnr_range_analysis(data_source='../../synthetic_data/rra_291_gross_premium_ibnr.csv'):
    """
    Analyze IBNR estimate ranges

    Returns:
    --------
    pandas.DataFrame
        IBNR range analysis
    """

    df = process_rra_291(data_source)

    analysis = df.groupby(['Year_of_Account', 'LOB_Code']).agg({
        'IBNR_Best_Estimate': 'sum',
        'IBNR_High': 'sum',
        'IBNR_Low': 'sum',
        'IBNR_Range': 'sum',
        'IBNR_Range_Pct': 'mean'
    }).reset_index()

    # Calculate coefficient of variation
    analysis['IBNR_CV'] = np.where(
        analysis['IBNR_Best_Estimate'] > 0,
        analysis['IBNR_Range'] / (2 * analysis['IBNR_Best_Estimate']),
        0
    )

    # Categorize uncertainty
    analysis['Uncertainty_Level'] = pd.cut(
        analysis['IBNR_Range_Pct'],
        bins=[0, 0.2, 0.4, 0.6, 100],
        labels=['Low', 'Moderate', 'High', 'Very High']
    )

    # Convert to millions
    for col in ['IBNR_Best_Estimate', 'IBNR_High', 'IBNR_Low', 'IBNR_Range']:
        analysis[f'{col}_M'] = analysis[col] / 1000000
        analysis = analysis.drop(columns=[col])

    analysis = analysis.round(2)

    return analysis


def get_ultimate_loss_ratio_trend(data_source='../../synthetic_data/rra_291_gross_premium_ibnr.csv'):
    """
    Analyze ultimate loss ratio trends

    Returns:
    --------
    pandas.DataFrame
        Loss ratio trends by year and LOB
    """

    df = process_rra_291(data_source)

    trend = df.groupby(['Year_of_Account', 'LOB_Code']).agg({
        'Gross_Earned_Premium': 'sum',
        'Total_Incurred_Gross': 'sum',
        'Ultimate_Loss_Ratio': 'mean',
        'Loss_Ratio_Incurred': 'mean',
        'Year_Age': 'first'
    }).reset_index()

    # Calculate actual loss ratio from totals
    trend['Actual_Loss_Ratio'] = np.where(
        trend['Gross_Earned_Premium'] > 0,
        trend['Total_Incurred_Gross'] / trend['Gross_Earned_Premium'],
        0
    )

    # Identify outliers (loss ratio > 1.0)
    trend['Is_Outlier'] = trend['Actual_Loss_Ratio'] > 1.0

    trend = trend.round(4)

    return trend


# For use in Power BI
# df = process_rra_291()


if __name__ == "__main__":
    # Test the functions
    print("Processing RRA 291 Gross Premium and IBNR Data...")
    df = process_rra_291()
    print(f"\nProcessed {len(df)} records")

    print("\n" + "="*80)
    print("IBNR Summary by Year of Account:")
    print("="*80)
    print(get_ibnr_summary_by_yoa())

    print("\n" + "="*80)
    print("IBNR Summary by Line of Business:")
    print("="*80)
    print(get_ibnr_summary_by_lob())

    print("\n" + "="*80)
    print("IBNR Range Analysis (Sample):")
    print("="*80)
    print(get_ibnr_range_analysis().head(10))
