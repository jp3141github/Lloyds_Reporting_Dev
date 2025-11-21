"""
Synthetic Lloyd's of London Data Generator for Solvency II AAD Returns
This script generates synthetic data that mimics Lloyd's of London insurance data
for use with Power BI and AAD return generation.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


class LloydsDataGenerator:
    """Generate synthetic Lloyd's of London insurance data"""

    def __init__(self, num_records=1000):
        self.num_records = num_records
        self.current_date = datetime(2024, 12, 31)

        # Lloyd's specific reference data
        self.portfolios = ['L', 'NL', 'RF']
        self.currencies = ['GBP', 'USD', 'EUR', 'JPY', 'CHF', 'AUD', 'CAD']
        self.countries = ['GB', 'US', 'DE', 'FR', 'IT', 'ES', 'NL', 'BE', 'IE', 'LU']
        self.asset_types = ['Government Bond', 'Corporate Bond', 'Equity', 'Property',
                           'Cash', 'Collective Investment', 'Derivatives']
        self.cic_codes = ['1', '2', '31', '32', '4', '5', '6', '71', '72', '8', '9']
        self.issuer_sectors = ['1', '2', '3', '4', '5', '6']
        self.rating_agencies = ['1', '2', '3', '4']
        self.external_ratings = ['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC']

    def generate_asset_id(self, id_type='ISIN'):
        """Generate synthetic asset identification codes"""
        if id_type == 'ISIN':
            # ISIN format: 2 letter country code + 9 alphanumeric + 1 check digit
            country = random.choice(self.countries)
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
            return f"{country}{code}{random.randint(0,9)}"
        elif id_type == 'SEDOL':
            # SEDOL format: 7 alphanumeric characters
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        elif id_type == 'CUSIP':
            # CUSIP format: 9 alphanumeric characters
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
        else:
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def generate_lei_code(self):
        """Generate synthetic Legal Entity Identifier"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

    def generate_dates(self):
        """Generate acquisition and maturity dates"""
        acquisition_date = self.current_date - timedelta(days=random.randint(30, 3650))
        maturity_date = acquisition_date + timedelta(days=random.randint(365, 10950))
        return acquisition_date, maturity_date

    def generate_aad230_assets(self):
        """Generate AAD230 - List of assets (S.06.02.01)"""
        data = []

        for i in range(self.num_records):
            portfolio = random.choice(self.portfolios)
            id_code_type = random.choice(['ISIN', 'SEDOL', 'CUSIP', 'BT'])
            currency = random.choice(self.currencies)
            cic = random.choice(self.cic_codes)

            acquisition_date, maturity_date = self.generate_dates()

            # Generate financial values
            quantity = random.randint(1000, 1000000)
            par_amount = quantity * random.uniform(0.8, 1.2)
            unit_price = random.uniform(50, 150)
            total_value = quantity * unit_price
            accrued_interest = total_value * random.uniform(0, 0.05)

            record = {
                'Portfolio': portfolio,
                'Fund_Number': random.randint(1, 50) if portfolio == 'RF' else None,
                'Asset_Held_Unit_Linked': random.choice(['Y', 'N']),
                'Asset_ID_Code': self.generate_asset_id(id_code_type),
                'Asset_ID_Code_Type': id_code_type,
                'Asset_Pledged_Collateral': random.choice(['Y', 'N']),
                'Item_Title': f"Asset {i+1} - {random.choice(self.asset_types)}",
                'Issuer_Name': f"Issuer {random.randint(1, 200)}",
                'Issuer_Code': self.generate_lei_code(),
                'Type_Issuer_Code': 'LEI',
                'Issuer_Sector': random.choice(self.issuer_sectors),
                'Issuer_Group': f"Group {random.randint(1, 50)}",
                'Issuer_Group_Code': self.generate_lei_code(),
                'Type_Issuer_Group_Code': 'LEI',
                'Issuer_Country': random.choice(self.countries),
                'Country_Custody': random.choice(self.countries),
                'Currency': currency,
                'CIC': cic,
                'Holdings_Related_Undertakings': random.choice(['Y', 'N']),
                'External_Rating': random.choice(self.external_ratings),
                'Nominated_ECAI': random.choice(self.rating_agencies),
                'Duration': round(random.uniform(0.5, 20), 2),
                'Quantity': quantity,
                'Par_Amount': round(par_amount, 2),
                'Unit_Solvency_II_Price': round(unit_price, 4),
                'Unit_Pct_Par_Amount_Price': round(random.uniform(95, 105), 4),
                'Valuation_Method': random.choice(['1', '2']),
                'Acquisition_Value': round(total_value * random.uniform(0.95, 1.05), 2),
                'Total_Solvency_II_Amount': round(total_value, 2),
                'Maturity_Date': maturity_date.strftime('%Y-%m-%d'),
                'Accrued_Interest': round(accrued_interest, 2),
                'Market_Value_Non_FIS': round(total_value * random.uniform(0.98, 1.02), 2),
                'Market_Value_FIS': round(total_value * random.uniform(0.98, 1.02), 2),
                'Issue_Type': random.choice(['1', '2', '3']),
                'Matching_Portfolio_Numbers': random.randint(1, 10),
                'Custodian': f"Custodian {random.randint(1, 20)}",
                'Infrastructure_Investment': random.choice(['Y', 'N']),
                'Credit_Quality_Step': random.randint(0, 6),
                'Internal_Rating': random.choice(['A', 'B', 'C', 'D']),
                'SCR_Calc_Approach_CIU': random.choice(['1', '2', '9']) if cic == '9' else None,
                'Asset_Liquidity': random.choice(['1', '2', '3']),
                'Fund_Redemption_Frequency': random.choice(['D', 'W', 'M', 'Q', 'A']) if cic == '9' else None,
                'Trust_Fund_Name': None
            }

            data.append(record)

        return pd.DataFrame(data)

    def generate_aad233_derivatives(self, num_derivatives=100):
        """Generate AAD233 - Open derivatives (S.08.01.01)"""
        data = []

        for i in range(num_derivatives):
            portfolio = random.choice(self.portfolios)
            derivative_type = random.choice(['FX Forward', 'Interest Rate Swap', 'Credit Default Swap',
                                            'Equity Option', 'Commodity Future'])

            acquisition_date, maturity_date = self.generate_dates()
            notional = random.uniform(1000000, 50000000)

            record = {
                'Portfolio': portfolio,
                'Fund_Number': random.randint(1, 50) if portfolio == 'RF' else None,
                'Derivatives_Unit_Linked': random.choice(['Y', 'N']),
                'Derivative_ID_Code': self.generate_asset_id('ISIN'),
                'Derivative_ID_Code_Type': 'ISIN',
                'Counterparty_Name': f"Counterparty {random.randint(1, 50)}",
                'Counterparty_Code': self.generate_lei_code(),
                'Type_Counterparty_Code': 'LEI',
                'External_Rating': random.choice(self.external_ratings),
                'Nominated_ECAI': random.choice(self.rating_agencies),
                'Counterparty_Group': f"CP Group {random.randint(1, 30)}",
                'Counterparty_Group_Code': self.generate_lei_code(),
                'Type_Counterparty_Group_Code': 'LEI',
                'Contract_Name': f"{derivative_type} Contract {i+1}",
                'Instrument_Underlying': random.choice(['Equity', 'Bond', 'Currency', 'Commodity', 'Index']),
                'Currency': random.choice(self.currencies),
                'CIC': random.choice(['A', 'B', 'C', 'D']),
                'Use_Derivative': random.choice(['MI', 'MA', 'EPM']),
                'Delta': round(random.uniform(-1, 1), 4),
                'Notional_Amount': round(notional, 2),
                'Buyer_Seller': random.choice(['B', 'S']),
                'Premium_Paid': round(notional * random.uniform(0, 0.05), 2),
                'Premium_Received': round(notional * random.uniform(0, 0.05), 2),
                'Number_Contracts': random.randint(1, 1000),
                'Contract_Size': round(random.uniform(100, 10000), 2),
                'Trigger_Value': round(notional * random.uniform(0.7, 1.3), 2),
                'Unwind_Trigger': random.choice(['B', 'F', 'R', 'N', 'M', 'O', 'NT']),
                'Max_Loss_Unwinding': round(notional * random.uniform(0.1, 0.3), 2),
                'Swap_Outflow_Amount': round(notional * random.uniform(0, 0.5), 2),
                'Swap_Inflow_Amount': round(notional * random.uniform(0, 0.5), 2),
                'Swap_Delivered_Currency': random.choice(self.currencies),
                'Swap_Received_Currency': random.choice(self.currencies),
                'Initial_Date': acquisition_date.strftime('%Y-%m-%d'),
                'Maturity_Date': maturity_date.strftime('%Y-%m-%d'),
                'Duration': round(random.uniform(0.1, 10), 2),
                'Valuation_Method': random.choice(['1', '2']),
                'Total_SII_Amount_Non_FIS': round(notional * random.uniform(-0.1, 0.1), 2),
                'Total_SII_Amount_FIS': round(notional * random.uniform(-0.1, 0.1), 2),
                'Solvency_II_Value': round(notional * random.uniform(-0.1, 0.1), 2),
                'Credit_Quality_Step': random.randint(0, 6),
                'Internal_Rating': random.choice(['A', 'B', 'C', 'D']),
                'Type_Code_Underlying': random.choice(['1', '2', '3']),
                'Trust_Fund_Name': None
            }

            data.append(record)

        return pd.DataFrame(data)

    def generate_aad235_income(self):
        """Generate AAD235 - Income/gains and losses (S.09.01.01)"""
        asset_categories = ['10', '20', '31', '32', '40', '50', '60', '71', '72', '80', '90', '95']
        data = []

        for category in asset_categories:
            record = {
                'Asset_Category': category,
                'Dividends': round(random.uniform(0, 5000000), 2),
                'Interest': round(random.uniform(0, 10000000), 2),
                'Rent': round(random.uniform(0, 2000000), 2),
                'Net_Gains_Losses': round(random.uniform(-5000000, 10000000), 2),
                'Unrealised_Gains_Losses': round(random.uniform(-3000000, 8000000), 2),
                'Portfolio': random.choice(self.portfolios),
                'Asset_Held_Unit_Linked': random.choice(['Y', 'N']),
                'Fund_Number': random.randint(1, 50) if random.random() > 0.7 else None
            }

            data.append(record)

        return pd.DataFrame(data)

    def generate_aad236_ciu_lookthrough(self, num_funds=50):
        """Generate AAD236 - Collective Investment Undertakings Look-through (S.06.03.01)"""
        data = []

        for i in range(num_funds):
            fund_value = random.uniform(5000000, 100000000)

            record = {
                'Investment_Fund_Code': self.generate_asset_id('ISIN'),
                'Investment_Fund_Code_Type': 'ISIN',
                'CIU_ID_Code': self.generate_asset_id('ISIN'),
                'CIU_ID_Code_Type': 'ISIN',
                'Item_Title': f"Fund {i+1} - {random.choice(['Equity Fund', 'Bond Fund', 'Mixed Fund', 'Property Fund'])}",
                'Issuer_Group': f"Fund Manager {random.randint(1, 30)}",
                'Issuer_Group_Code': self.generate_lei_code(),
                'Issuer_Group_Code_Type': 'LEI',
                'External_Rating': random.choice(self.external_ratings),
                'Rating_Agency': random.choice(self.rating_agencies),
                'Duration': round(random.uniform(1, 15), 2),
                'CIC': random.choice(['91', '92', '93', '94', '95', '96']),
                'Underlying_Asset_Category': random.choice(['1', '2', '3', '4', '5', '9']),
                'Country_Issue': random.choice(self.countries),
                'Currency': random.choice(self.currencies),
                'Total_SII_Amount_Non_FIS': round(fund_value * random.uniform(0.98, 1.02), 2),
                'Total_SII_Amount_FIS': round(fund_value * random.uniform(0.98, 1.02), 2),
                'Total_Solvency_II_Amount': round(fund_value, 2),
                'Issue_Type': random.choice(['1', '2', '3']),
                'Level_Look_Through': random.choice(['1', '2', '3', '9']),
                'Maturity_Date': (self.current_date + timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d'),
                'Fund_Number': random.randint(1, 50) if random.random() > 0.7 else None,
                'Notional_Amount': round(fund_value * random.uniform(0.95, 1.05), 2),
                'Asset_Liquidity': random.choice(['1', '2', '3']),
                'Trust_Fund_Name': None
            }

            data.append(record)

        return pd.DataFrame(data)

    def generate_aad237_loans_mortgages(self, num_loans=200):
        """Generate AAD237 - Loans and mortgages (S.10.01.01)"""
        data = []

        for i in range(num_loans):
            loan_amount = random.uniform(100000, 10000000)

            acquisition_date, maturity_date = self.generate_dates()

            record = {
                'Loan_ID': f"LOAN{random.randint(100000, 999999)}",
                'Loan_Type': random.choice(['1', '2', '3', '4']),
                'Portfolio': random.choice(self.portfolios),
                'Fund_Number': random.randint(1, 50) if random.random() > 0.7 else None,
                'Counterparty_Name': f"Borrower {random.randint(1, 500)}",
                'Counterparty_Code': self.generate_lei_code(),
                'Type_Counterparty_Code': 'LEI',
                'Country': random.choice(self.countries),
                'Currency': random.choice(self.currencies),
                'Original_Amount': round(loan_amount * random.uniform(1.1, 1.5), 2),
                'Outstanding_Amount': round(loan_amount, 2),
                'Interest_Rate': round(random.uniform(1, 8), 3),
                'Acquisition_Date': acquisition_date.strftime('%Y-%m-%d'),
                'Maturity_Date': maturity_date.strftime('%Y-%m-%d'),
                'Duration': round(random.uniform(1, 25), 2),
                'Collateral_Value': round(loan_amount * random.uniform(1.2, 2.0), 2),
                'Valuation_Method': random.choice(['1', '2']),
                'Total_Solvency_II_Amount': round(loan_amount * random.uniform(0.95, 1.05), 2),
                'Credit_Quality_Step': random.randint(0, 6),
                'Internal_Rating': random.choice(['A', 'B', 'C', 'D']),
                'Asset_Liquidity': random.choice(['1', '2', '3'])
            }

            data.append(record)

        return pd.DataFrame(data)

    def generate_aad238_property(self, num_properties=100):
        """Generate AAD238 - Property (S.11.01.01)"""
        data = []

        property_types = ['Office', 'Retail', 'Industrial', 'Residential', 'Mixed Use', 'Land']

        for i in range(num_properties):
            property_value = random.uniform(1000000, 50000000)

            record = {
                'Property_ID': f"PROP{random.randint(10000, 99999)}",
                'Portfolio': random.choice(self.portfolios),
                'Fund_Number': random.randint(1, 50) if random.random() > 0.7 else None,
                'Property_Type': random.choice(property_types),
                'Country': random.choice(self.countries),
                'Currency': random.choice(self.currencies),
                'Purchase_Date': (self.current_date - timedelta(days=random.randint(365, 7300))).strftime('%Y-%m-%d'),
                'Purchase_Price': round(property_value * random.uniform(0.7, 1.2), 2),
                'Valuation_Date': self.current_date.strftime('%Y-%m-%d'),
                'Current_Valuation': round(property_value, 2),
                'Rental_Income_Annual': round(property_value * random.uniform(0.03, 0.08), 2),
                'Occupancy_Rate': round(random.uniform(70, 100), 1),
                'Valuation_Method': random.choice(['1', '2']),
                'Total_Solvency_II_Amount': round(property_value, 2),
                'Asset_Liquidity': random.choice(['2', '3']),
                'Trust_Fund_Name': None
            }

            data.append(record)

        return pd.DataFrame(data)

    def generate_all_datasets(self):
        """Generate all AAD datasets and return as dictionary"""
        print("Generating synthetic Lloyd's data for AAD Returns...")

        datasets = {
            'AAD230_Assets': self.generate_aad230_assets(),
            'AAD233_Derivatives': self.generate_aad233_derivatives(),
            'AAD235_Income': self.generate_aad235_income(),
            'AAD236_CIU_Lookthrough': self.generate_aad236_ciu_lookthrough(),
            'AAD237_Loans_Mortgages': self.generate_aad237_loans_mortgages(),
            'AAD238_Property': self.generate_aad238_property()
        }

        print(f"Generated {len(datasets)} datasets:")
        for name, df in datasets.items():
            print(f"  - {name}: {len(df)} records, {len(df.columns)} columns")

        return datasets

    def save_datasets(self, output_dir='output'):
        """Save all datasets to CSV files"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        datasets = self.generate_all_datasets()

        for name, df in datasets.items():
            filepath = os.path.join(output_dir, f'{name}.csv')
            df.to_csv(filepath, index=False)
            print(f"Saved: {filepath}")

        print(f"\nAll datasets saved to '{output_dir}' directory")
        return datasets


def main():
    """Main execution function"""
    generator = LloydsDataGenerator(num_records=1000)
    datasets = generator.save_datasets(output_dir='synthetic_data')

    print("\nSample data from AAD230 (first 5 rows):")
    print(datasets['AAD230_Assets'].head())

    return datasets


if __name__ == "__main__":
    main()
