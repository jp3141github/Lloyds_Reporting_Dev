"""
Solvency II ASB Returns Generator for Power BI
==============================================
Generates Solvency II Annual Solvency Balance Sheet (ASB) returns data.
Compatible with Power BI as a Python data source.

Tables Generated:
- ASB_245_246_247_Claims: Claims Information (Gross/Net/Reinsurance)
- ASB_248_InflationRates: Inflation rates by LOB
- Claims_Summary: Aggregated claims summary
- Development_Analysis: Development year analysis
- Metadata: Generation metadata
- LinesOfBusiness: Reference table of LOB codes
- ASB245_Claims_Gross: Gross claims (detailed)
- ASB246_Claims_Reinsurance: Reinsurance claims
- ASB247_Claims_Net: Net claims
- ASB_Development_Factors: Development factors analysis

Usage in Power BI:
1. Get Data > More > Python script
2. Copy and paste this script
3. Select the tables you need from the list
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
SYNDICATE_NUMBER = '1234'
SYNDICATE_NAME = 'Example Marine & Energy Syndicate'
START_YEAR = 2015
END_YEAR = 2024
CLAIMS_RECORDS = 500
INFLATION_RECORDS = 200

# Lines of Business
LINES_OF_BUSINESS = {
    'LOB01': 'Medical expense insurance',
    'LOB02': 'Income protection insurance',
    'LOB03': 'Workers compensation insurance',
    'LOB04': 'Motor vehicle liability insurance',
    'LOB05': 'Other motor insurance',
    'LOB06': 'Marine, aviation and transport insurance',
    'LOB07': 'Fire and other damage to property insurance',
    'LOB08': 'General liability insurance',
    'LOB09': 'Credit and suretyship insurance',
    'LOB10': 'Legal expenses insurance',
    'LOB11': 'Assistance',
    'LOB12': 'Miscellaneous financial loss'
}

CURRENCIES = ['GBP', 'USD', 'EUR']


def generate_asb_245_246_247_data(num_records=500):
    """Generate ASB 245/246/247 claims data."""
    data = []

    for _ in range(num_records):
        currency = random.choice(CURRENCIES)
        lob_code = random.choice(list(LINES_OF_BUSINESS.keys()))
        underwriting_year = random.randint(START_YEAR, END_YEAR)
        development_year = random.randint(0, 10)

        base_claim = np.random.lognormal(mean=10, sigma=2)
        development_factor = max(1 - (development_year * 0.08), 0.3)

        gross_claim_paid = base_claim * development_factor * np.random.uniform(0.8, 1.2)
        reinsurance_recoveries = gross_claim_paid * np.random.uniform(0.1, 0.4)

        gross_be_provisions = gross_claim_paid * np.random.uniform(1.1, 1.5)
        discounting_gross = gross_be_provisions * np.random.uniform(0.02, 0.05)

        be_provisions_reins = reinsurance_recoveries * np.random.uniform(1.1, 1.5)
        discounting_reins = be_provisions_reins * np.random.uniform(0.02, 0.05)

        gross_rbns = gross_claim_paid * np.random.uniform(0.6, 0.9)
        reinsurance_rbns = reinsurance_recoveries * np.random.uniform(0.6, 0.9)

        discounting_rbns = gross_rbns * np.random.uniform(0.015, 0.04)
        discounting_reins_rbns = reinsurance_rbns * np.random.uniform(0.015, 0.04)

        record = {
            'Currency': currency,
            'LineOfBusiness': lob_code,
            'LineOfBusinessName': LINES_OF_BUSINESS[lob_code],
            'UnderwritingYear': underwriting_year,
            'DevelopmentYear': development_year,
            'GrossClaimPaid': round(gross_claim_paid, 2),
            'ReinsuranceRecoveries': round(reinsurance_recoveries, 2),
            'NetClaimPaid': round(gross_claim_paid - reinsurance_recoveries, 2),
            'GrossUndiscountedBEClaimsProvisions': round(gross_be_provisions, 2),
            'DiscountingGrossBEClaimsProvisions': round(discounting_gross, 2),
            'UndiscountedBEClaimsProvisionsReinsRecoverable': round(be_provisions_reins, 2),
            'DiscountingBEClaimsProvisionsReinsRecoverable': round(discounting_reins, 2),
            'GrossRBNS': round(gross_rbns, 2),
            'ReinsuranceRBNS': round(reinsurance_rbns, 2),
            'NetRBNS': round(gross_rbns - reinsurance_rbns, 2),
            'DiscountingRBNS': round(discounting_rbns, 2),
            'DiscountingReinsuranceRBNS': round(discounting_reins_rbns, 2)
        }
        data.append(record)

    df = pd.DataFrame(data)
    df = df.sort_values(['UnderwritingYear', 'LineOfBusiness', 'DevelopmentYear'])
    return df.reset_index(drop=True)


def generate_asb_248_data(num_records=200):
    """Generate ASB 248 inflation rates data."""
    data = []

    for _ in range(num_records):
        currency = random.choice(CURRENCIES)
        lob_code = random.choice(list(LINES_OF_BUSINESS.keys()))
        underwriting_year = random.randint(START_YEAR, END_YEAR)

        historic_total = np.random.uniform(1.5, 4.5)
        historic_external = historic_total * np.random.uniform(0.5, 0.7)
        historic_endogenous = historic_total - historic_external

        expected_total = historic_total * np.random.uniform(0.9, 1.1)
        expected_external = expected_total * np.random.uniform(0.5, 0.7)
        expected_endogenous = expected_total - expected_external

        record = {
            'Currency': currency,
            'LineOfBusiness': lob_code,
            'LineOfBusinessName': LINES_OF_BUSINESS[lob_code],
            'UnderwritingYear': underwriting_year,
            'HistoricInflationRateTotal': round(historic_total, 2),
            'HistoricInflationRateExternal': round(historic_external, 2),
            'HistoricInflationRateEndogenous': round(historic_endogenous, 2),
            'ExpectedInflationRateTotal': round(expected_total, 2),
            'ExpectedInflationRateExternal': round(expected_external, 2),
            'ExpectedInflationRateEndogenous': round(expected_endogenous, 2)
        }
        data.append(record)

    df = pd.DataFrame(data)
    df = df.sort_values(['UnderwritingYear', 'LineOfBusiness'])
    return df.reset_index(drop=True)


def generate_asb245_claims_gross(claims_df):
    """Generate ASB 245 - Claims Information Gross"""
    return claims_df[[
        'Currency', 'LineOfBusiness', 'LineOfBusinessName',
        'UnderwritingYear', 'DevelopmentYear',
        'GrossClaimPaid', 'GrossUndiscountedBEClaimsProvisions',
        'DiscountingGrossBEClaimsProvisions', 'GrossRBNS', 'DiscountingRBNS'
    ]].copy()


def generate_asb246_claims_reinsurance(claims_df):
    """Generate ASB 246 - Claims Information Reinsurance Share"""
    return claims_df[[
        'Currency', 'LineOfBusiness', 'LineOfBusinessName',
        'UnderwritingYear', 'DevelopmentYear',
        'ReinsuranceRecoveries', 'UndiscountedBEClaimsProvisionsReinsRecoverable',
        'DiscountingBEClaimsProvisionsReinsRecoverable', 'ReinsuranceRBNS',
        'DiscountingReinsuranceRBNS'
    ]].copy()


def generate_asb247_claims_net(claims_df):
    """Generate ASB 247 - Claims Information Net"""
    df = claims_df[[
        'Currency', 'LineOfBusiness', 'LineOfBusinessName',
        'UnderwritingYear', 'DevelopmentYear', 'NetClaimPaid', 'NetRBNS'
    ]].copy()

    df['NetBEClaimsProvisions'] = (
        claims_df['GrossUndiscountedBEClaimsProvisions'] -
        claims_df['UndiscountedBEClaimsProvisionsReinsRecoverable']
    ).round(2)

    return df


def generate_development_factors(claims_df):
    """Calculate claims development factors"""
    df = claims_df.sort_values(['LineOfBusiness', 'UnderwritingYear', 'DevelopmentYear']).copy()

    # Group by LOB and calculate age-to-age factors
    dev_factors = df.groupby(['LineOfBusiness', 'DevelopmentYear']).agg({
        'GrossClaimPaid': ['mean', 'sum', 'count'],
        'ReinsuranceRecoveries': ['mean', 'sum']
    }).reset_index()

    dev_factors.columns = [
        'LineOfBusiness', 'DevelopmentYear',
        'AvgGrossClaimPaid', 'TotalGrossClaimPaid', 'ClaimCount',
        'AvgReinsuranceRecoveries', 'TotalReinsuranceRecoveries'
    ]

    # Calculate development factors
    dev_factors['NetRetention'] = (
        (dev_factors['TotalGrossClaimPaid'] - dev_factors['TotalReinsuranceRecoveries']) /
        dev_factors['TotalGrossClaimPaid']
    ).round(4)

    return dev_factors


# =============================================================================
# GENERATE ALL TABLES FOR POWER BI
# =============================================================================
print("Generating Solvency II ASB Data for Power BI...")
print("=" * 60)

# Generate base claims data
ASB_245_246_247_Claims = generate_asb_245_246_247_data(CLAIMS_RECORDS)

# Generate inflation rates
ASB_248_InflationRates = generate_asb_248_data(INFLATION_RECORDS)

# Metadata table
Metadata = pd.DataFrame([{
    'SyndicateNumber': SYNDICATE_NUMBER,
    'SyndicateName': SYNDICATE_NAME,
    'StartYear': START_YEAR,
    'EndYear': END_YEAR,
    'GenerationDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'ClaimsRecords': len(ASB_245_246_247_Claims),
    'InflationRecords': len(ASB_248_InflationRates)
}])

# Lines of Business reference table
LinesOfBusiness = pd.DataFrame([
    {'LineOfBusiness': k, 'LineOfBusinessName': v}
    for k, v in LINES_OF_BUSINESS.items()
])

# Claims Summary
Claims_Summary = ASB_245_246_247_Claims.groupby(
    ['UnderwritingYear', 'LineOfBusiness', 'Currency']
).agg({
    'GrossClaimPaid': 'sum',
    'ReinsuranceRecoveries': 'sum',
    'NetClaimPaid': 'sum',
    'GrossRBNS': 'sum',
    'NetRBNS': 'sum'
}).reset_index()

# Development Analysis
Development_Analysis = ASB_245_246_247_Claims.groupby(
    ['DevelopmentYear', 'LineOfBusiness']
).agg({
    'GrossClaimPaid': ['mean', 'sum', 'count'],
    'ReinsuranceRecoveries': ['mean', 'sum']
}).reset_index()

Development_Analysis.columns = [
    'DevelopmentYear', 'LineOfBusiness',
    'AvgGrossClaimPaid', 'TotalGrossClaimPaid', 'ClaimCount',
    'AvgReinsuranceRecoveries', 'TotalReinsuranceRecoveries'
]

# Detailed ASB tables
ASB245_Claims_Gross = generate_asb245_claims_gross(ASB_245_246_247_Claims)
ASB246_Claims_Reinsurance = generate_asb246_claims_reinsurance(ASB_245_246_247_Claims)
ASB247_Claims_Net = generate_asb247_claims_net(ASB_245_246_247_Claims)
ASB_Development_Factors = generate_development_factors(ASB_245_246_247_Claims)

print(f"ASB_245_246_247_Claims: {len(ASB_245_246_247_Claims)} records")
print(f"ASB_248_InflationRates: {len(ASB_248_InflationRates)} records")
print(f"Claims_Summary: {len(Claims_Summary)} records")
print(f"Development_Analysis: {len(Development_Analysis)} records")
print(f"Metadata: {len(Metadata)} records")
print(f"LinesOfBusiness: {len(LinesOfBusiness)} records")
print(f"ASB245_Claims_Gross: {len(ASB245_Claims_Gross)} records")
print(f"ASB246_Claims_Reinsurance: {len(ASB246_Claims_Reinsurance)} records")
print(f"ASB247_Claims_Net: {len(ASB247_Claims_Net)} records")
print(f"ASB_Development_Factors: {len(ASB_Development_Factors)} records")
print("=" * 60)
print("Solvency II ASB data generated successfully!")
