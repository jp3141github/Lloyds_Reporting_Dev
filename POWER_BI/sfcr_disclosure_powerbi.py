"""
Lloyd's SFCR (Solvency and Financial Condition Report) - Power BI Synthetic Data Generator
===========================================================================================

Generates synthetic data for SFCR public disclosure requirements.

SFCR Structure (per Solvency II Delegated Regulation Articles 290-298):
- Section A: Business and Performance
- Section B: System of Governance
- Section C: Risk Profile
- Section D: Valuation for Solvency Purposes
- Section E: Capital Management
- Annexes: Public QRT subset

Note: RSR (Regular Supervisory Report) requirement ceased 31 December 2023.

Usage in Power BI:
    Get Data > Python script > Paste entire file contents

Author: Lloyd's Reporting Development Team
Version: 1.0
Date: 2024-11-23
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# =============================================================================
# CONFIGURATION
# =============================================================================

SYNDICATES = [33, 623, 1183, 1910, 2010, 2525, 2791, 2987, 4242, 5000]
REPORTING_YEAR = 2024
AS_AT_DATE = '2024-12-31'

SII_LOB = [
    'Medical expense', 'Income protection', 'Workers compensation',
    'Motor vehicle liability', 'Marine aviation transport',
    'Fire and other damage', 'General liability', 'Credit and suretyship',
    'Misc financial loss', 'Non-proportional casualty', 'Non-proportional property'
]

# =============================================================================
# SECTION A - BUSINESS AND PERFORMANCE
# =============================================================================

def generate_sfcr_a1_business_overview():
    """Section A.1 - Business Overview"""
    data = []
    for syn in SYNDICATES:
        row = {
            'syndicate': syn,
            'reporting_year': REPORTING_YEAR,
            'syndicate_name': f'Syndicate {syn}',
            'managing_agent': f'Managing Agent {syn // 100}',
            'year_of_formation': random.randint(1980, 2020),
            'primary_regulator': 'PRA/FCA via Lloyd\'s',
            'auditor': random.choice(['PwC', 'Deloitte', 'KPMG', 'EY']),
            'business_description': f'Syndicate {syn} underwrites a diversified portfolio of specialty insurance and reinsurance',
            'geographic_focus': 'Global with emphasis on UK, US, and Europe',
            'key_lines_of_business': 'Property, Casualty, Marine, Specialty',
            'material_changes': 'No material changes to business structure during the period',
            'stamp_capacity_gbp_m': np.random.uniform(200, 800),
            'capacity_utilisation_pct': np.random.uniform(70, 95)
        }
        data.append(row)
    return pd.DataFrame(data)

def generate_sfcr_a2_underwriting():
    """Section A.2 - Underwriting Performance"""
    data = []
    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        for lob in SII_LOB:
            gwp = np.random.uniform(20, 150) * scale * 1e6
            row = {
                'syndicate': syn,
                'reporting_year': REPORTING_YEAR,
                'line_of_business': lob,
                'gross_written_premium': gwp,
                'net_written_premium': gwp * np.random.uniform(0.65, 0.85),
                'gross_earned_premium': gwp * np.random.uniform(0.90, 0.98),
                'net_earned_premium': gwp * np.random.uniform(0.60, 0.80),
                'gross_claims_incurred': gwp * np.random.uniform(0.45, 0.70),
                'net_claims_incurred': gwp * np.random.uniform(0.35, 0.55),
                'expenses': gwp * np.random.uniform(0.28, 0.38),
                'underwriting_result': gwp * np.random.uniform(-0.10, 0.15),
                'loss_ratio': np.random.uniform(50, 75),
                'expense_ratio': np.random.uniform(28, 38),
                'combined_ratio': np.random.uniform(88, 105),
                'prior_year_reserve_movement': gwp * np.random.uniform(-0.05, 0.05)
            }
            data.append(row)
    return pd.DataFrame(data)

def generate_sfcr_a3_investment():
    """Section A.3 - Investment Performance"""
    data = []
    asset_classes = ['Government bonds', 'Corporate bonds', 'Equities', 'Cash', 'Other']
    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        total_assets = np.random.uniform(400, 1200) * scale * 1e6
        for asset in asset_classes:
            weight = {'Government bonds': 0.40, 'Corporate bonds': 0.35, 'Equities': 0.10, 'Cash': 0.10, 'Other': 0.05}[asset]
            value = total_assets * weight * np.random.uniform(0.8, 1.2)
            row = {
                'syndicate': syn,
                'reporting_year': REPORTING_YEAR,
                'asset_class': asset,
                'market_value': value,
                'percentage_of_portfolio': weight * 100,
                'investment_income': value * np.random.uniform(0.02, 0.05),
                'realised_gains_losses': value * np.random.uniform(-0.02, 0.04),
                'unrealised_gains_losses': value * np.random.uniform(-0.03, 0.05),
                'total_return': value * np.random.uniform(0.01, 0.08),
                'total_return_pct': np.random.uniform(1, 8),
                'average_duration': np.random.uniform(2, 6) if 'bond' in asset.lower() else None,
                'average_credit_quality': random.choice(['AA', 'A', 'BBB']) if 'bond' in asset.lower() else None
            }
            data.append(row)
    return pd.DataFrame(data)

# =============================================================================
# SECTION B - SYSTEM OF GOVERNANCE
# =============================================================================

def generate_sfcr_b_governance():
    """Section B - System of Governance"""
    data = []
    roles = ['Board of Directors', 'Audit Committee', 'Risk Committee', 'Remuneration Committee',
             'CEO', 'CFO', 'CRO', 'CUO', 'Compliance Officer', 'Actuary']
    for syn in SYNDICATES:
        for role in roles:
            row = {
                'syndicate': syn,
                'reporting_year': REPORTING_YEAR,
                'role': role,
                'role_holder': f'{role} - Syndicate {syn}',
                'fit_and_proper_confirmed': 'Yes',
                'responsibilities': f'Responsible for {role.lower()} functions',
                'reporting_line': 'Board' if role not in ['Board of Directors'] else 'Members',
                'meetings_per_year': random.randint(4, 12),
                'key_function': 'Yes' if role in ['CRO', 'Compliance Officer', 'Actuary', 'Audit Committee'] else 'No'
            }
            data.append(row)
    return pd.DataFrame(data)

# =============================================================================
# SECTION C - RISK PROFILE
# =============================================================================

def generate_sfcr_c_risk_profile():
    """Section C - Risk Profile"""
    data = []
    risk_categories = [
        ('Underwriting risk', 'Insurance risk from underwriting activities'),
        ('Market risk', 'Risk from adverse movements in financial markets'),
        ('Credit risk', 'Risk of counterparty default'),
        ('Liquidity risk', 'Risk of inability to meet obligations'),
        ('Operational risk', 'Risk from inadequate processes or systems'),
        ('Strategic risk', 'Risk from business strategy decisions'),
        ('Reputational risk', 'Risk of damage to reputation'),
        ('Regulatory risk', 'Risk from regulatory changes')
    ]
    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        total_scr = np.random.uniform(80, 250) * scale * 1e6
        for risk, description in risk_categories:
            risk_weights = {
                'Underwriting risk': 0.45, 'Market risk': 0.25, 'Credit risk': 0.10,
                'Liquidity risk': 0.05, 'Operational risk': 0.08, 'Strategic risk': 0.03,
                'Reputational risk': 0.02, 'Regulatory risk': 0.02
            }
            row = {
                'syndicate': syn,
                'reporting_year': REPORTING_YEAR,
                'risk_category': risk,
                'risk_description': description,
                'risk_exposure_gbp': total_scr * risk_weights[risk],
                'risk_exposure_pct_scr': risk_weights[risk] * 100,
                'risk_appetite': random.choice(['Low', 'Medium', 'High']),
                'risk_tolerance': f'{np.random.uniform(10, 30):.1f}% of capital',
                'key_mitigants': f'Diversification, reinsurance, limits for {risk.lower()}',
                'stress_test_impact': total_scr * risk_weights[risk] * np.random.uniform(0.1, 0.3),
                'year_on_year_change': np.random.uniform(-15, 20)
            }
            data.append(row)
    return pd.DataFrame(data)

# =============================================================================
# SECTION D - VALUATION FOR SOLVENCY
# =============================================================================

def generate_sfcr_d_valuation():
    """Section D - Valuation for Solvency Purposes"""
    data = []
    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        total_assets = np.random.uniform(600, 1500) * scale * 1e6
        total_tp = np.random.uniform(300, 900) * scale * 1e6
        row = {
            'syndicate': syn,
            'reporting_year': REPORTING_YEAR,
            # Assets
            'total_assets_sii': total_assets,
            'total_assets_gaap': total_assets * np.random.uniform(0.98, 1.02),
            'assets_valuation_difference': total_assets * np.random.uniform(-0.02, 0.02),
            'assets_valuation_method': 'Mark to market / Mark to model',
            # Technical Provisions
            'tp_best_estimate_claims': total_tp * 0.70,
            'tp_best_estimate_premium': total_tp * 0.25,
            'tp_risk_margin': total_tp * 0.05,
            'tp_total': total_tp,
            'tp_gaap': total_tp * np.random.uniform(0.95, 1.05),
            'tp_sii_vs_gaap_difference': total_tp * np.random.uniform(-0.05, 0.05),
            'discount_rate_used': np.random.uniform(2, 4),
            'expense_allowance': total_tp * np.random.uniform(0.02, 0.04),
            # Other Liabilities
            'other_liabilities_sii': total_assets * np.random.uniform(0.05, 0.15),
            'deferred_tax_liability': total_assets * np.random.uniform(0.01, 0.03)
        }
        data.append(row)
    return pd.DataFrame(data)

# =============================================================================
# SECTION E - CAPITAL MANAGEMENT
# =============================================================================

def generate_sfcr_e_capital():
    """Section E - Capital Management"""
    data = []
    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        scr = np.random.uniform(80, 250) * scale * 1e6
        mcr = scr * np.random.uniform(0.30, 0.40)
        own_funds = scr * np.random.uniform(1.20, 1.80)
        row = {
            'syndicate': syn,
            'reporting_year': REPORTING_YEAR,
            # Own Funds
            'tier1_unrestricted': own_funds * 0.85,
            'tier1_restricted': own_funds * 0.05,
            'tier2': own_funds * 0.08,
            'tier3': own_funds * 0.02,
            'total_own_funds': own_funds,
            'eligible_own_funds_scr': own_funds,
            'eligible_own_funds_mcr': own_funds * 0.90,
            # Capital Requirements
            'scr': scr,
            'mcr': mcr,
            'scr_coverage_ratio': (own_funds / scr) * 100,
            'mcr_coverage_ratio': (own_funds * 0.90 / mcr) * 100,
            # SCR Breakdown
            'scr_market_risk': scr * np.random.uniform(0.20, 0.30),
            'scr_counterparty_risk': scr * np.random.uniform(0.08, 0.15),
            'scr_underwriting_risk': scr * np.random.uniform(0.50, 0.60),
            'scr_operational_risk': scr * np.random.uniform(0.05, 0.10),
            'scr_diversification': scr * np.random.uniform(-0.15, -0.25),
            # Capital Policy
            'target_solvency_ratio': np.random.uniform(130, 160),
            'capital_add_on': 0,
            'dividend_paid': own_funds * np.random.uniform(0, 0.10),
            'capital_movements': own_funds * np.random.uniform(-0.05, 0.10)
        }
        data.append(row)
    return pd.DataFrame(data)

# =============================================================================
# ANNEX - PUBLIC QRT TEMPLATES
# =============================================================================

def generate_sfcr_qrt_s02_balance_sheet():
    """Public QRT S.02.01.02 - Balance Sheet"""
    data = []
    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        total_investments = np.random.uniform(400, 1200) * scale * 1e6
        tp = np.random.uniform(300, 900) * scale * 1e6
        row = {
            'syndicate': syn,
            'as_at_date': AS_AT_DATE,
            'template': 'S.02.01.02',
            'intangible_assets': 0,
            'deferred_tax_assets': total_investments * 0.02,
            'property_plant_equipment': total_investments * 0.01,
            'investments': total_investments,
            'ri_recoverables': tp * np.random.uniform(0.15, 0.30),
            'insurance_receivables': total_investments * np.random.uniform(0.10, 0.20),
            'cash_and_equivalents': total_investments * np.random.uniform(0.05, 0.10),
            'other_assets': total_investments * 0.02,
            'total_assets': total_investments * 1.3,
            'technical_provisions_best_estimate': tp * 0.95,
            'technical_provisions_risk_margin': tp * 0.05,
            'technical_provisions_total': tp,
            'other_liabilities': total_investments * 0.15,
            'total_liabilities': tp + total_investments * 0.15,
            'excess_of_assets_over_liabilities': total_investments * 1.3 - tp - total_investments * 0.15
        }
        data.append(row)
    return pd.DataFrame(data)

def generate_sfcr_qrt_s05_premiums():
    """Public QRT S.05.01.02 - Premiums, Claims, Expenses by LoB"""
    data = []
    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        for lob in SII_LOB[:8]:
            gwp = np.random.uniform(20, 150) * scale * 1e6
            row = {
                'syndicate': syn,
                'as_at_date': AS_AT_DATE,
                'template': 'S.05.01.02',
                'line_of_business': lob,
                'gross_written_premium': gwp,
                'gross_earned_premium': gwp * 0.95,
                'gross_claims_incurred': gwp * np.random.uniform(0.50, 0.70),
                'gross_expenses': gwp * np.random.uniform(0.28, 0.35),
                'reinsurance_balance': gwp * np.random.uniform(-0.10, 0.05),
                'net_combined_ratio': np.random.uniform(88, 105)
            }
            data.append(row)
    return pd.DataFrame(data)

def generate_sfcr_qrt_s23_own_funds():
    """Public QRT S.23.01.01 - Own Funds"""
    data = []
    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        own_funds = np.random.uniform(150, 400) * scale * 1e6
        row = {
            'syndicate': syn,
            'as_at_date': AS_AT_DATE,
            'template': 'S.23.01.01',
            'ordinary_share_capital': own_funds * 0.30,
            'reconciliation_reserve': own_funds * 0.50,
            'other_basic_own_funds': own_funds * 0.20,
            'total_basic_own_funds': own_funds,
            'total_ancillary_own_funds': 0,
            'total_eligible_own_funds_scr': own_funds,
            'total_eligible_own_funds_mcr': own_funds * 0.90,
            'scr': own_funds / np.random.uniform(1.20, 1.80),
            'mcr': own_funds / np.random.uniform(1.20, 1.80) * 0.35,
            'ratio_eligible_to_scr': np.random.uniform(120, 180),
            'ratio_eligible_to_mcr': np.random.uniform(350, 500)
        }
        data.append(row)
    return pd.DataFrame(data)

def generate_sfcr_qrt_s25_scr():
    """Public QRT S.25.01.21 - SCR"""
    data = []
    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        scr = np.random.uniform(80, 250) * scale * 1e6
        row = {
            'syndicate': syn,
            'as_at_date': AS_AT_DATE,
            'template': 'S.25.01.21',
            'market_risk': scr * 0.25,
            'counterparty_default_risk': scr * 0.10,
            'life_underwriting_risk': scr * 0.02,
            'health_underwriting_risk': scr * 0.05,
            'non_life_underwriting_risk': scr * 0.55,
            'diversification': scr * -0.20,
            'intangible_asset_risk': 0,
            'basic_scr': scr * 0.95,
            'operational_risk': scr * 0.08,
            'loss_absorbing_capacity_tp': scr * -0.03,
            'loss_absorbing_capacity_dt': 0,
            'capital_add_on': 0,
            'scr': scr,
            'approach': random.choice(['Standard Formula', 'Partial Internal Model', 'Full Internal Model'])
        }
        data.append(row)
    return pd.DataFrame(data)

# =============================================================================
# GENERATE ALL TABLES
# =============================================================================

# Section A - Business and Performance
SFCR_A1_Business = generate_sfcr_a1_business_overview()
SFCR_A2_Underwriting = generate_sfcr_a2_underwriting()
SFCR_A3_Investment = generate_sfcr_a3_investment()

# Section B - Governance
SFCR_B_Governance = generate_sfcr_b_governance()

# Section C - Risk Profile
SFCR_C_Risk_Profile = generate_sfcr_c_risk_profile()

# Section D - Valuation
SFCR_D_Valuation = generate_sfcr_d_valuation()

# Section E - Capital
SFCR_E_Capital = generate_sfcr_e_capital()

# Annex - Public QRTs
SFCR_QRT_S02_Balance_Sheet = generate_sfcr_qrt_s02_balance_sheet()
SFCR_QRT_S05_Premiums = generate_sfcr_qrt_s05_premiums()
SFCR_QRT_S23_Own_Funds = generate_sfcr_qrt_s23_own_funds()
SFCR_QRT_S25_SCR = generate_sfcr_qrt_s25_scr()

# Print confirmation
print(f"SFCR Solvency and Financial Condition Report - {REPORTING_YEAR}")
print(f"Generated for {len(SYNDICATES)} syndicates")
print(f"Tables: SFCR_A1-A3, SFCR_B, SFCR_C, SFCR_D, SFCR_E, QRT_S02, S05, S23, S25")
print(f"Total: 11 tables covering all SFCR sections")
