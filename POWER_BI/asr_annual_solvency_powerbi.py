# Annual Solvency Return (ASR) - Power BI Data Generator
# Year-End Solvency II Balance Sheet, Own Funds, SCR, Technical Provisions
#
# ASR is the ANNUAL Solvency II return (distinct from ASB which has triangles)
# Provides: Regulatory solvency view at syndicate level
# Excludes: Detailed claims triangles (those live in ASB)
#
# Generates 12 tables covering:
# - Control and submission metadata
# - Solvency II balance sheet (assets, liabilities, own funds)
# - Technical provisions breakdown (premium provision, claims provision, risk margin)
# - SCR calculation summary
# - MCR calculation
# - Own funds by tier
# - Reconciliation reserves (GAAP to SII bridge)
# - Variation analysis year-on-year
#
# Submitted annually, typically March following year-end
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
REPORTING_YEAR = 2024
PRIOR_YEAR = 2023
CURRENCY = 'GBP'

# Solvency II Lines of Business (per EIOPA classification)
SII_LINES_OF_BUSINESS = [
    ('1', 'Medical expense insurance'),
    ('2', 'Income protection insurance'),
    ('3', 'Workers compensation insurance'),
    ('4', 'Motor vehicle liability insurance'),
    ('5', 'Other motor insurance'),
    ('6', 'Marine, aviation and transport insurance'),
    ('7', 'Fire and other damage to property insurance'),
    ('8', 'General liability insurance'),
    ('9', 'Credit and suretyship insurance'),
    ('10', 'Legal expenses insurance'),
    ('11', 'Assistance'),
    ('12', 'Miscellaneous financial loss'),
    ('13', 'Non-proportional health reinsurance'),
    ('14', 'Non-proportional casualty reinsurance'),
    ('15', 'Non-proportional marine, aviation and transport reinsurance'),
    ('16', 'Non-proportional property reinsurance')
]

# Asset categories for SII balance sheet
ASSET_CATEGORIES = [
    ('GOV_BONDS', 'Government bonds'),
    ('CORP_BONDS', 'Corporate bonds'),
    ('EQUITY', 'Equities'),
    ('COLLECTIVE', 'Collective investment undertakings'),
    ('PROPERTY', 'Property'),
    ('CASH', 'Cash and cash equivalents'),
    ('LOANS', 'Loans and mortgages'),
    ('RI_RECOV', 'Reinsurance recoverables'),
    ('RECEIVABLES', 'Insurance and intermediaries receivables'),
    ('OTHER', 'Other assets')
]

# =============================================================================
# ASR_001_Control - Submission metadata
# =============================================================================
def generate_asr_001_control():
    records = []
    for syn in SYNDICATES:
        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'ReportingDate': datetime(REPORTING_YEAR, 12, 31),
            'SubmissionDeadline': datetime(REPORTING_YEAR + 1, 4, 7),  # Typically early April
            'SubmissionDate': datetime(REPORTING_YEAR + 1, 4, 1) + timedelta(days=np.random.randint(0, 5)),
            'ManagingAgent': f'MA{syn % 100:03d}',
            'ReportType': 'ASR',
            'ReturnVersion': '2024.1',
            'Status': 'Final',
            'Audited': 'Yes',
            'AuditorName': np.random.choice(['Deloitte', 'PwC', 'EY', 'KPMG']),
            'SCRApproach': np.random.choice(['LIM', 'Standard Formula'], p=[0.7, 0.3]),
            'Currency': CURRENCY
        })
    return pd.DataFrame(records)

# =============================================================================
# ASR_010_Balance_Sheet - Solvency II balance sheet
# =============================================================================
def generate_asr_010_balance_sheet():
    records = []
    for syn in SYNDICATES:
        # Generate realistic balance sheet items
        total_assets = np.random.uniform(400, 1200)

        # Asset allocation
        investments = total_assets * np.random.uniform(0.55, 0.70)
        ri_recoverables = total_assets * np.random.uniform(0.12, 0.22)
        receivables = total_assets * np.random.uniform(0.08, 0.15)
        cash = total_assets * np.random.uniform(0.05, 0.12)
        other_assets = total_assets - investments - ri_recoverables - receivables - cash

        # Liabilities
        technical_provisions = total_assets * np.random.uniform(0.55, 0.75)
        other_liabilities = total_assets * np.random.uniform(0.05, 0.12)
        total_liabilities = technical_provisions + other_liabilities

        # Own Funds (excess of assets over liabilities)
        excess_assets = total_assets - total_liabilities

        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'ReportingDate': datetime(REPORTING_YEAR, 12, 31),
            # Assets
            'Total_Assets_GBP_M': round(total_assets, 2),
            'Investments_GBP_M': round(investments, 2),
            'RI_Recoverables_GBP_M': round(ri_recoverables, 2),
            'Receivables_GBP_M': round(receivables, 2),
            'Cash_GBP_M': round(cash, 2),
            'Other_Assets_GBP_M': round(other_assets, 2),
            # Liabilities
            'Total_Liabilities_GBP_M': round(total_liabilities, 2),
            'Technical_Provisions_GBP_M': round(technical_provisions, 2),
            'Other_Liabilities_GBP_M': round(other_liabilities, 2),
            # Own Funds
            'Excess_Assets_Over_Liabilities_GBP_M': round(excess_assets, 2),
            'Currency': CURRENCY
        })
    return pd.DataFrame(records)

# =============================================================================
# ASR_020_Assets_Detail - Detailed asset breakdown
# =============================================================================
def generate_asr_020_assets_detail():
    records = []
    for syn in SYNDICATES:
        total_investments = np.random.uniform(250, 800)

        # Asset allocation weights
        weights = {
            'GOV_BONDS': np.random.uniform(0.30, 0.45),
            'CORP_BONDS': np.random.uniform(0.25, 0.35),
            'EQUITY': np.random.uniform(0.03, 0.08),
            'COLLECTIVE': np.random.uniform(0.02, 0.06),
            'PROPERTY': np.random.uniform(0.01, 0.04),
            'CASH': np.random.uniform(0.08, 0.15),
            'LOANS': np.random.uniform(0.01, 0.03),
            'RI_RECOV': np.random.uniform(0.12, 0.22),
            'RECEIVABLES': np.random.uniform(0.08, 0.15),
            'OTHER': np.random.uniform(0.02, 0.05)
        }

        # Normalize weights
        total_weight = sum(weights.values())
        weights = {k: v/total_weight for k, v in weights.items()}

        total_assets = total_investments / 0.6  # Investments are ~60% of total

        for asset_code, asset_name in ASSET_CATEGORIES:
            weight = weights[asset_code]
            sii_value = total_assets * weight

            # GAAP value may differ from SII value
            gaap_sii_diff = np.random.uniform(-0.05, 0.05)
            gaap_value = sii_value * (1 + gaap_sii_diff)

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'ReportingDate': datetime(REPORTING_YEAR, 12, 31),
                'Asset_Code': asset_code,
                'Asset_Name': asset_name,
                'SII_Value_GBP_M': round(sii_value, 2),
                'GAAP_Value_GBP_M': round(gaap_value, 2),
                'Valuation_Diff_GBP_M': round(sii_value - gaap_value, 2),
                'Allocation_Pct': round(weight * 100, 2),
                'Currency': CURRENCY
            })
    return pd.DataFrame(records)

# =============================================================================
# ASR_030_Technical_Provisions - TP breakdown by LOB
# =============================================================================
def generate_asr_030_technical_provisions():
    records = []
    for syn in SYNDICATES:
        total_tp = np.random.uniform(250, 750)

        # Generate weights for each LOB
        lob_weights = np.random.dirichlet(np.ones(len(SII_LINES_OF_BUSINESS)) * 0.5)

        for i, (lob_code, lob_name) in enumerate(SII_LINES_OF_BUSINESS):
            weight = lob_weights[i]

            # Skip if very small allocation
            if weight < 0.01:
                continue

            lob_tp = total_tp * weight

            # Best Estimate breakdown
            claims_be = lob_tp * np.random.uniform(0.70, 0.85)
            premium_be = lob_tp * np.random.uniform(0.05, 0.15)
            total_be = claims_be + premium_be

            # Risk Margin (typically 5-15% of BE for non-life)
            risk_margin = total_be * np.random.uniform(0.05, 0.12)

            # Recoverables from reinsurance
            ri_recov_claims = claims_be * np.random.uniform(0.15, 0.35)
            ri_recov_premium = premium_be * np.random.uniform(0.10, 0.25)
            total_ri_recov = ri_recov_claims + ri_recov_premium

            # Net TP
            net_tp = total_be + risk_margin - total_ri_recov

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'ReportingDate': datetime(REPORTING_YEAR, 12, 31),
                'LOB_Code': lob_code,
                'LOB_Name': lob_name,
                # Gross Best Estimate
                'Claims_BE_Gross_GBP_M': round(claims_be, 2),
                'Premium_BE_Gross_GBP_M': round(premium_be, 2),
                'Total_BE_Gross_GBP_M': round(total_be, 2),
                # Risk Margin
                'Risk_Margin_GBP_M': round(risk_margin, 2),
                # RI Recoverables
                'RI_Recov_Claims_GBP_M': round(ri_recov_claims, 2),
                'RI_Recov_Premium_GBP_M': round(ri_recov_premium, 2),
                'Total_RI_Recov_GBP_M': round(total_ri_recov, 2),
                # Net
                'Net_TP_GBP_M': round(net_tp, 2),
                'Gross_TP_GBP_M': round(total_be + risk_margin, 2),
                'Currency': CURRENCY
            })
    return pd.DataFrame(records)

# =============================================================================
# ASR_040_SCR_Summary - SCR calculation summary
# =============================================================================
def generate_asr_040_scr_summary():
    records = []
    for syn in SYNDICATES:
        # Base SCR components
        underwriting_risk = np.random.uniform(50, 150)
        market_risk = np.random.uniform(20, 80)
        counterparty_risk = np.random.uniform(10, 40)

        # Underwriting risk breakdown
        premium_reserve = underwriting_risk * np.random.uniform(0.45, 0.55)
        cat_risk = underwriting_risk * np.random.uniform(0.35, 0.45)
        lapse_risk = underwriting_risk * np.random.uniform(0.05, 0.15)

        # BSCR (pre-diversification)
        bscr_pre_div = underwriting_risk + market_risk + counterparty_risk

        # Diversification benefit (20-35%)
        div_benefit_pct = np.random.uniform(0.20, 0.35)
        div_benefit = bscr_pre_div * div_benefit_pct
        bscr = bscr_pre_div - div_benefit

        # Operational risk
        op_risk = bscr * np.random.uniform(0.05, 0.12)

        # LAC DT (Loss-absorbing capacity of deferred taxes)
        lac_dt = (bscr + op_risk) * np.random.uniform(0.02, 0.08)

        # Final SCR
        scr = bscr + op_risk - lac_dt

        # MCR
        mcr = scr * np.random.uniform(0.25, 0.35)

        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'ReportingDate': datetime(REPORTING_YEAR, 12, 31),
            # Risk modules
            'Underwriting_Risk_GBP_M': round(underwriting_risk, 2),
            'Premium_Reserve_Risk_GBP_M': round(premium_reserve, 2),
            'Cat_Risk_GBP_M': round(cat_risk, 2),
            'Lapse_Risk_GBP_M': round(lapse_risk, 2),
            'Market_Risk_GBP_M': round(market_risk, 2),
            'Counterparty_Risk_GBP_M': round(counterparty_risk, 2),
            # Aggregation
            'BSCR_PreDiv_GBP_M': round(bscr_pre_div, 2),
            'Diversification_Benefit_GBP_M': round(div_benefit, 2),
            'Diversification_Pct': round(div_benefit_pct * 100, 1),
            'BSCR_GBP_M': round(bscr, 2),
            'Operational_Risk_GBP_M': round(op_risk, 2),
            'LAC_DT_GBP_M': round(lac_dt, 2),
            # Final
            'SCR_GBP_M': round(scr, 2),
            'MCR_GBP_M': round(mcr, 2),
            'SCR_Approach': np.random.choice(['LIM', 'Standard Formula'], p=[0.7, 0.3]),
            'Currency': CURRENCY
        })
    return pd.DataFrame(records)

# =============================================================================
# ASR_050_Own_Funds - Own funds by tier
# =============================================================================
def generate_asr_050_own_funds():
    records = []
    for syn in SYNDICATES:
        scr = np.random.uniform(80, 250)
        coverage_target = np.random.uniform(1.30, 1.90)

        total_own_funds = scr * coverage_target

        # Tier composition
        tier1_unrestricted = total_own_funds * np.random.uniform(0.85, 0.95)
        tier1_restricted = total_own_funds * np.random.uniform(0, 0.05)
        tier2 = total_own_funds * np.random.uniform(0.02, 0.10)
        tier3 = 0  # Typically not used at Lloyd's

        # Recalculate total
        total_own_funds = tier1_unrestricted + tier1_restricted + tier2 + tier3

        # Eligible amounts (subject to tiering limits)
        eligible_scr = tier1_unrestricted + tier1_restricted + min(tier2, scr * 0.50)
        mcr = scr * np.random.uniform(0.25, 0.35)
        eligible_mcr = tier1_unrestricted + min(tier1_restricted, mcr * 0.20)

        # FAL (Funds at Lloyd's)
        fal = tier1_unrestricted * np.random.uniform(0.85, 0.95)

        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'ReportingDate': datetime(REPORTING_YEAR, 12, 31),
            # Tier breakdown
            'Tier1_Unrestricted_GBP_M': round(tier1_unrestricted, 2),
            'Tier1_Restricted_GBP_M': round(tier1_restricted, 2),
            'Tier2_GBP_M': round(tier2, 2),
            'Tier3_GBP_M': round(tier3, 2),
            'Total_Own_Funds_GBP_M': round(total_own_funds, 2),
            # Eligible amounts
            'Eligible_SCR_GBP_M': round(eligible_scr, 2),
            'Eligible_MCR_GBP_M': round(eligible_mcr, 2),
            # Capital requirements
            'SCR_GBP_M': round(scr, 2),
            'MCR_GBP_M': round(mcr, 2),
            # Coverage ratios
            'SCR_Coverage_Ratio': round(eligible_scr / scr, 3),
            'SCR_Coverage_Pct': round((eligible_scr / scr) * 100, 1),
            'MCR_Coverage_Ratio': round(eligible_mcr / mcr, 3),
            'MCR_Coverage_Pct': round((eligible_mcr / mcr) * 100, 1),
            # Lloyd's specific
            'FAL_GBP_M': round(fal, 2),
            'Surplus_Over_SCR_GBP_M': round(eligible_scr - scr, 2),
            'Currency': CURRENCY
        })
    return pd.DataFrame(records)

# =============================================================================
# ASR_060_Reconciliation_Reserves - GAAP to SII bridge
# =============================================================================
def generate_asr_060_reconciliation_reserves():
    records = []
    for syn in SYNDICATES:
        # GAAP reserves (starting point)
        gaap_reserves = np.random.uniform(200, 600)

        # Adjustments to get to SII
        remove_margin = gaap_reserves * np.random.uniform(0.03, 0.08)  # Remove prudence margins
        add_enids = gaap_reserves * np.random.uniform(0.01, 0.04)  # Add ENIDs (Events Not In Data)
        discounting = gaap_reserves * np.random.uniform(0.02, 0.06)  # Discounting effect
        ulae_adjustment = gaap_reserves * np.random.uniform(0.01, 0.03)  # ULAE/expense adjustment

        # Best Estimate (SII)
        sii_best_estimate = gaap_reserves - remove_margin + add_enids - discounting + ulae_adjustment

        # Risk Margin
        risk_margin = sii_best_estimate * np.random.uniform(0.06, 0.12)

        # Total SII Technical Provisions
        sii_tp = sii_best_estimate + risk_margin

        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'ReportingDate': datetime(REPORTING_YEAR, 12, 31),
            # Starting point
            'GAAP_Reserves_GBP_M': round(gaap_reserves, 2),
            # Adjustments
            'Remove_Prudence_Margin_GBP_M': round(-remove_margin, 2),
            'Add_ENIDs_GBP_M': round(add_enids, 2),
            'Discounting_Effect_GBP_M': round(-discounting, 2),
            'ULAE_Adjustment_GBP_M': round(ulae_adjustment, 2),
            'Other_Adjustments_GBP_M': round(np.random.uniform(-5, 5), 2),
            # SII values
            'SII_Best_Estimate_GBP_M': round(sii_best_estimate, 2),
            'SII_Risk_Margin_GBP_M': round(risk_margin, 2),
            'SII_Technical_Provisions_GBP_M': round(sii_tp, 2),
            # Summary
            'Total_Adjustment_GBP_M': round(sii_tp - gaap_reserves, 2),
            'Adjustment_Pct': round(((sii_tp / gaap_reserves) - 1) * 100, 2),
            'Currency': CURRENCY
        })
    return pd.DataFrame(records)

# =============================================================================
# ASR_070_Variation_Analysis - Year-on-year movement
# =============================================================================
def generate_asr_070_variation_analysis():
    records = []
    metrics = [
        ('Total_Assets', 'Total Assets'),
        ('Total_Liabilities', 'Total Liabilities'),
        ('Technical_Provisions', 'Technical Provisions'),
        ('Own_Funds', 'Own Funds'),
        ('SCR', 'Solvency Capital Requirement'),
        ('MCR', 'Minimum Capital Requirement'),
        ('Coverage_Ratio', 'SCR Coverage Ratio')
    ]

    for syn in SYNDICATES:
        for metric_code, metric_name in metrics:
            # Prior year value
            if metric_code == 'Coverage_Ratio':
                py_value = np.random.uniform(1.30, 1.80)
                cy_value = py_value * np.random.uniform(0.95, 1.10)
            else:
                py_value = np.random.uniform(100, 500)
                cy_value = py_value * np.random.uniform(0.90, 1.15)

            change = cy_value - py_value
            change_pct = ((cy_value / py_value) - 1) * 100 if py_value != 0 else 0

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Metric_Code': metric_code,
                'Metric_Name': metric_name,
                'Prior_Year_Value': round(py_value, 2),
                'Current_Year_Value': round(cy_value, 2),
                'Change_Absolute': round(change, 2),
                'Change_Pct': round(change_pct, 1),
                'Unit': 'Ratio' if metric_code == 'Coverage_Ratio' else 'GBP_M',
                'Currency': CURRENCY
            })
    return pd.DataFrame(records)

# =============================================================================
# ASR_080_Risk_Margin_Calculation - Risk margin methodology
# =============================================================================
def generate_asr_080_risk_margin():
    records = []
    for syn in SYNDICATES:
        # SCR projection over run-off
        year_0_scr = np.random.uniform(80, 200)
        coc_rate = 0.06  # 6% Cost of Capital rate

        # Project SCR run-off (typically declines over time)
        scr_projections = []
        cumulative_rm = 0

        for year in range(1, 11):  # 10-year projection
            decay_factor = np.exp(-0.3 * year)  # Exponential decay
            projected_scr = year_0_scr * decay_factor * np.random.uniform(0.9, 1.1)
            rm_contribution = projected_scr * coc_rate / (1.02 ** year)  # Discounted
            cumulative_rm += rm_contribution

            scr_projections.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Projection_Year': year,
                'Projected_SCR_GBP_M': round(projected_scr, 2),
                'CoC_Rate_Pct': coc_rate * 100,
                'Discount_Factor': round(1 / (1.02 ** year), 4),
                'RM_Contribution_GBP_M': round(rm_contribution, 2),
                'Cumulative_RM_GBP_M': round(cumulative_rm, 2),
                'Currency': CURRENCY
            })

        records.extend(scr_projections)
    return pd.DataFrame(records)

# =============================================================================
# ASR_090_QRT_S02 - S.02.01 Balance Sheet QRT format
# =============================================================================
def generate_asr_090_qrt_s02():
    """Generate S.02.01 Balance Sheet in QRT format"""
    records = []

    # QRT line items for S.02.01
    qrt_items = [
        ('R0030', 'Intangible assets'),
        ('R0040', 'Deferred tax assets'),
        ('R0050', 'Pension benefit surplus'),
        ('R0060', 'Property, plant & equipment held for own use'),
        ('R0070', 'Investments (other than index-linked)'),
        ('R0220', 'Assets held for index-linked and unit-linked contracts'),
        ('R0230', 'Loans and mortgages'),
        ('R0270', 'Reinsurance recoverables'),
        ('R0330', 'Deposits to cedants'),
        ('R0340', 'Insurance and intermediaries receivables'),
        ('R0350', 'Reinsurance receivables'),
        ('R0360', 'Receivables (trade, not insurance)'),
        ('R0370', 'Own shares'),
        ('R0380', 'Amounts due in respect of own fund items'),
        ('R0390', 'Cash and cash equivalents'),
        ('R0400', 'Any other assets, not elsewhere shown'),
        ('R0500', 'Total assets'),
        ('R0510', 'Technical provisions - non-life'),
        ('R0600', 'Technical provisions - life'),
        ('R0690', 'Other liabilities'),
        ('R0900', 'Total liabilities'),
        ('R1000', 'Excess of assets over liabilities')
    ]

    for syn in SYNDICATES:
        total_assets = np.random.uniform(400, 1200)

        for row_code, row_name in qrt_items:
            if row_code == 'R0500':
                value = total_assets
            elif row_code == 'R0900':
                value = total_assets * np.random.uniform(0.60, 0.80)
            elif row_code == 'R1000':
                liab = total_assets * np.random.uniform(0.60, 0.80)
                value = total_assets - liab
            elif 'R05' in row_code or 'R06' in row_code or 'R09' in row_code:
                value = total_assets * np.random.uniform(0.30, 0.50)
            else:
                value = total_assets * np.random.uniform(0.01, 0.15)

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'ReportingDate': datetime(REPORTING_YEAR, 12, 31),
                'QRT_Template': 'S.02.01',
                'Row_Code': row_code,
                'Row_Name': row_name,
                'Value_GBP_M': round(value, 2),
                'Currency': CURRENCY
            })
    return pd.DataFrame(records)

# =============================================================================
# ASR_100_QRT_S05 - S.05.01 Premiums, claims and expenses QRT
# =============================================================================
def generate_asr_100_qrt_s05():
    """Generate S.05.01 Premiums, claims and expenses QRT"""
    records = []

    for syn in SYNDICATES:
        total_gwp = np.random.uniform(200, 600)
        lob_weights = np.random.dirichlet(np.ones(len(SII_LINES_OF_BUSINESS)) * 0.5)

        for i, (lob_code, lob_name) in enumerate(SII_LINES_OF_BUSINESS):
            weight = lob_weights[i]
            if weight < 0.01:
                continue

            gwp = total_gwp * weight
            gep = gwp * np.random.uniform(0.90, 1.05)
            gcr = gep * np.random.uniform(0.50, 0.75)
            expenses = gep * np.random.uniform(0.25, 0.38)

            # Net figures
            ri_ceded_pct = np.random.uniform(0.10, 0.30)
            nwp = gwp * (1 - ri_ceded_pct)
            nep = gep * (1 - ri_ceded_pct)
            ncr = gcr * (1 - ri_ceded_pct * 0.8)

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'ReportingDate': datetime(REPORTING_YEAR, 12, 31),
                'QRT_Template': 'S.05.01',
                'LOB_Code': lob_code,
                'LOB_Name': lob_name,
                'GWP_GBP_M': round(gwp, 2),
                'GEP_GBP_M': round(gep, 2),
                'Gross_Claims_GBP_M': round(gcr, 2),
                'Expenses_GBP_M': round(expenses, 2),
                'RI_Ceded_GBP_M': round(gwp * ri_ceded_pct, 2),
                'NWP_GBP_M': round(nwp, 2),
                'NEP_GBP_M': round(nep, 2),
                'Net_Claims_GBP_M': round(ncr, 2),
                'Underwriting_Result_GBP_M': round(nep - ncr - expenses, 2),
                'Currency': CURRENCY
            })
    return pd.DataFrame(records)

# =============================================================================
# ASR_110_QRT_S23 - S.23.01 Own Funds QRT
# =============================================================================
def generate_asr_110_qrt_s23():
    """Generate S.23.01 Own Funds QRT format"""
    records = []

    for syn in SYNDICATES:
        scr = np.random.uniform(80, 250)
        coverage = np.random.uniform(1.30, 1.90)
        total_eof = scr * coverage

        # Component breakdown
        components = [
            ('R0010', 'Ordinary share capital', total_eof * 0.60),
            ('R0030', 'Share premium account', total_eof * 0.15),
            ('R0040', 'Initial funds, members contributions', total_eof * 0.10),
            ('R0050', 'Subordinated mutual member accounts', total_eof * 0.02),
            ('R0070', 'Surplus funds', total_eof * 0.05),
            ('R0090', 'Preference shares', 0),
            ('R0110', 'Subordinated liabilities - Tier 1', total_eof * 0.03),
            ('R0130', 'Subordinated liabilities - Tier 2', total_eof * 0.05),
            ('R0140', 'Reconciliation reserve', total_eof * 0.02),
            ('R0220', 'Total Tier 1 unrestricted', total_eof * 0.90),
            ('R0230', 'Total Tier 1 restricted', total_eof * 0.02),
            ('R0240', 'Total Tier 2', total_eof * 0.05),
            ('R0250', 'Total Tier 3', 0),
            ('R0290', 'Total eligible own funds to meet SCR', total_eof * 0.97),
            ('R0300', 'Total eligible own funds to meet MCR', total_eof * 0.92),
            ('R0310', 'SCR', scr),
            ('R0320', 'MCR', scr * 0.30),
            ('R0330', 'Ratio EOF to SCR', coverage),
            ('R0340', 'Ratio EOF to MCR', coverage * 3.2)
        ]

        for row_code, row_name, value in components:
            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'ReportingDate': datetime(REPORTING_YEAR, 12, 31),
                'QRT_Template': 'S.23.01',
                'Row_Code': row_code,
                'Row_Name': row_name,
                'Value': round(value, 2),
                'Unit': 'Ratio' if 'Ratio' in row_name else 'GBP_M',
                'Currency': CURRENCY
            })
    return pd.DataFrame(records)

# =============================================================================
# Generate all tables
# =============================================================================

# Control and metadata
ASR_001_Control = generate_asr_001_control()

# Balance sheet and assets
ASR_010_Balance_Sheet = generate_asr_010_balance_sheet()
ASR_020_Assets_Detail = generate_asr_020_assets_detail()

# Technical provisions
ASR_030_Technical_Provisions = generate_asr_030_technical_provisions()

# Capital
ASR_040_SCR_Summary = generate_asr_040_scr_summary()
ASR_050_Own_Funds = generate_asr_050_own_funds()

# Reconciliation and analysis
ASR_060_Reconciliation = generate_asr_060_reconciliation_reserves()
ASR_070_Variation = generate_asr_070_variation_analysis()
ASR_080_Risk_Margin = generate_asr_080_risk_margin()

# QRT templates
ASR_090_QRT_S02 = generate_asr_090_qrt_s02()
ASR_100_QRT_S05 = generate_asr_100_qrt_s05()
ASR_110_QRT_S23 = generate_asr_110_qrt_s23()

# Summary statistics
print("=" * 70)
print("ASR - Annual Solvency Return Data Generator")
print("=" * 70)
print(f"ASR_001_Control: {len(ASR_001_Control)} rows")
print(f"ASR_010_Balance_Sheet: {len(ASR_010_Balance_Sheet)} rows")
print(f"ASR_020_Assets_Detail: {len(ASR_020_Assets_Detail)} rows")
print(f"ASR_030_Technical_Provisions: {len(ASR_030_Technical_Provisions)} rows")
print(f"ASR_040_SCR_Summary: {len(ASR_040_SCR_Summary)} rows")
print(f"ASR_050_Own_Funds: {len(ASR_050_Own_Funds)} rows")
print(f"ASR_060_Reconciliation: {len(ASR_060_Reconciliation)} rows")
print(f"ASR_070_Variation: {len(ASR_070_Variation)} rows")
print(f"ASR_080_Risk_Margin: {len(ASR_080_Risk_Margin)} rows")
print(f"ASR_090_QRT_S02: {len(ASR_090_QRT_S02)} rows")
print(f"ASR_100_QRT_S05: {len(ASR_100_QRT_S05)} rows")
print(f"ASR_110_QRT_S23: {len(ASR_110_QRT_S23)} rows")
print("=" * 70)
print("ASR data generated successfully!")
