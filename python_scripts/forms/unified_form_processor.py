"""
Unified Form Processor for RRQ and RRA Data
Automatically detects and processes both quarterly and annual Lloyd's returns
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Literal


class UnifiedFormProcessor:
    """Process Lloyd's forms with automatic RRQ/RRA detection"""

    def __init__(self, data_source: str):
        """
        Initialize processor with data source

        Parameters:
        -----------
        data_source : str
            Path to CSV data file or directory containing multiple files
        """
        self.data_source = Path(data_source)
        self.return_type = None
        self.reporting_quarter = None
        self.reporting_year = None

    def _detect_return_type(self, df: pd.DataFrame) -> dict:
        """
        Automatically detect if data is RRQ or RRA

        Returns:
        --------
        dict : Detection results with return_type, quarter, year
        """
        if 'Return_Type' in df.columns:
            return_type = df['Return_Type'].iloc[0]
            reporting_quarter = df.get('Reporting_Quarter', pd.Series(['N/A'])).iloc[0]
            reporting_year = df.get('Reporting_Year', pd.Series([2024])).iloc[0]

            return {
                'return_type': return_type,
                'reporting_quarter': reporting_quarter if reporting_quarter != 'N/A' else None,
                'reporting_year': int(reporting_year) if pd.notna(reporting_year) else None,
                'is_quarterly': return_type == 'RRQ',
                'is_annual': return_type == 'RRA'
            }
        else:
            # Legacy data without Return_Type field - assume RRA
            return {
                'return_type': 'RRA',
                'reporting_quarter': None,
                'reporting_year': None,
                'is_quarterly': False,
                'is_annual': True
            }

    def process_form_193(self, data_source: Optional[str] = None) -> pd.DataFrame:
        """
        Process Form 193 (Net Claims Development) for RRQ or RRA

        Parameters:
        -----------
        data_source : str, optional
            Override default data source

        Returns:
        --------
        pandas.DataFrame
            Processed claims development data
        """
        if data_source:
            df = pd.read_csv(data_source)
        else:
            df = pd.read_csv(self.data_source)

        # Detect return type
        meta = self._detect_return_type(df)
        self.return_type = meta['return_type']
        self.reporting_quarter = meta['reporting_quarter']
        self.reporting_year = meta['reporting_year']

        # Calculate key metrics (same for both RRQ and RRA)
        df['Incurred_Claims'] = df['Cumulative_Paid_Claims'] + df['Case_Reserves'] + df['IBNR_Reserve']

        df['Loss_Ratio_Net'] = np.where(
            df['Net_Premium_Written'] > 0,
            df['Total_Incurred'] / df['Net_Premium_Written'],
            0
        )

        # Sort for development factor calculations
        df = df.sort_values(['Syndicate_Number', 'Year_of_Account', 'LOB_Code', 'Development_Year'])

        # Calculate development factors
        df['Prior_Cumulative_Paid'] = df.groupby(
            ['Syndicate_Number', 'Year_of_Account', 'LOB_Code']
        )['Cumulative_Paid_Claims'].shift(1)

        df['Paid_Development_Factor'] = np.where(
            (df['Prior_Cumulative_Paid'].notna()) & (df['Prior_Cumulative_Paid'] > 0),
            df['Cumulative_Paid_Claims'] / df['Prior_Cumulative_Paid'],
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

        # Add maturity indicators
        df['Maturity_Years'] = df['Development_Year']
        df['Is_Mature'] = df['Development_Year'] >= 3

        # Average claim amounts
        df['Average_Paid_Per_Claim'] = np.where(
            df['Number_of_Claims_Closed'] > 0,
            df['Cumulative_Paid_Claims'] / df['Number_of_Claims_Closed'],
            0
        )

        # Add return type specific fields
        df['Data_Scope'] = meta['return_type']
        if meta['is_quarterly']:
            df['Quarterly_Period'] = f"{meta['reporting_quarter']} {meta['reporting_year']}"
        else:
            df['Quarterly_Period'] = 'Annual'

        return df

    def process_form_291(self, data_source: Optional[str] = None) -> pd.DataFrame:
        """
        Process Form 291 (Gross Premium and IBNR) for RRQ or RRA

        Parameters:
        -----------
        data_source : str, optional
            Override default data source

        Returns:
        --------
        pandas.DataFrame
            Processed IBNR data
        """
        if data_source:
            df = pd.read_csv(data_source)
        else:
            df = pd.read_csv(self.data_source)

        # Detect return type
        meta = self._detect_return_type(df)

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

        # Calculate IBNR range
        df['IBNR_Range'] = df['IBNR_High'] - df['IBNR_Low']
        df['IBNR_Range_Pct'] = np.where(
            df['IBNR_Best_Estimate'] > 0,
            df['IBNR_Range'] / df['IBNR_Best_Estimate'],
            0
        )

        # Calculate loss ratios
        df['Loss_Ratio_Incurred'] = np.where(
            df['Gross_Earned_Premium'] > 0,
            df['Total_Incurred_Gross'] / df['Gross_Earned_Premium'],
            0
        )

        # Add return type context
        df['Data_Scope'] = meta['return_type']
        if meta['is_quarterly']:
            df['Quarterly_Period'] = f"{meta['reporting_quarter']} {meta['reporting_year']}"

        return df

    def compare_quarters(self, current_data: str, prior_data: str, form: str = '193') -> pd.DataFrame:
        """
        Compare current quarter vs prior quarter (RRQ only)

        Parameters:
        -----------
        current_data : str
            Path to current quarter data
        prior_data : str
            Path to prior quarter data
        form : str
            Form number to compare ('193', '291', etc.)

        Returns:
        --------
        pandas.DataFrame
            Quarter-over-quarter movement analysis
        """
        current = pd.read_csv(current_data)
        prior = pd.read_csv(prior_data)

        # Verify both are RRQ
        current_meta = self._detect_return_type(current)
        prior_meta = self._detect_return_type(prior)

        if not (current_meta['is_quarterly'] and prior_meta['is_quarterly']):
            raise ValueError("Both datasets must be RRQ for quarter comparison")

        # Merge on key dimensions
        key_cols = ['Syndicate_Number', 'Year_of_Account', 'LOB_Code', 'Development_Year']
        available_keys = [col for col in key_cols if col in current.columns and col in prior.columns]

        comparison = current.merge(
            prior,
            on=available_keys,
            how='outer',
            suffixes=('_Current', '_Prior'),
            indicator=True
        )

        # Calculate movements for Form 193
        if form == '193':
            comparison['Paid_Movement'] = (
                comparison.get('Cumulative_Paid_Claims_Current', 0) -
                comparison.get('Cumulative_Paid_Claims_Prior', 0)
            )

            comparison['IBNR_Movement'] = (
                comparison.get('IBNR_Reserve_Current', 0) -
                comparison.get('IBNR_Reserve_Prior', 0)
            )

            comparison['Total_Incurred_Movement'] = (
                comparison.get('Total_Incurred_Current', 0) -
                comparison.get('Total_Incurred_Prior', 0)
            )

            # Flag significant movements (>10% change)
            comparison['Significant_Movement'] = np.abs(
                comparison['Total_Incurred_Movement'] / comparison.get('Total_Incurred_Prior', 1)
            ) > 0.10

        elif form == '291':
            comparison['IBNR_Movement'] = (
                comparison.get('IBNR_Best_Estimate_Current', 0) -
                comparison.get('IBNR_Best_Estimate_Prior', 0)
            )

            comparison['Premium_Movement'] = (
                comparison.get('Gross_Written_Premium_Current', 0) -
                comparison.get('Gross_Written_Premium_Prior', 0)
            )

        comparison['Current_Quarter'] = f"{current_meta['reporting_quarter']} {current_meta['reporting_year']}"
        comparison['Prior_Quarter'] = f"{prior_meta['reporting_quarter']} {prior_meta['reporting_year']}"

        return comparison


def process_unified_rrq_rra(data_path: str, form_number: str) -> pd.DataFrame:
    """
    Convenience function to process any RRQ or RRA form

    Parameters:
    -----------
    data_path : str
        Path to data file
    form_number : str
        Form number ('193', '291', etc.)

    Returns:
    --------
    pandas.DataFrame
        Processed data

    Example:
    --------
    >>> df = process_unified_rrq_rra('rrq_193_net_claims.csv', '193')
    >>> print(df['Data_Scope'].iloc[0])  # 'RRQ' or 'RRA'
    """
    processor = UnifiedFormProcessor(data_path)

    if form_number == '193':
        return processor.process_form_193()
    elif form_number == '291':
        return processor.process_form_291()
    else:
        raise ValueError(f"Form {form_number} not yet supported in unified processor")


# Power BI usage example
"""
# In Power BI Python script:

import sys
sys.path.append(r'C:\path\to\python_scripts\forms')
from unified_form_processor import process_unified_rrq_rra

# Automatically detects RRQ vs RRA
df = process_unified_rrq_rra(
    r'C:\path\to\data\rrq_193_net_claims.csv',
    '193'
)

# df will have 'Data_Scope' column showing 'RRQ' or 'RRA'
# df will have 'Quarterly_Period' showing quarter for RRQ data
"""


if __name__ == "__main__":
    # Test with RRA data
    print("Testing with RRA data...")
    print("="*70)

    try:
        processor_rra = UnifiedFormProcessor('../../synthetic_data_rra_2024/rra_193_net_claims.csv')
        df_rra = processor_rra.process_form_193()
        print(f"Processed RRA Form 193: {len(df_rra)} records")
        print(f"Return Type: {df_rra['Data_Scope'].iloc[0]}")
        print(f"Years of Account: {sorted(df_rra['Year_of_Account'].unique())}")
        print(f"Development Years: 0-{df_rra['Development_Year'].max()}")
    except Exception as e:
        print(f"RRA test failed: {e}")

    print("\n" + "="*70)
    print("Testing with RRQ data...")
    print("="*70)

    try:
        processor_rrq = UnifiedFormProcessor('../../synthetic_data_rrq_2024_q2/rrq_193_net_claims.csv')
        df_rrq = processor_rrq.process_form_193()
        print(f"Processed RRQ Form 193: {len(df_rrq)} records")
        print(f"Return Type: {df_rrq['Data_Scope'].iloc[0]}")
        print(f"Quarter: {df_rrq['Quarterly_Period'].iloc[0]}")
        print(f"Years of Account: {sorted(df_rrq['Year_of_Account'].unique())}")
        print(f"Development Years: 0-{df_rrq['Development_Year'].max()}")

        # Show data reduction
        print("\n" + "="*70)
        print("RRQ vs RRA Data Comparison:")
        print("="*70)
        print(f"RRA records: {len(df_rra)}")
        print(f"RRQ records: {len(df_rrq)}")
        print(f"Reduction: {(1 - len(df_rrq)/len(df_rra))*100:.1f}%")
    except Exception as e:
        print(f"RRQ test failed: {e}")

    # Test quarter comparison
    print("\n" + "="*70)
    print("Testing Quarter Comparison (Q1 vs Q2)...")
    print("="*70)

    try:
        processor = UnifiedFormProcessor('.')
        comparison = processor.compare_quarters(
            current_data='../../synthetic_data_rrq_2024_q2/rrq_193_net_claims.csv',
            prior_data='../../synthetic_data_rrq_2024_q1/rrq_193_net_claims.csv',
            form='193'
        )
        print(f"Comparison records: {len(comparison)}")
        print(f"Significant movements: {comparison['Significant_Movement'].sum()}")
        print(f"New in current quarter: {(comparison['_merge'] == 'left_only').sum()}")
        print(f"Removed from prior quarter: {(comparison['_merge'] == 'right_only').sum()}")
    except Exception as e:
        print(f"Comparison test failed: {e}")
