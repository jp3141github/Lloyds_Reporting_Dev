"""
Solvency II QSR Reporting Generator for Power BI
================================================
Generates Quarterly Solvency Return (QSR) reports for Lloyd's syndicates.
Compatible with Power BI as a Python data source.

Tables Generated:
- QSR030_Basic_Information: Control form - Basic submission information
- QSR031_Content_Of_Submission: Control form - List of forms submitted
- QSR002_Balance_Sheet: S.02.01.02 Balance Sheet
- QSR210_Reconciliation: UK GAAP to Solvency II Own Funds reconciliation
- QSR220_Own_Funds: S.23.01.01 Own Funds
- QSR240_Technical_Provisions: S.17.01.02 Non-Life Technical Provisions
- QSR440_Premiums_Claims: S.05.01.02.01 Premiums & Claims
- QSR291_Operational_Risk: S.41.01.11 Operational Risk
- QSR292_Market_Risk: S.14.01.10.01 Market Risk
- QSR293_Counterparty_Risk: S.38.01.10.01 Counterparty Default Risk
- QSR510_MCR: S.28.01.01 MCR Calculation
- QSR923_Cash_Transfer: Cash Transfer Statement (Q4 only)
- SCR_Summary: SCR with all risk modules
- Solvency_Ratio_Report: Solvency coverage ratios

Usage in Power BI:
1. Get Data > More > Python script
2. Copy and paste this script
3. Select the tables you need from the list
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
SYNDICATES = [2987, 33, 1183, 2791, 623, 4242, 5000, 1910, 2010, 2525]
REPORTING_DATE = '2024-12-31'

# Lines of Business for technical provisions
LINES_OF_BUSINESS = [
    'Motor vehicle liability',
    'Other motor',
    'Marine, aviation, transport',
    'Fire and other property damage',
    'General liability',
    'Credit and suretyship',
    'Legal expenses',
    'Assistance',
    'Miscellaneous'
]


def generate_qsr030_basic_information():
    """Generate QSR 030 - Basic Information (Control Form)"""
    data = []

    for syndicate in SYNDICATES:
        data.append({
            'Syndicate': syndicate,
            'Reporting_Date': REPORTING_DATE,
            'Reporting_Reference_Date': REPORTING_DATE,
            'Reporting_Currency': 'GBP',
            'Accounting_Standards': 'UK GAAP',
            'Method_Of_Calculation': 'Standard Formula',
            'Use_Of_USP': 'No',
            'Use_Of_Matching_Adjustment': 'No',
            'Use_Of_Volatility_Adjustment': 'No',
            'Use_Of_Transitional_RFR': 'No',
            'Use_Of_Transitional_TP': 'No',
            'Initial_Submission': 'Yes',
            'Managing_Agent': f'Managing Agent {syndicate}',
            'Syndicate_Name': f'Syndicate {syndicate}',
            'LEI_Code': f'LEI{syndicate:08d}XXXX',
            'Quarter': 'Q4',
            'Year': 2024,
            'Submission_Date': datetime.now().strftime('%Y-%m-%d'),
            'Prepared_By': f'Compliance Officer {syndicate}'
        })

    return pd.DataFrame(data)


def generate_qsr031_content_of_submission():
    """Generate QSR 031 - Content of Submission (Control Form)"""
    # List of forms included in Non-Life QSR submission
    forms_list = [
        ('QSR.01.02', 'S.01.02.01', 'Basic Information - General', True),
        ('QSR.02.01', 'S.02.01.02', 'Balance Sheet', True),
        ('QSR.05.01', 'S.05.01.02', 'Premiums, Claims and Expenses by LOB', True),
        ('QSR.12.01', 'S.12.01.02', 'Life and Health SLT TP', False),  # Not applicable for Non-Life
        ('QSR.17.01', 'S.17.01.02', 'Non-Life Technical Provisions', True),
        ('QSR.19.01', 'S.19.01.21', 'Non-Life Insurance Claims', True),
        ('QSR.23.01', 'S.23.01.01', 'Own Funds', True),
        ('QSR.25.01', 'S.25.01.21', 'SCR Standard Formula', True),
        ('QSR.28.01', 'S.28.01.01', 'MCR - Non-Life and Non-SLT Health', True),
        ('QSR.21.00', 'QSR.21.00', 'Balance Sheet Reconciliation', True),
        ('QSR.92.30', 'QSR.92.30', 'Cash Transfer Statement', True),
    ]

    data = []
    for syndicate in SYNDICATES:
        for form_code, template_code, description, included in forms_list:
            data.append({
                'Syndicate': syndicate,
                'Reporting_Date': REPORTING_DATE,
                'Form_Code': form_code,
                'Template_Code': template_code,
                'Form_Description': description,
                'Included_In_Submission': included,
                'Reason_For_Exclusion': '' if included else 'Not applicable - Non-Life syndicate',
                'Number_Of_Records': random.randint(1, 100) if included else 0
            })

    return pd.DataFrame(data)


def generate_qsr210_reconciliation():
    """
    Generate QSR 210 - Balance Sheet Reconciliation
    Reconciles UK GAAP Members' Balances to Solvency II Own Funds
    This is mandatory for all Lloyd's syndicates.
    """
    data = []

    for syndicate in SYNDICATES:
        # UK GAAP figures (starting point)
        uk_gaap_members_balance = random.randint(100000000, 400000000)

        # Reconciliation adjustments
        reserve_strength_adj = random.randint(-30000000, 30000000)  # Reserve margin differences
        risk_margin_adj = -random.randint(5000000, 30000000)  # Risk margin (SII specific)
        valuation_diff_investments = random.randint(-10000000, 20000000)  # Investment revaluation
        valuation_diff_tp = random.randint(-20000000, 20000000)  # TP valuation differences
        deferred_tax_adj = random.randint(-5000000, 10000000)  # Deferred tax differences
        intangibles_adj = -random.randint(1000000, 10000000)  # Intangibles removed
        dac_adj = -random.randint(5000000, 25000000)  # DAC removed under SII
        pension_adj = random.randint(-2000000, 5000000)  # Pension adjustments
        other_adj = random.randint(-5000000, 5000000)  # Other adjustments

        total_adjustments = (reserve_strength_adj + risk_margin_adj + valuation_diff_investments +
                            valuation_diff_tp + deferred_tax_adj + intangibles_adj +
                            dac_adj + pension_adj + other_adj)

        sii_own_funds = uk_gaap_members_balance + total_adjustments

        data.append({
            'Syndicate': syndicate,
            'Reporting_Date': REPORTING_DATE,
            # UK GAAP Starting Point
            'R0010_UK_GAAP_Members_Balance': uk_gaap_members_balance,
            # Adjustment items
            'R0020_Reserve_Strength_Adjustment': reserve_strength_adj,
            'R0030_Risk_Margin_Adjustment': risk_margin_adj,
            'R0040_Investment_Valuation_Difference': valuation_diff_investments,
            'R0050_TP_Valuation_Difference': valuation_diff_tp,
            'R0060_Deferred_Tax_Adjustment': deferred_tax_adj,
            'R0070_Intangibles_Adjustment': intangibles_adj,
            'R0080_DAC_Adjustment': dac_adj,
            'R0090_Pension_Adjustment': pension_adj,
            'R0100_Other_Adjustments': other_adj,
            'R0110_Total_Adjustments': total_adjustments,
            # Solvency II End Point
            'R0120_Solvency_II_Own_Funds': sii_own_funds,
            # Reconciliation status
            'Reconciliation_Status': 'Reconciled',
            'Variance_Pct': round(total_adjustments / uk_gaap_members_balance * 100, 2) if uk_gaap_members_balance > 0 else 0
        })

    return pd.DataFrame(data)


def generate_qsr923_cash_transfer():
    """
    Generate QSR 923 - Cash Transfer Statement
    Handles Open Year Profit releases and cash transfers from trust funds (LDTF/SLTF).
    Critical for Q4 reporting.
    """
    data = []

    for syndicate in SYNDICATES:
        # Open Year Profits calculation
        prior_year_profit = random.randint(5000000, 50000000)
        current_year_profit = random.randint(-10000000, 60000000)
        total_open_year_profit = prior_year_profit + current_year_profit

        # Trust fund balances
        ldtf_opening = random.randint(50000000, 200000000)  # Lloyd's Deposit Trust Fund
        sltf_opening = random.randint(20000000, 100000000)  # Surplus Lines Trust Fund

        # Cash movements
        ldtf_cash_in = random.randint(10000000, 80000000)
        ldtf_cash_out = random.randint(5000000, 50000000)
        sltf_cash_in = random.randint(5000000, 40000000)
        sltf_cash_out = random.randint(2000000, 30000000)

        ldtf_closing = ldtf_opening + ldtf_cash_in - ldtf_cash_out
        sltf_closing = sltf_opening + sltf_cash_in - sltf_cash_out

        # Profit release (typically from closed years)
        profit_release_amount = random.randint(0, 30000000)
        profit_release_yoa = random.choice([2020, 2021, 2022])

        # Members' balances movements
        members_balance_opening = random.randint(80000000, 300000000)
        contributions = random.randint(10000000, 50000000)
        distributions = random.randint(5000000, 40000000)
        members_balance_closing = members_balance_opening + contributions - distributions

        data.append({
            'Syndicate': syndicate,
            'Reporting_Date': REPORTING_DATE,
            'Reporting_Quarter': 'Q4',
            # Open Year Profits Section
            'R0010_Prior_Year_Open_Profit': prior_year_profit,
            'R0020_Current_Year_Open_Profit': current_year_profit,
            'R0030_Total_Open_Year_Profit': total_open_year_profit,
            # LDTF (Lloyd's Deposit Trust Fund) Section
            'R0040_LDTF_Opening_Balance': ldtf_opening,
            'R0050_LDTF_Cash_Inflows': ldtf_cash_in,
            'R0060_LDTF_Cash_Outflows': ldtf_cash_out,
            'R0070_LDTF_Closing_Balance': ldtf_closing,
            # SLTF (Surplus Lines Trust Fund) Section
            'R0080_SLTF_Opening_Balance': sltf_opening,
            'R0090_SLTF_Cash_Inflows': sltf_cash_in,
            'R0100_SLTF_Cash_Outflows': sltf_cash_out,
            'R0110_SLTF_Closing_Balance': sltf_closing,
            # Profit Release Section
            'R0120_Profit_Release_Amount': profit_release_amount,
            'R0130_Profit_Release_YOA': profit_release_yoa,
            'R0140_Release_Approved': 'Yes' if profit_release_amount > 0 else 'N/A',
            # Members' Balances Section
            'R0150_Members_Balance_Opening': members_balance_opening,
            'R0160_Member_Contributions': contributions,
            'R0170_Member_Distributions': distributions,
            'R0180_Members_Balance_Closing': members_balance_closing,
            # Totals
            'R0190_Total_Trust_Fund_Assets': ldtf_closing + sltf_closing,
            'Transfer_Status': 'Completed'
        })

    return pd.DataFrame(data)


def generate_qsr002_balance_sheet():
    """Generate QSR 002 - Overall Balance Sheet (S.02.01.02)"""
    data = []

    for syndicate in SYNDICATES:
        # Assets
        goodwill = 0
        dac = random.randint(5000000, 50000000)
        intangible = random.randint(1000000, 10000000)
        deferred_tax_assets = random.randint(500000, 5000000)
        pension_surplus = random.randint(0, 2000000)
        ppe = random.randint(2000000, 20000000)
        investments = random.randint(100000000, 500000000)
        holdings = random.randint(0, 10000000)
        equities = random.randint(10000000, 80000000)
        bonds = random.randint(50000000, 300000000)
        gov_bonds = int(bonds * 0.4)
        corp_bonds = int(bonds * 0.6)
        collective = random.randint(5000000, 50000000)
        derivatives = random.randint(-5000000, 10000000)
        deposits = random.randint(5000000, 30000000)
        ri_recoverables = random.randint(20000000, 150000000)
        insurance_receivables = random.randint(10000000, 80000000)
        reins_receivables = random.randint(5000000, 40000000)
        trade_receivables = random.randint(2000000, 15000000)
        cash = random.randint(20000000, 100000000)
        other_assets = random.randint(1000000, 10000000)

        total_assets = (dac + intangible + deferred_tax_assets + pension_surplus +
                       ppe + investments + equities + bonds + collective +
                       deposits + ri_recoverables + insurance_receivables +
                       reins_receivables + trade_receivables + cash + other_assets)

        # Liabilities
        tp_nonlife = random.randint(80000000, 400000000)
        tp_life = random.randint(0, 20000000)
        best_estimate = int((tp_nonlife + tp_life) * 0.9)
        risk_margin = int((tp_nonlife + tp_life) * 0.1)
        deposits_reins = random.randint(5000000, 30000000)
        deferred_tax_liab = random.randint(1000000, 10000000)
        derivatives_liab = max(0, -derivatives) if derivatives < 0 else random.randint(0, 5000000)
        debts_credit = random.randint(0, 10000000)
        insurance_payables = random.randint(5000000, 40000000)
        reins_payables = random.randint(3000000, 25000000)
        trade_payables = random.randint(1000000, 10000000)
        other_liab = random.randint(500000, 5000000)

        total_liabilities = (tp_nonlife + tp_life + deposits_reins + deferred_tax_liab +
                            derivatives_liab + debts_credit + insurance_payables +
                            reins_payables + trade_payables + other_liab)

        excess = total_assets - total_liabilities

        data.append({
            'Syndicate': syndicate,
            'Reporting_Date': REPORTING_DATE,
            'R0010_Goodwill': goodwill,
            'R0020_Deferred_Acquisition_Costs': dac,
            'R0030_Intangible_Assets': intangible,
            'R0040_Deferred_Tax_Assets': deferred_tax_assets,
            'R0050_Pension_Benefit_Surplus': pension_surplus,
            'R0060_Property_Plant_Equipment': ppe,
            'R0070_Investments': investments,
            'R0080_Holdings_Related_Undertakings': holdings,
            'R0090_Equities': equities,
            'R0100_Bonds': bonds,
            'R0110_Government_Bonds': gov_bonds,
            'R0120_Corporate_Bonds': corp_bonds,
            'R0130_Collective_Investments': collective,
            'R0140_Derivatives': max(0, derivatives),
            'R0150_Deposits_Other_Than_Cash': deposits,
            'R0160_Reinsurance_Recoverables': ri_recoverables,
            'R0170_Insurance_Receivables': insurance_receivables,
            'R0180_Reinsurance_Receivables': reins_receivables,
            'R0190_Receivables_Trade': trade_receivables,
            'R0200_Cash_and_Cash_Equivalents': cash,
            'R0210_Other_Assets': other_assets,
            'R0220_Total_Assets': total_assets,
            'R0230_Technical_Provisions_NonLife': tp_nonlife,
            'R0240_Technical_Provisions_Life': tp_life,
            'R0250_Best_Estimate': best_estimate,
            'R0260_Risk_Margin': risk_margin,
            'R0270_Deposits_From_Reinsurers': deposits_reins,
            'R0280_Deferred_Tax_Liabilities': deferred_tax_liab,
            'R0290_Derivatives_Liabilities': derivatives_liab,
            'R0300_Debts_Credit_Institutions': debts_credit,
            'R0310_Insurance_Payables': insurance_payables,
            'R0320_Reinsurance_Payables': reins_payables,
            'R0330_Payables_Trade': trade_payables,
            'R0340_Other_Liabilities': other_liab,
            'R0350_Total_Liabilities': total_liabilities,
            'R0360_Excess_Assets_Over_Liabilities': excess
        })

    return pd.DataFrame(data)


def generate_qsr220_own_funds():
    """Generate QSR 220 - Own Funds (S.23.01.01)"""
    data = []

    for syndicate in SYNDICATES:
        members_fis = random.randint(50000000, 300000000)
        subordinated = random.randint(0, 50000000)
        reconciliation = random.randint(-20000000, 50000000)
        deductions = random.randint(0, 10000000)

        tier1_unrestricted = members_fis + reconciliation - deductions
        tier1_restricted = random.randint(0, 20000000)
        tier2 = subordinated
        tier3 = random.randint(0, 5000000)

        total_own_funds = tier1_unrestricted + tier1_restricted + tier2 + tier3
        eligible_scr = total_own_funds  # Simplified
        eligible_mcr = tier1_unrestricted + tier1_restricted + min(tier2, eligible_scr * 0.2)

        data.append({
            'Syndicate': syndicate,
            'Reporting_Date': REPORTING_DATE,
            'R0040_Members_Contributions_FIS_Tier1_Unrestricted': members_fis,
            'R0050_Subordinated_Liabilities_Tier2': subordinated,
            'R0060_Reconciliation_Reserve': reconciliation,
            'R0070_Deductions': deductions,
            'R0080_Tier_1_Unrestricted': tier1_unrestricted,
            'R0090_Tier_1_Restricted': tier1_restricted,
            'R0100_Tier_2': tier2,
            'R0110_Tier_3': tier3,
            'R0120_Total_Own_Funds': total_own_funds,
            'R0130_Eligible_Own_Funds_SCR': eligible_scr,
            'R0140_Eligible_Own_Funds_MCR': eligible_mcr
        })

    return pd.DataFrame(data)


def generate_qsr240_technical_provisions():
    """Generate QSR 240 - Non-Life Technical Provisions (S.17.01.02)"""
    data = []

    for syndicate in SYNDICATES:
        for lob in LINES_OF_BUSINESS:
            be_gross = random.randint(10000000, 100000000)
            be_recoverable = int(be_gross * random.uniform(0.1, 0.3))
            be_net = be_gross - be_recoverable
            risk_margin = int(be_gross * random.uniform(0.08, 0.12))
            tp_gross = be_gross + risk_margin
            tp_recoverable = be_recoverable
            tp_net = tp_gross - tp_recoverable

            data.append({
                'Syndicate': syndicate,
                'Reporting_Date': REPORTING_DATE,
                'Line_of_Business': lob,
                'Technical_Provisions_Calculated_Whole': tp_gross,
                'Best_Estimate_Gross': be_gross,
                'Best_Estimate_Recoverable': be_recoverable,
                'Best_Estimate_Net': be_net,
                'Risk_Margin': risk_margin,
                'Technical_Provisions_Gross': tp_gross,
                'Technical_Provisions_Recoverable': tp_recoverable,
                'Technical_Provisions_Net': tp_net
            })

    return pd.DataFrame(data)


def generate_qsr440_premiums_claims():
    """Generate QSR 440 - Non-Life Insurance Claims Information (S.05.01.02.01)"""
    data = []

    for syndicate in SYNDICATES:
        for lob in LINES_OF_BUSINESS:
            pw_gross = random.randint(20000000, 150000000)
            pw_reins = int(pw_gross * random.uniform(0.15, 0.35))
            pw_net = pw_gross - pw_reins

            pe_gross = int(pw_gross * random.uniform(0.85, 0.95))
            pe_reins = int(pw_reins * random.uniform(0.85, 0.95))
            pe_net = pe_gross - pe_reins

            ci_gross = int(pe_gross * random.uniform(0.5, 0.8))
            ci_reins = int(ci_gross * random.uniform(0.15, 0.35))
            ci_net = ci_gross - ci_reins

            ctp_gross = random.randint(-5000000, 10000000)
            ctp_reins = int(ctp_gross * 0.2) if ctp_gross > 0 else int(ctp_gross * 0.3)
            ctp_net = ctp_gross - ctp_reins

            expenses = int(pe_gross * random.uniform(0.25, 0.35))

            loss_ratio = round(ci_net / pe_net * 100, 2) if pe_net > 0 else 0
            expense_ratio = round(expenses / pe_net * 100, 2) if pe_net > 0 else 0
            combined_ratio = round(loss_ratio + expense_ratio, 2)

            data.append({
                'Syndicate': syndicate,
                'Reporting_Date': REPORTING_DATE,
                'Line_of_Business': lob,
                'Premiums_Written_Gross': pw_gross,
                'Premiums_Written_Reinsurers_Share': pw_reins,
                'Premiums_Written_Net': pw_net,
                'Premiums_Earned_Gross': pe_gross,
                'Premiums_Earned_Reinsurers_Share': pe_reins,
                'Premiums_Earned_Net': pe_net,
                'Claims_Incurred_Gross': ci_gross,
                'Claims_Incurred_Reinsurers_Share': ci_reins,
                'Claims_Incurred_Net': ci_net,
                'Changes_Other_TP_Gross': ctp_gross,
                'Changes_Other_TP_Reinsurers': ctp_reins,
                'Changes_Other_TP_Net': ctp_net,
                'Expenses_Incurred': expenses,
                'Loss_Ratio': loss_ratio,
                'Expense_Ratio': expense_ratio,
                'Combined_Ratio': combined_ratio
            })

    return pd.DataFrame(data)


def generate_qsr291_operational_risk():
    """Generate QSR 291 - Operational Risk (S.41.01.11)"""
    data = []

    for syndicate in SYNDICATES:
        operational_risk = random.randint(5000000, 40000000)
        data.append({
            'Syndicate': syndicate,
            'Reporting_Date': REPORTING_DATE,
            'Operational_Risk': operational_risk
        })

    return pd.DataFrame(data)


def generate_qsr292_market_risk():
    """Generate QSR 292 - Market Risk (S.14.01.10.01)"""
    data = []

    for syndicate in SYNDICATES:
        total_market = random.randint(20000000, 120000000)
        interest_rate = int(total_market * random.uniform(0.1, 0.2))
        equity = int(total_market * random.uniform(0.15, 0.25))
        property_risk = int(total_market * random.uniform(0.05, 0.15))
        spread = int(total_market * random.uniform(0.2, 0.35))
        currency = int(total_market * random.uniform(0.1, 0.2))
        concentration = int(total_market * random.uniform(0.05, 0.15))

        data.append({
            'Syndicate': syndicate,
            'Reporting_Date': REPORTING_DATE,
            'Market_Risk_Total': total_market,
            'Interest_Rate_Risk': interest_rate,
            'Equity_Risk': equity,
            'Property_Risk': property_risk,
            'Spread_Risk': spread,
            'Currency_Risk': currency,
            'Concentration_Risk': concentration
        })

    return pd.DataFrame(data)


def generate_qsr293_counterparty_risk():
    """Generate QSR 293 - Counterparty Default Risk (S.38.01.10.01)"""
    data = []

    for syndicate in SYNDICATES:
        counterparty_risk = random.randint(10000000, 80000000)
        data.append({
            'Syndicate': syndicate,
            'Reporting_Date': REPORTING_DATE,
            'Counterparty_Default_Risk': counterparty_risk
        })

    return pd.DataFrame(data)


def generate_qsr510_mcr():
    """Generate QSR 510 - Minimum Capital Requirement (S.28.01.01)"""
    data = []

    for syndicate in SYNDICATES:
        linear_mcr = random.randint(15000000, 80000000)
        scr = random.randint(50000000, 200000000)
        mcr_cap = int(scr * 0.45)
        mcr_floor = int(scr * 0.25)
        combined_mcr = min(max(linear_mcr, mcr_floor), mcr_cap)
        absolute_floor = 4000000
        mcr = max(combined_mcr, absolute_floor)

        data.append({
            'Syndicate': syndicate,
            'Reporting_Date': REPORTING_DATE,
            'Linear_MCR': linear_mcr,
            'SCR': scr,
            'MCR_Cap': mcr_cap,
            'MCR_Floor': mcr_floor,
            'Combined_MCR': combined_mcr,
            'Absolute_Floor_MCR': absolute_floor,
            'MCR': mcr
        })

    return pd.DataFrame(data)


def generate_scr_summary():
    """Generate SCR Summary with all risk modules"""
    data = []

    for syndicate in SYNDICATES:
        market = random.randint(20000000, 120000000)
        counterparty = random.randint(10000000, 80000000)
        life_uw = random.randint(0, 10000000)
        health_uw = random.randint(5000000, 30000000)
        nonlife_uw = random.randint(30000000, 150000000)

        # Calculate BSCR with diversification
        undiversified = market + counterparty + life_uw + health_uw + nonlife_uw
        diversification = int(undiversified * random.uniform(0.15, 0.25))
        bscr = undiversified - diversification

        operational = random.randint(5000000, 40000000)
        lac_dt = random.randint(0, 10000000)
        scr = bscr + operational - lac_dt

        data.append({
            'Syndicate': syndicate,
            'Reporting_Date': REPORTING_DATE,
            'Market_Risk': market,
            'Counterparty_Default_Risk': counterparty,
            'Life_Underwriting_Risk': life_uw,
            'Health_Underwriting_Risk': health_uw,
            'Non_Life_Underwriting_Risk': nonlife_uw,
            'Diversification': diversification,
            'BSCR': bscr,
            'Operational_Risk': operational,
            'Loss_Absorbing_Capacity_DT': lac_dt,
            'SCR': scr
        })

    return pd.DataFrame(data)


def generate_solvency_ratio_report():
    """Generate Solvency Ratio Report"""
    own_funds = generate_qsr220_own_funds()
    scr_data = generate_scr_summary()
    mcr_data = generate_qsr510_mcr()

    data = []

    for syndicate in SYNDICATES:
        of_row = own_funds[own_funds['Syndicate'] == syndicate].iloc[0]
        scr_row = scr_data[scr_data['Syndicate'] == syndicate].iloc[0]
        mcr_row = mcr_data[mcr_data['Syndicate'] == syndicate].iloc[0]

        scr_ratio = round(of_row['R0130_Eligible_Own_Funds_SCR'] / scr_row['SCR'] * 100, 2)
        mcr_ratio = round(of_row['R0140_Eligible_Own_Funds_MCR'] / mcr_row['MCR'] * 100, 2)

        data.append({
            'Syndicate': syndicate,
            'Reporting_Date': REPORTING_DATE,
            'Total_Own_Funds': of_row['R0120_Total_Own_Funds'],
            'Eligible_Own_Funds_SCR': of_row['R0130_Eligible_Own_Funds_SCR'],
            'Eligible_Own_Funds_MCR': of_row['R0140_Eligible_Own_Funds_MCR'],
            'SCR': scr_row['SCR'],
            'MCR': mcr_row['MCR'],
            'SCR_Ratio': scr_ratio,
            'MCR_Ratio': mcr_ratio,
            'Surplus_SCR': of_row['R0130_Eligible_Own_Funds_SCR'] - scr_row['SCR'],
            'Surplus_MCR': of_row['R0140_Eligible_Own_Funds_MCR'] - mcr_row['MCR']
        })

    return pd.DataFrame(data)


# =============================================================================
# GENERATE ALL TABLES FOR POWER BI
# =============================================================================
print("Generating Solvency II QSR Data for Power BI...")
print("=" * 60)

# Generate all QSR tables (these will be available in Power BI)
# Control Forms
QSR030_Basic_Information = generate_qsr030_basic_information()
QSR031_Content_Of_Submission = generate_qsr031_content_of_submission()

# Balance Sheet and Reconciliation
QSR002_Balance_Sheet = generate_qsr002_balance_sheet()
QSR210_Reconciliation = generate_qsr210_reconciliation()

# Own Funds and Capital
QSR220_Own_Funds = generate_qsr220_own_funds()
QSR240_Technical_Provisions = generate_qsr240_technical_provisions()
QSR440_Premiums_Claims = generate_qsr440_premiums_claims()

# Risk Modules
QSR291_Operational_Risk = generate_qsr291_operational_risk()
QSR292_Market_Risk = generate_qsr292_market_risk()
QSR293_Counterparty_Risk = generate_qsr293_counterparty_risk()
QSR510_MCR = generate_qsr510_mcr()

# Cash Transfer (Q4)
QSR923_Cash_Transfer = generate_qsr923_cash_transfer()

# Summaries
SCR_Summary = generate_scr_summary()
Solvency_Ratio_Report = generate_solvency_ratio_report()

print(f"QSR030_Basic_Information: {len(QSR030_Basic_Information)} records")
print(f"QSR031_Content_Of_Submission: {len(QSR031_Content_Of_Submission)} records")
print(f"QSR002_Balance_Sheet: {len(QSR002_Balance_Sheet)} records")
print(f"QSR210_Reconciliation: {len(QSR210_Reconciliation)} records")
print(f"QSR220_Own_Funds: {len(QSR220_Own_Funds)} records")
print(f"QSR240_Technical_Provisions: {len(QSR240_Technical_Provisions)} records")
print(f"QSR440_Premiums_Claims: {len(QSR440_Premiums_Claims)} records")
print(f"QSR291_Operational_Risk: {len(QSR291_Operational_Risk)} records")
print(f"QSR292_Market_Risk: {len(QSR292_Market_Risk)} records")
print(f"QSR293_Counterparty_Risk: {len(QSR293_Counterparty_Risk)} records")
print(f"QSR510_MCR: {len(QSR510_MCR)} records")
print(f"QSR923_Cash_Transfer: {len(QSR923_Cash_Transfer)} records")
print(f"SCR_Summary: {len(SCR_Summary)} records")
print(f"Solvency_Ratio_Report: {len(Solvency_Ratio_Report)} records")
print("=" * 60)
print("Solvency II QSR data generated successfully!")
