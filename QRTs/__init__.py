"""
PRA/BoE Quantitative Reporting Templates (QRT) Generators
=========================================================

Complete implementation of all 88 PRA/BoE QRT templates for Solvency II reporting.
Generates synthetic data compatible with Power BI and regulatory reporting.

Template Categories:
-------------------
1. AOC01 - Analysis of Change in SCR
2. IM00-IM03 - Internal Model Templates
3. IR0101-IR0104 - Basic Information
4. IR0201-IR0203 - Balance Sheet
5. IR0301-IR0303 - Off-Balance Sheet Items
6. IR0502-IR0510 - Premiums, Claims, Expenses
7. IR0602-IR0603 - Assets
8. IR0801 - Open Derivatives
9. IR0901 - Income, Gains and Losses
10. IR1001 - Securities Lending and Repos
11. IR1101 - Assets Held as Collateral
12. IR1201-IR1206 - Life Technical Provisions
13. IR1401 - Life Obligations Analysis
14. IR1601-IR1602 - Non-Life Annuities
15. IR1701-IR1703 - Non-Life Technical Provisions
16. IR1801-IR1802 - Non-Life Cash Flow Projections
17. IR1901-IR1902 - Non-Life Insurance Claims
18. IR2001 - Claims Distribution Development
19. IR2102, IR2104 - Underwriting Risks
20. IR2201, IR2204, IR2207 - LTG Measures
21. IR2301-IR2305 - Own Funds
22. IR2401 - Participations
23. IR2504-IR2506 - SCR Overview
24. IR2601-IR2607 - SCR Risk Modules
25. IR2701 - Catastrophe Risk
26. IR2801-IR2802 - MCR
27. IR3003-IR3008 - Outwards Reinsurance
28. IR3101 - Reinsurance Balance Sheet
29. IR3201 - Group Scope
30. IR3301 - Individual Requirements
31. IR3401 - Other Undertakings
32. IR3501 - Group Technical Provisions
33. IR3601-IR3604 - IGT
34. IRR2202-IRR2203 - Matching Adjustment
35. MALIR - Matching Adjustment Life Insurance Return
36. MR01 - Market Risk Sensitivities
37. QMC01 - Quarterly Model Change

Usage:
------
from QRTs import generate_all_qrts
all_data = generate_all_qrts()

Or import specific generators:
from QRTs.qrt_master_generator import generate_ir0201_balance_sheet
"""

from .qrt_master_generator import (
    generate_aoc01_analysis_of_change,
    generate_im00_submission_content,
    generate_im01_life_outputs,
    generate_im02_counterparty_risk,
    generate_im03_non_life_outputs,
    generate_ir0101_submission_content,
    generate_ir0102_basic_info_general,
    generate_ir0103_rff_matching_portfolios,
    generate_ir0104_branch_info,
    generate_ir0201_balance_sheet,
    generate_ir0202_assets_liabilities_by_currency,
    generate_ir0203_branch_balance_sheet,
    generate_ir0301_off_balance_sheet_general,
    generate_ir0302_guarantees_received,
    generate_ir0303_guarantees_provided,
)

from .qrt_premiums_claims_assets import (
    generate_ir0502_premiums_claims_by_country,
    generate_ir0503_life_income_expenditure,
    generate_ir0504_non_life_income_expenditure,
    generate_ir0505_life_premiums_claims_by_country,
    generate_ir0506_non_life_premiums_claims_by_country,
    generate_ir0507_fgi_business_model,
    generate_ir0508_pooling_arrangements,
    generate_ir0509_assessable_mutuals,
    generate_ir0510_excess_capital,
    generate_ir0602_list_of_assets,
    generate_ir0603_ciu_look_through,
    generate_ir0801_open_derivatives,
    generate_ir0901_income_gains_losses,
    generate_ir1001_securities_lending_repos,
    generate_ir1101_assets_collateral,
)

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
    generate_ir1901_non_life_claims,
    generate_ir1902_gl_claims_development,
    generate_ir2001_claims_distribution,
    generate_ir2102_non_life_underwriting_risks,
    generate_ir2104_cyber_underwriting_risk,
)

from .qrt_capital_scr import (
    generate_ir2201_ltg_impact,
    generate_ir2204_transitional_interest_rates,
    generate_ir2207_va_by_currency,
    generate_ir2301_own_funds,
    generate_ir2302_own_funds_by_tier,
    generate_ir2303_own_funds_movements,
    generate_ir2304_own_funds_items,
    generate_ir2305_lloyds_capital,
    generate_ir2401_participations,
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

from .qrt_reinsurance_group import (
    generate_ir3003_non_life_ri_contracts,
    generate_ir3004_non_life_ri_exposures,
    generate_ir3005_reinsurer_entity_info,
    generate_ir3006_life_ri_summary,
    generate_ir3007_life_ri_proportional,
    generate_ir3008_life_ri_non_proportional,
    generate_ir3101_ri_balance_sheet,
    generate_ir3201_group_scope,
    generate_ir3301_individual_requirements,
    generate_ir3401_other_undertakings,
    generate_ir3501_group_tp_contribution,
    generate_ir3601_igt_equity_debt,
    generate_ir3602_igt_derivatives,
    generate_ir3604_igt_other,
    generate_irr2202_ma_cash_flows,
    generate_irr2203_ma_calculation,
)

from .qrt_special_templates import (
    generate_malir_summary,
    generate_malir_portfolio_details,
    generate_malir_asset_listing,
    generate_malir_liability_analysis,
    generate_malir_cash_flow_matching,
    generate_malir_stress_tests,
    generate_mr01_market_risk_sensitivities,
    generate_mr01_duration_analysis,
    generate_qmc01_model_change,
    generate_qmc01_cumulative_changes,
)


def generate_all_qrts():
    """
    Generate all QRT templates and return as a dictionary of DataFrames.

    Returns:
        dict: Dictionary with template names as keys and DataFrames as values.
    """
    templates = {}

    # AOC
    templates['AOC01_Analysis_Of_Change_SCR'] = generate_aoc01_analysis_of_change()

    # Internal Model (IM)
    templates['IM00_Submission_Content'] = generate_im00_submission_content()
    templates['IM01_Life_Outputs'] = generate_im01_life_outputs()
    templates['IM02_Counterparty_Risk'] = generate_im02_counterparty_risk()
    templates['IM03_Non_Life_Outputs'] = generate_im03_non_life_outputs()

    # Basic Information (IR01)
    templates['IR0101_Submission_Content'] = generate_ir0101_submission_content()
    templates['IR0102_Basic_Info_General'] = generate_ir0102_basic_info_general()
    templates['IR0103_RFF_Matching_Portfolios'] = generate_ir0103_rff_matching_portfolios()
    templates['IR0104_Branch_Info'] = generate_ir0104_branch_info()

    # Balance Sheet (IR02)
    templates['IR0201_Balance_Sheet'] = generate_ir0201_balance_sheet()
    templates['IR0202_Assets_Liabilities_Currency'] = generate_ir0202_assets_liabilities_by_currency()
    templates['IR0203_Branch_Balance_Sheet'] = generate_ir0203_branch_balance_sheet()

    # Off-Balance Sheet (IR03)
    templates['IR0301_Off_Balance_Sheet_General'] = generate_ir0301_off_balance_sheet_general()
    templates['IR0302_Guarantees_Received'] = generate_ir0302_guarantees_received()
    templates['IR0303_Guarantees_Provided'] = generate_ir0303_guarantees_provided()

    # Premiums, Claims, Expenses (IR05)
    templates['IR0502_Premiums_Claims_Country'] = generate_ir0502_premiums_claims_by_country()
    templates['IR0503_Life_Income_Expenditure'] = generate_ir0503_life_income_expenditure()
    templates['IR0504_Non_Life_Income_Expenditure'] = generate_ir0504_non_life_income_expenditure()
    templates['IR0505_Life_Premiums_Claims_Country'] = generate_ir0505_life_premiums_claims_by_country()
    templates['IR0506_Non_Life_Premiums_Claims_Country'] = generate_ir0506_non_life_premiums_claims_by_country()
    templates['IR0507_FGI_Business_Model'] = generate_ir0507_fgi_business_model()
    templates['IR0508_Pooling_Arrangements'] = generate_ir0508_pooling_arrangements()
    templates['IR0509_Assessable_Mutuals'] = generate_ir0509_assessable_mutuals()
    templates['IR0510_Excess_Capital'] = generate_ir0510_excess_capital()

    # Assets (IR06)
    templates['IR0602_List_Of_Assets'] = generate_ir0602_list_of_assets()
    templates['IR0603_CIU_Look_Through'] = generate_ir0603_ciu_look_through()

    # Derivatives (IR08)
    templates['IR0801_Open_Derivatives'] = generate_ir0801_open_derivatives()

    # Income/Gains (IR09)
    templates['IR0901_Income_Gains_Losses'] = generate_ir0901_income_gains_losses()

    # Securities/Collateral (IR10-11)
    templates['IR1001_Securities_Lending_Repos'] = generate_ir1001_securities_lending_repos()
    templates['IR1101_Assets_Collateral'] = generate_ir1101_assets_collateral()

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

    # Underwriting Risks (IR21)
    templates['IR2102_Non_Life_Underwriting_Risks'] = generate_ir2102_non_life_underwriting_risks()
    templates['IR2104_Cyber_Underwriting_Risk'] = generate_ir2104_cyber_underwriting_risk()

    # LTG Measures (IR22)
    templates['IR2201_LTG_Impact'] = generate_ir2201_ltg_impact()
    templates['IR2204_Transitional_Interest_Rates'] = generate_ir2204_transitional_interest_rates()
    templates['IR2207_VA_By_Currency'] = generate_ir2207_va_by_currency()

    # Own Funds (IR23)
    templates['IR2301_Own_Funds'] = generate_ir2301_own_funds()
    templates['IR2302_Own_Funds_By_Tier'] = generate_ir2302_own_funds_by_tier()
    templates['IR2303_Own_Funds_Movements'] = generate_ir2303_own_funds_movements()
    templates['IR2304_Own_Funds_Items'] = generate_ir2304_own_funds_items()
    templates['IR2305_Lloyds_Capital'] = generate_ir2305_lloyds_capital()

    # Participations (IR24)
    templates['IR2401_Participations'] = generate_ir2401_participations()

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

    # Reinsurance (IR30-31)
    templates['IR3003_Non_Life_RI_Contracts'] = generate_ir3003_non_life_ri_contracts()
    templates['IR3004_Non_Life_RI_Exposures'] = generate_ir3004_non_life_ri_exposures()
    templates['IR3005_Reinsurer_Entity_Info'] = generate_ir3005_reinsurer_entity_info()
    templates['IR3006_Life_RI_Summary'] = generate_ir3006_life_ri_summary()
    templates['IR3007_Life_RI_Proportional'] = generate_ir3007_life_ri_proportional()
    templates['IR3008_Life_RI_Non_Proportional'] = generate_ir3008_life_ri_non_proportional()
    templates['IR3101_RI_Balance_Sheet'] = generate_ir3101_ri_balance_sheet()

    # Group (IR32-36)
    templates['IR3201_Group_Scope'] = generate_ir3201_group_scope()
    templates['IR3301_Individual_Requirements'] = generate_ir3301_individual_requirements()
    templates['IR3401_Other_Undertakings'] = generate_ir3401_other_undertakings()
    templates['IR3501_Group_TP_Contribution'] = generate_ir3501_group_tp_contribution()
    templates['IR3601_IGT_Equity_Debt'] = generate_ir3601_igt_equity_debt()
    templates['IR3602_IGT_Derivatives'] = generate_ir3602_igt_derivatives()
    templates['IR3604_IGT_Other'] = generate_ir3604_igt_other()

    # Matching Adjustment (IRR22)
    templates['IRR2202_MA_Cash_Flows'] = generate_irr2202_ma_cash_flows()
    templates['IRR2203_MA_Calculation'] = generate_irr2203_ma_calculation()

    # MALIR
    templates['MALIR_Summary'] = generate_malir_summary()
    templates['MALIR_Portfolio_Details'] = generate_malir_portfolio_details()
    templates['MALIR_Asset_Listing'] = generate_malir_asset_listing()
    templates['MALIR_Liability_Analysis'] = generate_malir_liability_analysis()
    templates['MALIR_Cash_Flow_Matching'] = generate_malir_cash_flow_matching()
    templates['MALIR_Stress_Tests'] = generate_malir_stress_tests()

    # MR01
    templates['MR01_Market_Risk_Sensitivities'] = generate_mr01_market_risk_sensitivities()
    templates['MR01_Duration_Analysis'] = generate_mr01_duration_analysis()

    # QMC01
    templates['QMC01_Model_Change'] = generate_qmc01_model_change()
    templates['QMC01_Cumulative_Changes'] = generate_qmc01_cumulative_changes()

    return templates


# Template mapping for reference
QRT_TEMPLATE_MAP = {
    # AOC
    'AOC01': 'Analysis of Change in SCR',
    # IM
    'IM00': 'Internal Model - Content of Submission',
    'IM01': 'Internal Model Outputs - Life',
    'IM02': 'Internal Model - Counterparty Risk',
    'IM03': 'Internal Model Outputs - Non-Life',
    # IR01 - Basic Information
    'IR0101': 'Content of the Submission',
    'IR0102': 'Basic Information - General',
    'IR0103': 'Basic Information - RFF and Matching Adjustment Portfolios',
    'IR0104': 'Basic Information - Branch/Legal Entity',
    # IR02 - Balance Sheet
    'IR0201': 'Balance Sheet',
    'IR0202': 'Assets and Liabilities by Currency',
    'IR0203': 'Additional Branch Balance Sheet Information',
    # IR03 - Off-Balance Sheet
    'IR0301': 'Off-Balance Sheet Items - General',
    'IR0302': 'Off-Balance Sheet Items - Unlimited Guarantees Received',
    'IR0303': 'Off-Balance Sheet Items - Unlimited Guarantees Provided',
    # IR05 - Premiums/Claims/Expenses
    'IR0502': 'Premiums, Claims and Expenses by Country',
    'IR0503': 'Life Income and Expenditure',
    'IR0504': 'Non-Life Income, Expenditure and Business Model Analysis',
    'IR0505': 'Life Premiums and Claims by Country',
    'IR0506': 'Non-Life Premiums and Claims by Country',
    'IR0507': 'Business Model Analysis - Financial Guarantee Insurers',
    'IR0508': 'Material Pooling Arrangements',
    'IR0509': 'Assessable Mutuals',
    'IR0510': 'Excess Capital Generation',
    # IR06 - Assets
    'IR0602': 'List of Assets',
    'IR0603': 'Collective Investment Undertakings - Look-Through Approach',
    # IR08 - Derivatives
    'IR0801': 'Open Derivatives',
    # IR09 - Income/Gains
    'IR0901': 'Income, Gains and Losses in the Period',
    # IR10 - Securities Lending
    'IR1001': 'Securities Lending and Repos',
    # IR11 - Collateral
    'IR1101': 'Assets Held as Collateral',
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
    # IR21 - Underwriting Risks
    'IR2102': 'Non-Life Underwriting Risks',
    'IR2104': 'Cyber Underwriting Risk',
    # IR22 - LTG Measures
    'IR2201': 'Impact of Long-Term Guarantees Measures and Transitionals',
    'IR2204': 'Information on the Transitional on Interest Rates Calculation',
    'IR2207': 'Best Estimate Subject to Volatility Adjustment by Currency',
    # IR23 - Own Funds
    'IR2301': 'Own Funds',
    'IR2302': 'Detailed Information by Tiers on Own Funds',
    'IR2303': 'Annual Movements on Own Funds',
    'IR2304': 'List of Items on Own Funds',
    'IR2305': 'Society of Lloyd\'s Own Funds and Capital Requirements',
    # IR24 - Participations
    'IR2401': 'Participations Held',
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
    # IR30-31 - Reinsurance
    'IR3003': 'Non-Life Outwards Reinsurance Contract Information',
    'IR3004': 'Non-Life Outwards Reinsurance Contract Reinsurer Exposures',
    'IR3005': 'Reinsurer and Collateral Provider Entity Information',
    'IR3006': 'Life Outwards Reinsurance Summary',
    'IR3007': 'Life Outwards Proportional Reinsurance',
    'IR3008': 'Life Outwards Non-Proportional Reinsurance',
    'IR3101': 'Outwards Reinsurance Balance Sheet Exposures',
    # IR32-36 - Group
    'IR3201': 'Undertakings in the Scope of the Group',
    'IR3301': 'Insurance and Reinsurance Individual Requirements',
    'IR3401': 'Other Regulated and Non-Regulated Financial Undertakings',
    'IR3501': 'Contribution to Group Technical Provisions',
    'IR3601': 'IGT - Equity-Type Transactions, Debt and Asset Transfer',
    'IR3602': 'IGT - Derivatives',
    'IR3604': 'IGT - Cost Sharing, Contingent Liabilities, Off-BS and Other Items',
    # IRR22 - Matching Adjustment
    'IRR2202': 'Matching Adjustment Portfolio Projection of Future Cash Flows',
    'IRR2203': 'Matching Adjustment Calculation',
    # Special Templates
    'MALIR': 'Matching Adjustment Life Insurance Return',
    'MR01': 'Market Risk Sensitivities',
    'QMC01': 'Quarterly Model Change',
}


__all__ = [
    'generate_all_qrts',
    'QRT_TEMPLATE_MAP',
]
