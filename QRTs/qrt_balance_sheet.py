"""
PRA/BoE QRT Generator - Balance Sheet Templates (IR02)
======================================================
Actuarial-focused balance sheet templates for Solvency II reporting.

Templates:
- IR0201: Balance Sheet
- IR0202: Assets and Liabilities by Currency
- IR0203: Branch Balance Sheet Information
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List, Optional
import string

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================================================
# Configuration
# ============================================================================

UNDERTAKINGS = [
    {'lei': '549300ABCDEF123456G7', 'name': "Lloyd's Syndicate 2987", 'type': 'Non-Life'},
    {'lei': '549300HIJKLM789012N3', 'name': "Lloyd's Syndicate 33", 'type': 'Non-Life'},
    {'lei': '549300OPQRS456789T0', 'name': "Lloyd's Syndicate 1183", 'type': 'Non-Life'},
    {'lei': '549300UVWXY012345Z1', 'name': "Lloyd's Syndicate 2791", 'type': 'Composite'},
    {'lei': '549300ABCDE678901F2', 'name': "Lloyd's Syndicate 623", 'type': 'Non-Life'},
]

REPORTING_DATE = '2024-12-31'
PREVIOUS_REPORTING_DATE = '2023-12-31'
CURRENCIES = ['GBP', 'USD', 'EUR', 'JPY', 'CHF', 'AUD', 'CAD']
COUNTRIES = ['GB', 'US', 'DE', 'FR', 'JP', 'CH', 'AU', 'CA', 'IE', 'LU', 'NL', 'IT', 'ES']

NON_LIFE_LOB = [
    'Medical expense insurance',
    'Income protection insurance',
    "Workers' compensation insurance",
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

LIFE_LOB = [
    'Insurance with profit participation',
    'Index-linked and unit-linked insurance',
    'Other life insurance',
    'Annuities stemming from non-life contracts',
    'Health insurance (SLT)',
    'Life reinsurance'
]

# ============================================================================
# Helper Functions
# ============================================================================

def generate_lei():
    """Generate a random LEI code"""
    return '549300' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))

def random_amount(min_val: float, max_val: float, precision: int = 2) -> float:
    """Generate a random monetary amount"""
    return round(np.random.uniform(min_val, max_val), precision)

def random_percentage(min_val: float = 0, max_val: float = 100) -> float:
    """Generate a random percentage"""
    return round(np.random.uniform(min_val, max_val), 4)


# ============================================================================
# IR0201 - Balance Sheet
# ============================================================================

def generate_ir0201_balance_sheet():
    """
    IR0201 - Balance Sheet
    Solvency II balance sheet with assets and liabilities at fair value.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        # Assets
        total_investments = random_amount(500_000_000, 2_000_000_000)

        row = {
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # Assets
            'Goodwill': random_amount(0, 5_000_000),
            'Deferred_Acquisition_Costs': random_amount(10_000_000, 50_000_000),
            'Intangible_Assets': random_amount(1_000_000, 20_000_000),
            'Deferred_Tax_Assets': random_amount(5_000_000, 30_000_000),
            'Pension_Benefit_Surplus': random_amount(0, 10_000_000),
            'Property_Plant_Equipment': random_amount(5_000_000, 50_000_000),
            'Investments_Property': random_amount(20_000_000, 100_000_000),
            'Holdings_Related_Undertakings': random_amount(0, 50_000_000),
            'Equities_Listed': random_amount(50_000_000, 200_000_000),
            'Equities_Unlisted': random_amount(10_000_000, 50_000_000),
            'Bonds_Government': random_amount(100_000_000, 500_000_000),
            'Bonds_Corporate': random_amount(100_000_000, 400_000_000),
            'Bonds_Structured_Notes': random_amount(20_000_000, 100_000_000),
            'Bonds_Collateralised': random_amount(10_000_000, 50_000_000),
            'Collective_Investment_Undertakings': random_amount(50_000_000, 200_000_000),
            'Derivatives': random_amount(5_000_000, 50_000_000),
            'Deposits_Other_Than_Cash': random_amount(10_000_000, 50_000_000),
            'Other_Investments': random_amount(5_000_000, 30_000_000),
            'Assets_Index_Unit_Linked': random_amount(0, 100_000_000),
            'Loans_And_Mortgages': random_amount(10_000_000, 50_000_000),
            'Reinsurance_Recoverables_Non_Life': random_amount(50_000_000, 200_000_000),
            'Reinsurance_Recoverables_Life': random_amount(10_000_000, 50_000_000),
            'Reinsurance_Recoverables_Health': random_amount(5_000_000, 20_000_000),
            'Deposits_To_Cedants': random_amount(5_000_000, 30_000_000),
            'Insurance_Receivables': random_amount(50_000_000, 150_000_000),
            'Reinsurance_Receivables': random_amount(20_000_000, 80_000_000),
            'Receivables_Trade': random_amount(5_000_000, 30_000_000),
            'Own_Shares': random_amount(0, 5_000_000),
            'Amounts_Due_Own_Fund_Items': random_amount(0, 10_000_000),
            'Cash_And_Cash_Equivalents': random_amount(20_000_000, 100_000_000),
            'Any_Other_Assets': random_amount(5_000_000, 30_000_000),
            # Liabilities
            'Technical_Provisions_Non_Life': random_amount(200_000_000, 800_000_000),
            'Technical_Provisions_Non_Life_Gross': random_amount(250_000_000, 900_000_000),
            'Technical_Provisions_Non_Life_RM': random_amount(20_000_000, 80_000_000),
            'Technical_Provisions_Life': random_amount(50_000_000, 300_000_000),
            'Technical_Provisions_Life_Gross': random_amount(60_000_000, 350_000_000),
            'Technical_Provisions_Life_RM': random_amount(5_000_000, 30_000_000),
            'Technical_Provisions_Index_Linked': random_amount(0, 100_000_000),
            'Technical_Provisions_Health': random_amount(10_000_000, 50_000_000),
            'Contingent_Liabilities': random_amount(0, 20_000_000),
            'Provisions_Other_Than_TP': random_amount(5_000_000, 30_000_000),
            'Pension_Benefit_Obligations': random_amount(10_000_000, 50_000_000),
            'Deposits_From_Reinsurers': random_amount(10_000_000, 50_000_000),
            'Deferred_Tax_Liabilities': random_amount(5_000_000, 40_000_000),
            'Derivatives_Liabilities': random_amount(2_000_000, 20_000_000),
            'Debts_Owed_Credit_Institutions': random_amount(0, 50_000_000),
            'Financial_Liabilities_Other': random_amount(5_000_000, 30_000_000),
            'Insurance_Payables': random_amount(20_000_000, 80_000_000),
            'Reinsurance_Payables': random_amount(10_000_000, 50_000_000),
            'Payables_Trade': random_amount(10_000_000, 40_000_000),
            'Subordinated_Liabilities': random_amount(0, 100_000_000),
            'Any_Other_Liabilities': random_amount(5_000_000, 30_000_000),
        }

        # Calculate totals
        asset_cols = [c for c in row.keys() if c not in ['LEI', 'Undertaking_Name', 'Reporting_Date']
                      and not c.startswith('Technical_Provisions') and not c.startswith('Contingent')
                      and not c.startswith('Provisions_Other') and not c.startswith('Pension_Benefit_Obligations')
                      and not c.startswith('Deposits_From') and not c.startswith('Deferred_Tax_Liabilities')
                      and not c.startswith('Derivatives_Liabilities') and not c.startswith('Debts_')
                      and not c.startswith('Financial_Liabilities') and not c.startswith('Insurance_Payables')
                      and not c.startswith('Reinsurance_Payables') and not c.startswith('Payables_')
                      and not c.startswith('Subordinated') and not c.startswith('Any_Other_Liabilities')]

        row['Total_Assets'] = sum(row[c] for c in asset_cols if c in row)

        liability_cols = ['Technical_Provisions_Non_Life', 'Technical_Provisions_Life',
                          'Technical_Provisions_Index_Linked', 'Technical_Provisions_Health',
                          'Contingent_Liabilities', 'Provisions_Other_Than_TP', 'Pension_Benefit_Obligations',
                          'Deposits_From_Reinsurers', 'Deferred_Tax_Liabilities', 'Derivatives_Liabilities',
                          'Debts_Owed_Credit_Institutions', 'Financial_Liabilities_Other', 'Insurance_Payables',
                          'Reinsurance_Payables', 'Payables_Trade', 'Subordinated_Liabilities', 'Any_Other_Liabilities']

        row['Total_Liabilities'] = sum(row.get(c, 0) for c in liability_cols)
        row['Excess_Assets_Over_Liabilities'] = row['Total_Assets'] - row['Total_Liabilities']

        data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR0202 - Assets and Liabilities by Currency
# ============================================================================

def generate_ir0202_assets_liabilities_by_currency():
    """
    IR0202 - Assets and Liabilities by Currency
    Breakdown of balance sheet items by reporting currency.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        total_assets = random_amount(800_000_000, 2_500_000_000)
        total_liabilities = random_amount(600_000_000, 2_000_000_000)

        # Distribute across currencies
        currency_weights = {
            'GBP': 0.40,
            'USD': 0.30,
            'EUR': 0.15,
            'JPY': 0.05,
            'CHF': 0.04,
            'AUD': 0.03,
            'CAD': 0.03
        }

        for currency, weight in currency_weights.items():
            currency_assets = total_assets * weight * np.random.uniform(0.8, 1.2)
            currency_liabilities = total_liabilities * weight * np.random.uniform(0.8, 1.2)

            row = {
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Currency': currency,
                'Currency_Weight': round(weight * 100, 2),
                'Investments_Bonds': random_amount(currency_assets * 0.3, currency_assets * 0.5),
                'Investments_Equity': random_amount(currency_assets * 0.1, currency_assets * 0.2),
                'Investments_Property': random_amount(currency_assets * 0.02, currency_assets * 0.08),
                'Investments_CIU': random_amount(currency_assets * 0.05, currency_assets * 0.15),
                'Investments_Derivatives': random_amount(currency_assets * 0.01, currency_assets * 0.05),
                'Investments_Other': random_amount(currency_assets * 0.02, currency_assets * 0.08),
                'Reinsurance_Recoverables': random_amount(currency_assets * 0.05, currency_assets * 0.15),
                'Cash_And_Equivalents': random_amount(currency_assets * 0.02, currency_assets * 0.08),
                'Other_Assets': random_amount(currency_assets * 0.03, currency_assets * 0.1),
                'Total_Assets': round(currency_assets, 2),
                'TP_Non_Life': random_amount(currency_liabilities * 0.4, currency_liabilities * 0.6),
                'TP_Life': random_amount(currency_liabilities * 0.1, currency_liabilities * 0.2),
                'TP_Health': random_amount(currency_liabilities * 0.02, currency_liabilities * 0.08),
                'Financial_Liabilities': random_amount(currency_liabilities * 0.05, currency_liabilities * 0.15),
                'Other_Liabilities': random_amount(currency_liabilities * 0.05, currency_liabilities * 0.15),
                'Total_Liabilities': round(currency_liabilities, 2),
                'Net_Position': round(currency_assets - currency_liabilities, 2),
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR0203 - Branch Balance Sheet Information
# ============================================================================

def generate_ir0203_branch_balance_sheet():
    """
    IR0203 - Additional Branch Balance Sheet Information
    Balance sheet breakdown by branch/jurisdiction.
    """
    data = []

    branches = [
        ('GB', 'United Kingdom - Head Office'),
        ('US', 'United States Branch'),
        ('DE', 'Germany Branch'),
        ('FR', 'France Branch'),
        ('CH', 'Switzerland Branch'),
    ]

    for undertaking in UNDERTAKINGS:
        for country_code, branch_name in branches:
            weight = 0.6 if country_code == 'GB' else np.random.uniform(0.05, 0.15)

            row = {
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Branch_Country': country_code,
                'Branch_Name': branch_name,
                'Branch_LEI': generate_lei() if country_code != 'GB' else undertaking['lei'],
                'Assets_Investments': random_amount(50_000_000 * weight, 500_000_000 * weight),
                'Assets_Reinsurance_Recoverables': random_amount(10_000_000 * weight, 100_000_000 * weight),
                'Assets_Receivables': random_amount(5_000_000 * weight, 50_000_000 * weight),
                'Assets_Cash': random_amount(2_000_000 * weight, 30_000_000 * weight),
                'Assets_Other': random_amount(1_000_000 * weight, 20_000_000 * weight),
                'Liabilities_TP': random_amount(30_000_000 * weight, 400_000_000 * weight),
                'Liabilities_Other': random_amount(5_000_000 * weight, 50_000_000 * weight),
                'Own_Funds_Allocated': random_amount(20_000_000 * weight, 150_000_000 * weight),
                'SCR_Allocated': random_amount(15_000_000 * weight, 120_000_000 * weight),
                'MCR_Allocated': random_amount(5_000_000 * weight, 40_000_000 * weight),
            }

            row['Total_Assets'] = (row['Assets_Investments'] + row['Assets_Reinsurance_Recoverables'] +
                                   row['Assets_Receivables'] + row['Assets_Cash'] + row['Assets_Other'])
            row['Total_Liabilities'] = row['Liabilities_TP'] + row['Liabilities_Other']

            data.append(row)

    return pd.DataFrame(data)


# Export all functions
__all__ = [
    'generate_ir0201_balance_sheet',
    'generate_ir0202_assets_liabilities_by_currency',
    'generate_ir0203_branch_balance_sheet',
    'UNDERTAKINGS',
    'REPORTING_DATE',
    'CURRENCIES',
    'COUNTRIES',
    'NON_LIFE_LOB',
    'LIFE_LOB',
    'generate_lei',
    'random_amount',
    'random_percentage',
]
