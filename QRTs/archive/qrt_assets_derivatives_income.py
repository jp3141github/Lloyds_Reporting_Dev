"""
PRA/BoE QRT Generators - Premiums, Claims, Expenses & Assets
============================================================
IR0502-IR0510: Premiums, Claims, Expenses templates
IR0602-IR0603: Assets templates
IR0801: Derivatives
IR0901: Income, Gains and Losses
IR1001: Securities Lending and Repos
IR1101: Assets Held as Collateral

Usage in Power BI:
1. Get Data > More > Python script
2. Copy and paste this script
3. Select the tables you need from the list
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================================================
# Configuration
# ============================================================================

UNDERTAKINGS = [
    {'lei': '549300ABCDEF123456G7', 'name': 'Lloyd\'s Syndicate 2987', 'type': 'Non-Life'},
    {'lei': '549300HIJKLM789012N3', 'name': 'Lloyd\'s Syndicate 33', 'type': 'Non-Life'},
    {'lei': '549300OPQRS456789T0', 'name': 'Lloyd\'s Syndicate 1183', 'type': 'Non-Life'},
    {'lei': '549300UVWXY012345Z1', 'name': 'Lloyd\'s Syndicate 2791', 'type': 'Composite'},
    {'lei': '549300ABCDE678901F2', 'name': 'Lloyd\'s Syndicate 623', 'type': 'Non-Life'},
]

REPORTING_DATE = '2024-12-31'

COUNTRIES = ['GB', 'US', 'DE', 'FR', 'JP', 'CH', 'AU', 'CA', 'IE', 'LU', 'NL', 'IT', 'ES']

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
    'Miscellaneous financial loss'
]

LIFE_LOB = [
    'Insurance with profit participation',
    'Index-linked and unit-linked insurance',
    'Other life insurance',
    'Annuities stemming from non-life contracts',
    'Health insurance (SLT)',
    'Life reinsurance'
]

# Helper functions
def generate_lei():
    return '549300' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))

def generate_isin():
    country = random.choice(['GB', 'US', 'DE', 'FR'])
    return country + ''.join(random.choices(string.ascii_uppercase + string.digits, k=9)) + str(random.randint(0, 9))

def random_amount(min_val, max_val, precision=2):
    return round(np.random.uniform(min_val, max_val), precision)

def random_percentage(min_val=0, max_val=100):
    return round(np.random.uniform(min_val, max_val), 4)


# ============================================================================
# IR0502 - Premiums, Claims and Expenses by Country
# ============================================================================

def generate_ir0502_premiums_claims_by_country():
    """
    IR0502 - Premiums, Claims and Expenses by Country
    Geographic breakdown of underwriting performance.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        for country in COUNTRIES[:8]:  # Top 8 countries
            gwp = random_amount(1_000_000, 100_000_000)
            nwp = gwp * random_percentage(60, 95) / 100

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Country': country,
                'Home_Country': 'Yes' if country == 'GB' else 'No',
                'Gross_Written_Premium': gwp,
                'Gross_Earned_Premium': gwp * random_percentage(85, 98) / 100,
                'Gross_Claims_Incurred': gwp * random_percentage(40, 75) / 100,
                'Gross_Operating_Expenses': gwp * random_percentage(15, 35) / 100,
                'Reinsurance_Premium_Ceded': gwp - nwp,
                'Net_Written_Premium': nwp,
                'Net_Earned_Premium': nwp * random_percentage(85, 98) / 100,
                'Net_Claims_Incurred': nwp * random_percentage(35, 70) / 100,
                'Acquisition_Costs': gwp * random_percentage(10, 25) / 100,
                'Administrative_Expenses': gwp * random_percentage(5, 15) / 100,
                'Investment_Management_Expenses': gwp * random_percentage(0.5, 2) / 100,
                'Claims_Management_Expenses': gwp * random_percentage(2, 8) / 100,
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# IR0503 - Life Income and Expenditure
# ============================================================================

def generate_ir0503_life_income_expenditure():
    """
    IR0503 - Life Income and Expenditure
    Detailed life insurance income and expense analysis.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            for lob in LIFE_LOB[:4]:
                gwp = random_amount(5_000_000, 200_000_000)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Line_Of_Business': lob,
                    'Gross_Written_Premium': gwp,
                    'Gross_Earned_Premium': gwp * random_percentage(90, 100) / 100,
                    'Reinsurance_Premium_Ceded': gwp * random_percentage(5, 25) / 100,
                    'Net_Written_Premium': gwp * random_percentage(75, 95) / 100,
                    'Gross_Benefits_Paid': gwp * random_percentage(30, 60) / 100,
                    'Gross_Change_In_TP': random_amount(-50_000_000, 50_000_000),
                    'Reinsurance_Recoveries': gwp * random_percentage(5, 20) / 100,
                    'Net_Benefits': gwp * random_percentage(25, 55) / 100,
                    'Commission_Expense': gwp * random_percentage(3, 15) / 100,
                    'Administrative_Expense': gwp * random_percentage(5, 12) / 100,
                    'Investment_Management_Expense': gwp * random_percentage(0.5, 3) / 100,
                    'Claims_Handling_Expense': gwp * random_percentage(1, 5) / 100,
                    'Other_Technical_Expenses': gwp * random_percentage(1, 4) / 100,
                    'Investment_Income': gwp * random_percentage(8, 20) / 100,
                    'Unrealised_Gains_Losses': random_amount(-20_000_000, 30_000_000),
                    'Other_Income': random_amount(0, 5_000_000),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR0504 - Non-Life Income, Expenditure and Business Model Analysis
# ============================================================================

def generate_ir0504_non_life_income_expenditure():
    """
    IR0504 - Non-Life Income, Expenditure and Business Model Analysis
    Comprehensive non-life underwriting and business model analysis.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            for lob in NON_LIFE_LOB[:10]:
                gwp = random_amount(10_000_000, 300_000_000)
                gep = gwp * random_percentage(88, 98) / 100
                claims_ratio = random_percentage(45, 85)
                expense_ratio = random_percentage(20, 40)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Line_Of_Business': lob,
                    # Premium Analysis
                    'Gross_Written_Premium': gwp,
                    'Gross_Earned_Premium': gep,
                    'Reinsurance_Premium_Ceded': gwp * random_percentage(10, 35) / 100,
                    'Net_Written_Premium': gwp * random_percentage(65, 90) / 100,
                    'Net_Earned_Premium': gep * random_percentage(65, 90) / 100,
                    # Claims Analysis
                    'Gross_Claims_Incurred': gep * claims_ratio / 100,
                    'Reinsurance_Recoveries': gep * claims_ratio * random_percentage(10, 30) / 10000,
                    'Net_Claims_Incurred': gep * claims_ratio * random_percentage(70, 90) / 10000,
                    'Claims_Paid': gep * claims_ratio * random_percentage(60, 85) / 10000,
                    'Change_In_Claims_Provisions': gep * claims_ratio * random_percentage(15, 40) / 10000,
                    # Expense Analysis
                    'Total_Expenses': gep * expense_ratio / 100,
                    'Acquisition_Costs': gep * random_percentage(12, 25) / 100,
                    'Administrative_Expenses': gep * random_percentage(6, 12) / 100,
                    'Other_Technical_Expenses': gep * random_percentage(2, 5) / 100,
                    # Business Model Analysis
                    'Number_Of_Policies': random.randint(1000, 100000),
                    'Average_Premium_Per_Policy': gwp / random.randint(1000, 100000),
                    'Policy_Retention_Rate': random_percentage(70, 95),
                    'New_Business_Premium': gwp * random_percentage(15, 40) / 100,
                    'Renewal_Premium': gwp * random_percentage(60, 85) / 100,
                    # Ratios
                    'Loss_Ratio': claims_ratio,
                    'Expense_Ratio': expense_ratio,
                    'Combined_Ratio': claims_ratio + expense_ratio,
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR0505 - Life Premiums and Claims by Country
# ============================================================================

def generate_ir0505_life_premiums_claims_by_country():
    """
    IR0505 - Life Premiums and Claims by Country
    Geographic breakdown of life insurance business.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            for country in COUNTRIES[:6]:
                gwp = random_amount(500_000, 50_000_000)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Country': country,
                    'Gross_Written_Premium': gwp,
                    'Reinsurance_Premium_Ceded': gwp * random_percentage(5, 20) / 100,
                    'Net_Written_Premium': gwp * random_percentage(80, 95) / 100,
                    'Gross_Claims_Paid': gwp * random_percentage(30, 60) / 100,
                    'Reinsurance_Recoveries': gwp * random_percentage(3, 15) / 100,
                    'Net_Claims_Paid': gwp * random_percentage(25, 55) / 100,
                    'Number_Of_Contracts': random.randint(100, 10000),
                    'Sum_Insured': gwp * random.randint(10, 50),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR0506 - Non-Life Premiums and Claims by Country
# ============================================================================

def generate_ir0506_non_life_premiums_claims_by_country():
    """
    IR0506 - Non-Life Premiums and Claims by Country
    Geographic breakdown of non-life insurance business.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            for lob in NON_LIFE_LOB[:6]:
                for country in COUNTRIES[:5]:
                    gwp = random_amount(500_000, 80_000_000)

                    data.append({
                        'LEI': undertaking['lei'],
                        'Undertaking_Name': undertaking['name'],
                        'Reporting_Date': REPORTING_DATE,
                        'Line_Of_Business': lob,
                        'Country': country,
                        'Gross_Written_Premium': gwp,
                        'Gross_Earned_Premium': gwp * random_percentage(88, 98) / 100,
                        'Gross_Claims_Incurred': gwp * random_percentage(40, 75) / 100,
                        'Gross_Expenses': gwp * random_percentage(20, 35) / 100,
                        'Reinsurance_Balance': gwp * random_percentage(-15, 15) / 100,
                        'Net_Written_Premium': gwp * random_percentage(70, 95) / 100,
                        'Number_Of_Policies': random.randint(50, 20000),
                        'Number_Of_Claims': random.randint(5, 2000),
                        'Currency': 'GBP'
                    })

    return pd.DataFrame(data)


# ============================================================================
# IR0507 - Business Model Analysis (Financial Guarantee Insurers)
# ============================================================================

def generate_ir0507_fgi_business_model():
    """
    IR0507 - Business Model Analysis for Financial Guarantee Insurers
    Specific template for financial guarantee business.
    """
    data = []

    guarantee_types = [
        'Municipal Bond Insurance',
        'Structured Finance Insurance',
        'Asset-Backed Securities Insurance',
        'Infrastructure Bond Insurance',
        'Trade Credit Insurance'
    ]

    for undertaking in UNDERTAKINGS[:2]:  # Only a couple have FGI business
        for g_type in guarantee_types[:3]:
            par_outstanding = random_amount(100_000_000, 2_000_000_000)

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Guarantee_Type': g_type,
                'Par_Outstanding': par_outstanding,
                'Gross_Premium_Received': par_outstanding * random_percentage(0.5, 2) / 100,
                'Unearned_Premium_Reserve': par_outstanding * random_percentage(0.3, 1.5) / 100,
                'Claims_Paid_Cumulative': par_outstanding * random_percentage(0, 5) / 100,
                'Claims_Outstanding': par_outstanding * random_percentage(0, 3) / 100,
                'Expected_Loss': par_outstanding * random_percentage(0.1, 2) / 100,
                'Risk_In_Force': par_outstanding * random_percentage(80, 100) / 100,
                'Average_Credit_Quality': random.choice(['AAA', 'AA', 'A', 'BBB']),
                'Weighted_Average_Life_Years': random_percentage(3, 15),
                'Concentration_Top_10_Pct': random_percentage(20, 60),
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# IR0508 - Material Pooling Arrangements
# ============================================================================

def generate_ir0508_pooling_arrangements():
    """
    IR0508 - Material Pooling Arrangements
    Details of participation in insurance pools.
    """
    data = []

    pool_names = [
        'Nuclear Pool', 'Terrorism Pool', 'Natural Catastrophe Pool',
        'Aviation Pool', 'Marine Pool'
    ]

    for undertaking in UNDERTAKINGS:
        if random.random() > 0.5:  # 50% participate in pools
            for pool in random.sample(pool_names, random.randint(1, 2)):
                share_pct = random_percentage(1, 15)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Pool_Name': pool,
                    'Pool_Manager': f'{pool} Management Ltd',
                    'Pool_Type': random.choice(['Mandatory', 'Voluntary']),
                    'Participation_Share_Pct': share_pct,
                    'Pool_Total_Premium': random_amount(50_000_000, 500_000_000),
                    'Undertaking_Share_Premium': random_amount(500_000, 50_000_000),
                    'Pool_Total_Claims': random_amount(10_000_000, 300_000_000),
                    'Undertaking_Share_Claims': random_amount(100_000, 30_000_000),
                    'Pool_Technical_Provisions': random_amount(100_000_000, 1_000_000_000),
                    'Undertaking_Share_TP': random_amount(1_000_000, 100_000_000),
                    'Maximum_Liability': random_amount(10_000_000, 200_000_000),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR0509 - Assessable Mutuals
# ============================================================================

def generate_ir0509_assessable_mutuals():
    """
    IR0509 - Assessable Mutuals
    Information on mutual insurance undertakings with assessment rights.
    """
    data = []

    # Only applicable to mutuals - create synthetic data for demonstration
    for i in range(2):
        base_premium = random_amount(20_000_000, 100_000_000)

        data.append({
            'LEI': generate_lei(),
            'Undertaking_Name': f'Mutual Insurance Company {i+1}',
            'Reporting_Date': REPORTING_DATE,
            'Mutual_Type': random.choice(['Protection and Indemnity', 'Professional Liability', 'Agricultural']),
            'Number_Of_Members': random.randint(500, 10000),
            'Regular_Premium_Income': base_premium,
            'Assessment_Right_Maximum': base_premium * random.randint(1, 3),
            'Assessment_Called_Current_Year': base_premium * random_percentage(0, 20) / 100,
            'Assessment_Called_Cumulative': base_premium * random_percentage(0, 50) / 100,
            'Average_Assessment_Rate': random_percentage(0, 25),
            'Member_Surplus': random_amount(10_000_000, 200_000_000),
            'Contingent_Liability': base_premium * random.randint(1, 3),
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


# ============================================================================
# IR0510 - Excess Capital Generation
# ============================================================================

def generate_ir0510_excess_capital():
    """
    IR0510 - Excess Capital Generation
    Analysis of capital generation and distribution.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        opening_own_funds = random_amount(200_000_000, 1_000_000_000)

        movements = {
            'Underwriting_Result': random_amount(-50_000_000, 100_000_000),
            'Investment_Return': random_amount(10_000_000, 80_000_000),
            'Other_Comprehensive_Income': random_amount(-20_000_000, 30_000_000),
            'Tax_Charge': random_amount(-30_000_000, -5_000_000),
            'Dividends_Paid': random_amount(-50_000_000, 0),
            'Capital_Raised': random_amount(0, 50_000_000),
            'Foreign_Exchange': random_amount(-10_000_000, 10_000_000),
            'Model_Changes': random_amount(-20_000_000, 20_000_000),
            'Regulatory_Adjustments': random_amount(-10_000_000, 10_000_000),
        }

        closing_own_funds = opening_own_funds + sum(movements.values())
        scr = closing_own_funds * random_percentage(40, 70) / 100
        excess = closing_own_funds - scr

        data.append({
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            'Opening_Own_Funds': opening_own_funds,
            **{f'Movement_{k}': v for k, v in movements.items()},
            'Total_Movement': sum(movements.values()),
            'Closing_Own_Funds': closing_own_funds,
            'SCR': scr,
            'Excess_Capital': excess,
            'Solvency_Ratio': closing_own_funds / scr * 100,
            'Return_On_Equity': (movements['Underwriting_Result'] + movements['Investment_Return']) / opening_own_funds * 100,
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


# ============================================================================
# IR0602 - List of Assets
# ============================================================================

def generate_ir0602_list_of_assets():
    """
    IR0602 - List of Assets
    Detailed listing of all assets held.
    """
    data = []

    asset_types = [
        ('Government Bonds', '1'),
        ('Corporate Bonds', '2'),
        ('Equity - Listed', '31'),
        ('Equity - Unlisted', '32'),
        ('Investment Funds', '4'),
        ('Structured Notes', '5'),
        ('Cash and Deposits', '7'),
        ('Mortgages and Loans', '8'),
        ('Property', '9'),
    ]

    for undertaking in UNDERTAKINGS:
        for asset_type, cic_prefix in asset_types:
            num_assets = random.randint(5, 50) if asset_type in ['Government Bonds', 'Corporate Bonds'] else random.randint(1, 15)

            for i in range(num_assets):
                par_value = random_amount(100_000, 50_000_000)
                acquisition_value = par_value * random_percentage(95, 105) / 100
                sii_value = par_value * random_percentage(90, 115) / 100

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Asset_ID': f'{undertaking["lei"][:8]}_{asset_type[:3]}_{i+1:04d}',
                    'Asset_Type': asset_type,
                    'CIC_Code': f'{cic_prefix}{random.randint(1,9):1d}',
                    'Asset_Held_In_Unit_Linked': random.choice(['No', 'No', 'No', 'Yes']),
                    'Country_Of_Issue': random.choice(COUNTRIES),
                    'Currency': random.choice(['GBP', 'USD', 'EUR']),
                    'Issuer_Name': f'Issuer {random.randint(1, 1000)}',
                    'Issuer_LEI': generate_lei() if random.random() > 0.3 else None,
                    'Issuer_Sector': random.choice(['Government', 'Financial', 'Corporate', 'Insurance']),
                    'Credit_Rating': random.choice(['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'NR']),
                    'ISIN': generate_isin() if asset_type in ['Government Bonds', 'Corporate Bonds', 'Equity - Listed'] else None,
                    'Par_Value': par_value,
                    'Acquisition_Value': acquisition_value,
                    'Total_Solvency_II_Value': sii_value,
                    'Accrued_Interest': par_value * random_percentage(0, 3) / 100 if 'Bond' in asset_type else 0,
                    'Maturity_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') +
                                     timedelta(days=random.randint(365, 10950))).strftime('%Y-%m-%d') if 'Bond' in asset_type else None,
                    'Coupon_Rate': random_percentage(1, 6) if 'Bond' in asset_type else None,
                    'Quantity_Held': random.randint(100, 100000) if 'Equity' in asset_type else None,
                    'Unit_Price': sii_value / random.randint(100, 100000) if 'Equity' in asset_type else None,
                    'Duration_Modified': random_percentage(1, 10) if 'Bond' in asset_type else None,
                    'Reporting_Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR0603 - Collective Investment Undertakings Look-Through
# ============================================================================

def generate_ir0603_ciu_look_through():
    """
    IR0603 - Collective Investment Undertakings Look-Through Approach
    Detailed breakdown of fund holdings.
    """
    data = []

    fund_types = ['Equity Fund', 'Bond Fund', 'Mixed Fund', 'Money Market Fund', 'Real Estate Fund']

    for undertaking in UNDERTAKINGS:
        for _ in range(random.randint(3, 10)):
            fund_value = random_amount(5_000_000, 100_000_000)
            fund_type = random.choice(fund_types)

            # Underlying asset allocation
            if fund_type == 'Equity Fund':
                allocations = {'Equity': 95, 'Cash': 5}
            elif fund_type == 'Bond Fund':
                allocations = {'Government Bonds': 40, 'Corporate Bonds': 55, 'Cash': 5}
            elif fund_type == 'Mixed Fund':
                allocations = {'Equity': 45, 'Bonds': 45, 'Cash': 10}
            elif fund_type == 'Money Market Fund':
                allocations = {'Cash': 60, 'Short-term Bonds': 40}
            else:
                allocations = {'Property': 85, 'Cash': 15}

            for asset_class, pct in allocations.items():
                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Fund_ID': f'FUND_{generate_isin()[:8]}',
                    'Fund_Name': f'{fund_type} - {random.randint(1, 100)}',
                    'Fund_Type': fund_type,
                    'Fund_Manager': f'Asset Manager {random.randint(1, 50)}',
                    'Fund_LEI': generate_lei(),
                    'Total_Fund_Value': fund_value,
                    'Undertaking_Share_Value': fund_value * random_percentage(0.5, 10) / 100,
                    'Underlying_Asset_Category': asset_class,
                    'Underlying_Asset_Value': fund_value * pct / 100,
                    'Underlying_Asset_Pct': pct,
                    'Country_Exposure': random.choice(COUNTRIES),
                    'Currency_Exposure': random.choice(['GBP', 'USD', 'EUR']),
                    'Look_Through_Level': random.randint(1, 3),
                    'Reporting_Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR0801 - Open Derivatives
# ============================================================================

def generate_ir0801_open_derivatives():
    """
    IR0801 - Open Derivatives
    Details of derivative positions.
    """
    data = []

    derivative_types = [
        ('Interest Rate Swap', 'D1'),
        ('Currency Swap', 'D2'),
        ('Forward FX', 'E1'),
        ('FX Option', 'E2'),
        ('Equity Option', 'F1'),
        ('Equity Future', 'F2'),
        ('Credit Default Swap', 'G1'),
        ('Interest Rate Future', 'D3'),
    ]

    purposes = ['Hedging', 'Efficient Portfolio Management', 'Speculation']

    for undertaking in UNDERTAKINGS:
        for deriv_type, cic_code in derivative_types:
            if random.random() > 0.4:  # 60% chance of having this derivative type
                for _ in range(random.randint(1, 5)):
                    notional = random_amount(10_000_000, 500_000_000)
                    mtm = random_amount(-notional * 0.05, notional * 0.05)

                    data.append({
                        'LEI': undertaking['lei'],
                        'Undertaking_Name': undertaking['name'],
                        'Reporting_Date': REPORTING_DATE,
                        'Derivative_ID': f'DERIV_{random.randint(10000, 99999)}',
                        'Derivative_Type': deriv_type,
                        'CIC_Code': cic_code,
                        'Counterparty_Name': f'Bank {random.randint(1, 50)}',
                        'Counterparty_LEI': generate_lei(),
                        'Counterparty_Credit_Rating': random.choice(['AAA', 'AA', 'A', 'BBB']),
                        'Purpose': random.choice(purposes),
                        'Hedged_Item': f'Asset Portfolio {random.randint(1, 10)}' if 'Hedging' in purposes[0] else None,
                        'Notional_Amount': notional,
                        'Mark_To_Market_Value': mtm,
                        'Solvency_II_Value': mtm,
                        'Trade_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') -
                                      timedelta(days=random.randint(30, 1095))).strftime('%Y-%m-%d'),
                        'Maturity_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') +
                                         timedelta(days=random.randint(30, 3650))).strftime('%Y-%m-%d'),
                        'Strike_Price': random_amount(0.8, 1.2) if 'Option' in deriv_type else None,
                        'Swap_Rate': random_percentage(1, 5) if 'Swap' in deriv_type else None,
                        'Delta': random_percentage(-1, 1) if 'Option' in deriv_type else None,
                        'Currency': random.choice(['GBP', 'USD', 'EUR']),
                        'Collateral_Posted': abs(mtm) * random_percentage(80, 120) / 100 if mtm < 0 else 0,
                        'Collateral_Received': abs(mtm) * random_percentage(80, 120) / 100 if mtm > 0 else 0,
                        'Reporting_Currency': 'GBP'
                    })

    return pd.DataFrame(data)


# ============================================================================
# IR0901 - Income, Gains and Losses in the Period
# ============================================================================

def generate_ir0901_income_gains_losses():
    """
    IR0901 - Income, Gains and Losses in the Period
    Investment income and capital movements.
    """
    data = []

    asset_categories = [
        'Government Bonds', 'Corporate Bonds', 'Equity', 'Property',
        'Collective Investment Undertakings', 'Derivatives', 'Cash and Deposits'
    ]

    for undertaking in UNDERTAKINGS:
        for category in asset_categories:
            avg_value = random_amount(20_000_000, 500_000_000)

            # Income components
            interest_income = avg_value * random_percentage(1, 5) / 100 if 'Bond' in category or category == 'Cash and Deposits' else 0
            dividend_income = avg_value * random_percentage(1, 4) / 100 if category in ['Equity', 'Collective Investment Undertakings'] else 0
            rental_income = avg_value * random_percentage(3, 7) / 100 if category == 'Property' else 0

            # Gains/Losses
            realised_gains = random_amount(-avg_value * 0.03, avg_value * 0.05)
            unrealised_gains = random_amount(-avg_value * 0.05, avg_value * 0.08)
            fx_gains = random_amount(-avg_value * 0.02, avg_value * 0.02)

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Asset_Category': category,
                'Opening_Value': avg_value * random_percentage(90, 110) / 100,
                'Purchases': random_amount(0, avg_value * 0.3),
                'Sales': random_amount(0, avg_value * 0.25),
                'Closing_Value': avg_value,
                'Interest_Income': interest_income,
                'Dividend_Income': dividend_income,
                'Rental_Income': rental_income,
                'Other_Income': random_amount(0, avg_value * 0.005),
                'Total_Income': interest_income + dividend_income + rental_income,
                'Realised_Gains_Losses': realised_gains,
                'Unrealised_Gains_Losses': unrealised_gains,
                'Foreign_Exchange_Gains_Losses': fx_gains,
                'Total_Return': interest_income + dividend_income + rental_income + realised_gains + unrealised_gains + fx_gains,
                'Investment_Expenses': avg_value * random_percentage(0.1, 0.5) / 100,
                'Net_Investment_Return': (interest_income + dividend_income + rental_income + realised_gains +
                                         unrealised_gains + fx_gains - avg_value * 0.003),
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# IR1001 - Securities Lending and Repos
# ============================================================================

def generate_ir1001_securities_lending_repos():
    """
    IR1001 - Securities Lending and Repos
    Securities lending and repurchase agreement details.
    """
    data = []

    transaction_types = ['Securities Lending', 'Repo', 'Reverse Repo', 'Securities Borrowing']

    for undertaking in UNDERTAKINGS:
        for trans_type in transaction_types:
            if random.random() > 0.5:  # 50% chance of having this type
                for _ in range(random.randint(1, 5)):
                    value = random_amount(5_000_000, 200_000_000)

                    data.append({
                        'LEI': undertaking['lei'],
                        'Undertaking_Name': undertaking['name'],
                        'Reporting_Date': REPORTING_DATE,
                        'Transaction_ID': f'SL_{random.randint(10000, 99999)}',
                        'Transaction_Type': trans_type,
                        'Counterparty_Name': f'Custodian Bank {random.randint(1, 20)}',
                        'Counterparty_LEI': generate_lei(),
                        'Securities_ISIN': generate_isin(),
                        'Securities_Type': random.choice(['Government Bond', 'Corporate Bond', 'Equity']),
                        'Securities_Value': value,
                        'Cash_Collateral_Amount': value * random_percentage(100, 105) / 100 if trans_type in ['Securities Lending', 'Repo'] else 0,
                        'Non_Cash_Collateral_Value': value * random_percentage(102, 110) / 100 if random.random() > 0.7 else 0,
                        'Fee_Income': value * random_percentage(0.05, 0.3) / 100 if 'Lending' in trans_type else 0,
                        'Fee_Expense': value * random_percentage(0.05, 0.3) / 100 if 'Borrowing' in trans_type else 0,
                        'Repo_Rate': random_percentage(0.5, 3) if 'Repo' in trans_type else None,
                        'Start_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') -
                                      timedelta(days=random.randint(1, 180))).strftime('%Y-%m-%d'),
                        'Maturity_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') +
                                         timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
                        'Open_Maturity': random.choice(['Yes', 'No']),
                        'Reinvestment_Of_Collateral': random.choice(['Yes', 'No']),
                        'Currency': 'GBP'
                    })

    return pd.DataFrame(data)


# ============================================================================
# IR1101 - Assets Held as Collateral
# ============================================================================

def generate_ir1101_assets_collateral():
    """
    IR1101 - Assets Held as Collateral
    Details of assets pledged or held as collateral.
    """
    data = []

    collateral_purposes = [
        'Derivatives margin',
        'Securities lending',
        'Reinsurance collateral',
        'Regulatory capital',
        'Letter of credit backing',
        'Trust fund'
    ]

    for undertaking in UNDERTAKINGS:
        for purpose in collateral_purposes:
            if random.random() > 0.4:  # 60% chance
                value = random_amount(5_000_000, 200_000_000)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Collateral_ID': f'COLL_{random.randint(10000, 99999)}',
                    'Collateral_Purpose': purpose,
                    'Collateral_Type': random.choice(['Cash', 'Government Bond', 'Corporate Bond', 'Letter of Credit']),
                    'Asset_ID': f'ASSET_{random.randint(10000, 99999)}',
                    'Asset_ISIN': generate_isin() if random.random() > 0.3 else None,
                    'Solvency_II_Value': value,
                    'Encumbered_Value': value * random_percentage(80, 100) / 100,
                    'Counterparty_Name': f'Counterparty {random.randint(1, 50)}',
                    'Counterparty_LEI': generate_lei(),
                    'Haircut_Percentage': random_percentage(0, 15),
                    'Value_After_Haircut': value * (1 - random_percentage(0, 15) / 100),
                    'Pledged_Or_Held': random.choice(['Pledged', 'Held']),
                    'Freely_Disposable': random.choice(['Yes', 'No']),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# Power BI Execution
# ============================================================================

if __name__ == "__main__":
    print("Generating Premiums, Claims, Expenses & Assets QRTs...")

# Generate all tables for Power BI
IR0502_Premiums_Claims_Country = generate_ir0502_premiums_claims_by_country()
IR0503_Life_Income_Expenditure = generate_ir0503_life_income_expenditure()
IR0504_Non_Life_Income_Expenditure = generate_ir0504_non_life_income_expenditure()
IR0505_Life_Premiums_Claims_Country = generate_ir0505_life_premiums_claims_by_country()
IR0506_Non_Life_Premiums_Claims_Country = generate_ir0506_non_life_premiums_claims_by_country()
IR0507_FGI_Business_Model = generate_ir0507_fgi_business_model()
IR0508_Pooling_Arrangements = generate_ir0508_pooling_arrangements()
IR0509_Assessable_Mutuals = generate_ir0509_assessable_mutuals()
IR0510_Excess_Capital = generate_ir0510_excess_capital()
IR0602_List_Of_Assets = generate_ir0602_list_of_assets()
IR0603_CIU_Look_Through = generate_ir0603_ciu_look_through()
IR0801_Open_Derivatives = generate_ir0801_open_derivatives()
IR0901_Income_Gains_Losses = generate_ir0901_income_gains_losses()
IR1001_Securities_Lending_Repos = generate_ir1001_securities_lending_repos()
IR1101_Assets_Collateral = generate_ir1101_assets_collateral()
