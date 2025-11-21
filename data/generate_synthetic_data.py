"""
Synthetic Lloyd's of London Data Generator
Generates realistic Lloyd's syndicate liquidity stress test data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Sample syndicate names and managing agents
SYNDICATES = [
    {"number": 2001, "name": "Alpha Syndicate", "agent": "Alpha Managing Agents Ltd"},
    {"number": 2002, "name": "Beta Syndicate", "agent": "Beta Insurance Management"},
    {"number": 2003, "name": "Gamma Syndicate", "agent": "Gamma Underwriting Ltd"},
    {"number": 2004, "name": "Delta Syndicate", "agent": "Delta Risk Services"},
    {"number": 2005, "name": "Epsilon Syndicate", "agent": "Epsilon Capital Management"},
]

def generate_capital_position(syndicate_number):
    """Generate realistic capital position data"""
    # Base FAL between 100M and 500M GBP
    fal = np.random.randint(100_000_000, 500_000_000)

    # FIS typically 80-95% of FAL
    fis = int(fal * np.random.uniform(0.80, 0.95))

    # uSCR typically 60-85% of FAL
    uscr = int(fal * np.random.uniform(0.60, 0.85))

    # uECA typically 10-20% of FAL
    ueca = int(fal * np.random.uniform(0.10, 0.20))

    return {
        'syndicate_fal': fal,
        'syndicate_fis': fis,
        'syndicate_uscr': uscr,
        'syndicate_ueca': ueca
    }

def generate_asset_liquidity_breakdown(capital_position):
    """Generate asset and liquidity breakdown across quarters"""
    fal = capital_position['syndicate_fal']

    # Restricted Assets (30-45% of FAL)
    us_trust_funds = int(fal * np.random.uniform(0.20, 0.30))
    other_trust_funds = int(fal * np.random.uniform(0.05, 0.10))
    other_restricted = int(fal * np.random.uniform(0.02, 0.05))
    restricted_total = us_trust_funds + other_trust_funds + other_restricted

    # Illiquid Assets (25-40% of FAL)
    reinsurance_recoverables = int(fal * np.random.uniform(0.15, 0.25))
    reinsurer_urp_unearned = int(fal * np.random.uniform(0.08, 0.12))
    other_illiquid = int(fal * np.random.uniform(0.02, 0.05))
    illiquid_total = reinsurance_recoverables + reinsurer_urp_unearned + other_illiquid

    # Liquid Assets (remainder to balance)
    closing_free_funds = int(fal * np.random.uniform(0.15, 0.25))
    other_liquid = int(fal * np.random.uniform(0.05, 0.15))
    liquid_total = closing_free_funds + other_liquid

    # Generate quarterly projections with some variation
    quarters = ['2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30', '2025-12-31']

    data = {
        'date': quarters,
        'us_trust_funds': [int(us_trust_funds * np.random.uniform(0.95, 1.05)) for _ in quarters],
        'other_trust_funds': [int(other_trust_funds * np.random.uniform(0.95, 1.05)) for _ in quarters],
        'other_restricted_assets': [int(other_restricted * np.random.uniform(0.95, 1.05)) for _ in quarters],
        'restricted_assets_total': [],
        'reinsurance_recoverables': [int(reinsurance_recoverables * np.random.uniform(0.90, 1.10)) for _ in quarters],
        'reinsurer_urp_unearned': [int(reinsurer_urp_unearned * np.random.uniform(0.95, 1.05)) for _ in quarters],
        'other_illiquid_assets': [int(other_illiquid * np.random.uniform(0.95, 1.05)) for _ in quarters],
        'illiquid_assets_total': [],
        'closing_free_funds': [int(closing_free_funds * np.random.uniform(0.90, 1.10)) for _ in quarters],
        'other_liquid_assets': [int(other_liquid * np.random.uniform(0.95, 1.05)) for _ in quarters],
        'liquid_assets_total': []
    }

    # Calculate totals
    for i in range(len(quarters)):
        data['restricted_assets_total'].append(
            data['us_trust_funds'][i] + data['other_trust_funds'][i] + data['other_restricted_assets'][i]
        )
        data['illiquid_assets_total'].append(
            data['reinsurance_recoverables'][i] + data['reinsurer_urp_unearned'][i] + data['other_illiquid_assets'][i]
        )
        data['liquid_assets_total'].append(
            data['closing_free_funds'][i] + data['other_liquid_assets'][i]
        )

    return pd.DataFrame(data)

def generate_cashflow_position(capital_position):
    """Generate cashflow position data"""
    fal = capital_position['syndicate_fal']

    quarters = ['2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30', '2025-12-31']

    # Opening free funds for first quarter
    opening_funds = int(fal * np.random.uniform(0.15, 0.25))

    cashflow_data = []

    for i, quarter in enumerate(quarters):
        if i == 0:
            opening = opening_funds
        else:
            opening = cashflow_data[i-1]['closing_free_funds']

        # Operating cash flows
        premium_income = int(fal * np.random.uniform(0.15, 0.30))
        reinsurance_recoveries = int(fal * np.random.uniform(0.05, 0.15))
        reinsurance_deposits = int(fal * np.random.uniform(-0.05, 0.05))
        trust_fund_flows = int(fal * np.random.uniform(-0.02, 0.02))
        claims_paid = -int(fal * np.random.uniform(0.10, 0.25))
        acquisition_costs = -int(fal * np.random.uniform(0.03, 0.08))
        reinsurance_premium = -int(fal * np.random.uniform(0.05, 0.12))
        operating_expenses = -int(fal * np.random.uniform(0.02, 0.05))

        total_operating = (premium_income + reinsurance_recoveries + reinsurance_deposits +
                          trust_fund_flows + claims_paid + acquisition_costs +
                          reinsurance_premium + operating_expenses)

        # Non-operating cash flows
        investment_income = int(fal * np.random.uniform(0.02, 0.05))
        deposits_to_from_fal = int(fal * np.random.uniform(-0.05, 0.05))
        member_transactions = int(fal * np.random.uniform(-0.03, 0.03))

        total_non_operating = investment_income + deposits_to_from_fal + member_transactions

        # Total movements
        total_movements = total_operating + total_non_operating
        closing = opening + total_movements

        cashflow_data.append({
            'date': quarter,
            'opening_free_funds': opening,
            'premium_income': premium_income,
            'reinsurance_recoveries': reinsurance_recoveries,
            'reinsurance_deposits': reinsurance_deposits,
            'trust_fund_flows': trust_fund_flows,
            'claims_paid': claims_paid,
            'acquisition_costs': acquisition_costs,
            'reinsurance_premium': reinsurance_premium,
            'operating_expenses': operating_expenses,
            'total_operating_cashflow': total_operating,
            'investment_income': investment_income,
            'deposits_to_from_fal': deposits_to_from_fal,
            'member_transactions': member_transactions,
            'total_non_operating_cashflow': total_non_operating,
            'total_movements': total_movements,
            'closing_free_funds': closing
        })

    return pd.DataFrame(cashflow_data)

def generate_stress_scenario(capital_position, cashflow_baseline):
    """Generate 1-in-200 stress scenario data"""
    fal = capital_position['syndicate_fal']

    # 1-in-200 gross loss (typically 1.5x to 2.5x FAL for major events)
    gross_loss_estimate = int(fal * np.random.uniform(1.5, 2.5))

    # Reinsurance recovery (typically 40-70% of gross loss)
    reinsurance_recovery = int(gross_loss_estimate * np.random.uniform(0.40, 0.70))

    # Net loss
    net_loss_estimate = gross_loss_estimate - reinsurance_recovery

    # US funding requirement (varies by business type)
    # For demonstration: 30% of estimated reserves
    us_funding_requirement = int(reinsurance_recovery * 0.30)

    # Disputed recoveries (3 largest reinsurers)
    total_disputed = int(reinsurance_recovery * np.random.uniform(0.15, 0.30))
    disputed_60_days = int(total_disputed * 0.60)
    disputed_90_days = int(total_disputed * 0.40)

    # Impact on cashflow over quarters
    stress_cashflow = []

    for i in range(5):  # 5 quarters
        if i == 0:  # Loss occurs in Feb 2025 (Q1)
            stress_impact = -int(net_loss_estimate * 0.20)  # Initial payments
        elif i == 1:  # Q2 - major funding requirement
            stress_impact = -(us_funding_requirement + int(net_loss_estimate * 0.30))
        elif i == 2:  # Q3 - continued payments
            stress_impact = -int(net_loss_estimate * 0.25)
        elif i == 3:  # Q4
            stress_impact = -int(net_loss_estimate * 0.15)
        else:  # Q1 2026
            stress_impact = -int(net_loss_estimate * 0.10)

        stress_cashflow.append(stress_impact)

    quarters = ['2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30', '2025-12-31']

    stress_data = {
        'date': quarters,
        'stress_scenario_impact': stress_cashflow,
        'cumulative_stress_impact': np.cumsum(stress_cashflow).tolist()
    }

    # Add scenario metadata
    scenario_metadata = {
        'scenario_type': 'US Windstorm',
        'loss_occurrence_date': '2025-02-15',
        'gross_loss_estimate': gross_loss_estimate,
        'reinsurance_recovery_estimate': reinsurance_recovery,
        'net_loss_estimate': net_loss_estimate,
        'us_funding_requirement': us_funding_requirement,
        'total_disputed_recoveries': total_disputed,
        'disputed_60_days': disputed_60_days,
        'disputed_90_days': disputed_90_days
    }

    return pd.DataFrame(stress_data), scenario_metadata

def generate_full_syndicate_data(syndicate_info):
    """Generate complete dataset for a syndicate"""

    # Generate capital position
    capital = generate_capital_position(syndicate_info['number'])

    # Generate asset & liquidity breakdown
    assets = generate_asset_liquidity_breakdown(capital)

    # Generate cashflow position
    cashflow = generate_cashflow_position(capital)

    # Generate stress scenario
    stress, stress_meta = generate_stress_scenario(capital, cashflow)

    # Combine metadata
    metadata = {
        'syndicate_number': syndicate_info['number'],
        'syndicate_name': syndicate_info['name'],
        'managing_agent': syndicate_info['agent'],
        'qma_date': '2024-12-31',
        'date_completed': datetime.now().strftime('%Y-%m-%d'),
        **capital,
        **stress_meta
    }

    return {
        'metadata': metadata,
        'assets': assets,
        'cashflow': cashflow,
        'stress': stress
    }

def main():
    """Generate synthetic data for all syndicates"""

    print("Generating Synthetic Lloyd's of London Data...")
    print("=" * 80)

    all_data = {}

    for syndicate in SYNDICATES:
        print(f"\nGenerating data for {syndicate['name']} (Syndicate {syndicate['number']})...")

        data = generate_full_syndicate_data(syndicate)
        all_data[syndicate['number']] = data

        # Save individual syndicate files
        syndicate_folder = f"data/syndicate_{syndicate['number']}"
        import os
        os.makedirs(syndicate_folder, exist_ok=True)

        # Save metadata as JSON
        import json
        with open(f"{syndicate_folder}/metadata.json", 'w') as f:
            json.dump(data['metadata'], f, indent=2)

        # Save CSVs
        data['assets'].to_csv(f"{syndicate_folder}/assets_liquidity.csv", index=False)
        data['cashflow'].to_csv(f"{syndicate_folder}/cashflow.csv", index=False)
        data['stress'].to_csv(f"{syndicate_folder}/stress_scenario.csv", index=False)

        print(f"  ✓ Saved to {syndicate_folder}/")

    # Create combined dataset
    print("\n" + "=" * 80)
    print("Creating combined dataset...")

    # Combine all metadata
    all_metadata = pd.DataFrame([data['metadata'] for data in all_data.values()])
    all_metadata.to_csv('data/all_syndicates_metadata.csv', index=False)

    # Combine assets data
    all_assets = []
    for synd_num, data in all_data.items():
        df = data['assets'].copy()
        df.insert(0, 'syndicate_number', synd_num)
        all_assets.append(df)
    pd.concat(all_assets, ignore_index=True).to_csv('data/all_syndicates_assets.csv', index=False)

    # Combine cashflow data
    all_cashflow = []
    for synd_num, data in all_data.items():
        df = data['cashflow'].copy()
        df.insert(0, 'syndicate_number', synd_num)
        all_cashflow.append(df)
    pd.concat(all_cashflow, ignore_index=True).to_csv('data/all_syndicates_cashflow.csv', index=False)

    # Combine stress data
    all_stress = []
    for synd_num, data in all_data.items():
        df = data['stress'].copy()
        df.insert(0, 'syndicate_number', synd_num)
        all_stress.append(df)
    pd.concat(all_stress, ignore_index=True).to_csv('data/all_syndicates_stress.csv', index=False)

    print("  ✓ Saved combined datasets to data/ folder")
    print("\n" + "=" * 80)
    print("Data generation complete!")
    print("\nGenerated files:")
    print("  - Individual syndicate folders: data/syndicate_XXXX/")
    print("  - Combined datasets: data/all_syndicates_*.csv")
    print("=" * 80)

if __name__ == "__main__":
    main()
