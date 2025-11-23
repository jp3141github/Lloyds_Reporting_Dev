"""
RRA Aggregator for Power BI
===========================
Aggregates and analyzes all RRA form data for comprehensive portfolio reporting.
Compatible with Power BI as a Python data source.

Tables Generated:
- portfolio_summary: Overall portfolio metrics across forms
- lob_analysis: Performance by Line of Business
- yoa_development_summary: Development patterns by year of account
- reserve_adequacy_indicators: Reserve adequacy metrics
- syndicate_profile: Individual syndicate profiles

Usage in Power BI:
1. Get Data > More > Python script
2. Copy and paste this script
3. Select the tables you need from the list

Note: This script generates synthetic data based on RRA form structures.
In production, this would aggregate from actual loaded RRA form data.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
SYNDICATES = [2987, 33, 1183, 2791, 623, 4242, 5000, 1910, 2010, 2525]
CURRENT_YEAR = 2024
YEARS_OF_ACCOUNT = list(range(2018, 2026))

# Lines of Business
LINES_OF_BUSINESS = {
    'A1': 'Direct Accident & Health',
    'D1': 'Direct Motor (Private Car)',
    'E1': 'Energy Offshore',
    'F1': 'Fire & Other Damage - Direct',
    'M1': 'Marine Cargo',
    'N1': 'Non-Marine Property Treaty',
    'P1': 'Professional Indemnity',
    'T1': 'Third Party Liability - Direct',
    'V1': 'Aviation',
    'X1': 'Catastrophe Reinsurance'
}


def generate_portfolio_summary():
    """Generate overall portfolio summary across all forms"""
    summary_data = []

    # Portfolio Overview
    total_capacity = sum([random.randint(50000000, 500000000) for _ in SYNDICATES])
    total_gwp = sum([random.randint(100000000, 800000000) for _ in SYNDICATES])
    total_gep = int(total_gwp * random.uniform(0.85, 0.95))
    total_ibnr = int(total_gwp * random.uniform(0.15, 0.30))
    avg_loss_ratio = random.uniform(0.55, 0.70)
    total_cat_losses = sum([random.randint(10000000, 100000000) for _ in range(4)])
    total_net_cat = int(total_cat_losses * random.uniform(0.4, 0.6))
    total_ulae = int(total_gwp * random.uniform(0.03, 0.06))
    total_lpt = sum([random.randint(5000000, 30000000) for _ in range(6)])

    summary_data.extend([
        {'Category': 'Portfolio Overview', 'Metric': 'Total Syndicates', 'Value': len(SYNDICATES), 'Unit': 'count'},
        {'Category': 'Portfolio Overview', 'Metric': 'Total Capacity', 'Value': total_capacity / 1000000, 'Unit': 'GBP M'},
        {'Category': 'Gross Premium', 'Metric': 'Total Gross Written Premium', 'Value': total_gwp / 1000000, 'Unit': 'GBP M'},
        {'Category': 'Gross Premium', 'Metric': 'Total Gross Earned Premium', 'Value': total_gep / 1000000, 'Unit': 'GBP M'},
        {'Category': 'IBNR Reserves', 'Metric': 'Total IBNR (Best Estimate)', 'Value': total_ibnr / 1000000, 'Unit': 'GBP M'},
        {'Category': 'Loss Ratios', 'Metric': 'Average Ultimate Loss Ratio', 'Value': avg_loss_ratio, 'Unit': 'ratio'},
        {'Category': 'Net Premium', 'Metric': 'Total Net Written Premium', 'Value': total_gwp * 0.85 / 1000000, 'Unit': 'GBP M'},
        {'Category': 'Net Premium', 'Metric': 'Total Net Earned Premium', 'Value': total_gep * 0.85 / 1000000, 'Unit': 'GBP M'},
        {'Category': 'Catastrophe Losses', 'Metric': 'Total Cat Events', 'Value': 80, 'Unit': 'count'},
        {'Category': 'Catastrophe Losses', 'Metric': 'Total Gross Cat Losses', 'Value': total_cat_losses / 1000000, 'Unit': 'GBP M'},
        {'Category': 'Catastrophe Losses', 'Metric': 'Total Net Cat Losses', 'Value': total_net_cat / 1000000, 'Unit': 'GBP M'},
        {'Category': 'ULAE', 'Metric': 'Total ULAE Reserves', 'Value': total_ulae / 1000000, 'Unit': 'GBP M'},
        {'Category': 'LPT', 'Metric': 'Total LPT Transfer Amount', 'Value': total_lpt / 1000000, 'Unit': 'GBP M'},
        {'Category': 'Data Quality', 'Metric': 'Forms with Errors', 'Value': random.randint(0, 5), 'Unit': 'count'},
        {'Category': 'Data Quality', 'Metric': 'Forms with Warnings', 'Value': random.randint(5, 20), 'Unit': 'count'},
        {'Category': 'Data Quality', 'Metric': 'Average Completeness Score', 'Value': random.uniform(0.95, 0.99), 'Unit': 'ratio'}
    ])

    df = pd.DataFrame(summary_data)
    df['Value'] = df['Value'].round(2)
    df['Report_Date'] = datetime.now().strftime('%Y-%m-%d')

    return df


def generate_lob_analysis():
    """Analyze performance across all lines of business"""
    data = []

    for lob_code, lob_desc in LINES_OF_BUSINESS.items():
        gwp = random.randint(50000000, 400000000)
        gep = int(gwp * random.uniform(0.85, 0.95))
        ibnr = int(gwp * random.uniform(0.12, 0.30))
        ulr = random.uniform(0.50, 0.75)
        num_syndicates = random.randint(3, 10)
        total_incurred = int(gwp * ulr)
        claims_count = random.randint(500, 5000)

        data.append({
            'LOB_Code': lob_code,
            'LOB_Description': lob_desc,
            'Gross_Written_Premium_M': round(gwp / 1000000, 2),
            'Gross_Earned_Premium_M': round(gep / 1000000, 2),
            'IBNR_Best_Estimate_M': round(ibnr / 1000000, 2),
            'Ultimate_Loss_Ratio': round(ulr, 4),
            'Number_of_Syndicates': num_syndicates,
            'Total_Incurred_M': round(total_incurred / 1000000, 2),
            'Claims_Count': claims_count,
            'Average_Claim_Size': round(total_incurred / claims_count, 2) if claims_count > 0 else 0,
            'Development_Pattern': random.choice(['Short Tail', 'Medium Tail', 'Long Tail']),
            'Report_Date': datetime.now().strftime('%Y-%m-%d')
        })

    return pd.DataFrame(data)


def generate_yoa_development_summary():
    """Analyze development patterns across years of account"""
    data = []

    for year in YEARS_OF_ACCOUNT[:-1]:
        max_dev = min(8, CURRENT_YEAR - year + 1)

        for dev_year in range(max_dev):
            earned_premium = random.randint(100000000, 500000000)
            paid_ratio = min(0.95, 0.15 + dev_year * 0.12 + random.uniform(-0.05, 0.05))
            incurred = int(earned_premium * random.uniform(0.55, 0.70))
            paid = int(incurred * paid_ratio)
            outstanding = incurred - paid

            data.append({
                'Year_of_Account': year,
                'Development_Year': dev_year,
                'Earned_Premium_M': round(earned_premium / 1000000, 2),
                'Incurred_Loss_M': round(incurred / 1000000, 2),
                'Paid_Loss_M': round(paid / 1000000, 2),
                'Outstanding_Reserve_M': round(outstanding / 1000000, 2),
                'Incurred_Loss_Ratio': round(incurred / earned_premium, 4),
                'Paid_Ratio': round(paid_ratio, 4),
                'Calendar_Year': year + dev_year,
                'Report_Date': datetime.now().strftime('%Y-%m-%d')
            })

    return pd.DataFrame(data)


def generate_reserve_adequacy_indicators():
    """Calculate reserve adequacy indicators"""
    indicators = []

    # IBNR to Premium ratios
    ibnr_to_premium = random.uniform(0.15, 0.25)
    ibnr_range_pct = random.uniform(0.20, 0.40)
    paid_claims_ratio = random.uniform(0.55, 0.75)
    ulae_ratio = random.uniform(0.04, 0.07)
    cat_to_total_ratio = random.uniform(0.05, 0.15)
    development_volatility = random.uniform(0.05, 0.15)

    indicators.extend([
        {
            'Indicator': 'Average IBNR to Premium Ratio',
            'Value': ibnr_to_premium,
            'Benchmark': 0.20,
            'Status': 'Within Range' if 0.12 < ibnr_to_premium < 0.28 else 'Review Required',
            'Interpretation': 'Lower is better (less uncertainty)'
        },
        {
            'Indicator': 'Average IBNR Range %',
            'Value': ibnr_range_pct,
            'Benchmark': 0.30,
            'Status': 'Within Range' if ibnr_range_pct < 0.35 else 'High Uncertainty',
            'Interpretation': 'Measure of estimation uncertainty'
        },
        {
            'Indicator': 'Average Paid Claims Ratio',
            'Value': paid_claims_ratio,
            'Benchmark': 0.65,
            'Status': 'Normal' if paid_claims_ratio > 0.50 else 'Low Development',
            'Interpretation': 'Higher indicates more mature claims'
        },
        {
            'Indicator': 'Average ULAE Ratio',
            'Value': ulae_ratio,
            'Benchmark': 0.05,
            'Status': 'Within Range' if ulae_ratio < 0.08 else 'Above Benchmark',
            'Interpretation': 'ULAE as % of loss reserves'
        },
        {
            'Indicator': 'Cat Losses to Total Reserves',
            'Value': cat_to_total_ratio,
            'Benchmark': 0.10,
            'Status': 'Normal' if cat_to_total_ratio < 0.12 else 'Elevated Cat Exposure',
            'Interpretation': 'Concentration risk from catastrophes'
        },
        {
            'Indicator': 'Development Volatility',
            'Value': development_volatility,
            'Benchmark': 0.10,
            'Status': 'Stable' if development_volatility < 0.12 else 'Volatile',
            'Interpretation': 'Year-on-year reserve movement variability'
        }
    ])

    df = pd.DataFrame(indicators)
    df['Value'] = df['Value'].round(4)
    df['Report_Date'] = datetime.now().strftime('%Y-%m-%d')

    return df


def generate_syndicate_profile():
    """Generate comprehensive profile for all syndicates"""
    data = []

    for syndicate in SYNDICATES:
        capacity = random.randint(50000000, 500000000)
        gwp = random.randint(100000000, 800000000)
        ibnr = int(gwp * random.uniform(0.12, 0.28))
        loss_ratio = random.uniform(0.50, 0.75)
        num_classes = random.randint(3, 8)
        solvency_ratio = random.uniform(1.2, 2.5)

        classes = random.sample(list(LINES_OF_BUSINESS.keys()), num_classes)

        data.append({
            'Syndicate_Number': syndicate,
            'Managing_Agent': f'Managing Agent {syndicate}',
            'Status': random.choice(['Active', 'Active', 'Active', 'Under Review']),
            'Capacity_GBP_M': round(capacity / 1000000, 2),
            'First_YoA': min(YEARS_OF_ACCOUNT),
            'Final_YoA': max(YEARS_OF_ACCOUNT) - 1,
            'Total_GWP_M': round(gwp / 1000000, 2),
            'Total_IBNR_M': round(ibnr / 1000000, 2),
            'Avg_Loss_Ratio': round(loss_ratio, 4),
            'Number_of_Classes': num_classes,
            'Classes_of_Business': ', '.join(classes),
            'Primary_Class': classes[0] if classes else 'N/A',
            'Solvency_Ratio': round(solvency_ratio, 2),
            'Validation_Status': random.choice(['Pass', 'Pass', 'Pass with Warnings', 'Review Required']),
            'Last_Update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    return pd.DataFrame(data)


# =============================================================================
# GENERATE ALL TABLES FOR POWER BI
# =============================================================================
print("Generating RRA Aggregator Data for Power BI...")
print("=" * 60)

# Generate aggregator tables (these will be available in Power BI)
portfolio_summary = generate_portfolio_summary()
lob_analysis = generate_lob_analysis()
yoa_development_summary = generate_yoa_development_summary()
reserve_adequacy_indicators = generate_reserve_adequacy_indicators()
syndicate_profile = generate_syndicate_profile()

print(f"portfolio_summary: {len(portfolio_summary)} records")
print(f"lob_analysis: {len(lob_analysis)} records")
print(f"yoa_development_summary: {len(yoa_development_summary)} records")
print(f"reserve_adequacy_indicators: {len(reserve_adequacy_indicators)} records")
print(f"syndicate_profile: {len(syndicate_profile)} records")
print("=" * 60)
print("RRA Aggregator data generated successfully!")
