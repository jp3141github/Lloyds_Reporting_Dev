"""
Liquidity Stress Test Data Generator for Power BI
==================================================
Generates Liquidity Stress Test data for Lloyd's syndicates.
Compatible with Power BI as a Python data source.

Tables Generated:
- capital_position: Capital Position summary
- liquidity_breakdown: Asset & Liquidity Breakdown
- cashflow_summary: Cashflow Summary
- stress_impact: Stress Test Impact analysis
- dashboard_summary: Executive Dashboard Summary

Usage in Power BI:
1. Get Data > More > Python script
2. Copy and paste this script
3. Select the tables you need from the list
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_SYNDICATES = 10
CURRENT_YEAR = 2024

# Lloyd's syndicate data
SYNDICATES = [
    {'number': 2987, 'name': 'Syndicate 2987', 'agent': 'Managing Agent Alpha'},
    {'number': 33, 'name': 'Syndicate 33', 'agent': 'Managing Agent Beta'},
    {'number': 1183, 'name': 'Syndicate 1183', 'agent': 'Managing Agent Gamma'},
    {'number': 2791, 'name': 'Syndicate 2791', 'agent': 'Managing Agent Delta'},
    {'number': 623, 'name': 'Syndicate 623', 'agent': 'Managing Agent Epsilon'},
    {'number': 4242, 'name': 'Syndicate 4242', 'agent': 'Managing Agent Zeta'},
    {'number': 5000, 'name': 'Syndicate 5000', 'agent': 'Managing Agent Eta'},
    {'number': 1910, 'name': 'Syndicate 1910', 'agent': 'Managing Agent Theta'},
    {'number': 2010, 'name': 'Syndicate 2010', 'agent': 'Managing Agent Iota'},
    {'number': 2525, 'name': 'Syndicate 2525', 'agent': 'Managing Agent Kappa'},
]


def generate_capital_position():
    """Generate Capital Position summary table"""
    data = []

    for synd in SYNDICATES:
        fal = random.randint(100000000, 800000000)
        fis = random.randint(50000000, 400000000)
        uscr = random.randint(80000000, 600000000)
        ueca = random.randint(70000000, 500000000)

        data.append({
            'syndicate_number': synd['number'],
            'syndicate_name': synd['name'],
            'managing_agent': synd['agent'],
            'qma_date': f'{CURRENT_YEAR}-12-31',
            'syndicate_fal': fal,
            'syndicate_fis': fis,
            'syndicate_uscr': uscr,
            'syndicate_ueca': ueca,
            'solvency_ratio': round(fal / uscr, 2) if uscr > 0 else 0,
            'eca_coverage': round(fal / ueca, 2) if ueca > 0 else 0,
            'syndicate_fal_formatted': f'£{fal:,.0f}',
            'syndicate_fis_formatted': f'£{fis:,.0f}',
            'syndicate_uscr_formatted': f'£{uscr:,.0f}',
            'syndicate_ueca_formatted': f'£{ueca:,.0f}'
        })

    return pd.DataFrame(data)


def generate_liquidity_breakdown():
    """Generate Asset & Liquidity Breakdown table"""
    data = []

    # Generate monthly data for each syndicate
    dates = pd.date_range(start=f'{CURRENT_YEAR}-01-01', end=f'{CURRENT_YEAR}-12-31', freq='M')

    for synd in SYNDICATES:
        for dt in dates:
            restricted = random.randint(20000000, 100000000)
            illiquid = random.randint(30000000, 150000000)
            liquid = random.randint(50000000, 300000000)
            total = restricted + illiquid + liquid

            data.append({
                'syndicate_number': synd['number'],
                'date': dt.strftime('%Y-%m-%d'),
                'restricted_assets_total': restricted,
                'illiquid_assets_total': illiquid,
                'liquid_assets_total': liquid,
                'total_assets': total,
                'restricted_pct': round(restricted / total * 100, 2) if total > 0 else 0,
                'illiquid_pct': round(illiquid / total * 100, 2) if total > 0 else 0,
                'liquid_pct': round(liquid / total * 100, 2) if total > 0 else 0,
                'cash_and_equivalents': random.randint(10000000, 100000000),
                'government_bonds': random.randint(20000000, 150000000),
                'corporate_bonds': random.randint(15000000, 80000000),
                'equities': random.randint(5000000, 50000000),
                'property': random.randint(5000000, 40000000),
                'other_investments': random.randint(2000000, 20000000)
            })

    return pd.DataFrame(data)


def generate_cashflow_summary():
    """Generate Cashflow Summary table"""
    data = []

    dates = pd.date_range(start=f'{CURRENT_YEAR}-01-01', end=f'{CURRENT_YEAR}-12-31', freq='M')

    for synd in SYNDICATES:
        opening_funds = random.randint(50000000, 200000000)

        for i, dt in enumerate(dates):
            premium_income = random.randint(5000000, 30000000)
            claims_paid = random.randint(4000000, 25000000)
            reinsurance_recoveries = random.randint(1000000, 8000000)
            expenses = random.randint(500000, 3000000)
            investment_income = random.randint(200000, 2000000)

            total_movements = premium_income + reinsurance_recoveries + investment_income - claims_paid - expenses

            if i == 0:
                closing_funds = opening_funds + total_movements
            else:
                opening_funds = data[-1]['closing_free_funds']
                closing_funds = opening_funds + total_movements

            data.append({
                'syndicate_number': synd['number'],
                'date': dt.strftime('%Y-%m-%d'),
                'month': dt.strftime('%B'),
                'opening_free_funds': opening_funds,
                'premium_income': premium_income,
                'claims_paid': claims_paid,
                'reinsurance_recoveries': reinsurance_recoveries,
                'expenses': expenses,
                'investment_income': investment_income,
                'total_movements': total_movements,
                'closing_free_funds': closing_funds
            })

    df = pd.DataFrame(data)

    # Add cumulative columns
    for synd in SYNDICATES:
        mask = df['syndicate_number'] == synd['number']
        df.loc[mask, 'cumulative_premium_income'] = df.loc[mask, 'premium_income'].cumsum()
        df.loc[mask, 'cumulative_claims_paid'] = df.loc[mask, 'claims_paid'].cumsum()
        df.loc[mask, 'cumulative_total_movements'] = df.loc[mask, 'total_movements'].cumsum()

    return df


def generate_stress_impact():
    """Generate Stress Test Impact table"""
    data = []

    dates = pd.date_range(start=f'{CURRENT_YEAR}-01-01', end=f'{CURRENT_YEAR}-12-31', freq='M')
    scenario_types = ['Severe Downturn', 'Market Crash', 'Cat Event', 'Cyber Attack', 'Pandemic']

    for synd in SYNDICATES:
        scenario_type = random.choice(scenario_types)
        gross_loss = random.randint(20000000, 150000000)
        net_loss = int(gross_loss * random.uniform(0.4, 0.7))

        for dt in dates:
            baseline_closing = random.randint(50000000, 200000000)
            stress_impact = -random.randint(5000000, 50000000)

            data.append({
                'syndicate_number': synd['number'],
                'date': dt.strftime('%Y-%m-%d'),
                'scenario_type': scenario_type,
                'closing_free_funds': baseline_closing,
                'stress_scenario_impact': stress_impact,
                'stressed_closing_funds': baseline_closing + stress_impact,
                'liquidity_gap': -stress_impact,
                'gross_loss_estimate': gross_loss,
                'net_loss_estimate': net_loss,
                'us_funding_requirement': random.randint(10000000, 60000000)
            })

    df = pd.DataFrame(data)

    # Add min liquidity columns
    for synd in SYNDICATES:
        mask = df['syndicate_number'] == synd['number']
        df.loc[mask, 'min_liquidity_baseline'] = df.loc[mask, 'closing_free_funds'].min()
        df.loc[mask, 'min_liquidity_stressed'] = df.loc[mask, 'stressed_closing_funds'].min()

    return df


def generate_dashboard_summary():
    """Generate Executive Dashboard Summary"""
    capital = generate_capital_position()
    stress = generate_stress_impact()

    summary_data = []

    for _, synd_capital in capital.iterrows():
        synd_num = synd_capital['syndicate_number']
        synd_stress = stress[stress['syndicate_number'] == synd_num]

        summary = {
            'syndicate_number': synd_num,
            'syndicate_name': synd_capital['syndicate_name'],
            'managing_agent': synd_capital['managing_agent'],
            'total_fal': synd_capital['syndicate_fal'],
            'solvency_ratio': synd_capital['solvency_ratio'],
            'baseline_min_liquidity': synd_stress['min_liquidity_baseline'].iloc[0] if len(synd_stress) > 0 else 0,
            'stressed_min_liquidity': synd_stress['min_liquidity_stressed'].iloc[0] if len(synd_stress) > 0 else 0,
            'max_liquidity_gap': synd_stress['liquidity_gap'].max() if len(synd_stress) > 0 else 0,
            'stress_scenario': synd_stress['scenario_type'].iloc[0] if len(synd_stress) > 0 else 'N/A',
            'gross_loss_estimate': synd_stress['gross_loss_estimate'].iloc[0] if len(synd_stress) > 0 else 0,
            'net_loss_estimate': synd_stress['net_loss_estimate'].iloc[0] if len(synd_stress) > 0 else 0,
            'us_funding_requirement': synd_stress['us_funding_requirement'].iloc[0] if len(synd_stress) > 0 else 0,
            'stress_test_pass': synd_stress['stressed_closing_funds'].min() > 0 if len(synd_stress) > 0 else False
        }

        summary_data.append(summary)

    return pd.DataFrame(summary_data)


# =============================================================================
# GENERATE ALL TABLES FOR POWER BI
# =============================================================================
print("Generating Liquidity Stress Test Data for Power BI...")
print("=" * 60)

# Generate tables (these will be available in Power BI)
capital_position = generate_capital_position()
liquidity_breakdown = generate_liquidity_breakdown()
cashflow_summary = generate_cashflow_summary()
stress_impact = generate_stress_impact()
dashboard_summary = generate_dashboard_summary()

print(f"capital_position: {len(capital_position)} records")
print(f"liquidity_breakdown: {len(liquidity_breakdown)} records")
print(f"cashflow_summary: {len(cashflow_summary)} records")
print(f"stress_impact: {len(stress_impact)} records")
print(f"dashboard_summary: {len(dashboard_summary)} records")
print("=" * 60)
print("Liquidity Stress Test data generated successfully!")
