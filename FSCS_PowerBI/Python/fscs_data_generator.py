"""
FSCS Data Generator for Lloyd's Syndicates
==========================================

This module generates synthetic Lloyd's of London insurance data for
Financial Services Compensation Scheme (FSCS) reporting purposes.

The data generated includes:
- Syndicate information
- Gross written premiums (General and Life business)
- Gross best estimate liabilities (General and Life business)

Data is generated for 'protected contracts with eligible claimants' only.
"""

import pandas as pd
import numpy as np
from datetime import datetime, date
import random


class FSCSDataGenerator:
    """Generates synthetic Lloyd's syndicate data for FSCS reporting."""

    def __init__(self, num_syndicates=10, reporting_year=2024, random_seed=42):
        """
        Initialize the FSCS data generator.

        Parameters:
        -----------
        num_syndicates : int
            Number of syndicates to generate data for
        reporting_year : int
            Year for which the data is being reported
        random_seed : int
            Seed for reproducibility
        """
        self.num_syndicates = num_syndicates
        self.reporting_year = reporting_year
        np.random.seed(random_seed)
        random.seed(random_seed)

    def generate_syndicate_numbers(self):
        """Generate realistic Lloyd's syndicate numbers (typically 3-4 digits)."""
        # Lloyd's syndicate numbers typically range from 1 to 9999
        # Common ranges are 2000-6000
        base_numbers = random.sample(range(2000, 6000), self.num_syndicates)
        return sorted(base_numbers)

    def generate_gross_written_premium(self, business_type='general'):
        """
        Generate gross written premium values.

        Parameters:
        -----------
        business_type : str
            'general' or 'life' business

        Returns:
        --------
        numpy.array : Array of premium values
        """
        if business_type == 'general':
            # General business typically has higher premiums
            # Range: £10M to £500M
            min_value = 10_000_000
            max_value = 500_000_000
            mean = 150_000_000
            std = 100_000_000
        else:  # life business
            # Life business typically has lower volumes in Lloyd's
            # Range: £1M to £100M
            min_value = 1_000_000
            max_value = 100_000_000
            mean = 30_000_000
            std = 25_000_000

        # Generate log-normal distribution (typical for insurance premiums)
        values = np.random.lognormal(
            mean=np.log(mean),
            sigma=0.5,
            size=self.num_syndicates
        )

        # Clip to realistic ranges
        values = np.clip(values, min_value, max_value)

        # Add some zero values (some syndicates may not write certain business)
        zero_mask = np.random.random(self.num_syndicates) < 0.2
        values[zero_mask] = 0

        return np.round(values, 2)

    def generate_best_estimate_liabilities(self, gwp_values, business_type='general'):
        """
        Generate gross best estimate liabilities.

        Best estimate liabilities are typically correlated with premiums
        but represent reserves for outstanding claims.

        Parameters:
        -----------
        gwp_values : numpy.array
            Gross written premium values
        business_type : str
            'general' or 'life' business

        Returns:
        --------
        numpy.array : Array of liability values
        """
        if business_type == 'general':
            # General business BEL typically 1.5-3x of annual premium
            multiplier = np.random.uniform(1.5, 3.0, self.num_syndicates)
        else:  # life business
            # Life business BEL typically 3-8x of annual premium
            multiplier = np.random.uniform(3.0, 8.0, self.num_syndicates)

        # Calculate BEL as multiple of GWP with some randomness
        values = gwp_values * multiplier

        # Add random variation (±20%)
        variation = np.random.uniform(0.8, 1.2, self.num_syndicates)
        values = values * variation

        # If GWP is zero, BEL should also be zero or very small
        zero_mask = gwp_values == 0
        values[zero_mask] = np.random.uniform(0, 5_000_000, np.sum(zero_mask))

        return np.round(values, 2)

    def generate_full_dataset(self):
        """
        Generate complete FSCS dataset for all syndicates.

        Returns:
        --------
        pandas.DataFrame : Complete dataset with all required fields
        """
        # Generate syndicate numbers
        syndicates = self.generate_syndicate_numbers()

        # Generate gross written premiums
        gwp_general = self.generate_gross_written_premium('general')
        gwp_life = self.generate_gross_written_premium('life')

        # Generate best estimate liabilities
        bel_general = self.generate_best_estimate_liabilities(gwp_general, 'general')
        bel_life = self.generate_best_estimate_liabilities(gwp_life, 'life')

        # Create DataFrame
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

        # Add syndicate characteristics
        df['managing_agent'] = df['syndicate_number'].apply(
            lambda x: f"Managing Agent {random.randint(1, 50):03d}"
        )

        # Add business mix percentage
        df['general_business_pct'] = np.where(
            df['gwp_total'] > 0,
            (df['gwp_general_business'] / df['gwp_total'] * 100).round(2),
            0
        )

        return df

    def generate_fscs_output_format(self):
        """
        Generate data in the exact format required by FSCS template.

        Returns:
        --------
        pandas.DataFrame : Data formatted for FSCS submission
        """
        df = self.generate_full_dataset()

        # Create output in FSCS format (one row per syndicate)
        output = pd.DataFrame({
            'Syndicate Number': df['syndicate_number'],
            'Reporting Year': df['reporting_year'],
            'Reporting Date': df['reporting_date'],
            'GWP General Business (£)': df['gwp_general_business'],
            'GWP Life Business (£)': df['gwp_life_business'],
            'BEL General Business (£)': df['bel_general_business'],
            'BEL Life Business (£)': df['bel_life_business'],
            'Notes': 'Protected contracts with eligible claimants only'
        })

        return output

    def generate_detail_dataset(self):
        """
        Generate detailed transactional data that could feed into the summary.
        This represents underlying policy/contract data.

        Returns:
        --------
        pandas.DataFrame : Detailed transaction-level data
        """
        base_df = self.generate_full_dataset()

        detail_records = []

        for _, row in base_df.iterrows():
            syndicate = row['syndicate_number']

            # Generate 50-200 contracts per syndicate
            num_contracts = random.randint(50, 200)

            for i in range(num_contracts):
                # Randomly assign business type
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

                # Distribute total amounts across contracts
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
                    'protected_contract': random.random() > 0.1,  # 90% are protected
                    'eligible_claimant': random.random() > 0.15,  # 85% are eligible
                    'territory': random.choice(['UK', 'EEA', 'Worldwide'])
                })

        detail_df = pd.DataFrame(detail_records)

        # Filter to only protected contracts with eligible claimants
        detail_df['included_in_fscs'] = (
            detail_df['protected_contract'] &
            detail_df['eligible_claimant']
        )

        return detail_df


# Power BI Integration Functions
def get_fscs_summary_data(num_syndicates=10, reporting_year=2024):
    """
    Main function to be called from Power BI for summary data.

    Parameters:
    -----------
    num_syndicates : int
        Number of syndicates to generate
    reporting_year : int
        Reporting year

    Returns:
    --------
    pandas.DataFrame : FSCS summary data
    """
    generator = FSCSDataGenerator(num_syndicates, reporting_year)
    return generator.generate_fscs_output_format()


def get_fscs_detail_data(num_syndicates=10, reporting_year=2024):
    """
    Function to be called from Power BI for detailed transaction data.

    Parameters:
    -----------
    num_syndicates : int
        Number of syndicates to generate
    reporting_year : int
        Reporting year

    Returns:
    --------
    pandas.DataFrame : Detailed transaction data
    """
    generator = FSCSDataGenerator(num_syndicates, reporting_year)
    return generator.generate_detail_dataset()


# For testing purposes
if __name__ == "__main__":
    # Generate sample data
    generator = FSCSDataGenerator(num_syndicates=10, reporting_year=2024)

    print("="*80)
    print("FSCS SUMMARY DATA")
    print("="*80)
    summary = generator.generate_fscs_output_format()
    print(summary.to_string())

    print("\n" + "="*80)
    print("DETAILED TRANSACTION DATA (First 20 records)")
    print("="*80)
    detail = generator.generate_detail_dataset()
    print(detail.head(20).to_string())

    print(f"\nTotal detail records generated: {len(detail)}")
    print(f"Records included in FSCS: {detail['included_in_fscs'].sum()}")
