"""
Generate Synthetic Lloyd's of London Premium Data
This script creates realistic synthetic data for Solvency II Pillar 3 Risk and Claims Reporting
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define lookup data
RISK_CODES = ['1E', '1T', '2E', '2T', '3E', '3T', '4', '5', '6', '7', '8', '9', 'eh', 'el', 'em']
CURRENCIES = ['GBP', 'USD', 'EUR', 'JPY', 'CHF', 'AUD', 'CAD']
COUNTRIES = [
    'UNITED KINGDOM', 'UNITED STATES', 'GERMANY', 'FRANCE', 'SPAIN', 'ITALY',
    'JAPAN', 'AUSTRALIA', 'CANADA', 'NETHERLANDS', 'BELGIUM', 'SWITZERLAND',
    'SINGAPORE', 'HONG KONG', 'BRAZIL', 'MEXICO', 'INDIA', 'CHINA'
]
POLICYHOLDER_TYPES = ['RETAIL', 'BUSINESS', 'CORPORATE', 'COMMERCIAL']
SYNDICATES = [623, 1234, 2791, 3456, 4567, 5678, 6789, 7890, 8901, 9012]
YEARS_OF_ACCOUNT = [2021, 2022, 2023, 2024, 2025]
PART_VII_INDICATORS = ['Y', 'N', '']

# Define insured names by type
RETAIL_NAMES = ['Smith Ltd', 'Jones & Co', 'Williams Group', 'Brown Enterprises', 'Davis LLC']
BUSINESS_NAMES = ['Global Industries Inc', 'International Trading Co', 'Worldwide Logistics Ltd',
                  'Continental Services plc', 'United Manufacturing Corp']
CORPORATE_NAMES = ['Mega Corporation plc', 'Supreme Holdings Ltd', 'Premier Group International',
                   'Elite Consortium Ltd', 'Prime Industries Corp']
COMMERCIAL_NAMES = ['ABC Commercial Ltd', 'XYZ Trading Co', 'Metro Business Group',
                    'City Enterprises plc', 'Urban Services Ltd']

def generate_umr(syndicate, year):
    """Generate realistic UMR (Unique Market Reference)"""
    prefix = chr(random.randint(65, 90))  # Random letter
    number = f"{random.randint(1000, 9999)}"
    suffix = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=3))
    return f"{prefix}{syndicate}{number}{suffix}"

def generate_risk_reference(risk_code):
    """Generate risk/certificate reference"""
    return f"{risk_code}{random.randint(1000, 9999)}"

def generate_signing_number():
    """Generate original signing number"""
    year = random.choice([21, 22, 23, 24])
    seq = random.randint(10000, 99999)
    return f"{year}/{seq}"

def generate_signing_date(yoa):
    """Generate original signing date based on year of account"""
    start_date = datetime(yoa, 1, 1)
    end_date = datetime(yoa, 12, 31)
    random_days = random.randint(0, 364)
    signing_date = start_date + timedelta(days=random_days)
    return signing_date.strftime('%d/%m/%Y')

def generate_insured_name(policyholder_type):
    """Generate insured name based on policyholder type"""
    name_mapping = {
        'RETAIL': RETAIL_NAMES,
        'BUSINESS': BUSINESS_NAMES,
        'CORPORATE': CORPORATE_NAMES,
        'COMMERCIAL': COMMERCIAL_NAMES
    }
    return random.choice(name_mapping.get(policyholder_type, BUSINESS_NAMES))

def generate_premium_records(num_records=1000):
    """Generate synthetic premium records"""
    records = []

    for _ in range(num_records):
        syndicate = random.choice(SYNDICATES)
        yoa = random.choice(YEARS_OF_ACCOUNT)
        risk_code = random.choice(RISK_CODES)
        currency = random.choice(CURRENCIES)
        country = random.choice(COUNTRIES)
        policyholder_type = random.choice(POLICYHOLDER_TYPES)

        # Generate varying premium amounts based on policyholder type
        premium_multipliers = {
            'RETAIL': (5000, 100000),
            'BUSINESS': (50000, 500000),
            'CORPORATE': (500000, 5000000),
            'COMMERCIAL': (100000, 1000000)
        }

        min_prem, max_prem = premium_multipliers[policyholder_type]
        premium = round(np.random.uniform(min_prem, max_prem), 2)

        # Sum insured is typically 5-20x the premium
        sum_insured = round(premium * np.random.uniform(5, 20), 2)

        record = {
            'Syndicate Number': syndicate,
            'UMR': generate_umr(syndicate, yoa),
            'Insured Country': country,
            'Risk Location': country,  # Often same as insured country
            'Insured Name': generate_insured_name(policyholder_type),
            'Insured - Policyholder Type': policyholder_type,
            'Risk Code': risk_code,
            'Risk / Certificate Reference': generate_risk_reference(risk_code),
            'Original Currency': currency,
            'Sum Insured': sum_insured,
            'Gross Annual Premium in Period': premium,
            'YOA': yoa,
            'Part VII Indicator': random.choice(PART_VII_INDICATORS),
            'Original Signing Number': generate_signing_number(),
            'Original Signing Date': generate_signing_date(yoa)
        }

        records.append(record)

    return pd.DataFrame(records)

def main():
    """Generate and save synthetic data"""
    print("Generating synthetic Lloyd's premium data...")

    # Generate premium data
    df_premium = generate_premium_records(1000)

    # Save to CSV
    csv_path = 'synthetic_data/synthetic_lloyds_premium_data.csv'
    df_premium.to_csv(csv_path, index=False)
    print(f"\nSaved {len(df_premium)} records to {csv_path}")

    # Save to Excel with multiple sheets
    excel_path = 'synthetic_data/synthetic_lloyds_premium_data.xlsx'
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df_premium.to_excel(writer, sheet_name='Premium Data', index=False)

        # Add summary sheet
        summary = pd.DataFrame({
            'Metric': [
                'Total Records',
                'Total Premium (GBP equivalent)',
                'Number of Syndicates',
                'Number of Unique Countries',
                'Earliest YOA',
                'Latest YOA'
            ],
            'Value': [
                len(df_premium),
                f"{df_premium[df_premium['Original Currency']=='GBP']['Gross Annual Premium in Period'].sum():,.2f}",
                df_premium['Syndicate Number'].nunique(),
                df_premium['Insured Country'].nunique(),
                df_premium['YOA'].min(),
                df_premium['YOA'].max()
            ]
        })
        summary.to_excel(writer, sheet_name='Summary', index=False)

    print(f"Saved Excel file to {excel_path}")

    # Display summary statistics
    print("\n" + "="*80)
    print("DATA SUMMARY")
    print("="*80)
    print(f"\nTotal Records: {len(df_premium)}")
    print(f"\nBy Syndicate:")
    print(df_premium.groupby('Syndicate Number').size())
    print(f"\nBy Year of Account:")
    print(df_premium.groupby('YOA').size())
    print(f"\nBy Policyholder Type:")
    print(df_premium.groupby('Insured - Policyholder Type').size())
    print(f"\nPremium Statistics (GBP):")
    gbp_premiums = df_premium[df_premium['Original Currency']=='GBP']['Gross Annual Premium in Period']
    print(f"  Mean: £{gbp_premiums.mean():,.2f}")
    print(f"  Median: £{gbp_premiums.median():,.2f}")
    print(f"  Total: £{gbp_premiums.sum():,.2f}")
    print("\n" + "="*80)

    # Display sample records
    print("\nSample Records (first 5):")
    print(df_premium.head().to_string())

if __name__ == "__main__":
    main()
