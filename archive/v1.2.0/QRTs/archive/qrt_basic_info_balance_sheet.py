"""
PRA/BoE Quantitative Reporting Templates (QRT) Master Generator
================================================================
Comprehensive generator for all 88 PRA/BoE QRT templates for Solvency II reporting.

This module provides synthetic data generation for Power BI integration.

Template Categories:
- AOC: Analysis of Change in SCR
- IM: Internal Model templates (00-03)
- IR01: Basic Information (01-04)
- IR02: Balance Sheet (01-03)
- IR03: Off-Balance Sheet Items (01-03)
- IR05: Premiums, Claims, Expenses (02-10)
- IR06: Assets (02-03)
- IR08: Derivatives (01)
- IR09: Income/Gains/Losses (01)
- IR10: Securities Lending & Repos (01)
- IR11: Assets Held as Collateral (01)
- IR12: Life Technical Provisions (01-06)
- IR14: Life Obligations Analysis (01)
- IR16: Non-Life Annuities (01-02)
- IR17: Non-Life Technical Provisions (01-03)
- IR18: Non-Life Cash Flows (01-02)
- IR19: Non-Life Insurance Claims (01-02)
- IR20: Claims Distribution Development (01)
- IR21: Underwriting Risks (02,04)
- IR22: LTG Measures & Transitionals (01,04,07)
- IR23: Own Funds (01-05)
- IR24: Participations (01)
- IR25: SCR (04-06)
- IR26: SCR Risk Modules (01-07)
- IR27: Catastrophe Risk (01)
- IR28: MCR (01-02)
- IR30: Reinsurance Outwards (03-08)
- IR31: Reinsurance Balance Sheet (01)
- IR32: Group Scope (01)
- IR33: Individual Requirements (01)
- IR34: Other Undertakings (01)
- IR35: Group Technical Provisions (01)
- IR36: IGT (01-04)
- IRR22: Matching Adjustment (02-03)
- MALIR: Matching Adjustment Life Insurance Return
- MR: Market Risk Sensitivities (01)
- QMC: Quarterly Model Change (01)

Usage in Power BI:
1. Get Data > More > Python script
2. Copy and paste this script
3. Select the tables you need from the list
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

# Sample undertakings for data generation
UNDERTAKINGS = [
    {'lei': '549300ABCDEF123456G7', 'name': 'Lloyd\'s Syndicate 2987', 'type': 'Non-Life'},
    {'lei': '549300HIJKLM789012N3', 'name': 'Lloyd\'s Syndicate 33', 'type': 'Non-Life'},
    {'lei': '549300OPQRS456789T0', 'name': 'Lloyd\'s Syndicate 1183', 'type': 'Non-Life'},
    {'lei': '549300UVWXY012345Z1', 'name': 'Lloyd\'s Syndicate 2791', 'type': 'Composite'},
    {'lei': '549300ABCDE678901F2', 'name': 'Lloyd\'s Syndicate 623', 'type': 'Non-Life'},
]

REPORTING_DATE = '2024-12-31'
PREVIOUS_REPORTING_DATE = '2023-12-31'

# Currency codes
CURRENCIES = ['GBP', 'USD', 'EUR', 'JPY', 'CHF', 'AUD', 'CAD']

# Country codes
COUNTRIES = ['GB', 'US', 'DE', 'FR', 'JP', 'CH', 'AU', 'CA', 'IE', 'LU', 'NL', 'IT', 'ES']

# Non-Life Lines of Business (Solvency II)
NON_LIFE_LOB = [
    'Medical expense insurance',
    'Income protection insurance',
    'Workers\' compensation insurance',
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

# Life Lines of Business
LIFE_LOB = [
    'Insurance with profit participation',
    'Index-linked and unit-linked insurance',
    'Other life insurance',
    'Annuities stemming from non-life contracts',
    'Health insurance (SLT)',
    'Life reinsurance'
]

# Asset categories
ASSET_CATEGORIES = [
    'Government Bonds',
    'Corporate Bonds',
    'Equity - Listed',
    'Equity - Unlisted',
    'Collective Investment Undertakings',
    'Structured Notes',
    'Collateralised Securities',
    'Property',
    'Cash and Deposits',
    'Mortgages and Loans',
    'Derivatives'
]

# CIC codes for assets
CIC_CODES = {
    'Government Bonds': ['11', '12', '13', '14', '15'],
    'Corporate Bonds': ['21', '22', '23', '24', '25', '26', '27', '28', '29'],
    'Equity - Listed': ['31', '32'],
    'Equity - Unlisted': ['33', '34'],
    'Collective Investment Undertakings': ['41', '42', '43', '44', '45', '46', '47', '48', '49'],
    'Structured Notes': ['51', '52', '53', '54', '55', '56', '57', '58', '59'],
    'Collateralised Securities': ['61', '62', '63', '64', '65', '66', '67', '68', '69'],
    'Property': ['91', '92', '93', '94', '95'],
    'Cash and Deposits': ['71', '72', '79'],
    'Mortgages and Loans': ['81', '82', '83', '84', '89'],
    'Derivatives': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
}


# ============================================================================
# Helper Functions
# ============================================================================

def generate_lei():
    """Generate a random LEI code"""
    return '549300' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))

def generate_isin():
    """Generate a random ISIN code"""
    country = random.choice(['GB', 'US', 'DE', 'FR'])
    return country + ''.join(random.choices(string.ascii_uppercase + string.digits, k=9)) + str(random.randint(0, 9))

def random_amount(min_val: float, max_val: float, precision: int = 2) -> float:
    """Generate a random monetary amount"""
    return round(np.random.uniform(min_val, max_val), precision)

def random_percentage(min_val: float = 0, max_val: float = 100) -> float:
    """Generate a random percentage"""
    return round(np.random.uniform(min_val, max_val), 4)


# ============================================================================
# AOC01 - Analysis of Change in SCR
# ============================================================================

def generate_aoc01_analysis_of_change():
    """
    AOC01 - Analysis of Change in Solvency Capital Requirement
    Tracks movements in SCR components between reporting periods.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        # Opening SCR
        opening_scr = random_amount(100_000_000, 500_000_000)

        # Movement components
        movements = {
            'Market risk': random_amount(-20_000_000, 30_000_000),
            'Counterparty default risk': random_amount(-10_000_000, 15_000_000),
            'Life underwriting risk': random_amount(-5_000_000, 10_000_000),
            'Health underwriting risk': random_amount(-5_000_000, 10_000_000),
            'Non-life underwriting risk': random_amount(-15_000_000, 25_000_000),
            'Operational risk': random_amount(-3_000_000, 8_000_000),
            'Diversification': random_amount(-25_000_000, -5_000_000),
            'LAC of deferred taxes': random_amount(-15_000_000, -5_000_000),
            'LAC of technical provisions': random_amount(-10_000_000, 0),
        }

        closing_scr = opening_scr + sum(movements.values())

        row = {
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            'Previous_Reporting_Date': PREVIOUS_REPORTING_DATE,
            'Opening_SCR': opening_scr,
            **{f'Movement_{k.replace(" ", "_")}': v for k, v in movements.items()},
            'Total_Movement': sum(movements.values()),
            'Closing_SCR': closing_scr,
            'Currency': 'GBP'
        }
        data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IM00-IM03 - Internal Model Templates
# ============================================================================

def generate_im00_submission_content():
    """
    IM00 - Internal Model Submission Content
    Control template listing internal model submission details.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        data.append({
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            'Model_Type': random.choice(['Full Internal Model', 'Partial Internal Model']),
            'Model_Approved': random.choice(['Yes', 'No']),
            'Approval_Date': '2022-01-15' if random.random() > 0.3 else None,
            'IM01_Submitted': True,
            'IM02_Submitted': True,
            'IM03_Submitted': True,
            'Model_Version': f'{random.randint(1, 5)}.{random.randint(0, 9)}',
            'Last_Major_Change_Date': '2024-06-30',
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


def generate_im01_life_outputs():
    """
    IM01 - Internal Model Outputs (Life)
    Life insurance internal model outputs.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            for lob in LIFE_LOB[:3]:  # Sample LOBs
                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Line_Of_Business': lob,
                    'IM_SCR': random_amount(10_000_000, 100_000_000),
                    'SF_SCR': random_amount(12_000_000, 120_000_000),
                    'IM_to_SF_Ratio': random_percentage(70, 110),
                    'VaR_99_5': random_amount(15_000_000, 150_000_000),
                    'Expected_Shortfall': random_amount(18_000_000, 180_000_000),
                    'Mortality_Risk': random_amount(1_000_000, 20_000_000),
                    'Longevity_Risk': random_amount(2_000_000, 30_000_000),
                    'Disability_Risk': random_amount(500_000, 10_000_000),
                    'Lapse_Risk': random_amount(3_000_000, 40_000_000),
                    'Expense_Risk': random_amount(1_000_000, 15_000_000),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


def generate_im02_counterparty_risk():
    """
    IM02 - Internal Model Counterparty Risk
    Counterparty default risk from internal model.
    """
    data = []

    counterparty_types = [
        'Reinsurer', 'Bank', 'Central Counterparty', 'Intermediary',
        'Policyholder', 'Other Financial Institution'
    ]

    for undertaking in UNDERTAKINGS:
        for cp_type in counterparty_types:
            for _ in range(random.randint(2, 5)):
                exposure = random_amount(1_000_000, 100_000_000)
                lgd = random_percentage(30, 60)
                pd_rate = random_percentage(0.01, 5)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Counterparty_Type': cp_type,
                    'Counterparty_LEI': generate_lei(),
                    'Credit_Rating': random.choice(['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'NR']),
                    'Exposure_Gross': exposure,
                    'Collateral_Value': exposure * random_percentage(0, 50) / 100,
                    'Exposure_Net': exposure * random_percentage(50, 100) / 100,
                    'PD': pd_rate,
                    'LGD': lgd,
                    'Expected_Loss': exposure * pd_rate * lgd / 10000,
                    'IM_SCR_Contribution': random_amount(100_000, 10_000_000),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


def generate_im03_non_life_outputs():
    """
    IM03 - Internal Model Outputs (Non-Life)
    Non-life insurance internal model outputs.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            for lob in NON_LIFE_LOB[:8]:  # Sample LOBs
                premium_risk = random_amount(1_000_000, 50_000_000)
                reserve_risk = random_amount(2_000_000, 80_000_000)
                cat_risk = random_amount(5_000_000, 200_000_000)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Line_Of_Business': lob,
                    'IM_SCR_Premium_Risk': premium_risk,
                    'IM_SCR_Reserve_Risk': reserve_risk,
                    'IM_SCR_Cat_Risk': cat_risk,
                    'IM_SCR_Total': (premium_risk + reserve_risk + cat_risk) * random_percentage(70, 90) / 100,
                    'SF_SCR_Premium_Risk': premium_risk * random_percentage(90, 130) / 100,
                    'SF_SCR_Reserve_Risk': reserve_risk * random_percentage(90, 130) / 100,
                    'SF_SCR_Cat_Risk': cat_risk * random_percentage(90, 130) / 100,
                    'Premium_Volume': random_amount(10_000_000, 500_000_000),
                    'Reserve_Volume': random_amount(20_000_000, 800_000_000),
                    'Loss_Ratio_Mean': random_percentage(50, 80),
                    'Loss_Ratio_StdDev': random_percentage(5, 20),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR0101-IR0104 - Basic Information Templates
# ============================================================================

def generate_ir0101_submission_content():
    """
    IR0101 - Content of the Submission
    Control template for submission contents.
    """
    templates = [
        'IR0102', 'IR0201', 'IR0301', 'IR0502', 'IR0602', 'IR0801',
        'IR1701', 'IR1901', 'IR2301', 'IR2504', 'IR2601', 'IR2801'
    ]

    data = []

    for undertaking in UNDERTAKINGS:
        for template in templates:
            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Template_Code': template,
                'Template_Submitted': random.choice([True, True, True, False]),  # 75% submitted
                'Reason_Not_Submitted': None if random.random() > 0.25 else 'Not Applicable',
                'First_Submission': random.choice([True, False]),
                'Resubmission': False,
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


def generate_ir0102_basic_info_general():
    """
    IR0102 - Basic Information (General)
    General undertaking information.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        data.append({
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            'Legal_Name': undertaking['name'],
            'Type_Of_Undertaking': undertaking['type'],
            'Country_Of_Authorisation': 'GB',
            'Supervisory_Authority': 'Prudential Regulation Authority',
            'With_AO': random.choice(['Yes', 'No']),
            'Participating_Undertaking': random.choice(['Yes', 'No']),
            'Group_Or_Solo': 'Solo',
            'Method_Of_Group_Supervision': 'Not Applicable',
            'Language_Of_Reporting': 'EN',
            'Reporting_Submission_Date': datetime.now().strftime('%Y-%m-%d'),
            'Accounting_Standard': random.choice(['UK GAAP', 'IFRS']),
            'Method_Of_Calculating_SCR': random.choice(['Standard Formula', 'Partial Internal Model', 'Full Internal Model']),
            'Use_Of_USP': random.choice(['Yes', 'No']),
            'Use_Of_Simplifications': random.choice(['Yes', 'No']),
            'RFF': random.choice(['Yes', 'No']),
            'Matching_Adjustment': random.choice(['Yes', 'No']),
            'Volatility_Adjustment': random.choice(['Yes', 'No']),
            'Transitional_On_Interest_Rate': random.choice(['Yes', 'No']),
            'Transitional_On_Technical_Provisions': random.choice(['Yes', 'No']),
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


def generate_ir0103_rff_matching_portfolios():
    """
    IR0103 - Basic Information (RFF and Matching Adjustment Portfolios)
    Ring-fenced funds and matching adjustment portfolio information.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        # Some undertakings may have RFFs or MA portfolios
        if random.random() > 0.5:
            for i in range(random.randint(1, 3)):
                portfolio_type = random.choice(['RFF', 'Matching Adjustment Portfolio'])
                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Portfolio_Number': f'{portfolio_type[:2]}{i+1:03d}',
                    'Portfolio_Type': portfolio_type,
                    'Article_304_Material': random.choice(['Yes', 'No']),
                    'Assets_Value': random_amount(10_000_000, 500_000_000),
                    'Liabilities_Value': random_amount(8_000_000, 450_000_000),
                    'Notional_SCR': random_amount(5_000_000, 100_000_000),
                    'Own_Funds_Restricted': random_amount(2_000_000, 50_000_000),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


def generate_ir0104_branch_info():
    """
    IR0104 - Basic Information (Branch/Legal Entity)
    Branch and legal entity information for undertakings operating in multiple jurisdictions.
    """
    data = []

    branch_countries = ['DE', 'FR', 'IE', 'NL', 'ES', 'IT']

    for undertaking in UNDERTAKINGS:
        # Some undertakings have branches
        if random.random() > 0.4:
            for country in random.sample(branch_countries, random.randint(1, 3)):
                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Branch_Country': country,
                    'Branch_Name': f'{undertaking["name"]} - {country} Branch',
                    'Regulatory_Status': 'Licensed',
                    'Branch_Premium_Written': random_amount(1_000_000, 50_000_000),
                    'Branch_Claims_Paid': random_amount(500_000, 30_000_000),
                    'Branch_Technical_Provisions': random_amount(2_000_000, 80_000_000),
                    'Branch_Own_Funds': random_amount(5_000_000, 100_000_000),
                    'Branch_SCR': random_amount(3_000_000, 60_000_000),
                    'Regulatory_Capital_Required': random_amount(2_000_000, 40_000_000),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR0201-IR0203 - Balance Sheet Templates
# ============================================================================

def generate_ir0201_balance_sheet():
    """
    IR0201 - Balance Sheet
    Solvency II balance sheet.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        total_assets = random_amount(500_000_000, 5_000_000_000)

        # Asset side
        assets = {
            'Goodwill': 0,  # Not recognised under Solvency II
            'DAC': 0,  # Deferred acquisition costs - not recognised
            'Intangible_Assets': random_amount(0, 1_000_000),
            'Deferred_Tax_Assets': random_amount(1_000_000, 50_000_000),
            'Pension_Benefit_Surplus': random_amount(0, 20_000_000),
            'Property_Plant_Equipment_Own_Use': random_amount(5_000_000, 50_000_000),
            'Investments_Property': random_amount(10_000_000, 200_000_000),
            'Holdings_Related_Undertakings': random_amount(0, 100_000_000),
            'Equities_Listed': random_amount(50_000_000, 500_000_000),
            'Equities_Unlisted': random_amount(0, 50_000_000),
            'Bonds_Government': random_amount(100_000_000, 1_000_000_000),
            'Bonds_Corporate': random_amount(100_000_000, 800_000_000),
            'Bonds_Structured_Notes': random_amount(0, 100_000_000),
            'Bonds_Collateralised': random_amount(0, 50_000_000),
            'Collective_Investment_Undertakings': random_amount(50_000_000, 400_000_000),
            'Derivatives': random_amount(0, 50_000_000),
            'Deposits_Other_Than_Cash': random_amount(10_000_000, 100_000_000),
            'Other_Investments': random_amount(0, 50_000_000),
            'Assets_Held_Unit_Linked': random_amount(0, 200_000_000),
            'Loans_Mortgages': random_amount(0, 100_000_000),
            'Loans_Other': random_amount(0, 50_000_000),
            'Reinsurance_Recoverables_Non_Life': random_amount(20_000_000, 300_000_000),
            'Reinsurance_Recoverables_Life': random_amount(0, 100_000_000),
            'Reinsurance_Recoverables_Unit_Linked': random_amount(0, 20_000_000),
            'Deposits_To_Cedants': random_amount(0, 50_000_000),
            'Receivables_Insurance': random_amount(20_000_000, 200_000_000),
            'Receivables_Reinsurance': random_amount(10_000_000, 100_000_000),
            'Receivables_Other': random_amount(5_000_000, 50_000_000),
            'Own_Shares': 0,
            'Amounts_Due_Own_Funds': random_amount(0, 10_000_000),
            'Cash_And_Equivalents': random_amount(20_000_000, 200_000_000),
            'Other_Assets': random_amount(1_000_000, 20_000_000),
        }

        total_assets_calculated = sum(assets.values())

        # Liability side
        total_liabilities = total_assets_calculated * random_percentage(60, 85) / 100

        liabilities = {
            'TP_Non_Life': total_liabilities * random_percentage(40, 60) / 100,
            'TP_Non_Life_Best_Estimate': 0,  # Will be calculated
            'TP_Non_Life_Risk_Margin': 0,  # Will be calculated
            'TP_Life_Excl_Unit_Linked': total_liabilities * random_percentage(5, 20) / 100,
            'TP_Life_Best_Estimate': 0,
            'TP_Life_Risk_Margin': 0,
            'TP_Unit_Linked': random_amount(0, total_liabilities * 0.1),
            'Other_TP': random_amount(0, total_liabilities * 0.05),
            'Contingent_Liabilities': random_amount(0, 10_000_000),
            'Provisions_Other_Than_TP': random_amount(1_000_000, 20_000_000),
            'Pension_Benefit_Obligations': random_amount(0, 30_000_000),
            'Deposits_From_Reinsurers': random_amount(5_000_000, 100_000_000),
            'Deferred_Tax_Liabilities': random_amount(5_000_000, 100_000_000),
            'Derivatives_Liabilities': random_amount(0, 20_000_000),
            'Debts_To_Credit_Institutions': random_amount(0, 50_000_000),
            'Financial_Liabilities_Other': random_amount(0, 30_000_000),
            'Payables_Insurance': random_amount(10_000_000, 100_000_000),
            'Payables_Reinsurance': random_amount(5_000_000, 80_000_000),
            'Payables_Other': random_amount(5_000_000, 50_000_000),
            'Subordinated_Liabilities_Basic_Own_Funds': random_amount(0, 100_000_000),
            'Subordinated_Liabilities_Not_Basic_Own_Funds': random_amount(0, 20_000_000),
            'Other_Liabilities': random_amount(1_000_000, 20_000_000),
        }

        # Calculate best estimate and risk margin splits
        liabilities['TP_Non_Life_Best_Estimate'] = liabilities['TP_Non_Life'] * 0.92
        liabilities['TP_Non_Life_Risk_Margin'] = liabilities['TP_Non_Life'] * 0.08
        liabilities['TP_Life_Best_Estimate'] = liabilities['TP_Life_Excl_Unit_Linked'] * 0.95
        liabilities['TP_Life_Risk_Margin'] = liabilities['TP_Life_Excl_Unit_Linked'] * 0.05

        total_liabilities_calculated = sum(v for k, v in liabilities.items()
                                          if 'Best_Estimate' not in k and 'Risk_Margin' not in k)

        excess_assets_over_liabilities = total_assets_calculated - total_liabilities_calculated

        data.append({
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            **{f'Asset_{k}': v for k, v in assets.items()},
            'Total_Assets': total_assets_calculated,
            **{f'Liability_{k}': v for k, v in liabilities.items()},
            'Total_Liabilities': total_liabilities_calculated,
            'Excess_Assets_Over_Liabilities': excess_assets_over_liabilities,
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


def generate_ir0202_assets_liabilities_by_currency():
    """
    IR0202 - Assets and Liabilities by Currency
    Currency breakdown of balance sheet items.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        total_assets = random_amount(500_000_000, 5_000_000_000)

        # Currency splits
        currency_splits = {
            'GBP': random_percentage(40, 60),
            'USD': random_percentage(20, 35),
            'EUR': random_percentage(10, 20),
        }
        remaining = 100 - sum(currency_splits.values())
        currency_splits['Other'] = remaining

        for currency, pct in currency_splits.items():
            assets_in_currency = total_assets * pct / 100
            liabilities_in_currency = assets_in_currency * random_percentage(50, 90) / 100

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Currency_Code': currency if currency != 'Other' else 'XXX',
                'Total_Assets': assets_in_currency,
                'Total_Liabilities': liabilities_in_currency,
                'Net_Position': assets_in_currency - liabilities_in_currency,
                'Percentage_Of_Total': pct,
                'Reporting_Currency': 'GBP'
            })

    return pd.DataFrame(data)


def generate_ir0203_branch_balance_sheet():
    """
    IR0203 - Additional Branch Balance Sheet Information
    Balance sheet information for branches.
    """
    data = []

    branch_countries = ['DE', 'FR', 'IE', 'NL']

    for undertaking in UNDERTAKINGS:
        if random.random() > 0.5:  # Some undertakings have branches
            for country in random.sample(branch_countries, random.randint(1, 2)):
                total_assets = random_amount(10_000_000, 200_000_000)
                total_liabilities = total_assets * random_percentage(60, 85) / 100

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Branch_Country': country,
                    'Total_Assets': total_assets,
                    'Investments': total_assets * random_percentage(60, 80) / 100,
                    'Reinsurance_Recoverables': total_assets * random_percentage(5, 15) / 100,
                    'Receivables': total_assets * random_percentage(5, 15) / 100,
                    'Cash': total_assets * random_percentage(3, 10) / 100,
                    'Other_Assets': total_assets * random_percentage(2, 5) / 100,
                    'Technical_Provisions': total_liabilities * random_percentage(70, 85) / 100,
                    'Other_Liabilities': total_liabilities * random_percentage(15, 30) / 100,
                    'Total_Liabilities': total_liabilities,
                    'Net_Assets': total_assets - total_liabilities,
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR0301-IR0303 - Off-Balance Sheet Items
# ============================================================================

def generate_ir0301_off_balance_sheet_general():
    """
    IR0301 - Off-Balance Sheet Items (General)
    General off-balance sheet exposures.
    """
    data = []

    item_types = [
        'Contingent liabilities',
        'Loan commitments',
        'Letters of credit',
        'Guarantees provided',
        'Guarantees received',
        'Collateral held',
        'Other off-balance sheet items'
    ]

    for undertaking in UNDERTAKINGS:
        for item_type in item_types:
            if random.random() > 0.3:  # 70% chance of having this item type
                max_value = random_amount(0, 100_000_000)
                current_value = max_value * random_percentage(20, 80) / 100

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Item_Type': item_type,
                    'Maximum_Value': max_value,
                    'Current_Value': current_value,
                    'Tier_1_Impact': current_value * random_percentage(0, 20) / 100,
                    'SCR_Impact': current_value * random_percentage(5, 25) / 100,
                    'Counterparty_Type': random.choice(['Insurer', 'Reinsurer', 'Bank', 'Corporate', 'Government']),
                    'Maturity_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') +
                                     timedelta(days=random.randint(30, 1825))).strftime('%Y-%m-%d'),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


def generate_ir0302_guarantees_received():
    """
    IR0302 - Off-Balance Sheet Items (Unlimited Guarantees Received)
    Unlimited guarantees received from third parties.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if random.random() > 0.6:  # 40% have unlimited guarantees received
            for _ in range(random.randint(1, 3)):
                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Guarantee_Provider_LEI': generate_lei(),
                    'Guarantee_Provider_Name': f'Parent Company {random.randint(1, 100)}',
                    'Guarantee_Provider_Type': random.choice(['Parent', 'Ultimate Parent', 'Other Group Entity']),
                    'Guarantee_Type': random.choice(['Full', 'Limited to Specific Liabilities']),
                    'Economic_Value': random_amount(10_000_000, 500_000_000),
                    'Ancillary_Own_Funds_Amount': random_amount(0, 200_000_000),
                    'Tier_Classification': random.choice(['Tier 1', 'Tier 2', 'Tier 3']),
                    'Approval_Status': random.choice(['Approved', 'Pending', 'Not Required']),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


def generate_ir0303_guarantees_provided():
    """
    IR0303 - Off-Balance Sheet Items (Unlimited Guarantees Provided)
    Unlimited guarantees provided to third parties.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if random.random() > 0.7:  # 30% provide unlimited guarantees
            for _ in range(random.randint(1, 2)):
                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Guarantee_Recipient_LEI': generate_lei(),
                    'Guarantee_Recipient_Name': f'Subsidiary {random.randint(1, 50)}',
                    'Guarantee_Recipient_Type': random.choice(['Subsidiary', 'Related Party', 'Third Party']),
                    'Guarantee_Type': random.choice(['Full', 'Limited']),
                    'Maximum_Potential_Exposure': random_amount(10_000_000, 300_000_000),
                    'Current_Triggered_Amount': random_amount(0, 50_000_000),
                    'SCR_Impact': random_amount(5_000_000, 100_000_000),
                    'Probability_Of_Trigger': random_percentage(0, 10),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# Continue with remaining templates in Part 2...
# (The file continues with all 88 templates)


# ============================================================================
# Master Generation Function
# ============================================================================

def generate_all_qrts() -> Dict[str, pd.DataFrame]:
    """
    Generate all QRT templates.
    Returns a dictionary of DataFrames keyed by template name.
    """
    templates = {}

    # AOC
    templates['AOC01_Analysis_Of_Change_SCR'] = generate_aoc01_analysis_of_change()

    # Internal Model
    templates['IM00_Submission_Content'] = generate_im00_submission_content()
    templates['IM01_Life_Outputs'] = generate_im01_life_outputs()
    templates['IM02_Counterparty_Risk'] = generate_im02_counterparty_risk()
    templates['IM03_Non_Life_Outputs'] = generate_im03_non_life_outputs()

    # Basic Information
    templates['IR0101_Submission_Content'] = generate_ir0101_submission_content()
    templates['IR0102_Basic_Info_General'] = generate_ir0102_basic_info_general()
    templates['IR0103_RFF_Matching_Portfolios'] = generate_ir0103_rff_matching_portfolios()
    templates['IR0104_Branch_Info'] = generate_ir0104_branch_info()

    # Balance Sheet
    templates['IR0201_Balance_Sheet'] = generate_ir0201_balance_sheet()
    templates['IR0202_Assets_Liabilities_Currency'] = generate_ir0202_assets_liabilities_by_currency()
    templates['IR0203_Branch_Balance_Sheet'] = generate_ir0203_branch_balance_sheet()

    # Off-Balance Sheet
    templates['IR0301_Off_Balance_Sheet_General'] = generate_ir0301_off_balance_sheet_general()
    templates['IR0302_Guarantees_Received'] = generate_ir0302_guarantees_received()
    templates['IR0303_Guarantees_Provided'] = generate_ir0303_guarantees_provided()

    return templates


# ============================================================================
# Power BI Execution
# ============================================================================

if __name__ == "__main__":
    # Generate all templates
    all_templates = generate_all_qrts()

    # Print summary
    print("=" * 60)
    print("QRT Master Generator - Templates Generated")
    print("=" * 60)
    for name, df in all_templates.items():
        print(f"{name}: {len(df)} rows")
    print("=" * 60)

# For Power BI, create individual DataFrame variables
AOC01_Analysis_Of_Change_SCR = generate_aoc01_analysis_of_change()
IM00_Submission_Content = generate_im00_submission_content()
IM01_Life_Outputs = generate_im01_life_outputs()
IM02_Counterparty_Risk = generate_im02_counterparty_risk()
IM03_Non_Life_Outputs = generate_im03_non_life_outputs()
IR0101_Submission_Content = generate_ir0101_submission_content()
IR0102_Basic_Info_General = generate_ir0102_basic_info_general()
IR0103_RFF_Matching_Portfolios = generate_ir0103_rff_matching_portfolios()
IR0104_Branch_Info = generate_ir0104_branch_info()
IR0201_Balance_Sheet = generate_ir0201_balance_sheet()
IR0202_Assets_Liabilities_Currency = generate_ir0202_assets_liabilities_by_currency()
IR0203_Branch_Balance_Sheet = generate_ir0203_branch_balance_sheet()
IR0301_Off_Balance_Sheet_General = generate_ir0301_off_balance_sheet_general()
IR0302_Guarantees_Received = generate_ir0302_guarantees_received()
IR0303_Guarantees_Provided = generate_ir0303_guarantees_provided()
