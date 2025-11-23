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
- qualitative_questionnaire: LST Qualitative Questionnaire responses
- us_funding_requirements: US Surplus Lines Funding (1-in-200 tiered logic)

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


def generate_qualitative_questionnaire():
    """
    Generate LST Qualitative Questionnaire responses.
    Contains text responses for qualitative questions required in the LST submission.
    """
    # Define the qualitative questions and standard responses
    questions = [
        {
            'Question_ID': 'Q1',
            'Section': 'Credit Facilities',
            'Question': 'Describe strategy towards arranging credit facilities',
            'Response': 'The syndicate maintains committed credit facilities with multiple banking counterparties to ensure adequate liquidity. Facilities are reviewed annually and stress tested quarterly.'
        },
        {
            'Question_ID': 'Q2',
            'Section': 'Credit Facilities',
            'Question': 'Details of committed credit facilities',
            'Response': 'Committed revolving credit facility of £100m with 3-year tenor. Additional uncommitted overdraft facility of £25m for operational flexibility.'
        },
        {
            'Question_ID': 'Q3',
            'Section': 'Credit Facilities',
            'Question': 'Details of uncommitted credit facilities',
            'Response': 'Uncommitted overdraft facility of £25m available on demand. Additional uncommitted letter of credit facility of £50m for US regulatory requirements.'
        },
        {
            'Question_ID': 'Q4',
            'Section': 'Liquidity Management',
            'Question': 'Describe liquidity risk management framework',
            'Response': 'Liquidity risk is managed through daily cash monitoring, weekly liquidity reporting, and monthly stress testing. Limits are set for minimum liquid asset ratios and maximum maturity mismatches.'
        },
        {
            'Question_ID': 'Q5',
            'Section': 'Liquidity Management',
            'Question': 'Describe liquidity contingency plan',
            'Response': 'Contingency plan includes drawdown of credit facilities, sale of liquid assets, acceleration of reinsurance collections, and if necessary, capital calls from members.'
        },
        {
            'Question_ID': 'Q6',
            'Section': 'Asset Liquidity',
            'Question': 'Describe approach to asset liquidity classification',
            'Response': 'Assets classified into three buckets: Liquid (cash, govt bonds - liquidatable in 1 week), Illiquid (corporate bonds, listed equities - 1-4 weeks), Restricted (property, private equity, regulatory deposits).'
        },
        {
            'Question_ID': 'Q7',
            'Section': 'Stress Testing',
            'Question': 'Describe stress testing methodology',
            'Response': 'Stress scenarios include: 1) Major catastrophe event with immediate claims surge, 2) Market dislocation with asset value falls, 3) Reinsurer default scenario, 4) Combined operational stress.'
        },
        {
            'Question_ID': 'Q8',
            'Section': 'Stress Testing',
            'Question': 'Describe assumptions for 1-in-200 catastrophe scenario',
            'Response': 'Based on Lloyd\'s Realistic Disaster Scenarios (RDS) with gross losses calibrated to syndicate-specific exposures. Net losses reflect reinsurance programme structure.'
        },
        {
            'Question_ID': 'Q9',
            'Section': 'US Trust Funds',
            'Question': 'Describe management of US trust fund requirements',
            'Response': 'US surplus lines trust fund maintained at minimum required levels plus buffer. Assets invested in high-quality fixed income securities meeting regulatory requirements.'
        },
        {
            'Question_ID': 'Q10',
            'Section': 'Governance',
            'Question': 'Describe liquidity risk governance and oversight',
            'Response': 'Liquidity risk overseen by Risk Committee with monthly reporting. Board receives quarterly liquidity dashboard. Limits approved by Board and monitored by Finance team.'
        }
    ]

    data = []
    for synd in SYNDICATES:
        for q in questions:
            data.append({
                'Syndicate_Number': synd['number'],
                'Syndicate_Name': synd['name'],
                'Question_ID': q['Question_ID'],
                'Section': q['Section'],
                'Question': q['Question'],
                'Response': q['Response'],
                'Last_Updated': datetime.now().strftime('%Y-%m-%d'),
                'Approved_By': f'CRO - {synd["agent"]}'
            })

    return pd.DataFrame(data)


def calculate_us_funding_requirement(us_surplus_lines_exposure):
    """
    Calculate US Surplus Lines funding requirement using Lloyd's tiered 1-in-200 logic.

    Tiered percentages:
    - <$200m: 30%
    - $200m-$500m: 25%
    - $500m-$1bn: 20%
    - >$1bn: 15%

    Parameters:
    -----------
    us_surplus_lines_exposure : float
        US Surplus Lines exposure in USD

    Returns:
    --------
    float
        Required funding amount in USD
    """
    if us_surplus_lines_exposure <= 0:
        return 0

    funding = 0

    # Tier 1: First $200m at 30%
    tier1_amount = min(us_surplus_lines_exposure, 200000000)
    funding += tier1_amount * 0.30

    # Tier 2: $200m to $500m at 25%
    if us_surplus_lines_exposure > 200000000:
        tier2_amount = min(us_surplus_lines_exposure - 200000000, 300000000)
        funding += tier2_amount * 0.25

    # Tier 3: $500m to $1bn at 20%
    if us_surplus_lines_exposure > 500000000:
        tier3_amount = min(us_surplus_lines_exposure - 500000000, 500000000)
        funding += tier3_amount * 0.20

    # Tier 4: Above $1bn at 15%
    if us_surplus_lines_exposure > 1000000000:
        tier4_amount = us_surplus_lines_exposure - 1000000000
        funding += tier4_amount * 0.15

    return funding


def generate_us_funding_requirements():
    """
    Generate US Surplus Lines Funding Requirements table.
    Implements Lloyd's tiered 1-in-200 funding logic.
    """
    data = []

    for synd in SYNDICATES:
        # Generate US Surplus Lines exposure (varies by syndicate)
        us_exposure = random.randint(50000000, 1500000000)

        # Calculate tiered funding requirement
        funding_required = calculate_us_funding_requirement(us_exposure)

        # Calculate tier breakdowns for transparency
        tier1_exposure = min(us_exposure, 200000000)
        tier2_exposure = min(max(us_exposure - 200000000, 0), 300000000)
        tier3_exposure = min(max(us_exposure - 500000000, 0), 500000000)
        tier4_exposure = max(us_exposure - 1000000000, 0)

        # Current funding held
        current_funding = random.randint(int(funding_required * 0.9), int(funding_required * 1.2))

        # Determine funding status
        surplus_deficit = current_funding - funding_required
        if surplus_deficit >= 0:
            status = 'Compliant'
        elif surplus_deficit > -funding_required * 0.1:
            status = 'Warning - Near Limit'
        else:
            status = 'Non-Compliant'

        data.append({
            'Syndicate_Number': synd['number'],
            'Syndicate_Name': synd['name'],
            'Reporting_Date': f'{CURRENT_YEAR}-12-31',
            # Exposure details
            'US_Surplus_Lines_Exposure_USD': us_exposure,
            'US_Exposure_GBP_Equivalent': int(us_exposure / 1.27),  # Approx USD to GBP
            # Tier breakdown
            'Tier1_Exposure_Up_To_200m': tier1_exposure,
            'Tier1_Rate': 0.30,
            'Tier1_Funding': tier1_exposure * 0.30,
            'Tier2_Exposure_200m_to_500m': tier2_exposure,
            'Tier2_Rate': 0.25,
            'Tier2_Funding': tier2_exposure * 0.25,
            'Tier3_Exposure_500m_to_1bn': tier3_exposure,
            'Tier3_Rate': 0.20,
            'Tier3_Funding': tier3_exposure * 0.20,
            'Tier4_Exposure_Above_1bn': tier4_exposure,
            'Tier4_Rate': 0.15,
            'Tier4_Funding': tier4_exposure * 0.15,
            # Totals
            'Total_Funding_Required_USD': funding_required,
            'Total_Funding_Required_GBP': int(funding_required / 1.27),
            'Current_Funding_Held_USD': current_funding,
            'Surplus_Deficit_USD': surplus_deficit,
            'Funding_Ratio': round(current_funding / funding_required * 100, 2) if funding_required > 0 else 0,
            'Compliance_Status': status,
            # Effective rate
            'Blended_Funding_Rate': round(funding_required / us_exposure * 100, 2) if us_exposure > 0 else 0
        })

    return pd.DataFrame(data)


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
qualitative_questionnaire = generate_qualitative_questionnaire()
us_funding_requirements = generate_us_funding_requirements()

print(f"capital_position: {len(capital_position)} records")
print(f"liquidity_breakdown: {len(liquidity_breakdown)} records")
print(f"cashflow_summary: {len(cashflow_summary)} records")
print(f"stress_impact: {len(stress_impact)} records")
print(f"dashboard_summary: {len(dashboard_summary)} records")
print(f"qualitative_questionnaire: {len(qualitative_questionnaire)} records")
print(f"us_funding_requirements: {len(us_funding_requirements)} records")
print("=" * 60)
print("Liquidity Stress Test data generated successfully!")
