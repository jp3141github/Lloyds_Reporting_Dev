# Syndicate Reinsurance Structure (SRS) - Power BI Data Generator
# Reinsurance Programme Structure and Counterparty Exposure Reporting
#
# SRS provides Lloyd's with visibility of syndicate reinsurance arrangements:
# - Reinsurance programme structure (QS, XL, FAC, etc.)
# - Reinsurer counterparty exposures and credit quality
# - Aggregate exposure by reinsurer
# - Collateral and security arrangements
#
# Key uses:
# - Credit risk assessment and capital (LCR)
# - Net exposure calculation (RDS)
# - Liquidity stress testing (LST) - RI recovery timing
# - Aggregate market reinsurer concentration monitoring
#
# Submitted at least twice yearly (typically June and December)
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
SUBMISSIONS = ['H1', 'H2']  # Twice yearly
CURRENCY = 'GBP'

# Reinsurance types
RI_TYPES = [
    ('QS', 'Quota Share', 'Proportional'),
    ('SS', 'Surplus Share', 'Proportional'),
    ('XL_WC', 'Working Cover XL', 'Non-Proportional'),
    ('XL_CAT', 'Catastrophe XL', 'Non-Proportional'),
    ('XL_CLASH', 'Clash Cover', 'Non-Proportional'),
    ('AGG_XL', 'Aggregate XL', 'Non-Proportional'),
    ('SL', 'Stop Loss', 'Non-Proportional'),
    ('FAC', 'Facultative', 'Facultative'),
    ('FAC_OBL', 'Fac Obligatory', 'Facultative')
]

# Lloyd's Risk Codes for RI programme coverage
RISK_CODE_GROUPS = [
    ('PROP', 'Property'),
    ('CAS', 'Casualty'),
    ('MAR', 'Marine'),
    ('AVI', 'Aviation'),
    ('ENE', 'Energy'),
    ('MOT', 'Motor'),
    ('CYB', 'Cyber'),
    ('FIN', 'Financial Lines'),
    ('WC', 'Whole Account')
]

# Major reinsurers
REINSURERS = [
    ('MR', 'Munich Re', 'AA-', 'DE', 0),
    ('SR', 'Swiss Re', 'AA-', 'CH', 0),
    ('HR', 'Hannover Re', 'AA-', 'DE', 0),
    ('SCOR', 'SCOR', 'AA-', 'FR', 0),
    ('RGA', 'RGA', 'A+', 'US', 0),
    ('BRK', 'Berkshire Hathaway', 'AA+', 'US', 0),
    ('LLYD', 'Lloyd\'s Syndicates', 'A+', 'GB', 0),
    ('EVER', 'Everest Re', 'A+', 'BM', 0),
    ('PART', 'PartnerRe', 'A+', 'BM', 0),
    ('TRAN', 'TransRe', 'A+', 'US', 0),
    ('AXA', 'AXA XL', 'A+', 'BM', 0),
    ('CHUBB', 'Chubb Re', 'AA', 'CH', 0),
    ('FAIR', 'Fairfax', 'A', 'CA', 1),  # Requires collateral
    ('CHINA', 'China Re', 'A', 'CN', 1),  # Requires collateral
    ('OTHER', 'Other Reinsurers', 'A-', 'XX', 0)
]

# =============================================================================
# SRS_001_Control - Submission metadata
# =============================================================================
def generate_srs_001_control():
    records = []
    for syn in SYNDICATES:
        for submission in SUBMISSIONS:
            submission_date = datetime(REPORTING_YEAR, 6, 30) if submission == 'H1' else datetime(REPORTING_YEAR, 12, 31)
            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Submission': submission,
                'SubmissionDate': submission_date + timedelta(days=np.random.randint(10, 20)),
                'ManagingAgent': f'MA{syn % 100:03d}',
                'ReportType': 'SRS',
                'ReturnVersion': '2024.1',
                'Status': 'Final',
                'Programme_Count': np.random.randint(8, 20),
                'Total_RI_Spend_GBP_M': round(np.random.uniform(20, 100), 2),
                'Currency': CURRENCY
            })
    return pd.DataFrame(records)

# =============================================================================
# SRS_010_Programme_Summary - Overall RI programme summary
# =============================================================================
def generate_srs_010_programme_summary():
    records = []
    for syn in SYNDICATES:
        # Syndicate size determines RI spend
        gwp = np.random.uniform(200, 700)
        total_ri_spend = gwp * np.random.uniform(0.08, 0.18)

        for submission in SUBMISSIONS:
            # RI type breakdown
            prop_ri = total_ri_spend * np.random.uniform(0.30, 0.45)
            nonprop_ri = total_ri_spend * np.random.uniform(0.45, 0.60)
            fac_ri = total_ri_spend - prop_ri - nonprop_ri

            # Expected recoveries
            expected_recovery = total_ri_spend * np.random.uniform(0.5, 0.8)

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Submission': submission,
                'GWP_GBP_M': round(gwp, 2),
                'Total_RI_Premium_GBP_M': round(total_ri_spend, 2),
                'RI_Ratio_Pct': round((total_ri_spend / gwp) * 100, 1),
                'Proportional_RI_GBP_M': round(prop_ri, 2),
                'NonProportional_RI_GBP_M': round(nonprop_ri, 2),
                'Facultative_RI_GBP_M': round(fac_ri, 2),
                'Expected_Recovery_GBP_M': round(expected_recovery, 2),
                'Net_Cost_GBP_M': round(total_ri_spend - expected_recovery, 2),
                'Active_Programmes': np.random.randint(10, 25),
                'Active_Reinsurers': np.random.randint(15, 40),
                'Currency': CURRENCY
            })
    return pd.DataFrame(records)

# =============================================================================
# SRS_020_Programme_Detail - Individual RI programme details
# =============================================================================
def generate_srs_020_programme_detail():
    records = []

    for syn in SYNDICATES:
        gwp = np.random.uniform(200, 700)
        programme_id = 1

        for submission in SUBMISSIONS:
            for ri_type_code, ri_type_name, ri_category in RI_TYPES:
                # Not every syndicate has every type
                if np.random.random() < 0.2:
                    continue

                for risk_group_code, risk_group_name in RISK_CODE_GROUPS:
                    # Some RI types are whole-account only
                    if ri_type_code in ['XL_CLASH', 'AGG_XL', 'SL'] and risk_group_code != 'WC':
                        continue

                    # Not every class needs its own programme
                    if ri_type_code not in ['XL_CLASH', 'AGG_XL', 'SL'] and risk_group_code == 'WC':
                        continue

                    if np.random.random() < 0.4:
                        continue

                    # Programme details
                    if ri_category == 'Proportional':
                        cession_pct = np.random.uniform(15, 40)
                        limit = None
                        retention = None
                        ri_premium = gwp * (cession_pct / 100) * np.random.uniform(0.2, 0.35)
                    elif ri_category == 'Non-Proportional':
                        cession_pct = None
                        limit = np.random.uniform(20, 100)
                        retention = np.random.uniform(5, 30)
                        ri_premium = limit * np.random.uniform(0.03, 0.12)
                    else:  # Facultative
                        cession_pct = np.random.uniform(10, 50)
                        limit = np.random.uniform(5, 50)
                        retention = None
                        ri_premium = np.random.uniform(0.5, 5)

                    # Reinstatements
                    reinstatements = np.random.choice([0, 1, 2, 'Unlimited']) if ri_category == 'Non-Proportional' else None

                    # Inception and expiry
                    inception = datetime(REPORTING_YEAR, 1, 1)
                    expiry = datetime(REPORTING_YEAR, 12, 31)

                    records.append({
                        'Syndicate': syn,
                        'ReportingYear': REPORTING_YEAR,
                        'Submission': submission,
                        'Programme_ID': f'{syn}_P{programme_id:03d}',
                        'RI_Type_Code': ri_type_code,
                        'RI_Type_Name': ri_type_name,
                        'RI_Category': ri_category,
                        'Risk_Group_Code': risk_group_code,
                        'Risk_Group_Name': risk_group_name,
                        'Cession_Pct': round(cession_pct, 1) if cession_pct else None,
                        'Limit_GBP_M': round(limit, 2) if limit else None,
                        'Retention_GBP_M': round(retention, 2) if retention else None,
                        'RI_Premium_GBP_M': round(ri_premium, 2),
                        'Reinstatements': str(reinstatements) if reinstatements is not None else None,
                        'Inception_Date': inception,
                        'Expiry_Date': expiry,
                        'Broker': np.random.choice(['Aon', 'Willis', 'Guy Carpenter', 'Gallagher Re']),
                        'Currency': CURRENCY
                    })

                    programme_id += 1

    return pd.DataFrame(records)

# =============================================================================
# SRS_030_Counterparty_Exposure - Reinsurer counterparty exposure
# =============================================================================
def generate_srs_030_counterparty_exposure():
    records = []

    for syn in SYNDICATES:
        total_exposure = np.random.uniform(100, 400)

        for submission in SUBMISSIONS:
            # Distribute exposure among reinsurers
            weights = np.random.dirichlet(np.ones(len(REINSURERS)) * 0.5)

            for i, (ri_code, ri_name, rating, country, coll_req) in enumerate(REINSURERS):
                weight = weights[i]
                exposure = total_exposure * weight

                if exposure < 1:  # Skip very small exposures
                    continue

                # Collateral held
                if coll_req:
                    collateral = exposure * np.random.uniform(0.50, 1.0)
                else:
                    collateral = exposure * np.random.uniform(0, 0.20)

                # Net exposure after collateral
                net_exposure = max(0, exposure - collateral)

                # Current recoverable and IBNR recoverable
                current_recoverable = exposure * np.random.uniform(0.15, 0.35)
                ibnr_recoverable = exposure * np.random.uniform(0.10, 0.25)

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Submission': submission,
                    'Reinsurer_Code': ri_code,
                    'Reinsurer_Name': ri_name,
                    'Rating': rating,
                    'Domicile': country,
                    'Total_Exposure_GBP_M': round(exposure, 2),
                    'Collateral_Held_GBP_M': round(collateral, 2),
                    'Net_Exposure_GBP_M': round(net_exposure, 2),
                    'Exposure_Pct_of_Total': round(weight * 100, 1),
                    'Current_Recoverable_GBP_M': round(current_recoverable, 2),
                    'IBNR_Recoverable_GBP_M': round(ibnr_recoverable, 2),
                    'Requires_Collateral': 'Yes' if coll_req else 'No',
                    'Within_Limit': 'Yes' if net_exposure < 50 else 'No',
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# SRS_040_Collateral_Detail - Collateral and security arrangements
# =============================================================================
def generate_srs_040_collateral_detail():
    records = []

    collateral_types = [
        ('LOC', 'Letter of Credit', 0.35),
        ('CASH', 'Cash Deposit', 0.25),
        ('TRUST', 'Trust Fund', 0.20),
        ('FUNDS_WH', 'Funds Withheld', 0.15),
        ('GUARANTEE', 'Parent Guarantee', 0.05)
    ]

    for syn in SYNDICATES:
        for submission in SUBMISSIONS:
            for ri_code, ri_name, rating, country, coll_req in REINSURERS[:8]:  # Top 8 reinsurers
                if coll_req == 0 and np.random.random() < 0.5:
                    continue  # Skip non-required collateral randomly

                exposure = np.random.uniform(20, 100)

                for coll_code, coll_name, base_weight in collateral_types:
                    # Randomly select collateral types used
                    if np.random.random() < 0.6:
                        continue

                    weight = base_weight * np.random.uniform(0.5, 1.5)
                    coll_amount = exposure * weight * np.random.uniform(0.1, 0.4)

                    if coll_amount < 0.5:
                        continue

                    # LOC details
                    if coll_code == 'LOC':
                        issuing_bank = np.random.choice(['HSBC', 'Barclays', 'Citi', 'JPMorgan', 'Deutsche'])
                        expiry_date = datetime(REPORTING_YEAR + 1, np.random.randint(3, 12), 15)
                    else:
                        issuing_bank = None
                        expiry_date = None

                    records.append({
                        'Syndicate': syn,
                        'ReportingYear': REPORTING_YEAR,
                        'Submission': submission,
                        'Reinsurer_Code': ri_code,
                        'Reinsurer_Name': ri_name,
                        'Collateral_Type': coll_code,
                        'Collateral_Description': coll_name,
                        'Amount_GBP_M': round(coll_amount, 2),
                        'Issuing_Bank': issuing_bank,
                        'Expiry_Date': expiry_date,
                        'Accessible': 'Yes' if coll_code in ['CASH', 'LOC'] else 'Restricted',
                        'Currency': CURRENCY
                    })

    return pd.DataFrame(records)

# =============================================================================
# SRS_050_Layer_Participation - XL layer participation details
# =============================================================================
def generate_srs_050_layer_participation():
    records = []

    for syn in SYNDICATES:
        for submission in SUBMISSIONS:
            # Generate a few XL programmes with layer detail
            for prog_num in range(1, np.random.randint(4, 8)):
                base_retention = np.random.uniform(5, 20)
                num_layers = np.random.randint(3, 6)

                layer_base = base_retention
                for layer_num in range(1, num_layers + 1):
                    layer_limit = np.random.uniform(10, 40)
                    layer_retention = layer_base

                    # Select reinsurers for this layer
                    num_reinsurers = np.random.randint(3, 8)
                    selected_reinsurers = np.random.choice(len(REINSURERS) - 1, num_reinsurers, replace=False)

                    shares = np.random.dirichlet(np.ones(num_reinsurers))

                    for i, ri_idx in enumerate(selected_reinsurers):
                        ri_code, ri_name, rating, country, _ = REINSURERS[ri_idx]
                        share_pct = shares[i] * 100

                        if share_pct < 2:
                            continue

                        records.append({
                            'Syndicate': syn,
                            'ReportingYear': REPORTING_YEAR,
                            'Submission': submission,
                            'Programme_ID': f'{syn}_XL{prog_num:02d}',
                            'Layer_Number': layer_num,
                            'Layer_Limit_GBP_M': round(layer_limit, 2),
                            'Layer_Retention_GBP_M': round(layer_retention, 2),
                            'Layer_Description': f'{round(layer_limit)}M xs {round(layer_retention)}M',
                            'Reinsurer_Code': ri_code,
                            'Reinsurer_Name': ri_name,
                            'Rating': rating,
                            'Share_Pct': round(share_pct, 1),
                            'Share_Amount_GBP_M': round(layer_limit * share_pct / 100, 2),
                            'Premium_Rate_Pct': round(np.random.uniform(3, 12), 2),
                            'Currency': CURRENCY
                        })

                    layer_base += layer_limit

    return pd.DataFrame(records)

# =============================================================================
# SRS_060_Recovery_Analysis - Expected recovery analysis
# =============================================================================
def generate_srs_060_recovery_analysis():
    records = []

    recovery_scenarios = [
        ('BASE', 'Base Case', 1.0),
        ('CAT_25', 'Cat 1-in-25', 1.5),
        ('CAT_50', 'Cat 1-in-50', 2.0),
        ('CAT_100', 'Cat 1-in-100', 3.0),
        ('CAT_200', 'Cat 1-in-200', 4.5),
        ('STRESS', 'Stressed (counterparty default)', 0.7)
    ]

    for syn in SYNDICATES:
        base_recovery = np.random.uniform(30, 120)

        for submission in SUBMISSIONS:
            for scenario_code, scenario_name, factor in recovery_scenarios:
                gross_loss = base_recovery * factor
                expected_recovery = gross_loss * np.random.uniform(0.35, 0.55)

                # Breakdown by RI type
                prop_recovery = expected_recovery * np.random.uniform(0.25, 0.40)
                xl_recovery = expected_recovery * np.random.uniform(0.45, 0.60)
                fac_recovery = expected_recovery - prop_recovery - xl_recovery

                # Default adjustment for stress scenario
                if scenario_code == 'STRESS':
                    default_haircut = expected_recovery * np.random.uniform(0.15, 0.30)
                else:
                    default_haircut = 0

                net_recovery = expected_recovery - default_haircut

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Submission': submission,
                    'Scenario_Code': scenario_code,
                    'Scenario_Name': scenario_name,
                    'Gross_Loss_GBP_M': round(gross_loss, 2),
                    'Total_Expected_Recovery_GBP_M': round(expected_recovery, 2),
                    'Proportional_Recovery_GBP_M': round(prop_recovery, 2),
                    'XL_Recovery_GBP_M': round(xl_recovery, 2),
                    'Facultative_Recovery_GBP_M': round(max(0, fac_recovery), 2),
                    'Default_Haircut_GBP_M': round(default_haircut, 2),
                    'Net_Recovery_GBP_M': round(net_recovery, 2),
                    'Recovery_Ratio_Pct': round((net_recovery / gross_loss) * 100, 1) if gross_loss > 0 else 0,
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# SRS_070_Concentration_Analysis - Market concentration analysis
# =============================================================================
def generate_srs_070_concentration_analysis():
    records = []

    for submission in SUBMISSIONS:
        # Market-wide concentration by reinsurer
        total_market_exposure = np.random.uniform(5000, 10000)

        for ri_code, ri_name, rating, country, _ in REINSURERS:
            market_share = np.random.uniform(0.02, 0.15)
            exposure = total_market_exposure * market_share

            # Syndicate count using this reinsurer
            syndicate_count = np.random.randint(20, 80)

            records.append({
                'ReportingYear': REPORTING_YEAR,
                'Submission': submission,
                'Reinsurer_Code': ri_code,
                'Reinsurer_Name': ri_name,
                'Rating': rating,
                'Domicile': country,
                'Market_Exposure_GBP_M': round(exposure, 2),
                'Market_Share_Pct': round(market_share * 100, 1),
                'Syndicate_Count': syndicate_count,
                'Avg_Exposure_Per_Syn_GBP_M': round(exposure / syndicate_count, 2),
                'Max_Single_Syn_Exposure_GBP_M': round(exposure * np.random.uniform(0.05, 0.15), 2),
                'Concentration_Flag': 'Yes' if market_share > 0.10 else 'No',
                'Currency': CURRENCY
            })

    return pd.DataFrame(records)

# =============================================================================
# Generate all tables
# =============================================================================

# Control
SRS_001_Control = generate_srs_001_control()

# Programme structure
SRS_010_Programme_Summary = generate_srs_010_programme_summary()
SRS_020_Programme_Detail = generate_srs_020_programme_detail()

# Counterparty exposure
SRS_030_Counterparty_Exposure = generate_srs_030_counterparty_exposure()
SRS_040_Collateral_Detail = generate_srs_040_collateral_detail()
SRS_050_Layer_Participation = generate_srs_050_layer_participation()

# Analysis
SRS_060_Recovery_Analysis = generate_srs_060_recovery_analysis()
SRS_070_Concentration_Analysis = generate_srs_070_concentration_analysis()

# Summary statistics
print("=" * 70)
print("SRS - Syndicate Reinsurance Structure Data Generator")
print("=" * 70)
print(f"SRS_001_Control: {len(SRS_001_Control)} rows")
print(f"SRS_010_Programme_Summary: {len(SRS_010_Programme_Summary)} rows")
print(f"SRS_020_Programme_Detail: {len(SRS_020_Programme_Detail)} rows")
print(f"SRS_030_Counterparty_Exposure: {len(SRS_030_Counterparty_Exposure)} rows")
print(f"SRS_040_Collateral_Detail: {len(SRS_040_Collateral_Detail)} rows")
print(f"SRS_050_Layer_Participation: {len(SRS_050_Layer_Participation)} rows")
print(f"SRS_060_Recovery_Analysis: {len(SRS_060_Recovery_Analysis)} rows")
print(f"SRS_070_Concentration_Analysis: {len(SRS_070_Concentration_Analysis)} rows")
print("=" * 70)
print("SRS data generated successfully!")
