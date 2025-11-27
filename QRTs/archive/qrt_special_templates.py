"""
PRA/BoE QRT Generators - Special Templates
==========================================
MALIR: Matching Adjustment Life Insurance Return
MR01: Market Risk Sensitivities
QMC01: Quarterly Model Change

Usage in Power BI:
1. Get Data > More > Python script
2. Copy and paste this script
3. Select the tables you need from the list
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================================================
# Configuration
# ============================================================================

UNDERTAKINGS = [
    {'lei': '549300ABCDEF123456G7', 'name': 'Lloyd\'s Syndicate 2987', 'type': 'Non-Life'},
    {'lei': '549300HIJKLM789012N3', 'name': 'Lloyd\'s Syndicate 33', 'type': 'Non-Life'},
    {'lei': '549300OPQRS456789T0', 'name': 'Lloyd\'s Syndicate 1183', 'type': 'Non-Life'},
    {'lei': '549300UVWXY012345Z1', 'name': 'Lloyd\'s Syndicate 2791', 'type': 'Composite'},
    {'lei': '549300ABCDE678901F2', 'name': 'Lloyd\'s Syndicate 623', 'type': 'Non-Life'},
]

REPORTING_DATE = '2024-12-31'

def generate_lei():
    return '549300' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))

def generate_isin():
    country = random.choice(['GB', 'US', 'DE', 'FR'])
    return country + ''.join(random.choices(string.ascii_uppercase + string.digits, k=9)) + str(random.randint(0, 9))

def random_amount(min_val, max_val, precision=2):
    return round(np.random.uniform(min_val, max_val), precision)

def random_percentage(min_val=0, max_val=100):
    return round(np.random.uniform(min_val, max_val), 4)


# ============================================================================
# MALIR - Matching Adjustment Life Insurance Return (Comprehensive)
# ============================================================================

def generate_malir_summary():
    """
    MALIR Summary - Overall matching adjustment portfolio summary.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            total_assets = random_amount(500_000_000, 10_000_000_000)
            total_liabilities = total_assets * random_percentage(90, 102) / 100

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Number_Of_MA_Portfolios': random.randint(1, 5),
                'Total_MA_Assets': total_assets,
                'Total_MA_Liabilities': total_liabilities,
                'Net_MA_Position': total_assets - total_liabilities,
                'Weighted_Average_MA_BPS': random_percentage(50, 150),
                'Impact_On_Own_Funds': (total_assets - total_liabilities) * random_percentage(5, 15) / 100,
                'Impact_On_SCR': random_amount(-50_000_000, -10_000_000),
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


def generate_malir_portfolio_details():
    """
    MALIR Portfolio Details - Individual portfolio information.
    """
    data = []

    portfolio_types = ['Annuities', 'With-Profits Annuities', 'Bulk Annuities', 'Other']

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            for i, port_type in enumerate(portfolio_types[:random.randint(1, 4)]):
                assets = random_amount(100_000_000, 3_000_000_000)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Portfolio_ID': f'MAP_{undertaking["lei"][:6]}_{i+1:02d}',
                    'Portfolio_Name': f'{port_type} Portfolio {i+1}',
                    'Portfolio_Type': port_type,
                    # Asset Information
                    'Total_Assets_Market_Value': assets,
                    'Government_Bonds': assets * random_percentage(20, 40) / 100,
                    'Corporate_Bonds': assets * random_percentage(40, 70) / 100,
                    'Infrastructure_Bonds': assets * random_percentage(5, 20) / 100,
                    'Other_Assets': assets * random_percentage(2, 10) / 100,
                    # Liability Information
                    'Total_Liabilities_BEL': assets * random_percentage(90, 100) / 100,
                    'Risk_Margin': assets * random_percentage(3, 8) / 100,
                    'Number_Of_Annuitants': random.randint(5000, 100000),
                    'Average_Age': random_percentage(65, 80),
                    # Matching Information
                    'Asset_Duration': random_percentage(8, 18),
                    'Liability_Duration': random_percentage(8, 18),
                    'Duration_Gap': random_percentage(-1, 1),
                    'Cash_Flow_Match_Ratio': random_percentage(95, 105),
                    # MA Calculation
                    'Risk_Free_Rate': random_percentage(3, 5),
                    'Asset_Spread': random_percentage(1.5, 3.5),
                    'Fundamental_Spread': random_percentage(0.3, 1),
                    'Matching_Adjustment_BPS': random_percentage(60, 180),
                    # Impact
                    'BEL_Without_MA': assets * random_percentage(95, 105) / 100,
                    'BEL_With_MA': assets * random_percentage(85, 98) / 100,
                    'Own_Funds_Benefit': assets * random_percentage(2, 10) / 100,
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


def generate_malir_asset_listing():
    """
    MALIR Asset Listing - Detailed asset listing for MA portfolios.
    """
    data = []

    asset_types = [
        ('UK Gilt', 'Government', '1'),
        ('Corporate Bond AAA', 'Corporate', '21'),
        ('Corporate Bond AA', 'Corporate', '22'),
        ('Corporate Bond A', 'Corporate', '23'),
        ('Corporate Bond BBB', 'Corporate', '24'),
        ('Infrastructure Bond', 'Corporate', '25'),
        ('Equity Release Mortgage', 'Loan', '84'),
    ]

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            for asset_name, asset_class, cic in asset_types:
                for _ in range(random.randint(5, 30)):
                    par_value = random_amount(1_000_000, 100_000_000)
                    market_value = par_value * random_percentage(90, 115) / 100

                    data.append({
                        'LEI': undertaking['lei'],
                        'Undertaking_Name': undertaking['name'],
                        'Reporting_Date': REPORTING_DATE,
                        'Portfolio_ID': f'MAP_{undertaking["lei"][:6]}_01',
                        'Asset_ID': f'ASSET_{generate_isin()[:10]}',
                        'ISIN': generate_isin() if asset_class != 'Loan' else None,
                        'Asset_Name': f'{asset_name} - {random.randint(2025, 2060)}',
                        'Asset_Class': asset_class,
                        'CIC_Code': cic,
                        'Rating': random.choice(['AAA', 'AA', 'A', 'BBB']) if asset_class == 'Corporate' else 'Sovereign' if asset_class == 'Government' else 'Unrated',
                        'Par_Value': par_value,
                        'Market_Value': market_value,
                        'Accrued_Interest': par_value * random_percentage(0, 3) / 100,
                        'Coupon_Rate': random_percentage(2, 6),
                        'Maturity_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') +
                                         timedelta(days=random.randint(365, 14600))).strftime('%Y-%m-%d'),
                        'Duration_Years': random_percentage(1, 30),
                        'Spread_BPS': random_percentage(20, 300) if asset_class == 'Corporate' else 0,
                        'Fundamental_Spread_BPS': random_percentage(10, 100) if asset_class == 'Corporate' else 0,
                        'MA_Eligible': 'Yes',
                        'Currency': random.choice(['GBP', 'USD', 'EUR'])
                    })

    return pd.DataFrame(data)


def generate_malir_liability_analysis():
    """
    MALIR Liability Analysis - Liability characteristics for MA portfolios.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            total_bel = random_amount(500_000_000, 5_000_000_000)

            # Age band analysis
            age_bands = ['Under 65', '65-69', '70-74', '75-79', '80-84', '85-89', '90+']

            for age_band in age_bands:
                band_pct = random_percentage(5, 25)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Portfolio_ID': f'MAP_{undertaking["lei"][:6]}_01',
                    'Age_Band': age_band,
                    'Number_Of_Annuitants': random.randint(500, 20000),
                    'BEL_Amount': total_bel * band_pct / 100,
                    'Percentage_Of_Total': band_pct,
                    'Average_Annual_Payment': random_amount(5000, 50000),
                    'Average_Remaining_Life_Expectancy': random_percentage(5, 30),
                    'Average_Duration': random_percentage(3, 25),
                    'Inflation_Linkage_Pct': random_percentage(0, 100),
                    'Spouses_Pension_Pct': random_percentage(30, 70),
                    'Mortality_Table': 'CMI 2023',
                    'Mortality_Improvement_Basis': 'CMI_2023_M_[1.5%]',
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


def generate_malir_cash_flow_matching():
    """
    MALIR Cash Flow Matching - Asset-liability cash flow comparison.
    """
    data = []

    years = list(range(1, 61))  # 60 year projection

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            initial_cf = random_amount(50_000_000, 300_000_000)

            for year in years:
                # Declining pattern
                liability_cf = initial_cf * (0.96 ** (year - 1))
                asset_cf = liability_cf * random_percentage(97, 103) / 100

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Portfolio_ID': f'MAP_{undertaking["lei"][:6]}_01',
                    'Projection_Year': year,
                    'Liability_Cash_Flow': liability_cf,
                    'Asset_Cash_Flow': asset_cf,
                    'Net_Cash_Flow': asset_cf - liability_cf,
                    'Cumulative_Net_Cash_Flow': (asset_cf - liability_cf) * year * 0.5,
                    'Liability_PV': liability_cf / ((1 + 0.04) ** year),
                    'Asset_PV': asset_cf / ((1 + 0.04) ** year),
                    'Match_Ratio_Year': asset_cf / liability_cf * 100 if liability_cf > 0 else 100,
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


def generate_malir_stress_tests():
    """
    MALIR Stress Tests - Stress testing results for MA portfolios.
    """
    data = []

    stress_scenarios = [
        ('Interest Rate +100bps', 'Interest Rate'),
        ('Interest Rate -100bps', 'Interest Rate'),
        ('Credit Spread +100bps', 'Credit'),
        ('Credit Migration', 'Credit'),
        ('Mass Lapse', 'Lapse'),
        ('Longevity +20%', 'Longevity'),
        ('Inflation +2%', 'Inflation'),
        ('Combined Stress', 'Combined'),
    ]

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            base_own_funds = random_amount(100_000_000, 500_000_000)
            base_scr = base_own_funds * random_percentage(40, 70) / 100

            for scenario, risk_type in stress_scenarios:
                impact_pct = random_percentage(-30, -5) if 'stress' in scenario.lower() or '+' in scenario else random_percentage(-15, 5)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Portfolio_ID': f'MAP_{undertaking["lei"][:6]}_01',
                    'Stress_Scenario': scenario,
                    'Risk_Type': risk_type,
                    'Base_Own_Funds': base_own_funds,
                    'Stressed_Own_Funds': base_own_funds * (1 + impact_pct / 100),
                    'Own_Funds_Impact': base_own_funds * impact_pct / 100,
                    'Own_Funds_Impact_Pct': impact_pct,
                    'Base_SCR': base_scr,
                    'Stressed_SCR': base_scr * random_percentage(95, 115) / 100,
                    'Base_Solvency_Ratio': base_own_funds / base_scr * 100,
                    'Stressed_Solvency_Ratio': (base_own_funds * (1 + impact_pct / 100)) / (base_scr * random_percentage(95, 115) / 100) * 100,
                    'MA_Change_BPS': random_percentage(-50, 50),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# MR01 - Market Risk Sensitivities
# ============================================================================

def generate_mr01_market_risk_sensitivities():
    """
    MR01 - Market Risk Sensitivities
    Sensitivity analysis for market risk factors.
    """
    data = []

    risk_factors = [
        # Interest Rate Sensitivities
        ('IR +50bps Parallel', 'Interest Rate', '+50bps parallel shift'),
        ('IR -50bps Parallel', 'Interest Rate', '-50bps parallel shift'),
        ('IR +100bps Parallel', 'Interest Rate', '+100bps parallel shift'),
        ('IR -100bps Parallel', 'Interest Rate', '-100bps parallel shift'),
        ('IR Steepening', 'Interest Rate', 'Steepening of yield curve'),
        ('IR Flattening', 'Interest Rate', 'Flattening of yield curve'),
        # Equity Sensitivities
        ('Equity -10%', 'Equity', '-10% equity fall'),
        ('Equity -25%', 'Equity', '-25% equity fall'),
        ('Equity -40%', 'Equity', '-40% equity fall'),
        ('Equity Vol +25%', 'Equity', '+25% implied volatility'),
        # Property Sensitivities
        ('Property -10%', 'Property', '-10% property fall'),
        ('Property -25%', 'Property', '-25% property fall'),
        # Spread Sensitivities
        ('Credit Spread +50bps', 'Spread', '+50bps credit spread'),
        ('Credit Spread +100bps', 'Spread', '+100bps credit spread'),
        ('Credit Spread +200bps', 'Spread', '+200bps credit spread'),
        # Currency Sensitivities
        ('USD -10%', 'Currency', '-10% USD depreciation'),
        ('EUR -10%', 'Currency', '-10% EUR depreciation'),
        ('FX Vol +25%', 'Currency', '+25% FX implied volatility'),
        # Inflation Sensitivities
        ('Inflation +1%', 'Inflation', '+1% inflation'),
        ('Inflation -1%', 'Inflation', '-1% inflation'),
    ]

    for undertaking in UNDERTAKINGS:
        base_nav = random_amount(500_000_000, 3_000_000_000)
        base_own_funds = base_nav * random_percentage(15, 30) / 100
        base_scr = base_own_funds * random_percentage(50, 80) / 100

        for risk_name, risk_type, description in risk_factors:
            # Calculate impact based on risk type
            if 'IR' in risk_name:
                nav_impact_pct = random_percentage(-8, 8)
            elif 'Equity' in risk_name:
                nav_impact_pct = random_percentage(-15, -2) if '-' in risk_name else random_percentage(-5, 2)
            elif 'Property' in risk_name:
                nav_impact_pct = random_percentage(-10, -2)
            elif 'Spread' in risk_name:
                nav_impact_pct = random_percentage(-12, -2)
            elif 'USD' in risk_name or 'EUR' in risk_name or 'FX' in risk_name:
                nav_impact_pct = random_percentage(-5, 5)
            elif 'Inflation' in risk_name:
                nav_impact_pct = random_percentage(-3, 3)
            else:
                nav_impact_pct = random_percentage(-5, 5)

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Risk_Factor': risk_name,
                'Risk_Type': risk_type,
                'Scenario_Description': description,
                # NAV Impact
                'Base_NAV': base_nav,
                'Stressed_NAV': base_nav * (1 + nav_impact_pct / 100),
                'NAV_Change': base_nav * nav_impact_pct / 100,
                'NAV_Change_Pct': nav_impact_pct,
                # Own Funds Impact
                'Base_Own_Funds': base_own_funds,
                'Stressed_Own_Funds': base_own_funds * (1 + nav_impact_pct * 0.8 / 100),
                'Own_Funds_Change': base_own_funds * nav_impact_pct * 0.8 / 100,
                'Own_Funds_Change_Pct': nav_impact_pct * 0.8,
                # SCR Impact
                'Base_SCR': base_scr,
                'Stressed_SCR': base_scr * random_percentage(95, 110) / 100,
                # Solvency Ratio
                'Base_Solvency_Ratio': base_own_funds / base_scr * 100,
                'Stressed_Solvency_Ratio': (base_own_funds * (1 + nav_impact_pct * 0.8 / 100)) / (base_scr * random_percentage(95, 110) / 100) * 100,
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


def generate_mr01_duration_analysis():
    """
    MR01 Duration Analysis - Interest rate sensitivity by duration bucket.
    """
    data = []

    duration_buckets = ['0-1y', '1-2y', '2-5y', '5-10y', '10-15y', '15-20y', '20-30y', '30y+']

    for undertaking in UNDERTAKINGS:
        total_assets = random_amount(500_000_000, 3_000_000_000)
        total_liabilities = total_assets * random_percentage(70, 95) / 100

        for bucket in duration_buckets:
            bucket_pct = random_percentage(5, 25)

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Duration_Bucket': bucket,
                # Asset Position
                'Asset_Value': total_assets * bucket_pct / 100,
                'Asset_Duration': random_percentage(0.5, 35),
                'Asset_DV01': total_assets * bucket_pct / 100 * random_percentage(0.005, 0.03),
                # Liability Position
                'Liability_Value': total_liabilities * bucket_pct * random_percentage(80, 120) / 10000,
                'Liability_Duration': random_percentage(0.5, 35),
                'Liability_DV01': total_liabilities * bucket_pct / 100 * random_percentage(0.005, 0.03),
                # Net Position
                'Net_DV01': random_amount(-5_000_000, 5_000_000),
                'Duration_Gap': random_percentage(-3, 3),
                # Sensitivity
                'Impact_100bps_Up': random_amount(-50_000_000, 50_000_000),
                'Impact_100bps_Down': random_amount(-50_000_000, 50_000_000),
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# QMC01 - Quarterly Model Change
# ============================================================================

def generate_qmc01_model_change():
    """
    QMC01 - Quarterly Model Change
    Reporting of internal model changes and their impact.
    """
    data = []

    change_types = [
        ('Parameter Update', 'Minor'),
        ('Methodology Enhancement', 'Minor'),
        ('Data Update', 'Minor'),
        ('Calibration Refinement', 'Minor'),
        ('New Risk Driver', 'Major'),
        ('Correlation Update', 'Major'),
        ('Model Extension', 'Major'),
        ('Regulatory Change', 'Major'),
    ]

    risk_modules = [
        'Market Risk', 'Credit Risk', 'Underwriting Risk - Non-Life',
        'Underwriting Risk - Life', 'Operational Risk', 'Aggregation'
    ]

    for undertaking in UNDERTAKINGS:
        if random.random() > 0.5:  # 50% have model changes to report
            for change_type, classification in random.sample(change_types, random.randint(1, 4)):
                scr_before = random_amount(100_000_000, 500_000_000)
                scr_impact_pct = random_percentage(-10, 10)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Quarter': 'Q4 2024',
                    'Change_ID': f'MC_{random.randint(10000, 99999)}',
                    'Change_Type': change_type,
                    'Change_Classification': classification,
                    'Risk_Module_Affected': random.choice(risk_modules),
                    'Description': f'{change_type} applied to {random.choice(risk_modules)} module',
                    'Rationale': random.choice([
                        'Improved risk capture',
                        'Updated market data',
                        'Enhanced calibration',
                        'Regulatory requirement',
                        'Model validation finding'
                    ]),
                    # Impact Assessment
                    'SCR_Before_Change': scr_before,
                    'SCR_After_Change': scr_before * (1 + scr_impact_pct / 100),
                    'SCR_Impact': scr_before * scr_impact_pct / 100,
                    'SCR_Impact_Pct': scr_impact_pct,
                    'Own_Funds_Impact': scr_before * scr_impact_pct / 100 * -0.3,
                    'Solvency_Ratio_Impact_PP': random_percentage(-5, 5),
                    # Dates
                    'Effective_Date': REPORTING_DATE,
                    'Approval_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') -
                                     timedelta(days=random.randint(7, 60))).strftime('%Y-%m-%d'),
                    # Governance
                    'Approval_Level': random.choice(['Model Change Committee', 'Board', 'Risk Committee']),
                    'PRA_Notification_Required': 'Yes' if classification == 'Major' else 'No',
                    'PRA_Notification_Date': (datetime.strptime(REPORTING_DATE, '%Y-%m-%d') -
                                             timedelta(days=random.randint(30, 90))).strftime('%Y-%m-%d') if classification == 'Major' else None,
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


def generate_qmc01_cumulative_changes():
    """
    QMC01 Cumulative Changes - Year-to-date model change summary.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        scr_start_of_year = random_amount(100_000_000, 500_000_000)

        # Cumulative changes by quarter
        quarters = ['Q1', 'Q2', 'Q3', 'Q4']
        cumulative_impact = 0

        for quarter in quarters:
            quarter_impact = random_percentage(-5, 5)
            cumulative_impact += quarter_impact

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Year': 2024,
                'Quarter': quarter,
                'Number_Of_Changes_Quarter': random.randint(0, 5),
                'Number_Of_Major_Changes': random.randint(0, 2),
                'Number_Of_Minor_Changes': random.randint(0, 4),
                'SCR_Start_Of_Year': scr_start_of_year,
                'Quarter_SCR_Impact_Pct': quarter_impact,
                'Quarter_SCR_Impact_Amount': scr_start_of_year * quarter_impact / 100,
                'Cumulative_SCR_Impact_Pct': cumulative_impact,
                'Cumulative_SCR_Impact_Amount': scr_start_of_year * cumulative_impact / 100,
                'SCR_End_Of_Quarter': scr_start_of_year * (1 + cumulative_impact / 100),
                'Material_Threshold_Pct': 5,
                'Within_Threshold': 'Yes' if abs(cumulative_impact) < 5 else 'No',
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# Power BI Execution
# ============================================================================

if __name__ == "__main__":
    print("Generating Special Template QRTs...")

# Generate all tables for Power BI
MALIR_Summary = generate_malir_summary()
MALIR_Portfolio_Details = generate_malir_portfolio_details()
MALIR_Asset_Listing = generate_malir_asset_listing()
MALIR_Liability_Analysis = generate_malir_liability_analysis()
MALIR_Cash_Flow_Matching = generate_malir_cash_flow_matching()
MALIR_Stress_Tests = generate_malir_stress_tests()
MR01_Market_Risk_Sensitivities = generate_mr01_market_risk_sensitivities()
MR01_Duration_Analysis = generate_mr01_duration_analysis()
QMC01_Model_Change = generate_qmc01_model_change()
QMC01_Cumulative_Changes = generate_qmc01_cumulative_changes()
