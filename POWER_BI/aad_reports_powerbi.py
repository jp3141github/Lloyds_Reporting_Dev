"""
AAD (Annual Actuarial Data) Reports Generator for Power BI
==========================================================
Generates Solvency II AAD reports for Lloyd's syndicates.
Compatible with Power BI as a Python data source.

Tables Generated:
- AAD230_Open_Market_Value: Open market value report (S.06.02.01)
- AAD230_Summary_By_Category: OMV Summary by asset category
- AAD233_Off_Balance_Sheet: Off-balance sheet items (S.08.01.01)
- AAD235_Derivatives: Derivatives report (S.09.01.01)
- AAD235_Derivatives_Summary: Derivatives risk summary
- AAD236_Collective_Investments: Collective investments (S.06.03.01)
- AAD237_Structured_Products: Structured products (S.10.01.01)
- AAD238_Securities_Lending: Securities lending (S.11.01.01)

Usage in Power BI:
1. Get Data > More > Python script
2. Copy and paste this script
3. Select the tables you need from the list
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
SYNDICATES = [2987, 33, 1183, 2791, 623, 4242, 5000, 1910, 2010, 2525]
REPORTING_DATE = '2024-12-31'
NUM_RECORDS_PER_SYNDICATE = 50

# Asset categories
ASSET_CATEGORIES = [
    'Government Bonds',
    'Corporate Bonds',
    'Equities - Listed',
    'Equities - Unlisted',
    'Collective Investments',
    'Property',
    'Loans and Mortgages',
    'Cash and Deposits',
    'Other Investments'
]

# Instrument types
INSTRUMENT_TYPES = [
    'Bond - Government',
    'Bond - Corporate IG',
    'Bond - Corporate HY',
    'Equity - Common Stock',
    'Equity - Preferred Stock',
    'Fund - Equity',
    'Fund - Fixed Income',
    'Fund - Mixed',
    'Property - Direct',
    'Property - Fund',
    'Derivative - Option',
    'Derivative - Future',
    'Derivative - Swap'
]

# Credit ratings
CREDIT_RATINGS = ['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-', 'BB+', 'BB', 'NR']

# Countries
COUNTRIES = ['UK', 'US', 'DE', 'FR', 'JP', 'CH', 'NL', 'BE', 'IE', 'LU']

# Derivative types
DERIVATIVE_TYPES = ['Interest Rate Swap', 'Currency Swap', 'Credit Default Swap', 'Equity Option', 'FX Forward', 'Futures']


def generate_aad230_open_market_value():
    """Generate AAD 230 - Open Market Value Report (S.06.02.01)"""
    data = []

    for syndicate in SYNDICATES:
        for i in range(NUM_RECORDS_PER_SYNDICATE):
            asset_category = random.choice(ASSET_CATEGORIES)
            instrument_type = random.choice(INSTRUMENT_TYPES)
            currency = random.choice(['GBP', 'USD', 'EUR'])

            solvency_value = random.randint(100000, 10000000)
            book_value = solvency_value * random.uniform(0.85, 1.15)

            data.append({
                'Syndicate': syndicate,
                'Reporting_Date': REPORTING_DATE,
                'Asset_ID': f'AST-{syndicate}-{i+1:05d}',
                'Instrument_Type': instrument_type,
                'Asset_Category': asset_category,
                'Issuer_Name': f'Issuer {random.randint(1, 100):03d}',
                'Issuer_Country': random.choice(COUNTRIES),
                'Currency': currency,
                'Quantity': random.randint(1000, 100000),
                'Unit_Price': round(random.uniform(50, 500), 2),
                'Total_Solvency_II_Value': round(solvency_value, 2),
                'Book_Value': round(book_value, 2),
                'Unrealized_Gain_Loss': round(solvency_value - book_value, 2),
                'Credit_Rating': random.choice(CREDIT_RATINGS),
                'Maturity_Date': (datetime.now() + timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d'),
                'CIC_Code': f'{random.randint(10, 99)}{random.randint(10, 99)}'
            })

    return pd.DataFrame(data)


def generate_aad230_summary_by_category(detailed_df):
    """Generate AAD 230 Summary by Asset Category"""
    summary = detailed_df.groupby(['Syndicate', 'Reporting_Date', 'Asset_Category']).agg({
        'Total_Solvency_II_Value': 'sum',
        'Book_Value': 'sum',
        'Asset_ID': 'count'
    }).reset_index()

    summary.rename(columns={'Asset_ID': 'Number_Of_Holdings'}, inplace=True)
    summary['Unrealized_Gain_Loss'] = summary['Total_Solvency_II_Value'] - summary['Book_Value']
    summary['Percentage_of_Total'] = summary.groupby('Syndicate')['Total_Solvency_II_Value'].transform(
        lambda x: round(x / x.sum() * 100, 2)
    )

    return summary


def generate_aad233_off_balance_sheet():
    """Generate AAD 233 - Off-Balance Sheet Items Report (S.08.01.01)"""
    data = []

    item_types = [
        'Guarantees Given',
        'Contingent Liabilities',
        'Collateral Held',
        'Letter of Credit',
        'Commitment to Subscribe',
        'Unfunded Pension Liability'
    ]

    for syndicate in SYNDICATES:
        for i in range(random.randint(5, 15)):
            max_exposure = random.randint(1000000, 50000000)
            prob_call = random.uniform(0.01, 0.3)
            expected_value = max_exposure * prob_call

            data.append({
                'Syndicate': syndicate,
                'Reporting_Date': REPORTING_DATE,
                'Item_ID': f'OBS-{syndicate}-{i+1:03d}',
                'Item_Type': random.choice(item_types),
                'Counterparty': f'Counterparty {random.randint(1, 50):03d}',
                'Maximum_Exposure': round(max_exposure, 2),
                'Probability_Of_Call': round(prob_call, 4),
                'Expected_Value': round(expected_value, 2),
                'Currency': random.choice(['GBP', 'USD', 'EUR']),
                'Maturity_Date': (datetime.now() + timedelta(days=random.randint(90, 1825))).strftime('%Y-%m-%d'),
                'Description': f'Off-balance sheet item {i+1}'
            })

    return pd.DataFrame(data)


def generate_aad235_derivatives():
    """Generate AAD 235 - Derivatives Report (S.09.01.01)"""
    data = []

    underlying_assets = ['Interest Rate', 'Currency', 'Equity Index', 'Credit', 'Commodity']
    purposes = ['Hedging', 'Efficient Portfolio Management', 'Speculation']

    for syndicate in SYNDICATES:
        for i in range(random.randint(10, 30)):
            notional = random.randint(5000000, 100000000)
            is_asset = random.random() > 0.4

            if is_asset:
                fair_value_asset = random.randint(100000, 5000000)
                fair_value_liability = 0
            else:
                fair_value_asset = 0
                fair_value_liability = random.randint(100000, 5000000)

            data.append({
                'Syndicate': syndicate,
                'Reporting_Date': REPORTING_DATE,
                'Contract_ID': f'DRV-{syndicate}-{i+1:04d}',
                'Derivative_Type': random.choice(DERIVATIVE_TYPES),
                'Underlying_Asset': random.choice(underlying_assets),
                'Counterparty': f'Bank {random.randint(1, 20):02d}',
                'Notional_Amount': notional,
                'Fair_Value_Asset': fair_value_asset,
                'Fair_Value_Liability': fair_value_liability,
                'Net_Fair_Value': fair_value_asset - fair_value_liability,
                'Delta': round(random.uniform(-1, 1), 4),
                'Gamma': round(random.uniform(0, 0.1), 6),
                'Vega': round(random.uniform(0, 100000), 2),
                'Purpose': random.choice(purposes),
                'Currency': random.choice(['GBP', 'USD', 'EUR']),
                'Maturity_Date': (datetime.now() + timedelta(days=random.randint(30, 1825))).strftime('%Y-%m-%d')
            })

    return pd.DataFrame(data)


def generate_aad235_derivatives_summary(derivatives_df):
    """Generate AAD 235 Derivatives Risk Summary"""
    summary = derivatives_df.groupby(['Syndicate', 'Reporting_Date', 'Derivative_Type']).agg({
        'Notional_Amount': 'sum',
        'Fair_Value_Asset': 'sum',
        'Fair_Value_Liability': 'sum',
        'Delta': 'sum',
        'Contract_ID': 'count'
    }).reset_index()

    summary.rename(columns={'Contract_ID': 'Number_Of_Contracts'}, inplace=True)
    summary['Net_Fair_Value'] = summary['Fair_Value_Asset'] - summary['Fair_Value_Liability']

    return summary


def generate_aad236_collective_investments():
    """Generate AAD 236 - Collective Investments Report (S.06.03.01)"""
    data = []

    fund_types = ['UCITS', 'AIF', 'ETF', 'Real Estate Fund', 'Private Equity Fund', 'Infrastructure Fund']
    managers = ['BlackRock', 'Vanguard', 'State Street', 'Fidelity', 'PIMCO', 'Schroders', 'M&G']

    for syndicate in SYNDICATES:
        for i in range(random.randint(8, 20)):
            total_value = random.randint(5000000, 50000000)
            look_through = random.random() > 0.3

            equities_pct = random.uniform(0, 60) if look_through else 0
            bonds_pct = random.uniform(0, 60) if look_through else 0
            other_pct = 100 - equities_pct - bonds_pct if look_through else 0

            data.append({
                'Syndicate': syndicate,
                'Reporting_Date': REPORTING_DATE,
                'Fund_ID': f'FND-{syndicate}-{i+1:03d}',
                'Fund_Name': f'Investment Fund {random.randint(1, 100):03d}',
                'Fund_Type': random.choice(fund_types),
                'Fund_Manager': random.choice(managers),
                'Currency': random.choice(['GBP', 'USD', 'EUR']),
                'Total_Value': total_value,
                'Number_Of_Units': random.randint(10000, 500000),
                'NAV_Per_Unit': round(total_value / random.randint(10000, 500000), 4),
                'Look_Through_Available': look_through,
                'Underlying_Equities_Pct': round(equities_pct, 2),
                'Underlying_Bonds_Pct': round(bonds_pct, 2),
                'Underlying_Other_Pct': round(other_pct, 2),
                'Domicile': random.choice(['LU', 'IE', 'UK', 'US', 'CH'])
            })

    return pd.DataFrame(data)


def generate_aad237_structured_products():
    """Generate AAD 237 - Structured Products Report (S.10.01.01)"""
    data = []

    product_types = [
        'Collateralised Loan Obligation',
        'Asset Backed Security',
        'Mortgage Backed Security',
        'Credit Linked Note',
        'Structured Note',
        'Capital Protected Note'
    ]

    for syndicate in SYNDICATES:
        for i in range(random.randint(3, 10)):
            notional = random.randint(5000000, 30000000)
            solvency_value = notional * random.uniform(0.85, 1.05)

            data.append({
                'Syndicate': syndicate,
                'Reporting_Date': REPORTING_DATE,
                'Product_ID': f'STP-{syndicate}-{i+1:03d}',
                'Product_Name': f'Structured Product {random.randint(1, 50):03d}',
                'Product_Type': random.choice(product_types),
                'Issuer': f'Issuer {random.randint(1, 30):03d}',
                'Currency': random.choice(['GBP', 'USD', 'EUR']),
                'Notional_Amount': notional,
                'Solvency_II_Value': round(solvency_value, 2),
                'Credit_Rating': random.choice(CREDIT_RATINGS),
                'Capital_Protection': round(random.uniform(0, 100), 2),
                'Attachment_Point': round(random.uniform(0, 10), 2),
                'Detachment_Point': round(random.uniform(10, 30), 2),
                'Maturity_Date': (datetime.now() + timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d')
            })

    return pd.DataFrame(data)


def generate_aad238_securities_lending():
    """Generate AAD 238 - Securities Lending Report (S.11.01.01)"""
    data = []

    transaction_types = ['Securities Lending', 'Securities Borrowing', 'Repo', 'Reverse Repo']
    security_types = ['Government Bond', 'Corporate Bond', 'Equity', 'Fund Units']
    collateral_types = ['Cash', 'Government Bond', 'Corporate Bond', 'Equity']

    for syndicate in SYNDICATES:
        for i in range(random.randint(5, 15)):
            security_value = random.randint(5000000, 50000000)
            collateral = security_value * random.uniform(1.02, 1.1)
            fee_rate = random.uniform(0.001, 0.005)
            income = security_value * fee_rate * random.uniform(0.5, 1)

            data.append({
                'Syndicate': syndicate,
                'Reporting_Date': REPORTING_DATE,
                'Transaction_ID': f'SLT-{syndicate}-{i+1:03d}',
                'Transaction_Type': random.choice(transaction_types),
                'Security_Type': random.choice(security_types),
                'Security_ID': f'SEC-{random.randint(10000, 99999)}',
                'Counterparty': f'Counterparty {random.randint(1, 30):03d}',
                'Currency': random.choice(['GBP', 'USD', 'EUR']),
                'Security_Value': security_value,
                'Collateral_Received': round(collateral, 2),
                'Collateral_Type': random.choice(collateral_types),
                'Haircut_Pct': round((collateral / security_value - 1) * 100, 2),
                'Fee_Rate': round(fee_rate * 100, 4),
                'Income_Generated': round(income, 2),
                'Start_Date': (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
                'Maturity_Date': (datetime.now() + timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
            })

    return pd.DataFrame(data)


# =============================================================================
# GENERATE ALL TABLES FOR POWER BI
# =============================================================================
print("Generating AAD Reports Data for Power BI...")
print("=" * 60)

# Generate AAD tables (these will be available in Power BI)
AAD230_Open_Market_Value = generate_aad230_open_market_value()
AAD230_Summary_By_Category = generate_aad230_summary_by_category(AAD230_Open_Market_Value)
AAD233_Off_Balance_Sheet = generate_aad233_off_balance_sheet()
AAD235_Derivatives = generate_aad235_derivatives()
AAD235_Derivatives_Summary = generate_aad235_derivatives_summary(AAD235_Derivatives)
AAD236_Collective_Investments = generate_aad236_collective_investments()
AAD237_Structured_Products = generate_aad237_structured_products()
AAD238_Securities_Lending = generate_aad238_securities_lending()

print(f"AAD230_Open_Market_Value: {len(AAD230_Open_Market_Value)} records")
print(f"AAD230_Summary_By_Category: {len(AAD230_Summary_By_Category)} records")
print(f"AAD233_Off_Balance_Sheet: {len(AAD233_Off_Balance_Sheet)} records")
print(f"AAD235_Derivatives: {len(AAD235_Derivatives)} records")
print(f"AAD235_Derivatives_Summary: {len(AAD235_Derivatives_Summary)} records")
print(f"AAD236_Collective_Investments: {len(AAD236_Collective_Investments)} records")
print(f"AAD237_Structured_Products: {len(AAD237_Structured_Products)} records")
print(f"AAD238_Securities_Lending: {len(AAD238_Securities_Lending)} records")
print("=" * 60)
print("AAD Reports data generated successfully!")
