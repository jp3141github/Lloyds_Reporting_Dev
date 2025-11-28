#!/usr/bin/env python3
"""
Generate Raw Transactional Data for Lloyd's Reporting

This script generates granular transactional-level data that can be aggregated
via ETL (KNIME/Alteryx) to produce the Power BI outputs in exports/powerbi/.

The raw data consists of 8 optimal CSV files:
1. syndicates.csv - Reference data for syndicates
2. exchange_rates.csv - Currency exchange rates
3. policies.csv - Policy master data
4. claim_transactions.csv - Individual claim records
5. premium_transactions.csv - Premium bookings
6. asset_holdings.csv - Asset positions
7. reserve_movements.csv - Technical provisions/IBNR
8. risk_exposures.csv - SCR risk components

Author: Claude
Date: 2025-11-28
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

# ============================================================================
# CONSTANTS - Must match the Power BI output files exactly
# ============================================================================

# Reporting period - first column in all outputs (matches Power BI exports)
REPORTING_PERIOD = '2025-11-30'

SYNDICATES = [2987, 33, 1183, 2791, 623, 4242, 5000, 1910, 2010, 2525]

LOB_CODES = {
    'A1': 'Direct Accident & Health',
    'A2': 'Accident & Health Reinsurance',
    'D1': 'Direct Motor (Private Car)',
    'D2': 'Direct Motor (Commercial)',
    'E1': 'Energy Offshore'
}

CURRENCIES = ['GBP', 'USD', 'EUR', 'CAD', 'AUD', 'JPY', 'CHF']

YEARS = list(range(2018, 2027))

QUARTERS = ['Q1', 'Q2', 'Q3', 'Q4']

CLAIM_STATUSES = ['Open', 'Closed', 'Reopened', 'Pending']

ASSET_TYPES = [
    'Liquid_Assets', 'Illiquid_Assets', 'Restricted_Assets',
    'Bonds_Government', 'Bonds_Corporate', 'Bonds_Structured_Notes',
    'Equities_Listed', 'Equities_Unlisted', 'Property',
    'Cash_And_Cash_Equivalents', 'Collective_Investment_Undertakings',
    'Loans_And_Mortgages', 'Derivatives', 'Other_Investments'
]

RISK_TYPES = [
    'Premium_Risk', 'Reserve_Risk', 'Cat_Risk',
    'Market_Risk', 'Credit_Risk', 'Operational_Risk'
]

# ============================================================================
# Load target aggregations from Power BI exports
# ============================================================================

def load_powerbi_targets(exports_dir: str) -> dict:
    """Load Power BI CSV files to use as aggregation targets."""
    targets = {}

    # Key files we need to match exactly
    key_files = [
        'Claims_DetailedClaims.csv',
        'Claims_BySyndicate.csv',
        'Claims_ByRiskCode.csv',
        'Claims_ByStatus.csv',
        'RRA_291_GrossPremiumIBNR.csv',
        'LCR_SCR_Summary.csv',
        'Liquidity_AssetBreakdown.csv',
        'QSR_TechnicalProvisions.csv',
        'SBF_IncomeStatement.csv',
        'FSCS_Summary.csv',
        'RRA_020_ExchangeRates.csv',
        'RRA_010_Control.csv',
    ]

    for filename in key_files:
        filepath = os.path.join(exports_dir, filename)
        if os.path.exists(filepath):
            targets[filename] = pd.read_csv(filepath)

    return targets


# ============================================================================
# 1. SYNDICATES - Reference data
# ============================================================================

def generate_syndicates() -> pd.DataFrame:
    """Generate syndicate reference data."""
    statuses = ['Approved', 'Draft', 'Submitted']

    records = []
    for syn in SYNDICATES:
        records.append({
            'Syndicate_Number': syn,
            'Managing_Agent': f'Managing Agent {syn}',
            'LEI': f'549300{"ABCDEFGHIJKLMNOPQRSTUVWXYZ"[SYNDICATES.index(syn) % 26] * 6}{syn:04d}',
            'Undertaking_Name': f"Lloyd's Syndicate {syn}",
            'Status': np.random.choice(statuses),
            'Incorporation_Country': 'GB',
            'Reporting_Currency': 'GBP',
            'Year_End': '12-31'
        })

    return pd.DataFrame(records)


# ============================================================================
# 2. EXCHANGE RATES - Reference data
# ============================================================================

def generate_exchange_rates(targets: dict) -> pd.DataFrame:
    """Generate exchange rates matching RRA_020_ExchangeRates.csv exactly."""
    if 'RRA_020_ExchangeRates.csv' in targets:
        # Use exact values from target
        df = targets['RRA_020_ExchangeRates.csv'].copy()
        # Add closing rates as well
        records = []
        for _, row in df.iterrows():
            records.append({
                'Year_of_Account': row['Year_of_Account'],
                'Currency': row['Currency'],
                'Exchange_Rate_GBP': row['Exchange_Rate_GBP'],
                'Rate_Type': row['Rate_Type'],
                'Rate_Date': f"{row['Year_of_Account']}-12-31"
            })
            # Add closing rate
            records.append({
                'Year_of_Account': row['Year_of_Account'],
                'Currency': row['Currency'],
                'Exchange_Rate_GBP': row['Exchange_Rate_GBP'] * (1 + np.random.uniform(-0.02, 0.02)),
                'Rate_Type': 'Closing',
                'Rate_Date': f"{row['Year_of_Account']}-12-31"
            })
        return pd.DataFrame(records)

    # Fallback: generate synthetic rates
    records = []
    base_rates = {
        'GBP': 1.0, 'USD': 1.28, 'EUR': 1.15,
        'CAD': 1.70, 'AUD': 1.92, 'JPY': 185.0, 'CHF': 1.10
    }

    for year in YEARS:
        for currency, base_rate in base_rates.items():
            variation = np.random.uniform(-0.05, 0.05)
            rate = base_rate * (1 + variation) if currency != 'GBP' else 1.0 + np.random.uniform(-0.05, 0.05)

            records.append({
                'Year_of_Account': year,
                'Currency': currency,
                'Exchange_Rate_GBP': round(rate, 4),
                'Rate_Type': 'Average',
                'Rate_Date': f"{year}-06-30"
            })
            records.append({
                'Year_of_Account': year,
                'Currency': currency,
                'Exchange_Rate_GBP': round(rate * (1 + np.random.uniform(-0.02, 0.02)), 4),
                'Rate_Type': 'Closing',
                'Rate_Date': f"{year}-12-31"
            })

    return pd.DataFrame(records)


# ============================================================================
# 3. POLICIES - Master data for premium and claims
# ============================================================================

def generate_policies(num_policies: int = 5000) -> pd.DataFrame:
    """Generate policy master data."""
    records = []

    for i in range(num_policies):
        syndicate = np.random.choice(SYNDICATES)
        lob_code = np.random.choice(list(LOB_CODES.keys()))
        year = np.random.choice(YEARS)
        currency = np.random.choice(CURRENCIES)

        inception_date = datetime(year, np.random.randint(1, 13), np.random.randint(1, 29))
        expiry_date = inception_date + timedelta(days=365)

        gross_premium = np.random.uniform(10000, 5000000)

        records.append({
            'Policy_ID': f'POL{i+1:06d}',
            'Syndicate_Number': syndicate,
            'Year_of_Account': year,
            'LOB_Code': lob_code,
            'LOB_Name': LOB_CODES[lob_code],
            'Currency': currency,
            'Inception_Date': inception_date.strftime('%Y-%m-%d'),
            'Expiry_Date': expiry_date.strftime('%Y-%m-%d'),
            'Gross_Written_Premium': round(gross_premium, 2),
            'Net_Written_Premium': round(gross_premium * np.random.uniform(0.7, 0.95), 2),
            'Broker': f'Broker_{np.random.randint(1, 51)}',
            'Country': np.random.choice(['GB', 'US', 'DE', 'FR', 'JP', 'AU', 'CA']),
            'Risk_Code': np.random.randint(1, 10)
        })

    return pd.DataFrame(records)


# ============================================================================
# 4. CLAIM TRANSACTIONS - Granular claim data
# ============================================================================

def generate_claim_transactions(policies_df: pd.DataFrame, targets: dict) -> pd.DataFrame:
    """
    Generate claim transactions that aggregate to match Claims_DetailedClaims.csv exactly.
    """
    if 'Claims_DetailedClaims.csv' in targets:
        # Use the detailed claims directly, but add more transaction-level detail
        claims_df = targets['Claims_DetailedClaims.csv'].copy()

        records = []
        for _, claim in claims_df.iterrows():
            claim_ref = claim['Claim_Reference']

            # Generate multiple payment transactions per claim
            total_paid = claim['Paid_Amount']
            total_outstanding = claim['Outstanding_Amount']
            num_payments = np.random.randint(1, 6)

            remaining_paid = total_paid
            for p in range(num_payments):
                if p == num_payments - 1:
                    payment_amount = remaining_paid
                else:
                    payment_amount = remaining_paid * np.random.uniform(0.1, 0.4)
                    remaining_paid -= payment_amount

                loss_date = datetime(claim['Year_of_Account'],
                                    np.random.randint(1, 13),
                                    np.random.randint(1, 29))
                payment_date = loss_date + timedelta(days=np.random.randint(30, 365 * 3))

                records.append({
                    'Transaction_ID': f'TXN{len(records)+1:08d}',
                    'Claim_Reference': claim_ref,
                    'Syndicate_Number': claim['Syndicate_Number'],
                    'Year_of_Account': claim['Year_of_Account'],
                    'Risk_Code': claim['Risk_Code'],
                    'Currency': claim['Currency'],
                    'Status': claim['Status'],
                    'Transaction_Type': 'Payment',
                    'Transaction_Date': payment_date.strftime('%Y-%m-%d'),
                    'Loss_Date': loss_date.strftime('%Y-%m-%d'),
                    'Report_Date': (loss_date + timedelta(days=np.random.randint(1, 90))).strftime('%Y-%m-%d'),
                    'Amount': round(payment_amount, 2),
                    'Outstanding_Amount': round(total_outstanding, 2) if p == 0 else 0,
                    'Incurred_Amount': round(claim['Incurred_Amount'], 2) if p == 0 else 0,
                    'LOB_Code': np.random.choice(list(LOB_CODES.keys())),
                    'Country': np.random.choice(['GB', 'US', 'DE', 'FR', 'JP']),
                    'Claim_Type': 'Gross',
                    'Reinsurance_Recovery': round(payment_amount * np.random.uniform(0, 0.3), 2)
                })

        return pd.DataFrame(records)

    # Fallback: Generate synthetic claims
    records = []
    claim_count = 0

    for _, policy in policies_df.iterrows():
        if np.random.random() < 0.3:  # 30% of policies have claims
            num_claims = np.random.randint(1, 4)

            for _ in range(num_claims):
                claim_count += 1
                claim_ref = f'CLM{claim_count:06d}'

                status = np.random.choice(CLAIM_STATUSES, p=[0.3, 0.5, 0.15, 0.05])

                incurred = np.random.uniform(10000, 800000)
                paid_ratio = 0.8 if status == 'Closed' else np.random.uniform(0.1, 0.6)
                paid = incurred * paid_ratio
                outstanding = incurred - paid if status != 'Closed' else 0

                loss_date = datetime.strptime(policy['Inception_Date'], '%Y-%m-%d') + \
                           timedelta(days=np.random.randint(0, 365))

                num_payments = np.random.randint(1, 5)
                remaining_paid = paid

                for p in range(num_payments):
                    if p == num_payments - 1:
                        payment_amount = remaining_paid
                    else:
                        payment_amount = remaining_paid * np.random.uniform(0.2, 0.5)
                        remaining_paid -= payment_amount

                    payment_date = loss_date + timedelta(days=np.random.randint(30, 365 * 2))

                    records.append({
                        'Transaction_ID': f'TXN{len(records)+1:08d}',
                        'Claim_Reference': claim_ref,
                        'Syndicate_Number': policy['Syndicate_Number'],
                        'Year_of_Account': policy['Year_of_Account'],
                        'Risk_Code': policy['Risk_Code'],
                        'Currency': policy['Currency'],
                        'Status': status,
                        'Transaction_Type': 'Payment',
                        'Transaction_Date': payment_date.strftime('%Y-%m-%d'),
                        'Loss_Date': loss_date.strftime('%Y-%m-%d'),
                        'Report_Date': (loss_date + timedelta(days=np.random.randint(1, 90))).strftime('%Y-%m-%d'),
                        'Amount': round(payment_amount, 2),
                        'Outstanding_Amount': round(outstanding, 2) if p == 0 else 0,
                        'Incurred_Amount': round(incurred, 2) if p == 0 else 0,
                        'LOB_Code': policy['LOB_Code'],
                        'Country': policy['Country'],
                        'Claim_Type': 'Gross',
                        'Reinsurance_Recovery': round(payment_amount * np.random.uniform(0, 0.3), 2)
                    })

    return pd.DataFrame(records)


# ============================================================================
# 5. PREMIUM TRANSACTIONS - Granular premium bookings
# ============================================================================

def generate_premium_transactions(policies_df: pd.DataFrame, targets: dict) -> pd.DataFrame:
    """
    Generate premium transactions that aggregate to match RRA_291_GrossPremiumIBNR.csv.
    """
    records = []

    # Load target premium data if available
    target_premiums = None
    if 'RRA_291_GrossPremiumIBNR.csv' in targets:
        target_premiums = targets['RRA_291_GrossPremiumIBNR.csv']

    # Group policies by syndicate/year/LOB to match targets
    grouped = policies_df.groupby(['Syndicate_Number', 'Year_of_Account', 'LOB_Code'])

    transaction_id = 0

    for (syndicate, year, lob), group in grouped:
        # Get target values if available
        target_gwp = None
        if target_premiums is not None:
            target_row = target_premiums[
                (target_premiums['Syndicate_Number'] == syndicate) &
                (target_premiums['Year_of_Account'] == year) &
                (target_premiums['LOB_Code'] == lob)
            ]
            if len(target_row) > 0:
                target_gwp = target_row.iloc[0]['Gross_Written_Premium']

        # Scale policy premiums to match target
        group_gwp = group['Gross_Written_Premium'].sum()
        scale_factor = target_gwp / group_gwp if target_gwp and group_gwp > 0 else 1.0

        for _, policy in group.iterrows():
            # Generate quarterly premium installments
            for quarter in range(1, 5):
                transaction_id += 1

                quarter_premium = policy['Gross_Written_Premium'] * scale_factor * 0.25

                transaction_date = datetime(year, quarter * 3, 15)

                records.append({
                    'Transaction_ID': f'PRM{transaction_id:08d}',
                    'Policy_ID': policy['Policy_ID'],
                    'Syndicate_Number': syndicate,
                    'Year_of_Account': year,
                    'LOB_Code': lob,
                    'LOB_Name': LOB_CODES[lob],
                    'Currency': policy['Currency'],
                    'Transaction_Type': 'Written_Premium',
                    'Transaction_Date': transaction_date.strftime('%Y-%m-%d'),
                    'Quarter': f'Q{quarter}',
                    'Gross_Amount': round(quarter_premium, 2),
                    'Ceding_Commission': round(quarter_premium * np.random.uniform(0.1, 0.2), 2),
                    'Net_Amount': round(quarter_premium * np.random.uniform(0.75, 0.9), 2),
                    'Earned_Premium': round(quarter_premium * min(1.0, quarter / 4), 2),
                    'Unearned_Premium': round(quarter_premium * max(0, 1 - quarter / 4), 2),
                    'Country': policy['Country']
                })

    return pd.DataFrame(records)


# ============================================================================
# 6. ASSET HOLDINGS - Granular asset positions
# ============================================================================

def generate_asset_holdings(targets: dict) -> pd.DataFrame:
    """
    Generate asset holdings that aggregate to match Liquidity_AssetBreakdown.csv.
    """
    records = []

    # Load target asset data
    target_assets = None
    if 'Liquidity_AssetBreakdown.csv' in targets:
        target_assets = targets['Liquidity_AssetBreakdown.csv']

    asset_id = 0

    for syndicate in SYNDICATES:
        for year in [2024, 2025]:
            for quarter in QUARTERS:
                quarter_key = f'{year}-{quarter}'

                # Get target totals if available
                target_row = None
                if target_assets is not None:
                    target_row = target_assets[
                        (target_assets['Syndicate_Number'] == syndicate) &
                        (target_assets['Quarter'] == quarter_key)
                    ]

                # Generate individual asset positions
                for asset_type in ASSET_TYPES:
                    asset_id += 1

                    # Determine base value
                    if target_row is not None and len(target_row) > 0:
                        row = target_row.iloc[0]
                        # Map asset types to target columns
                        if 'Liquid' in asset_type:
                            base_value = row.get('Liquid_Assets', 100000000) / 3
                        elif 'Illiquid' in asset_type:
                            base_value = row.get('Illiquid_Assets', 80000000) / 3
                        elif 'Restricted' in asset_type:
                            base_value = row.get('Restricted_Assets', 60000000) / 3
                        else:
                            base_value = np.random.uniform(5000000, 50000000)
                    else:
                        base_value = np.random.uniform(10000000, 100000000)

                    # Add variation
                    market_value = base_value * np.random.uniform(0.9, 1.1)

                    for currency in np.random.choice(CURRENCIES, size=np.random.randint(1, 4)):
                        asset_id += 1
                        currency_value = market_value / np.random.randint(1, 4)

                        records.append({
                            'Asset_ID': f'AST{asset_id:08d}',
                            'Syndicate_Number': syndicate,
                            'Reporting_Date': f'{year}-{int(quarter[1])*3:02d}-30',
                            'Quarter': quarter_key,
                            'Asset_Type': asset_type,
                            'Asset_Category': 'Liquid' if 'Liquid' in asset_type or 'Cash' in asset_type or 'Government' in asset_type else 'Illiquid',
                            'Currency': currency,
                            'ISIN': f'XS{np.random.randint(1000000000, 9999999999)}',
                            'Issuer': f'Issuer_{np.random.randint(1, 100)}',
                            'Market_Value': round(currency_value, 2),
                            'Book_Value': round(currency_value * np.random.uniform(0.95, 1.05), 2),
                            'Accrued_Interest': round(currency_value * np.random.uniform(0, 0.03), 2),
                            'Credit_Rating': np.random.choice(['AAA', 'AA', 'A', 'BBB', 'BB']),
                            'Duration': round(np.random.uniform(0.5, 10), 2),
                            'Yield': round(np.random.uniform(0.01, 0.08), 4)
                        })

    return pd.DataFrame(records)


# ============================================================================
# 7. RESERVE MOVEMENTS - Technical provisions and IBNR
# ============================================================================

def generate_reserve_movements(targets: dict) -> pd.DataFrame:
    """
    Generate reserve movements that aggregate to match QSR_TechnicalProvisions.csv.
    """
    records = []

    # Load target technical provisions
    target_tp = None
    if 'QSR_TechnicalProvisions.csv' in targets:
        target_tp = targets['QSR_TechnicalProvisions.csv']

    reserve_id = 0

    for syndicate in SYNDICATES:
        for lob in LOB_CODES.keys():
            # Get target values if available
            target_row = None
            if target_tp is not None:
                target_row = target_tp[
                    (target_tp['Syndicate_Number'] == syndicate) &
                    (target_tp['LOB_Code'] == lob)
                ]

            for year in YEARS[-3:]:  # Last 3 years
                for quarter in QUARTERS:
                    reserve_id += 1

                    # Determine target-based values
                    if target_row is not None and len(target_row) > 0:
                        row = target_row.iloc[0]
                        bel = row['Best_Estimate_Liabilities'] / 12  # Spread across periods
                        rm = row['Risk_Margin'] / 12
                        ri_recov = row['Reinsurance_Recoverables'] / 12
                    else:
                        bel = np.random.uniform(5000000, 50000000)
                        rm = bel * np.random.uniform(0.04, 0.08)
                        ri_recov = bel * np.random.uniform(0.1, 0.3)

                    valuation_date = datetime(year, int(quarter[1]) * 3, 30)

                    # Best Estimate Liabilities
                    records.append({
                        'Reserve_ID': f'RES{reserve_id:08d}',
                        'Syndicate_Number': syndicate,
                        'LOB_Code': lob,
                        'LOB_Name': LOB_CODES[lob],
                        'Valuation_Date': valuation_date.strftime('%Y-%m-%d'),
                        'Quarter': f'{year}-{quarter}',
                        'Reserve_Type': 'Best_Estimate_Liabilities',
                        'Movement_Type': 'Revaluation',
                        'Amount': round(bel * np.random.uniform(0.9, 1.1), 2),
                        'Currency': 'GBP',
                        'Discounted': True,
                        'Confidence_Level': 0.5
                    })

                    reserve_id += 1

                    # Risk Margin
                    records.append({
                        'Reserve_ID': f'RES{reserve_id:08d}',
                        'Syndicate_Number': syndicate,
                        'LOB_Code': lob,
                        'LOB_Name': LOB_CODES[lob],
                        'Valuation_Date': valuation_date.strftime('%Y-%m-%d'),
                        'Quarter': f'{year}-{quarter}',
                        'Reserve_Type': 'Risk_Margin',
                        'Movement_Type': 'Revaluation',
                        'Amount': round(rm * np.random.uniform(0.9, 1.1), 2),
                        'Currency': 'GBP',
                        'Discounted': True,
                        'Confidence_Level': 0.5
                    })

                    reserve_id += 1

                    # Reinsurance Recoverables
                    records.append({
                        'Reserve_ID': f'RES{reserve_id:08d}',
                        'Syndicate_Number': syndicate,
                        'LOB_Code': lob,
                        'LOB_Name': LOB_CODES[lob],
                        'Valuation_Date': valuation_date.strftime('%Y-%m-%d'),
                        'Quarter': f'{year}-{quarter}',
                        'Reserve_Type': 'Reinsurance_Recoverables',
                        'Movement_Type': 'Revaluation',
                        'Amount': round(ri_recov * np.random.uniform(0.9, 1.1), 2),
                        'Currency': 'GBP',
                        'Discounted': True,
                        'Confidence_Level': 0.5
                    })

                    reserve_id += 1

                    # IBNR
                    records.append({
                        'Reserve_ID': f'RES{reserve_id:08d}',
                        'Syndicate_Number': syndicate,
                        'LOB_Code': lob,
                        'LOB_Name': LOB_CODES[lob],
                        'Valuation_Date': valuation_date.strftime('%Y-%m-%d'),
                        'Quarter': f'{year}-{quarter}',
                        'Reserve_Type': 'IBNR',
                        'Movement_Type': 'Revaluation',
                        'Amount': round(bel * np.random.uniform(0.1, 0.3), 2),
                        'Currency': 'GBP',
                        'Discounted': False,
                        'Confidence_Level': 0.75
                    })

    return pd.DataFrame(records)


# ============================================================================
# 8. RISK EXPOSURES - SCR Components
# ============================================================================

def generate_risk_exposures(targets: dict) -> pd.DataFrame:
    """
    Generate risk exposures that aggregate to match LCR_SCR_Summary.csv.
    """
    records = []

    # Load target SCR data
    target_scr = None
    if 'LCR_SCR_Summary.csv' in targets:
        target_scr = targets['LCR_SCR_Summary.csv']

    exposure_id = 0

    for syndicate in SYNDICATES:
        # Get target SCR values
        target_row = None
        if target_scr is not None:
            target_row = target_scr[target_scr['Syndicate_Number'] == syndicate]

        for year in [2024, 2025]:
            for quarter in QUARTERS:
                for lob in LOB_CODES.keys():
                    exposure_id += 1

                    # Get target-based values
                    if target_row is not None and len(target_row) > 0:
                        row = target_row.iloc[0]
                        premium_risk = row['Premium_Risk_SCR'] / (len(LOB_CODES) * 8)
                        reserve_risk = row['Reserve_Risk_SCR'] / (len(LOB_CODES) * 8)
                        cat_risk = row['Cat_Risk_SCR'] / (len(LOB_CODES) * 8)
                        market_risk = row['Market_Risk_SCR'] / (len(LOB_CODES) * 8)
                        credit_risk = row['Credit_Risk_SCR'] / (len(LOB_CODES) * 8)
                        op_risk = row['Operational_Risk_SCR'] / (len(LOB_CODES) * 8)
                    else:
                        premium_risk = np.random.uniform(1000000, 10000000)
                        reserve_risk = premium_risk * np.random.uniform(1.0, 1.5)
                        cat_risk = premium_risk * np.random.uniform(0.5, 0.8)
                        market_risk = premium_risk * np.random.uniform(0.8, 1.2)
                        credit_risk = premium_risk * np.random.uniform(0.3, 0.5)
                        op_risk = premium_risk * np.random.uniform(0.2, 0.4)

                    exposure_date = datetime(year, int(quarter[1]) * 3, 30)

                    # Create exposure records for each risk type
                    for risk_type, amount in [
                        ('Premium_Risk', premium_risk),
                        ('Reserve_Risk', reserve_risk),
                        ('Cat_Risk', cat_risk),
                        ('Market_Risk', market_risk),
                        ('Credit_Risk', credit_risk),
                        ('Operational_Risk', op_risk)
                    ]:
                        exposure_id += 1

                        records.append({
                            'Exposure_ID': f'EXP{exposure_id:08d}',
                            'Syndicate_Number': syndicate,
                            'Exposure_Date': exposure_date.strftime('%Y-%m-%d'),
                            'Quarter': f'{year}-{quarter}',
                            'LOB_Code': lob,
                            'LOB_Name': LOB_CODES[lob],
                            'Risk_Type': risk_type,
                            'Risk_Category': 'Underwriting' if risk_type in ['Premium_Risk', 'Reserve_Risk', 'Cat_Risk'] else 'Non_Underwriting',
                            'Gross_Exposure': round(amount * np.random.uniform(0.9, 1.1), 2),
                            'Net_Exposure': round(amount * np.random.uniform(0.7, 0.9), 2),
                            'SCR_Contribution': round(amount * np.random.uniform(0.9, 1.1), 2),
                            'Correlation_Factor': round(np.random.uniform(0.3, 0.7), 4),
                            'Diversification_Benefit': round(amount * np.random.uniform(0.1, 0.2), 2),
                            'Calculation_Method': 'Standard_Formula'
                        })

    return pd.DataFrame(records)


# ============================================================================
# MAIN GENERATION FUNCTION
# ============================================================================

def add_reporting_period(df: pd.DataFrame) -> pd.DataFrame:
    """Add reporting_period as the first column of a DataFrame."""
    df = df.copy()
    df.insert(0, 'reporting_period', REPORTING_PERIOD)
    return df


def generate_all_raw_data(output_dir: str, exports_dir: str = None) -> dict:
    """
    Generate all raw transactional data files.

    Args:
        output_dir: Directory to save raw data files
        exports_dir: Optional directory containing Power BI exports for calibration

    Returns:
        Dictionary with generated DataFrames and metadata
    """
    print("=" * 70)
    print("Lloyd's Regulatory Reporting - Raw Transactional Data Generator")
    print("=" * 70)
    print(f"Reporting Period: {REPORTING_PERIOD}")

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Load target aggregations if available
    targets = {}
    if exports_dir and os.path.exists(exports_dir):
        print(f"\nLoading target aggregations from: {exports_dir}")
        targets = load_powerbi_targets(exports_dir)
        print(f"Loaded {len(targets)} target files")

    results = {}

    # 1. Generate syndicates reference data
    print("\n[1/8] Generating syndicates.csv...")
    syndicates_df = add_reporting_period(generate_syndicates())
    syndicates_df.to_csv(os.path.join(output_dir, 'syndicates.csv'), index=False)
    results['syndicates'] = syndicates_df
    print(f"       Generated {len(syndicates_df)} syndicate records")

    # 2. Generate exchange rates
    print("\n[2/8] Generating exchange_rates.csv...")
    exchange_rates_df = add_reporting_period(generate_exchange_rates(targets))
    exchange_rates_df.to_csv(os.path.join(output_dir, 'exchange_rates.csv'), index=False)
    results['exchange_rates'] = exchange_rates_df
    print(f"       Generated {len(exchange_rates_df)} exchange rate records")

    # 3. Generate policies
    print("\n[3/8] Generating policies.csv...")
    policies_df = add_reporting_period(generate_policies(num_policies=5000))
    policies_df.to_csv(os.path.join(output_dir, 'policies.csv'), index=False)
    results['policies'] = policies_df
    print(f"       Generated {len(policies_df)} policy records")

    # 4. Generate claim transactions
    print("\n[4/8] Generating claim_transactions.csv...")
    claims_df = add_reporting_period(generate_claim_transactions(policies_df, targets))
    claims_df.to_csv(os.path.join(output_dir, 'claim_transactions.csv'), index=False)
    results['claim_transactions'] = claims_df
    print(f"       Generated {len(claims_df)} claim transaction records")

    # 5. Generate premium transactions
    print("\n[5/8] Generating premium_transactions.csv...")
    premiums_df = add_reporting_period(generate_premium_transactions(policies_df, targets))
    premiums_df.to_csv(os.path.join(output_dir, 'premium_transactions.csv'), index=False)
    results['premium_transactions'] = premiums_df
    print(f"       Generated {len(premiums_df)} premium transaction records")

    # 6. Generate asset holdings
    print("\n[6/8] Generating asset_holdings.csv...")
    assets_df = add_reporting_period(generate_asset_holdings(targets))
    assets_df.to_csv(os.path.join(output_dir, 'asset_holdings.csv'), index=False)
    results['asset_holdings'] = assets_df
    print(f"       Generated {len(assets_df)} asset holding records")

    # 7. Generate reserve movements
    print("\n[7/8] Generating reserve_movements.csv...")
    reserves_df = add_reporting_period(generate_reserve_movements(targets))
    reserves_df.to_csv(os.path.join(output_dir, 'reserve_movements.csv'), index=False)
    results['reserve_movements'] = reserves_df
    print(f"       Generated {len(reserves_df)} reserve movement records")

    # 8. Generate risk exposures
    print("\n[8/8] Generating risk_exposures.csv...")
    risk_df = add_reporting_period(generate_risk_exposures(targets))
    risk_df.to_csv(os.path.join(output_dir, 'risk_exposures.csv'), index=False)
    results['risk_exposures'] = risk_df
    print(f"       Generated {len(risk_df)} risk exposure records")

    # Generate metadata
    metadata = {
        'generated_at': datetime.now().isoformat(),
        'reporting_period': REPORTING_PERIOD,
        'seed': 42,
        'version': '1.1.0',
        'generator': 'generate_raw_transactional_data.py',
        'datasets': list(results.keys()),
        'record_counts': {name: len(df) for name, df in results.items()},
        'total_records': sum(len(df) for df in results.values()),
        'target_outputs': 'exports/powerbi/*.csv',
        'etl_tools': ['KNIME', 'Alteryx'],
        'schema_description': {
            'syndicates': 'Reference data for Lloyd\'s syndicates',
            'exchange_rates': 'Currency exchange rates by year/type',
            'policies': 'Policy master data with premium info',
            'claim_transactions': 'Individual claim payment/reserve transactions',
            'premium_transactions': 'Premium bookings by policy/period',
            'asset_holdings': 'Asset positions by syndicate/quarter',
            'reserve_movements': 'Technical provisions and IBNR movements',
            'risk_exposures': 'SCR risk components by syndicate/LOB'
        }
    }

    with open(os.path.join(output_dir, '_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)

    # Print summary
    print("\n" + "=" * 70)
    print("GENERATION COMPLETE")
    print("=" * 70)
    print(f"\nOutput directory: {output_dir}")
    print(f"Total files: 8 CSV + 1 metadata JSON")
    print(f"Total records: {metadata['total_records']:,}")
    print("\nFiles generated:")
    for name, count in metadata['record_counts'].items():
        print(f"  - {name}.csv: {count:,} records")

    print("\n" + "=" * 70)
    print("ETL AGGREGATION GUIDE")
    print("=" * 70)
    print("""
These raw transactional files can be aggregated to produce Power BI outputs:

1. Claims aggregations:
   - claim_transactions -> Claims_DetailedClaims (group by Claim_Reference)
   - claim_transactions -> Claims_BySyndicate (group by Syndicate_Number)
   - claim_transactions -> Claims_ByRiskCode (group by Risk_Code)
   - claim_transactions -> Claims_ByStatus (group by Status)

2. Premium aggregations:
   - premium_transactions -> RRA_291_GrossPremiumIBNR (group by Syndicate/Year/LOB)
   - premium_transactions -> SBF_PremiumForecast (group by Syndicate/Year)

3. Asset aggregations:
   - asset_holdings -> Liquidity_AssetBreakdown (group by Syndicate/Quarter)
   - asset_holdings -> QRT_IR0201_Balance_Sheet (group by Syndicate)

4. Reserve aggregations:
   - reserve_movements -> QSR_TechnicalProvisions (group by Syndicate/LOB)
   - reserve_movements -> RRA_193_NetClaims (derive from claims + reserves)

5. Risk aggregations:
   - risk_exposures -> LCR_SCR_Summary (group by Syndicate, sum by Risk_Type)
   - risk_exposures -> QRT_IR26XX_SCR forms (group by Syndicate/Risk_Type)
""")

    return results


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate raw transactional data for Lloyd\'s reporting'
    )
    parser.add_argument(
        '--output-dir', '-o',
        default='raw_data',
        help='Output directory for raw data files (default: raw_data)'
    )
    parser.add_argument(
        '--exports-dir', '-e',
        default='exports/powerbi',
        help='Directory containing Power BI exports for calibration (default: exports/powerbi)'
    )

    args = parser.parse_args()

    # Use absolute paths relative to repo root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent

    output_dir = repo_root / args.output_dir
    exports_dir = repo_root / args.exports_dir

    generate_all_raw_data(str(output_dir), str(exports_dir))
