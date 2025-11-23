# Lloyd's Capital Return (LCR) - Power BI Data Generator
# THE MOST IMPORTANT Lloyd's Return - Annual Capital Setting
#
# Generates 14 tables covering all SCR risk modules:
# - Premium risk, reserve risk, catastrophe risk by peril
# - Market risk, credit risk, operational risk
# - Technical provisions with risk margin (4% to 6% CoC conversion)
# - Own funds analysis and capital coverage ratios
# - Year of Account capital allocation
# - SCR diversification matrices
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
YEARS_OF_ACCOUNT = list(range(2018, 2026))

# Lloyd's Lines of Business (simplified)
LINES_OF_BUSINESS = [
    ('PR', 'Property Direct'),
    ('CA', 'Casualty Direct'),
    ('MA', 'Marine Direct'),
    ('AV', 'Aviation Direct'),
    ('EN', 'Energy Direct'),
    ('MO', 'Motor Direct'),
    ('PA', 'Accident & Health'),
    ('CR', 'Credit & Surety'),
    ('PR_RI', 'Property Reinsurance'),
    ('CA_RI', 'Casualty Reinsurance'),
    ('MA_RI', 'Marine Reinsurance'),
    ('SP', 'Specialty')
]

# Catastrophe Perils
CAT_PERILS = [
    ('NA_HU', 'North Atlantic Hurricane', 0.35),
    ('EU_WS', 'European Windstorm', 0.15),
    ('US_EQ', 'US Earthquake', 0.12),
    ('JP_EQ', 'Japan Earthquake', 0.08),
    ('JP_TY', 'Japan Typhoon', 0.05),
    ('AU_EQ', 'Australian Earthquake', 0.03),
    ('FL', 'Flood', 0.08),
    ('TR', 'Terrorism', 0.05),
    ('CY', 'Cyber', 0.06),
    ('PAN', 'Pandemic', 0.03)
]

# Market Risk Categories
MARKET_RISK_TYPES = [
    ('IR', 'Interest Rate Risk'),
    ('EQ', 'Equity Risk'),
    ('PROP', 'Property Risk'),
    ('SPR', 'Spread Risk'),
    ('FX', 'Currency Risk'),
    ('CONC', 'Concentration Risk')
]

# =============================================================================
# LCR_001_Control - Submission metadata and control
# =============================================================================
def generate_lcr_001_control():
    records = []
    for syn in SYNDICATES:
        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'SubmissionDate': datetime(REPORTING_YEAR, 9, 30),
            'SubmissionType': 'Annual',
            'ModelType': np.random.choice(['LIM', 'Standard Formula'], p=[0.7, 0.3]),
            'ManagingAgent': f'MA{syn % 100:03d}',
            'ActiveMember': 'Y',
            'StampCapacity_GBP_M': round(np.random.uniform(200, 800), 1),
            'CapitalProvider': np.random.choice(['Corporate', 'Names', 'Mixed'], p=[0.6, 0.1, 0.3]),
            'ReportStatus': 'Final',
            'ApprovalDate': datetime(REPORTING_YEAR, 10, 15),
            'ApprovedBy': f'CFO_{syn}'
        })
    return pd.DataFrame(records)

# =============================================================================
# LCR_010_SCR_Summary - Overall SCR calculation
# =============================================================================
def generate_lcr_010_scr_summary():
    records = []
    for syn in SYNDICATES:
        # Base SCR components (GBP millions)
        premium_risk = np.random.uniform(30, 80)
        reserve_risk = np.random.uniform(40, 100)
        cat_risk = np.random.uniform(50, 150)
        market_risk = np.random.uniform(20, 60)
        credit_risk = np.random.uniform(10, 40)
        operational_risk = np.random.uniform(5, 25)

        # Pre-diversification SCR
        pre_div_scr = premium_risk + reserve_risk + cat_risk + market_risk + credit_risk + operational_risk

        # Diversification benefit (typically 20-35%)
        div_benefit_pct = np.random.uniform(0.20, 0.35)
        div_benefit = pre_div_scr * div_benefit_pct

        # Post-diversification SCR
        post_div_scr = pre_div_scr - div_benefit

        # Loss absorbing capacity of deferred taxes
        lac_dt = post_div_scr * np.random.uniform(0.02, 0.08)

        # Final SCR
        final_scr = post_div_scr - lac_dt

        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'PremiumRisk_GBP_M': round(premium_risk, 2),
            'ReserveRisk_GBP_M': round(reserve_risk, 2),
            'CatRisk_GBP_M': round(cat_risk, 2),
            'MarketRisk_GBP_M': round(market_risk, 2),
            'CreditRisk_GBP_M': round(credit_risk, 2),
            'OperationalRisk_GBP_M': round(operational_risk, 2),
            'PreDiversification_SCR_GBP_M': round(pre_div_scr, 2),
            'DiversificationBenefit_GBP_M': round(div_benefit, 2),
            'DiversificationBenefit_Pct': round(div_benefit_pct * 100, 1),
            'PostDiversification_SCR_GBP_M': round(post_div_scr, 2),
            'LAC_DT_GBP_M': round(lac_dt, 2),
            'Final_SCR_GBP_M': round(final_scr, 2),
            'MCR_GBP_M': round(final_scr * np.random.uniform(0.25, 0.35), 2),
            'Currency': 'GBP'
        })
    return pd.DataFrame(records)

# =============================================================================
# LCR_020_Premium_Risk - Premium risk by line of business
# =============================================================================
def generate_lcr_020_premium_risk():
    records = []
    for syn in SYNDICATES:
        total_premium_risk = np.random.uniform(30, 80)
        weights = np.random.dirichlet(np.ones(len(LINES_OF_BUSINESS)))

        for i, (lob_code, lob_name) in enumerate(LINES_OF_BUSINESS):
            net_premium = np.random.uniform(20, 150)
            volume_measure = net_premium * np.random.uniform(0.8, 1.2)
            sigma = np.random.uniform(0.05, 0.15)  # Standard deviation factor
            risk_charge = total_premium_risk * weights[i]

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'LOB_Code': lob_code,
                'LOB_Name': lob_name,
                'NetEarnedPremium_GBP_M': round(net_premium, 2),
                'VolumeMeasure_GBP_M': round(volume_measure, 2),
                'Sigma_Factor': round(sigma, 4),
                'PremiumRiskCharge_GBP_M': round(risk_charge, 2),
                'GeographicDiv_Factor': round(np.random.uniform(0.85, 0.98), 3),
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# LCR_030_Reserve_Risk - Reserve risk calculations
# =============================================================================
def generate_lcr_030_reserve_risk():
    records = []
    for syn in SYNDICATES:
        total_reserve_risk = np.random.uniform(40, 100)
        weights = np.random.dirichlet(np.ones(len(LINES_OF_BUSINESS)))

        for i, (lob_code, lob_name) in enumerate(LINES_OF_BUSINESS):
            best_estimate = np.random.uniform(30, 200)
            volume_measure = best_estimate * np.random.uniform(0.9, 1.1)
            sigma = np.random.uniform(0.08, 0.20)  # Reserve risk typically higher
            risk_charge = total_reserve_risk * weights[i]

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'LOB_Code': lob_code,
                'LOB_Name': lob_name,
                'BestEstimate_Reserves_GBP_M': round(best_estimate, 2),
                'VolumeMeasure_GBP_M': round(volume_measure, 2),
                'Sigma_Factor': round(sigma, 4),
                'ReserveRiskCharge_GBP_M': round(risk_charge, 2),
                'RunOff_Pattern_Years': np.random.choice([3, 5, 7, 10, 15]),
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# LCR_040_Cat_Risk_Summary - Catastrophe risk summary
# =============================================================================
def generate_lcr_040_cat_risk_summary():
    records = []
    for syn in SYNDICATES:
        total_cat_risk = np.random.uniform(50, 150)

        # Aggregate cat risk
        agg_cat_gross = total_cat_risk * np.random.uniform(1.5, 2.5)
        agg_cat_net = total_cat_risk  # After RI

        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'GrossCatRisk_GBP_M': round(agg_cat_gross, 2),
            'ReinsuranceBenefit_GBP_M': round(agg_cat_gross - agg_cat_net, 2),
            'NetCatRisk_GBP_M': round(agg_cat_net, 2),
            'CatModelUsed': np.random.choice(['RMS', 'AIR', 'Lloyd\'s RDS', 'Hybrid']),
            'SimulationCount': np.random.choice([10000, 50000, 100000]),
            'Return_Period_1_in_200': round(agg_cat_net * np.random.uniform(0.9, 1.1), 2),
            'Return_Period_1_in_100': round(agg_cat_net * np.random.uniform(0.6, 0.8), 2),
            'Return_Period_1_in_50': round(agg_cat_net * np.random.uniform(0.4, 0.6), 2),
            'OEP_99_5_Pct_GBP_M': round(agg_cat_net, 2),
            'AEP_99_5_Pct_GBP_M': round(agg_cat_net * np.random.uniform(1.1, 1.3), 2),
            'Currency': 'GBP'
        })
    return pd.DataFrame(records)

# =============================================================================
# LCR_041_Cat_By_Peril - Catastrophe risk by peril
# =============================================================================
def generate_lcr_041_cat_by_peril():
    records = []
    for syn in SYNDICATES:
        total_cat_risk = np.random.uniform(50, 150)

        for peril_code, peril_name, base_weight in CAT_PERILS:
            weight = base_weight * np.random.uniform(0.7, 1.3)
            gross_exposure = total_cat_risk * weight * np.random.uniform(1.5, 2.5)
            ri_recovery = gross_exposure * np.random.uniform(0.3, 0.6)
            net_exposure = gross_exposure - ri_recovery

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'PerilCode': peril_code,
                'PerilName': peril_name,
                'GrossExposure_GBP_M': round(gross_exposure, 2),
                'RIRecovery_GBP_M': round(ri_recovery, 2),
                'NetExposure_GBP_M': round(net_exposure, 2),
                'RDS_Scenario_GBP_M': round(net_exposure * np.random.uniform(0.8, 1.2), 2),
                'AAL_GBP_M': round(net_exposure * np.random.uniform(0.05, 0.15), 2),
                'PML_200_GBP_M': round(net_exposure, 2),
                'PML_100_GBP_M': round(net_exposure * np.random.uniform(0.6, 0.8), 2),
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# LCR_050_Market_Risk - Market risk breakdown
# =============================================================================
def generate_lcr_050_market_risk():
    records = []
    for syn in SYNDICATES:
        total_market_risk = np.random.uniform(20, 60)
        weights = np.random.dirichlet(np.ones(len(MARKET_RISK_TYPES)))

        for i, (risk_code, risk_name) in enumerate(MARKET_RISK_TYPES):
            exposure = np.random.uniform(50, 300)
            risk_charge = total_market_risk * weights[i]
            shock_factor = np.random.uniform(0.05, 0.25)

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'RiskType_Code': risk_code,
                'RiskType_Name': risk_name,
                'Exposure_GBP_M': round(exposure, 2),
                'ShockFactor_Pct': round(shock_factor * 100, 1),
                'RiskCharge_GBP_M': round(risk_charge, 2),
                'Stressed_Value_GBP_M': round(exposure * (1 - shock_factor), 2),
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# LCR_060_Credit_Risk - Counterparty default risk
# =============================================================================
def generate_lcr_060_credit_risk():
    records = []
    counterparty_types = [
        ('REINS', 'Reinsurers', 0.45),
        ('BANK', 'Banks & Depositories', 0.25),
        ('BROKER', 'Brokers Receivables', 0.15),
        ('OTHER', 'Other Counterparties', 0.15)
    ]

    for syn in SYNDICATES:
        total_credit_risk = np.random.uniform(10, 40)

        for cp_code, cp_name, base_weight in counterparty_types:
            weight = base_weight * np.random.uniform(0.8, 1.2)
            exposure = np.random.uniform(20, 150)
            lgd = np.random.uniform(0.4, 0.6)  # Loss Given Default
            pd = np.random.uniform(0.001, 0.05)  # Probability of Default
            risk_charge = total_credit_risk * weight

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'CounterpartyType_Code': cp_code,
                'CounterpartyType_Name': cp_name,
                'Exposure_GBP_M': round(exposure, 2),
                'AvgCreditRating': np.random.choice(['AAA', 'AA', 'A', 'BBB', 'BB']),
                'LGD_Pct': round(lgd * 100, 1),
                'PD_Pct': round(pd * 100, 3),
                'RiskCharge_GBP_M': round(risk_charge, 2),
                'Collateral_GBP_M': round(exposure * np.random.uniform(0.1, 0.4), 2),
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# LCR_070_Operational_Risk - Operational risk calculation
# =============================================================================
def generate_lcr_070_operational_risk():
    records = []
    for syn in SYNDICATES:
        gross_premium = np.random.uniform(200, 600)
        technical_provisions = np.random.uniform(300, 800)

        # Standard Formula: max(premium-based, TP-based)
        premium_op_risk = gross_premium * 0.04  # 4% of premium
        tp_op_risk = technical_provisions * 0.0045  # 0.45% of TP
        basic_op_risk = max(premium_op_risk, tp_op_risk)

        # Cap at 30% of BSCR
        bscr = np.random.uniform(80, 200)
        capped_op_risk = min(basic_op_risk, bscr * 0.30)

        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'GrossEarnedPremium_GBP_M': round(gross_premium, 2),
            'TechnicalProvisions_GBP_M': round(technical_provisions, 2),
            'PremiumBasedCharge_GBP_M': round(premium_op_risk, 2),
            'TPBasedCharge_GBP_M': round(tp_op_risk, 2),
            'BasicOpRisk_GBP_M': round(basic_op_risk, 2),
            'BSCR_GBP_M': round(bscr, 2),
            'OpRiskCap_30Pct_BSCR': round(bscr * 0.30, 2),
            'FinalOpRisk_GBP_M': round(capped_op_risk, 2),
            'OpRiskAsPctBSCR': round((capped_op_risk / bscr) * 100, 1),
            'Currency': 'GBP'
        })
    return pd.DataFrame(records)

# =============================================================================
# LCR_080_Technical_Provisions - TP with risk margin
# =============================================================================
def generate_lcr_080_technical_provisions():
    records = []
    for syn in SYNDICATES:
        # Best Estimate components
        premium_provision = np.random.uniform(50, 200)
        claims_provision = np.random.uniform(200, 600)
        best_estimate = premium_provision + claims_provision

        # Risk Margin calculation
        # Solvency II uses 4% CoC, Lloyd's capital setting uses 6% CoC
        scr_projection = np.random.uniform(80, 200)
        duration = np.random.uniform(3, 7)  # Modified duration

        risk_margin_4pct = scr_projection * 0.04 * duration  # Solvency II
        risk_margin_6pct = scr_projection * 0.06 * duration  # Lloyd's

        total_tp_sii = best_estimate + risk_margin_4pct
        total_tp_lloyds = best_estimate + risk_margin_6pct

        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'PremiumProvision_GBP_M': round(premium_provision, 2),
            'ClaimsProvision_GBP_M': round(claims_provision, 2),
            'BestEstimate_Total_GBP_M': round(best_estimate, 2),
            'SCR_Projection_GBP_M': round(scr_projection, 2),
            'ModifiedDuration_Years': round(duration, 2),
            'RiskMargin_4Pct_CoC_GBP_M': round(risk_margin_4pct, 2),
            'RiskMargin_6Pct_CoC_GBP_M': round(risk_margin_6pct, 2),
            'TotalTP_SolvencyII_GBP_M': round(total_tp_sii, 2),
            'TotalTP_LloydsCapital_GBP_M': round(total_tp_lloyds, 2),
            'RiskMarginUplift_GBP_M': round(risk_margin_6pct - risk_margin_4pct, 2),
            'Currency': 'GBP'
        })
    return pd.DataFrame(records)

# =============================================================================
# LCR_090_Own_Funds - Own funds analysis
# =============================================================================
def generate_lcr_090_own_funds():
    records = []
    for syn in SYNDICATES:
        scr = np.random.uniform(80, 200)
        coverage_target = np.random.uniform(1.35, 1.80)  # 135-180% coverage

        # Tier 1 unrestricted (main capital)
        tier1_unrestricted = scr * coverage_target * np.random.uniform(0.85, 0.95)

        # Tier 1 restricted (hybrid capital)
        tier1_restricted = tier1_unrestricted * np.random.uniform(0, 0.10)

        # Tier 2 (subordinated debt, letters of credit)
        tier2 = tier1_unrestricted * np.random.uniform(0.05, 0.15)

        # Tier 3 (limited use)
        tier3 = 0  # Typically not used

        total_own_funds = tier1_unrestricted + tier1_restricted + tier2 + tier3

        # Eligible amounts (subject to tiering limits)
        eligible_scr = min(total_own_funds, tier1_unrestricted + tier1_restricted + min(tier2, scr * 0.5))
        eligible_mcr = min(total_own_funds, tier1_unrestricted + min(tier1_restricted, scr * 0.2))

        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'Tier1_Unrestricted_GBP_M': round(tier1_unrestricted, 2),
            'Tier1_Restricted_GBP_M': round(tier1_restricted, 2),
            'Tier2_GBP_M': round(tier2, 2),
            'Tier3_GBP_M': round(tier3, 2),
            'Total_OwnFunds_GBP_M': round(total_own_funds, 2),
            'Eligible_SCR_GBP_M': round(eligible_scr, 2),
            'Eligible_MCR_GBP_M': round(eligible_mcr, 2),
            'SCR_GBP_M': round(scr, 2),
            'MCR_GBP_M': round(scr * 0.30, 2),
            'FAL_GBP_M': round(tier1_unrestricted * 0.9, 2),  # Funds at Lloyd's
            'Currency': 'GBP'
        })
    return pd.DataFrame(records)

# =============================================================================
# LCR_100_Coverage_Ratios - Capital coverage ratios
# =============================================================================
def generate_lcr_100_coverage_ratios():
    records = []
    for syn in SYNDICATES:
        scr = np.random.uniform(80, 200)
        mcr = scr * np.random.uniform(0.25, 0.35)

        own_funds = scr * np.random.uniform(1.20, 2.00)
        eligible_scr = own_funds * np.random.uniform(0.95, 1.0)
        eligible_mcr = own_funds * np.random.uniform(0.90, 0.98)

        scr_coverage = eligible_scr / scr
        mcr_coverage = eligible_mcr / mcr

        # Lloyd's minimum and targets
        lloyds_minimum = 1.00
        lloyds_target = 1.35

        surplus_over_minimum = eligible_scr - scr
        surplus_over_target = eligible_scr - (scr * lloyds_target)

        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'SCR_GBP_M': round(scr, 2),
            'MCR_GBP_M': round(mcr, 2),
            'EligibleOwnFunds_SCR_GBP_M': round(eligible_scr, 2),
            'EligibleOwnFunds_MCR_GBP_M': round(eligible_mcr, 2),
            'SCR_Coverage_Ratio': round(scr_coverage, 3),
            'SCR_Coverage_Pct': round(scr_coverage * 100, 1),
            'MCR_Coverage_Ratio': round(mcr_coverage, 3),
            'MCR_Coverage_Pct': round(mcr_coverage * 100, 1),
            'Lloyds_Minimum_Coverage': lloyds_minimum,
            'Lloyds_Target_Coverage': lloyds_target,
            'Surplus_Over_Minimum_GBP_M': round(surplus_over_minimum, 2),
            'Surplus_Over_Target_GBP_M': round(surplus_over_target, 2),
            'Capital_Status': 'Adequate' if scr_coverage >= lloyds_minimum else 'Deficient',
            'Currency': 'GBP'
        })
    return pd.DataFrame(records)

# =============================================================================
# LCR_110_YOA_Capital - Year of Account capital allocation
# =============================================================================
def generate_lcr_110_yoa_capital():
    records = []
    for syn in SYNDICATES:
        total_scr = np.random.uniform(80, 200)

        for yoa in YEARS_OF_ACCOUNT:
            years_developed = REPORTING_YEAR - yoa

            # Open/Closed status
            if years_developed >= 3:
                status = 'Closed' if np.random.random() < 0.8 else 'Run-Off'
            else:
                status = 'Open'

            # Weight by development (newer years = more risk)
            if status == 'Open':
                weight = np.random.uniform(0.15, 0.40)
            elif status == 'Run-Off':
                weight = np.random.uniform(0.05, 0.15)
            else:
                weight = np.random.uniform(0.01, 0.05)

            yoa_scr = total_scr * weight
            yoa_own_funds = yoa_scr * np.random.uniform(1.20, 1.80)

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'YearOfAccount': yoa,
                'YOA_Status': status,
                'DevelopmentYear': years_developed,
                'GWP_GBP_M': round(np.random.uniform(50, 300) if status == 'Open' else 0, 2),
                'NEP_GBP_M': round(np.random.uniform(40, 250), 2),
                'TechnicalProvisions_GBP_M': round(np.random.uniform(30, 200), 2),
                'YOA_SCR_GBP_M': round(yoa_scr, 2),
                'YOA_OwnFunds_GBP_M': round(yoa_own_funds, 2),
                'YOA_Coverage_Ratio': round(yoa_own_funds / yoa_scr, 2) if yoa_scr > 0 else 0,
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# LCR_120_Diversification - Risk diversification matrix
# =============================================================================
def generate_lcr_120_diversification():
    records = []
    risk_modules = ['Premium', 'Reserve', 'Cat', 'Market', 'Credit', 'Operational']

    # Correlation matrix (typical values)
    base_correlations = {
        ('Premium', 'Reserve'): 0.50,
        ('Premium', 'Cat'): 0.25,
        ('Premium', 'Market'): 0.25,
        ('Premium', 'Credit'): 0.50,
        ('Premium', 'Operational'): 0.00,
        ('Reserve', 'Cat'): 0.25,
        ('Reserve', 'Market'): 0.25,
        ('Reserve', 'Credit'): 0.50,
        ('Reserve', 'Operational'): 0.00,
        ('Cat', 'Market'): 0.25,
        ('Cat', 'Credit'): 0.25,
        ('Cat', 'Operational'): 0.00,
        ('Market', 'Credit'): 0.25,
        ('Market', 'Operational'): 0.00,
        ('Credit', 'Operational'): 0.00
    }

    for syn in SYNDICATES:
        for i, risk1 in enumerate(risk_modules):
            for j, risk2 in enumerate(risk_modules):
                if i <= j:  # Upper triangle including diagonal
                    if risk1 == risk2:
                        correlation = 1.0
                    else:
                        key = (risk1, risk2) if (risk1, risk2) in base_correlations else (risk2, risk1)
                        correlation = base_correlations.get(key, 0.25)
                        # Add some random variation
                        correlation = correlation * np.random.uniform(0.9, 1.1)
                        correlation = min(max(correlation, 0), 1)

                    records.append({
                        'Syndicate': syn,
                        'ReportingYear': REPORTING_YEAR,
                        'RiskModule_1': risk1,
                        'RiskModule_2': risk2,
                        'Correlation': round(correlation, 3),
                        'CorrelationType': 'EIOPA_Standard' if np.random.random() < 0.7 else 'LIM_Calibrated'
                    })
    return pd.DataFrame(records)

# =============================================================================
# Generate all tables
# =============================================================================

# Control and metadata
LCR_001_Control = generate_lcr_001_control()

# SCR calculation
LCR_010_SCR_Summary = generate_lcr_010_scr_summary()

# Risk modules
LCR_020_Premium_Risk = generate_lcr_020_premium_risk()
LCR_030_Reserve_Risk = generate_lcr_030_reserve_risk()
LCR_040_Cat_Risk_Summary = generate_lcr_040_cat_risk_summary()
LCR_041_Cat_By_Peril = generate_lcr_041_cat_by_peril()
LCR_050_Market_Risk = generate_lcr_050_market_risk()
LCR_060_Credit_Risk = generate_lcr_060_credit_risk()
LCR_070_Operational_Risk = generate_lcr_070_operational_risk()

# Technical provisions and own funds
LCR_080_Technical_Provisions = generate_lcr_080_technical_provisions()
LCR_090_Own_Funds = generate_lcr_090_own_funds()

# Coverage and analysis
LCR_100_Coverage_Ratios = generate_lcr_100_coverage_ratios()
LCR_110_YOA_Capital = generate_lcr_110_yoa_capital()
LCR_120_Diversification = generate_lcr_120_diversification()

# Summary statistics
print(f"LCR_001_Control: {len(LCR_001_Control)} rows")
print(f"LCR_010_SCR_Summary: {len(LCR_010_SCR_Summary)} rows")
print(f"LCR_020_Premium_Risk: {len(LCR_020_Premium_Risk)} rows")
print(f"LCR_030_Reserve_Risk: {len(LCR_030_Reserve_Risk)} rows")
print(f"LCR_040_Cat_Risk_Summary: {len(LCR_040_Cat_Risk_Summary)} rows")
print(f"LCR_041_Cat_By_Peril: {len(LCR_041_Cat_By_Peril)} rows")
print(f"LCR_050_Market_Risk: {len(LCR_050_Market_Risk)} rows")
print(f"LCR_060_Credit_Risk: {len(LCR_060_Credit_Risk)} rows")
print(f"LCR_070_Operational_Risk: {len(LCR_070_Operational_Risk)} rows")
print(f"LCR_080_Technical_Provisions: {len(LCR_080_Technical_Provisions)} rows")
print(f"LCR_090_Own_Funds: {len(LCR_090_Own_Funds)} rows")
print(f"LCR_100_Coverage_Ratios: {len(LCR_100_Coverage_Ratios)} rows")
print(f"LCR_110_YOA_Capital: {len(LCR_110_YOA_Capital)} rows")
print(f"LCR_120_Diversification: {len(LCR_120_Diversification)} rows")
