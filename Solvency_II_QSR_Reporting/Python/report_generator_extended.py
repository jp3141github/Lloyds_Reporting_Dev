"""
Extended Report Generator for Power BI
Generates Solvency II reports for:
- QSR (Quarterly Solvency Return)
- AAD (Annual Actuarial Data)
- ASB (Annual Solvency Balance Sheet)

This script can be imported and used within Power BI to transform
Lloyd's syndicate data into standardized reporting formats.
"""

import pandas as pd
import numpy as np
from datetime import datetime


class SolvencyReportGenerator:
    """
    Unified generator for Solvency II QSR, AAD, and ASB reports
    """

    def __init__(self, data_dir='../Data/'):
        """Initialize with data directory"""
        self.data_dir = data_dir
        self.qsr_data = {}
        self.aad_data = {}
        self.asb_data = {}

    def load_all_data(self):
        """Load all synthetic data files"""
        # QSR datasets
        qsr_datasets = [
            'balance_sheet', 'own_funds', 'technical_provisions',
            'premiums_claims', 'investments', 'scr_calculation', 'mcr_calculation'
        ]

        # AAD datasets
        aad_datasets = [
            'aad230_open_market_value', 'aad233_off_balance_sheet',
            'aad235_derivatives', 'aad236_collective_investments',
            'aad237_structured_products', 'aad238_securities_lending'
        ]

        # ASB datasets
        asb_datasets = ['asb_claims_triangles']

        # Load QSR data
        for dataset in qsr_datasets:
            try:
                filepath = f'{self.data_dir}synthetic_{dataset}.csv'
                self.qsr_data[dataset] = pd.read_csv(filepath)
                print(f'Loaded QSR {dataset}: {len(self.qsr_data[dataset])} rows')
            except FileNotFoundError:
                print(f'Warning: QSR {dataset} file not found')
                self.qsr_data[dataset] = pd.DataFrame()

        # Load AAD data
        for dataset in aad_datasets:
            try:
                filepath = f'{self.data_dir}synthetic_{dataset}.csv'
                self.aad_data[dataset] = pd.read_csv(filepath)
                print(f'Loaded AAD {dataset}: {len(self.aad_data[dataset])} rows')
            except FileNotFoundError:
                print(f'Warning: AAD {dataset} file not found')
                self.aad_data[dataset] = pd.DataFrame()

        # Load ASB data
        for dataset in asb_datasets:
            try:
                filepath = f'{self.data_dir}synthetic_{dataset}.csv'
                self.asb_data[dataset] = pd.read_csv(filepath)
                print(f'Loaded ASB {dataset}: {len(self.asb_data[dataset])} rows')
            except FileNotFoundError:
                print(f'Warning: ASB {dataset} file not found')
                self.asb_data[dataset] = pd.DataFrame()

    # ========================================================================
    # QSR REPORT GENERATION (from original generator)
    # ========================================================================

    def generate_qsr002_balance_sheet(self):
        """Generate QSR 002 - Overall Balance Sheet (S.02.01.02)"""
        if 'balance_sheet' not in self.qsr_data or self.qsr_data['balance_sheet'].empty:
            return pd.DataFrame()

        df = self.qsr_data['balance_sheet'].copy()

        # Format according to QSR 002 specification
        qsr002 = pd.DataFrame()
        qsr002['Syndicate'] = df['Syndicate']
        qsr002['Reporting_Date'] = df['Reporting_Date']

        # Assets
        qsr002['R0010_Goodwill'] = df['Goodwill']
        qsr002['R0020_Deferred_Acquisition_Costs'] = df['Deferred_Acquisition_Costs']
        qsr002['R0030_Intangible_Assets'] = df['Intangible_Assets']
        qsr002['R0040_Deferred_Tax_Assets'] = df['Deferred_Tax_Assets']
        qsr002['R0050_Pension_Benefit_Surplus'] = df['Pension_Benefit_Surplus']
        qsr002['R0060_Property_Plant_Equipment'] = df['Property_Plant_Equipment']
        qsr002['R0070_Investments'] = df['Investments']
        qsr002['R0220_Total_Assets'] = df['Total_Assets']

        # Liabilities
        qsr002['R0230_Technical_Provisions_NonLife'] = df['Technical_Provisions_NonLife']
        qsr002['R0350_Total_Liabilities'] = df['Total_Liabilities']
        qsr002['R0360_Excess_Assets_Over_Liabilities'] = df['Excess_Assets_Over_Liabilities']

        return qsr002

    def generate_qsr220_own_funds(self):
        """Generate QSR 220 - Own Funds (S.23.01.01)"""
        if 'own_funds' not in self.qsr_data or self.qsr_data['own_funds'].empty:
            return pd.DataFrame()

        df = self.qsr_data['own_funds'].copy()

        qsr220 = pd.DataFrame()
        qsr220['Syndicate'] = df['Syndicate']
        qsr220['Reporting_Date'] = df['Reporting_Date']
        qsr220['R0120_Total_Own_Funds'] = df['Total_Own_Funds']
        qsr220['R0130_Eligible_Own_Funds_SCR'] = df['Eligible_Own_Funds_SCR']
        qsr220['R0140_Eligible_Own_Funds_MCR'] = df['Eligible_Own_Funds_MCR']

        return qsr220

    # ========================================================================
    # AAD REPORT GENERATION
    # ========================================================================

    def generate_aad230_open_market_value_report(self):
        """
        Generate AAD 230 - Open Market Value Report (S.06.02.01)
        Aggregated and detailed views
        """
        if 'aad230_open_market_value' not in self.aad_data or self.aad_data['aad230_open_market_value'].empty:
            return pd.DataFrame()

        df = self.aad_data['aad230_open_market_value'].copy()

        # Detailed view (security level)
        aad230_detailed = df[['Syndicate', 'Reporting_Date', 'Asset_ID', 'Instrument_Type',
                             'Asset_Category', 'Issuer_Name', 'Issuer_Country', 'Currency',
                             'Total_Solvency_II_Value', 'Book_Value', 'Credit_Rating']].copy()

        return aad230_detailed

    def generate_aad230_summary_by_category(self):
        """AAD 230 Summary by Asset Category"""
        if 'aad230_open_market_value' not in self.aad_data or self.aad_data['aad230_open_market_value'].empty:
            return pd.DataFrame()

        df = self.aad_data['aad230_open_market_value'].copy()

        # Aggregate by syndicate and asset category
        summary = df.groupby(['Syndicate', 'Reporting_Date', 'Asset_Category']).agg({
            'Total_Solvency_II_Value': 'sum',
            'Book_Value': 'sum',
            'Asset_ID': 'count'
        }).reset_index()

        summary.rename(columns={'Asset_ID': 'Number_Of_Holdings'}, inplace=True)
        summary['Unrealized_Gain_Loss'] = summary['Total_Solvency_II_Value'] - summary['Book_Value']

        return summary

    def generate_aad233_off_balance_sheet_report(self):
        """Generate AAD 233 - Off-Balance Sheet Items Report (S.08.01.01)"""
        if 'aad233_off_balance_sheet' not in self.aad_data or self.aad_data['aad233_off_balance_sheet'].empty:
            return pd.DataFrame()

        df = self.aad_data['aad233_off_balance_sheet'].copy()

        aad233 = df[['Syndicate', 'Reporting_Date', 'Item_ID', 'Item_Type',
                     'Counterparty', 'Maximum_Exposure', 'Probability_Of_Call',
                     'Expected_Value', 'Maturity_Date']].copy()

        return aad233

    def generate_aad235_derivatives_report(self):
        """Generate AAD 235 - Derivatives Report (S.09.01.01)"""
        if 'aad235_derivatives' not in self.aad_data or self.aad_data['aad235_derivatives'].empty:
            return pd.DataFrame()

        df = self.aad_data['aad235_derivatives'].copy()

        aad235 = df[['Syndicate', 'Reporting_Date', 'Contract_ID', 'Derivative_Type',
                     'Underlying_Asset', 'Notional_Amount', 'Fair_Value_Asset',
                     'Fair_Value_Liability', 'Delta', 'Purpose', 'Maturity_Date']].copy()

        return aad235

    def generate_aad235_derivatives_summary(self):
        """AAD 235 Derivatives Risk Summary"""
        if 'aad235_derivatives' not in self.aad_data or self.aad_data['aad235_derivatives'].empty:
            return pd.DataFrame()

        df = self.aad_data['aad235_derivatives'].copy()

        # Aggregate by syndicate and derivative type
        summary = df.groupby(['Syndicate', 'Reporting_Date', 'Derivative_Type']).agg({
            'Notional_Amount': 'sum',
            'Fair_Value_Asset': 'sum',
            'Fair_Value_Liability': 'sum',
            'Delta': 'sum',
            'Contract_ID': 'count'
        }).reset_index()

        summary.rename(columns={'Contract_ID': 'Number_Of_Contracts'}, inplace=True)
        summary['Net_Fair_Value'] = summary['Fair_Value_Asset'] - summary['Fair_Value_Liability']

        return summary

    def generate_aad236_collective_investments_report(self):
        """Generate AAD 236 - Collective Investments Report (S.06.03.01)"""
        if 'aad236_collective_investments' not in self.aad_data or self.aad_data['aad236_collective_investments'].empty:
            return pd.DataFrame()

        df = self.aad_data['aad236_collective_investments'].copy()

        aad236 = df[['Syndicate', 'Reporting_Date', 'Fund_ID', 'Fund_Name', 'Fund_Type',
                     'Fund_Manager', 'Total_Value', 'Look_Through_Available',
                     'Underlying_Equities_Pct', 'Underlying_Bonds_Pct']].copy()

        return aad236

    def generate_aad237_structured_products_report(self):
        """Generate AAD 237 - Structured Products Report (S.10.01.01)"""
        if 'aad237_structured_products' not in self.aad_data or self.aad_data['aad237_structured_products'].empty:
            return pd.DataFrame()

        df = self.aad_data['aad237_structured_products'].copy()

        aad237 = df[['Syndicate', 'Reporting_Date', 'Product_ID', 'Product_Name',
                     'Product_Type', 'Issuer', 'Notional_Amount', 'Solvency_II_Value',
                     'Capital_Protection', 'Maturity_Date']].copy()

        return aad237

    def generate_aad238_securities_lending_report(self):
        """Generate AAD 238 - Securities Lending Report (S.11.01.01)"""
        if 'aad238_securities_lending' not in self.aad_data or self.aad_data['aad238_securities_lending'].empty:
            return pd.DataFrame()

        df = self.aad_data['aad238_securities_lending'].copy()

        aad238 = df[['Syndicate', 'Reporting_Date', 'Transaction_ID', 'Transaction_Type',
                     'Security_Type', 'Security_Value', 'Collateral_Received',
                     'Collateral_Type', 'Fee_Rate', 'Income_Generated']].copy()

        return aad238

    # ========================================================================
    # ASB REPORT GENERATION
    # ========================================================================

    def generate_asb245_claims_gross(self):
        """Generate ASB 245 - Claims Information Gross (S.19.01.01)"""
        if 'asb_claims_triangles' not in self.asb_data or self.asb_data['asb_claims_triangles'].empty:
            return pd.DataFrame()

        df = self.asb_data['asb_claims_triangles'].copy()

        asb245 = df[['Syndicate', 'Reporting_Date', 'Line_of_Business',
                     'Accident_Year', 'Development_Year',
                     'Gross_Claims_Reported', 'Gross_Claims_Paid',
                     'Gross_Claims_Outstanding', 'Gross_Ultimate_Estimate']].copy()

        return asb245

    def generate_asb246_claims_reinsurance(self):
        """Generate ASB 246 - Claims Information Reinsurance Share (S.19.01.01)"""
        if 'asb_claims_triangles' not in self.asb_data or self.asb_data['asb_claims_triangles'].empty:
            return pd.DataFrame()

        df = self.asb_data['asb_claims_triangles'].copy()

        asb246 = df[['Syndicate', 'Reporting_Date', 'Line_of_Business',
                     'Accident_Year', 'Development_Year',
                     'Reins_Claims_Reported', 'Reins_Claims_Paid',
                     'Reins_Claims_Outstanding']].copy()

        return asb246

    def generate_asb247_claims_net(self):
        """Generate ASB 247 - Claims Information Net (S.19.01.01)"""
        if 'asb_claims_triangles' not in self.asb_data or self.asb_data['asb_claims_triangles'].empty:
            return pd.DataFrame()

        df = self.asb_data['asb_claims_triangles'].copy()

        asb247 = df[['Syndicate', 'Reporting_Date', 'Line_of_Business',
                     'Accident_Year', 'Development_Year',
                     'Net_Claims_Reported', 'Net_Claims_Paid',
                     'Net_Claims_Outstanding', 'Net_Ultimate_Estimate']].copy()

        return asb247

    def generate_asb_claims_summary(self):
        """Generate ASB Claims Summary by Syndicate and Line of Business"""
        if 'asb_claims_triangles' not in self.asb_data or self.asb_data['asb_claims_triangles'].empty:
            return pd.DataFrame()

        df = self.asb_data['asb_claims_triangles'].copy()

        # Get latest development year for each accident year
        latest_dev = df.groupby(['Syndicate', 'Line_of_Business', 'Accident_Year'])['Development_Year'].max().reset_index()
        latest_dev.rename(columns={'Development_Year': 'Latest_Dev_Year'}, inplace=True)

        # Merge to get latest values only
        df_latest = df.merge(latest_dev, on=['Syndicate', 'Line_of_Business', 'Accident_Year'])
        df_latest = df_latest[df_latest['Development_Year'] == df_latest['Latest_Dev_Year']]

        # Aggregate
        summary = df_latest.groupby(['Syndicate', 'Reporting_Date', 'Line_of_Business']).agg({
            'Gross_Claims_Outstanding': 'sum',
            'Net_Claims_Outstanding': 'sum',
            'Gross_Claims_Paid': 'sum',
            'Net_Claims_Paid': 'sum'
        }).reset_index()

        return summary

    def generate_claims_development_factors(self):
        """Calculate claims development factors from triangles"""
        if 'asb_claims_triangles' not in self.asb_data or self.asb_data['asb_claims_triangles'].empty:
            return pd.DataFrame()

        df = self.asb_data['asb_claims_triangles'].copy()

        # Sort by accident year and development year
        df = df.sort_values(['Syndicate', 'Line_of_Business', 'Accident_Year', 'Development_Year'])

        # Calculate age-to-age factors
        df['Next_Reported'] = df.groupby(['Syndicate', 'Line_of_Business', 'Accident_Year'])['Gross_Claims_Reported'].shift(-1)
        df['Age_To_Age_Factor'] = df['Next_Reported'] / df['Gross_Claims_Reported']

        # Calculate average development factors by development period
        dev_factors = df[df['Age_To_Age_Factor'].notna()].groupby(['Syndicate', 'Line_of_Business', 'Development_Year']).agg({
            'Age_To_Age_Factor': ['mean', 'median', 'std']
        }).reset_index()

        dev_factors.columns = ['Syndicate', 'Line_of_Business', 'Development_Year',
                              'Avg_Dev_Factor', 'Median_Dev_Factor', 'Std_Dev_Factor']

        return dev_factors

    # ========================================================================
    # MASTER REPORT GENERATION
    # ========================================================================

    def generate_all_qsr_reports(self):
        """Generate all QSR reports"""
        from qsr_report_generator import QSRReportGenerator
        qsr_gen = QSRReportGenerator(data_dir=self.data_dir)
        qsr_gen.load_data()
        return qsr_gen.generate_all_reports()

    def generate_all_aad_reports(self):
        """Generate all AAD reports"""
        reports = {
            'AAD230_Open_Market_Value': self.generate_aad230_open_market_value_report(),
            'AAD230_Summary_By_Category': self.generate_aad230_summary_by_category(),
            'AAD233_Off_Balance_Sheet': self.generate_aad233_off_balance_sheet_report(),
            'AAD235_Derivatives': self.generate_aad235_derivatives_report(),
            'AAD235_Derivatives_Summary': self.generate_aad235_derivatives_summary(),
            'AAD236_Collective_Investments': self.generate_aad236_collective_investments_report(),
            'AAD237_Structured_Products': self.generate_aad237_structured_products_report(),
            'AAD238_Securities_Lending': self.generate_aad238_securities_lending_report(),
        }
        return reports

    def generate_all_asb_reports(self):
        """Generate all ASB reports"""
        reports = {
            'ASB245_Claims_Gross': self.generate_asb245_claims_gross(),
            'ASB246_Claims_Reinsurance': self.generate_asb246_claims_reinsurance(),
            'ASB247_Claims_Net': self.generate_asb247_claims_net(),
            'ASB_Claims_Summary': self.generate_asb_claims_summary(),
            'ASB_Development_Factors': self.generate_claims_development_factors(),
        }
        return reports

    def generate_all_reports(self, include_qsr=True, include_aad=True, include_asb=True):
        """Generate all reports (QSR, AAD, ASB)"""
        self.load_all_data()

        all_reports = {}

        if include_qsr:
            print("\nGenerating QSR reports...")
            all_reports.update(self.generate_all_qsr_reports())

        if include_aad:
            print("\nGenerating AAD reports...")
            all_reports.update(self.generate_all_aad_reports())

        if include_asb:
            print("\nGenerating ASB reports...")
            all_reports.update(self.generate_all_asb_reports())

        return all_reports


def main():
    """Main function to generate all reports"""
    generator = SolvencyReportGenerator(data_dir='../Data/')
    reports = generator.generate_all_reports(include_qsr=True, include_aad=True, include_asb=True)

    # Save reports to CSV
    output_dir = '../Data/'

    print("\n" + "="*80)
    print("SAVING ALL REPORTS")
    print("="*80)

    for report_name, df in reports.items():
        if not df.empty:
            output_file = f'{output_dir}{report_name}.csv'
            df.to_csv(output_file, index=False)
            print(f'✓ {report_name}: {len(df)} rows, {len(df.columns)} columns')
        else:
            print(f'⚠ Warning: {report_name} is empty')

    print("\n" + "="*80)
    print("ALL REPORTS GENERATED SUCCESSFULLY!")
    print("="*80)
    print(f"Total reports: {len([r for r in reports.values() if not r.empty])}")


# Power BI compatible functions
def get_aad230_investments():
    """Power BI function: Get AAD 230 Detailed Investments"""
    generator = SolvencyReportGenerator(data_dir='../Data/')
    generator.load_all_data()
    return generator.generate_aad230_open_market_value_report()


def get_aad235_derivatives():
    """Power BI function: Get AAD 235 Derivatives"""
    generator = SolvencyReportGenerator(data_dir='../Data/')
    generator.load_all_data()
    return generator.generate_aad235_derivatives_report()


def get_asb_claims_triangles():
    """Power BI function: Get ASB Claims Triangles"""
    generator = SolvencyReportGenerator(data_dir='../Data/')
    generator.load_all_data()
    return generator.generate_asb247_claims_net()


if __name__ == '__main__':
    main()
