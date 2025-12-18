"""
PRA/BoE Quantitative Reporting Templates (QRT) Generators - Actuarial Focus
============================================================================

Streamlined implementation of actuarial-focused PRA/BoE QRT templates for
Solvency II reporting. Non-actuarial templates have been archived.

Active Template Categories:
---------------------------
1. IR02 - Balance Sheet (01-03)
2. IR05 - Premiums, Claims, Expenses (02-06)
3. IR12 - Life Technical Provisions (01-06)
4. IR14 - Life Obligations Analysis (01)
5. IR16 - Non-Life Annuities (01-02)
6. IR17 - Non-Life Technical Provisions (01, 03)
7. IR18 - Non-Life Cash Flows (01-02)
8. IR19 - Non-Life Insurance Claims (01-02)
9. IR20 - Claims Distribution Development (01)
10. IR23 - Own Funds (01-05)
11. IR25 - SCR Overview (04-06)
12. IR26 - SCR Risk Modules (01-07)
13. IR27 - Catastrophe Risk (01)
14. IR28 - MCR (01-02)
15. IR32 - Group Scope (01)
16. IR33 - Individual Requirements (01)
17. IR34 - Other Undertakings (01)
18. IR35 - Group Technical Provisions (01)

Archived Templates (in /QRTs/archive/):
--------------------------------------
- AOC01, IM00-03 (Internal Model)
- IR01 (Basic Information)
- IR03 (Off-Balance Sheet)
- IR06 (Assets)
- IR08 (Derivatives)
- IR09 (Income/Gains/Losses)
- IR10-11 (Securities/Collateral)
- IR21 (Underwriting Risks)
- IR22 (LTG Measures)
- IR24 (Participations)
- IR30-31 (Reinsurance)
- IR36 (IGT)
- IRR22 (Matching Adjustment)
- MALIR, MR01, QMC01

Usage:
------
from QRTs import generate_all_qrts
all_data = generate_all_qrts()

Or import specific generators:
from QRTs.qrt_balance_sheet import generate_ir0201_balance_sheet
"""

# Balance Sheet (IR02)
from .qrt_balance_sheet import (
    generate_ir0201_balance_sheet,
    generate_ir0202_assets_liabilities_by_currency,
    generate_ir0203_branch_balance_sheet,
    UNDERTAKINGS,
    REPORTING_DATE,
    CURRENCIES,
    COUNTRIES,
    NON_LIFE_LOB,
    LIFE_LOB,
)

# Premiums and Claims (IR05)
from .qrt_premiums_claims import (
    generate_ir0502_premiums_claims_by_country,
    generate_ir0503_life_income_expenditure,
    generate_ir0504_non_life_income_expenditure,
    generate_ir0505_life_premiums_claims_by_country,
    generate_ir0506_non_life_premiums_claims_by_country,
)

# Technical Provisions (IR12-18)
from .qrt_technical_provisions import (
    generate_ir1201_life_technical_provisions,
    generate_ir1203_life_bel_by_country,
    generate_ir1204_life_be_assumptions,
    generate_ir1205_with_profits_bonus,
    generate_ir1206_with_profits_liabilities_assets,
    generate_ir1401_life_obligations,
    generate_ir1601_non_life_annuities,
    generate_ir1602_non_life_annuities_cash_flows,
    generate_ir1701_non_life_technical_provisions,
    generate_ir1703_non_life_bel_by_country,
    generate_ir1801_non_life_cash_flows,
    generate_ir1802_non_life_liability_cash_flows,
)

# Claims (IR19-20)
from .qrt_claims import (
    generate_ir1901_non_life_claims,
    generate_ir1902_gl_claims_development,
    generate_ir2001_claims_distribution,
)

# Own Funds and Capital (IR23, IR25-28)
from .qrt_own_funds_capital import (
    generate_ir2301_own_funds,
    generate_ir2302_own_funds_by_tier,
    generate_ir2303_own_funds_movements,
    generate_ir2304_own_funds_items,
    generate_ir2305_lloyds_capital,
    generate_ir2504_scr,
    generate_ir2505_scr_internal_model,
    generate_ir2506_scr_lac_dt,
    generate_ir2601_scr_market_risk,
    generate_ir2602_scr_counterparty_risk,
    generate_ir2603_scr_life_risk,
    generate_ir2604_scr_health_risk,
    generate_ir2605_scr_non_life_risk,
    generate_ir2606_scr_operational_risk,
    generate_ir2607_scr_simplifications,
    generate_ir2701_scr_catastrophe,
    generate_ir2801_mcr_non_life,
    generate_ir2802_mcr_composite,
)

# Group (IR32-35)
from .qrt_group import (
    generate_ir3201_group_scope,
    generate_ir3301_individual_requirements,
    generate_ir3401_other_undertakings,
    generate_ir3501_group_tp_contribution,
)


def generate_all_qrts():
    """
    Generate all actuarial-focused QRT templates and return as a dictionary of DataFrames.

    Returns:
        dict: Dictionary with template names as keys and DataFrames as values.
    """
    templates = {}

    # Balance Sheet (IR02)
    templates['IR0201_Balance_Sheet'] = generate_ir0201_balance_sheet()
    templates['IR0202_Assets_Liabilities_Currency'] = generate_ir0202_assets_liabilities_by_currency()
    templates['IR0203_Branch_Balance_Sheet'] = generate_ir0203_branch_balance_sheet()

    # Premiums, Claims, Expenses (IR05)
    templates['IR0502_Premiums_Claims_Country'] = generate_ir0502_premiums_claims_by_country()
    templates['IR0503_Life_Income_Expenditure'] = generate_ir0503_life_income_expenditure()
    templates['IR0504_Non_Life_Income_Expenditure'] = generate_ir0504_non_life_income_expenditure()
    templates['IR0505_Life_Premiums_Claims_Country'] = generate_ir0505_life_premiums_claims_by_country()
    templates['IR0506_Non_Life_Premiums_Claims_Country'] = generate_ir0506_non_life_premiums_claims_by_country()

    # Life Technical Provisions (IR12)
    templates['IR1201_Life_Technical_Provisions'] = generate_ir1201_life_technical_provisions()
    templates['IR1203_Life_BEL_By_Country'] = generate_ir1203_life_bel_by_country()
    templates['IR1204_Life_BE_Assumptions'] = generate_ir1204_life_be_assumptions()
    templates['IR1205_With_Profits_Bonus'] = generate_ir1205_with_profits_bonus()
    templates['IR1206_With_Profits_Liabilities_Assets'] = generate_ir1206_with_profits_liabilities_assets()

    # Life Obligations (IR14)
    templates['IR1401_Life_Obligations'] = generate_ir1401_life_obligations()

    # Non-Life Annuities (IR16)
    templates['IR1601_Non_Life_Annuities'] = generate_ir1601_non_life_annuities()
    templates['IR1602_Non_Life_Annuities_Cash_Flows'] = generate_ir1602_non_life_annuities_cash_flows()

    # Non-Life Technical Provisions (IR17)
    templates['IR1701_Non_Life_Technical_Provisions'] = generate_ir1701_non_life_technical_provisions()
    templates['IR1703_Non_Life_BEL_By_Country'] = generate_ir1703_non_life_bel_by_country()

    # Non-Life Cash Flows (IR18)
    templates['IR1801_Non_Life_Cash_Flows'] = generate_ir1801_non_life_cash_flows()
    templates['IR1802_Non_Life_Liability_Cash_Flows'] = generate_ir1802_non_life_liability_cash_flows()

    # Claims (IR19-20)
    templates['IR1901_Non_Life_Claims'] = generate_ir1901_non_life_claims()
    templates['IR1902_GL_Claims_Development'] = generate_ir1902_gl_claims_development()
    templates['IR2001_Claims_Distribution'] = generate_ir2001_claims_distribution()

    # Own Funds (IR23)
    templates['IR2301_Own_Funds'] = generate_ir2301_own_funds()
    templates['IR2302_Own_Funds_By_Tier'] = generate_ir2302_own_funds_by_tier()
    templates['IR2303_Own_Funds_Movements'] = generate_ir2303_own_funds_movements()
    templates['IR2304_Own_Funds_Items'] = generate_ir2304_own_funds_items()
    templates['IR2305_Lloyds_Capital'] = generate_ir2305_lloyds_capital()

    # SCR Overview (IR25)
    templates['IR2504_SCR'] = generate_ir2504_scr()
    templates['IR2505_SCR_Internal_Model'] = generate_ir2505_scr_internal_model()
    templates['IR2506_SCR_LAC_DT'] = generate_ir2506_scr_lac_dt()

    # SCR Risk Modules (IR26)
    templates['IR2601_SCR_Market_Risk'] = generate_ir2601_scr_market_risk()
    templates['IR2602_SCR_Counterparty_Risk'] = generate_ir2602_scr_counterparty_risk()
    templates['IR2603_SCR_Life_Risk'] = generate_ir2603_scr_life_risk()
    templates['IR2604_SCR_Health_Risk'] = generate_ir2604_scr_health_risk()
    templates['IR2605_SCR_Non_Life_Risk'] = generate_ir2605_scr_non_life_risk()
    templates['IR2606_SCR_Operational_Risk'] = generate_ir2606_scr_operational_risk()
    templates['IR2607_SCR_Simplifications'] = generate_ir2607_scr_simplifications()

    # Catastrophe Risk (IR27)
    templates['IR2701_SCR_Catastrophe'] = generate_ir2701_scr_catastrophe()

    # MCR (IR28)
    templates['IR2801_MCR_Non_Life'] = generate_ir2801_mcr_non_life()
    templates['IR2802_MCR_Composite'] = generate_ir2802_mcr_composite()

    # Group (IR32-35)
    templates['IR3201_Group_Scope'] = generate_ir3201_group_scope()
    templates['IR3301_Individual_Requirements'] = generate_ir3301_individual_requirements()
    templates['IR3401_Other_Undertakings'] = generate_ir3401_other_undertakings()
    templates['IR3501_Group_TP_Contribution'] = generate_ir3501_group_tp_contribution()

    return templates


# Actuarial-focused template mapping
QRT_TEMPLATE_MAP = {
    # IR02 - Balance Sheet
    'IR0201': 'Balance Sheet',
    'IR0202': 'Assets and Liabilities by Currency',
    'IR0203': 'Additional Branch Balance Sheet Information',
    # IR05 - Premiums/Claims/Expenses
    'IR0502': 'Premiums, Claims and Expenses by Country',
    'IR0503': 'Life Income and Expenditure',
    'IR0504': 'Non-Life Income, Expenditure and Business Model Analysis',
    'IR0505': 'Life Premiums and Claims by Country',
    'IR0506': 'Non-Life Premiums and Claims by Country',
    # IR12 - Life Technical Provisions
    'IR1201': 'Life Technical Provisions',
    'IR1203': 'Life Best Estimate Liabilities by Country',
    'IR1204': 'Best Estimate Assumptions for Life Insurance Risks',
    'IR1205': 'With-Profits Value of Bonus',
    'IR1206': 'With-Profits Liabilities and Assets',
    # IR14 - Life Obligations
    'IR1401': 'Life Obligations Analysis',
    # IR16 - Non-Life Annuities
    'IR1601': 'Non-Life Annuities Information',
    'IR1602': 'Non-Life Annuities Projection of Future Cash Flows',
    # IR17 - Non-Life Technical Provisions
    'IR1701': 'Non-Life Technical Provisions',
    'IR1703': 'Non-Life Best Estimate Liabilities by Country',
    # IR18 - Non-Life Cash Flows
    'IR1801': 'Non-Life Projection of Future Cash Flows',
    'IR1802': 'Non-Life Liability Projection of Future Cash Flows',
    # IR19-20 - Claims
    'IR1901': 'Non-Life Insurance Claims',
    'IR1902': 'Non-Life Claim Development - General Liability Sub-classes',
    'IR2001': 'Development of the Distribution of the Claims Incurred',
    # IR23 - Own Funds
    'IR2301': 'Own Funds',
    'IR2302': 'Detailed Information by Tiers on Own Funds',
    'IR2303': 'Annual Movements on Own Funds',
    'IR2304': 'List of Items on Own Funds',
    'IR2305': "Society of Lloyd's Own Funds and Capital Requirements",
    # IR25 - SCR
    'IR2504': 'Solvency Capital Requirement',
    'IR2505': 'SCR - Partial or Full Internal Model Components',
    'IR2506': 'SCR - Loss Absorbing Capacity of Deferred Taxes',
    # IR26 - SCR Risk Modules
    'IR2601': 'SCR - Market Risk',
    'IR2602': 'SCR - Counterparty Default Risk',
    'IR2603': 'SCR - Life Underwriting Risk',
    'IR2604': 'SCR - Health Underwriting Risk',
    'IR2605': 'SCR - Non-Life Underwriting Risk',
    'IR2606': 'SCR - Operational Risk',
    'IR2607': 'SCR - Simplifications',
    # IR27 - Catastrophe Risk
    'IR2701': 'SCR - Non-Life and Health Catastrophe Risk',
    # IR28 - MCR
    'IR2801': 'MCR - Only Life or Only Non-Life Activity',
    'IR2802': 'MCR - Both Life and Non-Life Activity',
    # IR32-35 - Group
    'IR3201': 'Undertakings in the Scope of the Group',
    'IR3301': 'Insurance and Reinsurance Individual Requirements',
    'IR3401': 'Other Regulated and Non-Regulated Financial Undertakings',
    'IR3501': 'Contribution to Group Technical Provisions',
}


__all__ = [
    'generate_all_qrts',
    'QRT_TEMPLATE_MAP',
    # Shared configuration
    'UNDERTAKINGS',
    'REPORTING_DATE',
    'CURRENCIES',
    'COUNTRIES',
    'NON_LIFE_LOB',
    'LIFE_LOB',
]
