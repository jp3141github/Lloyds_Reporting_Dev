"""
PRA/BoE QRT Generators - Reinsurance and Group Templates
========================================================
IR3003-IR3008: Outwards Reinsurance (Non-Life & Life)
IR3101: Reinsurance Balance Sheet Exposures
IR3201: Undertakings in Scope of Group
IR3301: Insurance/Reinsurance Individual Requirements
IR3401: Other Regulated/Non-Regulated Financial Undertakings
IR3501: Contribution to Group Technical Provisions
IR3601-IR3604: Intra-Group Transactions (IGT)
IRR2202-IRR2203: Matching Adjustment Templates

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

COUNTRIES = ['GB', 'US', 'DE', 'FR', 'BM', 'CH', 'AU', 'CA', 'IE', 'SG']

NON_LIFE_LOB = [
    'Motor vehicle liability insurance',
    'Other motor insurance',
    'Marine, aviation and transport insurance',
    'Fire and other damage to property insurance',
    'General liability insurance',
    'Credit and suretyship insurance'
]

LIFE_LOB = [
    'Insurance with profit participation',
    'Index-linked and unit-linked insurance',
    'Other life insurance'
]

def generate_lei():
    return '549300' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))

def random_amount(min_val, max_val, precision=2):
    return round(np.random.uniform(min_val, max_val), precision)

def random_percentage(min_val=0, max_val=100):
    return round(np.random.uniform(min_val, max_val), 4)


# ============================================================================
# IR3003 - Non-Life Outwards Reinsurance Contract Information
# ============================================================================

def generate_ir3003_non_life_ri_contracts():
    """
    IR3003 - Non-Life Outwards Reinsurance Contract Information
    Details of outwards reinsurance contracts for non-life business.
    """
    data = []

    ri_types = ['Quota Share', 'Surplus', 'Excess of Loss', 'Stop Loss', 'Aggregate XL']
    coverage_types = ['Property', 'Casualty', 'Marine', 'Motor', 'Multi-Line']

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            for _ in range(random.randint(5, 20)):
                ri_type = random.choice(ri_types)
                ceded_premium = random_amount(500_000, 50_000_000)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Contract_ID': f'RI_{random.randint(10000, 99999)}',
                    'Contract_Name': f'{ri_type} - {random.choice(coverage_types)}',
                    'Reinsurance_Type': ri_type,
                    'Coverage_Type': random.choice(coverage_types),
                    'Line_Of_Business': random.choice(NON_LIFE_LOB),
                    'Inception_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') -
                                      timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
                    'Expiry_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') +
                                   timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d'),
                    'Cession_Rate_Pct': random_percentage(10, 70) if ri_type in ['Quota Share', 'Surplus'] else None,
                    'Premium_Ceded': ceded_premium,
                    'Commission_Received': ceded_premium * random_percentage(20, 35) / 100,
                    'Claims_Recoverable': random_amount(100_000, ceded_premium * 2),
                    'Attachment_Point': random_amount(1_000_000, 20_000_000) if 'XL' in ri_type or ri_type == 'Excess of Loss' else None,
                    'Limit': random_amount(10_000_000, 200_000_000),
                    'Number_Of_Reinstatements': random.randint(0, 3) if 'XL' in ri_type else None,
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR3004 - Non-Life Outwards Reinsurance Reinsurer Exposures
# ============================================================================

def generate_ir3004_non_life_ri_exposures():
    """
    IR3004 - Non-Life Outwards Reinsurance Contract Reinsurer Exposures
    Exposures to reinsurers under non-life contracts.
    """
    data = []

    reinsurer_names = [
        'Munich Re', 'Swiss Re', 'Hannover Re', 'SCOR', 'Berkshire Hathaway',
        'Lloyd\'s', 'PartnerRe', 'Everest Re', 'RenaissanceRe', 'Transatlantic Re'
    ]

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            for reinsurer in random.sample(reinsurer_names, random.randint(3, 7)):
                exposure = random_amount(5_000_000, 200_000_000)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Reinsurer_Name': reinsurer,
                    'Reinsurer_LEI': generate_lei(),
                    'Reinsurer_Country': random.choice(['DE', 'CH', 'BM', 'US', 'GB', 'FR']),
                    'Credit_Rating': random.choice(['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A']),
                    'Rating_Agency': random.choice(['S&P', 'Moody\'s', 'AM Best', 'Fitch']),
                    'Premium_Ceded_Total': exposure * random_percentage(5, 15) / 100,
                    'Recoverables_Claims_Outstanding': exposure * random_percentage(40, 60) / 100,
                    'Recoverables_IBNR': exposure * random_percentage(20, 40) / 100,
                    'Total_Recoverables': exposure,
                    'Collateral_Held': exposure * random_percentage(0, 30) / 100,
                    'Net_Exposure': exposure * random_percentage(70, 100) / 100,
                    'SCR_Counterparty_Contribution': exposure * random_percentage(3, 10) / 100,
                    'Concentration_Percentage': random_percentage(2, 25),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR3005 - Reinsurer and Collateral Provider Entity Information
# ============================================================================

def generate_ir3005_reinsurer_entity_info():
    """
    IR3005 - Reinsurer and Collateral Provider Entity Information
    Detailed information on reinsurers and collateral providers.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        for _ in range(random.randint(5, 15)):
            entity_type = random.choice(['Reinsurer', 'Collateral Provider', 'LOC Provider'])

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Entity_LEI': generate_lei(),
                'Entity_Name': f'{entity_type} Entity {random.randint(1, 100)}',
                'Entity_Type': entity_type,
                'Country_Of_Domicile': random.choice(COUNTRIES),
                'Authorisation_Status': random.choice(['Authorised', 'Equivalent Jurisdiction', 'Non-Equivalent']),
                'Credit_Rating': random.choice(['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+']),
                'Rating_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') -
                               timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
                'Solvency_Ratio': random_percentage(120, 250) if entity_type == 'Reinsurer' else None,
                'Total_Exposure': random_amount(5_000_000, 200_000_000),
                'Collateral_Type': random.choice(['Cash', 'Government Bonds', 'LOC', 'Trust Fund']) if entity_type != 'Reinsurer' else None,
                'Collateral_Value': random_amount(1_000_000, 100_000_000) if entity_type != 'Reinsurer' else None,
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# IR3006 - Life Outwards Reinsurance Summary
# ============================================================================

def generate_ir3006_life_ri_summary():
    """
    IR3006 - Life Outwards Reinsurance Summary
    Summary of life reinsurance arrangements.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            for lob in LIFE_LOB:
                gross_be = random_amount(50_000_000, 500_000_000)
                ri_recoverables = gross_be * random_percentage(10, 30) / 100

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Line_Of_Business': lob,
                    'Gross_Best_Estimate': gross_be,
                    'RI_Recoverables': ri_recoverables,
                    'Net_Best_Estimate': gross_be - ri_recoverables,
                    'Premium_Ceded': gross_be * random_percentage(5, 15) / 100,
                    'Commission_Received': gross_be * random_percentage(1, 5) / 100,
                    'Number_Of_Treaties': random.randint(2, 10),
                    'Largest_Single_Exposure': ri_recoverables * random_percentage(20, 50) / 100,
                    'Weighted_Average_Rating': random.choice(['AA', 'AA-', 'A+', 'A']),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR3007 - Life Outwards Proportional Reinsurance
# ============================================================================

def generate_ir3007_life_ri_proportional():
    """
    IR3007 - Life Outwards Proportional Reinsurance
    Details of proportional reinsurance for life business.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            for _ in range(random.randint(2, 8)):
                original_sum_assured = random_amount(100_000_000, 2_000_000_000)
                cession_rate = random_percentage(20, 60)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Treaty_ID': f'LIFE_QS_{random.randint(1000, 9999)}',
                    'Treaty_Type': random.choice(['Quota Share', 'Surplus', 'Facultative']),
                    'Line_Of_Business': random.choice(LIFE_LOB),
                    'Reinsurer_Name': f'Life Reinsurer {random.randint(1, 20)}',
                    'Reinsurer_LEI': generate_lei(),
                    'Inception_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') -
                                      timedelta(days=random.randint(365, 1825))).strftime('%Y-%m-%d'),
                    'Cession_Rate_Pct': cession_rate,
                    'Original_Sum_Assured': original_sum_assured,
                    'Ceded_Sum_Assured': original_sum_assured * cession_rate / 100,
                    'Original_Premium': original_sum_assured * random_percentage(1, 3) / 100,
                    'Ceded_Premium': original_sum_assured * cession_rate / 100 * random_percentage(0.8, 1.5) / 100,
                    'Commission_Rate_Pct': random_percentage(25, 45),
                    'Profit_Commission_Rate_Pct': random_percentage(10, 30),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR3008 - Life Outwards Non-Proportional Reinsurance
# ============================================================================

def generate_ir3008_life_ri_non_proportional():
    """
    IR3008 - Life Outwards Non-Proportional Reinsurance
    Details of non-proportional reinsurance for life business.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            for _ in range(random.randint(1, 5)):
                retention = random_amount(500_000, 5_000_000)
                limit = retention * random.randint(5, 20)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Treaty_ID': f'LIFE_XL_{random.randint(1000, 9999)}',
                    'Treaty_Type': random.choice(['Individual XL', 'Catastrophe XL', 'Stop Loss']),
                    'Line_Of_Business': random.choice(LIFE_LOB),
                    'Reinsurer_Name': f'Life Reinsurer {random.randint(1, 20)}',
                    'Reinsurer_LEI': generate_lei(),
                    'Retention': retention,
                    'Limit': limit,
                    'Annual_Aggregate_Limit': limit * random.randint(2, 5),
                    'Premium_Paid': limit * random_percentage(1, 5) / 100,
                    'Claims_Recovered_YTD': random_amount(0, limit * 0.5),
                    'Reinstatements': random.randint(1, 3),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR3101 - Outwards Reinsurance Balance Sheet Exposures
# ============================================================================

def generate_ir3101_ri_balance_sheet():
    """
    IR3101 - Outwards Reinsurance Balance Sheet Exposures
    Balance sheet exposures arising from reinsurance.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        for reinsurer_idx in range(random.randint(3, 10)):
            gross_recoverables = random_amount(5_000_000, 150_000_000)

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Reinsurer_Name': f'Reinsurer {reinsurer_idx + 1}',
                'Reinsurer_LEI': generate_lei(),
                'Reinsurer_Rating': random.choice(['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A']),
                # Asset side
                'Recoverables_Claims_Outstanding': gross_recoverables * random_percentage(40, 60) / 100,
                'Recoverables_IBNR': gross_recoverables * random_percentage(25, 40) / 100,
                'Recoverables_Premium_Provisions': gross_recoverables * random_percentage(10, 20) / 100,
                'Total_Recoverables_Gross': gross_recoverables,
                'Bad_Debt_Adjustment': gross_recoverables * random_percentage(-5, -1) / 100,
                'Total_Recoverables_Net': gross_recoverables * random_percentage(95, 99) / 100,
                'Receivables_From_Reinsurers': random_amount(100_000, 10_000_000),
                # Liability side
                'Payables_To_Reinsurers': random_amount(100_000, 8_000_000),
                'Deposits_From_Reinsurers': random_amount(0, 20_000_000),
                # Net exposure
                'Net_Balance_Sheet_Exposure': gross_recoverables * random_percentage(80, 100) / 100,
                'Collateral_Held': gross_recoverables * random_percentage(0, 30) / 100,
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# IR3201 - Undertakings in Scope of Group
# ============================================================================

def generate_ir3201_group_scope():
    """
    IR3201 - Undertakings in the Scope of the Group
    List of undertakings included in group supervision.
    """
    data = []

    undertaking_categories = [
        ('Insurance Undertaking', 'Method 1'),
        ('Reinsurance Undertaking', 'Method 1'),
        ('Insurance Holding Company', 'Method 1'),
        ('Mixed Financial Holding Company', 'Method 1'),
        ('Ancillary Services Undertaking', 'Method 2'),
        ('Credit Institution', 'Method 2'),
        ('Investment Firm', 'Method 2'),
    ]

    # Create a sample group structure
    group_entities = []
    for i in range(10):
        cat = random.choice(undertaking_categories)
        group_entities.append({
            'entity_name': f'Group Entity {i+1}',
            'category': cat[0],
            'method': cat[1],
            'country': random.choice(COUNTRIES)
        })

    for entity in group_entities:
        ownership_pct = random_percentage(20, 100)

        data.append({
            'Group_Name': 'Sample Insurance Group',
            'Group_LEI': generate_lei(),
            'Reporting_Date': REPORTING_DATE,
            'Entity_Name': entity['entity_name'],
            'Entity_LEI': generate_lei(),
            'Entity_Category': entity['category'],
            'Country': entity['country'],
            'Supervisory_Authority': f'Regulator - {entity["country"]}',
            'Inclusion_Method': entity['method'],
            'Proportional_Share_Used': ownership_pct if entity['method'] == 'Method 1' else None,
            'Ownership_Percentage': ownership_pct,
            'Voting_Rights_Percentage': ownership_pct,
            'Group_Solvency_Contribution': random_amount(5_000_000, 200_000_000) if 'Insurance' in entity['category'] else 0,
            'Contribution_To_Group_Own_Funds': random_amount(10_000_000, 300_000_000) if 'Insurance' in entity['category'] else 0,
            'Contribution_To_Group_SCR': random_amount(3_000_000, 100_000_000) if 'Insurance' in entity['category'] else 0,
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


# ============================================================================
# IR3301 - Insurance/Reinsurance Individual Requirements
# ============================================================================

def generate_ir3301_individual_requirements():
    """
    IR3301 - Insurance and Reinsurance Individual Requirements
    Individual capital requirements for group entities.
    """
    data = []

    for i in range(5):
        own_funds = random_amount(50_000_000, 500_000_000)
        scr = own_funds * random_percentage(40, 70) / 100
        mcr = scr * random_percentage(25, 45) / 100

        data.append({
            'Group_Name': 'Sample Insurance Group',
            'Reporting_Date': REPORTING_DATE,
            'Entity_Name': f'Insurance Entity {i+1}',
            'Entity_LEI': generate_lei(),
            'Country': random.choice(['GB', 'DE', 'FR', 'IE']),
            'Entity_Type': random.choice(['Non-Life Insurer', 'Life Insurer', 'Composite', 'Reinsurer']),
            # Own Funds
            'Tier_1_Unrestricted': own_funds * random_percentage(60, 80) / 100,
            'Tier_1_Restricted': own_funds * random_percentage(5, 15) / 100,
            'Tier_2': own_funds * random_percentage(5, 15) / 100,
            'Tier_3': own_funds * random_percentage(0, 5) / 100,
            'Total_Eligible_Own_Funds_SCR': own_funds,
            'Total_Eligible_Own_Funds_MCR': own_funds * random_percentage(85, 95) / 100,
            # Capital Requirements
            'SCR': scr,
            'MCR': mcr,
            'Local_Regulatory_Capital': scr * random_percentage(80, 120) / 100,
            # Ratios
            'SCR_Ratio': own_funds / scr * 100,
            'MCR_Ratio': (own_funds * random_percentage(85, 95) / 100) / mcr * 100,
            # Restrictions
            'Non_Available_Own_Funds': random_amount(0, own_funds * 0.1),
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


# ============================================================================
# IR3401 - Other Regulated/Non-Regulated Financial Undertakings
# ============================================================================

def generate_ir3401_other_undertakings():
    """
    IR3401 - Other Regulated and Non-Regulated Financial Undertakings
    Information on non-insurance financial entities in the group.
    """
    data = []

    entity_types = [
        'Credit Institution',
        'Investment Firm',
        'UCITS Management Company',
        'AIFM',
        'Pension Fund',
        'Non-Regulated SPV'
    ]

    for entity_type in entity_types:
        if random.random() > 0.4:  # 60% chance of having this type
            data.append({
                'Group_Name': 'Sample Insurance Group',
                'Reporting_Date': REPORTING_DATE,
                'Entity_Name': f'{entity_type} Entity',
                'Entity_LEI': generate_lei(),
                'Entity_Type': entity_type,
                'Country': random.choice(COUNTRIES),
                'Regulatory_Framework': 'CRD IV' if 'Credit' in entity_type or 'Investment' in entity_type else 'UCITS' if 'UCITS' in entity_type else 'AIFMD' if 'AIFM' in entity_type else 'IORP II' if 'Pension' in entity_type else 'None',
                'Total_Balance_Sheet': random_amount(50_000_000, 1_000_000_000),
                'Regulatory_Own_Funds': random_amount(10_000_000, 200_000_000),
                'Regulatory_Capital_Requirement': random_amount(5_000_000, 100_000_000),
                'Capital_Surplus_Deficit': random_amount(5_000_000, 100_000_000),
                'Method_Of_Inclusion': random.choice(['Deduction', 'Method 2', 'Sectoral']),
                'Intra_Group_Exposures': random_amount(1_000_000, 50_000_000),
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# IR3501 - Contribution to Group Technical Provisions
# ============================================================================

def generate_ir3501_group_tp_contribution():
    """
    IR3501 - Contribution to Group Technical Provisions
    Technical provisions contribution by group entity.
    """
    data = []

    for i in range(5):
        gross_be = random_amount(100_000_000, 2_000_000_000)
        ri_recoverables = gross_be * random_percentage(10, 30) / 100

        data.append({
            'Group_Name': 'Sample Insurance Group',
            'Reporting_Date': REPORTING_DATE,
            'Entity_Name': f'Insurance Entity {i+1}',
            'Entity_LEI': generate_lei(),
            'Country': random.choice(['GB', 'DE', 'FR', 'IE']),
            # By LOB Category
            'TP_Non_Life_Gross': gross_be * random_percentage(50, 80) / 100 if random.random() > 0.3 else 0,
            'TP_Non_Life_RI_Recoverable': ri_recoverables * random_percentage(50, 80) / 100 if random.random() > 0.3 else 0,
            'TP_Life_Gross': gross_be * random_percentage(20, 50) / 100 if random.random() > 0.5 else 0,
            'TP_Life_RI_Recoverable': ri_recoverables * random_percentage(20, 50) / 100 if random.random() > 0.5 else 0,
            'TP_Health_SLT_Gross': gross_be * random_percentage(5, 15) / 100 if random.random() > 0.7 else 0,
            'TP_Health_SLT_RI_Recoverable': ri_recoverables * random_percentage(5, 15) / 100 if random.random() > 0.7 else 0,
            # Totals
            'Total_Gross_Best_Estimate': gross_be,
            'Total_RI_Recoverables': ri_recoverables,
            'Total_Net_Best_Estimate': gross_be - ri_recoverables,
            'Risk_Margin': (gross_be - ri_recoverables) * random_percentage(4, 8) / 100,
            'Total_Technical_Provisions': gross_be + (gross_be - ri_recoverables) * random_percentage(4, 8) / 100,
            'Percentage_Of_Group_TP': random_percentage(5, 40),
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


# ============================================================================
# IR3601 - IGT Equity-Type Transactions, Debt and Asset Transfer
# ============================================================================

def generate_ir3601_igt_equity_debt():
    """
    IR3601 - IGT Equity-Type Transactions, Debt and Asset Transfer
    Intra-group equity, debt and asset transfers.
    """
    data = []

    transaction_types = [
        'Equity Investment', 'Subordinated Loan', 'Senior Debt',
        'Dividend', 'Capital Injection', 'Asset Transfer'
    ]

    for trans_type in transaction_types:
        for _ in range(random.randint(1, 3)):
            amount = random_amount(5_000_000, 200_000_000)

            data.append({
                'Group_Name': 'Sample Insurance Group',
                'Reporting_Date': REPORTING_DATE,
                'Transaction_ID': f'IGT_{random.randint(10000, 99999)}',
                'Transaction_Type': trans_type,
                'Investor_Entity': f'Group Entity {random.randint(1, 5)}',
                'Investor_LEI': generate_lei(),
                'Issuer_Entity': f'Group Entity {random.randint(6, 10)}',
                'Issuer_LEI': generate_lei(),
                'Transaction_Amount': amount,
                'Interest_Rate': random_percentage(2, 8) if 'Loan' in trans_type or 'Debt' in trans_type else None,
                'Maturity_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') +
                                 timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d') if 'Loan' in trans_type or 'Debt' in trans_type else None,
                'Transaction_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') -
                                    timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d'),
                'Own_Funds_Impact_Investor': -amount if trans_type in ['Equity Investment', 'Subordinated Loan', 'Capital Injection'] else amount if trans_type == 'Dividend' else 0,
                'Own_Funds_Impact_Issuer': amount if trans_type in ['Equity Investment', 'Subordinated Loan', 'Capital Injection'] else -amount if trans_type == 'Dividend' else 0,
                'Regulatory_Approval_Required': random.choice(['Yes', 'No']),
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# IR3602 - IGT Derivatives
# ============================================================================

def generate_ir3602_igt_derivatives():
    """
    IR3602 - IGT Derivatives
    Intra-group derivative transactions.
    """
    data = []

    derivative_types = ['Interest Rate Swap', 'FX Forward', 'Currency Swap', 'Total Return Swap']

    for deriv_type in derivative_types:
        if random.random() > 0.5:
            notional = random_amount(10_000_000, 500_000_000)
            mtm = random_amount(-notional * 0.05, notional * 0.05)

            data.append({
                'Group_Name': 'Sample Insurance Group',
                'Reporting_Date': REPORTING_DATE,
                'Transaction_ID': f'IGT_DERIV_{random.randint(10000, 99999)}',
                'Derivative_Type': deriv_type,
                'Payer_Entity': f'Group Entity {random.randint(1, 5)}',
                'Payer_LEI': generate_lei(),
                'Receiver_Entity': f'Group Entity {random.randint(6, 10)}',
                'Receiver_LEI': generate_lei(),
                'Notional_Amount': notional,
                'Mark_To_Market_Value': mtm,
                'Trade_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') -
                              timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d'),
                'Maturity_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') +
                                 timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d'),
                'Fixed_Rate': random_percentage(1, 5) if 'Swap' in deriv_type else None,
                'Floating_Rate_Benchmark': 'SONIA' if 'Interest' in deriv_type else 'N/A',
                'Collateral_Posted': max(0, -mtm) * random_percentage(90, 110) / 100,
                'Collateral_Received': max(0, mtm) * random_percentage(90, 110) / 100,
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# IR3604 - IGT Cost Sharing, Contingent Liabilities, Off-BS Items
# ============================================================================

def generate_ir3604_igt_other():
    """
    IR3604 - IGT Cost Sharing, Contingent Liabilities, Off-BS and Other Items
    Other intra-group transactions.
    """
    data = []

    transaction_types = [
        'Cost Sharing Agreement', 'Management Fee', 'Guarantee Given',
        'Guarantee Received', 'Contingent Liability', 'Off-Balance Sheet Commitment'
    ]

    for trans_type in transaction_types:
        if random.random() > 0.4:
            amount = random_amount(500_000, 50_000_000)

            data.append({
                'Group_Name': 'Sample Insurance Group',
                'Reporting_Date': REPORTING_DATE,
                'Transaction_ID': f'IGT_OTHER_{random.randint(10000, 99999)}',
                'Transaction_Type': trans_type,
                'Provider_Entity': f'Group Entity {random.randint(1, 5)}',
                'Provider_LEI': generate_lei(),
                'Recipient_Entity': f'Group Entity {random.randint(6, 10)}',
                'Recipient_LEI': generate_lei(),
                'Annual_Amount': amount if 'Fee' in trans_type or 'Cost' in trans_type else None,
                'Maximum_Amount': amount * random.randint(1, 10) if 'Guarantee' in trans_type or 'Commitment' in trans_type else None,
                'Current_Exposure': amount,
                'Effective_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') -
                                  timedelta(days=random.randint(365, 1825))).strftime('%Y-%m-%d'),
                'Expiry_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') +
                               timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d'),
                'Probability_Of_Trigger': random_percentage(0, 20) if 'Contingent' in trans_type else None,
                'Impact_On_Own_Funds': random_amount(-5_000_000, 5_000_000),
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# IRR2202 - Matching Adjustment Portfolio Projection of Future Cash Flows
# ============================================================================

def generate_irr2202_ma_cash_flows():
    """
    IRR2202 - Matching Adjustment Portfolio Projection of Future Cash Flows
    Cash flow projections for matching adjustment portfolios.
    """
    data = []

    projection_years = list(range(1, 51))  # 50 year projection

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite'] and random.random() > 0.5:
            initial_liability_cf = random_amount(10_000_000, 100_000_000)
            initial_asset_cf = initial_liability_cf * random_percentage(98, 102) / 100

            for year in projection_years:
                liability_factor = 0.95 ** (year - 1)
                asset_factor = liability_factor * random_percentage(98, 102) / 100

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Portfolio_ID': f'MA_PORT_{undertaking["lei"][:6]}',
                    'Projection_Year': year,
                    # Liability Cash Flows
                    'Liability_Cash_Flow': initial_liability_cf * liability_factor,
                    'Liability_PV': initial_liability_cf * liability_factor / ((1 + 0.03) ** year),
                    # Asset Cash Flows
                    'Asset_Cash_Flow': initial_asset_cf * asset_factor,
                    'Asset_PV': initial_asset_cf * asset_factor / ((1 + 0.03) ** year),
                    # Mismatch
                    'Cash_Flow_Mismatch': (initial_asset_cf * asset_factor) - (initial_liability_cf * liability_factor),
                    'Cumulative_Mismatch': random_amount(-5_000_000, 5_000_000),
                    # Discount Rates
                    'Risk_Free_Rate': random_percentage(2.5, 4),
                    'Fundamental_Spread': random_percentage(0.3, 0.8),
                    'Matching_Adjustment': random_percentage(0.5, 1.5),
                    'Adjusted_Discount_Rate': random_percentage(3.5, 6),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IRR2203 - Matching Adjustment Calculation
# ============================================================================

def generate_irr2203_ma_calculation():
    """
    IRR2203 - Matching Adjustment Calculation
    Detailed calculation of the matching adjustment.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite'] and random.random() > 0.5:
            asset_value = random_amount(500_000_000, 5_000_000_000)

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Portfolio_ID': f'MA_PORT_{undertaking["lei"][:6]}',
                # Asset Information
                'Total_Assets_Market_Value': asset_value,
                'Asset_Spread': random_percentage(1, 3),
                'Weighted_Average_Duration': random_percentage(8, 20),
                'Weighted_Average_Rating': random.choice(['AA', 'A', 'BBB']),
                # Fundamental Spread Calculation
                'Probability_Of_Default': random_percentage(0.1, 1),
                'Cost_Of_Downgrade': random_percentage(0.1, 0.5),
                'Fundamental_Spread': random_percentage(0.3, 0.8),
                # Matching Adjustment Calculation
                'Risk_Corrected_Spread': random_percentage(0.5, 2),
                'Matching_Adjustment_BPS': random_percentage(50, 150),
                # Impact
                'TP_Without_MA': asset_value * random_percentage(90, 100) / 100,
                'TP_With_MA': asset_value * random_percentage(80, 95) / 100,
                'MA_Impact_On_TP': asset_value * random_percentage(-10, -3) / 100,
                'MA_Impact_On_Own_Funds': asset_value * random_percentage(3, 10) / 100,
                # Compliance
                'Cash_Flow_Matching_Test': 'Pass',
                'Currency_Matching_Test': 'Pass',
                'Concentration_Test': 'Pass',
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# Power BI Execution
# ============================================================================

if __name__ == "__main__":
    print("Generating Reinsurance and Group QRTs...")

# Generate all tables for Power BI
IR3003_Non_Life_RI_Contracts = generate_ir3003_non_life_ri_contracts()
IR3004_Non_Life_RI_Exposures = generate_ir3004_non_life_ri_exposures()
IR3005_Reinsurer_Entity_Info = generate_ir3005_reinsurer_entity_info()
IR3006_Life_RI_Summary = generate_ir3006_life_ri_summary()
IR3007_Life_RI_Proportional = generate_ir3007_life_ri_proportional()
IR3008_Life_RI_Non_Proportional = generate_ir3008_life_ri_non_proportional()
IR3101_RI_Balance_Sheet = generate_ir3101_ri_balance_sheet()
IR3201_Group_Scope = generate_ir3201_group_scope()
IR3301_Individual_Requirements = generate_ir3301_individual_requirements()
IR3401_Other_Undertakings = generate_ir3401_other_undertakings()
IR3501_Group_TP_Contribution = generate_ir3501_group_tp_contribution()
IR3601_IGT_Equity_Debt = generate_ir3601_igt_equity_debt()
IR3602_IGT_Derivatives = generate_ir3602_igt_derivatives()
IR3604_IGT_Other = generate_ir3604_igt_other()
IRR2202_MA_Cash_Flows = generate_irr2202_ma_cash_flows()
IRR2203_MA_Calculation = generate_irr2203_ma_calculation()
