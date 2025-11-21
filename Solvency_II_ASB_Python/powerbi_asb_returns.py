"""
Power BI Script for Solvency II ASB Returns
This script can be used directly in Power BI as a Python data source.

Instructions for Power BI:
1. Open Power BI Desktop
2. Get Data > More > Other > Python script
3. Copy and paste this script
4. Adjust parameters as needed
5. Select the tables you want to load
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# Add the current directory to path to import our generator
# Adjust this path if running from different location
# sys.path.append(r'C:\path\to\Solvency_II_ASB_Python')

# Import our synthetic data generator
# If running standalone, uncomment the import below
# from synthetic_data_generator import LloydsDataGenerator

# Inline generator for Power BI (embedded version)
class LloydsDataGenerator:
    """Generates synthetic Lloyd's insurance data for Solvency II ASB returns."""

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

    def __init__(self, syndicate_number='1234', syndicate_name='Example Syndicate',
                 start_year=2015, end_year=2024, random_seed=42):
        self.syndicate_number = syndicate_number
        self.syndicate_name = syndicate_name
        self.start_year = start_year
        self.end_year = end_year
        np.random.seed(random_seed)

    def generate_asb_245_246_247_data(self, num_records=500):
        """Generate ASB 245/246/247 claims data."""
        import random
        random.seed(42)

        data = []
        for _ in range(num_records):
            currency = random.choice(self.CURRENCIES)
            lob_code = random.choice(list(self.LINES_OF_BUSINESS.keys()))
            underwriting_year = random.randint(self.start_year, self.end_year)
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
                'LineOfBusinessName': self.LINES_OF_BUSINESS[lob_code],
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

    def generate_asb_248_data(self, num_records=200):
        """Generate ASB 248 inflation rates data."""
        import random
        random.seed(42)

        data = []
        for _ in range(num_records):
            currency = random.choice(self.CURRENCIES)
            lob_code = random.choice(list(self.LINES_OF_BUSINESS.keys()))
            underwriting_year = random.randint(self.start_year, self.end_year)

            historic_total = np.random.uniform(1.5, 4.5)
            historic_external = historic_total * np.random.uniform(0.5, 0.7)
            historic_endogenous = historic_total - historic_external

            expected_total = historic_total * np.random.uniform(0.9, 1.1)
            expected_external = expected_total * np.random.uniform(0.5, 0.7)
            expected_endogenous = expected_total - expected_external

            record = {
                'Currency': currency,
                'LineOfBusiness': lob_code,
                'LineOfBusinessName': self.LINES_OF_BUSINESS[lob_code],
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


# ============================================================================
# CONFIGURATION - Adjust these parameters as needed
# ============================================================================

SYNDICATE_NUMBER = '1234'
SYNDICATE_NAME = 'Example Marine & Energy Syndicate'
START_YEAR = 2015
END_YEAR = 2024
RANDOM_SEED = 42

# Number of records to generate
CLAIMS_RECORDS = 500
INFLATION_RECORDS = 200

# ============================================================================
# DATA GENERATION - This section runs when script is executed
# ============================================================================

# Create generator instance
generator = LloydsDataGenerator(
    syndicate_number=SYNDICATE_NUMBER,
    syndicate_name=SYNDICATE_NAME,
    start_year=START_YEAR,
    end_year=END_YEAR,
    random_seed=RANDOM_SEED
)

# Generate the data tables for Power BI
# These will appear as available tables in Power BI

# ASB 245/246/247: Non-Life Insurance Claims Information
ASB_245_246_247_Claims = generator.generate_asb_245_246_247_data(CLAIMS_RECORDS)

# ASB 248: Inflation Rates
ASB_248_InflationRates = generator.generate_asb_248_data(INFLATION_RECORDS)

# Metadata table for reference
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
    for k, v in generator.LINES_OF_BUSINESS.items()
])

# Summary statistics for Power BI dashboards
Claims_Summary = ASB_245_246_247_Claims.groupby(
    ['UnderwritingYear', 'LineOfBusiness', 'Currency']
).agg({
    'GrossClaimPaid': 'sum',
    'ReinsuranceRecoveries': 'sum',
    'NetClaimPaid': 'sum',
    'GrossRBNS': 'sum',
    'NetRBNS': 'sum'
}).reset_index()

# Development year analysis
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

# ============================================================================
# OUTPUT - Available tables for Power BI
# ============================================================================
# The following dataframes will be available in Power BI:
# 1. ASB_245_246_247_Claims - Main claims data
# 2. ASB_248_InflationRates - Inflation rates data
# 3. Metadata - Generation metadata
# 4. LinesOfBusiness - Reference table
# 5. Claims_Summary - Aggregated summary
# 6. Development_Analysis - Development year analysis

print("Data generation complete!")
print(f"ASB 245/246/247 Claims: {len(ASB_245_246_247_Claims)} records")
print(f"ASB 248 Inflation Rates: {len(ASB_248_InflationRates)} records")
