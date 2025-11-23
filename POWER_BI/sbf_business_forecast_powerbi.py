# Syndicate Business Forecast (SBF) - Power BI Data Generator
# Three-Year Business Plan Required for All Lloyd's Syndicates
#
# Generates 10 tables covering:
# - Income statements and 3-year forecasts
# - Premium projections by LOB and geography
# - Claims ratios, expense budgets, capacity plans
# - Reinsurance strategy and investment income
# - Combined ratio targets and stress scenarios
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
CURRENT_YEAR = 2024
FORECAST_YEARS = [2024, 2025, 2026]

# Lloyd's Lines of Business
LINES_OF_BUSINESS = [
    ('PR', 'Property Direct', 0.18),
    ('CA', 'Casualty Direct', 0.15),
    ('MA', 'Marine Direct', 0.08),
    ('AV', 'Aviation Direct', 0.05),
    ('EN', 'Energy Direct', 0.07),
    ('MO', 'Motor Direct', 0.04),
    ('PA', 'Accident & Health', 0.06),
    ('CR', 'Credit & Surety', 0.03),
    ('PR_RI', 'Property Reinsurance', 0.14),
    ('CA_RI', 'Casualty Reinsurance', 0.10),
    ('MA_RI', 'Marine Reinsurance', 0.05),
    ('SP', 'Specialty', 0.05)
]

# Geographic Regions
GEOGRAPHIES = [
    ('US', 'United States', 0.35),
    ('UK', 'United Kingdom', 0.20),
    ('EU', 'European Union', 0.15),
    ('APAC', 'Asia Pacific', 0.12),
    ('LATAM', 'Latin America', 0.08),
    ('MEA', 'Middle East & Africa', 0.05),
    ('CAN', 'Canada', 0.05)
]

# =============================================================================
# SBF_001_Control - Submission metadata
# =============================================================================
def generate_sbf_001_control():
    records = []
    for syn in SYNDICATES:
        base_capacity = np.random.uniform(200, 800)
        records.append({
            'Syndicate': syn,
            'PlanYear': CURRENT_YEAR,
            'SubmissionDate': datetime(CURRENT_YEAR, 8, 31),
            'ManagingAgent': f'MA{syn % 100:03d}',
            'SyndicateName': f'Syndicate {syn}',
            'BusinessType': np.random.choice(['Diversified', 'Specialist', 'Reinsurance'], p=[0.5, 0.35, 0.15]),
            'CurrentCapacity_GBP_M': round(base_capacity, 1),
            'ProposedCapacity_Y1_GBP_M': round(base_capacity * np.random.uniform(1.0, 1.15), 1),
            'ProposedCapacity_Y2_GBP_M': round(base_capacity * np.random.uniform(1.0, 1.25), 1),
            'ProposedCapacity_Y3_GBP_M': round(base_capacity * np.random.uniform(1.0, 1.35), 1),
            'PlanStatus': 'Submitted',
            'ApprovalStatus': np.random.choice(['Approved', 'Under Review', 'Conditional'], p=[0.7, 0.2, 0.1])
        })
    return pd.DataFrame(records)

# =============================================================================
# SBF_010_Income_Statement - Projected P&L for 3 years
# =============================================================================
def generate_sbf_010_income_statement():
    records = []
    for syn in SYNDICATES:
        base_gwp = np.random.uniform(200, 600)
        growth_rate = np.random.uniform(-0.05, 0.20)

        for i, year in enumerate(FORECAST_YEARS):
            gwp = base_gwp * (1 + growth_rate) ** i

            # Calculate components
            acquisition_cost_ratio = np.random.uniform(0.25, 0.35)
            admin_expense_ratio = np.random.uniform(0.08, 0.15)
            loss_ratio = np.random.uniform(0.50, 0.75)
            ri_cost_ratio = np.random.uniform(0.05, 0.15)

            nwp = gwp * (1 - ri_cost_ratio)
            nep = nwp * np.random.uniform(0.90, 1.00)  # Earned adjustment

            claims_incurred = nep * loss_ratio
            acquisition_costs = nep * acquisition_cost_ratio
            admin_expenses = nep * admin_expense_ratio

            technical_result = nep - claims_incurred - acquisition_costs - admin_expenses
            investment_income = base_gwp * np.random.uniform(0.02, 0.05)
            other_income = base_gwp * np.random.uniform(0, 0.02)

            profit_before_tax = technical_result + investment_income + other_income
            tax = profit_before_tax * 0.19 if profit_before_tax > 0 else 0
            profit_after_tax = profit_before_tax - tax

            combined_ratio = (claims_incurred + acquisition_costs + admin_expenses) / nep * 100

            records.append({
                'Syndicate': syn,
                'ForecastYear': year,
                'YearType': 'Actual' if year == CURRENT_YEAR else 'Forecast',
                'GWP_GBP_M': round(gwp, 2),
                'RI_Premium_Ceded_GBP_M': round(gwp * ri_cost_ratio, 2),
                'NWP_GBP_M': round(nwp, 2),
                'NEP_GBP_M': round(nep, 2),
                'ClaimsIncurred_GBP_M': round(claims_incurred, 2),
                'AcquisitionCosts_GBP_M': round(acquisition_costs, 2),
                'AdminExpenses_GBP_M': round(admin_expenses, 2),
                'TechnicalResult_GBP_M': round(technical_result, 2),
                'InvestmentIncome_GBP_M': round(investment_income, 2),
                'OtherIncome_GBP_M': round(other_income, 2),
                'ProfitBeforeTax_GBP_M': round(profit_before_tax, 2),
                'Tax_GBP_M': round(tax, 2),
                'ProfitAfterTax_GBP_M': round(profit_after_tax, 2),
                'LossRatio_Pct': round(loss_ratio * 100, 1),
                'AcquisitionRatio_Pct': round(acquisition_cost_ratio * 100, 1),
                'AdminRatio_Pct': round(admin_expense_ratio * 100, 1),
                'CombinedRatio_Pct': round(combined_ratio, 1),
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# SBF_020_Premium_Forecast - Premium by LOB and geography
# =============================================================================
def generate_sbf_020_premium_forecast():
    records = []
    for syn in SYNDICATES:
        base_gwp = np.random.uniform(200, 600)
        growth_rate = np.random.uniform(-0.05, 0.20)

        # Generate LOB weights (vary by syndicate)
        lob_weights = {lob[0]: lob[2] * np.random.uniform(0.5, 1.5) for lob in LINES_OF_BUSINESS}
        total_weight = sum(lob_weights.values())
        lob_weights = {k: v/total_weight for k, v in lob_weights.items()}

        for year_idx, year in enumerate(FORECAST_YEARS):
            year_gwp = base_gwp * (1 + growth_rate) ** year_idx

            for lob_code, lob_name, _ in LINES_OF_BUSINESS:
                lob_gwp = year_gwp * lob_weights[lob_code]
                lob_growth = np.random.uniform(-0.10, 0.25)

                records.append({
                    'Syndicate': syn,
                    'ForecastYear': year,
                    'LOB_Code': lob_code,
                    'LOB_Name': lob_name,
                    'GWP_GBP_M': round(lob_gwp, 2),
                    'NWP_GBP_M': round(lob_gwp * np.random.uniform(0.85, 0.95), 2),
                    'GrowthRate_Pct': round(lob_growth * 100, 1),
                    'RateChange_Pct': round(np.random.uniform(-5, 15), 1),
                    'ExposureChange_Pct': round(np.random.uniform(-10, 20), 1),
                    'MarketShare_Pct': round(np.random.uniform(0.5, 5), 2),
                    'Currency': 'GBP'
                })
    return pd.DataFrame(records)

# =============================================================================
# SBF_030_Claims_Forecast - Expected loss ratios and claims
# =============================================================================
def generate_sbf_030_claims_forecast():
    records = []
    for syn in SYNDICATES:
        for year in FORECAST_YEARS:
            for lob_code, lob_name, _ in LINES_OF_BUSINESS:
                # Different LOBs have different base loss ratios
                if 'RI' in lob_code:
                    base_lr = np.random.uniform(0.55, 0.75)
                elif lob_code in ['CA', 'PA']:
                    base_lr = np.random.uniform(0.60, 0.80)
                else:
                    base_lr = np.random.uniform(0.45, 0.70)

                attritional_lr = base_lr * np.random.uniform(0.70, 0.85)
                large_loss_lr = base_lr * np.random.uniform(0.10, 0.20)
                cat_loss_lr = base_lr * np.random.uniform(0.05, 0.15)

                nep = np.random.uniform(10, 100)

                records.append({
                    'Syndicate': syn,
                    'ForecastYear': year,
                    'LOB_Code': lob_code,
                    'LOB_Name': lob_name,
                    'NEP_GBP_M': round(nep, 2),
                    'ExpectedLossRatio_Pct': round(base_lr * 100, 1),
                    'AttritionalLR_Pct': round(attritional_lr * 100, 1),
                    'LargeLossLR_Pct': round(large_loss_lr * 100, 1),
                    'CatLossLR_Pct': round(cat_loss_lr * 100, 1),
                    'IBNR_Pct_Claims': round(np.random.uniform(15, 40), 1),
                    'PriorYearDevelopment_Pct': round(np.random.uniform(-5, 5), 1),
                    'Currency': 'GBP'
                })
    return pd.DataFrame(records)

# =============================================================================
# SBF_040_Expense_Budget - Acquisition and admin expenses
# =============================================================================
def generate_sbf_040_expense_budget():
    records = []
    expense_categories = [
        ('BROK', 'Brokerage', 0.15),
        ('COMM', 'Commission', 0.12),
        ('STAFF', 'Staff Costs', 0.06),
        ('IT', 'IT & Systems', 0.02),
        ('RENT', 'Premises & Rent', 0.01),
        ('PROF', 'Professional Fees', 0.015),
        ('MARKETING', 'Marketing & Business Dev', 0.01),
        ('OTHER', 'Other Admin', 0.015)
    ]

    for syn in SYNDICATES:
        base_gwp = np.random.uniform(200, 600)

        for year_idx, year in enumerate(FORECAST_YEARS):
            year_gwp = base_gwp * (1 + np.random.uniform(-0.05, 0.20)) ** year_idx
            year_nep = year_gwp * np.random.uniform(0.85, 0.95)

            for exp_code, exp_name, base_ratio in expense_categories:
                ratio = base_ratio * np.random.uniform(0.8, 1.2)
                amount = year_nep * ratio

                records.append({
                    'Syndicate': syn,
                    'ForecastYear': year,
                    'ExpenseCategory_Code': exp_code,
                    'ExpenseCategory_Name': exp_name,
                    'ExpenseType': 'Acquisition' if exp_code in ['BROK', 'COMM'] else 'Administrative',
                    'Amount_GBP_M': round(amount, 2),
                    'Ratio_Pct_NEP': round(ratio * 100, 2),
                    'YoY_Change_Pct': round(np.random.uniform(-10, 15), 1),
                    'Currency': 'GBP'
                })
    return pd.DataFrame(records)

# =============================================================================
# SBF_050_Capacity_Plan - Stamp capacity and utilization
# =============================================================================
def generate_sbf_050_capacity_plan():
    records = []
    for syn in SYNDICATES:
        base_capacity = np.random.uniform(200, 800)

        for year_idx, year in enumerate(FORECAST_YEARS):
            capacity = base_capacity * (1 + np.random.uniform(0, 0.15)) ** year_idx
            gwp = capacity * np.random.uniform(0.70, 0.95)  # Utilization
            utilization = gwp / capacity

            records.append({
                'Syndicate': syn,
                'ForecastYear': year,
                'StampCapacity_GBP_M': round(capacity, 2),
                'GWP_Forecast_GBP_M': round(gwp, 2),
                'Utilization_Pct': round(utilization * 100, 1),
                'CapacityChange_Pct': round(np.random.uniform(-5, 15), 1),
                'NewCapitalRequired_GBP_M': round(capacity * np.random.uniform(0, 0.1), 2),
                'CapacityHeadroom_GBP_M': round(capacity - gwp, 2),
                'MinimumCapacity_GBP_M': round(capacity * 0.5, 2),
                'MaximumCapacity_GBP_M': round(capacity * 1.5, 2),
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# SBF_060_Reinsurance_Strategy - RI program structure
# =============================================================================
def generate_sbf_060_reinsurance_strategy():
    records = []
    ri_programs = [
        ('QS', 'Quota Share', 'Proportional'),
        ('SS', 'Surplus Share', 'Proportional'),
        ('XOL', 'Excess of Loss', 'Non-Proportional'),
        ('CAT', 'Catastrophe XOL', 'Non-Proportional'),
        ('AGG', 'Aggregate Cover', 'Non-Proportional'),
        ('FAC', 'Facultative', 'Both')
    ]

    for syn in SYNDICATES:
        base_gwp = np.random.uniform(200, 600)

        for year in FORECAST_YEARS:
            for ri_code, ri_name, ri_type in ri_programs:
                if ri_code == 'QS':
                    cession_rate = np.random.uniform(0.10, 0.30)
                    premium_ceded = base_gwp * cession_rate
                elif ri_code == 'CAT':
                    cession_rate = 0
                    premium_ceded = base_gwp * np.random.uniform(0.02, 0.05)
                else:
                    cession_rate = np.random.uniform(0, 0.15)
                    premium_ceded = base_gwp * np.random.uniform(0.01, 0.05)

                records.append({
                    'Syndicate': syn,
                    'ForecastYear': year,
                    'RI_Program_Code': ri_code,
                    'RI_Program_Name': ri_name,
                    'RI_Type': ri_type,
                    'CessionRate_Pct': round(cession_rate * 100, 1),
                    'PremiumCeded_GBP_M': round(premium_ceded, 2),
                    'ExpectedRecovery_GBP_M': round(premium_ceded * np.random.uniform(0.5, 1.5), 2),
                    'RetentionLimit_GBP_M': round(np.random.uniform(1, 10), 2),
                    'CoverLimit_GBP_M': round(np.random.uniform(50, 200), 2),
                    'RI_Commission_Pct': round(np.random.uniform(20, 35), 1) if ri_type == 'Proportional' else 0,
                    'Currency': 'GBP'
                })
    return pd.DataFrame(records)

# =============================================================================
# SBF_070_Investment_Income - Investment return assumptions
# =============================================================================
def generate_sbf_070_investment_income():
    records = []
    asset_classes = [
        ('GOVT', 'Government Bonds', 0.40, 0.03),
        ('CORP', 'Corporate Bonds', 0.30, 0.04),
        ('CASH', 'Cash & Equivalents', 0.15, 0.02),
        ('EQ', 'Equities', 0.05, 0.07),
        ('PROP', 'Property', 0.05, 0.05),
        ('ALT', 'Alternative Investments', 0.05, 0.06)
    ]

    for syn in SYNDICATES:
        total_assets = np.random.uniform(300, 900)

        for year in FORECAST_YEARS:
            for asset_code, asset_name, base_alloc, base_return in asset_classes:
                allocation = base_alloc * np.random.uniform(0.7, 1.3)
                invested_amount = total_assets * allocation
                expected_return = base_return * np.random.uniform(0.7, 1.3)
                investment_income = invested_amount * expected_return

                records.append({
                    'Syndicate': syn,
                    'ForecastYear': year,
                    'AssetClass_Code': asset_code,
                    'AssetClass_Name': asset_name,
                    'Allocation_Pct': round(allocation * 100, 1),
                    'InvestedAmount_GBP_M': round(invested_amount, 2),
                    'ExpectedReturn_Pct': round(expected_return * 100, 2),
                    'InvestmentIncome_GBP_M': round(investment_income, 2),
                    'Duration_Years': round(np.random.uniform(1, 7), 1),
                    'CreditRating': np.random.choice(['AAA', 'AA', 'A', 'BBB', 'BB']) if 'Bond' in asset_name else 'N/A',
                    'Currency': 'GBP'
                })
    return pd.DataFrame(records)

# =============================================================================
# SBF_080_Combined_Ratios - Target combined ratios by LOB
# =============================================================================
def generate_sbf_080_combined_ratios():
    records = []
    for syn in SYNDICATES:
        for year in FORECAST_YEARS:
            for lob_code, lob_name, _ in LINES_OF_BUSINESS:
                # Different LOBs have different target ratios
                if 'RI' in lob_code:
                    target_lr = np.random.uniform(0.55, 0.70)
                elif lob_code in ['CA', 'PA']:
                    target_lr = np.random.uniform(0.60, 0.75)
                else:
                    target_lr = np.random.uniform(0.50, 0.65)

                expense_ratio = np.random.uniform(0.28, 0.38)
                combined_ratio = target_lr + expense_ratio

                records.append({
                    'Syndicate': syn,
                    'ForecastYear': year,
                    'LOB_Code': lob_code,
                    'LOB_Name': lob_name,
                    'TargetLossRatio_Pct': round(target_lr * 100, 1),
                    'TargetExpenseRatio_Pct': round(expense_ratio * 100, 1),
                    'TargetCombinedRatio_Pct': round(combined_ratio * 100, 1),
                    'Historical_3Yr_Avg_CR_Pct': round((combined_ratio + np.random.uniform(-0.05, 0.10)) * 100, 1),
                    'BestCase_CR_Pct': round((combined_ratio - np.random.uniform(0.05, 0.10)) * 100, 1),
                    'WorstCase_CR_Pct': round((combined_ratio + np.random.uniform(0.10, 0.20)) * 100, 1),
                    'Probability_Target_Met_Pct': round(np.random.uniform(50, 80), 1)
                })
    return pd.DataFrame(records)

# =============================================================================
# SBF_090_Stress_Scenarios - Downside scenario analysis
# =============================================================================
def generate_sbf_090_stress_scenarios():
    records = []
    scenarios = [
        ('BASE', 'Base Case', 1.0),
        ('MILD', 'Mild Stress', 0.85),
        ('MOD', 'Moderate Stress', 0.65),
        ('SEV', 'Severe Stress', 0.40),
        ('EXTR', 'Extreme Stress', 0.15),
        ('CAT1', '1-in-100 Cat Event', 0.50),
        ('CAT2', '1-in-250 Cat Event', 0.25),
        ('RATE', 'Rate Reduction 10%', 0.70),
        ('RES', 'Reserve Deterioration', 0.60),
        ('COMBO', 'Combined Adverse', 0.30)
    ]

    for syn in SYNDICATES:
        base_profit = np.random.uniform(20, 80)
        base_capital = np.random.uniform(150, 400)
        base_scr = base_capital * np.random.uniform(0.5, 0.8)

        for year in FORECAST_YEARS:
            for scen_code, scen_name, profit_factor in scenarios:
                profit_impact = base_profit * (profit_factor - 1) if scen_code != 'BASE' else 0
                capital_impact = profit_impact * np.random.uniform(0.8, 1.2)
                stressed_profit = base_profit + profit_impact
                stressed_capital = base_capital + capital_impact
                coverage_ratio = stressed_capital / base_scr

                records.append({
                    'Syndicate': syn,
                    'ForecastYear': year,
                    'Scenario_Code': scen_code,
                    'Scenario_Name': scen_name,
                    'BaseProfit_GBP_M': round(base_profit, 2),
                    'ProfitImpact_GBP_M': round(profit_impact, 2),
                    'StressedProfit_GBP_M': round(stressed_profit, 2),
                    'BaseCapital_GBP_M': round(base_capital, 2),
                    'CapitalImpact_GBP_M': round(capital_impact, 2),
                    'StressedCapital_GBP_M': round(stressed_capital, 2),
                    'SCR_GBP_M': round(base_scr, 2),
                    'CoverageRatio_Stressed': round(coverage_ratio, 2),
                    'CoverageRatio_Pct': round(coverage_ratio * 100, 1),
                    'PassFail': 'Pass' if coverage_ratio >= 1.0 else 'Fail',
                    'Currency': 'GBP'
                })
    return pd.DataFrame(records)

# =============================================================================
# Generate all tables
# =============================================================================

# Control
SBF_001_Control = generate_sbf_001_control()

# Income and forecasts
SBF_010_Income_Statement = generate_sbf_010_income_statement()
SBF_020_Premium_Forecast = generate_sbf_020_premium_forecast()
SBF_030_Claims_Forecast = generate_sbf_030_claims_forecast()
SBF_040_Expense_Budget = generate_sbf_040_expense_budget()

# Capacity and strategy
SBF_050_Capacity_Plan = generate_sbf_050_capacity_plan()
SBF_060_Reinsurance_Strategy = generate_sbf_060_reinsurance_strategy()
SBF_070_Investment_Income = generate_sbf_070_investment_income()

# Performance targets
SBF_080_Combined_Ratios = generate_sbf_080_combined_ratios()
SBF_090_Stress_Scenarios = generate_sbf_090_stress_scenarios()

# Summary statistics
print(f"SBF_001_Control: {len(SBF_001_Control)} rows")
print(f"SBF_010_Income_Statement: {len(SBF_010_Income_Statement)} rows")
print(f"SBF_020_Premium_Forecast: {len(SBF_020_Premium_Forecast)} rows")
print(f"SBF_030_Claims_Forecast: {len(SBF_030_Claims_Forecast)} rows")
print(f"SBF_040_Expense_Budget: {len(SBF_040_Expense_Budget)} rows")
print(f"SBF_050_Capacity_Plan: {len(SBF_050_Capacity_Plan)} rows")
print(f"SBF_060_Reinsurance_Strategy: {len(SBF_060_Reinsurance_Strategy)} rows")
print(f"SBF_070_Investment_Income: {len(SBF_070_Investment_Income)} rows")
print(f"SBF_080_Combined_Ratios: {len(SBF_080_Combined_Ratios)} rows")
print(f"SBF_090_Stress_Scenarios: {len(SBF_090_Stress_Scenarios)} rows")
