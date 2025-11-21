"""
RRA Premium Processing Script for Power BI
Solvency II Pillar 3 - Risk and Claim Reporting
Reserve Return Annual (RRA) Forms Generator

This script processes Lloyd's premium data and generates output tables
required by the RRA - Reserve Return Annual forms.

Compatible with Power BI Python visual and data transformations.
"""

import pandas as pd
import numpy as np
from datetime import datetime

class RRAPremiumProcessor:
    """
    Process premium data for RRA reporting requirements
    """

    def __init__(self, premium_data):
        """
        Initialize processor with premium data

        Parameters:
        -----------
        premium_data : pandas.DataFrame
            DataFrame containing premium data with required columns
        """
        self.premium_data = premium_data
        self.required_columns = [
            'Syndicate Number', 'UMR', 'Insured Country', 'Risk Location',
            'Insured Name', 'Insured - Policyholder Type', 'Risk Code',
            'Risk / Certificate Reference', 'Original Currency', 'Sum Insured',
            'Gross Annual Premium in Period', 'YOA', 'Part VII Indicator'
        ]
        self._validate_data()

    def _validate_data(self):
        """Validate that required columns exist in the data"""
        missing_cols = [col for col in self.required_columns if col not in self.premium_data.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

    def create_premium_summary_by_syndicate(self):
        """
        Create premium summary aggregated by syndicate

        Returns:
        --------
        pandas.DataFrame : Premium summary by syndicate
        """
        summary = self.premium_data.groupby(['Syndicate Number', 'YOA']).agg({
            'Gross Annual Premium in Period': ['sum', 'mean', 'count'],
            'Sum Insured': 'sum',
            'UMR': 'nunique'
        }).reset_index()

        summary.columns = [
            'Syndicate Number', 'YOA',
            'Total Premium', 'Average Premium', 'Number of Risks',
            'Total Sum Insured', 'Unique UMRs'
        ]

        summary = summary.round(2)
        return summary

    def create_premium_by_risk_code(self):
        """
        Create premium analysis by risk code

        Returns:
        --------
        pandas.DataFrame : Premium breakdown by risk code
        """
        risk_summary = self.premium_data.groupby(['Risk Code', 'YOA', 'Syndicate Number']).agg({
            'Gross Annual Premium in Period': 'sum',
            'Sum Insured': 'sum',
            'UMR': 'count'
        }).reset_index()

        risk_summary.columns = [
            'Risk Code', 'YOA', 'Syndicate Number',
            'Total Premium', 'Total Sum Insured', 'Number of Policies'
        ]

        risk_summary = risk_summary.round(2)
        return risk_summary

    def create_geographic_analysis(self):
        """
        Create geographic analysis of premiums

        Returns:
        --------
        pandas.DataFrame : Premium analysis by country
        """
        geo_summary = self.premium_data.groupby(['Insured Country', 'YOA']).agg({
            'Gross Annual Premium in Period': 'sum',
            'Sum Insured': 'sum',
            'Syndicate Number': 'nunique',
            'UMR': 'count'
        }).reset_index()

        geo_summary.columns = [
            'Country', 'YOA',
            'Total Premium', 'Total Sum Insured',
            'Number of Syndicates', 'Number of Policies'
        ]

        # Calculate market share percentage
        total_by_year = geo_summary.groupby('YOA')['Total Premium'].transform('sum')
        geo_summary['Premium Share %'] = (geo_summary['Total Premium'] / total_by_year * 100).round(2)

        geo_summary = geo_summary.round(2)
        return geo_summary

    def create_policyholder_type_analysis(self):
        """
        Create analysis by policyholder type (Retail vs Business)

        Returns:
        --------
        pandas.DataFrame : Premium analysis by policyholder type
        """
        type_summary = self.premium_data.groupby([
            'Insured - Policyholder Type', 'YOA', 'Syndicate Number'
        ]).agg({
            'Gross Annual Premium in Period': ['sum', 'mean'],
            'Sum Insured': 'sum',
            'UMR': 'count'
        }).reset_index()

        type_summary.columns = [
            'Policyholder Type', 'YOA', 'Syndicate Number',
            'Total Premium', 'Average Premium', 'Total Sum Insured', 'Number of Policies'
        ]

        type_summary = type_summary.round(2)
        return type_summary

    def create_currency_analysis(self):
        """
        Create currency breakdown analysis

        Returns:
        --------
        pandas.DataFrame : Premium analysis by currency
        """
        currency_summary = self.premium_data.groupby(['Original Currency', 'YOA']).agg({
            'Gross Annual Premium in Period': 'sum',
            'Sum Insured': 'sum',
            'UMR': 'count'
        }).reset_index()

        currency_summary.columns = [
            'Currency', 'YOA',
            'Total Premium', 'Total Sum Insured', 'Number of Policies'
        ]

        # Calculate currency distribution percentage
        total_by_year = currency_summary.groupby('YOA')['Number of Policies'].transform('sum')
        currency_summary['Policy Share %'] = (currency_summary['Number of Policies'] / total_by_year * 100).round(2)

        currency_summary = currency_summary.round(2)
        return currency_summary

    def create_part_vii_analysis(self):
        """
        Create Part VII indicator analysis

        Returns:
        --------
        pandas.DataFrame : Analysis of Part VII transfers
        """
        part_vii_summary = self.premium_data.groupby(['Part VII Indicator', 'YOA', 'Syndicate Number']).agg({
            'Gross Annual Premium in Period': 'sum',
            'Sum Insured': 'sum',
            'UMR': 'count'
        }).reset_index()

        part_vii_summary.columns = [
            'Part VII Indicator', 'YOA', 'Syndicate Number',
            'Total Premium', 'Total Sum Insured', 'Number of Policies'
        ]

        part_vii_summary = part_vii_summary.round(2)
        return part_vii_summary

    def create_detailed_risk_register(self):
        """
        Create detailed risk register for RRA reporting

        Returns:
        --------
        pandas.DataFrame : Detailed risk-level data
        """
        risk_register = self.premium_data.copy()

        # Add calculated fields
        risk_register['Premium to Sum Insured Ratio'] = (
            risk_register['Gross Annual Premium in Period'] / risk_register['Sum Insured'] * 100
        ).round(2)

        # Add risk classification based on premium size
        def classify_risk_size(premium):
            if premium < 50000:
                return 'Small'
            elif premium < 500000:
                return 'Medium'
            elif premium < 2000000:
                return 'Large'
            else:
                return 'Very Large'

        risk_register['Risk Size Classification'] = risk_register['Gross Annual Premium in Period'].apply(classify_risk_size)

        return risk_register

    def generate_all_outputs(self):
        """
        Generate all RRA output tables

        Returns:
        --------
        dict : Dictionary containing all output DataFrames
        """
        outputs = {
            'Premium_Summary_By_Syndicate': self.create_premium_summary_by_syndicate(),
            'Premium_By_Risk_Code': self.create_premium_by_risk_code(),
            'Geographic_Analysis': self.create_geographic_analysis(),
            'Policyholder_Type_Analysis': self.create_policyholder_type_analysis(),
            'Currency_Analysis': self.create_currency_analysis(),
            'Part_VII_Analysis': self.create_part_vii_analysis(),
            'Detailed_Risk_Register': self.create_detailed_risk_register()
        }

        return outputs

    def export_to_excel(self, output_path='rra_premium_output.xlsx'):
        """
        Export all outputs to Excel file with multiple sheets

        Parameters:
        -----------
        output_path : str
            Path to output Excel file
        """
        outputs = self.generate_all_outputs()

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for sheet_name, df in outputs.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"RRA outputs exported to {output_path}")


def process_premium_data_for_powerbi(dataset):
    """
    Main function for Power BI integration

    This function is designed to be called from Power BI Python visual or script.

    Parameters:
    -----------
    dataset : pandas.DataFrame
        Input dataset from Power BI

    Returns:
    --------
    pandas.DataFrame : Processed output for visualization
    """
    processor = RRAPremiumProcessor(dataset)

    # For Power BI, typically return a single DataFrame for visualization
    # You can modify this to return different outputs based on requirements
    return processor.create_premium_summary_by_syndicate()


# Example usage for standalone execution
if __name__ == "__main__":
    # Load synthetic data
    print("Loading premium data...")
    premium_data = pd.read_csv('../synthetic_data/synthetic_lloyds_premium_data.csv')

    print(f"Loaded {len(premium_data)} premium records")

    # Process data
    print("\nProcessing RRA outputs...")
    processor = RRAPremiumProcessor(premium_data)

    # Generate all outputs
    outputs = processor.generate_all_outputs()

    # Display summary of each output
    print("\n" + "="*80)
    print("RRA OUTPUT TABLES GENERATED")
    print("="*80)

    for name, df in outputs.items():
        print(f"\n{name}:")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {list(df.columns)}")
        print(f"\n  Preview:")
        print(df.head(5).to_string())
        print("-"*80)

    # Export to Excel
    output_file = '../synthetic_data/rra_premium_outputs.xlsx'
    processor.export_to_excel(output_file)
    print(f"\n✓ All outputs exported to {output_file}")

    # For Power BI demonstration
    print("\n" + "="*80)
    print("POWER BI INTEGRATION EXAMPLE")
    print("="*80)
    print("\nTo use in Power BI, import this module and call:")
    print("  result = process_premium_data_for_powerbi(dataset)")
    print("\nOr create custom visualizations using individual methods:")
    print("  processor = RRAPremiumProcessor(dataset)")
    print("  geographic_data = processor.create_geographic_analysis()")
