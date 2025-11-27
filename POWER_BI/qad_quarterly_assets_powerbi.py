# Quarterly Asset Data (QAD) - Power BI Data Generator
# Quarterly Asset Look-Through for Solvency II Reporting
#
# QAD complements QSR by providing detailed investment risk information
# Key features:
# - Quarterly granular asset portfolio details
# - Asset look-through for collective investments
# - Currency breakdown
# - Credit quality analysis
# - Duration and maturity analysis
# - Supports market/credit risk assessment and ALM
#
# Submitted quarterly alongside QSR
#
# Usage in Power BI:
# 1. Get Data > More > Other > Python script
# 2. Paste this entire file
# 3. Select tables from navigator
# 4. Load

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# Configuration
SYNDICATES = [33, 623, 1183, 1910, 2010, 2525, 2791, 2987, 4242, 5000]
REPORTING_YEAR = 2024
QUARTERS = ['Q1', 'Q2', 'Q3', 'Q4']
QUARTER_ENDS = {
    'Q1': datetime(2024, 3, 31),
    'Q2': datetime(2024, 6, 30),
    'Q3': datetime(2024, 9, 30),
    'Q4': datetime(2024, 12, 31)
}
CURRENCY = 'GBP'

# CIC codes (Complementary Identification Code) for asset classification
CIC_CODES = [
    ('11', 'Government bonds - Central government'),
    ('12', 'Government bonds - Regional/local'),
    ('13', 'Government bonds - Supranational'),
    ('21', 'Corporate bonds - Investment grade'),
    ('22', 'Corporate bonds - High yield'),
    ('31', 'Equity - Listed'),
    ('32', 'Equity - Unlisted'),
    ('41', 'Collective investments - Equity funds'),
    ('42', 'Collective investments - Debt funds'),
    ('43', 'Collective investments - Money market funds'),
    ('44', 'Collective investments - Asset allocation funds'),
    ('45', 'Collective investments - Real estate funds'),
    ('51', 'Structured notes'),
    ('61', 'Collateralised securities'),
    ('71', 'Cash and deposits'),
    ('72', 'Deposits other than cash'),
    ('81', 'Mortgages and loans'),
    ('91', 'Property - Office'),
    ('92', 'Property - Commercial'),
    ('93', 'Property - Residential')
]

# Credit Quality Steps (CQS) - Solvency II credit rating mapping
CQS_RATINGS = [
    (0, 'AAA'),
    (1, 'AA'),
    (2, 'A'),
    (3, 'BBB'),
    (4, 'BB'),
    (5, 'B'),
    (6, 'CCC or below'),
    (7, 'Not rated')
]

# Currencies for FX exposure
CURRENCIES = ['GBP', 'USD', 'EUR', 'CAD', 'AUD', 'JPY', 'CHF']

# Countries for geographic exposure
COUNTRIES = [
    ('GB', 'United Kingdom'),
    ('US', 'United States'),
    ('DE', 'Germany'),
    ('FR', 'France'),
    ('JP', 'Japan'),
    ('CA', 'Canada'),
    ('AU', 'Australia'),
    ('CH', 'Switzerland'),
    ('NL', 'Netherlands'),
    ('IE', 'Ireland')
]

# =============================================================================
# QAD_001_Control - Submission metadata
# =============================================================================
def generate_qad_001_control():
    records = []
    for syn in SYNDICATES:
        for quarter in QUARTERS:
            quarter_end = QUARTER_ENDS[quarter]
            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Quarter': quarter,
                'QuarterEnd': quarter_end,
                'SubmissionDeadline': quarter_end + timedelta(days=42),
                'SubmissionDate': quarter_end + timedelta(days=np.random.randint(35, 42)),
                'ManagingAgent': f'MA{syn % 100:03d}',
                'ReportType': 'QAD',
                'ReturnVersion': '2024.1',
                'Status': 'Final',
                'TotalAssets_GBP_M': round(np.random.uniform(300, 900), 2),
                'Currency': CURRENCY
            })
    return pd.DataFrame(records)

# =============================================================================
# QAD_010_Asset_Summary - High-level asset summary
# =============================================================================
def generate_qad_010_asset_summary():
    records = []
    for syn in SYNDICATES:
        base_assets = np.random.uniform(300, 900)

        for q_idx, quarter in enumerate(QUARTERS):
            # Assets grow through year
            growth = 1 + (q_idx * 0.03) + np.random.uniform(-0.02, 0.04)
            total_assets = base_assets * growth

            # High-level breakdown
            fixed_income = total_assets * np.random.uniform(0.65, 0.80)
            equities = total_assets * np.random.uniform(0.03, 0.08)
            collective_inv = total_assets * np.random.uniform(0.05, 0.12)
            cash = total_assets * np.random.uniform(0.08, 0.15)
            property_assets = total_assets * np.random.uniform(0.01, 0.04)
            other = total_assets - fixed_income - equities - collective_inv - cash - property_assets

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Quarter': quarter,
                'QuarterEnd': QUARTER_ENDS[quarter],
                'Total_Assets_GBP_M': round(total_assets, 2),
                'Fixed_Income_GBP_M': round(fixed_income, 2),
                'Equities_GBP_M': round(equities, 2),
                'Collective_Investments_GBP_M': round(collective_inv, 2),
                'Cash_Deposits_GBP_M': round(cash, 2),
                'Property_GBP_M': round(property_assets, 2),
                'Other_Assets_GBP_M': round(other, 2),
                # Allocation percentages
                'Fixed_Income_Pct': round((fixed_income / total_assets) * 100, 1),
                'Equities_Pct': round((equities / total_assets) * 100, 1),
                'Collective_Inv_Pct': round((collective_inv / total_assets) * 100, 1),
                'Cash_Pct': round((cash / total_assets) * 100, 1),
                'Currency': CURRENCY
            })
    return pd.DataFrame(records)

# =============================================================================
# QAD_020_Asset_By_CIC - Detailed breakdown by CIC code
# =============================================================================
def generate_qad_020_asset_by_cic():
    records = []

    # Base allocation weights by CIC category
    base_weights = {
        '11': 0.25, '12': 0.05, '13': 0.03,  # Government bonds
        '21': 0.25, '22': 0.05,              # Corporate bonds
        '31': 0.03, '32': 0.01,              # Equities
        '41': 0.02, '42': 0.03, '43': 0.05, '44': 0.02, '45': 0.01,  # Collective inv
        '51': 0.02, '61': 0.01,              # Structured/collateralised
        '71': 0.10, '72': 0.02,              # Cash and deposits
        '81': 0.02,                          # Mortgages and loans
        '91': 0.01, '92': 0.01, '93': 0.01   # Property
    }

    for syn in SYNDICATES:
        total_assets = np.random.uniform(300, 900)

        for quarter in QUARTERS:
            q_factor = 1 + (QUARTERS.index(quarter) * 0.03)

            for cic_code, cic_name in CIC_CODES:
                weight = base_weights.get(cic_code, 0.01) * np.random.uniform(0.7, 1.3)
                market_value = total_assets * q_factor * weight

                if market_value < 0.5:  # Skip very small allocations
                    continue

                # Calculate additional metrics based on asset type
                if cic_code.startswith('1') or cic_code.startswith('2'):  # Bonds
                    duration = np.random.uniform(2, 8)
                    yield_rate = np.random.uniform(0.02, 0.06)
                    cqs = np.random.choice([0, 1, 2, 3], p=[0.2, 0.4, 0.3, 0.1])
                elif cic_code.startswith('7'):  # Cash
                    duration = 0
                    yield_rate = np.random.uniform(0.01, 0.03)
                    cqs = 0
                else:
                    duration = 0
                    yield_rate = np.random.uniform(0.03, 0.08)
                    cqs = 7  # Not rated

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'CIC_Code': cic_code,
                    'CIC_Name': cic_name,
                    'Market_Value_GBP_M': round(market_value, 2),
                    'Book_Value_GBP_M': round(market_value * np.random.uniform(0.95, 1.05), 2),
                    'Accrued_Interest_GBP_M': round(market_value * np.random.uniform(0, 0.02), 2),
                    'Duration_Years': round(duration, 2) if duration > 0 else None,
                    'Yield_Pct': round(yield_rate * 100, 2),
                    'CQS': cqs,
                    'Allocation_Pct': round(weight * 100, 2),
                    'Currency': CURRENCY
                })
    return pd.DataFrame(records)

# =============================================================================
# QAD_030_Credit_Quality - Credit quality breakdown
# =============================================================================
def generate_qad_030_credit_quality():
    records = []

    for syn in SYNDICATES:
        total_fixed_income = np.random.uniform(200, 600)

        for quarter in QUARTERS:
            q_factor = 1 + (QUARTERS.index(quarter) * 0.03)

            # Credit quality distribution (investment grade focused)
            cqs_weights = [0.15, 0.35, 0.30, 0.12, 0.04, 0.02, 0.01, 0.01]

            for cqs, rating in CQS_RATINGS:
                weight = cqs_weights[cqs] * np.random.uniform(0.8, 1.2)
                market_value = total_fixed_income * q_factor * weight

                if market_value < 0.1:
                    continue

                # Risk charge factor (higher for lower quality)
                risk_charge_factor = [0.0, 0.009, 0.011, 0.014, 0.023, 0.039, 0.05, 0.03][cqs]

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'CQS': cqs,
                    'Rating_Description': rating,
                    'Market_Value_GBP_M': round(market_value, 2),
                    'Allocation_Pct': round(weight * 100, 1),
                    'Spread_Risk_Factor_Pct': round(risk_charge_factor * 100, 2),
                    'Spread_Risk_Charge_GBP_M': round(market_value * risk_charge_factor, 2),
                    'Avg_Duration_Years': round(np.random.uniform(2, 6), 1),
                    'Currency': CURRENCY
                })
    return pd.DataFrame(records)

# =============================================================================
# QAD_040_Currency_Exposure - FX exposure breakdown
# =============================================================================
def generate_qad_040_currency_exposure():
    records = []

    # Base currency weights
    base_fx_weights = {'GBP': 0.45, 'USD': 0.35, 'EUR': 0.12, 'CAD': 0.03,
                       'AUD': 0.02, 'JPY': 0.02, 'CHF': 0.01}

    for syn in SYNDICATES:
        total_assets = np.random.uniform(300, 900)

        for quarter in QUARTERS:
            q_factor = 1 + (QUARTERS.index(quarter) * 0.03)

            for currency in CURRENCIES:
                weight = base_fx_weights.get(currency, 0.01) * np.random.uniform(0.8, 1.2)
                asset_value = total_assets * q_factor * weight

                if asset_value < 0.5:
                    continue

                # Liability currency match
                liability_value = asset_value * np.random.uniform(0.7, 1.1)
                net_exposure = asset_value - liability_value

                # FX hedge percentage
                if currency != 'GBP':
                    hedge_pct = np.random.uniform(0.5, 0.95)
                else:
                    hedge_pct = 0

                hedged_exposure = net_exposure * (1 - hedge_pct)

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'Currency_Code': currency,
                    'Assets_Original_CCY_M': round(asset_value * np.random.uniform(0.8, 1.5), 2),
                    'Assets_GBP_M': round(asset_value, 2),
                    'Liabilities_GBP_M': round(liability_value, 2),
                    'Net_Exposure_GBP_M': round(net_exposure, 2),
                    'Hedge_Pct': round(hedge_pct * 100, 1),
                    'Hedged_Net_Exposure_GBP_M': round(hedged_exposure, 2),
                    'Allocation_Pct': round(weight * 100, 1),
                    'Base_Currency': CURRENCY
                })
    return pd.DataFrame(records)

# =============================================================================
# QAD_050_Duration_Analysis - Duration and maturity profile
# =============================================================================
def generate_qad_050_duration_analysis():
    records = []

    maturity_buckets = [
        ('0-1Y', '0-1 Years', 0.20),
        ('1-3Y', '1-3 Years', 0.30),
        ('3-5Y', '3-5 Years', 0.25),
        ('5-7Y', '5-7 Years', 0.15),
        ('7-10Y', '7-10 Years', 0.07),
        ('10Y+', '10+ Years', 0.03)
    ]

    for syn in SYNDICATES:
        total_fixed_income = np.random.uniform(200, 600)

        for quarter in QUARTERS:
            q_factor = 1 + (QUARTERS.index(quarter) * 0.03)

            for bucket_code, bucket_name, base_weight in maturity_buckets:
                weight = base_weight * np.random.uniform(0.8, 1.2)
                market_value = total_fixed_income * q_factor * weight

                # Duration based on bucket
                if bucket_code == '0-1Y':
                    duration = np.random.uniform(0.3, 0.8)
                elif bucket_code == '1-3Y':
                    duration = np.random.uniform(1.5, 2.5)
                elif bucket_code == '3-5Y':
                    duration = np.random.uniform(3.5, 4.5)
                elif bucket_code == '5-7Y':
                    duration = np.random.uniform(5.5, 6.5)
                elif bucket_code == '7-10Y':
                    duration = np.random.uniform(7.5, 9)
                else:
                    duration = np.random.uniform(10, 15)

                # Interest rate sensitivity
                ir_sensitivity = market_value * duration * 0.01  # 1% rate change

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'Maturity_Bucket': bucket_code,
                    'Maturity_Description': bucket_name,
                    'Market_Value_GBP_M': round(market_value, 2),
                    'Modified_Duration': round(duration, 2),
                    'Contribution_To_Portfolio_Duration': round(duration * weight, 3),
                    'IR_Sensitivity_100bp_GBP_M': round(ir_sensitivity, 2),
                    'Allocation_Pct': round(weight * 100, 1),
                    'Currency': CURRENCY
                })
    return pd.DataFrame(records)

# =============================================================================
# QAD_060_Geographic_Exposure - Country exposure
# =============================================================================
def generate_qad_060_geographic_exposure():
    records = []

    # Base country weights
    base_country_weights = {
        'GB': 0.35, 'US': 0.30, 'DE': 0.08, 'FR': 0.06, 'JP': 0.05,
        'CA': 0.04, 'AU': 0.04, 'CH': 0.03, 'NL': 0.03, 'IE': 0.02
    }

    for syn in SYNDICATES:
        total_assets = np.random.uniform(300, 900)

        for quarter in QUARTERS:
            q_factor = 1 + (QUARTERS.index(quarter) * 0.03)

            for country_code, country_name in COUNTRIES:
                weight = base_country_weights.get(country_code, 0.01) * np.random.uniform(0.8, 1.2)
                market_value = total_assets * q_factor * weight

                if market_value < 0.5:
                    continue

                # Sovereign exposure (subset of total)
                sovereign_pct = np.random.uniform(0.2, 0.5) if country_code in ['GB', 'US', 'DE'] else np.random.uniform(0.1, 0.3)

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'Country_Code': country_code,
                    'Country_Name': country_name,
                    'Total_Exposure_GBP_M': round(market_value, 2),
                    'Sovereign_Exposure_GBP_M': round(market_value * sovereign_pct, 2),
                    'Corporate_Exposure_GBP_M': round(market_value * (1 - sovereign_pct), 2),
                    'Allocation_Pct': round(weight * 100, 1),
                    'Currency': CURRENCY
                })
    return pd.DataFrame(records)

# =============================================================================
# QAD_070_Look_Through - Collective investment look-through
# =============================================================================
def generate_qad_070_look_through():
    records = []

    # Fund types with underlying asset breakdown
    fund_types = [
        ('EQ_FUND', 'Global Equity Fund', {'Equity': 0.95, 'Cash': 0.05}),
        ('BD_FUND', 'Corporate Bond Fund', {'Corp_Bonds': 0.90, 'Govt_Bonds': 0.05, 'Cash': 0.05}),
        ('MM_FUND', 'Money Market Fund', {'Cash': 0.70, 'Govt_Bonds': 0.20, 'Corp_Bonds': 0.10}),
        ('BAL_FUND', 'Balanced Fund', {'Equity': 0.50, 'Corp_Bonds': 0.35, 'Govt_Bonds': 0.10, 'Cash': 0.05}),
        ('RE_FUND', 'Real Estate Fund', {'Property': 0.90, 'Cash': 0.10}),
        ('ALT_FUND', 'Alternative Fund', {'Equity': 0.30, 'Corp_Bonds': 0.30, 'Property': 0.20, 'Other': 0.20})
    ]

    for syn in SYNDICATES:
        total_civ = np.random.uniform(30, 100)  # Collective Investment Vehicles

        for quarter in QUARTERS:
            q_factor = 1 + (QUARTERS.index(quarter) * 0.03)

            for fund_code, fund_name, allocations in fund_types:
                fund_weight = np.random.uniform(0.1, 0.25)
                fund_value = total_civ * q_factor * fund_weight

                if fund_value < 0.5:
                    continue

                for underlying_asset, underlying_weight in allocations.items():
                    underlying_value = fund_value * underlying_weight

                    records.append({
                        'Syndicate': syn,
                        'ReportingYear': REPORTING_YEAR,
                        'Quarter': quarter,
                        'QuarterEnd': QUARTER_ENDS[quarter],
                        'Fund_Code': fund_code,
                        'Fund_Name': fund_name,
                        'Fund_Value_GBP_M': round(fund_value, 2),
                        'Underlying_Asset_Type': underlying_asset,
                        'Underlying_Value_GBP_M': round(underlying_value, 2),
                        'Underlying_Pct': round(underlying_weight * 100, 1),
                        'Look_Through_Applied': 'Yes',
                        'Currency': CURRENCY
                    })
    return pd.DataFrame(records)

# =============================================================================
# QAD_080_Concentration_Risk - Large exposure analysis
# =============================================================================
def generate_qad_080_concentration_risk():
    records = []

    # Top counterparties/issuers
    counterparties = [
        ('UK_GOV', 'UK Government', 'Sovereign'),
        ('US_GOV', 'US Government', 'Sovereign'),
        ('DE_GOV', 'German Government', 'Sovereign'),
        ('HSBC', 'HSBC Holdings', 'Bank'),
        ('JPM', 'JP Morgan Chase', 'Bank'),
        ('SHELL', 'Shell PLC', 'Energy'),
        ('BP', 'BP PLC', 'Energy'),
        ('APPLE', 'Apple Inc', 'Technology'),
        ('MS', 'Morgan Stanley', 'Bank'),
        ('AVIVA', 'Aviva PLC', 'Insurance')
    ]

    for syn in SYNDICATES:
        total_assets = np.random.uniform(300, 900)

        for quarter in QUARTERS:
            q_factor = 1 + (QUARTERS.index(quarter) * 0.03)

            # Generate exposures for top counterparties
            for rank, (cp_code, cp_name, cp_type) in enumerate(counterparties, 1):
                # Sovereigns have higher exposures
                if cp_type == 'Sovereign':
                    weight = np.random.uniform(0.08, 0.15)
                else:
                    weight = np.random.uniform(0.01, 0.04)

                exposure = total_assets * q_factor * weight
                threshold = total_assets * q_factor * 0.03  # 3% concentration threshold

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'Rank': rank,
                    'Counterparty_Code': cp_code,
                    'Counterparty_Name': cp_name,
                    'Counterparty_Type': cp_type,
                    'Exposure_GBP_M': round(exposure, 2),
                    'Exposure_Pct': round(weight * 100, 2),
                    'Concentration_Threshold_GBP_M': round(threshold, 2),
                    'Exceeds_Threshold': 'Yes' if exposure > threshold else 'No',
                    'CQS': 0 if cp_type == 'Sovereign' else np.random.choice([1, 2, 3]),
                    'Currency': CURRENCY
                })
    return pd.DataFrame(records)

# =============================================================================
# QAD_090_QRT_S06 - S.06.02 Asset List QRT format (summary)
# =============================================================================
def generate_qad_090_qrt_s06():
    """Generate S.06.02 List of Assets - Summary by CIC"""
    records = []

    for syn in SYNDICATES:
        total_assets = np.random.uniform(300, 900)

        for quarter in QUARTERS:
            q_factor = 1 + (QUARTERS.index(quarter) * 0.03)

            for cic_code, cic_name in CIC_CODES[:10]:  # Top 10 CIC codes
                weight = np.random.uniform(0.03, 0.20)
                market_value = total_assets * q_factor * weight

                if market_value < 1:
                    continue

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'QRT_Template': 'S.06.02',
                    'CIC_Code': cic_code,
                    'CIC_Name': cic_name,
                    'Number_Of_Holdings': np.random.randint(5, 50),
                    'Acquisition_Cost_GBP_M': round(market_value * np.random.uniform(0.92, 1.02), 2),
                    'Market_Value_GBP_M': round(market_value, 2),
                    'Accrued_Interest_GBP_M': round(market_value * np.random.uniform(0, 0.015), 2),
                    'Total_Value_GBP_M': round(market_value * 1.01, 2),
                    'Currency': CURRENCY
                })
    return pd.DataFrame(records)

# =============================================================================
# Generate all tables
# =============================================================================

# Control and metadata
QAD_001_Control = generate_qad_001_control()

# Asset analysis
QAD_010_Asset_Summary = generate_qad_010_asset_summary()
QAD_020_Asset_By_CIC = generate_qad_020_asset_by_cic()
QAD_030_Credit_Quality = generate_qad_030_credit_quality()
QAD_040_Currency_Exposure = generate_qad_040_currency_exposure()
QAD_050_Duration_Analysis = generate_qad_050_duration_analysis()
QAD_060_Geographic_Exposure = generate_qad_060_geographic_exposure()

# Look-through and concentration
QAD_070_Look_Through = generate_qad_070_look_through()
QAD_080_Concentration_Risk = generate_qad_080_concentration_risk()

# QRT format
QAD_090_QRT_S06 = generate_qad_090_qrt_s06()

# Summary statistics
print("=" * 70)
print("QAD - Quarterly Asset Data Generator")
print("=" * 70)
print(f"QAD_001_Control: {len(QAD_001_Control)} rows")
print(f"QAD_010_Asset_Summary: {len(QAD_010_Asset_Summary)} rows")
print(f"QAD_020_Asset_By_CIC: {len(QAD_020_Asset_By_CIC)} rows")
print(f"QAD_030_Credit_Quality: {len(QAD_030_Credit_Quality)} rows")
print(f"QAD_040_Currency_Exposure: {len(QAD_040_Currency_Exposure)} rows")
print(f"QAD_050_Duration_Analysis: {len(QAD_050_Duration_Analysis)} rows")
print(f"QAD_060_Geographic_Exposure: {len(QAD_060_Geographic_Exposure)} rows")
print(f"QAD_070_Look_Through: {len(QAD_070_Look_Through)} rows")
print(f"QAD_080_Concentration_Risk: {len(QAD_080_Concentration_Risk)} rows")
print(f"QAD_090_QRT_S06: {len(QAD_090_QRT_S06)} rows")
print("=" * 70)
print("QAD data generated successfully!")
