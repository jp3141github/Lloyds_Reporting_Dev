"""
Lloyd's QMB (Quarterly Monitoring Return Part B) - Power BI Synthetic Data Generator
====================================================================================

Generates synthetic data for QMB forms - Class of Business analysis by Pure Year of Account.

Key difference from QMA:
- QMA = Reporting years (syndicates with open years)
- QMB = Pure underwriting years (last 5 active underwriting years)

Forms Covered:
- QMB 100: Pure YoA Technical Account
- QMB 105: Premiums/Claims/Expenses by CoB/Currency/YoA
- QMB 105s: Reinsurance by Currency/YoA
- QMB 110: Lloyd's Risk Code Analysis
- QMB 120: Distribution Channel Analysis
- QMB 200: YoA Performance Tracking
- QMB 220: YoA Claims Development

Usage in Power BI:
    Get Data > Python script > Paste entire file contents

Author: Lloyd's Reporting Development Team
Version: 1.0
Date: 2024-11-23
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# =============================================================================
# CONFIGURATION
# =============================================================================

SYNDICATES = [33, 623, 1183, 1910, 2010, 2525, 2791, 2987, 4242, 5000]
REPORTING_YEAR = 2024
QUARTER = 3  # Q1, Q2, Q3, or Q4

# Pure Years of Account (last 5 active years)
PURE_YEARS = list(range(REPORTING_YEAR - 4, REPORTING_YEAR + 1))  # 2020-2024

# Lloyd's Risk Codes
RISK_CODES = {
    'PR': ('Property', ['PR100', 'PR110', 'PR120', 'PR130', 'PR140', 'PR150']),
    'PP': ('Property Proportional RI', ['PP200', 'PP210', 'PP220']),
    'PN': ('Property Non-Proportional RI', ['PN300', 'PN310', 'PN320']),
    'CA': ('Casualty', ['CA400', 'CA410', 'CA420', 'CA430', 'CA440']),
    'CP': ('Casualty Proportional RI', ['CP500', 'CP510']),
    'CN': ('Casualty Non-Proportional RI', ['CN600', 'CN610']),
    'MA': ('Marine', ['MA700', 'MA710', 'MA720', 'MA730']),
    'AV': ('Aviation', ['AV800', 'AV810', 'AV820']),
    'EN': ('Energy', ['EN900', 'EN910', 'EN920']),
    'MO': ('Motor', ['MO100', 'MO110']),
    'AC': ('Accident & Health', ['AC200', 'AC210', 'AC220']),
    'LI': ('Life', ['LI300', 'LI310']),
    'PC': ('Pecuniary', ['PC400', 'PC410', 'PC420']),
    'SP': ('Specialty', ['SP500', 'SP510', 'SP520', 'SP530'])
}

# Distribution Channels
DISTRIBUTION_CHANNELS = ['Open Market', 'Coverholder', 'Lineslip', 'Service Company', 'Direct']

# Currencies
CURRENCIES = ['GBP', 'USD', 'EUR', 'CAD', 'AUD', 'JPY']

# =============================================================================
# QMB 100 - PURE YOA TECHNICAL ACCOUNT
# =============================================================================

def generate_qmb_100():
    """Generate Pure Year of Account Technical Account"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        for yoa in PURE_YEARS:
            development_year = REPORTING_YEAR - yoa
            maturity_factor = min(1.0, development_year / 3)  # Approaches 1 by year 3

            gwp = np.random.uniform(100, 400) * scale * 1e6
            ri_premium = gwp * np.random.uniform(0.15, 0.35)
            nwp = gwp - ri_premium

            earned_factor = min(1.0, (development_year + 0.5 + QUARTER/4))
            gep = gwp * min(earned_factor, 1.0)
            nep = nwp * min(earned_factor, 1.0)

            claims_factor = maturity_factor * np.random.uniform(0.5, 0.75)
            gross_claims = gwp * claims_factor
            ri_recoveries = gross_claims * np.random.uniform(0.15, 0.35)
            net_claims = gross_claims - ri_recoveries

            acquisition_costs = gwp * np.random.uniform(0.20, 0.30)
            admin_expenses = gwp * np.random.uniform(0.05, 0.10)
            total_expenses = acquisition_costs + admin_expenses

            underwriting_result = nep - net_claims - total_expenses

            row = {
                'syndicate': syn,
                'as_at_date': f'{REPORTING_YEAR}-{[3,6,9,12][QUARTER-1]:02d}-{[31,30,30,31][QUARTER-1]}',
                'quarter': f'Q{QUARTER}',
                'reporting_year': REPORTING_YEAR,
                'pure_year_of_account': yoa,
                'development_year': development_year,
                # Premium
                'gross_written_premium': gwp,
                'outward_ri_premium': ri_premium,
                'net_written_premium': nwp,
                'gross_earned_premium': gep,
                'ri_share_earned': ri_premium * min(earned_factor, 1.0),
                'net_earned_premium': nep,
                'unearned_premium_reserve': max(0, gwp - gep),
                # Claims
                'gross_claims_paid': gross_claims * maturity_factor * 0.7,
                'gross_claims_outstanding': gross_claims * (1 - maturity_factor * 0.7),
                'gross_claims_incurred': gross_claims,
                'ri_recoveries_paid': ri_recoveries * maturity_factor * 0.7,
                'ri_recoveries_outstanding': ri_recoveries * (1 - maturity_factor * 0.7),
                'ri_recoveries_incurred': ri_recoveries,
                'net_claims_incurred': net_claims,
                # Expenses
                'brokerage': acquisition_costs * 0.6,
                'commission': acquisition_costs * 0.4,
                'acquisition_costs_total': acquisition_costs,
                'admin_expenses': admin_expenses,
                'total_expenses': total_expenses,
                # Results
                'underwriting_result': underwriting_result,
                'investment_return': nwp * np.random.uniform(0.02, 0.05),
                'total_result': underwriting_result + nwp * np.random.uniform(0.02, 0.05),
                # Ratios
                'loss_ratio_gross': (gross_claims / gep * 100) if gep > 0 else 0,
                'loss_ratio_net': (net_claims / nep * 100) if nep > 0 else 0,
                'expense_ratio': (total_expenses / nep * 100) if nep > 0 else 0,
                'combined_ratio': ((net_claims + total_expenses) / nep * 100) if nep > 0 else 0,
                'yoa_status': 'Open' if yoa >= REPORTING_YEAR - 2 else 'RITC'
            }
            data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# QMB 105 - PREMIUMS/CLAIMS/EXPENSES BY COB/CURRENCY/YOA
# =============================================================================

def generate_qmb_105():
    """Generate Class of Business breakdown"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        for yoa in PURE_YEARS:
            development_year = REPORTING_YEAR - yoa

            for category, (category_name, codes) in RISK_CODES.items():
                for code in codes[:2]:  # Top 2 codes per category
                    for currency in ['GBP', 'USD', 'EUR'][:2]:  # Top 2 currencies

                        # Random weighting for this combination
                        weight = np.random.uniform(0.01, 0.15)
                        gwp_base = np.random.uniform(100, 400) * scale * 1e6
                        gwp = gwp_base * weight

                        if gwp < 100000:  # Skip very small amounts
                            continue

                        maturity = min(1.0, development_year / 3)
                        loss_ratio = np.random.uniform(0.45, 0.80)

                        row = {
                            'syndicate': syn,
                            'quarter': f'Q{QUARTER}',
                            'pure_year_of_account': yoa,
                            'development_year': development_year,
                            'risk_code': code,
                            'risk_category': category,
                            'risk_category_name': category_name,
                            'currency': currency,
                            'gross_written_premium': gwp,
                            'ri_premium_ceded': gwp * np.random.uniform(0.15, 0.35),
                            'net_written_premium': gwp * np.random.uniform(0.65, 0.85),
                            'gross_earned_premium': gwp * min(1.0, development_year + 0.5),
                            'net_earned_premium': gwp * np.random.uniform(0.65, 0.85) * min(1.0, development_year + 0.5),
                            'gross_claims_paid': gwp * loss_ratio * maturity * 0.7,
                            'gross_claims_outstanding': gwp * loss_ratio * (1 - maturity * 0.7),
                            'gross_claims_incurred': gwp * loss_ratio,
                            'net_claims_incurred': gwp * np.random.uniform(0.65, 0.85) * loss_ratio,
                            'acquisition_costs': gwp * np.random.uniform(0.20, 0.30),
                            'admin_expenses': gwp * np.random.uniform(0.05, 0.10),
                            'loss_ratio': loss_ratio * 100,
                            'claim_count': int(gwp / np.random.uniform(50000, 200000)),
                            'policy_count': int(gwp / np.random.uniform(100000, 500000))
                        }
                        data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# QMB 105S - REINSURANCE BY CURRENCY/YOA
# =============================================================================

def generate_qmb_105s():
    """Generate Reinsurance breakdown by currency and YoA"""
    data = []
    ri_types = ['Quota Share', 'Surplus', 'XoL Working', 'XoL Cat', 'Stop Loss']

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        for yoa in PURE_YEARS:
            for currency in ['GBP', 'USD', 'EUR']:
                for ri_type in ri_types:
                    premium_ceded = np.random.uniform(2, 30) * scale * 1e6

                    row = {
                        'syndicate': syn,
                        'quarter': f'Q{QUARTER}',
                        'pure_year_of_account': yoa,
                        'currency': currency,
                        'ri_type': ri_type,
                        'ri_category': 'Proportional' if ri_type in ['Quota Share', 'Surplus'] else 'Non-Proportional',
                        'ri_premium_ceded': premium_ceded,
                        'ri_commission_received': premium_ceded * np.random.uniform(0.20, 0.35) if ri_type in ['Quota Share', 'Surplus'] else 0,
                        'ri_claims_recoveries': premium_ceded * np.random.uniform(0.3, 0.8),
                        'ri_recoveries_outstanding': premium_ceded * np.random.uniform(0.1, 0.4),
                        'ri_bad_debt_provision': premium_ceded * np.random.uniform(0, 0.02),
                        'number_of_treaties': random.randint(1, 5),
                        'average_cession_pct': np.random.uniform(10, 40) if ri_type in ['Quota Share', 'Surplus'] else None
                    }
                    data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# QMB 110 - LLOYD'S RISK CODE ANALYSIS
# =============================================================================

def generate_qmb_110():
    """Generate detailed Risk Code analysis"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        for category, (category_name, codes) in RISK_CODES.items():
            for code in codes:
                total_gwp = np.random.uniform(10, 100) * scale * 1e6
                policy_count = int(total_gwp / np.random.uniform(50000, 300000))

                row = {
                    'syndicate': syn,
                    'quarter': f'Q{QUARTER}',
                    'reporting_year': REPORTING_YEAR,
                    'risk_code': code,
                    'risk_category': category,
                    'risk_category_name': category_name,
                    'gross_written_premium_ytd': total_gwp,
                    'gross_written_premium_qtd': total_gwp * 0.25,
                    'net_written_premium_ytd': total_gwp * np.random.uniform(0.65, 0.85),
                    'policy_count': policy_count,
                    'average_premium': total_gwp / policy_count if policy_count > 0 else 0,
                    'max_line_size': total_gwp / policy_count * np.random.uniform(3, 10) if policy_count > 0 else 0,
                    'gross_claims_ytd': total_gwp * np.random.uniform(0.4, 0.7),
                    'claim_count': int(policy_count * np.random.uniform(0.05, 0.20)),
                    'loss_ratio_ytd': np.random.uniform(45, 80),
                    'prior_year_development': np.random.uniform(-0.05, 0.10) * total_gwp,
                    'rate_change_pct': np.random.uniform(-10, 25),
                    'retention_ratio_pct': np.random.uniform(70, 95)
                }
                data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# QMB 120 - DISTRIBUTION CHANNEL ANALYSIS
# =============================================================================

def generate_qmb_120():
    """Generate Distribution Channel analysis"""
    data = []

    channel_weights = {
        'Open Market': 0.50,
        'Coverholder': 0.25,
        'Lineslip': 0.15,
        'Service Company': 0.08,
        'Direct': 0.02
    }

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        total_gwp = np.random.uniform(200, 600) * scale * 1e6

        for yoa in PURE_YEARS:
            for channel in DISTRIBUTION_CHANNELS:
                weight = channel_weights[channel] * np.random.uniform(0.7, 1.3)
                gwp = total_gwp * weight / len(PURE_YEARS)

                row = {
                    'syndicate': syn,
                    'quarter': f'Q{QUARTER}',
                    'pure_year_of_account': yoa,
                    'distribution_channel': channel,
                    'gross_written_premium': gwp,
                    'net_written_premium': gwp * np.random.uniform(0.65, 0.85),
                    'policy_count': int(gwp / np.random.uniform(50000, 300000)),
                    'claim_count': int(gwp / np.random.uniform(200000, 800000)),
                    'gross_claims_incurred': gwp * np.random.uniform(0.45, 0.75),
                    'net_claims_incurred': gwp * np.random.uniform(0.35, 0.60),
                    'acquisition_cost_ratio': np.random.uniform(20, 35),
                    'loss_ratio': np.random.uniform(50, 75),
                    'combined_ratio': np.random.uniform(88, 105),
                    'average_rate_change': np.random.uniform(-5, 20),
                    'new_business_pct': np.random.uniform(20, 50),
                    'renewal_retention_pct': np.random.uniform(75, 95)
                }
                data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# QMB 200 - YOA PERFORMANCE TRACKING
# =============================================================================

def generate_qmb_200():
    """Generate YoA performance tracking by quarter"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        for yoa in PURE_YEARS:
            for q in range(1, QUARTER + 1):
                development_quarters = (REPORTING_YEAR - yoa) * 4 + q
                ultimate_gwp = np.random.uniform(100, 400) * scale * 1e6

                # Build up pattern
                written_pct = min(1.0, development_quarters / 4)  # Fully written by Q4 of YoA
                earned_pct = min(1.0, max(0, (development_quarters - 2) / 6))
                paid_pct = min(0.9, max(0, (development_quarters - 4) / 12))

                row = {
                    'syndicate': syn,
                    'year': REPORTING_YEAR,
                    'quarter': q,
                    'pure_year_of_account': yoa,
                    'development_quarter': development_quarters,
                    'gwp_to_date': ultimate_gwp * written_pct,
                    'gwp_this_quarter': ultimate_gwp * written_pct * 0.25,
                    'nwp_to_date': ultimate_gwp * written_pct * np.random.uniform(0.65, 0.85),
                    'earned_premium_to_date': ultimate_gwp * earned_pct * np.random.uniform(0.65, 0.85),
                    'unearned_premium': ultimate_gwp * (written_pct - earned_pct) * np.random.uniform(0.65, 0.85),
                    'claims_paid_to_date': ultimate_gwp * paid_pct * np.random.uniform(0.45, 0.65),
                    'claims_outstanding': ultimate_gwp * (np.random.uniform(0.50, 0.70) - paid_pct * 0.7) * np.random.uniform(0.65, 0.85),
                    'claims_incurred_to_date': ultimate_gwp * np.random.uniform(0.45, 0.70) * min(1.0, development_quarters / 8),
                    'ibnr': ultimate_gwp * np.random.uniform(0.05, 0.20) * max(0, 1 - development_quarters / 20),
                    'expense_ratio': np.random.uniform(28, 38),
                    'loss_ratio_to_date': np.random.uniform(50, 75),
                    'combined_ratio_to_date': np.random.uniform(85, 105),
                    'ultimate_loss_ratio_estimate': np.random.uniform(55, 72),
                    'ultimate_combined_ratio_estimate': np.random.uniform(90, 100),
                    'projected_result_pct': np.random.uniform(-5, 15)
                }
                data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# QMB 220 - YOA CLAIMS DEVELOPMENT
# =============================================================================

def generate_qmb_220():
    """Generate YoA claims development triangles"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        for yoa in PURE_YEARS:
            ultimate = np.random.uniform(50, 200) * scale * 1e6

            for dev_year in range(yoa, REPORTING_YEAR + 1):
                dev_period = dev_year - yoa

                # Development pattern (S-curve)
                dev_factor = 1 - (0.75 ** (dev_period + 1))
                paid_to_date = ultimate * dev_factor * np.random.uniform(0.95, 1.05)
                outstanding = ultimate * (1 - dev_factor) * np.random.uniform(0.3, 0.5)
                ibnr = ultimate * (1 - dev_factor) * np.random.uniform(0.5, 0.7)

                row = {
                    'syndicate': syn,
                    'quarter': f'Q{QUARTER}',
                    'pure_year_of_account': yoa,
                    'development_year': dev_year,
                    'development_period': dev_period,
                    'gross_paid_cumulative': paid_to_date,
                    'gross_paid_incremental': paid_to_date * (1 - 0.75) if dev_period > 0 else paid_to_date * 0.25,
                    'gross_case_outstanding': outstanding,
                    'gross_ibnr': ibnr,
                    'gross_ultimate': paid_to_date + outstanding + ibnr,
                    'net_paid_cumulative': paid_to_date * np.random.uniform(0.65, 0.85),
                    'net_case_outstanding': outstanding * np.random.uniform(0.65, 0.85),
                    'net_ibnr': ibnr * np.random.uniform(0.65, 0.85),
                    'net_ultimate': (paid_to_date + outstanding + ibnr) * np.random.uniform(0.65, 0.85),
                    'claim_count_reported': int(ultimate / np.random.uniform(100000, 300000) * dev_factor),
                    'claim_count_closed': int(ultimate / np.random.uniform(100000, 300000) * dev_factor * dev_factor),
                    'average_paid_per_claim': paid_to_date / max(1, int(ultimate / np.random.uniform(100000, 300000) * dev_factor)),
                    'development_factor': 1 / dev_factor if dev_factor > 0 else 10
                }
                data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# QMB SUMMARY
# =============================================================================

def generate_qmb_summary():
    """Generate QMB Summary dashboard"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        total_gwp = np.random.uniform(300, 800) * scale * 1e6

        row = {
            'syndicate': syn,
            'quarter': f'Q{QUARTER}',
            'reporting_year': REPORTING_YEAR,
            # Overall metrics
            'total_gwp_all_yoa': total_gwp,
            'total_nwp_all_yoa': total_gwp * np.random.uniform(0.65, 0.85),
            'total_gep_all_yoa': total_gwp * np.random.uniform(0.85, 0.95),
            'total_nep_all_yoa': total_gwp * np.random.uniform(0.55, 0.75),
            'total_claims_incurred': total_gwp * np.random.uniform(0.45, 0.65),
            # YoA breakdown
            'open_yoa_count': 3,
            'ritc_yoa_count': 2,
            'current_yoa_gwp': total_gwp * 0.35,
            'prior_yoa_gwp': total_gwp * 0.65,
            # Performance
            'overall_loss_ratio': np.random.uniform(55, 70),
            'overall_expense_ratio': np.random.uniform(30, 38),
            'overall_combined_ratio': np.random.uniform(90, 102),
            # Risk code concentration
            'top_5_risk_codes_pct': np.random.uniform(50, 75),
            'number_of_risk_codes': random.randint(30, 60),
            # Distribution
            'open_market_pct': np.random.uniform(40, 60),
            'coverholder_pct': np.random.uniform(20, 35),
            'lineslip_pct': np.random.uniform(10, 20),
            # Claims
            'total_claim_count': int(total_gwp / np.random.uniform(80000, 150000)),
            'large_loss_count': int(total_gwp / np.random.uniform(5000000, 15000000)),
            'large_loss_threshold': 1000000
        }
        data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# GENERATE ALL TABLES
# =============================================================================

# QMB Forms
QMB_100_YoA_Technical = generate_qmb_100()
QMB_105_CoB_Analysis = generate_qmb_105()
QMB_105s_Reinsurance = generate_qmb_105s()
QMB_110_Risk_Code = generate_qmb_110()
QMB_120_Distribution = generate_qmb_120()
QMB_200_YoA_Performance = generate_qmb_200()
QMB_220_Claims_Development = generate_qmb_220()

# Summary
QMB_Summary = generate_qmb_summary()

# Print confirmation
print(f"QMB Quarterly Monitoring Part B - Q{QUARTER} {REPORTING_YEAR}")
print(f"Generated for {len(SYNDICATES)} syndicates, {len(PURE_YEARS)} Pure Years of Account")
print(f"Tables: QMB_100, QMB_105, QMB_105s, QMB_110, QMB_120, QMB_200, QMB_220, QMB_Summary")
print(f"Total: 8 tables covering key QMB forms")
