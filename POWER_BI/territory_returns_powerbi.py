"""
Lloyd's Territory Returns - Power BI Synthetic Data Generator
=============================================================

Generates synthetic data for territory-specific reporting requirements.

Territories Covered:
- USA: US Situs, NAIC, Surplus Lines, TRIA
- Canada: Canadian Situs (LCTF)
- Japan: FSA Japan requirements
- Singapore: MAS requirements

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

# US States
US_STATES = [
    ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
    ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
    ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
    ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
    ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
    ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
    ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
    ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
    ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
    ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
    ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
    ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'), ('WY', 'Wyoming'), ('DC', 'District of Columbia')
]

# Canadian Provinces
CA_PROVINCES = [
    ('ON', 'Ontario'), ('QC', 'Quebec'), ('BC', 'British Columbia'), ('AB', 'Alberta'),
    ('MB', 'Manitoba'), ('SK', 'Saskatchewan'), ('NS', 'Nova Scotia'), ('NB', 'New Brunswick'),
    ('NL', 'Newfoundland and Labrador'), ('PE', 'Prince Edward Island'),
    ('NT', 'Northwest Territories'), ('YT', 'Yukon'), ('NU', 'Nunavut')
]

# Surplus Lines Tax Rates (approximate)
SURPLUS_LINES_TAX = {
    'CA': 0.0315, 'FL': 0.05, 'NY': 0.036, 'TX': 0.049, 'IL': 0.035,
    'PA': 0.03, 'OH': 0.05, 'GA': 0.04, 'NC': 0.05, 'NJ': 0.03,
    'DEFAULT': 0.03
}

# =============================================================================
# US SITUS REPORTING
# =============================================================================

def generate_us_situs_premium():
    """Generate US Situs premium allocation by state"""
    data = []

    # State weights (approximate based on market size)
    state_weights = {
        'CA': 0.15, 'NY': 0.12, 'TX': 0.10, 'FL': 0.08, 'IL': 0.05,
        'PA': 0.04, 'OH': 0.03, 'GA': 0.03, 'NC': 0.03, 'NJ': 0.03
    }

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        us_gwp = np.random.uniform(50, 200) * scale * 1e6

        for state_code, state_name in US_STATES:
            weight = state_weights.get(state_code, 0.01) * np.random.uniform(0.5, 1.5)
            gwp = us_gwp * weight

            if gwp < 10000:  # Skip very small amounts
                continue

            tax_rate = SURPLUS_LINES_TAX.get(state_code, SURPLUS_LINES_TAX['DEFAULT'])

            row = {
                'syndicate': syn,
                'reporting_year': REPORTING_YEAR,
                'state_code': state_code,
                'state_name': state_name,
                'gross_written_premium_usd': gwp,
                'net_written_premium_usd': gwp * np.random.uniform(0.65, 0.85),
                'gross_earned_premium_usd': gwp * np.random.uniform(0.90, 0.98),
                'gross_claims_incurred_usd': gwp * np.random.uniform(0.45, 0.70),
                'surplus_lines_tax_rate': tax_rate * 100,
                'surplus_lines_tax_due_usd': gwp * tax_rate,
                'stamping_fee_rate': 0.0018,
                'stamping_fee_usd': gwp * 0.0018,
                'total_taxes_fees_usd': gwp * (tax_rate + 0.0018),
                'policy_count': int(gwp / np.random.uniform(50000, 200000)),
                'claim_count': int(gwp / np.random.uniform(200000, 800000)),
                'is_admitted': False,
                'filing_status': 'Filed' if random.random() > 0.1 else 'Pending'
            }
            data.append(row)

    return pd.DataFrame(data)

def generate_us_latf_trust_fund():
    """Generate Lloyd's American Trust Fund (LATF) allocations"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        us_liabilities = np.random.uniform(100, 400) * scale * 1e6

        row = {
            'syndicate': syn,
            'reporting_year': REPORTING_YEAR,
            'as_at_date': f'{REPORTING_YEAR}-12-31',
            'trust_fund': 'LATF',
            'territory': 'USA',
            'gross_liabilities_usd': us_liabilities,
            'ri_recoverables_usd': us_liabilities * np.random.uniform(0.15, 0.30),
            'net_liabilities_usd': us_liabilities * np.random.uniform(0.70, 0.85),
            'required_deposit_usd': us_liabilities * np.random.uniform(0.70, 0.85) * 1.0,  # 100% of net
            'actual_deposit_usd': us_liabilities * np.random.uniform(0.75, 0.95),
            'surplus_deficit_usd': us_liabilities * np.random.uniform(-0.05, 0.15),
            'deposit_coverage_pct': np.random.uniform(95, 115),
            'asset_allocation_bonds_pct': np.random.uniform(70, 90),
            'asset_allocation_cash_pct': np.random.uniform(10, 30),
            'yield_on_deposits': np.random.uniform(2, 5),
            'custodian': random.choice(['BNY Mellon', 'State Street', 'Citibank'])
        }
        data.append(row)

    return pd.DataFrame(data)

def generate_us_naic():
    """Generate NAIC Annual Statement data"""
    data = []

    naic_lines = [
        ('1', 'Fire'), ('2', 'Allied Lines'), ('3', 'Farmowners Multi-Peril'),
        ('4', 'Homeowners Multi-Peril'), ('5', 'Commercial Multi-Peril'),
        ('6', 'Mortgage Guaranty'), ('8', 'Ocean Marine'), ('9', 'Inland Marine'),
        ('10', 'Financial Guaranty'), ('11', 'Medical Malpractice'),
        ('12', 'Earthquake'), ('13', 'Group A&H'), ('14', 'Credit A&H'),
        ('15', 'Other A&H'), ('16', 'Workers Compensation'), ('17', 'Other Liability'),
        ('18', 'Products Liability'), ('19', 'Auto Liability'), ('20', 'Auto Physical Damage'),
        ('21', 'Aircraft'), ('22', 'Fidelity'), ('23', 'Surety'), ('24', 'Burglary and Theft'),
        ('26', 'Boiler and Machinery'), ('27', 'Credit'), ('28', 'International'),
        ('29', 'Warranty'), ('30', 'Reinsurance - Nonproportional Assumed')
    ]

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        for line_code, line_name in naic_lines[:15]:  # Top 15 lines
            dwp = np.random.uniform(5, 50) * scale * 1e6

            if dwp < 100000:
                continue

            row = {
                'syndicate': syn,
                'reporting_year': REPORTING_YEAR,
                'naic_line_code': line_code,
                'naic_line_name': line_name,
                'direct_premiums_written_usd': dwp,
                'direct_premiums_earned_usd': dwp * np.random.uniform(0.90, 0.98),
                'ri_ceded_usd': dwp * np.random.uniform(0.15, 0.35),
                'net_premiums_written_usd': dwp * np.random.uniform(0.65, 0.85),
                'net_premiums_earned_usd': dwp * np.random.uniform(0.60, 0.80),
                'losses_incurred_usd': dwp * np.random.uniform(0.45, 0.70),
                'loss_adjustment_expenses_usd': dwp * np.random.uniform(0.05, 0.15),
                'underwriting_expenses_usd': dwp * np.random.uniform(0.25, 0.35),
                'net_underwriting_gain_usd': dwp * np.random.uniform(-0.10, 0.15),
                'loss_ratio': np.random.uniform(50, 75),
                'expense_ratio': np.random.uniform(28, 38),
                'combined_ratio': np.random.uniform(88, 105)
            }
            data.append(row)

    return pd.DataFrame(data)

def generate_us_tria():
    """Generate TRIA (Terrorism Risk Insurance Act) reporting"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        total_premium = np.random.uniform(100, 400) * scale * 1e6

        # TRIA applies to commercial P&C lines
        tria_premium = total_premium * np.random.uniform(0.60, 0.80)
        tria_exposure = tria_premium * np.random.uniform(5, 15)  # Implied SI multiple

        row = {
            'syndicate': syn,
            'reporting_year': REPORTING_YEAR,
            'program_year': REPORTING_YEAR,
            'direct_earned_premium_usd': tria_premium,
            'terrorism_premium_usd': tria_premium * np.random.uniform(0.01, 0.05),
            'insured_loss_exposure_usd': tria_exposure,
            'insurer_deductible_pct': 20,  # Current TRIA deductible
            'insurer_deductible_usd': tria_premium * 0.20,
            'federal_share_pct': 80,  # Current federal backstop
            'insurer_copay_pct': 20,
            'program_trigger_usd': 200000000,  # $200M certification threshold
            'program_cap_usd': 100000000000,  # $100B cap
            'make_available_compliant': True,
            'terrorism_exclusion_used': False,
            'nbcr_coverage': random.choice([True, False]),
            'cyber_terrorism_coverage': random.choice([True, False])
        }
        data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# CANADIAN REPORTING
# =============================================================================

def generate_canada_situs():
    """Generate Canadian Situs premium allocation"""
    data = []

    province_weights = {
        'ON': 0.40, 'QC': 0.20, 'BC': 0.15, 'AB': 0.15, 'MB': 0.03,
        'SK': 0.02, 'NS': 0.02, 'NB': 0.01
    }

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        ca_gwp = np.random.uniform(20, 80) * scale * 1e6

        for prov_code, prov_name in CA_PROVINCES:
            weight = province_weights.get(prov_code, 0.005) * np.random.uniform(0.7, 1.3)
            gwp = ca_gwp * weight

            if gwp < 10000:
                continue

            row = {
                'syndicate': syn,
                'reporting_year': REPORTING_YEAR,
                'province_code': prov_code,
                'province_name': prov_name,
                'gross_written_premium_cad': gwp,
                'net_written_premium_cad': gwp * np.random.uniform(0.65, 0.85),
                'gross_claims_incurred_cad': gwp * np.random.uniform(0.45, 0.70),
                'provincial_premium_tax_rate': np.random.uniform(2, 4),
                'premium_tax_due_cad': gwp * np.random.uniform(0.02, 0.04),
                'fire_insurance_tax_cad': gwp * 0.01 if random.random() > 0.5 else 0,
                'policy_count': int(gwp / np.random.uniform(30000, 150000)),
                'unlicensed_insurance': True,
                'broker_licensed': True
            }
            data.append(row)

    return pd.DataFrame(data)

def generate_canada_lctf():
    """Generate Lloyd's Canadian Trust Fund (LCTF) data"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        ca_liabilities = np.random.uniform(30, 120) * scale * 1e6

        row = {
            'syndicate': syn,
            'reporting_year': REPORTING_YEAR,
            'as_at_date': f'{REPORTING_YEAR}-12-31',
            'trust_fund': 'LCTF',
            'territory': 'Canada',
            'gross_liabilities_cad': ca_liabilities,
            'ri_recoverables_cad': ca_liabilities * np.random.uniform(0.15, 0.30),
            'net_liabilities_cad': ca_liabilities * np.random.uniform(0.70, 0.85),
            'required_deposit_cad': ca_liabilities * np.random.uniform(0.70, 0.85) * 1.15,  # 115% margin
            'actual_deposit_cad': ca_liabilities * np.random.uniform(0.80, 1.00),
            'margin_fund_contribution_cad': ca_liabilities * np.random.uniform(0.02, 0.05),
            'deposit_coverage_pct': np.random.uniform(100, 120),
            'osfi_compliant': True,
            'custodian': random.choice(['RBC', 'TD', 'BMO', 'CIBC'])
        }
        data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# JAPAN REPORTING
# =============================================================================

def generate_japan_fsa():
    """Generate Japan FSA reporting data"""
    data = []

    japan_lines = [
        'Fire', 'Marine', 'Personal Accident', 'Auto', 'Aviation',
        'Liability', 'Engineering', 'Credit', 'Nuclear', 'Reinsurance'
    ]

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        for line in japan_lines[:6]:
            gwp_jpy = np.random.uniform(500, 3000) * scale * 1e6

            row = {
                'syndicate': syn,
                'reporting_year': REPORTING_YEAR,
                'business_line': line,
                'gross_written_premium_jpy': gwp_jpy,
                'gross_written_premium_gbp': gwp_jpy / 185,  # Approx JPY/GBP
                'net_written_premium_jpy': gwp_jpy * np.random.uniform(0.65, 0.85),
                'claims_paid_jpy': gwp_jpy * np.random.uniform(0.30, 0.50),
                'claims_outstanding_jpy': gwp_jpy * np.random.uniform(0.15, 0.30),
                'policy_count': int(gwp_jpy / np.random.uniform(10000000, 50000000)),
                'market_model': 'Open Market',  # Japan Open Market Model
                'service_company': f'Lloyd\'s Japan SC {random.randint(1,5)}',
                'fsa_registration': 'Registered',
                'consumption_tax_rate': 10,
                'consumption_tax_jpy': gwp_jpy * 0.10 if line not in ['Reinsurance'] else 0
            }
            data.append(row)

    return pd.DataFrame(data)

def generate_japan_trust_fund():
    """Generate Japan trust fund data"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        jp_liabilities = np.random.uniform(1000, 5000) * scale * 1e6

        row = {
            'syndicate': syn,
            'reporting_year': REPORTING_YEAR,
            'as_at_date': f'{REPORTING_YEAR}-12-31',
            'territory': 'Japan',
            'gross_liabilities_jpy': jp_liabilities,
            'net_liabilities_jpy': jp_liabilities * np.random.uniform(0.70, 0.85),
            'required_deposit_jpy': jp_liabilities * np.random.uniform(0.70, 0.85) * 1.0,
            'actual_deposit_jpy': jp_liabilities * np.random.uniform(0.75, 0.95),
            'deposit_coverage_pct': np.random.uniform(95, 115),
            'deposit_currency': 'JPY',
            'custodian': random.choice(['MUFG', 'SMBC', 'Mizuho'])
        }
        data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# SINGAPORE REPORTING
# =============================================================================

def generate_singapore_mas():
    """Generate Singapore MAS reporting data"""
    data = []

    sg_lines = ['Property', 'Marine', 'Aviation', 'Liability', 'Engineering', 'Offshore Energy']

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        for line in sg_lines:
            gwp_sgd = np.random.uniform(5, 30) * scale * 1e6

            row = {
                'syndicate': syn,
                'reporting_year': REPORTING_YEAR,
                'business_line': line,
                'policy_type': random.choice(['Singapore Policies', 'Offshore Policies']),
                'gross_written_premium_sgd': gwp_sgd,
                'gross_written_premium_gbp': gwp_sgd / 1.70,  # Approx SGD/GBP
                'net_written_premium_sgd': gwp_sgd * np.random.uniform(0.65, 0.85),
                'claims_paid_sgd': gwp_sgd * np.random.uniform(0.30, 0.50),
                'claims_outstanding_sgd': gwp_sgd * np.random.uniform(0.15, 0.30),
                'policy_count': int(gwp_sgd / np.random.uniform(100000, 500000)),
                'service_company': 'Lloyd\'s Asia Pte Ltd',
                'mas_registration': 'Registered',
                'gst_rate': 9,  # Singapore GST
                'gst_sgd': gwp_sgd * 0.09
            }
            data.append(row)

    return pd.DataFrame(data)

def generate_singapore_trust_fund():
    """Generate Lloyd's Asia trust fund data"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        for policy_type in ['Singapore Policies', 'Offshore Policies']:
            liabilities = np.random.uniform(10, 50) * scale * 1e6

            row = {
                'syndicate': syn,
                'reporting_year': REPORTING_YEAR,
                'as_at_date': f'{REPORTING_YEAR}-12-31',
                'trust_fund': f'Lloyd\'s Asia ({policy_type})',
                'territory': 'Singapore',
                'policy_type': policy_type,
                'gross_liabilities_sgd': liabilities,
                'net_liabilities_sgd': liabilities * np.random.uniform(0.70, 0.85),
                'required_deposit_sgd': liabilities * np.random.uniform(0.70, 0.85) * 1.0,
                'actual_deposit_sgd': liabilities * np.random.uniform(0.75, 0.95),
                'deposit_coverage_pct': np.random.uniform(95, 115),
                'custodian': random.choice(['DBS', 'OCBC', 'UOB', 'Standard Chartered'])
            }
            data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# TERRITORY SUMMARY
# =============================================================================

def generate_territory_summary():
    """Generate Territory summary dashboard"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        territories = [
            ('USA', 'USD', np.random.uniform(50, 200) * scale * 1e6, 'LATF'),
            ('Canada', 'CAD', np.random.uniform(20, 80) * scale * 1e6, 'LCTF'),
            ('Japan', 'JPY', np.random.uniform(500, 3000) * scale * 1e6, 'Japan Deposit'),
            ('Singapore', 'SGD', np.random.uniform(10, 50) * scale * 1e6, 'Lloyd\'s Asia')
        ]

        for territory, currency, gwp, trust_fund in territories:
            row = {
                'syndicate': syn,
                'reporting_year': REPORTING_YEAR,
                'territory': territory,
                'currency': currency,
                'gross_written_premium': gwp,
                'gross_written_premium_gbp': gwp / {'USD': 1.27, 'CAD': 1.72, 'JPY': 185, 'SGD': 1.70}[currency],
                'net_written_premium': gwp * np.random.uniform(0.65, 0.85),
                'gross_liabilities': gwp * np.random.uniform(1.5, 2.5),
                'trust_fund': trust_fund,
                'trust_fund_balance': gwp * np.random.uniform(1.5, 2.5) * np.random.uniform(0.75, 0.95),
                'deposit_coverage_pct': np.random.uniform(95, 115),
                'regulatory_status': 'Compliant',
                'filing_status': 'Current'
            }
            data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# GENERATE ALL TABLES
# =============================================================================

# USA
US_Situs_Premium = generate_us_situs_premium()
US_LATF_Trust_Fund = generate_us_latf_trust_fund()
US_NAIC = generate_us_naic()
US_TRIA = generate_us_tria()

# Canada
Canada_Situs = generate_canada_situs()
Canada_LCTF = generate_canada_lctf()

# Japan
Japan_FSA = generate_japan_fsa()
Japan_Trust_Fund = generate_japan_trust_fund()

# Singapore
Singapore_MAS = generate_singapore_mas()
Singapore_Trust_Fund = generate_singapore_trust_fund()

# Summary
Territory_Summary = generate_territory_summary()

# Print confirmation
print(f"Territory Returns - {REPORTING_YEAR}")
print(f"Generated for {len(SYNDICATES)} syndicates")
print(f"USA Tables: US_Situs_Premium, US_LATF, US_NAIC, US_TRIA")
print(f"Canada Tables: Canada_Situs, Canada_LCTF")
print(f"Japan Tables: Japan_FSA, Japan_Trust_Fund")
print(f"Singapore Tables: Singapore_MAS, Singapore_Trust_Fund")
print(f"Summary: Territory_Summary")
print(f"Total: 11 tables covering 4 territories")
