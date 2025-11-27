"""
PRA/BoE Other Regulatory Templates (OTH) Generators
====================================================

Non-IR regulatory templates for Solvency II reporting.
These templates are separate from the main QRT IR-series returns.

Template Categories:
--------------------
1. AOC01 - Analysis of Change in SCR
2. IM00-IM03 - Internal Model Templates
3. MALIR - Matching Adjustment Life Insurance Return
4. MR01 - Market Risk Sensitivities
5. QMC01 - Quarterly Model Change

Usage:
------
from OTH import generate_all_oth
all_data = generate_all_oth()

Or import specific generators:
from OTH.oth_internal_model import generate_aoc01_analysis_of_change
"""

# Internal Model Templates (AOC, IM)
from .oth_internal_model import (
    generate_aoc01_analysis_of_change,
    generate_im00_submission_content,
    generate_im01_life_outputs,
    generate_im02_counterparty_risk,
    generate_im03_non_life_outputs,
    UNDERTAKINGS,
    REPORTING_DATE,
)

# Special Templates (MALIR, MR01, QMC01)
from .oth_special_templates import (
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


def generate_all_oth():
    """
    Generate all OTH (non-IR) templates and return as a dictionary of DataFrames.

    Returns:
        dict: Dictionary with template names as keys and DataFrames as values.
    """
    templates = {}

    # AOC - Analysis of Change
    templates['AOC01_Analysis_Of_Change_SCR'] = generate_aoc01_analysis_of_change()

    # Internal Model (IM)
    templates['IM00_Submission_Content'] = generate_im00_submission_content()
    templates['IM01_Life_Outputs'] = generate_im01_life_outputs()
    templates['IM02_Counterparty_Risk'] = generate_im02_counterparty_risk()
    templates['IM03_Non_Life_Outputs'] = generate_im03_non_life_outputs()

    # MALIR - Matching Adjustment Life Insurance Return
    templates['MALIR_Summary'] = generate_malir_summary()
    templates['MALIR_Portfolio_Details'] = generate_malir_portfolio_details()
    templates['MALIR_Asset_Listing'] = generate_malir_asset_listing()
    templates['MALIR_Liability_Analysis'] = generate_malir_liability_analysis()
    templates['MALIR_Cash_Flow_Matching'] = generate_malir_cash_flow_matching()
    templates['MALIR_Stress_Tests'] = generate_malir_stress_tests()

    # MR01 - Market Risk Sensitivities
    templates['MR01_Market_Risk_Sensitivities'] = generate_mr01_market_risk_sensitivities()
    templates['MR01_Duration_Analysis'] = generate_mr01_duration_analysis()

    # QMC01 - Quarterly Model Change
    templates['QMC01_Model_Change'] = generate_qmc01_model_change()
    templates['QMC01_Cumulative_Changes'] = generate_qmc01_cumulative_changes()

    return templates


# Template mapping for reference
OTH_TEMPLATE_MAP = {
    # AOC
    'AOC01': 'Analysis of Change in SCR',
    # IM - Internal Model
    'IM00': 'Internal Model - Content of Submission',
    'IM01': 'Internal Model Outputs - Life',
    'IM02': 'Internal Model - Counterparty Risk',
    'IM03': 'Internal Model Outputs - Non-Life',
    # MALIR
    'MALIR': 'Matching Adjustment Life Insurance Return',
    # MR
    'MR01': 'Market Risk Sensitivities',
    # QMC
    'QMC01': 'Quarterly Model Change',
}


__all__ = [
    'generate_all_oth',
    'OTH_TEMPLATE_MAP',
    'UNDERTAKINGS',
    'REPORTING_DATE',
]
