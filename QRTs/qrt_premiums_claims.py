"""
PRA/BoE QRT Generator - Premiums and Claims Templates (IR05)
=============================================================
Actuarial-focused premiums and claims templates for Solvency II reporting.

Templates:
- IR0502: Premiums, Claims and Expenses by Country
- IR0503: Life Income and Expenditure
- IR0504: Non-Life Income, Expenditure and Business Model Analysis
- IR0505: Life Premiums and Claims by Country
- IR0506: Non-Life Premiums and Claims by Country
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
# IR0502 - Premiums, Claims and Expenses by Country
# ============================================================================

def generate_ir0502_premiums_claims_by_country():
    """
    IR0502 - Premiums, Claims and Expenses by Country
    Geographic breakdown of underwriting performance.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        for country in COUNTRIES[:8]:  # Top 8 countries
            for lob in NON_LIFE_LOB[:6]:  # Main lines of business
                gwp = random_amount(5_000_000, 50_000_000)
                claims_ratio = np.random.uniform(0.50, 0.85)
                expense_ratio = np.random.uniform(0.25, 0.40)

                row = {
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Country': country,
                    'Line_Of_Business': lob,
                    'Gross_Written_Premium': gwp,
                    'Gross_Earned_Premium': gwp * np.random.uniform(0.85, 0.98),
                    'Reinsurance_Premium_Ceded': gwp * np.random.uniform(0.15, 0.35),
                    'Net_Written_Premium': gwp * np.random.uniform(0.65, 0.85),
                    'Net_Earned_Premium': gwp * np.random.uniform(0.60, 0.80),
                    'Gross_Claims_Incurred': gwp * claims_ratio,
                    'Reinsurance_Recoveries': gwp * claims_ratio * np.random.uniform(0.15, 0.35),
                    'Net_Claims_Incurred': gwp * claims_ratio * np.random.uniform(0.65, 0.85),
                    'Gross_Claims_Paid': gwp * claims_ratio * np.random.uniform(0.70, 0.90),
                    'Reinsurance_Recoveries_Paid': gwp * claims_ratio * np.random.uniform(0.10, 0.25),
                    'Net_Claims_Paid': gwp * claims_ratio * np.random.uniform(0.50, 0.75),
                    'Acquisition_Costs': gwp * np.random.uniform(0.15, 0.25),
                    'Administrative_Expenses': gwp * expense_ratio * np.random.uniform(0.20, 0.35),
                    'Other_Expenses': gwp * np.random.uniform(0.02, 0.08),
                    'Total_Expenses': gwp * expense_ratio,
                    'Combined_Ratio': round((claims_ratio + expense_ratio) * 100, 2),
                    'Loss_Ratio': round(claims_ratio * 100, 2),
                    'Expense_Ratio': round(expense_ratio * 100, 2),
                }
                data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR0503 - Life Income and Expenditure
# ============================================================================

def generate_ir0503_life_income_expenditure():
    """
    IR0503 - Life Income and Expenditure
    Life insurance revenue and cost breakdown.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        for lob in LIFE_LOB:
            gwp = random_amount(10_000_000, 100_000_000)

            row = {
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Line_Of_Business': lob,
                # Premiums
                'Gross_Written_Premium': gwp,
                'Gross_Earned_Premium': gwp * np.random.uniform(0.92, 0.99),
                'Reinsurance_Premium_Ceded': gwp * np.random.uniform(0.05, 0.20),
                'Net_Written_Premium': gwp * np.random.uniform(0.80, 0.95),
                'Net_Earned_Premium': gwp * np.random.uniform(0.78, 0.93),
                # Claims
                'Claims_Paid_Death': gwp * np.random.uniform(0.15, 0.30),
                'Claims_Paid_Maturity': gwp * np.random.uniform(0.20, 0.40),
                'Claims_Paid_Surrender': gwp * np.random.uniform(0.05, 0.15),
                'Claims_Paid_Annuity': gwp * np.random.uniform(0.10, 0.25),
                'Claims_Paid_Other': gwp * np.random.uniform(0.02, 0.08),
                'Total_Claims_Paid': gwp * np.random.uniform(0.55, 0.75),
                'Change_In_TP': gwp * np.random.uniform(-0.10, 0.20),
                # Expenses
                'Acquisition_Costs': gwp * np.random.uniform(0.08, 0.15),
                'Administrative_Expenses': gwp * np.random.uniform(0.05, 0.12),
                'Investment_Management_Expenses': gwp * np.random.uniform(0.02, 0.05),
                'Claims_Management_Expenses': gwp * np.random.uniform(0.01, 0.04),
                'Other_Expenses': gwp * np.random.uniform(0.01, 0.05),
                'Total_Expenses': gwp * np.random.uniform(0.18, 0.35),
                # Investment Income
                'Investment_Income': gwp * np.random.uniform(0.15, 0.40),
                'Realised_Gains': gwp * np.random.uniform(-0.05, 0.15),
                'Unrealised_Gains': gwp * np.random.uniform(-0.10, 0.20),
                'Total_Investment_Return': gwp * np.random.uniform(0.10, 0.45),
                # Result
                'Technical_Result': gwp * np.random.uniform(-0.05, 0.15),
                'Non_Technical_Result': gwp * np.random.uniform(-0.02, 0.05),
                'Total_Result': gwp * np.random.uniform(-0.05, 0.18),
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR0504 - Non-Life Income, Expenditure and Business Model Analysis
# ============================================================================

def generate_ir0504_non_life_income_expenditure():
    """
    IR0504 - Non-Life Income, Expenditure and Business Model Analysis
    Non-life insurance revenue and cost breakdown with business model metrics.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        for lob in NON_LIFE_LOB:
            gwp = random_amount(20_000_000, 150_000_000)
            claims_ratio = np.random.uniform(0.50, 0.80)
            expense_ratio = np.random.uniform(0.25, 0.40)

            row = {
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Line_Of_Business': lob,
                # Premiums
                'Gross_Written_Premium': gwp,
                'Gross_Earned_Premium': gwp * np.random.uniform(0.88, 0.98),
                'Reinsurance_Premium_Ceded': gwp * np.random.uniform(0.15, 0.35),
                'Net_Written_Premium': gwp * np.random.uniform(0.65, 0.85),
                'Net_Earned_Premium': gwp * np.random.uniform(0.60, 0.82),
                # Claims
                'Gross_Claims_Incurred': gwp * claims_ratio,
                'Prior_Year_Claims_Development': gwp * np.random.uniform(-0.08, 0.08),
                'Current_Year_Claims': gwp * claims_ratio * np.random.uniform(0.85, 1.05),
                'Reinsurance_Recoveries': gwp * claims_ratio * np.random.uniform(0.15, 0.35),
                'Net_Claims_Incurred': gwp * claims_ratio * np.random.uniform(0.65, 0.85),
                'Claims_Paid': gwp * claims_ratio * np.random.uniform(0.60, 0.85),
                'Change_In_Claims_Reserves': gwp * claims_ratio * np.random.uniform(-0.10, 0.25),
                # Expenses
                'Acquisition_Costs': gwp * np.random.uniform(0.15, 0.28),
                'Reinsurance_Commissions': gwp * np.random.uniform(0.02, 0.08),
                'Administrative_Expenses': gwp * np.random.uniform(0.08, 0.15),
                'Other_Operating_Expenses': gwp * np.random.uniform(0.02, 0.06),
                'Total_Expenses': gwp * expense_ratio,
                # Ratios
                'Net_Loss_Ratio': round(claims_ratio * 100, 2),
                'Net_Expense_Ratio': round(expense_ratio * 100, 2),
                'Net_Combined_Ratio': round((claims_ratio + expense_ratio) * 100, 2),
                # Investment
                'Investment_Income_Allocated': gwp * np.random.uniform(0.03, 0.10),
                # Business Model Metrics
                'Policy_Count': random.randint(1000, 50000),
                'Average_Premium': round(gwp / random.randint(1000, 50000), 2),
                'Average_Claim_Size': round(gwp * claims_ratio / random.randint(100, 5000), 2),
                'Claim_Frequency': round(random.randint(100, 5000) / random.randint(1000, 50000) * 100, 2),
                'Retention_Rate': random_percentage(75, 95),
                'New_Business_Rate': random_percentage(5, 25),
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR0505 - Life Premiums and Claims by Country
# ============================================================================

def generate_ir0505_life_premiums_claims_by_country():
    """
    IR0505 - Life Premiums and Claims by Country
    Geographic breakdown of life insurance business.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        for country in COUNTRIES[:6]:
            for lob in LIFE_LOB[:4]:
                gwp = random_amount(2_000_000, 30_000_000)

                row = {
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Country': country,
                    'Line_Of_Business': lob,
                    'Gross_Written_Premium': gwp,
                    'Net_Written_Premium': gwp * np.random.uniform(0.80, 0.95),
                    'Gross_Earned_Premium': gwp * np.random.uniform(0.92, 0.99),
                    'Net_Earned_Premium': gwp * np.random.uniform(0.75, 0.92),
                    'Claims_Incurred_Gross': gwp * np.random.uniform(0.55, 0.80),
                    'Claims_Incurred_Net': gwp * np.random.uniform(0.45, 0.70),
                    'Claims_Paid_Gross': gwp * np.random.uniform(0.40, 0.65),
                    'Claims_Paid_Net': gwp * np.random.uniform(0.35, 0.58),
                    'Acquisition_Costs': gwp * np.random.uniform(0.08, 0.18),
                    'Administrative_Expenses': gwp * np.random.uniform(0.05, 0.12),
                    'Number_Of_Policies': random.randint(500, 10000),
                    'Number_Of_Claims': random.randint(50, 500),
                    'Sum_Insured': gwp * np.random.uniform(15, 30),
                }
                data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR0506 - Non-Life Premiums and Claims by Country
# ============================================================================

def generate_ir0506_non_life_premiums_claims_by_country():
    """
    IR0506 - Non-Life Premiums and Claims by Country
    Geographic breakdown of non-life insurance business.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        for country in COUNTRIES[:8]:
            for lob in NON_LIFE_LOB[:8]:
                gwp = random_amount(3_000_000, 40_000_000)
                claims_ratio = np.random.uniform(0.50, 0.85)

                row = {
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Country': country,
                    'Line_Of_Business': lob,
                    'Gross_Written_Premium': gwp,
                    'Gross_Earned_Premium': gwp * np.random.uniform(0.88, 0.98),
                    'Reinsurance_Premium_Ceded': gwp * np.random.uniform(0.15, 0.35),
                    'Net_Written_Premium': gwp * np.random.uniform(0.65, 0.85),
                    'Net_Earned_Premium': gwp * np.random.uniform(0.60, 0.82),
                    'Gross_Claims_Incurred': gwp * claims_ratio,
                    'Reinsurance_Recoveries': gwp * claims_ratio * np.random.uniform(0.15, 0.35),
                    'Net_Claims_Incurred': gwp * claims_ratio * np.random.uniform(0.65, 0.85),
                    'Gross_Claims_Paid': gwp * claims_ratio * np.random.uniform(0.60, 0.85),
                    'Net_Claims_Paid': gwp * claims_ratio * np.random.uniform(0.50, 0.70),
                    'Acquisition_Costs': gwp * np.random.uniform(0.15, 0.28),
                    'Administrative_Expenses': gwp * np.random.uniform(0.08, 0.15),
                    'Other_Expenses': gwp * np.random.uniform(0.02, 0.06),
                    'Policy_Count': random.randint(500, 20000),
                    'Claim_Count': random.randint(50, 2000),
                    'Average_Premium': round(gwp / random.randint(500, 20000), 2),
                    'Average_Claim': round(gwp * claims_ratio / random.randint(50, 2000), 2),
                }
                data.append(row)

    return pd.DataFrame(data)


# Export all functions
__all__ = [
    'generate_ir0502_premiums_claims_by_country',
    'generate_ir0503_life_income_expenditure',
    'generate_ir0504_non_life_income_expenditure',
    'generate_ir0505_life_premiums_claims_by_country',
    'generate_ir0506_non_life_premiums_claims_by_country',
]
