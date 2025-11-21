"""
Synthetic Data Generator for Lloyd's of London Solvency II ASB Returns
This module generates realistic synthetic insurance data for testing and demonstration purposes.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random

class LloydsDataGenerator:
    """
    Generates synthetic Lloyd's of London insurance data for Solvency II ASB returns.
    """

    # Lloyd's Lines of Business codes (EIOPA classifications)
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
        """
        Initialize the data generator.

        Parameters:
        -----------
        syndicate_number : str
            Lloyd's syndicate number
        syndicate_name : str
            Name of the syndicate
        start_year : int
            Starting underwriting year
        end_year : int
            Ending underwriting year
        random_seed : int
            Random seed for reproducibility
        """
        self.syndicate_number = syndicate_number
        self.syndicate_name = syndicate_name
        self.start_year = start_year
        self.end_year = end_year
        np.random.seed(random_seed)
        random.seed(random_seed)

    def generate_asb_245_246_247_data(self, num_records=500):
        """
        Generate synthetic data for ASB 245/246/247 (S.19.01.01)
        Non-Life Insurance Claims Information

        Returns:
        --------
        pd.DataFrame : DataFrame with claims data
        """
        data = []

        for _ in range(num_records):
            # Random selections
            currency = random.choice(self.CURRENCIES)
            lob_code = random.choice(list(self.LINES_OF_BUSINESS.keys()))
            underwriting_year = random.randint(self.start_year, self.end_year)

            # Development year (0 to 10 years)
            development_year = random.randint(0, 10)

            # Generate realistic claim amounts (in thousands)
            base_claim = np.random.lognormal(mean=10, sigma=2)

            # Development pattern - claims develop over time
            development_factor = 1 - (development_year * 0.08)
            development_factor = max(development_factor, 0.3)

            gross_claim_paid = base_claim * development_factor * np.random.uniform(0.8, 1.2)
            reinsurance_recoveries = gross_claim_paid * np.random.uniform(0.1, 0.4)

            # Best estimate claims provisions
            gross_be_provisions = gross_claim_paid * np.random.uniform(1.1, 1.5)
            discounting_gross = gross_be_provisions * np.random.uniform(0.02, 0.05)

            be_provisions_reins = reinsurance_recoveries * np.random.uniform(1.1, 1.5)
            discounting_reins = be_provisions_reins * np.random.uniform(0.02, 0.05)

            # RBNS (Reported But Not Settled)
            gross_rbns = gross_claim_paid * np.random.uniform(0.6, 0.9)
            reinsurance_rbns = reinsurance_recoveries * np.random.uniform(0.6, 0.9)

            discounting_rbns = gross_rbns * np.random.uniform(0.015, 0.04)
            discounting_reins_rbns = reinsurance_rbns * np.random.uniform(0.015, 0.04)

            record = {
                'Currency': currency,
                'LineOfBusiness': lob_code,
                'UnderwritingYear': underwriting_year,
                'DevelopmentYear': development_year,
                'GrossClaimPaid': round(gross_claim_paid, 2),
                'ReinsuranceRecoveries': round(reinsurance_recoveries, 2),
                'GrossUndiscountedBEClaimsProvisions': round(gross_be_provisions, 2),
                'DiscountingGrossBEClaimsProvisions': round(discounting_gross, 2),
                'UndiscountedBEClaimsProvisionsReinsRecoverable': round(be_provisions_reins, 2),
                'DiscountingBEClaimsProvisionsReinsRecoverable': round(discounting_reins, 2),
                'GrossRBNS': round(gross_rbns, 2),
                'ReinsuranceRBNS': round(reinsurance_rbns, 2),
                'DiscountingRBNS': round(discounting_rbns, 2),
                'DiscountingReinsuranceRBNS': round(discounting_reins_rbns, 2)
            }

            data.append(record)

        df = pd.DataFrame(data)

        # Sort by underwriting year, development year, and line of business
        df = df.sort_values(['UnderwritingYear', 'LineOfBusiness', 'DevelopmentYear'])
        df = df.reset_index(drop=True)

        return df

    def generate_asb_248_data(self, num_records=200):
        """
        Generate synthetic data for ASB 248 (S.19.01.01)
        Non-Life Insurance Claims Information - Inflation Rates

        Returns:
        --------
        pd.DataFrame : DataFrame with inflation rates data
        """
        data = []

        for _ in range(num_records):
            currency = random.choice(self.CURRENCIES)
            lob_code = random.choice(list(self.LINES_OF_BUSINESS.keys()))
            underwriting_year = random.randint(self.start_year, self.end_year)

            # Generate realistic inflation rates (as percentages)
            # Historic inflation rates
            historic_total = np.random.uniform(1.5, 4.5)
            historic_external = historic_total * np.random.uniform(0.5, 0.7)
            historic_endogenous = historic_total - historic_external

            # Expected inflation rates (usually slightly different from historic)
            expected_total = historic_total * np.random.uniform(0.9, 1.1)
            expected_external = expected_total * np.random.uniform(0.5, 0.7)
            expected_endogenous = expected_total - expected_external

            record = {
                'Currency': currency,
                'LineOfBusiness': lob_code,
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

        # Sort by underwriting year and line of business
        df = df.sort_values(['UnderwritingYear', 'LineOfBusiness'])
        df = df.reset_index(drop=True)

        return df

    def generate_all_data(self, claims_records=500, inflation_records=200):
        """
        Generate all ASB return data.

        Returns:
        --------
        dict : Dictionary containing all dataframes
        """
        return {
            'ASB_245_246_247': self.generate_asb_245_246_247_data(claims_records),
            'ASB_248': self.generate_asb_248_data(inflation_records),
            'metadata': {
                'syndicate_number': self.syndicate_number,
                'syndicate_name': self.syndicate_name,
                'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'lines_of_business': self.LINES_OF_BUSINESS
            }
        }


if __name__ == '__main__':
    # Example usage
    generator = LloydsDataGenerator(
        syndicate_number='1234',
        syndicate_name='Example Marine & Energy Syndicate',
        start_year=2015,
        end_year=2024
    )

    # Generate all data
    all_data = generator.generate_all_data()

    print("=" * 80)
    print("SYNTHETIC DATA GENERATION COMPLETE")
    print("=" * 80)
    print(f"\nSyndicate: {all_data['metadata']['syndicate_number']} - {all_data['metadata']['syndicate_name']}")
    print(f"Generation Date: {all_data['metadata']['generation_date']}")

    print("\nASB 245/246/247 Data:")
    print(all_data['ASB_245_246_247'].head(10))
    print(f"\nTotal records: {len(all_data['ASB_245_246_247'])}")

    print("\n" + "=" * 80)
    print("ASB 248 Data:")
    print(all_data['ASB_248'].head(10))
    print(f"\nTotal records: {len(all_data['ASB_248'])}")

    # Save to CSV files
    all_data['ASB_245_246_247'].to_csv('ASB_245_246_247_synthetic_data.csv', index=False)
    all_data['ASB_248'].to_csv('ASB_248_synthetic_data.csv', index=False)

    print("\n" + "=" * 80)
    print("Data saved to CSV files:")
    print("  - ASB_245_246_247_synthetic_data.csv")
    print("  - ASB_248_synthetic_data.csv")
    print("=" * 80)
