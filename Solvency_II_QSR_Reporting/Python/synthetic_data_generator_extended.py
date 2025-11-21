"""
Extended Synthetic Lloyd's of London Data Generator
Generates realistic synthetic data for Solvency II reporting:
- QSR (Quarterly Solvency Return)
- AAD (Annual Actuarial Data)
- ASB (Annual Solvency Balance Sheet)

This script creates comprehensive synthetic data for both quarterly and annual reporting.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


class LloydsDataGeneratorExtended:
    """Generate synthetic Lloyd's of London data for QSR, AAD, and ASB returns"""

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

        # Specific instrument types for AAD 230
        self.instrument_types = [
            'Sovereign bonds',
            'Corporate bonds - Investment grade',
            'Corporate bonds - Non-investment grade',
            'Equities - Listed',
            'Equities - Unlisted',
            'Collective investment undertakings',
            'Mortgage loans',
            'Policy loans',
            'Deposits with credit institutions',
            'Real estate',
            'Other investments'
        ]

        # Derivative types for AAD 235
        self.derivative_types = [
            'Interest rate swaps',
            'Currency forwards',
            'Equity options',
            'Credit default swaps',
            'Commodity futures',
            'FX options'
        ]

        # Countries for geographical diversification
        self.countries = ['GB', 'US', 'DE', 'FR', 'JP', 'AU', 'CA', 'CH', 'NL', 'IT']

        # Currency codes
        self.currencies = ['GBP', 'USD', 'EUR', 'JPY', 'CHF', 'AUD', 'CAD']

        # Reporting dates
        self.quarterly_date_q3 = datetime(2025, 9, 30)  # Q3 2025
        self.annual_date_2024 = datetime(2024, 12, 31)  # Year-end 2024

    # ========================================================================
    # QSR DATA GENERATION (Existing methods from original generator)
    # ========================================================================

    def generate_balance_sheet_data(self, num_syndicates=10, reporting_date=None):
        """Generate QSR 002 - Balance Sheet data"""
        if reporting_date is None:
            reporting_date = self.quarterly_date_q3

        data = []
        syndicates = random.sample(self.syndicates, min(num_syndicates, len(self.syndicates)))

        for syndicate in syndicates:
            assets = {
                'Syndicate': syndicate,
                'Reporting_Date': reporting_date,
                'Goodwill': 0,
                'Deferred_Acquisition_Costs': 0,
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

            assets['Total_Assets'] = sum([v for k, v in assets.items()
                                         if k not in ['Syndicate', 'Reporting_Date']])

            tech_provisions = np.random.uniform(150000000, 400000000)
            assets['Technical_Provisions_NonLife'] = tech_provisions
            assets['Technical_Provisions_Life'] = 0
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

            assets['Total_Liabilities'] = (assets['Technical_Provisions_NonLife'] +
                                          assets['Technical_Provisions_Life'] +
                                          assets['Deposits_From_Reinsurers'] +
                                          assets['Deferred_Tax_Liabilities'] +
                                          assets['Derivatives_Liabilities'] +
                                          assets['Debts_Owed_Credit_Institutions'] +
                                          assets['Insurance_Payables'] +
                                          assets['Reinsurance_Payables'] +
                                          assets['Payables_Trade'] +
                                          assets['Other_Liabilities'])

            assets['Excess_Assets_Over_Liabilities'] = assets['Total_Assets'] - assets['Total_Liabilities']

            data.append(assets)

        return pd.DataFrame(data)

    # ========================================================================
    # AAD DATA GENERATION (Annual Actuarial Data)
    # ========================================================================

    def generate_aad230_open_market_value(self, num_syndicates=10):
        """
        Generate AAD 230 - Open Market Value of Investments (S.06.02.01)
        Detailed investment holdings at security level
        """
        data = []
        syndicates = random.sample(self.syndicates, min(num_syndicates, len(self.syndicates)))

        for syndicate in syndicates:
            # Generate 20-50 investment holdings per syndicate
            num_holdings = random.randint(20, 50)

            for i in range(num_holdings):
                holding = {
                    'Syndicate': syndicate,
                    'Reporting_Date': self.annual_date_2024,
                    'Asset_ID': f'{syndicate}-INV-{i+1:04d}',
                    'Instrument_Type': random.choice(self.instrument_types),
                    'Asset_Category': random.choice(self.asset_classes),
                    'Issuer_Name': f'Issuer_{random.randint(1, 500)}',
                    'Issuer_Country': random.choice(self.countries),
                    'Issuer_Sector': random.choice(['Financial', 'Industrial', 'Utilities', 'Government']),
                    'Currency': random.choice(self.currencies),
                    'Quantity': np.random.uniform(1000, 1000000),
                    'Unit_Solvency_II_Value': np.random.uniform(50, 500),
                    'Total_Solvency_II_Value': 0,  # Will calculate
                    'Book_Value': 0,  # Will calculate
                    'Maturity_Date': datetime(2025 + random.randint(1, 15), random.randint(1, 12), 1),
                    'Credit_Rating': random.choice(['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'Not rated']),
                    'External_Rating': random.choice(['S&P', 'Moodys', 'Fitch', 'None']),
                    'Internal_Rating': random.choice(['1', '2', '3', '4', '5', '6']),
                }

                holding['Total_Solvency_II_Value'] = holding['Quantity'] * holding['Unit_Solvency_II_Value']
                holding['Book_Value'] = holding['Total_Solvency_II_Value'] * np.random.uniform(0.95, 1.05)

                data.append(holding)

        return pd.DataFrame(data)

    def generate_aad233_off_balance_sheet(self, num_syndicates=10):
        """
        Generate AAD 233 - Off-Balance Sheet Items (S.08.01.01)
        Contingent liabilities, commitments, etc.
        """
        data = []
        syndicates = random.sample(self.syndicates, min(num_syndicates, len(self.syndicates)))

        off_balance_types = [
            'Guarantees provided',
            'Letters of credit',
            'Committed undrawn credit facilities',
            'Unfunded pension obligations',
            'Legal contingencies',
            'Operating lease commitments'
        ]

        for syndicate in syndicates:
            # 3-8 off-balance sheet items per syndicate
            num_items = random.randint(3, 8)

            for i in range(num_items):
                item = {
                    'Syndicate': syndicate,
                    'Reporting_Date': self.annual_date_2024,
                    'Item_ID': f'{syndicate}-OBS-{i+1:03d}',
                    'Item_Type': random.choice(off_balance_types),
                    'Description': f'Off-balance sheet item {i+1}',
                    'Counterparty': f'Counterparty_{random.randint(1, 100)}',
                    'Maximum_Exposure': np.random.uniform(1000000, 50000000),
                    'Probability_Of_Call': np.random.uniform(0, 0.3),
                    'Expected_Value': 0,  # Will calculate
                    'Maturity_Date': datetime(2025 + random.randint(1, 10), random.randint(1, 12), 1),
                }

                item['Expected_Value'] = item['Maximum_Exposure'] * item['Probability_Of_Call']

                data.append(item)

        return pd.DataFrame(data)

    def generate_aad235_derivatives(self, num_syndicates=10):
        """
        Generate AAD 235 - Derivatives (S.09.01.01)
        All derivative contracts
        """
        data = []
        syndicates = random.sample(self.syndicates, min(num_syndicates, len(self.syndicates)))

        for syndicate in syndicates:
            # 5-15 derivative contracts per syndicate
            num_derivatives = random.randint(5, 15)

            for i in range(num_derivatives):
                derivative = {
                    'Syndicate': syndicate,
                    'Reporting_Date': self.annual_date_2024,
                    'Contract_ID': f'{syndicate}-DRV-{i+1:04d}',
                    'Derivative_Type': random.choice(self.derivative_types),
                    'Underlying_Asset': random.choice(['Interest Rate', 'FX', 'Equity', 'Commodity', 'Credit']),
                    'Notional_Amount': np.random.uniform(5000000, 100000000),
                    'Currency': random.choice(self.currencies),
                    'Counterparty': f'Derivative_CP_{random.randint(1, 50)}',
                    'Counterparty_Rating': random.choice(['AAA', 'AA', 'A', 'BBB', 'BB']),
                    'Cleared_Or_OTC': random.choice(['Cleared', 'OTC']),
                    'Fair_Value_Asset': np.random.uniform(0, 2000000) if random.random() > 0.5 else 0,
                    'Fair_Value_Liability': np.random.uniform(0, 2000000) if random.random() > 0.5 else 0,
                    'Delta': np.random.uniform(-1, 1),
                    'Gamma': np.random.uniform(0, 0.1),
                    'Vega': np.random.uniform(0, 100000),
                    'Trade_Date': datetime(2024, random.randint(1, 12), random.randint(1, 28)),
                    'Maturity_Date': datetime(2025 + random.randint(0, 5), random.randint(1, 12), 1),
                    'Purpose': random.choice(['Hedging', 'Trading', 'Other']),
                }

                data.append(derivative)

        return pd.DataFrame(data)

    def generate_aad236_collective_investments(self, num_syndicates=10):
        """
        Generate AAD 236 - Collective Investments Undertakings (S.06.03.01)
        Detailed fund holdings
        """
        data = []
        syndicates = random.sample(self.syndicates, min(num_syndicates, len(self.syndicates)))

        fund_types = [
            'Equity fund',
            'Bond fund',
            'Mixed fund',
            'Real estate fund',
            'Hedge fund',
            'Private equity fund',
            'Infrastructure fund'
        ]

        for syndicate in syndicates:
            # 5-15 fund holdings per syndicate
            num_funds = random.randint(5, 15)

            for i in range(num_funds):
                fund = {
                    'Syndicate': syndicate,
                    'Reporting_Date': self.annual_date_2024,
                    'Fund_ID': f'{syndicate}-FUND-{i+1:03d}',
                    'Fund_Name': f'Investment Fund {i+1}',
                    'Fund_Type': random.choice(fund_types),
                    'Fund_Manager': f'Manager_{random.randint(1, 50)}',
                    'Domicile': random.choice(self.countries),
                    'Currency': random.choice(self.currencies),
                    'Units_Held': np.random.uniform(1000, 100000),
                    'NAV_Per_Unit': np.random.uniform(50, 500),
                    'Total_Value': 0,  # Will calculate
                    'Look_Through_Available': random.choice(['Yes', 'No', 'Partial']),
                    'Underlying_Equities_Pct': np.random.uniform(0, 100),
                    'Underlying_Bonds_Pct': np.random.uniform(0, 100),
                    'Underlying_Property_Pct': np.random.uniform(0, 100),
                    'Underlying_Other_Pct': 0,  # Will calculate
                }

                fund['Total_Value'] = fund['Units_Held'] * fund['NAV_Per_Unit']

                # Ensure percentages sum to 100
                total_pct = (fund['Underlying_Equities_Pct'] +
                            fund['Underlying_Bonds_Pct'] +
                            fund['Underlying_Property_Pct'])
                if total_pct > 0:
                    fund['Underlying_Equities_Pct'] = fund['Underlying_Equities_Pct'] / total_pct * 100
                    fund['Underlying_Bonds_Pct'] = fund['Underlying_Bonds_Pct'] / total_pct * 100
                    fund['Underlying_Property_Pct'] = fund['Underlying_Property_Pct'] / total_pct * 100
                    fund['Underlying_Other_Pct'] = 0
                else:
                    fund['Underlying_Other_Pct'] = 100

                data.append(fund)

        return pd.DataFrame(data)

    def generate_aad237_structured_products(self, num_syndicates=10):
        """
        Generate AAD 237 - Structured Products (S.10.01.01)
        """
        data = []
        syndicates = random.sample(self.syndicates, min(num_syndicates, len(self.syndicates)))

        product_types = [
            'Credit-linked notes',
            'Equity-linked notes',
            'Structured bonds',
            'Capital protected notes',
            'Reverse convertibles'
        ]

        for syndicate in syndicates:
            # 2-8 structured products per syndicate
            num_products = random.randint(2, 8)

            for i in range(num_products):
                product = {
                    'Syndicate': syndicate,
                    'Reporting_Date': self.annual_date_2024,
                    'Product_ID': f'{syndicate}-STRUCT-{i+1:03d}',
                    'Product_Name': f'Structured Product {i+1}',
                    'Product_Type': random.choice(product_types),
                    'Issuer': f'Issuer_{random.randint(1, 100)}',
                    'Issuer_Rating': random.choice(['AAA', 'AA', 'A', 'BBB', 'BB']),
                    'Notional_Amount': np.random.uniform(5000000, 50000000),
                    'Currency': random.choice(self.currencies),
                    'Solvency_II_Value': np.random.uniform(4000000, 52000000),
                    'Underlying_Type': random.choice(['Equity Index', 'Credit Index', 'Commodity', 'Mixed']),
                    'Capital_Protection': np.random.uniform(80, 100),
                    'Participation_Rate': np.random.uniform(50, 150),
                    'Issue_Date': datetime(2020 + random.randint(0, 4), random.randint(1, 12), 1),
                    'Maturity_Date': datetime(2025 + random.randint(0, 10), random.randint(1, 12), 1),
                }

                data.append(product)

        return pd.DataFrame(data)

    def generate_aad238_securities_lending(self, num_syndicates=10):
        """
        Generate AAD 238 - Securities Lending and Repos (S.11.01.01)
        """
        data = []
        syndicates = random.sample(self.syndicates, min(num_syndicates, len(self.syndicates)))

        transaction_types = [
            'Securities lending',
            'Repo',
            'Reverse repo'
        ]

        for syndicate in syndicates:
            # 3-10 lending/repo transactions per syndicate
            num_transactions = random.randint(3, 10)

            for i in range(num_transactions):
                transaction = {
                    'Syndicate': syndicate,
                    'Reporting_Date': self.annual_date_2024,
                    'Transaction_ID': f'{syndicate}-SECLEND-{i+1:03d}',
                    'Transaction_Type': random.choice(transaction_types),
                    'Security_Type': random.choice(self.asset_classes),
                    'Security_Value': np.random.uniform(5000000, 50000000),
                    'Collateral_Received': np.random.uniform(5000000, 55000000),
                    'Collateral_Type': random.choice(['Cash', 'Government bonds', 'Corporate bonds', 'Equities']),
                    'Counterparty': f'SecLend_CP_{random.randint(1, 30)}',
                    'Counterparty_Rating': random.choice(['AAA', 'AA', 'A', 'BBB']),
                    'Start_Date': datetime(2024, random.randint(1, 12), random.randint(1, 28)),
                    'End_Date': datetime(2025, random.randint(1, 12), random.randint(1, 28)),
                    'Fee_Rate': np.random.uniform(0.1, 2.0),
                    'Income_Generated': 0,  # Will calculate
                }

                # Calculate income
                days = (transaction['End_Date'] - transaction['Start_Date']).days
                transaction['Income_Generated'] = (transaction['Security_Value'] *
                                                  transaction['Fee_Rate'] / 100 *
                                                  days / 365)

                data.append(transaction)

        return pd.DataFrame(data)

    # ========================================================================
    # ASB DATA GENERATION (Annual Solvency Balance Sheet - Claims Triangles)
    # ========================================================================

    def generate_asb_claims_triangle(self, num_syndicates=10, num_accident_years=10):
        """
        Generate ASB 245/246/247/248 - Claims Development Triangles
        Accident year claims development for gross, reinsurance, and net
        """
        data = []
        syndicates = random.sample(self.syndicates, min(num_syndicates, len(self.syndicates)))

        # Accident years: 2015-2024
        accident_years = list(range(2024 - num_accident_years + 1, 2025))

        for syndicate in syndicates:
            # Select 5-8 lines of business per syndicate
            selected_lobs = random.sample(self.lines_of_business[:12], random.randint(5, 8))

            for lob in selected_lobs:
                for accident_year in accident_years:
                    # Development years: 0 to 10
                    max_dev_year = 2024 - accident_year

                    for dev_year in range(max_dev_year + 1):
                        # Generate gross claims
                        if dev_year == 0:
                            # Initial estimate
                            ultimate = np.random.uniform(5000000, 50000000)
                            reported = ultimate * np.random.uniform(0.2, 0.4)
                            paid = reported * np.random.uniform(0, 0.3)
                        else:
                            # Claims develop over time
                            development_factor = 1 + (dev_year * 0.15) + np.random.uniform(-0.05, 0.05)
                            reported = ultimate * min(development_factor * 0.3, 1.0)
                            payment_factor = 0.3 + (dev_year * 0.1)
                            paid = reported * min(payment_factor, 0.95)

                        # Reinsurance recoverable (30-50% of gross)
                        reins_reported = reported * np.random.uniform(0.3, 0.5)
                        reins_paid = paid * np.random.uniform(0.3, 0.5)

                        # Net = Gross - Reinsurance
                        net_reported = reported - reins_reported
                        net_paid = paid - reins_paid

                        triangle = {
                            'Syndicate': syndicate,
                            'Reporting_Date': self.annual_date_2024,
                            'Line_of_Business': lob,
                            'Accident_Year': accident_year,
                            'Development_Year': dev_year,

                            # Gross amounts (ASB 245)
                            'Gross_Claims_Reported': reported,
                            'Gross_Claims_Paid': paid,
                            'Gross_Claims_Outstanding': reported - paid,

                            # Reinsurance share (ASB 246)
                            'Reins_Claims_Reported': reins_reported,
                            'Reins_Claims_Paid': reins_paid,
                            'Reins_Claims_Outstanding': reins_reported - reins_paid,

                            # Net amounts (ASB 247)
                            'Net_Claims_Reported': net_reported,
                            'Net_Claims_Paid': net_paid,
                            'Net_Claims_Outstanding': net_reported - net_paid,

                            # Ultimate estimates
                            'Gross_Ultimate_Estimate': ultimate if dev_year == max_dev_year else None,
                            'Net_Ultimate_Estimate': (ultimate - ultimate * 0.4) if dev_year == max_dev_year else None,
                        }

                        data.append(triangle)

        return pd.DataFrame(data)

    # ========================================================================
    # MASTER DATA GENERATION
    # ========================================================================

    def generate_all_quarterly_data(self, num_syndicates=15):
        """Generate all QSR (Quarterly) data"""
        from synthetic_data_generator import LloydsDataGenerator

        # Use original generator for QSR data
        qsr_gen = LloydsDataGenerator(seed=42)
        return qsr_gen.generate_all_data(num_syndicates)

    def generate_all_annual_aad_data(self, num_syndicates=15):
        """Generate all AAD (Annual Actuarial Data)"""
        return {
            'aad230_open_market_value': self.generate_aad230_open_market_value(num_syndicates),
            'aad233_off_balance_sheet': self.generate_aad233_off_balance_sheet(num_syndicates),
            'aad235_derivatives': self.generate_aad235_derivatives(num_syndicates),
            'aad236_collective_investments': self.generate_aad236_collective_investments(num_syndicates),
            'aad237_structured_products': self.generate_aad237_structured_products(num_syndicates),
            'aad238_securities_lending': self.generate_aad238_securities_lending(num_syndicates),
        }

    def generate_all_annual_asb_data(self, num_syndicates=15):
        """Generate all ASB (Annual Solvency Balance Sheet - Claims)"""
        return {
            'asb_claims_triangles': self.generate_asb_claims_triangle(num_syndicates, num_accident_years=10),
        }

    def generate_all_data(self, num_syndicates=15, include_quarterly=True, include_annual=True):
        """Generate all data for QSR and/or Annual returns"""
        all_data = {}

        if include_quarterly:
            print("Generating Quarterly (QSR) data...")
            all_data['qsr'] = self.generate_all_quarterly_data(num_syndicates)

        if include_annual:
            print("Generating Annual Actuarial Data (AAD)...")
            all_data['aad'] = self.generate_all_annual_aad_data(num_syndicates)

            print("Generating Annual Solvency Balance Sheet (ASB)...")
            all_data['asb'] = self.generate_all_annual_asb_data(num_syndicates)

        return all_data


def main():
    """Main function to generate and save all synthetic data"""
    generator = LloydsDataGeneratorExtended(seed=42)

    # Generate all data (both quarterly and annual)
    all_data = generator.generate_all_data(num_syndicates=15,
                                          include_quarterly=True,
                                          include_annual=True)

    output_dir = '../Data/'

    # Save QSR data
    if 'qsr' in all_data:
        print("\n" + "="*80)
        print("SAVING QSR (QUARTERLY) DATA")
        print("="*80)
        for dataset_name, df in all_data['qsr'].items():
            output_file = f'{output_dir}synthetic_{dataset_name}.csv'
            df.to_csv(output_file, index=False)
            print(f'✓ {dataset_name}: {len(df)} rows, {len(df.columns)} columns')

    # Save AAD data
    if 'aad' in all_data:
        print("\n" + "="*80)
        print("SAVING AAD (ANNUAL ACTUARIAL DATA)")
        print("="*80)
        for dataset_name, df in all_data['aad'].items():
            output_file = f'{output_dir}synthetic_{dataset_name}.csv'
            df.to_csv(output_file, index=False)
            print(f'✓ {dataset_name}: {len(df)} rows, {len(df.columns)} columns')

    # Save ASB data
    if 'asb' in all_data:
        print("\n" + "="*80)
        print("SAVING ASB (ANNUAL CLAIMS TRIANGLES)")
        print("="*80)
        for dataset_name, df in all_data['asb'].items():
            output_file = f'{output_dir}synthetic_{dataset_name}.csv'
            df.to_csv(output_file, index=False)
            print(f'✓ {dataset_name}: {len(df)} rows, {len(df.columns)} columns')

    print("\n" + "="*80)
    print("SYNTHETIC DATA GENERATION COMPLETE!")
    print("="*80)
    print(f"QSR datasets: {len(all_data.get('qsr', {}))}")
    print(f"AAD datasets: {len(all_data.get('aad', {}))}")
    print(f"ASB datasets: {len(all_data.get('asb', {}))}")


if __name__ == '__main__':
    main()
