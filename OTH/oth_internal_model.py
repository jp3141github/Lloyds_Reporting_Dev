"""
PRA/BoE Other Templates - Internal Model and Analysis of Change
================================================================
Non-IR regulatory templates for internal model reporting.

Templates:
- AOC01: Analysis of Change in SCR
- IM00: Internal Model Submission Content
- IM01: Internal Model Outputs (Life)
- IM02: Internal Model Counterparty Risk
- IM03: Internal Model Outputs (Non-Life)
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random
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


def generate_lei():
    """Generate a random LEI code"""
    return '549300' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))


def random_amount(min_val, max_val, precision=2):
    """Generate a random monetary amount"""
    return round(np.random.uniform(min_val, max_val), precision)


def random_percentage(min_val=0, max_val=100):
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
        opening_scr = random_amount(100_000_000, 500_000_000)

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
# IM00 - Internal Model Submission Content
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


# ============================================================================
# IM01 - Internal Model Outputs (Life)
# ============================================================================

def generate_im01_life_outputs():
    """
    IM01 - Internal Model Outputs (Life)
    Life insurance internal model outputs.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            for lob in LIFE_LOB[:3]:
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


# ============================================================================
# IM02 - Internal Model Counterparty Risk
# ============================================================================

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


# ============================================================================
# IM03 - Internal Model Outputs (Non-Life)
# ============================================================================

def generate_im03_non_life_outputs():
    """
    IM03 - Internal Model Outputs (Non-Life)
    Non-life insurance internal model outputs.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            for lob in NON_LIFE_LOB[:8]:
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


# Export all functions
__all__ = [
    'generate_aoc01_analysis_of_change',
    'generate_im00_submission_content',
    'generate_im01_life_outputs',
    'generate_im02_counterparty_risk',
    'generate_im03_non_life_outputs',
    'UNDERTAKINGS',
    'REPORTING_DATE',
]
