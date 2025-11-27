# Performance Management Data Return (PMDR) - Power BI Data Generator
# Monthly Contract-Level Performance Feed
#
# PMDR is Lloyd's near real-time monitoring tool for Performance Management:
# - Monthly submission of contract-level data
# - Written premium, rate change (RARC), early loss information
# - Business mix monitoring vs SBF
# - Cumulative through the year
# - Enables Performance Management to monitor underwriting behavior vs SBF
#
# Key relationships:
# - PMDR -> QMB (PMDR is monthly granular, QMB aggregates quarterly)
# - PMDR + SBF (PMDR tracks actual vs SBF plan at contract level)
#
# Submitted monthly, typically 15 business days after month-end
#
# Usage in Power BI:
# 1. Get Data > More > Other > Python script
# 2. Paste this entire file
# 3. Select tables from navigator
# 4. Load

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import string

# Set seed for reproducibility
np.random.seed(42)

# Configuration
SYNDICATES = [33, 623, 1183, 1910, 2010, 2525, 2791, 2987, 4242, 5000]
REPORTING_YEAR = 2024
MONTHS = list(range(1, 13))
MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
CURRENCY = 'GBP'

# Lloyd's risk codes
RISK_CODES = [
    ('A1', 'Property D&F - Direct'),
    ('A2', 'Property D&F - Facultative'),
    ('A3', 'Property Commercial - Direct'),
    ('B1', 'Casualty - General Liability'),
    ('B2', 'Casualty - Professional Liability'),
    ('B3', 'Casualty - Financial Lines D&O'),
    ('B4', 'Casualty - Financial Lines PI'),
    ('C1', 'Marine Hull'),
    ('C2', 'Marine Cargo'),
    ('D1', 'Energy Offshore'),
    ('E1', 'Aviation Hull'),
    ('F1', 'Motor - UK'),
    ('G1', 'Accident & Health'),
    ('H1', 'Credit & Surety'),
    ('I1', 'Cyber'),
    ('J1', 'Political Risk & Terror'),
    ('K1', 'Property Treaty XL'),
    ('L1', 'Casualty Treaty XL')
]

# Placement types
PLACEMENT_TYPES = ['Open Market', 'Binder', 'Lineslip', 'Facility', 'Delegated Authority']

# Brokers
BROKERS = ['Aon', 'Marsh', 'Willis', 'Gallagher', 'Miller', 'Ed', 'BMS', 'Lockton', 'Howden', 'McGill']

# Territories
TERRITORIES = [
    ('UK', 'United Kingdom'),
    ('US', 'United States'),
    ('EU', 'European Union'),
    ('APAC', 'Asia Pacific'),
    ('LATAM', 'Latin America'),
    ('MEA', 'Middle East & Africa'),
    ('CAN', 'Canada'),
    ('AUS', 'Australia')
]

# =============================================================================
# Helper functions
# =============================================================================
def generate_umr():
    """Generate a Unique Market Reference"""
    broker_code = ''.join(np.random.choice(list(string.ascii_uppercase), 2))
    year = str(REPORTING_YEAR)[2:]
    seq = ''.join(np.random.choice(list(string.digits), 5))
    return f'B{broker_code}{year}{seq}'

def generate_osnd():
    """Generate an OSND (Original Signing Number Date)"""
    return f'{np.random.randint(1, 999):03d}/{REPORTING_YEAR}'

# =============================================================================
# PMDR_001_Control - Submission metadata
# =============================================================================
def generate_pmdr_001_control():
    records = []
    for syn in SYNDICATES:
        for month in MONTHS:
            month_end = datetime(REPORTING_YEAR, month, 28 if month == 2 else 30 if month in [4, 6, 9, 11] else 31)
            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'ReportingMonth': month,
                'MonthName': MONTH_NAMES[month - 1],
                'MonthEnd': month_end,
                'SubmissionDeadline': month_end + timedelta(days=15),
                'SubmissionDate': month_end + timedelta(days=np.random.randint(12, 15)),
                'ManagingAgent': f'MA{syn % 100:03d}',
                'ReportType': 'PMDR',
                'ReturnVersion': '2024.1',
                'Status': 'Final',
                'RecordCount': np.random.randint(500, 2000),
                'Currency': CURRENCY
            })
    return pd.DataFrame(records)

# =============================================================================
# PMDR_010_Contract_Summary - Contract-level premium summary
# =============================================================================
def generate_pmdr_010_contract_summary():
    records = []

    for syn in SYNDICATES:
        # Each syndicate has a different number of contracts per month
        base_contracts_per_month = np.random.randint(40, 100)

        for month in MONTHS:
            # Seasonality in contract volume
            seasonality = 1.0 + 0.3 * np.sin((month - 1) * np.pi / 6)  # Peak around Q1/Q2
            num_contracts = int(base_contracts_per_month * seasonality * np.random.uniform(0.8, 1.2))

            for contract_idx in range(num_contracts):
                umr = generate_umr()
                osnd = generate_osnd()
                risk_code, risk_name = RISK_CODES[np.random.randint(0, len(RISK_CODES))]
                territory_code, territory_name = TERRITORIES[np.random.randint(0, len(TERRITORIES))]

                # Premium and line details
                gwp = np.random.lognormal(mean=np.log(50), sigma=1.2)
                gwp = max(5, min(gwp, 2000))  # Cap between 5K and 2M
                signed_line = np.random.uniform(0.05, 0.50)
                syndicate_share = gwp * signed_line

                # Rate change (RARC)
                rarc = np.random.normal(3, 8)  # Average 3% increase
                rarc = max(-30, min(rarc, 50))  # Cap at reasonable bounds

                # Inception date (during reporting month)
                inception_day = np.random.randint(1, 28)
                inception_date = datetime(REPORTING_YEAR, month, inception_day)

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'ReportingMonth': month,
                    'MonthName': MONTH_NAMES[month - 1],
                    'UMR': umr,
                    'OSND': osnd,
                    'Risk_Code': risk_code,
                    'Risk_Name': risk_name,
                    'Territory_Code': territory_code,
                    'Territory_Name': territory_name,
                    'Placement_Type': np.random.choice(PLACEMENT_TYPES, p=[0.50, 0.20, 0.15, 0.10, 0.05]),
                    'Broker': np.random.choice(BROKERS),
                    'Inception_Date': inception_date,
                    'Expiry_Date': inception_date + timedelta(days=365),
                    # Premium
                    'GWP_100Pct_GBP_K': round(gwp, 2),
                    'Signed_Line_Pct': round(signed_line * 100, 1),
                    'Syndicate_Share_GBP_K': round(syndicate_share, 2),
                    # Rate
                    'RARC_Pct': round(rarc, 1),
                    'Risk_Adjusted': 'Yes' if abs(rarc) > 0 else 'No',
                    # Flags
                    'New_Business': 'Yes' if np.random.random() < 0.4 else 'No',
                    'Renewal': 'Yes' if np.random.random() >= 0.4 else 'No',
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# PMDR_020_Monthly_Aggregation - Monthly summary by class
# =============================================================================
def generate_pmdr_020_monthly_aggregation():
    records = []

    for syn in SYNDICATES:
        for month in MONTHS:
            for risk_code, risk_name in RISK_CODES:
                # Not all syndicates write all classes
                if np.random.random() < 0.3:
                    continue

                # Monthly premium
                gwp = np.random.uniform(500, 5000)  # GBP thousands

                # Seasonality
                seasonality = 1.0 + 0.2 * np.sin((month - 1) * np.pi / 6)
                gwp *= seasonality

                # Contract counts
                num_contracts = np.random.randint(5, 50)
                avg_size = gwp / num_contracts

                # Rate metrics
                avg_rarc = np.random.normal(3, 5)
                weighted_rarc = avg_rarc * np.random.uniform(0.9, 1.1)

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'ReportingMonth': month,
                    'MonthName': MONTH_NAMES[month - 1],
                    'Risk_Code': risk_code,
                    'Risk_Name': risk_name,
                    'Contract_Count': num_contracts,
                    'GWP_GBP_K': round(gwp, 2),
                    'Avg_Contract_Size_GBP_K': round(avg_size, 2),
                    'New_Business_Pct': round(np.random.uniform(30, 60), 1),
                    'Renewal_Pct': round(np.random.uniform(40, 70), 1),
                    'Avg_RARC_Pct': round(avg_rarc, 1),
                    'Weighted_RARC_Pct': round(weighted_rarc, 1),
                    'Avg_Signed_Line_Pct': round(np.random.uniform(10, 35), 1),
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# PMDR_030_YTD_Premium - Year-to-date premium tracking
# =============================================================================
def generate_pmdr_030_ytd_premium():
    records = []

    for syn in SYNDICATES:
        for risk_code, risk_name in RISK_CODES:
            if np.random.random() < 0.3:
                continue

            # Annual plan from SBF
            plan_fy_gwp = np.random.uniform(5000, 50000)  # GBP thousands

            # Cumulative through year
            ytd_gwp = 0
            for month in MONTHS:
                # Monthly increment
                monthly_pct = np.random.uniform(0.06, 0.12)
                monthly_gwp = plan_fy_gwp * monthly_pct * np.random.uniform(0.85, 1.15)
                ytd_gwp += monthly_gwp

                # Plan YTD (linear assumption)
                plan_ytd = plan_fy_gwp * (month / 12)

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'ReportingMonth': month,
                    'MonthName': MONTH_NAMES[month - 1],
                    'Risk_Code': risk_code,
                    'Risk_Name': risk_name,
                    # Plan
                    'Plan_FY_GWP_GBP_K': round(plan_fy_gwp, 2),
                    'Plan_YTD_GWP_GBP_K': round(plan_ytd, 2),
                    # Actual
                    'Actual_Month_GWP_GBP_K': round(monthly_gwp, 2),
                    'Actual_YTD_GWP_GBP_K': round(ytd_gwp, 2),
                    # Variance
                    'YTD_Variance_GBP_K': round(ytd_gwp - plan_ytd, 2),
                    'YTD_Variance_Pct': round(((ytd_gwp / plan_ytd) - 1) * 100, 1) if plan_ytd > 0 else 0,
                    # Projection
                    'Projected_FY_GWP_GBP_K': round(ytd_gwp / (month / 12), 2) if month > 0 else 0,
                    'On_Track': 'Yes' if abs((ytd_gwp / plan_ytd) - 1) < 0.10 else 'No' if plan_ytd > 0 else 'N/A',
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# PMDR_040_Rate_Change_Detail - Detailed rate change analysis
# =============================================================================
def generate_pmdr_040_rate_change_detail():
    records = []

    for syn in SYNDICATES:
        for month in MONTHS:
            for risk_code, risk_name in RISK_CODES:
                if np.random.random() < 0.4:
                    continue

                # Rate change distribution for this class/month
                avg_rate = np.random.normal(3, 6)

                # Breakdown by rate band
                rate_bands = [
                    ('<-10%', 'Significant decrease'),
                    ('-10% to -5%', 'Moderate decrease'),
                    ('-5% to 0%', 'Small decrease'),
                    ('0% to 5%', 'Small increase'),
                    ('5% to 10%', 'Moderate increase'),
                    ('10% to 20%', 'Significant increase'),
                    ('>20%', 'Large increase')
                ]

                # Generate distribution
                if avg_rate < -5:
                    weights = [0.15, 0.25, 0.30, 0.15, 0.10, 0.04, 0.01]
                elif avg_rate < 0:
                    weights = [0.05, 0.15, 0.35, 0.25, 0.12, 0.06, 0.02]
                elif avg_rate < 5:
                    weights = [0.02, 0.08, 0.20, 0.35, 0.20, 0.10, 0.05]
                else:
                    weights = [0.01, 0.04, 0.10, 0.25, 0.30, 0.20, 0.10]

                total_contracts = np.random.randint(10, 100)
                total_premium = np.random.uniform(500, 5000)

                for (band, desc), weight in zip(rate_bands, weights):
                    contracts_in_band = int(total_contracts * weight)
                    premium_in_band = total_premium * weight * np.random.uniform(0.8, 1.2)

                    if contracts_in_band == 0:
                        continue

                    records.append({
                        'Syndicate': syn,
                        'ReportingYear': REPORTING_YEAR,
                        'ReportingMonth': month,
                        'MonthName': MONTH_NAMES[month - 1],
                        'Risk_Code': risk_code,
                        'Risk_Name': risk_name,
                        'Rate_Band': band,
                        'Rate_Band_Description': desc,
                        'Contract_Count': contracts_in_band,
                        'Premium_GBP_K': round(premium_in_band, 2),
                        'Pct_of_Contracts': round(weight * 100, 1),
                        'Pct_of_Premium': round(weight * 100, 1),
                        'Currency': CURRENCY
                    })

    return pd.DataFrame(records)

# =============================================================================
# PMDR_050_Business_Mix - Business mix analysis
# =============================================================================
def generate_pmdr_050_business_mix():
    records = []

    # Mix dimensions
    dimensions = [
        ('Territory', TERRITORIES),
        ('Placement_Type', [(p, p) for p in PLACEMENT_TYPES]),
        ('Broker', [(b, b) for b in BROKERS])
    ]

    for syn in SYNDICATES:
        for month in MONTHS:
            for dim_name, dim_values in dimensions:
                total_premium = np.random.uniform(2000, 10000)
                weights = np.random.dirichlet(np.ones(len(dim_values)))

                for i, (code, name) in enumerate(dim_values):
                    weight = weights[i]
                    premium = total_premium * weight

                    if premium < 10:
                        continue

                    records.append({
                        'Syndicate': syn,
                        'ReportingYear': REPORTING_YEAR,
                        'ReportingMonth': month,
                        'MonthName': MONTH_NAMES[month - 1],
                        'Dimension': dim_name,
                        'Category_Code': code,
                        'Category_Name': name,
                        'Premium_GBP_K': round(premium, 2),
                        'Mix_Pct': round(weight * 100, 1),
                        'Contract_Count': np.random.randint(5, 100),
                        'Avg_RARC_Pct': round(np.random.normal(3, 5), 1),
                        'Currency': CURRENCY
                    })

    return pd.DataFrame(records)

# =============================================================================
# PMDR_060_Early_Loss_Indicators - Early loss signals
# =============================================================================
def generate_pmdr_060_early_loss_indicators():
    records = []

    for syn in SYNDICATES:
        for month in MONTHS:
            for risk_code, risk_name in RISK_CODES:
                if np.random.random() < 0.5:
                    continue

                # Earned premium
                earned_premium = np.random.uniform(300, 3000)

                # Loss indicators
                reported_claims = np.random.randint(0, 20)
                reported_incurred = earned_premium * np.random.uniform(0.1, 0.6)

                # Large losses (>100K)
                large_losses = np.random.randint(0, 3)
                large_loss_amount = large_losses * np.random.uniform(100, 500) if large_losses > 0 else 0

                # Early loss ratio
                early_lr = (reported_incurred + large_loss_amount) / earned_premium * 100 if earned_premium > 0 else 0

                # Expected loss ratio from pricing
                expected_lr = np.random.uniform(55, 75)

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'ReportingMonth': month,
                    'MonthName': MONTH_NAMES[month - 1],
                    'Risk_Code': risk_code,
                    'Risk_Name': risk_name,
                    'Earned_Premium_GBP_K': round(earned_premium, 2),
                    'Reported_Claims_Count': reported_claims,
                    'Reported_Incurred_GBP_K': round(reported_incurred, 2),
                    'Large_Losses_Count': large_losses,
                    'Large_Loss_Amount_GBP_K': round(large_loss_amount, 2),
                    'Early_Loss_Ratio_Pct': round(early_lr, 1),
                    'Expected_Loss_Ratio_Pct': round(expected_lr, 1),
                    'Variance_Pct': round(early_lr - expected_lr, 1),
                    'Status': 'On Track' if early_lr <= expected_lr * 1.1 else 'Monitor' if early_lr <= expected_lr * 1.3 else 'Concern',
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# PMDR_070_SBF_Comparison - Comparison to SBF assumptions
# =============================================================================
def generate_pmdr_070_sbf_comparison():
    records = []

    metrics = [
        ('GWP', 'Gross Written Premium'),
        ('RARC', 'Risk Adjusted Rate Change'),
        ('Avg_Line', 'Average Signed Line'),
        ('New_Business_Pct', 'New Business Percentage'),
        ('Top_10_Broker_Pct', 'Top 10 Broker Share'),
        ('US_Exposure_Pct', 'US Exposure')
    ]

    for syn in SYNDICATES:
        for month in MONTHS:
            for metric_code, metric_name in metrics:
                # SBF assumption
                if metric_code == 'GWP':
                    sbf_value = np.random.uniform(5000, 20000)
                    actual_value = sbf_value * np.random.uniform(0.85, 1.15) * (month / 12)
                    sbf_ytd = sbf_value * (month / 12)
                elif metric_code == 'RARC':
                    sbf_value = np.random.uniform(2, 8)
                    actual_value = sbf_value + np.random.normal(0, 3)
                    sbf_ytd = sbf_value
                else:
                    sbf_value = np.random.uniform(20, 50)
                    actual_value = sbf_value * np.random.uniform(0.85, 1.15)
                    sbf_ytd = sbf_value

                variance = actual_value - sbf_ytd
                variance_pct = (variance / sbf_ytd * 100) if sbf_ytd != 0 else 0

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'ReportingMonth': month,
                    'MonthName': MONTH_NAMES[month - 1],
                    'Metric_Code': metric_code,
                    'Metric_Name': metric_name,
                    'SBF_FY_Value': round(sbf_value, 2),
                    'SBF_YTD_Value': round(sbf_ytd, 2),
                    'Actual_Value': round(actual_value, 2),
                    'Variance': round(variance, 2),
                    'Variance_Pct': round(variance_pct, 1),
                    'Within_Tolerance': 'Yes' if abs(variance_pct) <= 10 else 'No',
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# Generate all tables
# =============================================================================

# Control
PMDR_001_Control = generate_pmdr_001_control()

# Contract and premium data
PMDR_010_Contract_Summary = generate_pmdr_010_contract_summary()
PMDR_020_Monthly_Aggregation = generate_pmdr_020_monthly_aggregation()
PMDR_030_YTD_Premium = generate_pmdr_030_ytd_premium()

# Rate and mix analysis
PMDR_040_Rate_Change_Detail = generate_pmdr_040_rate_change_detail()
PMDR_050_Business_Mix = generate_pmdr_050_business_mix()

# Performance indicators
PMDR_060_Early_Loss_Indicators = generate_pmdr_060_early_loss_indicators()
PMDR_070_SBF_Comparison = generate_pmdr_070_sbf_comparison()

# Summary statistics
print("=" * 70)
print("PMDR - Performance Management Data Return (Monthly) Generator")
print("=" * 70)
print(f"PMDR_001_Control: {len(PMDR_001_Control)} rows")
print(f"PMDR_010_Contract_Summary: {len(PMDR_010_Contract_Summary)} rows")
print(f"PMDR_020_Monthly_Aggregation: {len(PMDR_020_Monthly_Aggregation)} rows")
print(f"PMDR_030_YTD_Premium: {len(PMDR_030_YTD_Premium)} rows")
print(f"PMDR_040_Rate_Change_Detail: {len(PMDR_040_Rate_Change_Detail)} rows")
print(f"PMDR_050_Business_Mix: {len(PMDR_050_Business_Mix)} rows")
print(f"PMDR_060_Early_Loss_Indicators: {len(PMDR_060_Early_Loss_Indicators)} rows")
print(f"PMDR_070_SBF_Comparison: {len(PMDR_070_SBF_Comparison)} rows")
print("=" * 70)
print("PMDR data generated successfully!")
