"""
QSR Report Generator for Power BI
Generates Solvency II Quarterly Solvency Return (QSR) reports

This script can be imported and used within Power BI to transform
Lloyd's syndicate data into standardized QSR return formats.
"""

import pandas as pd
import numpy as np
from datetime import datetime


class QSRReportGenerator:
    """Generate Solvency II QSR reports from Lloyd's syndicate data"""

    def __init__(self, data_dir='../Data/'):
        """Initialize with data directory"""
        self.data_dir = data_dir
        self.data = {}

    def load_data(self):
        """Load all synthetic data files"""
        datasets = [
            'balance_sheet',
            'own_funds',
            'technical_provisions',
            'premiums_claims',
            'investments',
            'scr_calculation',
            'mcr_calculation'
        ]

        for dataset in datasets:
            try:
                filepath = f'{self.data_dir}synthetic_{dataset}.csv'
                self.data[dataset] = pd.read_csv(filepath)
                print(f'Loaded {dataset}: {len(self.data[dataset])} rows')
            except FileNotFoundError:
                print(f'Warning: {dataset} file not found')
                self.data[dataset] = pd.DataFrame()

    def generate_qsr002_balance_sheet(self):
        """
        Generate QSR 002 - Overall Balance Sheet (S.02.01.02)

        Returns a DataFrame formatted according to Solvency II specifications
        """
        if 'balance_sheet' not in self.data or self.data['balance_sheet'].empty:
            return pd.DataFrame()

        df = self.data['balance_sheet'].copy()

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
        qsr002['R0080_Holdings_Related_Undertakings'] = df['Holdings_Related_Undertakings']
        qsr002['R0090_Equities'] = df['Equities']
        qsr002['R0100_Bonds'] = df['Bonds']
        qsr002['R0110_Government_Bonds'] = df['Government_Bonds']
        qsr002['R0120_Corporate_Bonds'] = df['Corporate_Bonds']
        qsr002['R0130_Collective_Investments'] = df['Collective_Investments']
        qsr002['R0140_Derivatives'] = df['Derivatives']
        qsr002['R0150_Deposits_Other_Than_Cash'] = df['Deposits_Other_Than_Cash']
        qsr002['R0160_Reinsurance_Recoverables'] = df['Reinsurance_Recoverables']
        qsr002['R0170_Insurance_Receivables'] = df['Insurance_Receivables']
        qsr002['R0180_Reinsurance_Receivables'] = df['Reinsurance_Receivables']
        qsr002['R0190_Receivables_Trade'] = df['Receivables_Trade']
        qsr002['R0200_Cash_and_Cash_Equivalents'] = df['Cash_and_Cash_Equivalents']
        qsr002['R0210_Other_Assets'] = df['Other_Assets']
        qsr002['R0220_Total_Assets'] = df['Total_Assets']

        # Liabilities
        qsr002['R0230_Technical_Provisions_NonLife'] = df['Technical_Provisions_NonLife']
        qsr002['R0240_Technical_Provisions_Life'] = df['Technical_Provisions_Life']
        qsr002['R0250_Best_Estimate'] = df['Best_Estimate']
        qsr002['R0260_Risk_Margin'] = df['Risk_Margin']
        qsr002['R0270_Deposits_From_Reinsurers'] = df['Deposits_From_Reinsurers']
        qsr002['R0280_Deferred_Tax_Liabilities'] = df['Deferred_Tax_Liabilities']
        qsr002['R0290_Derivatives_Liabilities'] = df['Derivatives_Liabilities']
        qsr002['R0300_Debts_Credit_Institutions'] = df['Debts_Owed_Credit_Institutions']
        qsr002['R0310_Insurance_Payables'] = df['Insurance_Payables']
        qsr002['R0320_Reinsurance_Payables'] = df['Reinsurance_Payables']
        qsr002['R0330_Payables_Trade'] = df['Payables_Trade']
        qsr002['R0340_Other_Liabilities'] = df['Other_Liabilities']
        qsr002['R0350_Total_Liabilities'] = df['Total_Liabilities']
        qsr002['R0360_Excess_Assets_Over_Liabilities'] = df['Excess_Assets_Over_Liabilities']

        return qsr002

    def generate_qsr220_own_funds(self):
        """
        Generate QSR 220 - Own Funds (S.23.01.01)

        Returns a DataFrame formatted according to Solvency II specifications
        """
        if 'own_funds' not in self.data or self.data['own_funds'].empty:
            return pd.DataFrame()

        df = self.data['own_funds'].copy()

        qsr220 = pd.DataFrame()
        qsr220['Syndicate'] = df['Syndicate']
        qsr220['Reporting_Date'] = df['Reporting_Date']

        # Basic own funds
        qsr220['R0040_Members_Contributions_FIS_Tier1_Unrestricted'] = df['Members_Contributions_FIS']
        qsr220['R0050_Subordinated_Liabilities_Tier2'] = df['Subordinated_Liabilities']
        qsr220['R0060_Reconciliation_Reserve'] = df['Reconciliation_Reserve']
        qsr220['R0070_Deductions'] = df['Deductions_Own_Funds']

        # Tier classification
        qsr220['R0080_Tier_1_Unrestricted'] = df['Tier_1_Unrestricted']
        qsr220['R0090_Tier_1_Restricted'] = df['Tier_1_Restricted']
        qsr220['R0100_Tier_2'] = df['Tier_2']
        qsr220['R0110_Tier_3'] = df['Tier_3']

        # Total and eligible own funds
        qsr220['R0120_Total_Own_Funds'] = df['Total_Own_Funds']
        qsr220['R0130_Eligible_Own_Funds_SCR'] = df['Eligible_Own_Funds_SCR']
        qsr220['R0140_Eligible_Own_Funds_MCR'] = df['Eligible_Own_Funds_MCR']

        return qsr220

    def generate_qsr240_technical_provisions(self):
        """
        Generate QSR 240 - Non-Life Technical Provisions (S.17.01.02)

        Returns a DataFrame formatted according to Solvency II specifications
        """
        if 'technical_provisions' not in self.data or self.data['technical_provisions'].empty:
            return pd.DataFrame()

        df = self.data['technical_provisions'].copy()

        qsr240 = pd.DataFrame()
        qsr240['Syndicate'] = df['Syndicate']
        qsr240['Reporting_Date'] = df['Reporting_Date']
        qsr240['Line_of_Business'] = df['Line_of_Business']

        # Technical provisions components
        qsr240['Technical_Provisions_Calculated_Whole'] = df['Technical_Provisions_Calculated_Whole']

        # Best Estimate
        qsr240['Best_Estimate_Gross'] = df['Best_Estimate_Gross']
        qsr240['Best_Estimate_Recoverable'] = df['Best_Estimate_Recoverable']
        qsr240['Best_Estimate_Net'] = df['Best_Estimate_Net']

        # Risk Margin
        qsr240['Risk_Margin'] = df['Risk_Margin']

        # Total Technical Provisions
        qsr240['Technical_Provisions_Gross'] = df['Technical_Provisions_Gross']
        qsr240['Technical_Provisions_Recoverable'] = df['Technical_Provisions_Recoverable']
        qsr240['Technical_Provisions_Net'] = df['Technical_Provisions_Net']

        return qsr240

    def generate_qsr440_premiums_claims(self):
        """
        Generate QSR 440 - Non-Life Insurance Claims Information (S.05.01.02.01)

        Returns a DataFrame formatted according to Solvency II specifications
        """
        if 'premiums_claims' not in self.data or self.data['premiums_claims'].empty:
            return pd.DataFrame()

        df = self.data['premiums_claims'].copy()

        qsr440 = pd.DataFrame()
        qsr440['Syndicate'] = df['Syndicate']
        qsr440['Reporting_Date'] = df['Reporting_Date']
        qsr440['Line_of_Business'] = df['Line_of_Business']

        # Premiums
        qsr440['Premiums_Written_Gross'] = df['Premiums_Written_Gross']
        qsr440['Premiums_Written_Reinsurers_Share'] = df['Premiums_Written_Reinsurers_Share']
        qsr440['Premiums_Written_Net'] = df['Premiums_Written_Net']
        qsr440['Premiums_Earned_Gross'] = df['Premiums_Earned_Gross']
        qsr440['Premiums_Earned_Reinsurers_Share'] = df['Premiums_Earned_Reinsurers_Share']
        qsr440['Premiums_Earned_Net'] = df['Premiums_Earned_Net']

        # Claims
        qsr440['Claims_Incurred_Gross'] = df['Claims_Incurred_Gross']
        qsr440['Claims_Incurred_Reinsurers_Share'] = df['Claims_Incurred_Reinsurers_Share']
        qsr440['Claims_Incurred_Net'] = df['Claims_Incurred_Net']

        # Changes in other technical provisions
        qsr440['Changes_Other_TP_Gross'] = df['Changes_Other_Technical_Provisions_Gross']
        qsr440['Changes_Other_TP_Reinsurers'] = df['Changes_Other_Technical_Provisions_Reinsurers']
        qsr440['Changes_Other_TP_Net'] = df['Changes_Other_Technical_Provisions_Net']

        # Expenses
        qsr440['Expenses_Incurred'] = df['Expenses_Incurred']

        # Ratios
        qsr440['Loss_Ratio'] = df['Loss_Ratio']
        qsr440['Expense_Ratio'] = df['Expense_Ratio']
        qsr440['Combined_Ratio'] = df['Combined_Ratio']

        return qsr440

    def generate_qsr291_operational_risk(self):
        """
        Generate QSR 291 - Operational Risk (S.41.01.11)

        Returns a DataFrame with operational risk calculations
        """
        if 'scr_calculation' not in self.data or self.data['scr_calculation'].empty:
            return pd.DataFrame()

        df = self.data['scr_calculation'].copy()

        qsr291 = pd.DataFrame()
        qsr291['Syndicate'] = df['Syndicate']
        qsr291['Reporting_Date'] = df['Reporting_Date']
        qsr291['Operational_Risk'] = df['Operational_Risk']

        return qsr291

    def generate_qsr292_market_risk(self):
        """
        Generate QSR 292 - Market Risk (S.14.01.10.01)

        Returns a DataFrame with detailed market risk sub-modules
        """
        if 'scr_calculation' not in self.data or self.data['scr_calculation'].empty:
            return pd.DataFrame()

        df = self.data['scr_calculation'].copy()

        qsr292 = pd.DataFrame()
        qsr292['Syndicate'] = df['Syndicate']
        qsr292['Reporting_Date'] = df['Reporting_Date']
        qsr292['Market_Risk_Total'] = df['Market_Risk']
        qsr292['Interest_Rate_Risk'] = df['Interest_Rate_Risk']
        qsr292['Equity_Risk'] = df['Equity_Risk']
        qsr292['Property_Risk'] = df['Property_Risk']
        qsr292['Spread_Risk'] = df['Spread_Risk']
        qsr292['Currency_Risk'] = df['Currency_Risk']
        qsr292['Concentration_Risk'] = df['Concentration_Risk']

        return qsr292

    def generate_qsr293_counterparty_risk(self):
        """
        Generate QSR 293 - Counterparty Default Risk (S.38.01.10.01)

        Returns a DataFrame with counterparty default risk
        """
        if 'scr_calculation' not in self.data or self.data['scr_calculation'].empty:
            return pd.DataFrame()

        df = self.data['scr_calculation'].copy()

        qsr293 = pd.DataFrame()
        qsr293['Syndicate'] = df['Syndicate']
        qsr293['Reporting_Date'] = df['Reporting_Date']
        qsr293['Counterparty_Default_Risk'] = df['Counterparty_Default_Risk']

        return qsr293

    def generate_qsr510_mcr(self):
        """
        Generate QSR 510 - Minimum Capital Requirement (S.28.01.01)

        Returns a DataFrame formatted according to Solvency II specifications
        """
        if 'mcr_calculation' not in self.data or self.data['mcr_calculation'].empty:
            return pd.DataFrame()

        df = self.data['mcr_calculation'].copy()

        qsr510 = pd.DataFrame()
        qsr510['Syndicate'] = df['Syndicate']
        qsr510['Reporting_Date'] = df['Reporting_Date']
        qsr510['Linear_MCR'] = df['Linear_MCR']
        qsr510['SCR'] = df['SCR']
        qsr510['MCR_Cap'] = df['MCR_Cap']
        qsr510['MCR_Floor'] = df['MCR_Floor']
        qsr510['Combined_MCR'] = df['Combined_MCR']
        qsr510['Absolute_Floor_MCR'] = df['Absolute_Floor_MCR']
        qsr510['MCR'] = df['MCR']

        return qsr510

    def generate_scr_summary(self):
        """
        Generate SCR Summary with all risk modules

        Returns a comprehensive DataFrame with SCR calculation
        """
        if 'scr_calculation' not in self.data or self.data['scr_calculation'].empty:
            return pd.DataFrame()

        df = self.data['scr_calculation'].copy()

        scr_summary = pd.DataFrame()
        scr_summary['Syndicate'] = df['Syndicate']
        scr_summary['Reporting_Date'] = df['Reporting_Date']

        # Risk modules
        scr_summary['Market_Risk'] = df['Market_Risk']
        scr_summary['Counterparty_Default_Risk'] = df['Counterparty_Default_Risk']
        scr_summary['Life_Underwriting_Risk'] = df['Life_Underwriting_Risk']
        scr_summary['Health_Underwriting_Risk'] = df['Health_Underwriting_Risk']
        scr_summary['Non_Life_Underwriting_Risk'] = df['Non_Life_Underwriting_Risk']
        scr_summary['Diversification'] = df['Diversification']
        scr_summary['BSCR'] = df['BSCR']
        scr_summary['Operational_Risk'] = df['Operational_Risk']
        scr_summary['Loss_Absorbing_Capacity_DT'] = df['Loss_Absorbing_Capacity_DT']
        scr_summary['SCR'] = df['SCR']

        return scr_summary

    def generate_solvency_ratio_report(self):
        """
        Generate Solvency Ratio Report combining Own Funds and SCR/MCR

        Returns a DataFrame with solvency coverage ratios
        """
        if ('own_funds' not in self.data or self.data['own_funds'].empty or
            'scr_calculation' not in self.data or self.data['scr_calculation'].empty or
            'mcr_calculation' not in self.data or self.data['mcr_calculation'].empty):
            return pd.DataFrame()

        # Merge own funds with SCR and MCR
        df = self.data['own_funds'].copy()
        scr = self.data['scr_calculation'][['Syndicate', 'SCR']].copy()
        mcr = self.data['mcr_calculation'][['Syndicate', 'MCR']].copy()

        solvency = df.merge(scr, on='Syndicate', how='left')
        solvency = solvency.merge(mcr, on='Syndicate', how='left')

        # Calculate ratios
        solvency['SCR_Ratio'] = (solvency['Eligible_Own_Funds_SCR'] / solvency['SCR'] * 100).round(2)
        solvency['MCR_Ratio'] = (solvency['Eligible_Own_Funds_MCR'] / solvency['MCR'] * 100).round(2)
        solvency['Surplus_SCR'] = solvency['Eligible_Own_Funds_SCR'] - solvency['SCR']
        solvency['Surplus_MCR'] = solvency['Eligible_Own_Funds_MCR'] - solvency['MCR']

        # Select columns for report
        report = solvency[['Syndicate', 'Reporting_Date', 'Total_Own_Funds',
                          'Eligible_Own_Funds_SCR', 'Eligible_Own_Funds_MCR',
                          'SCR', 'MCR', 'SCR_Ratio', 'MCR_Ratio',
                          'Surplus_SCR', 'Surplus_MCR']]

        return report

    def generate_all_reports(self):
        """Generate all QSR reports"""
        self.load_data()

        reports = {
            'QSR002_Balance_Sheet': self.generate_qsr002_balance_sheet(),
            'QSR220_Own_Funds': self.generate_qsr220_own_funds(),
            'QSR240_Technical_Provisions': self.generate_qsr240_technical_provisions(),
            'QSR440_Premiums_Claims': self.generate_qsr440_premiums_claims(),
            'QSR291_Operational_Risk': self.generate_qsr291_operational_risk(),
            'QSR292_Market_Risk': self.generate_qsr292_market_risk(),
            'QSR293_Counterparty_Risk': self.generate_qsr293_counterparty_risk(),
            'QSR510_MCR': self.generate_qsr510_mcr(),
            'SCR_Summary': self.generate_scr_summary(),
            'Solvency_Ratio_Report': self.generate_solvency_ratio_report(),
        }

        return reports


def main():
    """Main function to generate QSR reports"""
    generator = QSRReportGenerator(data_dir='../Data/')
    reports = generator.generate_all_reports()

    # Save reports to CSV
    output_dir = '../Data/'

    for report_name, df in reports.items():
        if not df.empty:
            output_file = f'{output_dir}{report_name}.csv'
            df.to_csv(output_file, index=False)
            print(f'Generated {report_name}: {len(df)} rows, {len(df.columns)} columns')
        else:
            print(f'Warning: {report_name} is empty')

    print('\nAll QSR reports generated successfully!')


# Power BI compatible functions
# These functions can be called directly from Power BI Python scripts

def get_balance_sheet():
    """Power BI function: Get QSR 002 Balance Sheet"""
    generator = QSRReportGenerator(data_dir='../Data/')
    generator.load_data()
    return generator.generate_qsr002_balance_sheet()


def get_own_funds():
    """Power BI function: Get QSR 220 Own Funds"""
    generator = QSRReportGenerator(data_dir='../Data/')
    generator.load_data()
    return generator.generate_qsr220_own_funds()


def get_technical_provisions():
    """Power BI function: Get QSR 240 Technical Provisions"""
    generator = QSRReportGenerator(data_dir='../Data/')
    generator.load_data()
    return generator.generate_qsr240_technical_provisions()


def get_premiums_claims():
    """Power BI function: Get QSR 440 Premiums and Claims"""
    generator = QSRReportGenerator(data_dir='../Data/')
    generator.load_data()
    return generator.generate_qsr440_premiums_claims()


def get_solvency_ratios():
    """Power BI function: Get Solvency Ratios Report"""
    generator = QSRReportGenerator(data_dir='../Data/')
    generator.load_data()
    return generator.generate_solvency_ratio_report()


if __name__ == '__main__':
    main()
