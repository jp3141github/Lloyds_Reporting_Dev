"""
Lloyd's LCM/LSM Capital Models - Power BI Synthetic Data Generator
==================================================================

Generates synthetic data for Lloyd's capital model submissions.

Models Covered:
- LCM (Lloyd's Catastrophe Model) - Cat risk outputs for internal models
- LSM (Lloyd's Standard Model) - Standard formula approach for syndicates
  without approved internal models (SIABs, new entrants)

Forms Covered:
- LCM 313: Catastrophe Risk Summary
- LCM 314: Peril-by-Peril Breakdown
- LCM 315: Regional Exposure Analysis
- LCM 316: Sensitivity Results
- LSM Market Risk (Solvency II Standard Formula)
- LSM Counterparty Default Risk (Solvency II Standard Formula)
- LSM Insurance Risk (Lloyd's bespoke)
- LSM Operational Risk (Lloyd's bespoke)

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
YOA = 2025  # Year of Account for capital setting

# Catastrophe Perils
CAT_PERILS = [
    ('NA_Hurricane', 'North Atlantic Hurricane', 'Natural'),
    ('NA_Earthquake', 'North American Earthquake', 'Natural'),
    ('EU_Windstorm', 'European Windstorm', 'Natural'),
    ('JP_Typhoon', 'Japan Typhoon', 'Natural'),
    ('JP_Earthquake', 'Japan Earthquake', 'Natural'),
    ('AU_Cyclone', 'Australian Cyclone', 'Natural'),
    ('NZ_Earthquake', 'New Zealand Earthquake', 'Natural'),
    ('Flood', 'Flood (Multi-region)', 'Natural'),
    ('Wildfire', 'Wildfire', 'Natural'),
    ('Terrorism', 'Terrorism', 'Man-made'),
    ('Cyber', 'Cyber Attack', 'Man-made'),
    ('Pandemic', 'Pandemic', 'Man-made'),
    ('Marine_Clash', 'Marine Clash', 'Man-made')
]

# Return Periods
RETURN_PERIODS = [10, 25, 50, 100, 200, 250, 500, 1000]

# Regions
REGIONS = [
    ('NAM', 'North America'), ('EUR', 'Europe'), ('APAC', 'Asia Pacific'),
    ('LATAM', 'Latin America'), ('MEA', 'Middle East & Africa'), ('WW', 'Worldwide')
]

# =============================================================================
# LCM 313 - CATASTROPHE RISK SUMMARY
# =============================================================================

def generate_lcm_313():
    """Generate Catastrophe Risk Summary"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        total_cat_exposure = np.random.uniform(500, 2000) * scale * 1e6

        for peril_code, peril_name, peril_type in CAT_PERILS:
            # Peril weight based on type
            if peril_code == 'NA_Hurricane':
                weight = np.random.uniform(0.25, 0.35)
            elif 'Earthquake' in peril_code:
                weight = np.random.uniform(0.10, 0.20)
            elif peril_code in ['Cyber', 'Terrorism', 'Pandemic']:
                weight = np.random.uniform(0.05, 0.10)
            else:
                weight = np.random.uniform(0.02, 0.08)

            gross_100yr = total_cat_exposure * weight
            ri_recovery = gross_100yr * np.random.uniform(0.30, 0.60)

            row = {
                'syndicate': syn,
                'yoa': YOA,
                'peril_code': peril_code,
                'peril_name': peril_name,
                'peril_type': peril_type,
                'gross_100yr_aep': gross_100yr,
                'gross_250yr_aep': gross_100yr * np.random.uniform(1.4, 1.8),
                'gross_100yr_oep': gross_100yr * np.random.uniform(0.85, 0.95),
                'gross_250yr_oep': gross_100yr * np.random.uniform(1.2, 1.5),
                'ri_recovery_100yr': ri_recovery,
                'ri_recovery_250yr': ri_recovery * np.random.uniform(1.3, 1.6),
                'net_100yr_aep': gross_100yr - ri_recovery,
                'net_250yr_aep': gross_100yr * np.random.uniform(1.4, 1.8) - ri_recovery * np.random.uniform(1.3, 1.6),
                'net_100yr_oep': (gross_100yr - ri_recovery) * np.random.uniform(0.85, 0.95),
                'net_250yr_oep': (gross_100yr * np.random.uniform(1.4, 1.8) - ri_recovery * np.random.uniform(1.3, 1.6)) * np.random.uniform(0.85, 0.95),
                'standard_deviation': gross_100yr * np.random.uniform(0.3, 0.6),
                'coefficient_of_variation': np.random.uniform(0.3, 0.8),
                'expected_annual_loss': gross_100yr * np.random.uniform(0.05, 0.15),
                'contribution_to_scr_pct': weight * 100 * np.random.uniform(0.8, 1.2)
            }
            data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# LCM 314 - PERIL EP CURVES
# =============================================================================

def generate_lcm_314():
    """Generate Peril-by-Peril EP Curves"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        for peril_code, peril_name, peril_type in CAT_PERILS[:8]:  # Top 8 perils
            base_loss = np.random.uniform(50, 200) * scale * 1e6

            for rp in RETURN_PERIODS:
                # EP curve shape - increasing losses at higher return periods
                loss_factor = np.log10(rp) / np.log10(10)  # Scales from 1 at RP10 to 3 at RP1000
                gross_aep = base_loss * loss_factor * np.random.uniform(0.9, 1.1)
                gross_oep = gross_aep * np.random.uniform(0.7, 0.9)
                ri_factor = np.random.uniform(0.30, 0.60)

                row = {
                    'syndicate': syn,
                    'yoa': YOA,
                    'peril_code': peril_code,
                    'peril_name': peril_name,
                    'return_period': rp,
                    'exceedance_probability': 1 / rp,
                    'gross_aep_loss': gross_aep,
                    'gross_oep_loss': gross_oep,
                    'ri_recovery_aep': gross_aep * ri_factor,
                    'ri_recovery_oep': gross_oep * ri_factor,
                    'net_aep_loss': gross_aep * (1 - ri_factor),
                    'net_oep_loss': gross_oep * (1 - ri_factor),
                    'model_used': random.choice(['AIR', 'RMS', 'CoreLogic', 'JBA', 'Internal']),
                    'confidence_level': random.choice(['High', 'Medium', 'Low'])
                }
                data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# LCM 315 - REGIONAL EXPOSURE ANALYSIS
# =============================================================================

def generate_lcm_315():
    """Generate Regional Exposure Analysis"""
    data = []

    region_weights = {
        'NAM': 0.40, 'EUR': 0.30, 'APAC': 0.20, 'LATAM': 0.05, 'MEA': 0.03, 'WW': 0.02
    }

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        total_exposure = np.random.uniform(2000, 8000) * scale * 1e6

        for region_code, region_name in REGIONS:
            weight = region_weights[region_code] * np.random.uniform(0.7, 1.3)
            tiv = total_exposure * weight

            row = {
                'syndicate': syn,
                'yoa': YOA,
                'region_code': region_code,
                'region_name': region_name,
                'total_insured_value': tiv,
                'gross_written_premium': tiv * np.random.uniform(0.005, 0.015),
                'policy_count': int(tiv / np.random.uniform(5000000, 20000000)),
                'primary_perils': 'Hurricane, Earthquake' if region_code == 'NAM' else 'Windstorm, Flood' if region_code == 'EUR' else 'Typhoon, Earthquake',
                'average_rate_on_line': np.random.uniform(0.5, 2.0),
                'max_single_risk': tiv * np.random.uniform(0.01, 0.05),
                'agg_limit': tiv * np.random.uniform(0.15, 0.30),
                'pml_100yr': tiv * np.random.uniform(0.05, 0.15),
                'pml_250yr': tiv * np.random.uniform(0.08, 0.20),
                'modeled_pct': np.random.uniform(70, 95),
                'geocoding_quality': random.choice(['High', 'Medium', 'Low'])
            }
            data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# LCM 316 - SENSITIVITY RESULTS
# =============================================================================

def generate_lcm_316():
    """Generate Sensitivity Test Results"""
    data = []

    sensitivities = [
        ('+10% Premium Volume', 'premium_volume', 1.10),
        ('+10% Cat Exposure', 'cat_exposure', 1.10),
        ('+20% Loss Ratio', 'loss_ratio', 1.20),
        ('100bp Interest Rate Rise', 'interest_rate', 1.05),
        ('10% Equity Decline', 'equity', 0.90),
        ('10% FX Adverse', 'fx', 1.08),
        ('Major Cat Loss ($500M)', 'major_cat', 1.25),
        ('Pandemic Scenario', 'pandemic', 1.15),
        ('Cyber Aggregation', 'cyber', 1.12),
        ('Climate Change +1C', 'climate', 1.08)
    ]

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        base_scr = np.random.uniform(80, 250) * scale * 1e6

        for sensitivity_name, sensitivity_type, impact_factor in sensitivities:
            stressed_scr = base_scr * impact_factor * np.random.uniform(0.95, 1.05)

            row = {
                'syndicate': syn,
                'yoa': YOA,
                'sensitivity_name': sensitivity_name,
                'sensitivity_type': sensitivity_type,
                'base_scr': base_scr,
                'stressed_scr': stressed_scr,
                'scr_change_abs': stressed_scr - base_scr,
                'scr_change_pct': ((stressed_scr / base_scr) - 1) * 100,
                'base_coverage_ratio': np.random.uniform(130, 170),
                'stressed_coverage_ratio': np.random.uniform(130, 170) / impact_factor,
                'still_compliant': True if np.random.uniform(130, 170) / impact_factor > 100 else False,
                'management_action_required': 'No' if impact_factor < 1.15 else 'Monitor',
                'reverse_stress_breach_point': f'{(impact_factor - 1) * 100 * np.random.uniform(2, 4):.0f}%'
            }
            data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# LSM - MARKET RISK (SOLVENCY II STANDARD FORMULA)
# =============================================================================

def generate_lsm_market_risk():
    """Generate LSM Market Risk calculation (SII Standard Formula)"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        total_investments = np.random.uniform(400, 1200) * scale * 1e6

        # Market risk sub-modules
        ir_up = total_investments * 0.40 * np.random.uniform(0.02, 0.05)  # Bond sensitivity to rates up
        ir_down = total_investments * 0.40 * np.random.uniform(0.01, 0.03)
        equity_type1 = total_investments * 0.08 * 0.39  # Listed equity shock
        equity_type2 = total_investments * 0.02 * 0.49  # Other equity shock
        property_shock = total_investments * 0.02 * 0.25
        spread_bonds = total_investments * 0.35 * np.random.uniform(0.03, 0.08)
        spread_structured = total_investments * 0.05 * np.random.uniform(0.05, 0.15)
        currency = total_investments * np.random.uniform(0.15, 0.30) * 0.25

        # Concentration (simplified)
        concentration = total_investments * np.random.uniform(0, 0.02)

        # Aggregate with diversification
        undiversified = ir_up + equity_type1 + equity_type2 + property_shock + spread_bonds + spread_structured + currency + concentration
        diversification = undiversified * np.random.uniform(0.20, 0.30)
        market_scr = undiversified - diversification

        row = {
            'syndicate': syn,
            'yoa': YOA,
            'model': 'LSM',
            'module': 'Market Risk',
            'calculation_basis': 'Solvency II Standard Formula',
            # Assets base
            'total_investments': total_investments,
            'government_bonds': total_investments * 0.40,
            'corporate_bonds': total_investments * 0.35,
            'equities_listed': total_investments * 0.08,
            'equities_other': total_investments * 0.02,
            'property': total_investments * 0.02,
            'structured_products': total_investments * 0.05,
            'cash': total_investments * 0.08,
            # Risk calculations
            'interest_rate_risk_up': ir_up,
            'interest_rate_risk_down': ir_down,
            'interest_rate_risk': max(ir_up, ir_down),
            'equity_risk_type1': equity_type1,
            'equity_risk_type2': equity_type2,
            'equity_risk_total': equity_type1 + equity_type2,
            'property_risk': property_shock,
            'spread_risk_bonds': spread_bonds,
            'spread_risk_structured': spread_structured,
            'spread_risk_total': spread_bonds + spread_structured,
            'currency_risk': currency,
            'concentration_risk': concentration,
            # Aggregation
            'market_risk_undiversified': undiversified,
            'diversification_benefit': diversification,
            'market_risk_scr': market_scr
        }
        data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# LSM - COUNTERPARTY DEFAULT RISK
# =============================================================================

def generate_lsm_counterparty_risk():
    """Generate LSM Counterparty Default Risk (SII Standard Formula)"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        # Type 1: Reinsurance, derivatives, cash at bank
        ri_recoverables = np.random.uniform(50, 200) * scale * 1e6
        derivatives_positive = np.random.uniform(5, 30) * scale * 1e6
        cash_at_bank = np.random.uniform(30, 100) * scale * 1e6

        # Type 2: Insurance receivables, other
        insurance_receivables = np.random.uniform(50, 200) * scale * 1e6
        other_receivables = np.random.uniform(10, 50) * scale * 1e6

        # LGD calculations (simplified)
        lgd_type1 = (ri_recoverables * 0.50 + derivatives_positive * 0.90 + cash_at_bank * 0.15) * np.random.uniform(0.10, 0.25)
        type1_scr = lgd_type1 * np.random.uniform(0.8, 1.2)

        type2_exposure = insurance_receivables + other_receivables
        type2_scr = type2_exposure * np.random.uniform(0.08, 0.15)

        # Diversification
        total_undiv = type1_scr + type2_scr
        diversification = total_undiv * np.random.uniform(0.05, 0.15)
        cpd_scr = total_undiv - diversification

        row = {
            'syndicate': syn,
            'yoa': YOA,
            'model': 'LSM',
            'module': 'Counterparty Default Risk',
            'calculation_basis': 'Solvency II Standard Formula',
            # Type 1 exposures
            'ri_recoverables': ri_recoverables,
            'derivatives_positive_value': derivatives_positive,
            'cash_at_bank': cash_at_bank,
            'type1_total_exposure': ri_recoverables + derivatives_positive + cash_at_bank,
            'type1_lgd': lgd_type1,
            'type1_scr': type1_scr,
            # Type 2 exposures
            'insurance_receivables_due': insurance_receivables * 0.3,
            'insurance_receivables_not_due': insurance_receivables * 0.7,
            'other_receivables': other_receivables,
            'type2_total_exposure': type2_exposure,
            'type2_scr': type2_scr,
            # Aggregation
            'cpd_undiversified': total_undiv,
            'diversification_benefit': diversification,
            'cpd_scr': cpd_scr
        }
        data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# LSM - INSURANCE RISK (LLOYD'S BESPOKE)
# =============================================================================

def generate_lsm_insurance_risk():
    """Generate LSM Insurance Risk (Lloyd's Bespoke Method)"""
    data = []

    risk_codes = ['PR', 'CA', 'MA', 'AV', 'EN', 'AC', 'PC', 'SP']

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        total_nep = np.random.uniform(150, 500) * scale * 1e6
        total_reserves = np.random.uniform(200, 600) * scale * 1e6

        for code in risk_codes:
            weight = np.random.uniform(0.05, 0.25)
            nep = total_nep * weight
            reserves = total_reserves * weight

            # Lloyd's bespoke factors (illustrative)
            premium_risk_factor = np.random.uniform(0.08, 0.20)
            reserve_risk_factor = np.random.uniform(0.10, 0.25)

            premium_risk = nep * premium_risk_factor
            reserve_risk = reserves * reserve_risk_factor

            # Correlation between premium and reserve risk
            combined = np.sqrt(premium_risk**2 + reserve_risk**2 + 2 * 0.5 * premium_risk * reserve_risk)

            row = {
                'syndicate': syn,
                'yoa': YOA,
                'model': 'LSM',
                'module': 'Insurance Risk',
                'calculation_basis': 'Lloyd\'s Bespoke',
                'risk_code': code,
                # Volume measures
                'net_earned_premium': nep,
                'net_best_estimate_reserves': reserves,
                # Risk factors
                'premium_risk_factor': premium_risk_factor * 100,
                'reserve_risk_factor': reserve_risk_factor * 100,
                # Risk calculations
                'premium_risk': premium_risk,
                'reserve_risk': reserve_risk,
                'correlation': 0.5,
                'combined_premium_reserve': combined,
                # Loss ratios
                'expected_loss_ratio': np.random.uniform(55, 75),
                'one_year_reserve_risk': reserves * np.random.uniform(0.05, 0.15)
            }
            data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# LSM - OPERATIONAL RISK (LLOYD'S BESPOKE)
# =============================================================================

def generate_lsm_operational_risk():
    """Generate LSM Operational Risk (Lloyd's Bespoke Method)"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        gep = np.random.uniform(150, 500) * scale * 1e6
        tp = np.random.uniform(300, 900) * scale * 1e6

        # Op risk calculation (Lloyd's method)
        op_risk_premium = gep * 0.03  # 3% of gross earned premium
        op_risk_tp = tp * 0.003  # 0.3% of technical provisions
        op_risk = max(op_risk_premium, op_risk_tp)

        # Cap at 30% of BSCR (illustrative)
        bscr = np.random.uniform(80, 250) * scale * 1e6
        op_risk_capped = min(op_risk, bscr * 0.30)

        row = {
            'syndicate': syn,
            'yoa': YOA,
            'model': 'LSM',
            'module': 'Operational Risk',
            'calculation_basis': 'Lloyd\'s Bespoke',
            # Volume measures
            'gross_earned_premium': gep,
            'gross_earned_premium_prior_year': gep * np.random.uniform(0.90, 1.10),
            'technical_provisions': tp,
            # Risk factors
            'premium_factor': 3.0,
            'tp_factor': 0.3,
            # Calculations
            'op_risk_premium_based': op_risk_premium,
            'op_risk_tp_based': op_risk_tp,
            'op_risk_basic': op_risk,
            'bscr_for_cap': bscr,
            'cap_percentage': 30,
            'op_risk_capped': op_risk_capped,
            'op_risk_scr': op_risk_capped,
            # Breakdown by category
            'people_risk': op_risk_capped * np.random.uniform(0.20, 0.30),
            'process_risk': op_risk_capped * np.random.uniform(0.25, 0.35),
            'systems_risk': op_risk_capped * np.random.uniform(0.20, 0.30),
            'external_risk': op_risk_capped * np.random.uniform(0.10, 0.20)
        }
        data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# LSM SUMMARY
# =============================================================================

def generate_lsm_summary():
    """Generate LSM Summary aggregation"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        # Risk modules
        market_risk = np.random.uniform(25, 75) * scale * 1e6
        cpd_risk = np.random.uniform(10, 30) * scale * 1e6
        insurance_risk = np.random.uniform(60, 180) * scale * 1e6
        operational_risk = np.random.uniform(8, 25) * scale * 1e6

        # BSCR aggregation
        bscr_undiv = market_risk + cpd_risk + insurance_risk
        diversification = bscr_undiv * np.random.uniform(0.20, 0.30)
        bscr = bscr_undiv - diversification

        # Total SCR
        scr = bscr + operational_risk

        # Own funds and coverage
        own_funds = scr * np.random.uniform(1.25, 1.75)
        coverage_ratio = (own_funds / scr) * 100

        row = {
            'syndicate': syn,
            'yoa': YOA,
            'model': 'LSM',
            'as_at_date': f'{REPORTING_YEAR}-12-31',
            # Risk modules
            'market_risk_scr': market_risk,
            'counterparty_risk_scr': cpd_risk,
            'insurance_risk_scr': insurance_risk,
            'operational_risk_scr': operational_risk,
            # Aggregation
            'bscr_undiversified': bscr_undiv,
            'diversification_benefit': diversification,
            'diversification_pct': (diversification / bscr_undiv) * 100,
            'bscr': bscr,
            'scr': scr,
            # Own funds
            'own_funds_tier1': own_funds * 0.90,
            'own_funds_tier2': own_funds * 0.08,
            'own_funds_tier3': own_funds * 0.02,
            'total_own_funds': own_funds,
            'eligible_own_funds': own_funds,
            # Coverage
            'scr_coverage_ratio': coverage_ratio,
            'target_coverage_ratio': 140,
            'surplus_over_scr': own_funds - scr,
            'surplus_over_target': own_funds - scr * 1.40,
            # Comparison
            'scr_vs_lcr': np.random.uniform(0.95, 1.05),
            'sbf_premium_volume': np.random.uniform(200, 600) * scale * 1e6,
            'consistency_check': 'Pass'
        }
        data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# GENERATE ALL TABLES
# =============================================================================

# LCM Tables
LCM_313_Cat_Summary = generate_lcm_313()
LCM_314_EP_Curves = generate_lcm_314()
LCM_315_Regional_Exposure = generate_lcm_315()
LCM_316_Sensitivity = generate_lcm_316()

# LSM Tables
LSM_Market_Risk = generate_lsm_market_risk()
LSM_Counterparty_Risk = generate_lsm_counterparty_risk()
LSM_Insurance_Risk = generate_lsm_insurance_risk()
LSM_Operational_Risk = generate_lsm_operational_risk()
LSM_Summary = generate_lsm_summary()

# Print confirmation
print(f"LCM/LSM Capital Models - YOA {YOA}")
print(f"Generated for {len(SYNDICATES)} syndicates")
print(f"LCM Tables: LCM_313, LCM_314, LCM_315, LCM_316")
print(f"LSM Tables: LSM_Market_Risk, LSM_Counterparty_Risk, LSM_Insurance_Risk, LSM_Operational_Risk, LSM_Summary")
print(f"Total: 9 tables covering LCM cat model and LSM standard model")
