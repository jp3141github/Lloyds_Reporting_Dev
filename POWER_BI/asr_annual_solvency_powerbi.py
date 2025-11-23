# Annual Solvency Return (ASR) - Power BI Data Generator
# Lloyd's Annual Pillar 3 Solvency II Reporting
#
# DISTINCT FROM QSR: ASR covers annual-only disclosures not in quarterly returns:
# - Full year variation analysis
# - Annual public disclosure elements (SFCR-related)
# - Year-end technical provisions reconciliation
# - Annual own funds movement analysis
# - Solvency II annual templates (ASR002, ASR210, ASR220, ASR240, ASR280, ASR510, ASR910)
#
# Usage in Power BI:
# 1. Get Data > More > Other > Python script
# 2. Paste this entire file
# 3. Select tables from navigator
# 4. Load

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# Configuration
SYNDICATES = [33, 623, 1183, 1910, 2010, 2525, 2791, 2987, 4242, 5000]
REPORTING_YEAR = 2024
PRIOR_YEAR = 2023

# Lloyd's Lines of Business (Solvency II)
SII_LINES_OF_BUSINESS = [
    ('1', 'Medical expense insurance'),
    ('2', 'Income protection insurance'),
    ('3', 'Workers compensation insurance'),
    ('4', 'Motor vehicle liability insurance'),
    ('5', 'Other motor insurance'),
    ('6', 'Marine, aviation and transport insurance'),
    ('7', 'Fire and other damage to property insurance'),
    ('8', 'General liability insurance'),
    ('9', 'Credit and suretyship insurance'),
    ('10', 'Legal expenses insurance'),
    ('11', 'Assistance'),
    ('12', 'Miscellaneous financial loss'),
    ('25', 'Non-proportional casualty reinsurance'),
    ('26', 'Non-proportional marine, aviation and transport reinsurance'),
    ('27', 'Non-proportional property reinsurance')
]

# =============================================================================
# ASR_001_Control - Annual submission metadata
# =============================================================================
def generate_asr_001_control():
    records = []
    for syn in SYNDICATES:
        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'ReportingPeriodEnd': datetime(REPORTING_YEAR, 12, 31),
            'SubmissionDeadline': datetime(REPORTING_YEAR + 1, 4, 7),
            'SubmissionDate': datetime(REPORTING_YEAR + 1, 4, 5),
            'ManagingAgent': f'MA{syn % 100:03d}',
            'ReportType': 'ASR',
            'ReportVersion': '2024.1',
            'AuditStatus': 'Audited',
            'AuditorName': np.random.choice(['PwC', 'Deloitte', 'EY', 'KPMG', 'BDO']),
            'AuditOpinion': 'Unqualified',
            'Currency': 'GBP',
            'ExchangeRateSource': 'Lloyd\'s Official Rates'
        })
    return pd.DataFrame(records)

# =============================================================================
# ASR_002_Balance_Sheet - S.02.01.02 Annual Balance Sheet
# =============================================================================
def generate_asr_002_balance_sheet():
    records = []
    for syn in SYNDICATES:
        # Generate realistic balance sheet with YoY comparison
        base_assets = np.random.uniform(400, 1200)
        growth = np.random.uniform(-0.05, 0.15)

        for year in [PRIOR_YEAR, REPORTING_YEAR]:
            factor = 1.0 if year == PRIOR_YEAR else (1 + growth)
            total_assets = base_assets * factor

            # Asset breakdown
            investments = total_assets * np.random.uniform(0.55, 0.70)
            govt_bonds = investments * np.random.uniform(0.35, 0.50)
            corp_bonds = investments * np.random.uniform(0.25, 0.40)
            equities = investments * np.random.uniform(0.03, 0.08)
            collective_investments = investments * np.random.uniform(0.05, 0.15)
            other_investments = investments - govt_bonds - corp_bonds - equities - collective_investments

            ri_recoverables = total_assets * np.random.uniform(0.12, 0.22)
            insurance_receivables = total_assets * np.random.uniform(0.08, 0.15)
            cash = total_assets * np.random.uniform(0.05, 0.12)
            other_assets = total_assets - investments - ri_recoverables - insurance_receivables - cash

            # Liabilities
            total_liabilities = total_assets * np.random.uniform(0.65, 0.80)
            technical_provisions = total_liabilities * np.random.uniform(0.75, 0.88)
            tp_non_life = technical_provisions * np.random.uniform(0.85, 0.95)
            tp_life = technical_provisions - tp_non_life
            insurance_payables = total_liabilities * np.random.uniform(0.08, 0.15)
            other_liabilities = total_liabilities - technical_provisions - insurance_payables

            # Own Funds
            excess_assets = total_assets - total_liabilities

            records.append({
                'Syndicate': syn,
                'ReportingYear': year,
                'YearEnd': datetime(year, 12, 31),
                # Assets
                'TotalAssets_GBP_M': round(total_assets, 2),
                'Investments_GBP_M': round(investments, 2),
                'GovernmentBonds_GBP_M': round(govt_bonds, 2),
                'CorporateBonds_GBP_M': round(corp_bonds, 2),
                'Equities_GBP_M': round(equities, 2),
                'CollectiveInvestments_GBP_M': round(collective_investments, 2),
                'OtherInvestments_GBP_M': round(other_investments, 2),
                'RI_Recoverables_GBP_M': round(ri_recoverables, 2),
                'InsuranceReceivables_GBP_M': round(insurance_receivables, 2),
                'Cash_GBP_M': round(cash, 2),
                'OtherAssets_GBP_M': round(other_assets, 2),
                # Liabilities
                'TotalLiabilities_GBP_M': round(total_liabilities, 2),
                'TechnicalProvisions_GBP_M': round(technical_provisions, 2),
                'TP_NonLife_GBP_M': round(tp_non_life, 2),
                'TP_Life_GBP_M': round(tp_life, 2),
                'InsurancePayables_GBP_M': round(insurance_payables, 2),
                'OtherLiabilities_GBP_M': round(other_liabilities, 2),
                # Excess
                'ExcessAssetsOverLiabilities_GBP_M': round(excess_assets, 2),
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# ASR_210_Variation_Analysis - S.29.03/04 Variation Analysis
# =============================================================================
def generate_asr_210_variation_analysis():
    """Annual-only form showing year-on-year variation in excess of assets over liabilities"""
    records = []
    variation_items = [
        ('OPEN_EOF', 'Opening Excess of Assets over Liabilities', 'Opening'),
        ('UW_RESULT', 'Underwriting Result', 'Movement'),
        ('INV_RETURN', 'Investment Return', 'Movement'),
        ('FX_IMPACT', 'Foreign Exchange Impact', 'Movement'),
        ('TP_CHANGE', 'Technical Provisions Change', 'Movement'),
        ('RI_CHANGE', 'Reinsurance Recoverables Change', 'Movement'),
        ('OTHER_COMP', 'Other Comprehensive Income', 'Movement'),
        ('DIST', 'Distributions to Members', 'Movement'),
        ('CAP_CALL', 'Capital Calls', 'Movement'),
        ('OTHER_MOV', 'Other Movements', 'Movement'),
        ('CLOSE_EOF', 'Closing Excess of Assets over Liabilities', 'Closing')
    ]

    for syn in SYNDICATES:
        opening = np.random.uniform(80, 250)
        uw_result = np.random.uniform(-20, 60)
        inv_return = np.random.uniform(5, 30)
        fx_impact = np.random.uniform(-15, 15)
        tp_change = np.random.uniform(-30, 10)
        ri_change = np.random.uniform(-10, 10)
        other_comp = np.random.uniform(-5, 5)
        distributions = np.random.uniform(0, 30)
        cap_calls = np.random.uniform(0, 20)
        other_mov = np.random.uniform(-5, 5)

        closing = opening + uw_result + inv_return + fx_impact + tp_change + ri_change + other_comp - distributions + cap_calls + other_mov

        amounts = {
            'OPEN_EOF': opening,
            'UW_RESULT': uw_result,
            'INV_RETURN': inv_return,
            'FX_IMPACT': fx_impact,
            'TP_CHANGE': tp_change,
            'RI_CHANGE': ri_change,
            'OTHER_COMP': other_comp,
            'DIST': -distributions,
            'CAP_CALL': cap_calls,
            'OTHER_MOV': other_mov,
            'CLOSE_EOF': closing
        }

        for item_code, item_name, item_type in variation_items:
            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'ItemCode': item_code,
                'ItemName': item_name,
                'ItemType': item_type,
                'Amount_GBP_M': round(amounts[item_code], 2),
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# ASR_220_Own_Funds - S.23.01.01 Annual Own Funds (with movement)
# =============================================================================
def generate_asr_220_own_funds():
    """Annual own funds with full movement analysis"""
    records = []
    for syn in SYNDICATES:
        scr = np.random.uniform(80, 200)
        mcr = scr * np.random.uniform(0.25, 0.35)

        # Prior year
        py_tier1_unrestricted = scr * np.random.uniform(1.20, 1.60)
        py_tier1_restricted = py_tier1_unrestricted * np.random.uniform(0, 0.08)
        py_tier2 = py_tier1_unrestricted * np.random.uniform(0.03, 0.12)
        py_tier3 = 0
        py_total = py_tier1_unrestricted + py_tier1_restricted + py_tier2 + py_tier3

        # Current year (with movement)
        movement_factor = np.random.uniform(-0.10, 0.20)
        cy_tier1_unrestricted = py_tier1_unrestricted * (1 + movement_factor)
        cy_tier1_restricted = py_tier1_restricted * (1 + movement_factor * 0.5)
        cy_tier2 = py_tier2 * (1 + movement_factor * 0.3)
        cy_tier3 = 0
        cy_total = cy_tier1_unrestricted + cy_tier1_restricted + cy_tier2 + cy_tier3

        for year, tier1_u, tier1_r, tier2, tier3, total in [
            (PRIOR_YEAR, py_tier1_unrestricted, py_tier1_restricted, py_tier2, py_tier3, py_total),
            (REPORTING_YEAR, cy_tier1_unrestricted, cy_tier1_restricted, cy_tier2, cy_tier3, cy_total)
        ]:
            eligible_scr = total
            eligible_mcr = tier1_u + min(tier1_r, total * 0.2)

            records.append({
                'Syndicate': syn,
                'ReportingYear': year,
                'YearEnd': datetime(year, 12, 31),
                'Tier1_Unrestricted_GBP_M': round(tier1_u, 2),
                'Tier1_Restricted_GBP_M': round(tier1_r, 2),
                'Tier2_GBP_M': round(tier2, 2),
                'Tier3_GBP_M': round(tier3, 2),
                'TotalOwnFunds_GBP_M': round(total, 2),
                'Eligible_SCR_GBP_M': round(eligible_scr, 2),
                'Eligible_MCR_GBP_M': round(eligible_mcr, 2),
                'SCR_GBP_M': round(scr, 2),
                'MCR_GBP_M': round(mcr, 2),
                'SCR_Coverage_Pct': round((eligible_scr / scr) * 100, 1),
                'MCR_Coverage_Pct': round((eligible_mcr / mcr) * 100, 1),
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# ASR_240_Technical_Provisions_By_LOB - S.17.01.02 Annual TP by LOB
# =============================================================================
def generate_asr_240_technical_provisions_by_lob():
    """Full annual breakdown of technical provisions by Solvency II LOB"""
    records = []
    for syn in SYNDICATES:
        total_tp = np.random.uniform(300, 900)
        weights = np.random.dirichlet(np.ones(len(SII_LINES_OF_BUSINESS)))

        for i, (lob_code, lob_name) in enumerate(SII_LINES_OF_BUSINESS):
            lob_tp = total_tp * weights[i]

            # Split into components
            premium_provision = lob_tp * np.random.uniform(0.15, 0.35)
            claims_provision = lob_tp - premium_provision

            # Best estimate and risk margin
            be_premium = premium_provision * np.random.uniform(0.90, 0.98)
            rm_premium = premium_provision - be_premium
            be_claims = claims_provision * np.random.uniform(0.92, 0.98)
            rm_claims = claims_provision - be_claims

            # Gross and RI
            ri_recov_pct = np.random.uniform(0.15, 0.40)
            gross_be = (be_premium + be_claims) / (1 - ri_recov_pct)
            ri_recov = gross_be * ri_recov_pct

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'YearEnd': datetime(REPORTING_YEAR, 12, 31),
                'LOB_Code': lob_code,
                'LOB_Name': lob_name,
                # Premium Provision
                'PremiumProvision_BE_GBP_M': round(be_premium, 2),
                'PremiumProvision_RM_GBP_M': round(rm_premium, 2),
                'PremiumProvision_Total_GBP_M': round(premium_provision, 2),
                # Claims Provision
                'ClaimsProvision_BE_GBP_M': round(be_claims, 2),
                'ClaimsProvision_RM_GBP_M': round(rm_claims, 2),
                'ClaimsProvision_Total_GBP_M': round(claims_provision, 2),
                # Totals
                'Total_BE_GBP_M': round(be_premium + be_claims, 2),
                'Total_RM_GBP_M': round(rm_premium + rm_claims, 2),
                'Total_TP_GBP_M': round(lob_tp, 2),
                # Gross and RI
                'Gross_BE_GBP_M': round(gross_be, 2),
                'RI_Recoverables_GBP_M': round(ri_recov, 2),
                'Net_BE_GBP_M': round(be_premium + be_claims, 2),
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# ASR_280_SCR_Components - S.25.01.21 Annual SCR Calculation
# =============================================================================
def generate_asr_280_scr_components():
    """Annual SCR calculation with full component breakdown"""
    records = []
    scr_components = [
        ('MARKET', 'Market Risk', 0.18),
        ('MARKET_IR', 'Interest Rate Risk', 0.04),
        ('MARKET_EQ', 'Equity Risk', 0.03),
        ('MARKET_PROP', 'Property Risk', 0.02),
        ('MARKET_SPREAD', 'Spread Risk', 0.06),
        ('MARKET_FX', 'Currency Risk', 0.03),
        ('COUNTERPARTY', 'Counterparty Default Risk', 0.08),
        ('HEALTH', 'Health Underwriting Risk', 0.02),
        ('NON_LIFE', 'Non-Life Underwriting Risk', 0.45),
        ('NL_PREM_RES', 'NL Premium and Reserve Risk', 0.30),
        ('NL_CAT', 'NL Catastrophe Risk', 0.15),
        ('LIFE', 'Life Underwriting Risk', 0.02),
        ('INTANGIBLE', 'Intangible Asset Risk', 0.00),
        ('BSCR_UNDIV', 'Basic SCR (Undiversified)', 0.75),
        ('DIVERSIFICATION', 'Diversification Benefit', -0.20),
        ('BSCR', 'Basic SCR', 0.55),
        ('OPERATIONAL', 'Operational Risk', 0.06),
        ('LAC_TP', 'Loss Absorbing Capacity of TP', -0.02),
        ('LAC_DT', 'Loss Absorbing Capacity of DT', -0.03),
        ('SCR', 'Solvency Capital Requirement', 0.56)
    ]

    for syn in SYNDICATES:
        base_scr = np.random.uniform(80, 200)

        for comp_code, comp_name, base_weight in scr_components:
            weight = base_weight * np.random.uniform(0.8, 1.2)
            amount = base_scr * weight

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'YearEnd': datetime(REPORTING_YEAR, 12, 31),
                'ComponentCode': comp_code,
                'ComponentName': comp_name,
                'Amount_GBP_M': round(amount, 2),
                'Pct_of_SCR': round(weight * 100 / 0.56, 1),  # As % of final SCR
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# ASR_510_MCR - S.28.01.01 Annual MCR Calculation
# =============================================================================
def generate_asr_510_mcr():
    """Annual Minimum Capital Requirement calculation"""
    records = []
    for syn in SYNDICATES:
        scr = np.random.uniform(80, 200)

        # MCR calculation components
        linear_mcr = scr * np.random.uniform(0.20, 0.30)
        scr_cap = scr * 0.45  # 45% of SCR
        scr_floor = scr * 0.25  # 25% of SCR
        absolute_floor = 3.7  # EUR 3.7m absolute floor (approx GBP)

        # Combined MCR
        combined_mcr = max(min(linear_mcr, scr_cap), scr_floor, absolute_floor)

        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'YearEnd': datetime(REPORTING_YEAR, 12, 31),
            'LinearMCR_GBP_M': round(linear_mcr, 2),
            'SCR_GBP_M': round(scr, 2),
            'MCR_Cap_45Pct_SCR_GBP_M': round(scr_cap, 2),
            'MCR_Floor_25Pct_SCR_GBP_M': round(scr_floor, 2),
            'AbsoluteFloor_GBP_M': round(absolute_floor, 2),
            'CombinedMCR_GBP_M': round(combined_mcr, 2),
            'MCR_Ratio_to_SCR_Pct': round((combined_mcr / scr) * 100, 1),
            'Currency': 'GBP'
        })
    return pd.DataFrame(records)

# =============================================================================
# ASR_910_SFCR_Metrics - Public Disclosure / SFCR Summary
# =============================================================================
def generate_asr_910_sfcr_metrics():
    """Key metrics for Solvency and Financial Condition Report (SFCR)"""
    records = []
    for syn in SYNDICATES:
        gwp = np.random.uniform(200, 700)
        nep = gwp * np.random.uniform(0.80, 0.92)
        claims = nep * np.random.uniform(0.50, 0.75)
        expenses = nep * np.random.uniform(0.25, 0.38)
        uw_result = nep - claims - expenses
        inv_return = gwp * np.random.uniform(0.02, 0.05)
        total_result = uw_result + inv_return

        scr = np.random.uniform(80, 200)
        mcr = scr * np.random.uniform(0.28, 0.35)
        own_funds = scr * np.random.uniform(1.25, 1.85)

        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'YearEnd': datetime(REPORTING_YEAR, 12, 31),
            # Business Performance
            'GWP_GBP_M': round(gwp, 2),
            'NEP_GBP_M': round(nep, 2),
            'ClaimsIncurred_GBP_M': round(claims, 2),
            'Expenses_GBP_M': round(expenses, 2),
            'UnderwritingResult_GBP_M': round(uw_result, 2),
            'InvestmentReturn_GBP_M': round(inv_return, 2),
            'TotalResult_GBP_M': round(total_result, 2),
            'LossRatio_Pct': round((claims / nep) * 100, 1),
            'ExpenseRatio_Pct': round((expenses / nep) * 100, 1),
            'CombinedRatio_Pct': round(((claims + expenses) / nep) * 100, 1),
            # Capital
            'SCR_GBP_M': round(scr, 2),
            'MCR_GBP_M': round(mcr, 2),
            'OwnFunds_GBP_M': round(own_funds, 2),
            'SCR_Coverage_Pct': round((own_funds / scr) * 100, 1),
            'MCR_Coverage_Pct': round((own_funds / mcr) * 100, 1),
            # Risk Profile Summary
            'DominantRisk': np.random.choice(['Non-Life UW', 'Market', 'Catastrophe', 'Reserve']),
            'MaterialChanges': np.random.choice(['None', 'Business Mix', 'RI Structure', 'Market Conditions']),
            'Currency': 'GBP'
        })
    return pd.DataFrame(records)

# =============================================================================
# ASR_TP_Reconciliation - Technical Provisions Reconciliation (Annual only)
# =============================================================================
def generate_asr_tp_reconciliation():
    """Annual reconciliation of technical provisions - not available quarterly"""
    records = []
    recon_items = [
        ('OPEN_TP', 'Opening Technical Provisions'),
        ('PREM_WRITTEN', 'Premiums Written'),
        ('PREM_EARNED', 'Change in Unearned Premium'),
        ('CLAIMS_PAID', 'Claims Paid'),
        ('CLAIMS_MOVE', 'Movement in Claims Outstanding'),
        ('IBNR_MOVE', 'Movement in IBNR'),
        ('RM_MOVE', 'Movement in Risk Margin'),
        ('FX_IMPACT', 'Foreign Exchange Impact'),
        ('OTHER', 'Other Movements'),
        ('CLOSE_TP', 'Closing Technical Provisions')
    ]

    for syn in SYNDICATES:
        opening_tp = np.random.uniform(300, 800)
        prem_written = np.random.uniform(150, 400)
        prem_earned = np.random.uniform(-30, 30)
        claims_paid = np.random.uniform(-200, -80)
        claims_move = np.random.uniform(-50, 50)
        ibnr_move = np.random.uniform(-30, 30)
        rm_move = np.random.uniform(-10, 10)
        fx_impact = np.random.uniform(-20, 20)
        other = np.random.uniform(-10, 10)

        closing_tp = opening_tp + prem_written + prem_earned + claims_paid + claims_move + ibnr_move + rm_move + fx_impact + other

        amounts = {
            'OPEN_TP': opening_tp,
            'PREM_WRITTEN': prem_written,
            'PREM_EARNED': prem_earned,
            'CLAIMS_PAID': claims_paid,
            'CLAIMS_MOVE': claims_move,
            'IBNR_MOVE': ibnr_move,
            'RM_MOVE': rm_move,
            'FX_IMPACT': fx_impact,
            'OTHER': other,
            'CLOSE_TP': closing_tp
        }

        for item_code, item_name in recon_items:
            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'ItemCode': item_code,
                'ItemName': item_name,
                'Amount_GBP_M': round(amounts[item_code], 2),
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# Generate all tables
# =============================================================================

# Control
ASR_001_Control = generate_asr_001_control()

# Balance Sheet and Own Funds
ASR_002_Balance_Sheet = generate_asr_002_balance_sheet()
ASR_220_Own_Funds = generate_asr_220_own_funds()

# Variation Analysis (Annual only)
ASR_210_Variation_Analysis = generate_asr_210_variation_analysis()

# Technical Provisions
ASR_240_Technical_Provisions_By_LOB = generate_asr_240_technical_provisions_by_lob()
ASR_TP_Reconciliation = generate_asr_tp_reconciliation()

# Capital Requirements
ASR_280_SCR_Components = generate_asr_280_scr_components()
ASR_510_MCR = generate_asr_510_mcr()

# Public Disclosure
ASR_910_SFCR_Metrics = generate_asr_910_sfcr_metrics()

# Summary statistics
print(f"ASR_001_Control: {len(ASR_001_Control)} rows")
print(f"ASR_002_Balance_Sheet: {len(ASR_002_Balance_Sheet)} rows")
print(f"ASR_210_Variation_Analysis: {len(ASR_210_Variation_Analysis)} rows")
print(f"ASR_220_Own_Funds: {len(ASR_220_Own_Funds)} rows")
print(f"ASR_240_Technical_Provisions_By_LOB: {len(ASR_240_Technical_Provisions_By_LOB)} rows")
print(f"ASR_280_SCR_Components: {len(ASR_280_SCR_Components)} rows")
print(f"ASR_510_MCR: {len(ASR_510_MCR)} rows")
print(f"ASR_910_SFCR_Metrics: {len(ASR_910_SFCR_Metrics)} rows")
print(f"ASR_TP_Reconciliation: {len(ASR_TP_Reconciliation)} rows")
