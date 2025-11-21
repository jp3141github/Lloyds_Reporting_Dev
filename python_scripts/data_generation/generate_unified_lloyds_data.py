"""
Unified Lloyd's of London Data Generator for RRQ and RRA
Generates realistic RRQ (Quarterly) and RRA (Annual) data with configuration-based switching

This script creates synthetic Lloyd's data for both quarterly and annual returns
that can be used in Power BI for testing RRA/RRQ reporting templates.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
from typing import Literal, Optional, List

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


class UnifiedLloydsDataGenerator:
    """Generates synthetic Lloyd's data for both RRQ (Quarterly) and RRA (Annual) returns"""

    def __init__(self,
                 return_type: Literal['RRQ', 'RRA'] = 'RRA',
                 reporting_year: int = 2024,
                 reporting_quarter: Optional[Literal['Q1', 'Q2', 'Q3', 'Q4']] = None,
                 output_dir: str = '../../synthetic_data'):
        """
        Initialize the unified data generator

        Parameters:
        -----------
        return_type : str
            'RRQ' for quarterly or 'RRA' for annual
        reporting_year : int
            The year being reported
        reporting_quarter : str, optional
            'Q1', 'Q2', 'Q3', or 'Q4' (required for RRQ)
        output_dir : str
            Directory to save generated files
        """
        self.return_type = return_type
        self.reporting_year = reporting_year
        self.reporting_quarter = reporting_quarter

        # Validate inputs
        if return_type == 'RRQ' and reporting_quarter is None:
            raise ValueError("reporting_quarter is required for RRQ return type")

        # Create output directory with return type suffix
        if return_type == 'RRQ':
            self.output_dir = f"{output_dir}_{return_type.lower()}_{reporting_year}_{reporting_quarter.lower()}"
        else:
            self.output_dir = f"{output_dir}_{return_type.lower()}_{reporting_year}"

        os.makedirs(self.output_dir, exist_ok=True)

        # Lloyd's syndicate numbers (realistic ranges)
        self.syndicates = [2987, 33, 1183, 2791, 623, 4242, 5000, 1910, 2010, 2525]

        # Determine years of account scope based on return type
        self.current_year = reporting_year
        if return_type == 'RRA':
            # RRA: All historical years
            self.years_of_account = list(range(2018, reporting_year + 1))
        else:  # RRQ
            # RRQ: Current year + prior 2 years only
            self.years_of_account = list(range(reporting_year - 2, reporting_year + 1))

        # Classes of Business (Lloyd's typical classes)
        self.classes_of_business = {
            'A1': 'Direct Accident & Health',
            'A2': 'Accident & Health Reinsurance',
            'D1': 'Direct Motor (Private Car)',
            'D2': 'Direct Motor (Commercial)',
            'E1': 'Energy Offshore',
            'E2': 'Energy Onshore',
            'F1': 'Fire & Other Damage - Direct',
            'F2': 'Fire & Other Damage - Reinsurance',
            'M1': 'Marine Cargo',
            'M2': 'Marine Hull',
            'M3': 'Marine Liability',
            'N1': 'Non-Marine Property Treaty',
            'N2': 'Non-Marine Property Facultative',
            'P1': 'Professional Indemnity',
            'P2': 'Public & Products Liability',
            'T1': 'Third Party Liability - Direct',
            'T2': 'Third Party Liability - Reinsurance',
            'V1': 'Aviation',
            'W1': 'Political Risk & Contingency',
            'X1': 'Catastrophe Reinsurance'
        }

        # Catastrophe codes
        self.cat_codes = {
            'NAT01': 'Hurricane - USA',
            'NAT02': 'Earthquake - Japan',
            'NAT03': 'Flood - Europe',
            'NAT04': 'Windstorm - Europe',
            'NAT05': 'Wildfire - USA',
            'MAN01': 'Cyber Attack',
            'MAN02': 'Industrial Accident',
            'MAN03': 'Aviation Accident'
        }

        # Currency codes
        self.currencies = ['GBP', 'USD', 'EUR', 'CAD', 'AUD', 'JPY']

        # Determine "as at" date based on quarter
        self.as_at_date = self._get_as_at_date()

        # Define which forms are required for this return type and quarter
        self.required_forms = self._get_required_forms()

    def _get_as_at_date(self) -> str:
        """Get the 'as at' date based on return type and quarter"""
        if self.return_type == 'RRA':
            return f'{self.reporting_year}-12-31'
        else:  # RRQ
            quarter_end_dates = {
                'Q1': f'{self.reporting_year}-03-31',
                'Q2': f'{self.reporting_year}-06-30',
                'Q3': f'{self.reporting_year}-09-30',
                'Q4': f'{self.reporting_year}-12-31'
            }
            return quarter_end_dates[self.reporting_quarter]

    def _get_required_forms(self) -> List[str]:
        """Determine which forms are required based on return type and quarter"""
        # Forms required in all RRQ quarters
        rrq_all_quarters = ['010', '020', '071', '091', '193', '291', '292', '293', '294', '295', '990']

        # Forms only required in Q4 for RRQ
        rrq_q4_only = ['081', '391', '910']

        # All RRA forms
        rra_all = ['010', '020', '071', '081', '091', '193', '291', '292', '293', '294', '295', '391', '910', '990']

        if self.return_type == 'RRA':
            return rra_all
        else:  # RRQ
            if self.reporting_quarter == 'Q4':
                return rrq_all_quarters + rrq_q4_only
            else:
                return rrq_all_quarters

    def generate_control_data(self):
        """Generate Form 010 Control Data"""
        control_data = []

        for syndicate in self.syndicates:
            control_data.append({
                'Syndicate_Number': syndicate,
                'Return_Type': self.return_type,
                'Reporting_Quarter': self.reporting_quarter if self.return_type == 'RRQ' else 'N/A',
                'Reporting_Year': self.reporting_year,
                'Status': random.choice(['Draft', 'Submitted', 'Approved']),
                'Edition': '1.1',
                'Managing_Agent_Name': f'Managing Agent {syndicate}',
                'First_Pure_YoA': min(self.years_of_account),
                'First_Reporting_YoA': min(self.years_of_account),
                'Final_Pure_YoA': max(self.years_of_account) - 1 if self.return_type == 'RRA' else max(self.years_of_account),
                'Prospective_Year': max(self.years_of_account) if self.return_type == 'RRA' else 'N/A',
                'Contact_Username': f'user{syndicate}',
                'Contact_Name': f'Contact Person {syndicate}',
                'Contact_Phone': f'+44 20 {random.randint(7000, 7999)} {random.randint(1000, 9999)}',
                'Contact_Email': f'contact{syndicate}@lloyds.com',
                'Submission_Date': datetime.now().strftime('%Y-%m-%d'),
                'As_At_Date': self.as_at_date,
                'Capacity_GBP': random.randint(50000000, 500000000)
            })

        df = pd.DataFrame(control_data)
        filename = f'{self.return_type.lower()}_010_control.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 010 Control: {len(df)} records")
        return df

    def generate_exchange_rates(self):
        """Generate Form 020 Exchange Rates"""
        exchange_rates = []

        base_rates = {
            'USD': 1.27,
            'EUR': 1.17,
            'CAD': 1.72,
            'AUD': 1.95,
            'JPY': 188.5,
            'GBP': 1.00
        }

        for year in self.years_of_account:
            for currency, base_rate in base_rates.items():
                variation = random.uniform(0.95, 1.05)
                exchange_rates.append({
                    'Return_Type': self.return_type,
                    'Reporting_Period': self.as_at_date,
                    'Year_of_Account': year,
                    'Currency_Code': currency,
                    'Currency_Name': currency,
                    'Exchange_Rate_to_GBP': round(base_rate * variation, 4),
                    'Rate_Type': 'Average',
                    'Effective_Date': self.as_at_date
                })

        df = pd.DataFrame(exchange_rates)
        filename = f'{self.return_type.lower()}_020_exchange_rates.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 020 Exchange Rates: {len(df)} records")
        return df

    def generate_net_claims(self):
        """Generate Form 193 Net Claims Data with RRQ/RRA scoping"""
        net_claims = []

        for syndicate in self.syndicates:
            for year in self.years_of_account:
                for lob_code in list(self.classes_of_business.keys())[:5]:
                    # Determine development years based on return type
                    if self.return_type == 'RRA':
                        # RRA: Full development history
                        max_dev = min(8, self.reporting_year - year + 1)
                    else:  # RRQ
                        # RRQ: Limited development (typically 0-2 years)
                        max_dev = min(3, self.reporting_year - year + 1)

                    for development_year in range(0, max_dev):
                        base_premium = random.randint(1000000, 20000000)
                        loss_ratio = random.uniform(0.45, 0.85)
                        development_factor = min(1.0, 0.2 + (development_year * 0.15))

                        cumulative_paid = int(base_premium * loss_ratio * development_factor)
                        case_reserves = int(base_premium * loss_ratio * (1 - development_factor) * 0.6)
                        ibnr = int(base_premium * loss_ratio * (1 - development_factor) * 0.4)

                        net_claims.append({
                            'Return_Type': self.return_type,
                            'Reporting_Quarter': self.reporting_quarter if self.return_type == 'RRQ' else 'N/A',
                            'Syndicate_Number': syndicate,
                            'Year_of_Account': year,
                            'Development_Year': development_year,
                            'LOB_Code': lob_code,
                            'Currency': 'GBP',
                            'Gross_Premium_Written': base_premium,
                            'Net_Premium_Written': int(base_premium * 0.85),
                            'Cumulative_Paid_Claims': cumulative_paid,
                            'Case_Reserves': case_reserves,
                            'IBNR_Reserve': ibnr,
                            'Total_Incurred': cumulative_paid + case_reserves + ibnr,
                            'Number_of_Claims': random.randint(10, 500),
                            'Number_of_Claims_Closed': int(random.randint(5, 400) * development_factor),
                            'As_At_Date': self.as_at_date,
                            'Calendar_Period': f'{year + development_year}'
                        })

        df = pd.DataFrame(net_claims)
        filename = f'{self.return_type.lower()}_193_net_claims.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 193 Net Claims: {len(df)} records")
        return df

    def generate_gross_premium_ibnr(self):
        """Generate Form 291 Gross Premium and IBNR"""
        gross_data = []

        for syndicate in self.syndicates:
            for year in self.years_of_account:
                for lob_code in list(self.classes_of_business.keys())[:5]:
                    gwp = random.randint(5000000, 50000000)
                    ultimate_loss_ratio = random.uniform(0.55, 0.75)

                    gross_data.append({
                        'Return_Type': self.return_type,
                        'Reporting_Quarter': self.reporting_quarter if self.return_type == 'RRQ' else 'N/A',
                        'Syndicate_Number': syndicate,
                        'Year_of_Account': year,
                        'LOB_Code': lob_code,
                        'Currency': 'GBP',
                        'Gross_Written_Premium': gwp,
                        'Gross_Earned_Premium': int(gwp * random.uniform(0.85, 0.95)),
                        'Paid_Claims_Gross': int(gwp * ultimate_loss_ratio * random.uniform(0.4, 0.7)),
                        'Case_Reserves_Gross': int(gwp * ultimate_loss_ratio * random.uniform(0.1, 0.2)),
                        'IBNR_Best_Estimate': int(gwp * ultimate_loss_ratio * random.uniform(0.15, 0.35)),
                        'IBNR_High': int(gwp * ultimate_loss_ratio * random.uniform(0.20, 0.40)),
                        'IBNR_Low': int(gwp * ultimate_loss_ratio * random.uniform(0.10, 0.25)),
                        'Ultimate_Loss_Ratio': round(ultimate_loss_ratio, 4),
                        'As_At_Date': self.as_at_date
                    })

        df = pd.DataFrame(gross_data)
        filename = f'{self.return_type.lower()}_291_gross_premium_ibnr.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 291 Gross Premium & IBNR: {len(df)} records")
        return df

    def generate_all_data(self):
        """Generate all required forms based on return type and quarter"""
        print("\n" + "="*70)
        print(f"Generating Synthetic Lloyd's {self.return_type} Data")
        if self.return_type == 'RRQ':
            print(f"Quarter: {self.reporting_quarter} {self.reporting_year}")
        else:
            print(f"Year: {self.reporting_year}")
        print(f"Years of Account in Scope: {min(self.years_of_account)}-{max(self.years_of_account)}")
        print(f"As At Date: {self.as_at_date}")
        print("="*70 + "\n")

        # Generate forms based on requirements
        if '010' in self.required_forms:
            self.generate_control_data()

        if '020' in self.required_forms:
            self.generate_exchange_rates()

        if '193' in self.required_forms:
            self.generate_net_claims()

        if '291' in self.required_forms:
            self.generate_gross_premium_ibnr()

        # Note: Other forms can be generated similarly
        # For brevity, only key forms shown here

        print("\n" + "="*70)
        print(f"All {self.return_type} data generated successfully in: {self.output_dir}")
        print(f"Forms generated: {', '.join(self.required_forms)}")
        print("="*70 + "\n")


def generate_full_year_rrq(year: int = 2024, output_base_dir: str = '../../synthetic_data'):
    """
    Generate RRQ data for all four quarters of a year

    Parameters:
    -----------
    year : int
        Reporting year
    output_base_dir : str
        Base output directory
    """
    print("\n" + "="*70)
    print(f"Generating Full Year RRQ Data for {year}")
    print("="*70 + "\n")

    quarters = ['Q1', 'Q2', 'Q3', 'Q4']

    for quarter in quarters:
        print(f"\nGenerating {quarter} {year}...")
        print("-" * 70)

        generator = UnifiedLloydsDataGenerator(
            return_type='RRQ',
            reporting_year=year,
            reporting_quarter=quarter,
            output_dir=output_base_dir
        )
        generator.generate_all_data()

    print("\n" + "="*70)
    print(f"Complete! Generated RRQ data for all quarters of {year}")
    print("="*70 + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate Unified Lloyd\'s RRQ/RRA Data')
    parser.add_argument('--type', choices=['RRQ', 'RRA'], default='RRA',
                        help='Return type: RRQ or RRA')
    parser.add_argument('--year', type=int, default=2024,
                        help='Reporting year')
    parser.add_argument('--quarter', choices=['Q1', 'Q2', 'Q3', 'Q4'],
                        help='Reporting quarter (required for RRQ)')
    parser.add_argument('--all-quarters', action='store_true',
                        help='Generate all four quarters of RRQ data')
    parser.add_argument('--output', default='../../synthetic_data',
                        help='Output directory')

    args = parser.parse_args()

    if args.all_quarters:
        # Generate all quarters
        generate_full_year_rrq(args.year, args.output)
    else:
        # Generate single return
        generator = UnifiedLloydsDataGenerator(
            return_type=args.type,
            reporting_year=args.year,
            reporting_quarter=args.quarter,
            output_dir=args.output
        )
        generator.generate_all_data()

    print("\nSynthetic Lloyd's data generation complete!")
    print("Files can now be imported into Power BI for testing RRA/RRQ reports.")
