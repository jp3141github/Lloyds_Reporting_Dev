"""
Lloyd's Liquidity Stress Test - Python Implementation for Power BI
Processes Lloyd's syndicate data to generate RRA (Reserve Return Annual) form outputs
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

class LiquidityStressTest:
    """
    Main class for processing Lloyd's Liquidity Stress Test data
    Compatible with Power BI Python visual
    """

    def __init__(self, data_path='../data'):
        """
        Initialize with path to data directory

        Args:
            data_path (str): Path to directory containing syndicate data
        """
        self.data_path = data_path
        self.syndicates = []
        self.metadata = None
        self.assets_data = None
        self.cashflow_data = None
        self.stress_data = None

    def load_data(self, syndicate_number=None):
        """
        Load data for analysis

        Args:
            syndicate_number (int, optional): Specific syndicate to load.
                                             If None, loads all syndicates.

        Returns:
            dict: Loaded data dictionary
        """
        if syndicate_number:
            # Load individual syndicate
            syndicate_path = os.path.join(self.data_path, f'syndicate_{syndicate_number}')

            with open(os.path.join(syndicate_path, 'metadata.json'), 'r') as f:
                metadata = json.load(f)

            assets = pd.read_csv(os.path.join(syndicate_path, 'assets_liquidity.csv'))
            cashflow = pd.read_csv(os.path.join(syndicate_path, 'cashflow.csv'))
            stress = pd.read_csv(os.path.join(syndicate_path, 'stress_scenario.csv'))

            return {
                'metadata': metadata,
                'assets': assets,
                'cashflow': cashflow,
                'stress': stress
            }
        else:
            # Load all syndicates combined
            self.metadata = pd.read_csv(os.path.join(self.data_path, 'all_syndicates_metadata.csv'))
            self.assets_data = pd.read_csv(os.path.join(self.data_path, 'all_syndicates_assets.csv'))
            self.cashflow_data = pd.read_csv(os.path.join(self.data_path, 'all_syndicates_cashflow.csv'))
            self.stress_data = pd.read_csv(os.path.join(self.data_path, 'all_syndicates_stress.csv'))

            return {
                'metadata': self.metadata,
                'assets': self.assets_data,
                'cashflow': self.cashflow_data,
                'stress': self.stress_data
            }

    def calculate_capital_position_table(self, syndicate_number=None):
        """
        Generate Capital Position summary table for RRA forms

        Args:
            syndicate_number (int, optional): Filter for specific syndicate

        Returns:
            pd.DataFrame: Capital position table
        """
        if self.metadata is None:
            self.load_data()

        df = self.metadata.copy()

        if syndicate_number:
            df = df[df['syndicate_number'] == syndicate_number]

        # Select relevant columns
        capital_position = df[[
            'syndicate_number',
            'syndicate_name',
            'managing_agent',
            'qma_date',
            'syndicate_fal',
            'syndicate_fis',
            'syndicate_uscr',
            'syndicate_ueca'
        ]].copy()

        # Calculate key ratios
        capital_position['solvency_ratio'] = (
            capital_position['syndicate_fal'] / capital_position['syndicate_uscr']
        ).round(2)

        capital_position['eca_coverage'] = (
            capital_position['syndicate_fal'] / capital_position['syndicate_ueca']
        ).round(2)

        # Format currency columns
        currency_cols = ['syndicate_fal', 'syndicate_fis', 'syndicate_uscr', 'syndicate_ueca']
        for col in currency_cols:
            capital_position[f'{col}_formatted'] = capital_position[col].apply(
                lambda x: f'£{x:,.0f}'
            )

        return capital_position

    def calculate_liquidity_breakdown_table(self, syndicate_number=None, date=None):
        """
        Generate Asset & Liquidity Breakdown table for RRA forms

        Args:
            syndicate_number (int, optional): Filter for specific syndicate
            date (str, optional): Filter for specific date (YYYY-MM-DD)

        Returns:
            pd.DataFrame: Liquidity breakdown table
        """
        if self.assets_data is None:
            self.load_data()

        df = self.assets_data.copy()

        if syndicate_number:
            df = df[df['syndicate_number'] == syndicate_number]

        if date:
            df = df[df['date'] == date]

        # Calculate totals and percentages
        df['total_assets'] = (
            df['restricted_assets_total'] +
            df['illiquid_assets_total'] +
            df['liquid_assets_total']
        )

        df['restricted_pct'] = (df['restricted_assets_total'] / df['total_assets'] * 100).round(2)
        df['illiquid_pct'] = (df['illiquid_assets_total'] / df['total_assets'] * 100).round(2)
        df['liquid_pct'] = (df['liquid_assets_total'] / df['total_assets'] * 100).round(2)

        return df

    def calculate_cashflow_summary_table(self, syndicate_number=None):
        """
        Generate Cashflow Summary table for RRA forms

        Args:
            syndicate_number (int, optional): Filter for specific syndicate

        Returns:
            pd.DataFrame: Cashflow summary table
        """
        if self.cashflow_data is None:
            self.load_data()

        df = self.cashflow_data.copy()

        if syndicate_number:
            df = df[df['syndicate_number'] == syndicate_number]

        # Add cumulative columns
        for syndicate in df['syndicate_number'].unique():
            mask = df['syndicate_number'] == syndicate

            df.loc[mask, 'cumulative_premium_income'] = df.loc[mask, 'premium_income'].cumsum()
            df.loc[mask, 'cumulative_claims_paid'] = df.loc[mask, 'claims_paid'].cumsum()
            df.loc[mask, 'cumulative_total_movements'] = df.loc[mask, 'total_movements'].cumsum()

        return df

    def calculate_stress_impact_table(self, syndicate_number=None):
        """
        Generate Stress Test Impact table for RRA forms

        Args:
            syndicate_number (int, optional): Filter for specific syndicate

        Returns:
            pd.DataFrame: Stress impact table with baseline vs stressed scenarios
        """
        if self.cashflow_data is None or self.stress_data is None:
            self.load_data()

        # Merge baseline cashflow with stress scenario
        baseline = self.cashflow_data.copy()
        stress = self.stress_data.copy()

        merged = baseline.merge(
            stress,
            on=['syndicate_number', 'date'],
            how='left'
        )

        if syndicate_number:
            merged = merged[merged['syndicate_number'] == syndicate_number]

        # Calculate stressed cashflow positions
        merged['stressed_closing_funds'] = (
            merged['closing_free_funds'] + merged['stress_scenario_impact']
        )

        merged['liquidity_gap'] = merged['closing_free_funds'] - merged['stressed_closing_funds']

        # Calculate minimum liquidity position
        for syndicate in merged['syndicate_number'].unique():
            mask = merged['syndicate_number'] == syndicate
            merged.loc[mask, 'min_liquidity_baseline'] = merged.loc[mask, 'closing_free_funds'].min()
            merged.loc[mask, 'min_liquidity_stressed'] = merged.loc[mask, 'stressed_closing_funds'].min()

        return merged

    def calculate_rra_output_tables(self, syndicate_number=None):
        """
        Generate all RRA output tables

        Args:
            syndicate_number (int, optional): Filter for specific syndicate

        Returns:
            dict: Dictionary containing all output tables
        """
        return {
            'capital_position': self.calculate_capital_position_table(syndicate_number),
            'liquidity_breakdown': self.calculate_liquidity_breakdown_table(syndicate_number),
            'cashflow_summary': self.calculate_cashflow_summary_table(syndicate_number),
            'stress_impact': self.calculate_stress_impact_table(syndicate_number)
        }

    def create_dashboard_summary(self, syndicate_number=None):
        """
        Create executive dashboard summary with key metrics

        Args:
            syndicate_number (int, optional): Filter for specific syndicate

        Returns:
            pd.DataFrame: Dashboard summary metrics
        """
        if self.metadata is None:
            self.load_data()

        capital = self.calculate_capital_position_table(syndicate_number)
        stress = self.calculate_stress_impact_table(syndicate_number)

        summary_data = []

        for _, synd_capital in capital.iterrows():
            synd_num = synd_capital['syndicate_number']

            synd_stress = stress[stress['syndicate_number'] == synd_num]

            # Get stress scenario metadata
            synd_meta = self.metadata[self.metadata['syndicate_number'] == synd_num].iloc[0]

            summary = {
                'syndicate_number': synd_num,
                'syndicate_name': synd_capital['syndicate_name'],
                'managing_agent': synd_capital['managing_agent'],
                'total_fal': synd_capital['syndicate_fal'],
                'solvency_ratio': synd_capital['solvency_ratio'],
                'baseline_min_liquidity': synd_stress['min_liquidity_baseline'].iloc[0],
                'stressed_min_liquidity': synd_stress['min_liquidity_stressed'].iloc[0],
                'max_liquidity_gap': synd_stress['liquidity_gap'].max(),
                'stress_scenario': synd_meta['scenario_type'],
                'gross_loss_estimate': synd_meta['gross_loss_estimate'],
                'net_loss_estimate': synd_meta['net_loss_estimate'],
                'us_funding_requirement': synd_meta['us_funding_requirement'],
                'stress_test_pass': synd_stress['stressed_closing_funds'].min() > 0
            }

            summary_data.append(summary)

        return pd.DataFrame(summary_data)

    def export_to_excel(self, output_path, syndicate_number=None):
        """
        Export all tables to Excel workbook for easy viewing

        Args:
            output_path (str): Path for output Excel file
            syndicate_number (int, optional): Filter for specific syndicate
        """
        tables = self.calculate_rra_output_tables(syndicate_number)
        summary = self.create_dashboard_summary(syndicate_number)

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            summary.to_excel(writer, sheet_name='Dashboard Summary', index=False)
            tables['capital_position'].to_excel(writer, sheet_name='Capital Position', index=False)
            tables['liquidity_breakdown'].to_excel(writer, sheet_name='Liquidity Breakdown', index=False)
            tables['cashflow_summary'].to_excel(writer, sheet_name='Cashflow Summary', index=False)
            tables['stress_impact'].to_excel(writer, sheet_name='Stress Impact Analysis', index=False)

        print(f"✓ Exported to {output_path}")


# Power BI Integration Functions
# These functions can be called directly from Power BI Python visuals

def get_capital_position(dataset):
    """
    Power BI wrapper for capital position table

    Args:
        dataset (pd.DataFrame): Input dataset from Power BI

    Returns:
        pd.DataFrame: Processed capital position table
    """
    lst = LiquidityStressTest()
    lst.metadata = dataset
    return lst.calculate_capital_position_table()


def get_liquidity_breakdown(dataset):
    """
    Power BI wrapper for liquidity breakdown table

    Args:
        dataset (pd.DataFrame): Input dataset from Power BI

    Returns:
        pd.DataFrame: Processed liquidity breakdown table
    """
    lst = LiquidityStressTest()
    lst.assets_data = dataset
    return lst.calculate_liquidity_breakdown_table()


def get_stress_impact(cashflow_dataset, stress_dataset):
    """
    Power BI wrapper for stress impact analysis

    Args:
        cashflow_dataset (pd.DataFrame): Cashflow data from Power BI
        stress_dataset (pd.DataFrame): Stress scenario data from Power BI

    Returns:
        pd.DataFrame: Processed stress impact table
    """
    lst = LiquidityStressTest()
    lst.cashflow_data = cashflow_dataset
    lst.stress_data = stress_dataset
    return lst.calculate_stress_impact_table()


# Example usage and testing
if __name__ == "__main__":
    print("Lloyd's Liquidity Stress Test - Python Implementation")
    print("=" * 80)

    # Initialize
    lst = LiquidityStressTest('data')

    # Load all data
    print("\nLoading data...")
    lst.load_data()
    print(f"✓ Loaded data for {len(lst.metadata)} syndicates")

    # Generate dashboard summary
    print("\nGenerating dashboard summary...")
    summary = lst.create_dashboard_summary()
    print(summary.to_string())

    # Export all tables for syndicate 2001
    print("\n" + "=" * 80)
    print("Exporting detailed analysis for Syndicate 2001...")
    lst.export_to_excel('python_implementation/syndicate_2001_analysis.xlsx', syndicate_number=2001)

    # Export combined analysis for all syndicates
    print("\nExporting combined analysis for all syndicates...")
    lst.export_to_excel('python_implementation/all_syndicates_analysis.xlsx')

    print("\n" + "=" * 80)
    print("Processing complete!")
