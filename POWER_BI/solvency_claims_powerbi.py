"""
Solvency II Claims Processing for Power BI
==========================================
Processes Lloyd's of London claims data for Solvency II reporting.
Compatible with Power BI as a Python data source.

Tables Generated:
- detailed_claims: Full claims detail
- by_syndicate: Claims aggregated by Syndicate
- by_risk_code: Claims aggregated by Risk Code
- by_claim_status: Claims aggregated by Claim Status
- summary: Overall claims summary

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
NUM_CLAIMS_PER_SYNDICATE = 100
CURRENT_YEAR = 2024

# Lloyd's syndicates
SYNDICATES = [2987, 33, 1183, 2791, 623, 4242, 5000, 1910, 2010, 2525]

# Risk codes
RISK_CODES = ['PR', 'CA', 'MA', 'AV', 'EN', 'PI', 'PL', 'MO', 'CY', 'PA']

# Claim statuses
CLAIM_STATUSES = ['Open', 'Re-opened', 'Closed', 'Pending Review', 'In Litigation']


def generate_synthetic_claims():
    """Generate synthetic claims data for all syndicates"""
    claims = []

    for syndicate in SYNDICATES:
        for i in range(NUM_CLAIMS_PER_SYNDICATE):
            year_of_account = random.randint(CURRENT_YEAR - 6, CURRENT_YEAR)
            risk_code = random.choice(RISK_CODES)

            # Generate claim amounts
            os_beginning = random.randint(10000, 500000) if random.random() > 0.3 else 0
            paid_to_date = random.randint(5000, 300000)
            paid_in_year = random.randint(0, 100000)
            os_end = max(0, os_beginning + random.randint(-50000, 100000))

            # Determine claim status based on amounts
            if os_end == 0 and paid_to_date > 0:
                status_end = 'Closed'
            elif os_end > os_beginning:
                status_end = random.choice(['Open', 'Re-opened', 'In Litigation'])
            else:
                status_end = random.choice(CLAIM_STATUSES)

            status_beginning = 'Closed' if os_beginning == 0 else random.choice(['Open', 'Re-opened', 'Pending Review'])

            claims.append({
                'Syndicate Number': syndicate,
                'Claim Reference': f'CLM-{syndicate}-{year_of_account}-{i+1:05d}',
                'UMR': f'B{random.randint(1000, 9999)}{syndicate}{random.randint(10, 99)}',
                'Risk Code': risk_code,
                'Year of Account': year_of_account,
                'Original Currency': random.choice(['GBP', 'USD', 'EUR']),
                'Claim status at beginning of period': status_beginning,
                'Claim status at end of period': status_end,
                'Outstanding Claims Amount as at beginning of period': os_beginning,
                'Paid to Date Amount': paid_to_date,
                'Paid in Year amount': paid_in_year,
                'Outstanding Claim amount as at end of period': os_end,
                'Inception Date': f'{year_of_account}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}',
                'Loss Date': f'{year_of_account + random.randint(0, 1)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}',
                'Notification Date': f'{year_of_account + random.randint(0, 2)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'
            })

    return pd.DataFrame(claims)


def calculate_incurred_amounts(df):
    """Calculate total incurred amounts for claims."""
    df = df.copy()

    # Total Incurred = Paid to Date + Outstanding at end of period
    df['Total Incurred as at end of period'] = (
        df['Paid to Date Amount'] +
        df['Outstanding Claim amount as at end of period']
    )

    # Movement in year
    df['Movement in Year'] = (
        df['Outstanding Claim amount as at end of period'] -
        df['Outstanding Claims Amount as at beginning of period'] +
        df['Paid in Year amount']
    )

    # Reserve movement
    df['Reserve Movement'] = (
        df['Outstanding Claim amount as at end of period'] -
        df['Outstanding Claims Amount as at beginning of period']
    )

    return df


def aggregate_by_syndicate(df):
    """Aggregate claims data by syndicate and year of account."""
    agg_dict = {
        'Claim Reference': 'count',
        'Outstanding Claims Amount as at beginning of period': 'sum',
        'Paid to Date Amount': 'sum',
        'Paid in Year amount': 'sum',
        'Outstanding Claim amount as at end of period': 'sum',
        'Total Incurred as at end of period': 'sum',
        'Movement in Year': 'sum',
        'Reserve Movement': 'sum'
    }

    grouped = df.groupby([
        'Syndicate Number',
        'Year of Account'
    ]).agg(agg_dict).reset_index()

    grouped.rename(columns={'Claim Reference': 'Number of Claims'}, inplace=True)

    return grouped


def aggregate_by_risk_code(df):
    """Aggregate claims data by risk code and year of account."""
    agg_dict = {
        'Claim Reference': 'count',
        'Outstanding Claims Amount as at beginning of period': 'sum',
        'Paid to Date Amount': 'sum',
        'Paid in Year amount': 'sum',
        'Outstanding Claim amount as at end of period': 'sum',
        'Total Incurred as at end of period': 'sum',
        'Movement in Year': 'sum',
        'Reserve Movement': 'sum'
    }

    grouped = df.groupby([
        'Syndicate Number',
        'Year of Account',
        'Risk Code'
    ]).agg(agg_dict).reset_index()

    grouped.rename(columns={'Claim Reference': 'Number of Claims'}, inplace=True)

    return grouped


def aggregate_by_claim_status(df):
    """Aggregate claims data by claim status."""
    agg_dict = {
        'Claim Reference': 'count',
        'Outstanding Claims Amount as at beginning of period': 'sum',
        'Paid to Date Amount': 'sum',
        'Paid in Year amount': 'sum',
        'Outstanding Claim amount as at end of period': 'sum',
        'Total Incurred as at end of period': 'sum',
        'Movement in Year': 'sum',
        'Reserve Movement': 'sum'
    }

    grouped = df.groupby([
        'Syndicate Number',
        'Year of Account',
        'Claim status at end of period'
    ]).agg(agg_dict).reset_index()

    grouped.rename(columns={'Claim Reference': 'Number of Claims'}, inplace=True)

    return grouped


def create_summary_report(df):
    """Create overall summary report for all syndicates."""
    summary_data = {
        'Total Number of Claims': len(df),
        'Number of Syndicates': df['Syndicate Number'].nunique(),
        'Outstanding Claims Amount Beginning': df['Outstanding Claims Amount as at beginning of period'].sum(),
        'Paid to Date Amount': df['Paid to Date Amount'].sum(),
        'Paid in Year Amount': df['Paid in Year amount'].sum(),
        'Outstanding Claims Amount End': df['Outstanding Claim amount as at end of period'].sum(),
        'Total Incurred': df['Total Incurred as at end of period'].sum(),
        'Movement in Year': df['Movement in Year'].sum(),
        'Reserve Movement': df['Reserve Movement'].sum(),
        'Average Claim Size': df['Total Incurred as at end of period'].mean(),
        'Largest Single Claim': df['Total Incurred as at end of period'].max(),
        'Report Date': datetime.now().strftime('%Y-%m-%d')
    }

    return pd.DataFrame([summary_data])


# =============================================================================
# GENERATE ALL TABLES FOR POWER BI
# =============================================================================
print("Generating Solvency II Claims Data for Power BI...")
print("=" * 60)

# Generate base claims data
raw_claims = generate_synthetic_claims()

# Calculate derived amounts
claims_with_calcs = calculate_incurred_amounts(raw_claims)

# Generate all tables (these will be available in Power BI)
detailed_claims = claims_with_calcs
by_syndicate = aggregate_by_syndicate(claims_with_calcs)
by_risk_code = aggregate_by_risk_code(claims_with_calcs)
by_claim_status = aggregate_by_claim_status(claims_with_calcs)
summary = create_summary_report(claims_with_calcs)

print(f"detailed_claims: {len(detailed_claims)} records")
print(f"by_syndicate: {len(by_syndicate)} records")
print(f"by_risk_code: {len(by_risk_code)} records")
print(f"by_claim_status: {len(by_claim_status)} records")
print(f"summary: {len(summary)} records")
print("=" * 60)
print("Solvency II Claims data generated successfully!")
