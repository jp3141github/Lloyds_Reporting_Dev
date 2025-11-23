"""
FSCS Data Generator for Power BI
================================
Generates Financial Services Compensation Scheme (FSCS) data for Lloyd's syndicates.
Compatible with Power BI as a Python data source.

Tables Generated:
- fscs_summary: Summary FSCS data by syndicate
- fscs_detail: Detailed transaction-level FSCS data

Usage in Power BI:
1. Get Data > More > Python script
2. Copy and paste this script
3. Select the tables you need from the list
"""

import pandas as pd
import numpy as np
from datetime import datetime, date
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_SYNDICATES = 10
REPORTING_YEAR = 2024


class FSCSDataGenerator:
    """Generates synthetic Lloyd's syndicate data for FSCS reporting."""

    def __init__(self, num_syndicates=10, reporting_year=2024):
        self.num_syndicates = num_syndicates
        self.reporting_year = reporting_year

    def generate_syndicate_numbers(self):
        """Generate realistic Lloyd's syndicate numbers."""
        base_numbers = random.sample(range(2000, 6000), self.num_syndicates)
        return sorted(base_numbers)

    def generate_gross_written_premium(self, business_type='general'):
        """Generate gross written premium values."""
        if business_type == 'general':
            min_value = 10_000_000
            max_value = 500_000_000
            mean = 150_000_000
        else:
            min_value = 1_000_000
            max_value = 100_000_000
            mean = 30_000_000

        values = np.random.lognormal(mean=np.log(mean), sigma=0.5, size=self.num_syndicates)
        values = np.clip(values, min_value, max_value)
        zero_mask = np.random.random(self.num_syndicates) < 0.2
        values[zero_mask] = 0

        return np.round(values, 2)

    def generate_best_estimate_liabilities(self, gwp_values, business_type='general'):
        """Generate gross best estimate liabilities."""
        if business_type == 'general':
            multiplier = np.random.uniform(1.5, 3.0, self.num_syndicates)
        else:
            multiplier = np.random.uniform(3.0, 8.0, self.num_syndicates)

        values = gwp_values * multiplier
        variation = np.random.uniform(0.8, 1.2, self.num_syndicates)
        values = values * variation

        zero_mask = gwp_values == 0
        values[zero_mask] = np.random.uniform(0, 5_000_000, np.sum(zero_mask))

        return np.round(values, 2)

    def generate_full_dataset(self):
        """Generate complete FSCS dataset for all syndicates."""
        syndicates = self.generate_syndicate_numbers()

        gwp_general = self.generate_gross_written_premium('general')
        gwp_life = self.generate_gross_written_premium('life')

        bel_general = self.generate_best_estimate_liabilities(gwp_general, 'general')
        bel_life = self.generate_best_estimate_liabilities(gwp_life, 'life')

        df = pd.DataFrame({
            'syndicate_number': syndicates,
            'reporting_year': self.reporting_year,
            'reporting_date': date(self.reporting_year, 12, 31),
            'gwp_general_business': gwp_general,
            'gwp_life_business': gwp_life,
            'bel_general_business': bel_general,
            'bel_life_business': bel_life,
            'gwp_total': gwp_general + gwp_life,
            'bel_total': bel_general + bel_life
        })

        df['managing_agent'] = df['syndicate_number'].apply(
            lambda x: f"Managing Agent {random.randint(1, 50):03d}"
        )

        df['general_business_pct'] = np.where(
            df['gwp_total'] > 0,
            (df['gwp_general_business'] / df['gwp_total'] * 100).round(2),
            0
        )

        return df

    def generate_fscs_output_format(self):
        """Generate data in the exact format required by FSCS template."""
        df = self.generate_full_dataset()

        output = pd.DataFrame({
            'Syndicate Number': df['syndicate_number'],
            'Reporting Year': df['reporting_year'],
            'Reporting Date': df['reporting_date'],
            'GWP General Business (GBP)': df['gwp_general_business'],
            'GWP Life Business (GBP)': df['gwp_life_business'],
            'BEL General Business (GBP)': df['bel_general_business'],
            'BEL Life Business (GBP)': df['bel_life_business'],
            'GWP Total (GBP)': df['gwp_total'],
            'BEL Total (GBP)': df['bel_total'],
            'Managing Agent': df['managing_agent'],
            'General Business Pct': df['general_business_pct'],
            'Notes': 'Protected contracts with eligible claimants only'
        })

        return output

    def generate_detail_dataset(self):
        """Generate detailed transactional data."""
        base_df = self.generate_full_dataset()

        detail_records = []

        for _, row in base_df.iterrows():
            syndicate = row['syndicate_number']
            num_contracts = random.randint(50, 200)

            for i in range(num_contracts):
                is_general = random.random() > 0.3

                if is_general:
                    business_type = 'General'
                    total_gwp = row['gwp_general_business']
                    total_bel = row['bel_general_business']
                    classes = ['Property', 'Casualty', 'Marine', 'Aviation', 'Energy']
                else:
                    business_type = 'Life'
                    total_gwp = row['gwp_life_business']
                    total_bel = row['bel_life_business']
                    classes = ['Term Life', 'Whole Life', 'Annuities', 'Critical Illness']

                if total_gwp > 0:
                    contract_gwp = (total_gwp / num_contracts) * random.uniform(0.5, 1.5)
                    contract_bel = (total_bel / num_contracts) * random.uniform(0.5, 1.5)
                else:
                    contract_gwp = 0
                    contract_bel = 0

                detail_records.append({
                    'syndicate_number': syndicate,
                    'contract_id': f"CON-{syndicate}-{i+1:05d}",
                    'business_type': business_type,
                    'business_class': random.choice(classes),
                    'inception_date': date(self.reporting_year - random.randint(0, 3),
                                          random.randint(1, 12),
                                          random.randint(1, 28)),
                    'expiry_date': date(self.reporting_year + random.randint(1, 5),
                                       random.randint(1, 12),
                                       random.randint(1, 28)),
                    'gwp': round(contract_gwp, 2),
                    'bel': round(contract_bel, 2),
                    'currency': 'GBP',
                    'protected_contract': random.random() > 0.1,
                    'eligible_claimant': random.random() > 0.15,
                    'territory': random.choice(['UK', 'EEA', 'Worldwide'])
                })

        detail_df = pd.DataFrame(detail_records)
        detail_df['included_in_fscs'] = (
            detail_df['protected_contract'] &
            detail_df['eligible_claimant']
        )

        return detail_df


# =============================================================================
# GENERATE ALL TABLES FOR POWER BI
# =============================================================================
print("Generating FSCS Data for Power BI...")
print("=" * 60)

# Create generator
generator = FSCSDataGenerator(num_syndicates=NUM_SYNDICATES, reporting_year=REPORTING_YEAR)

# Generate tables (these will be available in Power BI)
fscs_summary = generator.generate_fscs_output_format()
fscs_detail = generator.generate_detail_dataset()

print(f"fscs_summary: {len(fscs_summary)} records")
print(f"fscs_detail: {len(fscs_detail)} records")
print("=" * 60)
print("FSCS data generated successfully!")
