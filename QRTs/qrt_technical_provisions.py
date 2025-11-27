"""
PRA/BoE QRT Generator - Technical Provisions Templates (IR12-18)
================================================================
Actuarial-focused technical provisions templates for Solvency II reporting.

Templates:
- IR1201: Life Technical Provisions
- IR1203: Life Best Estimate Liabilities by Country
- IR1204: Best Estimate Assumptions for Life Insurance Risks
- IR1205: With-Profits Value of Bonus
- IR1206: With-Profits Liabilities and Assets
- IR1401: Life Obligations Analysis
- IR1601: Non-Life Annuities Information
- IR1602: Non-Life Annuities Projection of Future Cash Flows
- IR1701: Non-Life Technical Provisions
- IR1703: Non-Life Best Estimate Liabilities by Country
- IR1801: Non-Life Projection of Future Cash Flows
- IR1802: Non-Life Liability Projection of Future Cash Flows
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random
from typing import Dict, List

from .qrt_balance_sheet import (
    UNDERTAKINGS, REPORTING_DATE, CURRENCIES, COUNTRIES,
    NON_LIFE_LOB, LIFE_LOB, random_amount, random_percentage
)

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


# ============================================================================
# IR1201 - Life Technical Provisions
# ============================================================================

def generate_ir1201_life_technical_provisions():
    """
    IR1201 - Life Technical Provisions
    Comprehensive breakdown of life insurance technical provisions.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        for lob in LIFE_LOB:
            bel = random_amount(50_000_000, 500_000_000)
            rm = bel * np.random.uniform(0.03, 0.08)

            row = {
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Line_Of_Business': lob,
                # Best Estimate
                'Best_Estimate_Gross': bel,
                'Reinsurance_Recoverables': bel * np.random.uniform(0.05, 0.20),
                'Best_Estimate_Net': bel * np.random.uniform(0.80, 0.95),
                # Risk Margin
                'Risk_Margin': rm,
                # Technical Provisions Total
                'TP_Gross': bel + rm,
                'TP_Net': (bel * np.random.uniform(0.80, 0.95)) + rm,
                # BE Components
                'BE_Future_Premiums': bel * np.random.uniform(-0.15, -0.05),
                'BE_Future_Claims': bel * np.random.uniform(0.50, 0.70),
                'BE_Future_Expenses': bel * np.random.uniform(0.08, 0.15),
                'BE_Other_Cash_Flows': bel * np.random.uniform(0.05, 0.15),
                # Transitional Measures
                'Transitional_TP': random_amount(0, bel * 0.05),
                'Transitional_Interest_Rate': random_amount(0, bel * 0.03),
                # Matching Adjustment
                'Matching_Adjustment_Applied': random.choice([True, False]),
                'Matching_Adjustment_Amount': random_amount(0, bel * 0.02),
                # Volatility Adjustment
                'Volatility_Adjustment_Applied': random.choice([True, False]),
                'Volatility_Adjustment_Amount': random_amount(0, bel * 0.01),
                # Duration
                'Modified_Duration': round(np.random.uniform(5, 20), 2),
                'Average_Duration_Liabilities': round(np.random.uniform(8, 25), 2),
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR1203 - Life Best Estimate Liabilities by Country
# ============================================================================

def generate_ir1203_life_bel_by_country():
    """
    IR1203 - Life Best Estimate Liabilities by Country
    Geographic breakdown of life BEL.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        for country in COUNTRIES[:6]:
            for lob in LIFE_LOB[:4]:
                bel = random_amount(5_000_000, 80_000_000)

                row = {
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Country_Of_Risk': country,
                    'Line_Of_Business': lob,
                    'Best_Estimate_Gross': bel,
                    'Reinsurance_Recoverables': bel * np.random.uniform(0.05, 0.20),
                    'Best_Estimate_Net': bel * np.random.uniform(0.80, 0.95),
                    'BE_Death_Benefits': bel * np.random.uniform(0.15, 0.30),
                    'BE_Survival_Benefits': bel * np.random.uniform(0.30, 0.50),
                    'BE_Surrender_Benefits': bel * np.random.uniform(0.05, 0.15),
                    'BE_Other_Benefits': bel * np.random.uniform(0.10, 0.25),
                    'BE_Expenses': bel * np.random.uniform(0.05, 0.12),
                    'Number_Of_Policies': random.randint(1000, 50000),
                    'Sum_Insured': bel * np.random.uniform(3, 8),
                }
                data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR1204 - Best Estimate Assumptions for Life Insurance Risks
# ============================================================================

def generate_ir1204_life_be_assumptions():
    """
    IR1204 - Best Estimate Assumptions for Life Insurance Risks
    Key actuarial assumptions used in life BEL calculation.
    """
    data = []

    assumption_types = [
        ('Mortality', 'qx', 'Per mille'),
        ('Longevity', 'qx', 'Per mille'),
        ('Morbidity', 'i', 'Per mille'),
        ('Lapse', 'lapse_rate', 'Percentage'),
        ('Expense', 'expense_per_policy', 'GBP'),
        ('Expense_Inflation', 'inflation_rate', 'Percentage'),
        ('Discount_Rate', 'rate', 'Percentage'),
    ]

    for undertaking in UNDERTAKINGS:
        for lob in LIFE_LOB[:4]:
            for assumption_name, assumption_code, unit in assumption_types:
                row = {
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Line_Of_Business': lob,
                    'Assumption_Type': assumption_name,
                    'Assumption_Code': assumption_code,
                    'Unit': unit,
                    'Best_Estimate_Value': round(np.random.uniform(0.5, 5.0), 4),
                    'Upper_Bound': round(np.random.uniform(5.1, 8.0), 4),
                    'Lower_Bound': round(np.random.uniform(0.1, 0.4), 4),
                    'Year_1': round(np.random.uniform(0.5, 5.0), 4),
                    'Year_2': round(np.random.uniform(0.5, 5.0), 4),
                    'Year_5': round(np.random.uniform(0.5, 5.0), 4),
                    'Year_10': round(np.random.uniform(0.5, 5.0), 4),
                    'Year_20': round(np.random.uniform(0.5, 5.0), 4),
                    'Ultimate': round(np.random.uniform(0.5, 5.0), 4),
                    'Source': random.choice(['Internal Experience', 'Industry Tables', 'Regulatory Prescribed']),
                    'Last_Review_Date': '2024-06-30',
                }
                data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR1205 - With-Profits Value of Bonus
# ============================================================================

def generate_ir1205_with_profits_bonus():
    """
    IR1205 - With-Profits Value of Bonus
    Analysis of with-profits bonus provisions.
    """
    data = []

    bonus_types = ['Reversionary Bonus', 'Terminal Bonus', 'Special Bonus', 'Interim Bonus']

    for undertaking in UNDERTAKINGS:
        total_with_profits = random_amount(100_000_000, 800_000_000)

        for bonus_type in bonus_types:
            row = {
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Bonus_Type': bonus_type,
                'Opening_Value': random_amount(total_with_profits * 0.02, total_with_profits * 0.15),
                'Declared_Bonus': random_amount(total_with_profits * 0.005, total_with_profits * 0.03),
                'Claims_Paid': random_amount(total_with_profits * 0.01, total_with_profits * 0.05),
                'Surrenders': random_amount(total_with_profits * 0.005, total_with_profits * 0.02),
                'Other_Movements': random_amount(-total_with_profits * 0.01, total_with_profits * 0.01),
                'Closing_Value': random_amount(total_with_profits * 0.02, total_with_profits * 0.18),
                'Bonus_Rate_Declared': random_percentage(0.5, 3.5),
                'Asset_Share_Coverage': random_percentage(95, 110),
                'Smoothing_Adjustment': random_amount(-total_with_profits * 0.02, total_with_profits * 0.02),
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR1206 - With-Profits Liabilities and Assets
# ============================================================================

def generate_ir1206_with_profits_liabilities_assets():
    """
    IR1206 - With-Profits Liabilities and Assets
    With-profits fund asset-liability matching analysis.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        total_assets = random_amount(200_000_000, 1_000_000_000)
        total_liabilities = total_assets * np.random.uniform(0.85, 0.98)

        row = {
            'LEI': undertaking['lei'],
            'Undertaking_Name': undertaking['name'],
            'Reporting_Date': REPORTING_DATE,
            # Assets
            'Assets_Equities': total_assets * np.random.uniform(0.30, 0.50),
            'Assets_Fixed_Income': total_assets * np.random.uniform(0.30, 0.45),
            'Assets_Property': total_assets * np.random.uniform(0.05, 0.15),
            'Assets_Cash': total_assets * np.random.uniform(0.02, 0.08),
            'Assets_Other': total_assets * np.random.uniform(0.02, 0.10),
            'Total_Assets': total_assets,
            # Liabilities
            'Guaranteed_Benefits': total_liabilities * np.random.uniform(0.60, 0.80),
            'Future_Discretionary_Benefits': total_liabilities * np.random.uniform(0.10, 0.25),
            'Declared_Bonus_Not_Yet_Credited': total_liabilities * np.random.uniform(0.02, 0.08),
            'Expenses_Provision': total_liabilities * np.random.uniform(0.03, 0.08),
            'Total_Liabilities': total_liabilities,
            # Surplus
            'Free_Assets': total_assets - total_liabilities,
            'Estate_Ratio': round((total_assets - total_liabilities) / total_liabilities * 100, 2),
            # Risk Metrics
            'Equity_Backing_Ratio': random_percentage(30, 50),
            'Duration_Mismatch': round(np.random.uniform(-3, 3), 2),
            'Currency_Mismatch': random_percentage(0, 10),
        }
        data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR1401 - Life Obligations Analysis
# ============================================================================

def generate_ir1401_life_obligations():
    """
    IR1401 - Life Obligations Analysis
    Detailed analysis of life insurance obligations by policy characteristics.
    """
    data = []

    product_types = [
        'Term Assurance',
        'Whole of Life',
        'Endowment',
        'Pure Endowment',
        'Immediate Annuity',
        'Deferred Annuity',
        'Unit-Linked',
        'With-Profits',
    ]

    for undertaking in UNDERTAKINGS:
        for product in product_types:
            bel = random_amount(20_000_000, 200_000_000)

            row = {
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Product_Type': product,
                'Number_Of_Policies': random.randint(1000, 100000),
                'Sum_Insured': bel * np.random.uniform(5, 15),
                'Annual_Premium': bel * np.random.uniform(0.05, 0.15),
                'Best_Estimate': bel,
                'Risk_Margin': bel * np.random.uniform(0.03, 0.08),
                'Technical_Provisions': bel * np.random.uniform(1.03, 1.08),
                'Average_Age': round(np.random.uniform(35, 65), 1),
                'Average_Duration': round(np.random.uniform(5, 25), 1),
                'Average_Premium': round(bel * 0.1 / random.randint(1000, 100000), 2),
                'Persistency_Rate': random_percentage(85, 98),
                'Claim_Rate': random_percentage(0.1, 5.0),
                'New_Business_Strain': bel * np.random.uniform(-0.05, 0.05),
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR1601 - Non-Life Annuities Information
# ============================================================================

def generate_ir1601_non_life_annuities():
    """
    IR1601 - Non-Life Annuities Information
    Annuities arising from non-life insurance contracts.
    """
    data = []

    annuity_origins = [
        'Motor - Bodily Injury',
        'Employers Liability',
        'Public Liability',
        'Professional Indemnity',
        'Marine Personal Injury',
    ]

    for undertaking in UNDERTAKINGS:
        for origin in annuity_origins:
            bel = random_amount(5_000_000, 50_000_000)

            row = {
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Annuity_Origin': origin,
                'Number_Of_Annuitants': random.randint(50, 500),
                'Total_Annual_Payment': bel * np.random.uniform(0.04, 0.08),
                'Average_Age': round(np.random.uniform(45, 70), 1),
                'Average_Remaining_Duration': round(np.random.uniform(10, 30), 1),
                'Best_Estimate_Gross': bel,
                'Reinsurance_Recoverables': bel * np.random.uniform(0.10, 0.30),
                'Best_Estimate_Net': bel * np.random.uniform(0.70, 0.90),
                'Risk_Margin': bel * np.random.uniform(0.04, 0.10),
                'Technical_Provisions': bel * np.random.uniform(1.04, 1.10),
                'Mortality_Table_Used': random.choice(['PMA08', 'PFA08', 'S3PMA', 'S3PFA']),
                'Mortality_Improvement': random.choice(['CMI_2022', 'CMI_2023', 'None']),
                'Discount_Rate': random_percentage(1.0, 4.0),
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR1602 - Non-Life Annuities Projection of Future Cash Flows
# ============================================================================

def generate_ir1602_non_life_annuities_cash_flows():
    """
    IR1602 - Non-Life Annuities Projection of Future Cash Flows
    Cash flow projections for non-life annuity obligations.
    """
    data = []

    years = list(range(1, 51))  # 50 year projection

    for undertaking in UNDERTAKINGS:
        base_payment = random_amount(2_000_000, 10_000_000)

        for year in years:
            decay_factor = np.exp(-0.03 * year)  # Mortality run-off

            row = {
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Projection_Year': year,
                'Calendar_Year': 2024 + year,
                'Annuity_Payments': round(base_payment * decay_factor, 2),
                'Expenses': round(base_payment * decay_factor * 0.02, 2),
                'Reinsurance_Recoveries': round(base_payment * decay_factor * np.random.uniform(0.1, 0.3), 2),
                'Net_Cash_Flow': round(base_payment * decay_factor * np.random.uniform(0.68, 0.88), 2),
                'Discount_Factor': round(np.exp(-0.025 * year), 6),
                'Present_Value': round(base_payment * decay_factor * np.exp(-0.025 * year), 2),
                'Number_Of_Annuitants': max(1, int(200 * decay_factor)),
                'Cumulative_PV': round(base_payment * (1 - np.exp(-0.025 * year)) / 0.025, 2),
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR1701 - Non-Life Technical Provisions
# ============================================================================

def generate_ir1701_non_life_technical_provisions():
    """
    IR1701 - Non-Life Technical Provisions
    Comprehensive breakdown of non-life insurance technical provisions.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        for lob in NON_LIFE_LOB:
            claims_provision = random_amount(20_000_000, 300_000_000)
            premium_provision = random_amount(5_000_000, 100_000_000)

            row = {
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Line_Of_Business': lob,
                # Claims Provision
                'Claims_Provision_Gross': claims_provision,
                'Claims_Provision_RI_Recoverables': claims_provision * np.random.uniform(0.15, 0.35),
                'Claims_Provision_Net': claims_provision * np.random.uniform(0.65, 0.85),
                # Premium Provision
                'Premium_Provision_Gross': premium_provision,
                'Premium_Provision_RI_Recoverables': premium_provision * np.random.uniform(0.10, 0.25),
                'Premium_Provision_Net': premium_provision * np.random.uniform(0.75, 0.90),
                # Best Estimate
                'Best_Estimate_Claims': claims_provision * np.random.uniform(0.92, 0.98),
                'Best_Estimate_Premium': premium_provision * np.random.uniform(0.92, 0.98),
                'Best_Estimate_Total': (claims_provision + premium_provision) * np.random.uniform(0.92, 0.98),
                # Risk Margin
                'Risk_Margin': (claims_provision + premium_provision) * np.random.uniform(0.04, 0.08),
                # Total Technical Provisions
                'TP_Gross': claims_provision + premium_provision,
                'TP_RI_Recoverables': (claims_provision + premium_provision) * np.random.uniform(0.12, 0.30),
                'TP_Net': (claims_provision + premium_provision) * np.random.uniform(0.70, 0.88),
                # ENID
                'ENID_Adjustment': (claims_provision + premium_provision) * np.random.uniform(0.01, 0.05),
                # Duration
                'Modified_Duration': round(np.random.uniform(1.5, 5.0), 2),
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR1703 - Non-Life Best Estimate Liabilities by Country
# ============================================================================

def generate_ir1703_non_life_bel_by_country():
    """
    IR1703 - Non-Life Best Estimate Liabilities by Country
    Geographic breakdown of non-life BEL.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        for country in COUNTRIES[:8]:
            for lob in NON_LIFE_LOB[:8]:
                bel = random_amount(3_000_000, 50_000_000)

                row = {
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Country_Of_Risk': country,
                    'Line_Of_Business': lob,
                    'Claims_Provision_BE': bel * np.random.uniform(0.65, 0.80),
                    'Premium_Provision_BE': bel * np.random.uniform(0.20, 0.35),
                    'Best_Estimate_Gross': bel,
                    'RI_Recoverables': bel * np.random.uniform(0.15, 0.30),
                    'Best_Estimate_Net': bel * np.random.uniform(0.70, 0.85),
                    'IBNR': bel * np.random.uniform(0.20, 0.40),
                    'Case_Reserves': bel * np.random.uniform(0.30, 0.50),
                    'ULAE': bel * np.random.uniform(0.02, 0.06),
                    'ENID': bel * np.random.uniform(0.01, 0.04),
                    'Binary_Events': bel * np.random.uniform(0.005, 0.02),
                }
                data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR1801 - Non-Life Projection of Future Cash Flows
# ============================================================================

def generate_ir1801_non_life_cash_flows():
    """
    IR1801 - Non-Life Projection of Future Cash Flows
    Cash flow projections for non-life insurance obligations.
    """
    data = []

    years = list(range(1, 21))  # 20 year projection

    for undertaking in UNDERTAKINGS:
        for lob in NON_LIFE_LOB[:6]:
            base_claims = random_amount(10_000_000, 80_000_000)

            for year in years:
                decay = np.exp(-0.25 * year)  # Claims run-off pattern

                row = {
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Line_Of_Business': lob,
                    'Projection_Year': year,
                    'Calendar_Year': 2024 + year,
                    # Outflows
                    'Claims_Payments': round(base_claims * decay, 2),
                    'Expenses_Claims_Handling': round(base_claims * decay * 0.08, 2),
                    'Expenses_Administration': round(base_claims * decay * 0.03, 2),
                    'Total_Outflows': round(base_claims * decay * 1.11, 2),
                    # Inflows
                    'Premium_Receivables': round(base_claims * decay * 0.15 if year <= 2 else 0, 2),
                    'RI_Recoveries': round(base_claims * decay * np.random.uniform(0.15, 0.30), 2),
                    'Salvage_Subrogation': round(base_claims * decay * np.random.uniform(0.02, 0.08), 2),
                    'Total_Inflows': round(base_claims * decay * np.random.uniform(0.20, 0.45), 2),
                    # Net
                    'Net_Cash_Flow': round(base_claims * decay * np.random.uniform(0.65, 0.85), 2),
                    'Discount_Factor': round(np.exp(-0.025 * year), 6),
                    'Present_Value': round(base_claims * decay * np.exp(-0.025 * year), 2),
                }
                data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR1802 - Non-Life Liability Projection of Future Cash Flows
# ============================================================================

def generate_ir1802_non_life_liability_cash_flows():
    """
    IR1802 - Non-Life Liability Projection of Future Cash Flows
    Detailed liability cash flow projections by development period.
    """
    data = []

    development_periods = list(range(0, 11))  # 0-10 years development

    for undertaking in UNDERTAKINGS:
        for lob in NON_LIFE_LOB[:8]:
            ultimate_loss = random_amount(50_000_000, 300_000_000)

            for dev_period in development_periods:
                # Typical development pattern
                if dev_period == 0:
                    cumulative_pct = 0.35
                elif dev_period == 1:
                    cumulative_pct = 0.60
                elif dev_period == 2:
                    cumulative_pct = 0.75
                elif dev_period == 3:
                    cumulative_pct = 0.85
                elif dev_period == 4:
                    cumulative_pct = 0.92
                else:
                    cumulative_pct = min(1.0, 0.92 + 0.015 * (dev_period - 4))

                incremental_pct = cumulative_pct - (0 if dev_period == 0 else
                                                    0.35 if dev_period == 1 else
                                                    0.60 if dev_period == 2 else
                                                    0.75 if dev_period == 3 else
                                                    0.85 if dev_period == 4 else
                                                    min(1.0, 0.92 + 0.015 * (dev_period - 5)))

                row = {
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Line_Of_Business': lob,
                    'Development_Year': dev_period,
                    'Calendar_Year': 2024 + dev_period,
                    'Incremental_Claims_Paid': round(ultimate_loss * incremental_pct, 2),
                    'Cumulative_Claims_Paid': round(ultimate_loss * cumulative_pct, 2),
                    'Outstanding_Reserve': round(ultimate_loss * (1 - cumulative_pct), 2),
                    'IBNR': round(ultimate_loss * (1 - cumulative_pct) * np.random.uniform(0.3, 0.6), 2),
                    'Case_Reserves': round(ultimate_loss * (1 - cumulative_pct) * np.random.uniform(0.4, 0.7), 2),
                    'Ultimate_Loss': ultimate_loss,
                    'Development_Factor': round(1 / cumulative_pct if cumulative_pct > 0 else 999, 4),
                    'Incremental_Percentage': round(incremental_pct * 100, 2),
                    'Cumulative_Percentage': round(cumulative_pct * 100, 2),
                }
                data.append(row)

    return pd.DataFrame(data)


# Export all functions
__all__ = [
    'generate_ir1201_life_technical_provisions',
    'generate_ir1203_life_bel_by_country',
    'generate_ir1204_life_be_assumptions',
    'generate_ir1205_with_profits_bonus',
    'generate_ir1206_with_profits_liabilities_assets',
    'generate_ir1401_life_obligations',
    'generate_ir1601_non_life_annuities',
    'generate_ir1602_non_life_annuities_cash_flows',
    'generate_ir1701_non_life_technical_provisions',
    'generate_ir1703_non_life_bel_by_country',
    'generate_ir1801_non_life_cash_flows',
    'generate_ir1802_non_life_liability_cash_flows',
]
