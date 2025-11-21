"""
Synthetic Lloyd's of London Data Generator
Generates realistic synthetic data for Solvency II QSR reporting

This script creates synthetic data mimicking Lloyd's of London syndicate data
for use in Power BI reporting and analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class LloydsDataGenerator:
    """Generate synthetic Lloyd's of London syndicate data"""

    def __init__(self, seed=42):
        """Initialize the data generator with a random seed for reproducibility"""
        np.random.seed(seed)
        random.seed(seed)

        # Define syndicate numbers (typical Lloyd's syndicate numbers)
        self.syndicates = [
            '0001', '0033', '0099', '0218', '0308', '0510', '0609', '0727',
            '0886', '1003', '1183', '1221', '1458', '1729', '1955', '2001',
            '2003', '2121', '2488', '2623', '2791', '3000', '3210', '3456',
            '4242', '5000', '5820', '6104', '6117', '6129'
        ]

        # Lines of business (Solvency II classification)
        self.lines_of_business = [
            'Medical expense insurance',
            'Income protection insurance',
            'Workers compensation insurance',
            'Motor vehicle liability insurance',
            'Other motor insurance',
            'Marine, aviation and transport insurance',
            'Fire and other damage to property insurance',
            'General liability insurance',
            'Credit and suretyship insurance',
            'Legal expenses insurance',
            'Assistance',
            'Miscellaneous financial loss',
            'Non-proportional health reinsurance',
            'Non-proportional casualty reinsurance',
            'Non-proportional marine, aviation and transport reinsurance',
            'Non-proportional property reinsurance'
        ]

        # Asset classes for investments
        self.asset_classes = [
            'Government bonds',
            'Corporate bonds',
            'Equities',
            'Investment funds',
            'Property',
            'Loans and mortgages',
            'Cash and deposits'
        ]

        # Countries for geographical diversification
        self.countries = ['GB', 'US', 'DE', 'FR', 'JP', 'AU', 'CA', 'CH', 'NL', 'IT']

        # Reporting date
        self.reporting_date = datetime(2025, 9, 30)  # Q3 2025

    def generate_balance_sheet_data(self, num_syndicates=10):
        """Generate QSR 002 - Balance Sheet data"""
        data = []

        syndicates = random.sample(self.syndicates, min(num_syndicates, len(self.syndicates)))

        for syndicate in syndicates:
            # Assets
            assets = {
                'Syndicate': syndicate,
                'Reporting_Date': self.reporting_date,
                'Goodwill': 0,  # Always 0 per validation
                'Deferred_Acquisition_Costs': 0,  # Always 0 per validation
                'Intangible_Assets': 0,
                'Deferred_Tax_Assets': np.random.uniform(0, 5000000),
                'Pension_Benefit_Surplus': np.random.uniform(0, 2000000),
                'Property_Plant_Equipment': np.random.uniform(1000000, 10000000),
                'Investments': np.random.uniform(100000000, 500000000),
                'Holdings_Related_Undertakings': np.random.uniform(0, 50000000),
                'Equities': np.random.uniform(10000000, 100000000),
                'Bonds': np.random.uniform(50000000, 300000000),
                'Government_Bonds': np.random.uniform(30000000, 200000000),
                'Corporate_Bonds': np.random.uniform(20000000, 100000000),
                'Collective_Investments': np.random.uniform(5000000, 50000000),
                'Derivatives': np.random.uniform(0, 10000000),
                'Deposits_Other_Than_Cash': np.random.uniform(5000000, 30000000),
                'Reinsurance_Recoverables': np.random.uniform(20000000, 150000000),
                'Insurance_Receivables': np.random.uniform(10000000, 80000000),
                'Reinsurance_Receivables': np.random.uniform(5000000, 40000000),
                'Receivables_Trade': np.random.uniform(3000000, 20000000),
                'Cash_and_Cash_Equivalents': np.random.uniform(10000000, 60000000),
                'Other_Assets': np.random.uniform(2000000, 15000000),
            }

            # Calculate total assets
            assets['Total_Assets'] = sum([v for k, v in assets.items()
                                         if k not in ['Syndicate', 'Reporting_Date']])

            # Liabilities
            tech_provisions = np.random.uniform(150000000, 400000000)
            assets['Technical_Provisions_NonLife'] = tech_provisions
            assets['Technical_Provisions_Life'] = 0  # Assuming non-life only
            assets['Best_Estimate'] = tech_provisions * 0.85
            assets['Risk_Margin'] = tech_provisions * 0.15
            assets['Deposits_From_Reinsurers'] = np.random.uniform(5000000, 30000000)
            assets['Deferred_Tax_Liabilities'] = np.random.uniform(0, 3000000)
            assets['Derivatives_Liabilities'] = np.random.uniform(0, 5000000)
            assets['Debts_Owed_Credit_Institutions'] = np.random.uniform(0, 20000000)
            assets['Insurance_Payables'] = np.random.uniform(8000000, 50000000)
            assets['Reinsurance_Payables'] = np.random.uniform(4000000, 25000000)
            assets['Payables_Trade'] = np.random.uniform(2000000, 15000000)
            assets['Other_Liabilities'] = np.random.uniform(3000000, 20000000)

            # Calculate total liabilities
            total_liabilities = (assets['Technical_Provisions_NonLife'] +
                               assets['Technical_Provisions_Life'] +
                               assets['Deposits_From_Reinsurers'] +
                               assets['Deferred_Tax_Liabilities'] +
                               assets['Derivatives_Liabilities'] +
                               assets['Debts_Owed_Credit_Institutions'] +
                               assets['Insurance_Payables'] +
                               assets['Reinsurance_Payables'] +
                               assets['Payables_Trade'] +
                               assets['Other_Liabilities'])

            assets['Total_Liabilities'] = total_liabilities

            # Excess of assets over liabilities (Own Funds)
            assets['Excess_Assets_Over_Liabilities'] = assets['Total_Assets'] - assets['Total_Liabilities']

            data.append(assets)

        return pd.DataFrame(data)

    def generate_own_funds_data(self, num_syndicates=10):
        """Generate QSR 220 - Own Funds data"""
        data = []

        syndicates = random.sample(self.syndicates, min(num_syndicates, len(self.syndicates)))

        for syndicate in syndicates:
            own_funds = {
                'Syndicate': syndicate,
                'Reporting_Date': self.reporting_date,
                'Members_Contributions_FIS': np.random.uniform(50000000, 200000000),
                'Subordinated_Liabilities': np.random.uniform(0, 30000000),
                'Reconciliation_Reserve': np.random.uniform(20000000, 100000000),
                'Deductions_Own_Funds': np.random.uniform(0, 5000000),
            }

            # Tier classification
            own_funds['Tier_1_Unrestricted'] = own_funds['Members_Contributions_FIS'] + own_funds['Reconciliation_Reserve']
            own_funds['Tier_1_Restricted'] = 0
            own_funds['Tier_2'] = own_funds['Subordinated_Liabilities']
            own_funds['Tier_3'] = 0

            own_funds['Total_Own_Funds'] = (own_funds['Tier_1_Unrestricted'] +
                                           own_funds['Tier_1_Restricted'] +
                                           own_funds['Tier_2'] +
                                           own_funds['Tier_3'] -
                                           own_funds['Deductions_Own_Funds'])

            # Eligible own funds to meet SCR and MCR
            own_funds['Eligible_Own_Funds_SCR'] = own_funds['Total_Own_Funds']
            own_funds['Eligible_Own_Funds_MCR'] = own_funds['Tier_1_Unrestricted'] + min(own_funds['Tier_2'], own_funds['Tier_1_Unrestricted'] * 0.2)

            data.append(own_funds)

        return pd.DataFrame(data)

    def generate_technical_provisions_data(self, num_syndicates=10):
        """Generate QSR 240 - Technical Provisions data"""
        data = []

        syndicates = random.sample(self.syndicates, min(num_syndicates, len(self.syndicates)))

        for syndicate in syndicates:
            for lob in random.sample(self.lines_of_business[:12], 8):  # Select 8 non-life LOBs
                tp = {
                    'Syndicate': syndicate,
                    'Reporting_Date': self.reporting_date,
                    'Line_of_Business': lob,
                    'Technical_Provisions_Calculated_Whole': 0,
                    'Best_Estimate_Gross': np.random.uniform(10000000, 50000000),
                    'Best_Estimate_Recoverable': np.random.uniform(2000000, 15000000),
                    'Best_Estimate_Net': 0,  # Will be calculated
                    'Risk_Margin': np.random.uniform(1000000, 8000000),
                    'Technical_Provisions_Gross': 0,  # Will be calculated
                    'Technical_Provisions_Recoverable': 0,  # Will be calculated
                    'Technical_Provisions_Net': 0,  # Will be calculated
                }

                tp['Best_Estimate_Net'] = tp['Best_Estimate_Gross'] - tp['Best_Estimate_Recoverable']
                tp['Technical_Provisions_Gross'] = tp['Best_Estimate_Gross'] + tp['Risk_Margin']
                tp['Technical_Provisions_Recoverable'] = tp['Best_Estimate_Recoverable']
                tp['Technical_Provisions_Net'] = tp['Technical_Provisions_Gross'] - tp['Technical_Provisions_Recoverable']

                data.append(tp)

        return pd.DataFrame(data)

    def generate_premiums_claims_data(self, num_syndicates=10):
        """Generate QSR 440/450 - Premiums, Claims and Expenses data"""
        data = []

        syndicates = random.sample(self.syndicates, min(num_syndicates, len(self.syndicates)))

        for syndicate in syndicates:
            for lob in random.sample(self.lines_of_business[:12], 8):
                pc = {
                    'Syndicate': syndicate,
                    'Reporting_Date': self.reporting_date,
                    'Line_of_Business': lob,
                    'Premiums_Written_Gross': np.random.uniform(20000000, 100000000),
                    'Premiums_Written_Reinsurers_Share': np.random.uniform(5000000, 30000000),
                    'Premiums_Written_Net': 0,  # Will be calculated
                    'Premiums_Earned_Gross': np.random.uniform(18000000, 95000000),
                    'Premiums_Earned_Reinsurers_Share': np.random.uniform(4500000, 28500000),
                    'Premiums_Earned_Net': 0,  # Will be calculated
                    'Claims_Incurred_Gross': np.random.uniform(12000000, 70000000),
                    'Claims_Incurred_Reinsurers_Share': np.random.uniform(3000000, 21000000),
                    'Claims_Incurred_Net': 0,  # Will be calculated
                    'Changes_Other_Technical_Provisions_Gross': np.random.uniform(-5000000, 5000000),
                    'Changes_Other_Technical_Provisions_Reinsurers': np.random.uniform(-1500000, 1500000),
                    'Changes_Other_Technical_Provisions_Net': 0,  # Will be calculated
                    'Expenses_Incurred': np.random.uniform(5000000, 25000000),
                }

                pc['Premiums_Written_Net'] = pc['Premiums_Written_Gross'] - pc['Premiums_Written_Reinsurers_Share']
                pc['Premiums_Earned_Net'] = pc['Premiums_Earned_Gross'] - pc['Premiums_Earned_Reinsurers_Share']
                pc['Claims_Incurred_Net'] = pc['Claims_Incurred_Gross'] - pc['Claims_Incurred_Reinsurers_Share']
                pc['Changes_Other_Technical_Provisions_Net'] = (pc['Changes_Other_Technical_Provisions_Gross'] -
                                                                pc['Changes_Other_Technical_Provisions_Reinsurers'])

                # Calculate loss ratio
                pc['Loss_Ratio'] = (pc['Claims_Incurred_Net'] / pc['Premiums_Earned_Net'] * 100) if pc['Premiums_Earned_Net'] != 0 else 0
                pc['Expense_Ratio'] = (pc['Expenses_Incurred'] / pc['Premiums_Earned_Net'] * 100) if pc['Premiums_Earned_Net'] != 0 else 0
                pc['Combined_Ratio'] = pc['Loss_Ratio'] + pc['Expense_Ratio']

                data.append(pc)

        return pd.DataFrame(data)

    def generate_investments_data(self, num_syndicates=10):
        """Generate investment portfolio data"""
        data = []

        syndicates = random.sample(self.syndicates, min(num_syndicates, len(self.syndicates)))

        for syndicate in syndicates:
            for asset_class in self.asset_classes:
                inv = {
                    'Syndicate': syndicate,
                    'Reporting_Date': self.reporting_date,
                    'Asset_Class': asset_class,
                    'Solvency_II_Value': np.random.uniform(5000000, 80000000),
                    'Accrued_Interest': np.random.uniform(0, 500000),
                    'Country': random.choice(self.countries),
                }
                data.append(inv)

        return pd.DataFrame(data)

    def generate_scr_calculation_data(self, num_syndicates=10):
        """Generate SCR (Solvency Capital Requirement) calculation data"""
        data = []

        syndicates = random.sample(self.syndicates, min(num_syndicates, len(self.syndicates)))

        for syndicate in syndicates:
            scr = {
                'Syndicate': syndicate,
                'Reporting_Date': self.reporting_date,
                'Market_Risk': np.random.uniform(15000000, 60000000),
                'Interest_Rate_Risk': np.random.uniform(3000000, 15000000),
                'Equity_Risk': np.random.uniform(5000000, 25000000),
                'Property_Risk': np.random.uniform(2000000, 10000000),
                'Spread_Risk': np.random.uniform(4000000, 20000000),
                'Currency_Risk': np.random.uniform(2000000, 12000000),
                'Concentration_Risk': np.random.uniform(1000000, 5000000),
                'Counterparty_Default_Risk': np.random.uniform(8000000, 35000000),
                'Life_Underwriting_Risk': 0,  # Assuming non-life only
                'Health_Underwriting_Risk': np.random.uniform(2000000, 10000000),
                'Non_Life_Underwriting_Risk': np.random.uniform(25000000, 100000000),
                'Premium_Reserve_Risk': np.random.uniform(15000000, 70000000),
                'Lapse_Risk': np.random.uniform(0, 5000000),
                'CAT_Risk': np.random.uniform(10000000, 40000000),
                'Operational_Risk': np.random.uniform(5000000, 20000000),
                'Loss_Absorbing_Capacity_DT': np.random.uniform(-10000000, -2000000),
            }

            # Calculate BSCR (Basic SCR before operational risk and loss absorbing capacity)
            bscr_before_diversification = (scr['Market_Risk'] +
                                          scr['Counterparty_Default_Risk'] +
                                          scr['Life_Underwriting_Risk'] +
                                          scr['Health_Underwriting_Risk'] +
                                          scr['Non_Life_Underwriting_Risk'])

            # Apply diversification benefit (typically 10-30%)
            diversification_benefit = bscr_before_diversification * np.random.uniform(-0.30, -0.10)
            scr['Diversification'] = diversification_benefit
            scr['BSCR'] = bscr_before_diversification + diversification_benefit

            # Calculate final SCR
            scr['SCR'] = scr['BSCR'] + scr['Operational_Risk'] + scr['Loss_Absorbing_Capacity_DT']

            # Ensure SCR is positive
            scr['SCR'] = max(scr['SCR'], 0)

            data.append(scr)

        return pd.DataFrame(data)

    def generate_mcr_calculation_data(self, num_syndicates=10):
        """Generate QSR 510/511 - MCR (Minimum Capital Requirement) data"""
        data = []

        syndicates = random.sample(self.syndicates, min(num_syndicates, len(self.syndicates)))

        for syndicate in syndicates:
            # Get corresponding SCR
            scr_value = np.random.uniform(60000000, 150000000)

            mcr = {
                'Syndicate': syndicate,
                'Reporting_Date': self.reporting_date,
                'Linear_MCR': np.random.uniform(15000000, 50000000),
                'SCR': scr_value,
                'MCR_Cap': scr_value * 0.45,
                'MCR_Floor': scr_value * 0.25,
                'Combined_MCR': 0,  # Will be calculated
                'Absolute_Floor_MCR': 2200000,  # EUR 2.2m converted to GBP equivalent
            }

            # MCR is the maximum of Linear MCR and Absolute Floor,
            # but capped between MCR Floor and MCR Cap
            mcr['Combined_MCR'] = max(
                min(mcr['Linear_MCR'], mcr['MCR_Cap']),
                max(mcr['MCR_Floor'], mcr['Absolute_Floor_MCR'])
            )

            mcr['MCR'] = mcr['Combined_MCR']

            data.append(mcr)

        return pd.DataFrame(data)

    def generate_all_data(self, num_syndicates=10):
        """Generate all synthetic data for QSR reporting"""
        return {
            'balance_sheet': self.generate_balance_sheet_data(num_syndicates),
            'own_funds': self.generate_own_funds_data(num_syndicates),
            'technical_provisions': self.generate_technical_provisions_data(num_syndicates),
            'premiums_claims': self.generate_premiums_claims_data(num_syndicates),
            'investments': self.generate_investments_data(num_syndicates),
            'scr_calculation': self.generate_scr_calculation_data(num_syndicates),
            'mcr_calculation': self.generate_mcr_calculation_data(num_syndicates),
        }


def main():
    """Main function to generate and save synthetic data"""
    generator = LloydsDataGenerator(seed=42)

    # Generate data for 15 syndicates
    all_data = generator.generate_all_data(num_syndicates=15)

    # Save to CSV files
    output_dir = '../Data/'

    for dataset_name, df in all_data.items():
        output_file = f'{output_dir}synthetic_{dataset_name}.csv'
        df.to_csv(output_file, index=False)
        print(f'Generated {output_file}: {len(df)} rows, {len(df.columns)} columns')

    print('\nSynthetic data generation complete!')
    print(f'Total datasets created: {len(all_data)}')


if __name__ == '__main__':
    main()
