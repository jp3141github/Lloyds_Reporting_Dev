"""
PRA/BoE QRT Generator - Own Funds and Capital Templates (IR23, IR25-28)
=======================================================================
Actuarial-focused capital and solvency templates for Solvency II reporting.

Templates:
- IR2301: Own Funds
- IR2302: Detailed Information by Tiers on Own Funds
- IR2303: Annual Movements on Own Funds
- IR2304: List of Items on Own Funds
- IR2305: Society of Lloyd's Own Funds and Capital Requirements
- IR2504: Solvency Capital Requirement
- IR2505: SCR - Partial or Full Internal Model Components
- IR2506: SCR - Loss Absorbing Capacity of Deferred Taxes
- IR2601: SCR - Market Risk
- IR2602: SCR - Counterparty Default Risk
- IR2603: SCR - Life Underwriting Risk
- IR2604: SCR - Health Underwriting Risk
- IR2605: SCR - Non-Life Underwriting Risk
- IR2606: SCR - Operational Risk
- IR2607: SCR - Simplifications
- IR2701: SCR - Non-Life and Health Catastrophe Risk
- IR2801: MCR - Only Life or Only Non-Life Activity
- IR2802: MCR - Both Life and Non-Life Activity
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random
from typing import Dict, List

from .qrt_balance_sheet import (
    UNDERTAKINGS, REPORTING_DATE, PREVIOUS_REPORTING_DATE,
    random_amount, random_percentage, generate_lei
)

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


# ============================================================================
# IR2301 - Own Funds
# ============================================================================

def generate_ir2301_own_funds():
    """
    IR2301 - Own Funds
    Summary of eligible own funds and capital composition.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        total_of = random_amount(200_000_000, 800_000_000)
        scr = random_amount(100_000_000, 400_000_000)
        mcr = scr * np.random.uniform(0.25, 0.35)

        row = {
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # Basic Own Funds
            'Ordinary_Share_Capital': random_amount(50_000_000, 200_000_000),
            'Share_Premium': random_amount(10_000_000, 100_000_000),
            'Initial_Funds': random_amount(0, 20_000_000),
            'Subordinated_Mutual_Members_Accounts': random_amount(0, 10_000_000),
            'Surplus_Funds': random_amount(0, 30_000_000),
            'Preference_Shares': random_amount(0, 50_000_000),
            'Reconciliation_Reserve': random_amount(50_000_000, 300_000_000),
            'Subordinated_Liabilities': random_amount(0, 100_000_000),
            'Deductions': random_amount(-50_000_000, 0),
            'Total_Basic_Own_Funds': total_of * np.random.uniform(0.90, 1.0),
            # Ancillary Own Funds
            'Ancillary_Unpaid_Share_Capital': random_amount(0, 20_000_000),
            'Ancillary_Letters_Of_Credit': random_amount(0, 30_000_000),
            'Ancillary_Other': random_amount(0, 10_000_000),
            'Total_Ancillary_Own_Funds': random_amount(0, 60_000_000),
            # Eligible Own Funds
            'Eligible_OF_To_Meet_SCR': total_of,
            'Eligible_OF_To_Meet_MCR': total_of * np.random.uniform(0.85, 0.95),
            # Tier Split
            'Tier_1_Unrestricted': total_of * np.random.uniform(0.70, 0.85),
            'Tier_1_Restricted': total_of * np.random.uniform(0.05, 0.15),
            'Tier_2': total_of * np.random.uniform(0.05, 0.15),
            'Tier_3': total_of * np.random.uniform(0, 0.05),
            # Capital Requirements
            'SCR': scr,
            'MCR': mcr,
            # Ratios
            'SCR_Ratio': round(total_of / scr * 100, 2),
            'MCR_Ratio': round(total_of * 0.9 / mcr * 100, 2),
        }
        data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2302 - Detailed Information by Tiers on Own Funds
# ============================================================================

def generate_ir2302_own_funds_by_tier():
    """
    IR2302 - Detailed Information by Tiers on Own Funds
    Breakdown of own funds by tier and item type.
    """
    data = []

    tier_items = [
        ('Tier 1 - Unrestricted', 'Ordinary Share Capital', 1, 0),
        ('Tier 1 - Unrestricted', 'Share Premium', 1, 0),
        ('Tier 1 - Unrestricted', 'Reconciliation Reserve', 1, 0),
        ('Tier 1 - Unrestricted', 'Initial Funds', 1, 0),
        ('Tier 1 - Restricted', 'Preference Shares', 1, 1),
        ('Tier 1 - Restricted', 'Subordinated Liabilities (Tier 1)', 1, 1),
        ('Tier 2', 'Subordinated Liabilities (Tier 2)', 2, 0),
        ('Tier 2', 'Ancillary Own Funds (Tier 2)', 2, 0),
        ('Tier 3', 'Deferred Tax Assets', 3, 0),
        ('Tier 3', 'Subordinated Liabilities (Tier 3)', 3, 0),
    ]

    for undertaking in UNDERTAKINGS:
        total_of = random_amount(200_000_000, 800_000_000)

        for tier_name, item_name, tier_num, restricted in tier_items:
            weight = {
                'Ordinary Share Capital': 0.25,
                'Share Premium': 0.10,
                'Reconciliation Reserve': 0.35,
                'Initial Funds': 0.05,
                'Preference Shares': 0.05,
                'Subordinated Liabilities (Tier 1)': 0.05,
                'Subordinated Liabilities (Tier 2)': 0.08,
                'Ancillary Own Funds (Tier 2)': 0.03,
                'Deferred Tax Assets': 0.02,
                'Subordinated Liabilities (Tier 3)': 0.02,
            }.get(item_name, 0.05)

            amount = total_of * weight * np.random.uniform(0.8, 1.2)

            row = {
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Tier': tier_name,
                'Tier_Number': tier_num,
                'Restricted': bool(restricted),
                'Item_Name': item_name,
                'Amount': round(amount, 2),
                'Eligible_For_SCR': round(amount, 2),
                'Eligible_For_MCR': round(amount * (1 if tier_num <= 2 else 0), 2),
                'Limit_Applied': random.choice([True, False]),
                'Limit_Amount': round(amount * 0.2, 2) if random.choice([True, False]) else 0,
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2303 - Annual Movements on Own Funds
# ============================================================================

def generate_ir2303_own_funds_movements():
    """
    IR2303 - Annual Movements on Own Funds
    Reconciliation of opening to closing own funds.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        opening_of = random_amount(180_000_000, 750_000_000)

        row = {
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            'Previous_Reporting_Date': PREVIOUS_REPORTING_DATE,
            'Opening_Own_Funds': opening_of,
            # Movements
            'Profit_Loss_Recognised': random_amount(-50_000_000, 100_000_000),
            'Dividends_Paid': random_amount(-30_000_000, 0),
            'Share_Capital_Issued': random_amount(0, 50_000_000),
            'Share_Capital_Redeemed': random_amount(-20_000_000, 0),
            'Subordinated_Liabilities_Issued': random_amount(0, 30_000_000),
            'Subordinated_Liabilities_Redeemed': random_amount(-20_000_000, 0),
            'Change_In_Revaluation_Reserve': random_amount(-20_000_000, 30_000_000),
            'Change_In_Pension_Surplus': random_amount(-5_000_000, 5_000_000),
            'Currency_Translation': random_amount(-10_000_000, 10_000_000),
            'Change_In_Deferred_Taxes': random_amount(-15_000_000, 15_000_000),
            'Change_In_TP_Valuation': random_amount(-30_000_000, 30_000_000),
            'Other_Movements': random_amount(-10_000_000, 10_000_000),
            'Closing_Own_Funds': opening_of * np.random.uniform(0.95, 1.15),
            # Tier Movements
            'Tier_1_Opening': opening_of * 0.80,
            'Tier_1_Movement': random_amount(-20_000_000, 40_000_000),
            'Tier_1_Closing': opening_of * 0.80 * np.random.uniform(0.95, 1.10),
            'Tier_2_Opening': opening_of * 0.15,
            'Tier_2_Movement': random_amount(-10_000_000, 15_000_000),
            'Tier_2_Closing': opening_of * 0.15 * np.random.uniform(0.90, 1.15),
            'Tier_3_Opening': opening_of * 0.05,
            'Tier_3_Movement': random_amount(-5_000_000, 5_000_000),
            'Tier_3_Closing': opening_of * 0.05 * np.random.uniform(0.85, 1.20),
        }
        data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2304 - List of Items on Own Funds
# ============================================================================

def generate_ir2304_own_funds_items():
    """
    IR2304 - List of Items on Own Funds
    Detailed listing of individual own funds items.
    """
    data = []

    item_types = [
        ('Share Capital', 'Ordinary Shares', 1, 'Unrestricted'),
        ('Share Capital', 'Preference Shares A', 1, 'Restricted'),
        ('Share Capital', 'Preference Shares B', 1, 'Restricted'),
        ('Subordinated', 'Sub Debt 2025', 2, 'N/A'),
        ('Subordinated', 'Sub Debt 2030', 2, 'N/A'),
        ('Subordinated', 'Sub Debt 2035', 3, 'N/A'),
        ('Ancillary', 'Letter of Credit - Bank A', 2, 'N/A'),
        ('Ancillary', 'Guarantee - Parent Co', 2, 'N/A'),
    ]

    for undertaking in UNDERTAKINGS:
        for category, item_name, tier, restricted in item_types:
            issue_date = f'{random.randint(2010, 2023)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}'
            maturity_date = f'{random.randint(2025, 2050)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}'

            row = {
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Item_ID': f'OF_{undertaking["lei"][:8]}_{random.randint(1000, 9999)}',
                'Category': category,
                'Item_Name': item_name,
                'Tier': tier,
                'Restricted': restricted,
                'Issue_Date': issue_date,
                'Maturity_Date': maturity_date if 'Sub' in item_name or 'Letter' in item_name else 'Perpetual',
                'Nominal_Amount': random_amount(10_000_000, 100_000_000),
                'Solvency_II_Value': random_amount(10_000_000, 100_000_000),
                'Coupon_Rate': random_percentage(3, 8) if 'Sub' in item_name else 0,
                'Currency': random.choice(['GBP', 'USD', 'EUR']),
                'Callable': random.choice([True, False]),
                'First_Call_Date': maturity_date if random.choice([True, False]) else None,
                'Approved_By_PRA': True,
                'Approval_Date': issue_date,
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2305 - Society of Lloyd's Own Funds and Capital Requirements
# ============================================================================

def generate_ir2305_lloyds_capital():
    """
    IR2305 - Society of Lloyd's Own Funds and Capital Requirements
    Lloyd's-specific capital requirements and funds at Lloyd's.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        scr = random_amount(100_000_000, 400_000_000)
        eca = scr * np.random.uniform(1.30, 1.50)

        row = {
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            'Syndicate_Number': undertaking['name'].split()[-1] if 'Syndicate' in undertaking['name'] else '0000',
            # Funds at Lloyd's
            'FAL_Required': eca,
            'FAL_Provided': eca * np.random.uniform(1.0, 1.20),
            'FAL_Surplus_Deficit': eca * np.random.uniform(0, 0.20),
            'FAL_LOC': random_amount(0, 50_000_000),
            'FAL_Cash': random_amount(10_000_000, 100_000_000),
            'FAL_Other_Approved': random_amount(0, 30_000_000),
            # Economic Capital
            'ECA': eca,
            'SCR': scr,
            'ECA_Over_SCR': round((eca / scr) * 100, 2),
            # Lloyd's Central Fund
            'Central_Fund_Contribution': random_amount(1_000_000, 10_000_000),
            'Callable_Layer': random_amount(5_000_000, 30_000_000),
            # Member Capital
            'Member_Balances': random_amount(50_000_000, 200_000_000),
            'Member_Deposits': random_amount(20_000_000, 80_000_000),
            # Capacity
            'Stamp_Capacity': random_amount(200_000_000, 1_000_000_000),
            'Premium_Income_Limit': random_amount(150_000_000, 800_000_000),
            'PIL_Utilisation': random_percentage(60, 95),
        }
        data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2504 - Solvency Capital Requirement
# ============================================================================

def generate_ir2504_scr():
    """
    IR2504 - Solvency Capital Requirement
    Summary SCR calculation using standard formula or internal model.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        bscr = random_amount(80_000_000, 350_000_000)

        row = {
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            'Calculation_Method': random.choice(['Standard Formula', 'Partial Internal Model', 'Full Internal Model']),
            # Risk Modules
            'Market_Risk': random_amount(30_000_000, 150_000_000),
            'Counterparty_Default_Risk': random_amount(10_000_000, 50_000_000),
            'Life_Underwriting_Risk': random_amount(5_000_000, 40_000_000),
            'Health_Underwriting_Risk': random_amount(5_000_000, 30_000_000),
            'Non_Life_Underwriting_Risk': random_amount(30_000_000, 150_000_000),
            'Diversification_BSCR': random_amount(-40_000_000, -15_000_000),
            'Intangible_Asset_Risk': random_amount(0, 5_000_000),
            'Basic_SCR': bscr,
            # Adjustments
            'Operational_Risk': random_amount(5_000_000, 30_000_000),
            'LAC_Technical_Provisions': random_amount(-20_000_000, 0),
            'LAC_Deferred_Taxes': random_amount(-30_000_000, -5_000_000),
            # Capital Add-ons
            'Capital_Add_On': random_amount(0, 10_000_000),
            # Final SCR
            'SCR': bscr * np.random.uniform(0.90, 1.15),
            # Other
            'USP_Applied': random.choice([True, False]),
            'Simplifications_Used': random.choice([True, False]),
        }
        data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2505 - SCR - Partial or Full Internal Model Components
# ============================================================================

def generate_ir2505_scr_internal_model():
    """
    IR2505 - SCR - Partial or Full Internal Model Components
    Internal model SCR components and comparison with standard formula.
    """
    data = []

    risk_components = [
        'Market Risk - Interest Rate',
        'Market Risk - Equity',
        'Market Risk - Property',
        'Market Risk - Spread',
        'Market Risk - Currency',
        'Market Risk - Concentration',
        'Counterparty Default Risk',
        'Non-Life Premium Risk',
        'Non-Life Reserve Risk',
        'Non-Life Catastrophe Risk',
        'Life Mortality Risk',
        'Life Longevity Risk',
        'Life Lapse Risk',
        'Operational Risk',
    ]

    for undertaking in UNDERTAKINGS:
        for component in risk_components:
            im_value = random_amount(5_000_000, 80_000_000)
            sf_value = im_value * np.random.uniform(0.8, 1.4)

            row = {
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Risk_Component': component,
                'Internal_Model_SCR': im_value,
                'Standard_Formula_SCR': sf_value,
                'Difference': im_value - sf_value,
                'Difference_Percentage': round((im_value / sf_value - 1) * 100, 2),
                'Model_Change_Impact': random_amount(-5_000_000, 5_000_000),
                'Validation_Status': random.choice(['Passed', 'Minor Issues', 'Under Review']),
                'Last_Validation_Date': '2024-06-30',
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2506 - SCR - Loss Absorbing Capacity of Deferred Taxes
# ============================================================================

def generate_ir2506_scr_lac_dt():
    """
    IR2506 - SCR - Loss Absorbing Capacity of Deferred Taxes
    Calculation of LAC DT adjustment to SCR.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        loss_before_tax = random_amount(100_000_000, 500_000_000)
        tax_rate = np.random.uniform(0.19, 0.25)

        row = {
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # Notional SCR
            'SCR_Before_LAC_DT': random_amount(100_000_000, 400_000_000),
            # DTA/DTL Position
            'DTA_Balance_Sheet': random_amount(10_000_000, 50_000_000),
            'DTL_Balance_Sheet': random_amount(20_000_000, 80_000_000),
            'Net_DT_Position': random_amount(-30_000_000, 30_000_000),
            # Loss Scenario
            'Notional_Loss_Pre_Tax': loss_before_tax,
            'Tax_Rate_Applied': round(tax_rate * 100, 2),
            'Maximum_LAC_DT': round(loss_before_tax * tax_rate, 2),
            # Recoverability
            'Future_Taxable_Profits': random_amount(50_000_000, 200_000_000),
            'Projection_Period_Years': random.randint(3, 10),
            'Carry_Forward_Losses': random_amount(0, 50_000_000),
            'Carry_Back_Available': random.choice([True, False]),
            # Final LAC DT
            'LAC_DT_Claimed': random_amount(10_000_000, 40_000_000),
            'LAC_DT_Percentage_Of_Max': random_percentage(50, 100),
            # Justification
            'Justification_Method': random.choice(['Profit Projection', 'Stress Testing', 'Look-Back']),
        }
        data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2601 - SCR - Market Risk
# ============================================================================

def generate_ir2601_scr_market_risk():
    """
    IR2601 - SCR - Market Risk
    Detailed market risk SCR sub-modules.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        row = {
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # Sub-modules
            'Interest_Rate_Risk_Up': random_amount(10_000_000, 60_000_000),
            'Interest_Rate_Risk_Down': random_amount(15_000_000, 70_000_000),
            'Interest_Rate_Risk': random_amount(15_000_000, 70_000_000),
            'Equity_Risk_Type1': random_amount(20_000_000, 100_000_000),
            'Equity_Risk_Type2': random_amount(10_000_000, 50_000_000),
            'Equity_Risk': random_amount(25_000_000, 120_000_000),
            'Property_Risk': random_amount(5_000_000, 40_000_000),
            'Spread_Risk_Bonds': random_amount(15_000_000, 80_000_000),
            'Spread_Risk_Securitisations': random_amount(2_000_000, 15_000_000),
            'Spread_Risk_Derivatives': random_amount(1_000_000, 10_000_000),
            'Spread_Risk': random_amount(18_000_000, 95_000_000),
            'Currency_Risk': random_amount(10_000_000, 60_000_000),
            'Concentration_Risk': random_amount(5_000_000, 30_000_000),
            # Diversification
            'Diversification_Market': random_amount(-30_000_000, -10_000_000),
            # Total
            'Total_Market_Risk': random_amount(50_000_000, 200_000_000),
            # Symmetric Adjustment
            'Equity_Dampener': random_percentage(-10, 10),
            'Dampener_Impact': random_amount(-5_000_000, 5_000_000),
        }
        data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2602 - SCR - Counterparty Default Risk
# ============================================================================

def generate_ir2602_scr_counterparty_risk():
    """
    IR2602 - SCR - Counterparty Default Risk
    Counterparty default risk SCR calculation.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        row = {
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # Type 1 Exposures
            'Type1_Reinsurance': random_amount(20_000_000, 100_000_000),
            'Type1_Derivatives': random_amount(5_000_000, 40_000_000),
            'Type1_Cash_At_Banks': random_amount(5_000_000, 30_000_000),
            'Type1_Other': random_amount(2_000_000, 15_000_000),
            'Type1_Total_Exposure': random_amount(35_000_000, 180_000_000),
            'Type1_LGD': random_amount(10_000_000, 80_000_000),
            'Type1_SCR': random_amount(5_000_000, 40_000_000),
            # Type 2 Exposures
            'Type2_Receivables_Intermediaries': random_amount(10_000_000, 50_000_000),
            'Type2_Policyholder_Debtors': random_amount(5_000_000, 30_000_000),
            'Type2_Other': random_amount(2_000_000, 15_000_000),
            'Type2_Total_Exposure': random_amount(17_000_000, 95_000_000),
            'Type2_Past_Due_3m': random_amount(1_000_000, 10_000_000),
            'Type2_SCR': random_amount(2_000_000, 15_000_000),
            # Total
            'Total_Counterparty_Risk': random_amount(7_000_000, 55_000_000),
            # Risk Mitigation
            'Collateral_Held': random_amount(5_000_000, 50_000_000),
            'Collateral_Impact': random_amount(-5_000_000, 0),
        }
        data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2603 - SCR - Life Underwriting Risk
# ============================================================================

def generate_ir2603_scr_life_risk():
    """
    IR2603 - SCR - Life Underwriting Risk
    Life underwriting risk SCR sub-modules.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        row = {
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # Sub-modules
            'Mortality_Risk': random_amount(5_000_000, 30_000_000),
            'Longevity_Risk': random_amount(3_000_000, 25_000_000),
            'Disability_Morbidity_Risk': random_amount(2_000_000, 15_000_000),
            'Lapse_Risk_Up': random_amount(5_000_000, 35_000_000),
            'Lapse_Risk_Down': random_amount(3_000_000, 20_000_000),
            'Lapse_Risk_Mass': random_amount(10_000_000, 60_000_000),
            'Lapse_Risk': random_amount(10_000_000, 60_000_000),
            'Expense_Risk': random_amount(3_000_000, 20_000_000),
            'Revision_Risk': random_amount(1_000_000, 10_000_000),
            'Catastrophe_Risk_Life': random_amount(5_000_000, 40_000_000),
            # Diversification
            'Diversification_Life': random_amount(-15_000_000, -5_000_000),
            # Total
            'Total_Life_Risk': random_amount(20_000_000, 120_000_000),
        }
        data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2604 - SCR - Health Underwriting Risk
# ============================================================================

def generate_ir2604_scr_health_risk():
    """
    IR2604 - SCR - Health Underwriting Risk
    Health underwriting risk SCR sub-modules.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        row = {
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # SLT Health
            'SLT_Mortality': random_amount(1_000_000, 10_000_000),
            'SLT_Longevity': random_amount(500_000, 5_000_000),
            'SLT_Disability': random_amount(2_000_000, 15_000_000),
            'SLT_Lapse': random_amount(1_000_000, 8_000_000),
            'SLT_Expense': random_amount(500_000, 4_000_000),
            'SLT_Revision': random_amount(200_000, 2_000_000),
            'SLT_Diversification': random_amount(-3_000_000, -1_000_000),
            'SLT_Health_Total': random_amount(3_000_000, 25_000_000),
            # NSLT Health
            'NSLT_Premium_Reserve': random_amount(5_000_000, 30_000_000),
            'NSLT_Lapse': random_amount(1_000_000, 8_000_000),
            'NSLT_Health_Total': random_amount(6_000_000, 35_000_000),
            # Catastrophe
            'Health_Catastrophe': random_amount(2_000_000, 15_000_000),
            # Diversification
            'Diversification_Health': random_amount(-5_000_000, -2_000_000),
            # Total
            'Total_Health_Risk': random_amount(10_000_000, 60_000_000),
        }
        data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2605 - SCR - Non-Life Underwriting Risk
# ============================================================================

def generate_ir2605_scr_non_life_risk():
    """
    IR2605 - SCR - Non-Life Underwriting Risk
    Non-life underwriting risk SCR sub-modules.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        row = {
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # Premium and Reserve Risk
            'Premium_Risk': random_amount(30_000_000, 150_000_000),
            'Reserve_Risk': random_amount(40_000_000, 200_000_000),
            'Premium_Reserve_Diversification': random_amount(-25_000_000, -10_000_000),
            'Premium_Reserve_Risk': random_amount(50_000_000, 280_000_000),
            # Geographic Diversification
            'Geographic_Diversification': random_amount(-10_000_000, -3_000_000),
            # Lapse Risk
            'Non_Life_Lapse_Risk': random_amount(5_000_000, 30_000_000),
            # Catastrophe Risk
            'Natural_Cat_Risk': random_amount(20_000_000, 100_000_000),
            'Man_Made_Cat_Risk': random_amount(10_000_000, 60_000_000),
            'Other_Cat_Risk': random_amount(5_000_000, 30_000_000),
            'Cat_Diversification': random_amount(-15_000_000, -5_000_000),
            'Total_Cat_Risk': random_amount(30_000_000, 160_000_000),
            # Diversification
            'Diversification_Non_Life': random_amount(-30_000_000, -10_000_000),
            # Total
            'Total_Non_Life_Risk': random_amount(60_000_000, 350_000_000),
        }
        data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2606 - SCR - Operational Risk
# ============================================================================

def generate_ir2606_scr_operational_risk():
    """
    IR2606 - SCR - Operational Risk
    Operational risk SCR calculation.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        gep = random_amount(200_000_000, 800_000_000)
        tp = random_amount(300_000_000, 1_200_000_000)

        row = {
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # Inputs
            'Gross_Earned_Premium_Life': random_amount(20_000_000, 100_000_000),
            'Gross_Earned_Premium_Non_Life': random_amount(100_000_000, 500_000_000),
            'Gross_Earned_Premium_Unit_Linked': random_amount(5_000_000, 50_000_000),
            'Total_Gross_Earned_Premium': gep,
            'TP_Life': random_amount(50_000_000, 300_000_000),
            'TP_Non_Life': random_amount(150_000_000, 600_000_000),
            'TP_Unit_Linked': random_amount(10_000_000, 100_000_000),
            'Total_TP': tp,
            # Calculation
            'Op_Premium_Component': gep * 0.04,
            'Op_TP_Component': tp * 0.0045,
            'Basic_Op_Risk': max(gep * 0.04, tp * 0.0045),
            # Expense Component (for Unit-Linked)
            'Expense_Unit_Linked': random_amount(2_000_000, 20_000_000),
            'Op_Expense_Component': random_amount(500_000, 5_000_000),
            # Cap
            'BSCR': random_amount(80_000_000, 350_000_000),
            'Op_Risk_Cap': random_amount(80_000_000, 350_000_000) * 0.30,
            # Final
            'Operational_Risk_SCR': random_amount(5_000_000, 35_000_000),
        }
        data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2607 - SCR - Simplifications
# ============================================================================

def generate_ir2607_scr_simplifications():
    """
    IR2607 - SCR - Simplifications
    Record of simplifications used in SCR calculation.
    """
    data = []

    simplifications = [
        ('Spread Risk', 'Credit Quality Step Approach', True),
        ('Counterparty Risk Type 2', 'Standard LGD', True),
        ('Life Lapse Risk', 'Homogeneous Risk Groups', True),
        ('Non-Life Premium Risk', 'Undertaking-Specific Parameters', False),
        ('Non-Life Reserve Risk', 'Undertaking-Specific Parameters', False),
        ('Catastrophe Risk', 'Standard Scenarios', True),
        ('Concentration Risk', 'Exposure Aggregation', True),
        ('Currency Risk', 'Material Currencies Only', True),
    ]

    for undertaking in UNDERTAKINGS:
        for risk_module, simplification_name, used in simplifications:
            impact = random_amount(-5_000_000, 10_000_000) if used else 0

            row = {
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Risk_Module': risk_module,
                'Simplification': simplification_name,
                'Used': used,
                'Justification': 'Proportionality - immaterial exposure' if used else 'Full calculation performed',
                'Impact_On_SCR': impact,
                'Impact_Percentage': round(impact / random_amount(100_000_000, 400_000_000) * 100, 2) if used else 0,
                'Last_Review_Date': '2024-06-30',
                'Approved_By_Board': True,
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2701 - SCR - Non-Life and Health Catastrophe Risk
# ============================================================================

def generate_ir2701_scr_catastrophe():
    """
    IR2701 - SCR - Non-Life and Health Catastrophe Risk
    Detailed catastrophe risk SCR calculation.
    """
    data = []

    cat_perils = [
        ('Windstorm', 'EU'),
        ('Earthquake', 'EU'),
        ('Flood', 'EU'),
        ('Hail', 'EU'),
        ('Subsidence', 'GB'),
        ('Windstorm', 'US'),
        ('Earthquake', 'US'),
        ('Hurricane', 'US'),
    ]

    for undertaking in UNDERTAKINGS:
        total_natural = 0
        for peril, region in cat_perils:
            gross = random_amount(5_000_000, 50_000_000)
            ri_recovery = gross * np.random.uniform(0.60, 0.90)
            net = gross - ri_recovery
            total_natural += net

            row = {
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Category': 'Natural Catastrophe',
                'Peril': peril,
                'Region': region,
                'Sum_Insured': random_amount(500_000_000, 3_000_000_000),
                'Gross_Loss': gross,
                'RI_Recovery': ri_recovery,
                'Net_Loss': net,
                'Reinstatement_Premiums': random_amount(500_000, 5_000_000),
                'Scenario_Probability': random_percentage(0.1, 2.0),
            }
            data.append(row)

        # Man-Made scenarios
        man_made = [
            ('Motor Third Party', 'Liability'),
            ('Fire', 'Property'),
            ('Marine', 'Marine'),
            ('Aviation', 'Aviation'),
            ('Liability', 'Liability'),
            ('Credit & Suretyship', 'Credit'),
            ('Terrorism', 'Property'),
        ]

        for scenario, risk_type in man_made:
            gross = random_amount(2_000_000, 30_000_000)
            ri_recovery = gross * np.random.uniform(0.50, 0.85)

            row = {
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Category': 'Man-Made Catastrophe',
                'Peril': scenario,
                'Region': 'All',
                'Sum_Insured': random_amount(100_000_000, 1_000_000_000),
                'Gross_Loss': gross,
                'RI_Recovery': ri_recovery,
                'Net_Loss': gross - ri_recovery,
                'Reinstatement_Premiums': random_amount(200_000, 2_000_000),
                'Scenario_Probability': random_percentage(0.05, 1.0),
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2801 - MCR - Only Life or Only Non-Life Activity
# ============================================================================

def generate_ir2801_mcr_non_life():
    """
    IR2801 - MCR - Only Life or Only Non-Life Activity
    MCR calculation for mono-line undertakings.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        tp = random_amount(200_000_000, 800_000_000)
        wp = random_amount(150_000_000, 600_000_000)
        scr = random_amount(80_000_000, 350_000_000)

        linear_mcr_tp = tp * 0.085
        linear_mcr_wp = wp * 0.16
        linear_mcr = linear_mcr_tp + linear_mcr_wp

        mcr_floor = scr * 0.25
        mcr_cap = scr * 0.45
        absolute_floor = 3_700_000  # EUR converted

        row = {
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            'Activity_Type': 'Non-Life',
            # Inputs
            'Net_TP_Non_Life': tp,
            'Net_Written_Premium': wp,
            'SCR': scr,
            # Linear MCR Components
            'Linear_MCR_TP_Component': linear_mcr_tp,
            'Linear_MCR_Premium_Component': linear_mcr_wp,
            'Linear_MCR': linear_mcr,
            # Floors and Caps
            'MCR_Floor_25_SCR': mcr_floor,
            'MCR_Cap_45_SCR': mcr_cap,
            'Absolute_Floor': absolute_floor,
            # Combined MCR
            'Combined_MCR': min(max(linear_mcr, mcr_floor), mcr_cap),
            # Final MCR
            'MCR': max(min(max(linear_mcr, mcr_floor), mcr_cap), absolute_floor),
            # Eligible Own Funds
            'Eligible_OF_For_MCR': random_amount(100_000_000, 400_000_000),
            'MCR_Ratio': round(random_amount(100_000_000, 400_000_000) / max(min(max(linear_mcr, mcr_floor), mcr_cap), absolute_floor) * 100, 2),
        }
        data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR2802 - MCR - Both Life and Non-Life Activity
# ============================================================================

def generate_ir2802_mcr_composite():
    """
    IR2802 - MCR - Both Life and Non-Life Activity
    MCR calculation for composite undertakings.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        # Life component
        tp_life = random_amount(50_000_000, 300_000_000)
        car_life = random_amount(20_000_000, 150_000_000)

        # Non-Life component
        tp_non_life = random_amount(150_000_000, 600_000_000)
        wp_non_life = random_amount(100_000_000, 400_000_000)

        scr = random_amount(80_000_000, 350_000_000)

        # Linear MCR calculations
        linear_mcr_life = tp_life * 0.035 + car_life * 0.045
        linear_mcr_non_life = tp_non_life * 0.085 + wp_non_life * 0.16
        linear_mcr = linear_mcr_life + linear_mcr_non_life

        mcr_floor = scr * 0.25
        mcr_cap = scr * 0.45
        absolute_floor_life = 3_700_000
        absolute_floor_non_life = 2_500_000

        row = {
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            'Activity_Type': 'Composite',
            # Life Inputs
            'Net_TP_Life': tp_life,
            'Capital_At_Risk_Life': car_life,
            'Linear_MCR_Life': linear_mcr_life,
            # Non-Life Inputs
            'Net_TP_Non_Life': tp_non_life,
            'Net_Written_Premium_Non_Life': wp_non_life,
            'Linear_MCR_Non_Life': linear_mcr_non_life,
            # Combined
            'Total_Linear_MCR': linear_mcr,
            'SCR': scr,
            # Floors and Caps
            'MCR_Floor_25_SCR': mcr_floor,
            'MCR_Cap_45_SCR': mcr_cap,
            'Absolute_Floor_Life': absolute_floor_life,
            'Absolute_Floor_Non_Life': absolute_floor_non_life,
            # Combined MCR
            'Combined_MCR': min(max(linear_mcr, mcr_floor), mcr_cap),
            # Notional MCRs
            'Notional_MCR_Life': max(linear_mcr_life * (scr * 0.35 / linear_mcr), absolute_floor_life),
            'Notional_MCR_Non_Life': max(linear_mcr_non_life * (scr * 0.35 / linear_mcr), absolute_floor_non_life),
            # Final MCR
            'MCR': max(min(max(linear_mcr, mcr_floor), mcr_cap), max(absolute_floor_life, absolute_floor_non_life)),
            # Eligible Own Funds
            'Eligible_OF_For_MCR': random_amount(100_000_000, 400_000_000),
        }
        data.append(row)

    return pd.DataFrame(data)


# Export all functions
__all__ = [
    'generate_ir2301_own_funds',
    'generate_ir2302_own_funds_by_tier',
    'generate_ir2303_own_funds_movements',
    'generate_ir2304_own_funds_items',
    'generate_ir2305_lloyds_capital',
    'generate_ir2504_scr',
    'generate_ir2505_scr_internal_model',
    'generate_ir2506_scr_lac_dt',
    'generate_ir2601_scr_market_risk',
    'generate_ir2602_scr_counterparty_risk',
    'generate_ir2603_scr_life_risk',
    'generate_ir2604_scr_health_risk',
    'generate_ir2605_scr_non_life_risk',
    'generate_ir2606_scr_operational_risk',
    'generate_ir2607_scr_simplifications',
    'generate_ir2701_scr_catastrophe',
    'generate_ir2801_mcr_non_life',
    'generate_ir2802_mcr_composite',
]
