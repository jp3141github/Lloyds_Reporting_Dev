"""
Generate Synthetic Lloyd's of London Claims Data

This script generates realistic synthetic claims data for testing
the Solvency II reporting templates in Power BI.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string


def generate_umr(syndicate_num: int) -> str:
    """Generate a realistic UMR (Unique Market Reference)"""
    year = random.choice(['B', 'A'])  # Binding or Anticipated
    year_code = str(random.randint(0, 4))
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{year}{year_code}{random_chars}{syndicate_num:04d}"


def generate_claim_reference() -> str:
    """Generate a realistic claim reference number"""
    prefix = random.choice(['CLM', 'REF', 'INC'])
    year = random.randint(2015, 2024)
    number = random.randint(10000, 99999)
    return f"{prefix}{year}{number}"


def generate_synthetic_claims_data(num_claims: int = 500, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic Lloyd's of London claims data.

    Args:
        num_claims: Number of claims to generate
        seed: Random seed for reproducibility

    Returns:
        DataFrame with synthetic claims data
    """
    np.random.seed(seed)
    random.seed(seed)

    # Define possible values
    syndicates = [123, 456, 789, 1001, 2468, 3579, 4321, 5678]
    risk_codes = ['1', '2', '3', '4', '5', '6', '7', '8', '9',
                  '1E', '1T', '2E', '2T', '3E', '3T', '4E', '4T',
                  'AO', 'AP', 'AW', 'cf']
    years_of_account = list(range(2015, 2025))
    currencies = ['GBP', 'USD', 'EUR', 'JPY', 'AUD', 'CAD', 'CHF']
    claim_statuses = ['Open', 'Closed', 'Reported in year']
    part_vii_indicators = ['Y', 'N']

    data = []

    for i in range(num_claims):
        syndicate = random.choice(syndicates)
        year_of_account = random.choice(years_of_account)

        # Generate claim reference and UMR
        claim_ref = generate_claim_reference()
        umr = generate_umr(syndicate)

        # Select risk code and currency
        risk_code = random.choice(risk_codes)
        currency = random.choice(currencies)

        # Generate claim status
        status_beginning = random.choice(claim_statuses)
        # If closed at beginning, stay closed; if open, can be open or closed
        if status_beginning == 'Closed':
            status_end = 'Closed'
        else:
            status_end = random.choice(claim_statuses)

        # Generate realistic monetary amounts
        # Base amount depends on risk code and year
        base_multiplier = random.uniform(0.5, 2.0)

        if risk_code in ['1', '2', '3', 'cf']:
            # Higher value risk codes
            outstanding_begin = random.uniform(50000, 500000) * base_multiplier
        else:
            outstanding_begin = random.uniform(10000, 200000) * base_multiplier

        # Paid to date is cumulative
        paid_to_date = random.uniform(0, outstanding_begin * 1.5)

        # Paid in year is a portion of paid to date
        paid_in_year = random.uniform(0, paid_to_date * 0.3)

        # Outstanding at end depends on status
        if status_end == 'Closed':
            outstanding_end = 0
        else:
            # Can increase or decrease
            change_factor = random.uniform(0.7, 1.3)
            outstanding_end = outstanding_begin * change_factor

        # Part VII indicator
        part_vii = random.choice(part_vii_indicators)

        # Generate signing details
        original_signing_number = f"OS{random.randint(100000, 999999)}"
        days_back = random.randint(365, 3650)
        signing_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

        # UCR and COR (optional fields)
        ucr = f"UCR{random.randint(100000, 999999)}" if random.random() > 0.3 else None
        cor = f"COR{random.randint(100000, 999999)}" if random.random() > 0.5 else None

        claim_data = {
            'Syndicate Number': syndicate,
            'Claim Reference': claim_ref,
            'UMR': umr,
            'Risk Code': risk_code,
            'Year of Account': year_of_account,
            'Original Currency': currency,
            'Claim status at beginning of period': status_beginning,
            'Claim status at end of period': status_end,
            'Outstanding Claims Amount as at beginning of period': round(outstanding_begin, 2),
            'Paid to Date Amount': round(paid_to_date, 2),
            'Paid in Year amount': round(paid_in_year, 2),
            'Outstanding Claim amount as at end of period': round(outstanding_end, 2),
            'Part VII Indicator': part_vii,
            'Original Signing Number': original_signing_number,
            'Original Signing Date': signing_date,
            'UCR': ucr,
            'COR': cor
        }

        data.append(claim_data)

    df = pd.DataFrame(data)
    return df


def create_lookup_tables() -> dict:
    """
    Create lookup/reference tables for the data.

    Returns:
        Dictionary containing lookup tables
    """
    risk_codes_df = pd.DataFrame({
        'Risk Code': ['1', '2', '3', '4', '5', '6', '7', '8', '9',
                      '1E', '1T', '2E', '2T', '3E', '3T', '4E', '4T',
                      '5T', '6T', '7T', '8T', 'AO', 'AP', 'AW', 'cf'],
        'Description': [
            'Accident & Health', 'Motor (Third Party Liability)', 'Motor (Other Classes)',
            'Marine, Aviation, Transport', 'Fire & Other Property Damage', 'Third Party Liability',
            'Credit & Suretyship', 'Legal Expenses', 'Assistance',
            'Life', 'Life Treaty', 'Accident Treaty', 'Accident & Health Treaty',
            'Motor Treaty', 'Motor Other Treaty', 'Marine Aviation Transport Treaty',
            'Marine Treaty', 'Property Treaty', 'Third Party Liability Treaty',
            'Credit Treaty', 'Legal Expenses Treaty', 'Aviation Other',
            'Aviation Passengers', 'Aviation War', 'Casualty Fire'
        ]
    })

    claim_status_df = pd.DataFrame({
        'Claim Status': ['Open', 'Closed', 'Reported in year'],
        'Description': [
            'Claim is currently open and being handled',
            'Claim has been settled and closed',
            'Claim was reported during the current year'
        ]
    })

    currency_df = pd.DataFrame({
        'Currency Code': ['GBP', 'USD', 'EUR', 'JPY', 'AUD', 'CAD', 'CHF', 'AED', 'ARS', 'BRL'],
        'Currency Name': [
            'British Pound Sterling', 'US Dollar', 'Euro', 'Japanese Yen',
            'Australian Dollar', 'Canadian Dollar', 'Swiss Franc',
            'UAE Dirham', 'Argentine Peso', 'Brazilian Real'
        ]
    })

    syndicate_df = pd.DataFrame({
        'Syndicate Number': [123, 456, 789, 1001, 2468, 3579, 4321, 5678],
        'Syndicate Name': [
            'Syndicate 123 - Marine & Energy',
            'Syndicate 456 - Property & Casualty',
            'Syndicate 789 - Specialty Lines',
            'Syndicate 1001 - Aviation',
            'Syndicate 2468 - Reinsurance',
            'Syndicate 3579 - Financial Lines',
            'Syndicate 4321 - Motor & Liability',
            'Syndicate 5678 - Professional Indemnity'
        ]
    })

    return {
        'risk_codes': risk_codes_df,
        'claim_status': claim_status_df,
        'currencies': currency_df,
        'syndicates': syndicate_df
    }


def export_synthetic_data(output_path: str = 'synthetic_lloyds_claims_data.xlsx'):
    """
    Generate and export synthetic claims data to Excel.

    Args:
        output_path: Path to save the Excel file
    """
    print("Generating synthetic Lloyd's of London claims data...")

    # Generate main claims data
    claims_df = generate_synthetic_claims_data(num_claims=500)

    # Generate lookup tables
    lookups = create_lookup_tables()

    # Create Excel file with multiple sheets
    print(f"Exporting data to {output_path}...")

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Write main claims data
        claims_df.to_excel(writer, sheet_name='input Sheet', index=False)

        # Write a smaller sample
        claims_df.head(10).to_excel(writer, sheet_name='sample', index=False)

        # Write lookup tables
        lookups['risk_codes'].to_excel(writer, sheet_name='Risk Codes', index=False)
        lookups['claim_status'].to_excel(writer, sheet_name='Claim Status', index=False)
        lookups['currencies'].to_excel(writer, sheet_name='Currencies', index=False)
        lookups['syndicates'].to_excel(writer, sheet_name='Syndicates', index=False)

    print(f"Successfully generated {len(claims_df)} synthetic claims records")
    print(f"\nData summary:")
    print(f"  - Syndicates: {claims_df['Syndicate Number'].nunique()}")
    print(f"  - Years of Account: {sorted(claims_df['Year of Account'].unique())}")
    print(f"  - Total Outstanding (Beginning): £{claims_df['Outstanding Claims Amount as at beginning of period'].sum():,.2f}")
    print(f"  - Total Paid to Date: £{claims_df['Paid to Date Amount'].sum():,.2f}")
    print(f"  - Total Outstanding (End): £{claims_df['Outstanding Claim amount as at end of period'].sum():,.2f}")
    print(f"\nFile saved to: {output_path}")


if __name__ == "__main__":
    # Generate and export the data
    export_synthetic_data('synthetic_lloyds_claims_data.xlsx')
