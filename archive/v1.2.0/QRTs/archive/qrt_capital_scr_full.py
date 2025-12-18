"""
PRA/BoE QRT Generators - Capital and Solvency Requirements
=========================================================
IR2201, IR2204, IR2207: Long-Term Guarantees Measures
IR2301-IR2305: Own Funds
IR2401: Participations
IR2504-IR2506: SCR Overview
IR2601-IR2607: SCR Risk Modules
IR2701: Catastrophe Risk
IR2801-IR2802: MCR

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
CURRENCIES = ['GBP', 'USD', 'EUR', 'JPY', 'CHF']

def generate_lei():
    return '549300' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))

def random_amount(min_val, max_val, precision=2):
    return round(np.random.uniform(min_val, max_val), precision)

def random_percentage(min_val=0, max_val=100):
    return round(np.random.uniform(min_val, max_val), 4)


# ============================================================================
# IR2201 - Impact of Long-Term Guarantees Measures and Transitionals
# ============================================================================

def generate_ir2201_ltg_impact():
    """
    IR2201 - Impact of Long-Term Guarantees Measures and Transitionals
    Shows impact of LTG measures on own funds, SCR, and technical provisions.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        # Base values without LTG measures
        base_tp = random_amount(200_000_000, 2_000_000_000)
        base_own_funds = random_amount(100_000_000, 800_000_000)
        base_scr = random_amount(80_000_000, 500_000_000)

        # Impact of various measures
        va_impact_tp = random_amount(-base_tp * 0.05, -base_tp * 0.01)
        ma_impact_tp = random_amount(-base_tp * 0.08, -base_tp * 0.02) if random.random() > 0.5 else 0
        trans_tp_impact = random_amount(-base_tp * 0.1, -base_tp * 0.03) if random.random() > 0.6 else 0
        trans_ir_impact = random_amount(-base_tp * 0.05, -base_tp * 0.01) if random.random() > 0.7 else 0

        data.append({
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # Technical Provisions
            'TP_Without_LTG_Measures': base_tp,
            'Impact_VA_On_TP': va_impact_tp,
            'Impact_MA_On_TP': ma_impact_tp,
            'Impact_Transitional_TP': trans_tp_impact,
            'Impact_Transitional_IR': trans_ir_impact,
            'TP_With_LTG_Measures': base_tp + va_impact_tp + ma_impact_tp + trans_tp_impact + trans_ir_impact,
            # Own Funds
            'Basic_Own_Funds_Without_LTG': base_own_funds,
            'Impact_VA_On_Own_Funds': -va_impact_tp * 0.8,  # Inverse impact
            'Impact_MA_On_Own_Funds': -ma_impact_tp * 0.8 if ma_impact_tp else 0,
            'Impact_Transitional_TP_On_Own_Funds': -trans_tp_impact * 0.8 if trans_tp_impact else 0,
            'Impact_Transitional_IR_On_Own_Funds': -trans_ir_impact * 0.8 if trans_ir_impact else 0,
            'Basic_Own_Funds_With_LTG': base_own_funds + (-va_impact_tp - ma_impact_tp - trans_tp_impact - trans_ir_impact) * 0.8,
            # Eligible Own Funds
            'Eligible_Own_Funds_Without_LTG': base_own_funds * 0.95,
            'Eligible_Own_Funds_With_LTG': (base_own_funds + (-va_impact_tp - ma_impact_tp - trans_tp_impact - trans_ir_impact) * 0.8) * 0.95,
            # SCR
            'SCR_Without_LTG': base_scr,
            'Impact_VA_On_SCR': base_scr * random_percentage(-3, -1) / 100,
            'Impact_MA_On_SCR': base_scr * random_percentage(-5, -2) / 100 if ma_impact_tp else 0,
            'Impact_Transitional_On_SCR': 0,  # Transitionals don't affect SCR
            'SCR_With_LTG': base_scr * random_percentage(92, 98) / 100,
            # Solvency Ratios
            'Solvency_Ratio_Without_LTG': (base_own_funds * 0.95 / base_scr) * 100,
            'Solvency_Ratio_With_LTG': ((base_own_funds + (-va_impact_tp - ma_impact_tp) * 0.8) * 0.95 / (base_scr * 0.95)) * 100,
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


# ============================================================================
# IR2204 - Information on Transitional on Interest Rates
# ============================================================================

def generate_ir2204_transitional_interest_rates():
    """
    IR2204 - Information on the Transitional on Interest Rates Calculation
    Details of transitional measure on interest rates.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if random.random() > 0.6:  # Only some undertakings use this
            for currency in CURRENCIES[:3]:
                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Currency': currency,
                    'RFR_End_2015': random_percentage(1.5, 3),
                    'Current_RFR': random_percentage(3, 5),
                    'Difference': random_percentage(0.5, 2),
                    'Transitional_Deduction_Pct': random_percentage(30, 70),
                    'Transitional_Adjustment': random_percentage(0.2, 1),
                    'Adjusted_RFR': random_percentage(3.2, 5.5),
                    'TP_At_Current_RFR': random_amount(50_000_000, 500_000_000),
                    'TP_At_Adjusted_RFR': random_amount(45_000_000, 480_000_000),
                    'Impact_On_TP': random_amount(-20_000_000, -5_000_000),
                    'Years_To_Phase_Out': random.randint(5, 12),
                    'Reporting_Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR2207 - Best Estimate Subject to Volatility Adjustment by Currency
# ============================================================================

def generate_ir2207_va_by_currency():
    """
    IR2207 - Best Estimate Subject to Volatility Adjustment by Currency
    Breakdown of VA application by currency.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        for currency in CURRENCIES[:4]:
            be_amount = random_amount(20_000_000, 300_000_000)

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Currency': currency,
                'Volatility_Adjustment_BPS': random_percentage(10, 50),
                'Best_Estimate_Subject_To_VA': be_amount,
                'Best_Estimate_Without_VA': be_amount * random_percentage(101, 105) / 100,
                'Impact_Of_VA': be_amount * random_percentage(-5, -1) / 100,
                'Duration_Of_Liabilities': random_percentage(5, 15),
                'Country_VA_Applicable': random.choice(['Yes', 'No']),
                'Country_Increase': random_percentage(0, 20) if random.random() > 0.7 else 0,
                'Reporting_Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# IR2301 - Own Funds
# ============================================================================

def generate_ir2301_own_funds():
    """
    IR2301 - Own Funds
    Comprehensive own funds breakdown by tier.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        total_assets = random_amount(500_000_000, 5_000_000_000)
        total_liabilities = total_assets * random_percentage(60, 85) / 100
        excess = total_assets - total_liabilities

        # Own funds components
        paid_in_capital = random_amount(50_000_000, 200_000_000)
        share_premium = random_amount(0, 50_000_000)
        initial_funds = random_amount(10_000_000, 50_000_000)
        subordinated_mutual = 0
        surplus_funds = random_amount(0, 30_000_000)
        reconciliation_reserve = excess - paid_in_capital - share_premium - initial_funds

        data.append({
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # Basic Own Funds
            'Ordinary_Share_Capital': paid_in_capital,
            'Non_Available_At_Group': 0,
            'Share_Premium_Related_To_OSC': share_premium,
            'Initial_Funds': initial_funds,
            'Subordinated_Mutual_Member_Accounts': subordinated_mutual,
            'Surplus_Funds': surplus_funds,
            'Preference_Shares': random_amount(0, 20_000_000),
            'Share_Premium_Preference': random_amount(0, 5_000_000),
            'Reconciliation_Reserve': reconciliation_reserve,
            'Subordinated_Liabilities': random_amount(0, 100_000_000),
            'Amount_Equal_To_Deferred_Tax_Assets': random_amount(0, 30_000_000),
            'Other_Items_Approved': random_amount(0, 10_000_000),
            # Tier Classification
            'Tier_1_Unrestricted': excess * random_percentage(70, 85) / 100,
            'Tier_1_Restricted': excess * random_percentage(5, 15) / 100,
            'Tier_2': excess * random_percentage(5, 15) / 100,
            'Tier_3': excess * random_percentage(0, 5) / 100,
            'Total_Basic_Own_Funds': excess,
            # Ancillary Own Funds
            'Ancillary_Unpaid_Capital': random_amount(0, 50_000_000),
            'Ancillary_Letters_Of_Credit': random_amount(0, 30_000_000),
            'Ancillary_Other': random_amount(0, 10_000_000),
            'Total_Ancillary_Own_Funds': random_amount(0, 90_000_000),
            # Total
            'Total_Own_Funds': excess + random_amount(0, 90_000_000),
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


# ============================================================================
# IR2302 - Detailed Information by Tiers on Own Funds
# ============================================================================

def generate_ir2302_own_funds_by_tier():
    """
    IR2302 - Detailed Information by Tiers on Own Funds
    Detailed tier-by-tier breakdown.
    """
    data = []

    tiers = ['Tier 1 - Unrestricted', 'Tier 1 - Restricted', 'Tier 2', 'Tier 3']

    for undertaking in UNDERTAKINGS:
        total_own_funds = random_amount(150_000_000, 800_000_000)

        tier_allocations = {
            'Tier 1 - Unrestricted': random_percentage(65, 80),
            'Tier 1 - Restricted': random_percentage(5, 15),
            'Tier 2': random_percentage(5, 15),
            'Tier 3': random_percentage(0, 5)
        }

        for tier in tiers:
            tier_amount = total_own_funds * tier_allocations[tier] / 100

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Tier': tier,
                'Total_Amount': tier_amount,
                'Ordinary_Share_Capital': tier_amount * random_percentage(30, 60) / 100 if 'Unrestricted' in tier else 0,
                'Share_Premium': tier_amount * random_percentage(5, 15) / 100 if 'Unrestricted' in tier else 0,
                'Reconciliation_Reserve': tier_amount * random_percentage(20, 40) / 100 if 'Unrestricted' in tier else 0,
                'Subordinated_Liabilities': tier_amount if tier in ['Tier 2', 'Tier 3'] else 0,
                'Deferred_Tax_Assets': tier_amount if tier == 'Tier 3' else 0,
                'Amount_Subject_To_Transitional': tier_amount * random_percentage(0, 20) / 100,
                'Callable_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') +
                                 timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d') if 'Tier 2' in tier or 'Tier 3' in tier else None,
                'First_Call_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') +
                                   timedelta(days=random.randint(365, 1825))).strftime('%Y-%m-%d') if 'Tier 2' in tier else None,
                'Currency': 'GBP'
            })

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
        opening = random_amount(150_000_000, 700_000_000)

        movements = {
            'Underwriting_Result': random_amount(-50_000_000, 80_000_000),
            'Investment_Return': random_amount(10_000_000, 60_000_000),
            'Foreign_Exchange': random_amount(-15_000_000, 15_000_000),
            'Dividends_Paid': random_amount(-40_000_000, 0),
            'Capital_Issued': random_amount(0, 30_000_000),
            'Capital_Redeemed': random_amount(-20_000_000, 0),
            'Subordinated_Debt_Changes': random_amount(-10_000_000, 10_000_000),
            'Assumption_Changes': random_amount(-30_000_000, 30_000_000),
            'Model_Changes': random_amount(-20_000_000, 20_000_000),
            'Tax': random_amount(-30_000_000, -5_000_000),
            'Other_Movements': random_amount(-10_000_000, 10_000_000),
        }

        closing = opening + sum(movements.values())

        data.append({
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            'Opening_Own_Funds': opening,
            **{f'Movement_{k}': v for k, v in movements.items()},
            'Total_Movements': sum(movements.values()),
            'Closing_Own_Funds': closing,
            'Change_Percentage': (closing - opening) / opening * 100,
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


# ============================================================================
# IR2304 - List of Items on Own Funds
# ============================================================================

def generate_ir2304_own_funds_items():
    """
    IR2304 - List of Items on Own Funds
    Detailed listing of own fund instruments.
    """
    data = []

    instrument_types = [
        'Ordinary Shares', 'Preference Shares', 'Subordinated Notes',
        'Subordinated Loans', 'Surplus Funds', 'Ancillary Own Funds'
    ]

    for undertaking in UNDERTAKINGS:
        for inst_type in instrument_types:
            if random.random() > 0.3:  # 70% chance of having this type
                amount = random_amount(5_000_000, 100_000_000)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Instrument_ID': f'OF_{undertaking["lei"][:6]}_{inst_type[:3]}_{random.randint(1, 99):02d}',
                    'Instrument_Type': inst_type,
                    'Tier_Classification': 'Tier 1' if inst_type in ['Ordinary Shares', 'Surplus Funds'] else random.choice(['Tier 1 Restricted', 'Tier 2', 'Tier 3']),
                    'Amount': amount,
                    'Holder_Name': f'Investor {random.randint(1, 100)}' if inst_type != 'Ordinary Shares' else 'Various',
                    'Holder_LEI': generate_lei() if inst_type not in ['Ordinary Shares', 'Surplus Funds'] else None,
                    'Issue_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') -
                                  timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d'),
                    'Maturity_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') +
                                     timedelta(days=random.randint(365, 7300))).strftime('%Y-%m-%d') if inst_type not in ['Ordinary Shares', 'Surplus Funds'] else None,
                    'Coupon_Rate': random_percentage(3, 8) if 'Subordinated' in inst_type else None,
                    'Call_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') +
                                 timedelta(days=random.randint(365, 1825))).strftime('%Y-%m-%d') if 'Subordinated' in inst_type else None,
                    'Regulatory_Approval': random.choice(['Approved', 'Not Required', 'Pending']),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR2305 - Society of Lloyd's Own Funds and Capital Requirements
# ============================================================================

def generate_ir2305_lloyds_capital():
    """
    IR2305 - Society of Lloyd's Own Funds and Capital Requirements
    Lloyd's-specific capital reporting.
    """
    data = []

    # Society level data
    data.append({
        'Entity': 'Society of Lloyd\'s',
        'LEI': '5493000F4ZO33MV32P92',
        'Reporting_Date': REPORTING_DATE,
        'Central_Fund': random_amount(2_000_000_000, 3_000_000_000),
        'Subordinated_Debt': random_amount(500_000_000, 800_000_000),
        'Central_Assets': random_amount(500_000_000, 800_000_000),
        'Total_Central_Resources': random_amount(3_000_000_000, 4_500_000_000),
        'Member_Capital': random_amount(35_000_000_000, 45_000_000_000),
        'FAL': random_amount(30_000_000_000, 40_000_000_000),
        'LOC_Guarantees': random_amount(1_000_000_000, 3_000_000_000),
        'Total_Member_Resources': random_amount(66_000_000_000, 88_000_000_000),
        'Total_Own_Funds': random_amount(69_000_000_000, 92_000_000_000),
        'Market_Wide_SCR': random_amount(25_000_000_000, 35_000_000_000),
        'Member_SCR_Uplift': random_amount(5_000_000_000, 10_000_000_000),
        'Total_SCR': random_amount(30_000_000_000, 45_000_000_000),
        'MCR': random_amount(8_000_000_000, 12_000_000_000),
        'Solvency_Ratio': random_percentage(150, 250),
        'Currency': 'GBP'
    })

    return pd.DataFrame(data)


# ============================================================================
# IR2401 - Participations Held
# ============================================================================

def generate_ir2401_participations():
    """
    IR2401 - Participations Held
    Details of participations in related undertakings.
    """
    data = []

    participation_types = [
        'Insurance Subsidiary', 'Reinsurance Subsidiary', 'Insurance Holding',
        'Financial Subsidiary', 'Service Company', 'Investment SPV'
    ]

    for undertaking in UNDERTAKINGS:
        for _ in range(random.randint(2, 8)):
            ownership_pct = random_percentage(20, 100)
            carrying_value = random_amount(5_000_000, 200_000_000)

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Participation_Name': f'Subsidiary Co {random.randint(1, 100)}',
                'Participation_LEI': generate_lei(),
                'Participation_Type': random.choice(participation_types),
                'Country_Of_Incorporation': random.choice(['GB', 'US', 'DE', 'FR', 'IE', 'LU']),
                'Ownership_Percentage': ownership_pct,
                'Voting_Rights_Percentage': ownership_pct,
                'Goodwill': random_amount(0, carrying_value * 0.1),
                'Carrying_Value_SII': carrying_value,
                'Carrying_Value_Statutory': carrying_value * random_percentage(90, 110) / 100,
                'Net_Asset_Value': carrying_value * random_percentage(85, 115) / 100,
                'Profit_Loss_Current_Year': random_amount(-10_000_000, 30_000_000),
                'Dividend_Received': random_amount(0, 10_000_000),
                'Method_Of_Valuation': random.choice(['Equity Method', 'Adjusted Equity Method', 'Full Consolidation']),
                'Contribution_To_Group_SCR': carrying_value * random_percentage(5, 15) / 100,
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# IR2504 - Solvency Capital Requirement
# ============================================================================

def generate_ir2504_scr():
    """
    IR2504 - Solvency Capital Requirement (Standard Formula)
    Full SCR calculation breakdown.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        # Risk module components
        market_risk = random_amount(30_000_000, 200_000_000)
        counterparty_risk = random_amount(10_000_000, 80_000_000)
        life_risk = random_amount(5_000_000, 50_000_000) if undertaking['type'] in ['Life', 'Composite'] else 0
        health_risk = random_amount(5_000_000, 40_000_000)
        non_life_risk = random_amount(40_000_000, 300_000_000) if undertaking['type'] in ['Non-Life', 'Composite'] else 0

        # BSCR calculation
        bscr_undiversified = market_risk + counterparty_risk + life_risk + health_risk + non_life_risk
        diversification = bscr_undiversified * random_percentage(-30, -15) / 100
        bscr = bscr_undiversified + diversification

        # Operational risk
        operational_risk = bscr * random_percentage(5, 12) / 100

        # Loss absorbing capacity
        lac_tp = bscr * random_percentage(-5, 0) / 100
        lac_dt = bscr * random_percentage(-10, -3) / 100

        scr = bscr + operational_risk + lac_tp + lac_dt

        data.append({
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # Risk Modules
            'Market_Risk': market_risk,
            'Counterparty_Default_Risk': counterparty_risk,
            'Life_Underwriting_Risk': life_risk,
            'Health_Underwriting_Risk': health_risk,
            'Non_Life_Underwriting_Risk': non_life_risk,
            # Aggregation
            'BSCR_Undiversified': bscr_undiversified,
            'Diversification_Benefit': diversification,
            'Basic_SCR': bscr,
            # Adjustments
            'Operational_Risk': operational_risk,
            'LAC_Technical_Provisions': lac_tp,
            'LAC_Deferred_Taxes': lac_dt,
            'Capital_Add_On': 0,
            # Final SCR
            'SCR': scr,
            # Comparison
            'SCR_Change_From_Prior': random_percentage(-15, 15),
            'Eligible_Own_Funds': scr * random_percentage(150, 250) / 100,
            'Solvency_Ratio': random_percentage(150, 250),
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


# ============================================================================
# IR2505 - SCR Partial/Full Internal Model Components
# ============================================================================

def generate_ir2505_scr_internal_model():
    """
    IR2505 - SCR for Undertakings Using Partial or Full Internal Model
    SCR breakdown when internal model is used.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if random.random() > 0.5:  # 50% use internal model
            im_scr = random_amount(80_000_000, 400_000_000)

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Model_Type': random.choice(['Full Internal Model', 'Partial Internal Model']),
                'Model_Approval_Date': '2020-01-01',
                # IM SCR Components
                'IM_Market_Risk': im_scr * random_percentage(25, 40) / 100,
                'IM_Counterparty_Risk': im_scr * random_percentage(5, 15) / 100,
                'IM_Life_Risk': im_scr * random_percentage(5, 15) / 100 if undertaking['type'] in ['Life', 'Composite'] else 0,
                'IM_Health_Risk': im_scr * random_percentage(3, 10) / 100,
                'IM_Non_Life_Risk': im_scr * random_percentage(30, 50) / 100 if undertaking['type'] in ['Non-Life', 'Composite'] else 0,
                'IM_Operational_Risk': im_scr * random_percentage(5, 10) / 100,
                'IM_Diversification': im_scr * random_percentage(-25, -10) / 100,
                'IM_SCR_Before_LAC': im_scr * random_percentage(110, 130) / 100,
                'IM_LAC_TP': im_scr * random_percentage(-5, 0) / 100,
                'IM_LAC_DT': im_scr * random_percentage(-10, -3) / 100,
                'IM_SCR': im_scr,
                # Comparison to SF
                'SF_SCR_Equivalent': im_scr * random_percentage(100, 130) / 100,
                'IM_To_SF_Ratio': random_percentage(75, 105),
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# IR2506 - SCR Loss Absorbing Capacity of Deferred Taxes
# ============================================================================

def generate_ir2506_scr_lac_dt():
    """
    IR2506 - SCR Loss Absorbing Capacity of Deferred Taxes
    Detailed calculation of LAC DT.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        bscr = random_amount(80_000_000, 400_000_000)
        dta = random_amount(5_000_000, 50_000_000)
        dtl = random_amount(10_000_000, 80_000_000)

        data.append({
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # Pre-stress Position
            'DTA_Before_Shock': dta,
            'DTL_Before_Shock': dtl,
            'Net_DT_Before_Shock': dtl - dta,
            # Post-stress Position
            'Loss_Before_Tax': bscr,
            'Tax_Rate': random_percentage(19, 25),
            'Tax_Credit_On_Loss': bscr * random_percentage(19, 25) / 100,
            'DTA_After_Shock': dta + bscr * random_percentage(5, 15) / 100,
            'DTL_After_Shock': dtl - bscr * random_percentage(15, 25) / 100,
            'Net_DT_After_Shock': (dtl - bscr * random_percentage(15, 25) / 100) - (dta + bscr * random_percentage(5, 15) / 100),
            # LAC DT Calculation
            'Change_In_Net_DT': random_amount(-50_000_000, -10_000_000),
            'LAC_DT_Uncapped': random_amount(-60_000_000, -10_000_000),
            'Maximum_LAC_DT': random_amount(-50_000_000, -8_000_000),
            'LAC_DT_Applied': min(random_amount(-50_000_000, -10_000_000), random_amount(-50_000_000, -8_000_000)),
            # Justification
            'Future_Profits_Support': random.choice(['Yes', 'Partial', 'No']),
            'Reversal_Of_Temporary_Differences': random.choice(['Yes', 'Partial', 'No']),
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


# ============================================================================
# IR2601 - SCR Market Risk
# ============================================================================

def generate_ir2601_scr_market_risk():
    """
    IR2601 - Solvency Capital Requirement - Market Risk
    Detailed breakdown of market risk SCR.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        total_market_risk = random_amount(30_000_000, 200_000_000)

        data.append({
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # Sub-modules
            'Interest_Rate_Risk': total_market_risk * random_percentage(15, 30) / 100,
            'IR_Risk_Up_Scenario': total_market_risk * random_percentage(10, 20) / 100,
            'IR_Risk_Down_Scenario': total_market_risk * random_percentage(5, 15) / 100,
            'Equity_Risk': total_market_risk * random_percentage(20, 40) / 100,
            'Equity_Type_1': total_market_risk * random_percentage(15, 30) / 100,
            'Equity_Type_2': total_market_risk * random_percentage(5, 15) / 100,
            'Property_Risk': total_market_risk * random_percentage(5, 15) / 100,
            'Spread_Risk': total_market_risk * random_percentage(15, 35) / 100,
            'Spread_Bonds': total_market_risk * random_percentage(10, 25) / 100,
            'Spread_Structured': total_market_risk * random_percentage(2, 8) / 100,
            'Spread_Derivatives': total_market_risk * random_percentage(1, 5) / 100,
            'Currency_Risk': total_market_risk * random_percentage(10, 25) / 100,
            'Concentration_Risk': total_market_risk * random_percentage(5, 15) / 100,
            # Aggregation
            'Market_Risk_Undiversified': total_market_risk * random_percentage(110, 130) / 100,
            'Diversification_Within_Module': total_market_risk * random_percentage(-20, -10) / 100,
            'Market_Risk_Total': total_market_risk,
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


# ============================================================================
# IR2602 - SCR Counterparty Default Risk
# ============================================================================

def generate_ir2602_scr_counterparty_risk():
    """
    IR2602 - Solvency Capital Requirement - Counterparty Default Risk
    Counterparty default risk calculation.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        total_cp_risk = random_amount(10_000_000, 80_000_000)

        data.append({
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # Type 1 Exposures (Reinsurers, Banks, Derivatives)
            'Type_1_Exposure_Total': random_amount(50_000_000, 500_000_000),
            'Type_1_LGD': random_amount(20_000_000, 200_000_000),
            'Type_1_SCR': total_cp_risk * random_percentage(60, 80) / 100,
            # Type 2 Exposures (Receivables, Intermediaries)
            'Type_2_Exposure_Total': random_amount(20_000_000, 200_000_000),
            'Type_2_Overdue_3m': random_amount(0, 20_000_000),
            'Type_2_Not_Overdue': random_amount(15_000_000, 180_000_000),
            'Type_2_SCR': total_cp_risk * random_percentage(20, 40) / 100,
            # Totals
            'Total_Counterparty_Risk_SCR': total_cp_risk,
            # Risk Mitigation
            'Collateral_Received': random_amount(10_000_000, 100_000_000),
            'Guarantees_Received': random_amount(0, 50_000_000),
            'Effect_Of_Risk_Mitigation': random_amount(-20_000_000, -5_000_000),
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


# ============================================================================
# IR2603 - SCR Life Underwriting Risk
# ============================================================================

def generate_ir2603_scr_life_risk():
    """
    IR2603 - Solvency Capital Requirement - Life Underwriting Risk
    Life underwriting risk SCR breakdown.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            total_life_risk = random_amount(5_000_000, 100_000_000)

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                # Sub-modules
                'Mortality_Risk': total_life_risk * random_percentage(10, 25) / 100,
                'Longevity_Risk': total_life_risk * random_percentage(5, 20) / 100,
                'Disability_Morbidity_Risk': total_life_risk * random_percentage(5, 15) / 100,
                'Lapse_Risk': total_life_risk * random_percentage(20, 40) / 100,
                'Lapse_Risk_Up': total_life_risk * random_percentage(10, 20) / 100,
                'Lapse_Risk_Down': total_life_risk * random_percentage(5, 15) / 100,
                'Lapse_Risk_Mass': total_life_risk * random_percentage(15, 30) / 100,
                'Expense_Risk': total_life_risk * random_percentage(10, 20) / 100,
                'Revision_Risk': total_life_risk * random_percentage(2, 8) / 100,
                'Catastrophe_Risk': total_life_risk * random_percentage(5, 15) / 100,
                # Aggregation
                'Life_Risk_Undiversified': total_life_risk * random_percentage(110, 130) / 100,
                'Diversification_Within_Module': total_life_risk * random_percentage(-20, -10) / 100,
                'Life_Risk_Total': total_life_risk,
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# IR2604 - SCR Health Underwriting Risk
# ============================================================================

def generate_ir2604_scr_health_risk():
    """
    IR2604 - Solvency Capital Requirement - Health Underwriting Risk
    Health underwriting risk SCR breakdown.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        total_health_risk = random_amount(5_000_000, 50_000_000)

        data.append({
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # NSLT Health
            'NSLT_Health_Premium_Reserve_Risk': total_health_risk * random_percentage(30, 50) / 100,
            'NSLT_Health_Lapse_Risk': total_health_risk * random_percentage(5, 15) / 100,
            # SLT Health
            'SLT_Health_Mortality_Risk': total_health_risk * random_percentage(5, 10) / 100,
            'SLT_Health_Longevity_Risk': total_health_risk * random_percentage(3, 8) / 100,
            'SLT_Health_Disability_Risk': total_health_risk * random_percentage(10, 20) / 100,
            'SLT_Health_Expense_Risk': total_health_risk * random_percentage(5, 10) / 100,
            'SLT_Health_Revision_Risk': total_health_risk * random_percentage(2, 5) / 100,
            'SLT_Health_Lapse_Risk': total_health_risk * random_percentage(5, 10) / 100,
            # Catastrophe
            'Health_Catastrophe_Risk': total_health_risk * random_percentage(10, 20) / 100,
            'Mass_Accident_Risk': total_health_risk * random_percentage(5, 10) / 100,
            'Concentration_Risk': total_health_risk * random_percentage(3, 8) / 100,
            'Pandemic_Risk': total_health_risk * random_percentage(5, 12) / 100,
            # Aggregation
            'Health_Risk_Undiversified': total_health_risk * random_percentage(110, 125) / 100,
            'Diversification_Within_Module': total_health_risk * random_percentage(-15, -5) / 100,
            'Health_Risk_Total': total_health_risk,
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


# ============================================================================
# IR2605 - SCR Non-Life Underwriting Risk
# ============================================================================

def generate_ir2605_scr_non_life_risk():
    """
    IR2605 - Solvency Capital Requirement - Non-Life Underwriting Risk
    Non-life underwriting risk SCR breakdown.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            total_nl_risk = random_amount(40_000_000, 300_000_000)

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                # Premium and Reserve Risk
                'Premium_Reserve_Risk': total_nl_risk * random_percentage(60, 80) / 100,
                'Premium_Risk': total_nl_risk * random_percentage(25, 40) / 100,
                'Reserve_Risk': total_nl_risk * random_percentage(30, 45) / 100,
                'Geographic_Diversification': random_percentage(0.7, 0.95),
                # Lapse Risk
                'NL_Lapse_Risk': total_nl_risk * random_percentage(2, 8) / 100,
                # Catastrophe Risk
                'NL_Catastrophe_Risk': total_nl_risk * random_percentage(20, 40) / 100,
                'Natural_Cat_Risk': total_nl_risk * random_percentage(15, 30) / 100,
                'Man_Made_Cat_Risk': total_nl_risk * random_percentage(5, 15) / 100,
                'Other_Cat_Risk': total_nl_risk * random_percentage(2, 8) / 100,
                # Aggregation
                'NL_Risk_Undiversified': total_nl_risk * random_percentage(110, 130) / 100,
                'Diversification_Within_Module': total_nl_risk * random_percentage(-20, -10) / 100,
                'Non_Life_Risk_Total': total_nl_risk,
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# IR2606 - SCR Operational Risk
# ============================================================================

def generate_ir2606_scr_operational_risk():
    """
    IR2606 - Solvency Capital Requirement - Operational Risk
    Operational risk SCR calculation.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        bscr = random_amount(80_000_000, 400_000_000)
        gross_premium = random_amount(100_000_000, 1_000_000_000)
        gross_tp = random_amount(200_000_000, 2_000_000_000)

        # Op risk calculation
        op_basic_premium = gross_premium * 0.04  # 4% of premiums
        op_basic_tp = gross_tp * 0.0045  # 0.45% of TP
        op_basic = max(op_basic_premium, op_basic_tp)
        op_ul = random_amount(1_000_000, 20_000_000)  # Unit-linked
        op_risk = min(op_basic + op_ul, bscr * 0.3)  # Capped at 30% of BSCR

        data.append({
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # Input Amounts
            'Gross_Earned_Premium_Life': gross_premium * random_percentage(10, 30) / 100 if undertaking['type'] in ['Life', 'Composite'] else 0,
            'Gross_Earned_Premium_Non_Life': gross_premium * random_percentage(70, 90) / 100 if undertaking['type'] in ['Non-Life', 'Composite'] else 0,
            'Gross_Earned_Premium_Total': gross_premium,
            'Gross_TP_Life': gross_tp * random_percentage(20, 40) / 100 if undertaking['type'] in ['Life', 'Composite'] else 0,
            'Gross_TP_Non_Life': gross_tp * random_percentage(60, 80) / 100 if undertaking['type'] in ['Non-Life', 'Composite'] else 0,
            'Gross_TP_Total': gross_tp,
            # Calculation
            'Op_Risk_Based_On_Premium': op_basic_premium,
            'Op_Risk_Based_On_TP': op_basic_tp,
            'Op_Risk_Basic': op_basic,
            'Op_Risk_Unit_Linked': op_ul if undertaking['type'] in ['Life', 'Composite'] else 0,
            'Op_Risk_Gross': op_basic + op_ul,
            'Cap_30_Pct_BSCR': bscr * 0.3,
            'Operational_Risk_SCR': op_risk,
            'Currency': 'GBP'
        })

    return pd.DataFrame(data)


# ============================================================================
# IR2607 - SCR Simplifications
# ============================================================================

def generate_ir2607_scr_simplifications():
    """
    IR2607 - Solvency Capital Requirement - Simplifications Used
    Details of simplifications applied in SCR calculation.
    """
    data = []

    simplification_types = [
        ('Spread Risk - Bonds', 'Market'),
        ('Spread Risk - Loans', 'Market'),
        ('Counterparty Type 1', 'Counterparty'),
        ('Counterparty Type 2', 'Counterparty'),
        ('Mortality Risk', 'Life'),
        ('Longevity Risk', 'Life'),
        ('Disability Risk', 'Life'),
        ('Premium Reserve Risk', 'Non-Life'),
        ('Catastrophe Risk NL', 'Non-Life'),
        ('Health SLT', 'Health'),
    ]

    for undertaking in UNDERTAKINGS:
        for simp_name, risk_module in simplification_types:
            if random.random() > 0.7:  # 30% use simplifications
                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Simplification': simp_name,
                    'Risk_Module': risk_module,
                    'Simplification_Used': 'Yes',
                    'Reason': random.choice(['Proportionality', 'Immateriality', 'Data Unavailability']),
                    'SCR_With_Simplification': random_amount(1_000_000, 30_000_000),
                    'SCR_Full_Calculation_Estimate': random_amount(800_000, 35_000_000),
                    'Materiality_Threshold_Pct': random_percentage(1, 5),
                    'Actual_Exposure_Pct': random_percentage(0.5, 4),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR2701 - SCR Non-Life and Health Catastrophe Risk
# ============================================================================

def generate_ir2701_scr_catastrophe():
    """
    IR2701 - Solvency Capital Requirement - Non-Life and Health Catastrophe Risk
    Detailed catastrophe risk calculation.
    """
    data = []

    cat_perils = [
        ('Windstorm', 'Natural'),
        ('Earthquake', 'Natural'),
        ('Flood', 'Natural'),
        ('Hail', 'Natural'),
        ('Subsidence', 'Natural'),
        ('Fire', 'Man-Made'),
        ('Motor', 'Man-Made'),
        ('Marine', 'Man-Made'),
        ('Aviation', 'Man-Made'),
        ('Liability', 'Man-Made'),
        ('Credit & Suretyship', 'Man-Made'),
        ('Terrorism', 'Man-Made'),
    ]

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            total_cat_risk = random_amount(20_000_000, 200_000_000)

            for peril, cat_type in cat_perils:
                gross_loss = random_amount(5_000_000, 100_000_000)
                ri_recovery = gross_loss * random_percentage(30, 70) / 100

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Catastrophe_Peril': peril,
                    'Catastrophe_Type': cat_type,
                    'Gross_Loss_1_in_200': gross_loss,
                    'Reinsurance_Recovery': ri_recovery,
                    'Net_Loss_1_in_200': gross_loss - ri_recovery,
                    'Sum_Insured_Exposure': gross_loss * random.randint(50, 200),
                    'Number_Of_Policies_Exposed': random.randint(1000, 100000),
                    'Average_Loss_Per_Policy': gross_loss / random.randint(1000, 100000),
                    'Correlation_Factor': random_percentage(0.1, 0.5),
                    'SCR_Contribution': (gross_loss - ri_recovery) * random_percentage(0.5, 1.5),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR2801 - MCR (Non-Life Only)
# ============================================================================

def generate_ir2801_mcr_non_life():
    """
    IR2801 - Minimum Capital Requirement - Non-Life or Non-SLT Health Only
    MCR calculation for non-life undertakings.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] == 'Non-Life':
            scr = random_amount(80_000_000, 300_000_000)
            net_tp = random_amount(150_000_000, 1_500_000_000)
            net_premium = random_amount(100_000_000, 800_000_000)

            # MCR calculation components
            linear_mcr = net_tp * 0.035 + net_premium * 0.045
            mcr_floor = scr * 0.25
            mcr_cap = scr * 0.45
            absolute_floor = 2_700_000  # For non-life

            mcr = max(min(linear_mcr, mcr_cap), mcr_floor, absolute_floor)

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                # Inputs
                'Net_Technical_Provisions': net_tp,
                'Net_Written_Premium': net_premium,
                'SCR': scr,
                # MCR Calculation
                'Linear_MCR_TP_Component': net_tp * 0.035,
                'Linear_MCR_Premium_Component': net_premium * 0.045,
                'Linear_MCR': linear_mcr,
                'MCR_Floor_25_SCR': mcr_floor,
                'MCR_Cap_45_SCR': mcr_cap,
                'MCR_Absolute_Floor': absolute_floor,
                'MCR_Combined': mcr,
                # Coverage
                'Eligible_Basic_Own_Funds': mcr * random_percentage(300, 600) / 100,
                'MCR_Coverage_Ratio': random_percentage(300, 600),
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# IR2802 - MCR (Composite)
# ============================================================================

def generate_ir2802_mcr_composite():
    """
    IR2802 - Minimum Capital Requirement - Both Life and Non-Life Activity
    MCR calculation for composite undertakings.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] == 'Composite':
            scr = random_amount(100_000_000, 400_000_000)

            # Life component
            life_tp = random_amount(50_000_000, 500_000_000)
            life_sar = random_amount(1_000_000_000, 10_000_000_000)  # Sum at risk

            # Non-life component
            nl_tp = random_amount(100_000_000, 800_000_000)
            nl_premium = random_amount(80_000_000, 600_000_000)

            # MCR components
            linear_mcr_life = life_tp * 0.0085 + life_sar * 0.001
            linear_mcr_nl = nl_tp * 0.035 + nl_premium * 0.045
            linear_mcr = linear_mcr_life + linear_mcr_nl

            mcr_floor = scr * 0.25
            mcr_cap = scr * 0.45
            absolute_floor = max(3_700_000, 2_700_000)  # Higher of life and non-life

            mcr = max(min(linear_mcr, mcr_cap), mcr_floor, absolute_floor)

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                # Life Inputs
                'Life_TP': life_tp,
                'Life_Sum_At_Risk': life_sar,
                'Linear_MCR_Life': linear_mcr_life,
                # Non-Life Inputs
                'Non_Life_TP': nl_tp,
                'Non_Life_Premium': nl_premium,
                'Linear_MCR_Non_Life': linear_mcr_nl,
                # Combined MCR
                'Linear_MCR_Combined': linear_mcr,
                'SCR': scr,
                'MCR_Floor_25_SCR': mcr_floor,
                'MCR_Cap_45_SCR': mcr_cap,
                'MCR_Absolute_Floor': absolute_floor,
                'MCR_Combined': mcr,
                # Split by Activity
                'Notional_MCR_Life': mcr * linear_mcr_life / linear_mcr if linear_mcr > 0 else 0,
                'Notional_MCR_Non_Life': mcr * linear_mcr_nl / linear_mcr if linear_mcr > 0 else 0,
                # Coverage
                'Eligible_Basic_Own_Funds': mcr * random_percentage(300, 600) / 100,
                'MCR_Coverage_Ratio': random_percentage(300, 600),
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# Power BI Execution
# ============================================================================

if __name__ == "__main__":
    print("Generating Capital and SCR QRTs...")

# Generate all tables for Power BI
IR2201_LTG_Impact = generate_ir2201_ltg_impact()
IR2204_Transitional_Interest_Rates = generate_ir2204_transitional_interest_rates()
IR2207_VA_By_Currency = generate_ir2207_va_by_currency()
IR2301_Own_Funds = generate_ir2301_own_funds()
IR2302_Own_Funds_By_Tier = generate_ir2302_own_funds_by_tier()
IR2303_Own_Funds_Movements = generate_ir2303_own_funds_movements()
IR2304_Own_Funds_Items = generate_ir2304_own_funds_items()
IR2305_Lloyds_Capital = generate_ir2305_lloyds_capital()
IR2401_Participations = generate_ir2401_participations()
IR2504_SCR = generate_ir2504_scr()
IR2505_SCR_Internal_Model = generate_ir2505_scr_internal_model()
IR2506_SCR_LAC_DT = generate_ir2506_scr_lac_dt()
IR2601_SCR_Market_Risk = generate_ir2601_scr_market_risk()
IR2602_SCR_Counterparty_Risk = generate_ir2602_scr_counterparty_risk()
IR2603_SCR_Life_Risk = generate_ir2603_scr_life_risk()
IR2604_SCR_Health_Risk = generate_ir2604_scr_health_risk()
IR2605_SCR_Non_Life_Risk = generate_ir2605_scr_non_life_risk()
IR2606_SCR_Operational_Risk = generate_ir2606_scr_operational_risk()
IR2607_SCR_Simplifications = generate_ir2607_scr_simplifications()
IR2701_SCR_Catastrophe = generate_ir2701_scr_catastrophe()
IR2801_MCR_Non_Life = generate_ir2801_mcr_non_life()
IR2802_MCR_Composite = generate_ir2802_mcr_composite()
