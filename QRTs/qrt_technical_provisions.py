"""
PRA/BoE QRT Generators - Technical Provisions
==============================================
IR1201-IR1206: Life Technical Provisions
IR1401: Life Obligations Analysis
IR1601-IR1602: Non-Life Annuities
IR1701-IR1703: Non-Life Technical Provisions
IR1801-IR1802: Non-Life Cash Flow Projections
IR1901-IR1902: Non-Life Insurance Claims
IR2001: Claims Distribution Development
IR2102, IR2104: Underwriting Risks

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

COUNTRIES = ['GB', 'US', 'DE', 'FR', 'JP', 'CH', 'AU', 'CA', 'IE', 'NL']

NON_LIFE_LOB = [
    'Medical expense insurance',
    'Income protection insurance',
    'Workers\' compensation insurance',
    'Motor vehicle liability insurance',
    'Other motor insurance',
    'Marine, aviation and transport insurance',
    'Fire and other damage to property insurance',
    'General liability insurance',
    'Credit and suretyship insurance',
    'Legal expenses insurance',
    'Assistance',
    'Miscellaneous financial loss'
]

LIFE_LOB = [
    'Insurance with profit participation',
    'Index-linked and unit-linked insurance',
    'Other life insurance',
    'Annuities stemming from non-life contracts',
    'Health insurance (SLT)',
    'Life reinsurance'
]

def generate_lei():
    return '549300' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))

def random_amount(min_val, max_val, precision=2):
    return round(np.random.uniform(min_val, max_val), precision)

def random_percentage(min_val=0, max_val=100):
    return round(np.random.uniform(min_val, max_val), 4)


# ============================================================================
# IR1201 - Life Technical Provisions
# ============================================================================

def generate_ir1201_life_technical_provisions():
    """
    IR1201 - Life Technical Provisions
    Detailed breakdown of life insurance technical provisions.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            for lob in LIFE_LOB:
                gross_be = random_amount(10_000_000, 500_000_000)
                ri_recoverables = gross_be * random_percentage(5, 25) / 100
                net_be = gross_be - ri_recoverables
                risk_margin = gross_be * random_percentage(3, 8) / 100

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Line_Of_Business': lob,
                    # Gross Best Estimate
                    'Gross_Best_Estimate': gross_be,
                    'BE_Claims_Provisions': gross_be * random_percentage(30, 50) / 100,
                    'BE_Premium_Provisions': gross_be * random_percentage(50, 70) / 100,
                    # Reinsurance Recoverables
                    'RI_Recoverables_Total': ri_recoverables,
                    'RI_Recoverables_Claims': ri_recoverables * random_percentage(60, 80) / 100,
                    'RI_Recoverables_Premium': ri_recoverables * random_percentage(20, 40) / 100,
                    # Net Best Estimate
                    'Net_Best_Estimate': net_be,
                    # Risk Margin
                    'Risk_Margin': risk_margin,
                    # Total Technical Provisions
                    'Gross_Technical_Provisions': gross_be + risk_margin,
                    'Net_Technical_Provisions': net_be + risk_margin,
                    # Transitional Measures
                    'Transitional_TP_Deduction': random_amount(0, gross_be * 0.1),
                    'Transitional_Interest_Rate': random_amount(0, gross_be * 0.05),
                    # Final TP
                    'Technical_Provisions_After_Transitional': gross_be + risk_margin - random_amount(0, gross_be * 0.1),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR1203 - Life Best Estimate Liabilities by Country
# ============================================================================

def generate_ir1203_life_bel_by_country():
    """
    IR1203 - Life Best Estimate Liabilities by Country
    Geographic breakdown of life best estimate.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            total_bel = random_amount(100_000_000, 1_000_000_000)

            for country in COUNTRIES[:6]:
                country_pct = random_percentage(5, 40) if country == 'GB' else random_percentage(2, 15)
                country_bel = total_bel * country_pct / 100

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Country': country,
                    'Best_Estimate_Gross': country_bel,
                    'Best_Estimate_Ceded': country_bel * random_percentage(5, 20) / 100,
                    'Best_Estimate_Net': country_bel * random_percentage(80, 95) / 100,
                    'Percentage_Of_Total': country_pct,
                    'Number_Of_Contracts': random.randint(100, 50000),
                    'Sum_Insured': country_bel * random.randint(10, 30),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR1204 - Best Estimate Assumptions for Life Insurance Risks
# ============================================================================

def generate_ir1204_life_be_assumptions():
    """
    IR1204 - Best Estimate Assumptions for Life Insurance Risks
    Key assumptions used in calculating life best estimates.
    """
    data = []

    risk_types = [
        'Mortality', 'Longevity', 'Disability/Morbidity',
        'Lapse', 'Expense', 'Revision'
    ]

    age_bands = ['0-30', '31-45', '46-60', '61-75', '76+']

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            for lob in LIFE_LOB[:3]:
                for risk_type in risk_types:
                    for age_band in age_bands:
                        base_rate = random_percentage(0.1, 5) if risk_type == 'Mortality' else random_percentage(0.5, 15)

                        data.append({
                            'LEI': undertaking['lei'],
                            'Undertaking_Name': undertaking['name'],
                            'Reporting_Date': REPORTING_DATE,
                            'Line_Of_Business': lob,
                            'Risk_Type': risk_type,
                            'Age_Band': age_band,
                            'Base_Table': f'{risk_type[:3].upper()}_2024',
                            'Base_Rate_Pct': base_rate,
                            'Loading_Factor': random_percentage(90, 120),
                            'Trend_Assumption_Pct': random_percentage(-2, 2),
                            'Selection_Factor': random_percentage(80, 100),
                            'Experience_Adjustment': random_percentage(90, 110),
                            'Uncertainty_Margin': random_percentage(5, 15),
                            'Sensitivity_10pct_Increase': random_amount(100_000, 10_000_000),
                            'Currency': 'GBP'
                        })

    return pd.DataFrame(data)


# ============================================================================
# IR1205 - With-Profits Value of Bonus
# ============================================================================

def generate_ir1205_with_profits_bonus():
    """
    IR1205 - With-Profits Value of Bonus
    Analysis of with-profits bonus reserves.
    """
    data = []

    bonus_types = ['Reversionary Bonus', 'Terminal Bonus', 'Cash Bonus', 'Asset Share']

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            for bonus_type in bonus_types:
                total_value = random_amount(10_000_000, 200_000_000)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Bonus_Type': bonus_type,
                    'Total_Bonus_Value': total_value,
                    'Guaranteed_Bonus': total_value * random_percentage(60, 80) / 100 if bonus_type == 'Reversionary Bonus' else 0,
                    'Non_Guaranteed_Bonus': total_value * random_percentage(20, 40) / 100 if bonus_type == 'Reversionary Bonus' else total_value,
                    'Opening_Balance': total_value * random_percentage(90, 110) / 100,
                    'Bonus_Additions': total_value * random_percentage(3, 8) / 100,
                    'Claims_Paid': total_value * random_percentage(5, 15) / 100,
                    'Surrenders': total_value * random_percentage(2, 8) / 100,
                    'Transfers': random_amount(-5_000_000, 5_000_000),
                    'Closing_Balance': total_value,
                    'Number_Of_Policies': random.randint(1000, 50000),
                    'Average_Bonus_Per_Policy': total_value / random.randint(1000, 50000),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR1206 - With-Profits Liabilities and Assets
# ============================================================================

def generate_ir1206_with_profits_liabilities_assets():
    """
    IR1206 - With-Profits Liabilities and Assets
    With-profits fund balance sheet analysis.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            total_assets = random_amount(500_000_000, 5_000_000_000)
            total_liabilities = total_assets * random_percentage(85, 98) / 100

            data.append({
                'LEI': undertaking['lei'],
                'Undertaking_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                # Assets
                'Total_Assets': total_assets,
                'Bonds': total_assets * random_percentage(30, 50) / 100,
                'Equities': total_assets * random_percentage(20, 40) / 100,
                'Property': total_assets * random_percentage(5, 15) / 100,
                'Cash': total_assets * random_percentage(3, 10) / 100,
                'Other_Assets': total_assets * random_percentage(2, 8) / 100,
                # Liabilities
                'Total_Liabilities': total_liabilities,
                'With_Profits_BEL': total_liabilities * random_percentage(80, 90) / 100,
                'Guaranteed_Benefits': total_liabilities * random_percentage(50, 70) / 100,
                'Future_Discretionary_Benefits': total_liabilities * random_percentage(10, 25) / 100,
                'Risk_Margin': total_liabilities * random_percentage(3, 8) / 100,
                'Other_Liabilities': total_liabilities * random_percentage(5, 12) / 100,
                # Surplus
                'Estate': total_assets - total_liabilities,
                'Support_Assets': random_amount(10_000_000, 100_000_000),
                'PPFM_Ratio': random_percentage(0, 50),
                'Currency': 'GBP'
            })

    return pd.DataFrame(data)


# ============================================================================
# IR1401 - Life Obligations Analysis
# ============================================================================

def generate_ir1401_life_obligations():
    """
    IR1401 - Life Obligations Analysis
    Detailed analysis of life insurance obligations.
    """
    data = []

    product_types = [
        'Term Assurance', 'Whole of Life', 'Endowment',
        'Annuity in Payment', 'Deferred Annuity', 'Unit-Linked'
    ]

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Life', 'Composite']:
            for product in product_types:
                num_policies = random.randint(1000, 100000)
                avg_sum_assured = random_amount(50_000, 500_000)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Product_Type': product,
                    'Number_Of_Policies': num_policies,
                    'Number_Of_Lives': int(num_policies * random_percentage(90, 110) / 100),
                    'Sum_At_Risk': num_policies * avg_sum_assured,
                    'Best_Estimate_Liability': random_amount(10_000_000, 500_000_000),
                    'Premium_Income_Annual': num_policies * random_amount(500, 5000),
                    'Average_Age_At_Entry': random_percentage(25, 55),
                    'Average_Current_Age': random_percentage(35, 65),
                    'Average_Duration_Years': random_percentage(5, 25),
                    'Average_Term_Remaining': random_percentage(5, 30),
                    'Lapse_Rate_Assumption': random_percentage(2, 10),
                    'Expense_Assumption_Per_Policy': random_amount(50, 200),
                    'Currency': 'GBP'
                })

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

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            for lob in ['Motor vehicle liability insurance', 'Workers\' compensation insurance', 'General liability insurance']:
                num_annuities = random.randint(50, 2000)
                avg_annual_payment = random_amount(10_000, 100_000)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Line_Of_Business': lob,
                    'Number_Of_Annuities': num_annuities,
                    'Total_Annual_Payment': num_annuities * avg_annual_payment,
                    'Average_Age_Of_Annuitant': random_percentage(35, 70),
                    'Average_Remaining_Life_Expectancy': random_percentage(10, 40),
                    'Best_Estimate_Provision': num_annuities * avg_annual_payment * random_percentage(8, 20),
                    'Risk_Margin': num_annuities * avg_annual_payment * random_percentage(0.5, 2),
                    'Total_Technical_Provision': num_annuities * avg_annual_payment * random_percentage(8.5, 22),
                    'Discount_Rate_Used': random_percentage(1, 4),
                    'Mortality_Table': 'CMI 2023',
                    'Inflation_Assumption': random_percentage(2, 4),
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR1602 - Non-Life Annuities Projection of Future Cash Flows
# ============================================================================

def generate_ir1602_non_life_annuities_cash_flows():
    """
    IR1602 - Non-Life Annuities Projection of Future Cash Flows
    Cash flow projections for non-life annuities.
    """
    data = []

    projection_years = list(range(1, 51))  # 50 year projection

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            initial_payment = random_amount(5_000_000, 50_000_000)

            for year in projection_years:
                # Declining payments over time
                payment_factor = max(0.01, 1 - (year - 1) * 0.025)  # Reduce by 2.5% per year
                inflation_factor = (1.025) ** year  # 2.5% inflation

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Projection_Year': year,
                    'Cash_Out_Payments': initial_payment * payment_factor * inflation_factor,
                    'Cash_Out_Expenses': initial_payment * payment_factor * 0.03,
                    'Total_Cash_Out': initial_payment * payment_factor * inflation_factor * 1.03,
                    'Discount_Factor': 1 / ((1 + 0.03) ** year),
                    'Discounted_Cash_Flow': initial_payment * payment_factor * inflation_factor * 1.03 / ((1 + 0.03) ** year),
                    'Survivors_Assumed': 100 * (0.98 ** year),  # 2% mortality per year
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR1701 - Non-Life Technical Provisions
# ============================================================================

def generate_ir1701_non_life_technical_provisions():
    """
    IR1701 - Non-Life Technical Provisions
    Detailed breakdown of non-life technical provisions.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            for lob in NON_LIFE_LOB:
                claims_provision = random_amount(10_000_000, 500_000_000)
                premium_provision = random_amount(5_000_000, 200_000_000)

                # RI Recoverables
                ri_claims = claims_provision * random_percentage(10, 35) / 100
                ri_premium = premium_provision * random_percentage(10, 35) / 100

                risk_margin = (claims_provision + premium_provision) * random_percentage(4, 10) / 100

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Line_Of_Business': lob,
                    # Claims Provisions
                    'Gross_Claims_Provision': claims_provision,
                    'Gross_IBNR': claims_provision * random_percentage(30, 60) / 100,
                    'Gross_Case_Reserves': claims_provision * random_percentage(40, 70) / 100,
                    'RI_Recoverables_Claims': ri_claims,
                    'Net_Claims_Provision': claims_provision - ri_claims,
                    # Premium Provisions
                    'Gross_Premium_Provision': premium_provision,
                    'Expected_Future_Premiums': premium_provision * random_percentage(80, 100) / 100,
                    'Expected_Future_Claims': premium_provision * random_percentage(60, 85) / 100,
                    'Expected_Future_Expenses': premium_provision * random_percentage(15, 30) / 100,
                    'RI_Recoverables_Premium': ri_premium,
                    'Net_Premium_Provision': premium_provision - ri_premium,
                    # Risk Margin
                    'Risk_Margin': risk_margin,
                    # Totals
                    'Gross_Best_Estimate': claims_provision + premium_provision,
                    'Total_RI_Recoverables': ri_claims + ri_premium,
                    'Net_Best_Estimate': (claims_provision - ri_claims) + (premium_provision - ri_premium),
                    'Gross_Technical_Provisions': claims_provision + premium_provision + risk_margin,
                    'Net_Technical_Provisions': (claims_provision - ri_claims) + (premium_provision - ri_premium) + risk_margin,
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR1703 - Non-Life Best Estimate Liabilities by Country
# ============================================================================

def generate_ir1703_non_life_bel_by_country():
    """
    IR1703 - Non-Life Best Estimate Liabilities by Country
    Geographic breakdown of non-life best estimate.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            for lob in NON_LIFE_LOB[:6]:
                total_bel = random_amount(20_000_000, 300_000_000)

                for country in COUNTRIES[:5]:
                    country_pct = random_percentage(20, 50) if country == 'GB' else random_percentage(5, 20)
                    country_bel = total_bel * country_pct / 100

                    data.append({
                        'LEI': undertaking['lei'],
                        'Undertaking_Name': undertaking['name'],
                        'Reporting_Date': REPORTING_DATE,
                        'Line_Of_Business': lob,
                        'Country': country,
                        'Claims_Provision': country_bel * random_percentage(60, 80) / 100,
                        'Premium_Provision': country_bel * random_percentage(20, 40) / 100,
                        'Total_Best_Estimate': country_bel,
                        'RI_Recoverables': country_bel * random_percentage(10, 30) / 100,
                        'Net_Best_Estimate': country_bel * random_percentage(70, 90) / 100,
                        'Percentage_Of_Total': country_pct,
                        'Currency': 'GBP'
                    })

    return pd.DataFrame(data)


# ============================================================================
# IR1801 - Non-Life Projection of Future Cash Flows
# ============================================================================

def generate_ir1801_non_life_cash_flows():
    """
    IR1801 - Non-Life Projection of Future Cash Flows
    Cash flow projections for non-life technical provisions.
    """
    data = []

    projection_years = list(range(1, 31))  # 30 year projection

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            for lob in NON_LIFE_LOB[:6]:
                initial_claims = random_amount(20_000_000, 200_000_000)
                initial_premium = random_amount(50_000_000, 300_000_000)

                for year in projection_years:
                    # Claims runoff pattern (faster in early years)
                    claims_factor = 0.6 ** (year - 1) if year <= 5 else 0.6 ** 4 * 0.9 ** (year - 5)
                    premium_factor = max(0, 1 - year * 0.3)  # Earned over ~3 years

                    data.append({
                        'LEI': undertaking['lei'],
                        'Undertaking_Name': undertaking['name'],
                        'Reporting_Date': REPORTING_DATE,
                        'Line_Of_Business': lob,
                        'Projection_Year': year,
                        # Cash Inflows
                        'Future_Premiums_Receivable': initial_premium * premium_factor,
                        'Salvage_And_Subrogation': initial_claims * claims_factor * 0.02,
                        'Total_Cash_In': initial_premium * premium_factor + initial_claims * claims_factor * 0.02,
                        # Cash Outflows
                        'Claims_Payments': initial_claims * claims_factor,
                        'Claims_Expenses': initial_claims * claims_factor * 0.08,
                        'Administrative_Expenses': initial_premium * premium_factor * 0.05,
                        'Acquisition_Costs': initial_premium * premium_factor * 0.15,
                        'Total_Cash_Out': initial_claims * claims_factor * 1.08 + initial_premium * premium_factor * 0.2,
                        # Discounted Values
                        'Discount_Factor': 1 / ((1 + 0.03) ** year),
                        'Discounted_Net_Cash_Flow': ((initial_premium * premium_factor + initial_claims * claims_factor * 0.02) -
                                                    (initial_claims * claims_factor * 1.08 + initial_premium * premium_factor * 0.2)) / ((1 + 0.03) ** year),
                        'Currency': 'GBP'
                    })

    return pd.DataFrame(data)


# ============================================================================
# IR1802 - Non-Life Liability Projection of Future Cash Flows
# ============================================================================

def generate_ir1802_non_life_liability_cash_flows():
    """
    IR1802 - Non-Life Liability Projection of Future Cash Flows
    Detailed liability cash flow projections.
    """
    data = []

    projection_years = list(range(1, 21))

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            for lob in NON_LIFE_LOB[:4]:
                initial_reserve = random_amount(30_000_000, 300_000_000)

                for year in projection_years:
                    runoff_factor = 0.7 ** (year - 1) if year <= 3 else 0.7 ** 2 * 0.85 ** (year - 3)

                    data.append({
                        'LEI': undertaking['lei'],
                        'Undertaking_Name': undertaking['name'],
                        'Reporting_Date': REPORTING_DATE,
                        'Line_Of_Business': lob,
                        'Projection_Year': year,
                        'Opening_Reserve': initial_reserve * (0.7 ** (year - 1)) if year > 1 else initial_reserve,
                        'Claims_Paid': initial_reserve * runoff_factor * random_percentage(20, 40) / 100,
                        'Reserve_Movement': initial_reserve * runoff_factor * random_percentage(-10, 10) / 100,
                        'Closing_Reserve': initial_reserve * runoff_factor,
                        'ALAE_Paid': initial_reserve * runoff_factor * 0.05,
                        'ULAE_Paid': initial_reserve * runoff_factor * 0.03,
                        'Discount_Rate': 0.03,
                        'Discounted_Reserve': initial_reserve * runoff_factor / ((1 + 0.03) ** year),
                        'Currency': 'GBP'
                    })

    return pd.DataFrame(data)


# ============================================================================
# IR1901 - Non-Life Insurance Claims
# ============================================================================

def generate_ir1901_non_life_claims():
    """
    IR1901 - Non-Life Insurance Claims
    Claims development triangles and analysis.
    """
    data = []

    accident_years = list(range(2015, 2025))
    development_years = list(range(0, 10))

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            for lob in NON_LIFE_LOB[:8]:
                for acc_year in accident_years:
                    ultimate = random_amount(20_000_000, 200_000_000)

                    for dev_year in development_years:
                        if acc_year + dev_year <= 2024:
                            # Development pattern
                            cumulative_paid_pct = min(100, 30 + dev_year * 15 + random_percentage(-5, 5))
                            cumulative_incurred_pct = min(100, 60 + dev_year * 8 + random_percentage(-3, 3))

                            data.append({
                                'LEI': undertaking['lei'],
                                'Undertaking_Name': undertaking['name'],
                                'Reporting_Date': REPORTING_DATE,
                                'Line_Of_Business': lob,
                                'Accident_Year': acc_year,
                                'Development_Year': dev_year,
                                'Reporting_Year': acc_year + dev_year,
                                # Gross amounts
                                'Gross_Claims_Paid_Cumulative': ultimate * cumulative_paid_pct / 100,
                                'Gross_Claims_Incurred_Cumulative': ultimate * cumulative_incurred_pct / 100,
                                'Gross_Case_Reserves': ultimate * (cumulative_incurred_pct - cumulative_paid_pct) / 100,
                                'Gross_IBNR': ultimate * (100 - cumulative_incurred_pct) / 100,
                                # Net amounts (after RI)
                                'Net_Claims_Paid_Cumulative': ultimate * cumulative_paid_pct / 100 * 0.75,
                                'Net_Claims_Incurred_Cumulative': ultimate * cumulative_incurred_pct / 100 * 0.75,
                                # Development factors
                                'Paid_Development_Factor': 1 / (cumulative_paid_pct / 100) if cumulative_paid_pct > 0 else None,
                                'Incurred_Development_Factor': 1 / (cumulative_incurred_pct / 100) if cumulative_incurred_pct > 0 else None,
                                'Number_Of_Claims_Open': int(1000 * (1 - cumulative_paid_pct / 100)),
                                'Number_Of_Claims_Closed': int(1000 * cumulative_paid_pct / 100),
                                'Currency': 'GBP'
                            })

    return pd.DataFrame(data)


# ============================================================================
# IR1902 - Non-Life Claim Development (General Liability Sub-classes)
# ============================================================================

def generate_ir1902_gl_claims_development():
    """
    IR1902 - Non-Life Claim Development (General Liability Sub-classes)
    Detailed claim development for general liability.
    """
    data = []

    gl_subclasses = [
        'Public Liability', 'Products Liability', 'Employers Liability',
        'Professional Indemnity', 'Directors & Officers', 'Medical Malpractice'
    ]

    accident_years = list(range(2015, 2025))
    development_years = list(range(0, 15))  # Longer tail for GL

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            for subclass in gl_subclasses:
                for acc_year in accident_years:
                    ultimate = random_amount(5_000_000, 80_000_000)

                    for dev_year in development_years:
                        if acc_year + dev_year <= 2024:
                            # GL has longer development pattern
                            cumulative_paid_pct = min(100, 10 + dev_year * 8 + random_percentage(-3, 3))
                            cumulative_incurred_pct = min(100, 40 + dev_year * 6 + random_percentage(-2, 2))

                            data.append({
                                'LEI': undertaking['lei'],
                                'Undertaking_Name': undertaking['name'],
                                'Reporting_Date': REPORTING_DATE,
                                'GL_Subclass': subclass,
                                'Accident_Year': acc_year,
                                'Development_Year': dev_year,
                                'Gross_Paid_Cumulative': ultimate * cumulative_paid_pct / 100,
                                'Gross_Incurred_Cumulative': ultimate * cumulative_incurred_pct / 100,
                                'Gross_Outstanding': ultimate * (cumulative_incurred_pct - cumulative_paid_pct) / 100,
                                'Large_Claims_Count': random.randint(0, 10),
                                'Large_Claims_Value': ultimate * random_percentage(20, 50) / 100,
                                'Average_Claim_Size': ultimate / random.randint(50, 500),
                                'Currency': 'GBP'
                            })

    return pd.DataFrame(data)


# ============================================================================
# IR2001 - Development of Distribution of Claims Incurred
# ============================================================================

def generate_ir2001_claims_distribution():
    """
    IR2001 - Development of the Distribution of the Claims Incurred
    Statistical distribution of claims development.
    """
    data = []

    percentiles = [10, 25, 50, 75, 90, 95, 99]

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            for lob in NON_LIFE_LOB[:6]:
                mean_ultimate = random_amount(50_000_000, 500_000_000)
                cv = random_percentage(10, 30) / 100  # Coefficient of variation

                for percentile in percentiles:
                    # Normal distribution approximation
                    z_score = {10: -1.28, 25: -0.67, 50: 0, 75: 0.67, 90: 1.28, 95: 1.65, 99: 2.33}
                    ultimate_at_percentile = mean_ultimate * (1 + z_score[percentile] * cv)

                    data.append({
                        'LEI': undertaking['lei'],
                        'Undertaking_Name': undertaking['name'],
                        'Reporting_Date': REPORTING_DATE,
                        'Line_Of_Business': lob,
                        'Percentile': percentile,
                        'Ultimate_Claims_Gross': ultimate_at_percentile,
                        'Ultimate_Claims_Net': ultimate_at_percentile * random_percentage(65, 85) / 100,
                        'Best_Estimate': mean_ultimate,
                        'Standard_Deviation': mean_ultimate * cv,
                        'Coefficient_Of_Variation': cv * 100,
                        'Skewness': random_percentage(0.5, 2),
                        'Currency': 'GBP'
                    })

    return pd.DataFrame(data)


# ============================================================================
# IR2102 - Non-Life Underwriting Risks
# ============================================================================

def generate_ir2102_non_life_underwriting_risks():
    """
    IR2102 - Non-Life Underwriting Risks
    Analysis of non-life underwriting risk exposures.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            for lob in NON_LIFE_LOB:
                premium_volume = random_amount(20_000_000, 500_000_000)
                reserve_volume = random_amount(30_000_000, 600_000_000)

                data.append({
                    'LEI': undertaking['lei'],
                    'Undertaking_Name': undertaking['name'],
                    'Reporting_Date': REPORTING_DATE,
                    'Line_Of_Business': lob,
                    # Premium Risk
                    'Net_Premium_Volume': premium_volume,
                    'Premium_Risk_Std_Dev': random_percentage(5, 15),
                    'USP_Premium_Risk': random.choice(['Yes', 'No']),
                    'Premium_Risk_SCR': premium_volume * random_percentage(10, 25) / 100,
                    # Reserve Risk
                    'Net_Reserve_Volume': reserve_volume,
                    'Reserve_Risk_Std_Dev': random_percentage(8, 20),
                    'USP_Reserve_Risk': random.choice(['Yes', 'No']),
                    'Reserve_Risk_SCR': reserve_volume * random_percentage(15, 35) / 100,
                    # Lapse Risk
                    'Lapse_Risk_Exposure': premium_volume * random_percentage(20, 50) / 100,
                    'Lapse_Risk_SCR': premium_volume * random_percentage(2, 8) / 100,
                    # Combined
                    'Geographic_Diversification': random_percentage(0.7, 0.95),
                    'Combined_SCR_Before_Div': (premium_volume * random_percentage(10, 25) / 100 +
                                               reserve_volume * random_percentage(15, 35) / 100),
                    'Combined_SCR_After_Div': (premium_volume * random_percentage(10, 25) / 100 +
                                              reserve_volume * random_percentage(15, 35) / 100) * 0.85,
                    'Currency': 'GBP'
                })

    return pd.DataFrame(data)


# ============================================================================
# IR2104 - Cyber Underwriting Risk
# ============================================================================

def generate_ir2104_cyber_underwriting_risk():
    """
    IR2104 - Cyber Underwriting Risk
    Specific analysis of cyber insurance risks.
    """
    data = []

    cyber_coverages = [
        'First Party - Data Breach',
        'First Party - Business Interruption',
        'Third Party - Liability',
        'Third Party - Privacy Liability',
        'Cyber Extortion',
        'Media Liability'
    ]

    industry_sectors = [
        'Financial Services', 'Healthcare', 'Retail', 'Technology',
        'Manufacturing', 'Professional Services', 'Public Sector'
    ]

    for undertaking in UNDERTAKINGS:
        if undertaking['type'] in ['Non-Life', 'Composite']:
            for coverage in cyber_coverages:
                for sector in industry_sectors[:4]:
                    gwp = random_amount(500_000, 30_000_000)

                    data.append({
                        'LEI': undertaking['lei'],
                        'Undertaking_Name': undertaking['name'],
                        'Reporting_Date': REPORTING_DATE,
                        'Cyber_Coverage_Type': coverage,
                        'Industry_Sector': sector,
                        'Gross_Written_Premium': gwp,
                        'Net_Written_Premium': gwp * random_percentage(60, 90) / 100,
                        'Total_Sum_Insured': gwp * random.randint(50, 200),
                        'Policy_Count': random.randint(10, 1000),
                        'Average_Limit': gwp * random.randint(50, 200) / random.randint(10, 1000),
                        'Average_Deductible': random_amount(10_000, 500_000),
                        'Claims_Count_Current_Year': random.randint(0, 50),
                        'Claims_Incurred_Current_Year': gwp * random_percentage(20, 80) / 100,
                        'Loss_Ratio': random_percentage(30, 90),
                        'Aggregate_Exposure': gwp * random.randint(50, 200),
                        'PML_1_in_100': gwp * random.randint(20, 80),
                        'PML_1_in_250': gwp * random.randint(40, 120),
                        'Correlation_Assumption': random_percentage(20, 60),
                        'Currency': 'GBP'
                    })

    return pd.DataFrame(data)


# ============================================================================
# Power BI Execution
# ============================================================================

if __name__ == "__main__":
    print("Generating Technical Provisions QRTs...")

# Generate all tables for Power BI
IR1201_Life_Technical_Provisions = generate_ir1201_life_technical_provisions()
IR1203_Life_BEL_By_Country = generate_ir1203_life_bel_by_country()
IR1204_Life_BE_Assumptions = generate_ir1204_life_be_assumptions()
IR1205_With_Profits_Bonus = generate_ir1205_with_profits_bonus()
IR1206_With_Profits_Liabilities_Assets = generate_ir1206_with_profits_liabilities_assets()
IR1401_Life_Obligations = generate_ir1401_life_obligations()
IR1601_Non_Life_Annuities = generate_ir1601_non_life_annuities()
IR1602_Non_Life_Annuities_Cash_Flows = generate_ir1602_non_life_annuities_cash_flows()
IR1701_Non_Life_Technical_Provisions = generate_ir1701_non_life_technical_provisions()
IR1703_Non_Life_BEL_By_Country = generate_ir1703_non_life_bel_by_country()
IR1801_Non_Life_Cash_Flows = generate_ir1801_non_life_cash_flows()
IR1802_Non_Life_Liability_Cash_Flows = generate_ir1802_non_life_liability_cash_flows()
IR1901_Non_Life_Claims = generate_ir1901_non_life_claims()
IR1902_GL_Claims_Development = generate_ir1902_gl_claims_development()
IR2001_Claims_Distribution = generate_ir2001_claims_distribution()
IR2102_Non_Life_Underwriting_Risks = generate_ir2102_non_life_underwriting_risks()
IR2104_Cyber_Underwriting_Risk = generate_ir2104_cyber_underwriting_risk()
