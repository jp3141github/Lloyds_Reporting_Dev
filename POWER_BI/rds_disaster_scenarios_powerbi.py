# Realistic Disaster Scenarios (RDS) - Power BI Data Generator
# Lloyd's Catastrophe and Extreme Event Exposure Reporting
#
# RDS provides loss estimates for prescribed extreme scenarios:
# - Natural catastrophe (hurricane, earthquake, windstorm, flood)
# - Terrorism
# - Cyber
# - Liability
# - Pandemic
# - Syndicate-defined scenarios
# - "Lite" thresholds for exposure monitoring
#
# Key uses:
# - Aggregate exposure management at Lloyd's market level
# - Cat risk calibration in LCR internal models
# - Liquidity stress testing inputs
# - Reinsurance programme adequacy assessment
#
# Submitted annually with quarterly updates for material changes
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
CURRENCY = 'GBP'

# Lloyd's Prescribed RDS Scenarios
PRESCRIBED_SCENARIOS = [
    # Natural Catastrophe - Hurricane
    ('RDS_HU_FL', 'Hurricane - Florida Landfall (Miami)', 'Hurricane', 'Natural Cat', '1-in-100'),
    ('RDS_HU_NE', 'Hurricane - Northeast US', 'Hurricane', 'Natural Cat', '1-in-200'),
    ('RDS_HU_GC', 'Hurricane - Gulf Coast (Houston)', 'Hurricane', 'Natural Cat', '1-in-100'),

    # Natural Catastrophe - Earthquake
    ('RDS_EQ_SF', 'Earthquake - San Francisco', 'Earthquake', 'Natural Cat', '1-in-250'),
    ('RDS_EQ_LA', 'Earthquake - Los Angeles', 'Earthquake', 'Natural Cat', '1-in-200'),
    ('RDS_EQ_JP', 'Earthquake - Japan (Tokyo)', 'Earthquake', 'Natural Cat', '1-in-200'),
    ('RDS_EQ_NZ', 'Earthquake - New Zealand', 'Earthquake', 'Natural Cat', '1-in-200'),

    # Natural Catastrophe - Windstorm
    ('RDS_WS_EU', 'European Windstorm', 'Windstorm', 'Natural Cat', '1-in-200'),
    ('RDS_WS_UK', 'UK Windstorm', 'Windstorm', 'Natural Cat', '1-in-200'),

    # Natural Catastrophe - Flood
    ('RDS_FL_UK', 'UK Flood', 'Flood', 'Natural Cat', '1-in-200'),
    ('RDS_FL_EU', 'European Flood', 'Flood', 'Natural Cat', '1-in-200'),

    # Terrorism
    ('RDS_TR_NY', 'Terrorism - New York', 'Terrorism', 'Man-Made', '1-in-200'),
    ('RDS_TR_LN', 'Terrorism - London', 'Terrorism', 'Man-Made', '1-in-200'),
    ('RDS_TR_WMD', 'Terrorism - WMD Attack', 'Terrorism', 'Man-Made', '1-in-500'),

    # Cyber
    ('RDS_CY_CL', 'Cyber - Cloud Outage', 'Cyber', 'Man-Made', '1-in-200'),
    ('RDS_CY_MA', 'Cyber - Mass Ransomware', 'Cyber', 'Man-Made', '1-in-100'),
    ('RDS_CY_DT', 'Cyber - Data Breach', 'Cyber', 'Man-Made', '1-in-100'),
    ('RDS_CY_PG', 'Cyber - Power Grid Attack', 'Cyber', 'Man-Made', '1-in-500'),

    # Liability
    ('RDS_LI_US', 'US Liability - Mass Tort', 'Liability', 'Liability', '1-in-200'),
    ('RDS_LI_PH', 'Pharmaceutical Recall', 'Liability', 'Liability', '1-in-200'),
    ('RDS_LI_AV', 'Aviation - Major Incident', 'Liability', 'Liability', '1-in-200'),

    # Marine / Energy
    ('RDS_MA_GC', 'Marine - Gulf of Mexico Platform', 'Marine/Energy', 'Marine', '1-in-200'),
    ('RDS_MA_PC', 'Marine - Port Accumulation', 'Marine/Energy', 'Marine', '1-in-200'),

    # Pandemic
    ('RDS_PAN_G', 'Pandemic - Global', 'Pandemic', 'Pandemic', '1-in-200'),

    # Other
    ('RDS_SAT', 'Satellite Loss - Multiple', 'Satellite', 'Space', '1-in-200'),
    ('RDS_FIN', 'Financial Lines - Major D&O Event', 'Financial', 'Liability', '1-in-200')
]

# RDS Lines of Business mapping
RDS_LOBS = [
    'Property D&F',
    'Property Treaty',
    'Casualty',
    'Marine',
    'Aviation',
    'Energy',
    'Motor',
    'Cyber',
    'Terrorism',
    'D&O / Financial Lines',
    'Contingency',
    'Other'
]

# =============================================================================
# RDS_001_Control - Submission metadata
# =============================================================================
def generate_rds_001_control():
    records = []
    for syn in SYNDICATES:
        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'ReportingDate': datetime(REPORTING_YEAR, 6, 30),  # Mid-year submission
            'SubmissionDate': datetime(REPORTING_YEAR, 7, 15) + timedelta(days=np.random.randint(0, 5)),
            'ManagingAgent': f'MA{syn % 100:03d}',
            'ReportType': 'RDS',
            'ReturnVersion': '2024.1',
            'Status': 'Final',
            'ModelProvider': np.random.choice(['RMS', 'AIR', 'Internal', 'Hybrid'], p=[0.35, 0.30, 0.20, 0.15]),
            'Stamp_Capacity_GBP_M': round(np.random.uniform(200, 800), 1),
            'Currency': CURRENCY
        })
    return pd.DataFrame(records)

# =============================================================================
# RDS_010_Scenario_Summary - All scenarios summary
# =============================================================================
def generate_rds_010_scenario_summary():
    records = []
    for syn in SYNDICATES:
        # Syndicate size affects loss estimates
        size_factor = np.random.uniform(0.5, 2.0)

        for scenario_code, scenario_name, peril, category, return_period in PRESCRIBED_SCENARIOS:
            # Base loss estimate varies by peril
            if peril == 'Hurricane':
                base_gross = np.random.uniform(50, 200) * size_factor
            elif peril == 'Earthquake':
                base_gross = np.random.uniform(30, 150) * size_factor
            elif peril == 'Windstorm':
                base_gross = np.random.uniform(20, 80) * size_factor
            elif peril == 'Terrorism':
                base_gross = np.random.uniform(15, 60) * size_factor
            elif peril == 'Cyber':
                base_gross = np.random.uniform(10, 50) * size_factor
            elif peril == 'Pandemic':
                base_gross = np.random.uniform(30, 100) * size_factor
            else:
                base_gross = np.random.uniform(10, 40) * size_factor

            # Reinsurance recovery
            ri_recovery_pct = np.random.uniform(0.30, 0.60)
            ri_recovery = base_gross * ri_recovery_pct
            net_loss = base_gross - ri_recovery

            # Reinstatement premiums
            reinstatement = ri_recovery * np.random.uniform(0.05, 0.15)

            # Final net after reinstatement
            final_net = net_loss + reinstatement

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Scenario_Code': scenario_code,
                'Scenario_Name': scenario_name,
                'Peril': peril,
                'Category': category,
                'Return_Period': return_period,
                'Gross_Loss_GBP_M': round(base_gross, 2),
                'RI_Recovery_GBP_M': round(ri_recovery, 2),
                'RI_Recovery_Pct': round(ri_recovery_pct * 100, 1),
                'Net_Loss_Pre_Reinst_GBP_M': round(net_loss, 2),
                'Reinstatement_Premium_GBP_M': round(reinstatement, 2),
                'Final_Net_Loss_GBP_M': round(final_net, 2),
                'Currency': CURRENCY
            })
    return pd.DataFrame(records)

# =============================================================================
# RDS_020_Scenario_By_LOB - Scenario losses by line of business
# =============================================================================
def generate_rds_020_scenario_by_lob():
    records = []

    # LOB relevance by peril type
    peril_lob_weights = {
        'Hurricane': {'Property D&F': 0.35, 'Property Treaty': 0.30, 'Marine': 0.10, 'Motor': 0.05,
                      'Contingency': 0.05, 'Other': 0.15},
        'Earthquake': {'Property D&F': 0.40, 'Property Treaty': 0.35, 'Contingency': 0.10, 'Other': 0.15},
        'Windstorm': {'Property D&F': 0.35, 'Property Treaty': 0.30, 'Motor': 0.15, 'Other': 0.20},
        'Flood': {'Property D&F': 0.40, 'Property Treaty': 0.30, 'Motor': 0.10, 'Other': 0.20},
        'Terrorism': {'Property D&F': 0.25, 'Casualty': 0.20, 'Terrorism': 0.30, 'Aviation': 0.10,
                      'Other': 0.15},
        'Cyber': {'Cyber': 0.50, 'Casualty': 0.20, 'D&O / Financial Lines': 0.20, 'Other': 0.10},
        'Liability': {'Casualty': 0.40, 'D&O / Financial Lines': 0.30, 'Aviation': 0.15, 'Other': 0.15},
        'Marine/Energy': {'Marine': 0.35, 'Energy': 0.40, 'Property D&F': 0.15, 'Other': 0.10},
        'Pandemic': {'Contingency': 0.40, 'Casualty': 0.25, 'Other': 0.35},
        'Satellite': {'Aviation': 0.50, 'Property D&F': 0.30, 'Other': 0.20},
        'Financial': {'D&O / Financial Lines': 0.60, 'Casualty': 0.25, 'Other': 0.15}
    }

    for syn in SYNDICATES:
        size_factor = np.random.uniform(0.5, 2.0)

        for scenario_code, scenario_name, peril, category, return_period in PRESCRIBED_SCENARIOS[:10]:  # Top 10 scenarios
            # Get weights for this peril
            weights = peril_lob_weights.get(peril, {'Other': 1.0})

            # Total scenario loss
            if peril == 'Hurricane':
                total_gross = np.random.uniform(50, 200) * size_factor
            elif peril == 'Earthquake':
                total_gross = np.random.uniform(30, 150) * size_factor
            else:
                total_gross = np.random.uniform(20, 80) * size_factor

            for lob in RDS_LOBS:
                weight = weights.get(lob, 0)
                if weight == 0:
                    continue

                lob_gross = total_gross * weight * np.random.uniform(0.8, 1.2)
                ri_recovery = lob_gross * np.random.uniform(0.25, 0.55)
                lob_net = lob_gross - ri_recovery

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Scenario_Code': scenario_code,
                    'Scenario_Name': scenario_name,
                    'Peril': peril,
                    'LOB': lob,
                    'Gross_Loss_GBP_M': round(lob_gross, 2),
                    'RI_Recovery_GBP_M': round(ri_recovery, 2),
                    'Net_Loss_GBP_M': round(lob_net, 2),
                    'LOB_Contribution_Pct': round(weight * 100, 1),
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# RDS_030_Cat_Scenarios - Detailed natural cat scenarios
# =============================================================================
def generate_rds_030_cat_scenarios():
    records = []

    # Return period points for cat curve
    return_periods = [10, 25, 50, 100, 200, 250, 500, 1000]

    # Cat perils subset
    cat_scenarios = [s for s in PRESCRIBED_SCENARIOS if s[3] == 'Natural Cat']

    for syn in SYNDICATES:
        size_factor = np.random.uniform(0.5, 2.0)

        for scenario_code, scenario_name, peril, category, base_rp in cat_scenarios[:6]:  # Top 6 cat scenarios
            for rp in return_periods:
                # Loss scales with return period
                rp_factor = np.log(rp) / np.log(200)  # Normalize to 1-in-200

                if peril == 'Hurricane':
                    base_loss = 100 * size_factor
                elif peril == 'Earthquake':
                    base_loss = 80 * size_factor
                else:
                    base_loss = 50 * size_factor

                gross_loss = base_loss * rp_factor * np.random.uniform(0.9, 1.1)

                # RI more effective at higher return periods
                ri_pct = min(0.65, 0.25 + (np.log(rp) / np.log(1000)) * 0.4)
                ri_recovery = gross_loss * ri_pct
                net_loss = gross_loss - ri_recovery

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Scenario_Code': scenario_code,
                    'Scenario_Name': scenario_name,
                    'Peril': peril,
                    'Return_Period': rp,
                    'Return_Period_Label': f'1-in-{rp}',
                    'Annual_Exceedance_Prob_Pct': round(100 / rp, 2),
                    'Gross_Loss_GBP_M': round(gross_loss, 2),
                    'RI_Recovery_GBP_M': round(ri_recovery, 2),
                    'Net_Loss_GBP_M': round(net_loss, 2),
                    'Model_Source': np.random.choice(['RMS', 'AIR', 'Internal']),
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# RDS_040_Cyber_Scenarios - Detailed cyber scenarios
# =============================================================================
def generate_rds_040_cyber_scenarios():
    records = []

    cyber_sub_scenarios = [
        ('CY_CLOUD_AWS', 'Cloud Outage - AWS', 'Cloud Provider Failure'),
        ('CY_CLOUD_AZ', 'Cloud Outage - Azure', 'Cloud Provider Failure'),
        ('CY_RANSOM_WC', 'Ransomware - WannaCry-style', 'Malware'),
        ('CY_RANSOM_TA', 'Ransomware - Targeted Attack', 'Malware'),
        ('CY_BREACH_FI', 'Data Breach - Financial Services', 'Data Breach'),
        ('CY_BREACH_HC', 'Data Breach - Healthcare', 'Data Breach'),
        ('CY_SUPPLY', 'Supply Chain Attack', 'Supply Chain'),
        ('CY_INFRA', 'Critical Infrastructure Attack', 'Infrastructure')
    ]

    for syn in SYNDICATES:
        cyber_exposure = np.random.uniform(20, 100)  # Syndicate cyber book size

        for sub_code, sub_name, attack_type in cyber_sub_scenarios:
            # Vary loss by attack type
            if attack_type == 'Cloud Provider Failure':
                base_loss = cyber_exposure * np.random.uniform(0.3, 0.5)
            elif attack_type == 'Malware':
                base_loss = cyber_exposure * np.random.uniform(0.4, 0.6)
            elif attack_type == 'Data Breach':
                base_loss = cyber_exposure * np.random.uniform(0.2, 0.4)
            else:
                base_loss = cyber_exposure * np.random.uniform(0.25, 0.45)

            # Loss components
            bi_loss = base_loss * np.random.uniform(0.35, 0.50)
            liability_loss = base_loss * np.random.uniform(0.25, 0.40)
            forensic_cost = base_loss * np.random.uniform(0.10, 0.20)
            other_loss = base_loss - bi_loss - liability_loss - forensic_cost

            # RI recovery
            ri_recovery = base_loss * np.random.uniform(0.20, 0.45)
            net_loss = base_loss - ri_recovery

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Sub_Scenario_Code': sub_code,
                'Sub_Scenario_Name': sub_name,
                'Attack_Type': attack_type,
                'Gross_Loss_GBP_M': round(base_loss, 2),
                'BI_Loss_GBP_M': round(bi_loss, 2),
                'Liability_Loss_GBP_M': round(liability_loss, 2),
                'Forensic_Cost_GBP_M': round(forensic_cost, 2),
                'Other_Loss_GBP_M': round(max(0, other_loss), 2),
                'RI_Recovery_GBP_M': round(ri_recovery, 2),
                'Net_Loss_GBP_M': round(net_loss, 2),
                'Affirmative_Pct': round(np.random.uniform(60, 90), 1),
                'Silent_Pct': round(np.random.uniform(10, 40), 1),
                'Currency': CURRENCY
            })

    return pd.DataFrame(records)

# =============================================================================
# RDS_050_Syndicate_Defined - Syndicate's own scenarios
# =============================================================================
def generate_rds_050_syndicate_defined():
    records = []

    # Syndicate-specific scenarios (varies by syndicate focus)
    syndicate_scenarios = [
        ('SD_SPEC_1', 'Specialty - Combined Satellite Loss', 'Satellite', '1-in-150'),
        ('SD_SPEC_2', 'Specialty - Major Sports Event Cancellation', 'Contingency', '1-in-100'),
        ('SD_MAR_1', 'Marine - Major Port Blockage', 'Marine', '1-in-200'),
        ('SD_AVI_1', 'Aviation - Fleet Grounding', 'Aviation', '1-in-200'),
        ('SD_POL_1', 'Political Risk - Sovereign Default', 'Political Risk', '1-in-200'),
        ('SD_CAS_1', 'Casualty - US Opioid Litigation', 'Casualty', '1-in-100'),
        ('SD_FIN_1', 'Financial Lines - Crypto Collapse', 'Financial', '1-in-100'),
        ('SD_ENE_1', 'Energy - North Sea Platform Loss', 'Energy', '1-in-200')
    ]

    for syn in SYNDICATES:
        # Each syndicate selects 3-5 relevant scenarios
        num_scenarios = np.random.randint(3, 6)
        selected_scenarios = np.random.choice(len(syndicate_scenarios), num_scenarios, replace=False)

        for idx in selected_scenarios:
            sd_code, sd_name, peril, return_period = syndicate_scenarios[idx]

            # Loss estimate
            gross_loss = np.random.uniform(20, 100)
            ri_recovery = gross_loss * np.random.uniform(0.25, 0.55)
            net_loss = gross_loss - ri_recovery

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Scenario_Code': f'{syn}_{sd_code}',
                'Scenario_Name': sd_name,
                'Peril': peril,
                'Return_Period': return_period,
                'Gross_Loss_GBP_M': round(gross_loss, 2),
                'RI_Recovery_GBP_M': round(ri_recovery, 2),
                'Net_Loss_GBP_M': round(net_loss, 2),
                'Rationale': f'Scenario reflects {peril.lower()} exposure specific to syndicate {syn} portfolio',
                'Model_Source': np.random.choice(['Internal', 'Hybrid']),
                'Currency': CURRENCY
            })

    return pd.DataFrame(records)

# =============================================================================
# RDS_060_Lite_Thresholds - RDS Lite monitoring thresholds
# =============================================================================
def generate_rds_060_lite_thresholds():
    records = []

    # RDS Lite zones and thresholds
    lite_zones = [
        ('Zone A', 'Caribbean Hurricane', 'Hurricane', 50, 100, 150, 200),
        ('Zone B', 'US Gulf Hurricane', 'Hurricane', 45, 90, 135, 180),
        ('Zone C', 'US East Coast Hurricane', 'Hurricane', 40, 80, 120, 160),
        ('Zone D', 'California Earthquake', 'Earthquake', 35, 70, 105, 140),
        ('Zone E', 'Pacific Northwest Earthquake', 'Earthquake', 30, 60, 90, 120),
        ('Zone F', 'Japan Earthquake', 'Earthquake', 35, 70, 105, 140),
        ('Zone G', 'European Windstorm', 'Windstorm', 25, 50, 75, 100),
        ('Zone H', 'UK Flood', 'Flood', 20, 40, 60, 80)
    ]

    for syn in SYNDICATES:
        for zone, zone_name, peril, t1, t2, t3, t4 in lite_zones:
            # Current exposure relative to thresholds
            size_factor = np.random.uniform(0.5, 1.8)

            gross_exposure = t2 * size_factor * np.random.uniform(0.7, 1.3)
            net_exposure = gross_exposure * np.random.uniform(0.45, 0.70)

            # Determine RAG status
            if net_exposure <= t1:
                rag = 'Green'
            elif net_exposure <= t2:
                rag = 'Amber'
            elif net_exposure <= t3:
                rag = 'Red'
            else:
                rag = 'Breach'

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Zone': zone,
                'Zone_Name': zone_name,
                'Peril': peril,
                'Threshold_1_GBP_M': t1,
                'Threshold_2_GBP_M': t2,
                'Threshold_3_GBP_M': t3,
                'Threshold_4_GBP_M': t4,
                'Gross_Exposure_GBP_M': round(gross_exposure, 2),
                'Net_Exposure_GBP_M': round(net_exposure, 2),
                'RAG_Status': rag,
                'Headroom_GBP_M': round(t2 - net_exposure, 2),
                'Utilization_Pct': round((net_exposure / t2) * 100, 1),
                'Currency': CURRENCY
            })

    return pd.DataFrame(records)

# =============================================================================
# RDS_070_Aggregate_Exposure - Market aggregate view
# =============================================================================
def generate_rds_070_aggregate_exposure():
    records = []

    # Aggregate by peril across syndicates
    perils = ['Hurricane', 'Earthquake', 'Windstorm', 'Flood', 'Terrorism', 'Cyber', 'Pandemic']

    for peril in perils:
        # Aggregate market exposure
        total_gross = np.random.uniform(500, 2000)
        total_net = total_gross * np.random.uniform(0.40, 0.60)

        # Top 5 syndicates contribution
        top_5_gross = total_gross * np.random.uniform(0.35, 0.55)
        top_5_net = total_net * np.random.uniform(0.35, 0.55)

        # Concentration metrics
        hhi = np.random.uniform(500, 1500)  # Herfindahl-Hirschman Index

        records.append({
            'ReportingYear': REPORTING_YEAR,
            'Peril': peril,
            'Market_Gross_GBP_M': round(total_gross, 2),
            'Market_Net_GBP_M': round(total_net, 2),
            'RI_Benefit_Pct': round((1 - total_net / total_gross) * 100, 1),
            'Top_5_Syndicates_Gross_GBP_M': round(top_5_gross, 2),
            'Top_5_Syndicates_Net_GBP_M': round(top_5_net, 2),
            'Top_5_Concentration_Pct': round((top_5_gross / total_gross) * 100, 1),
            'HHI_Index': round(hhi, 0),
            'Syndicate_Count': np.random.randint(30, 70),
            'YoY_Change_Pct': round(np.random.uniform(-10, 15), 1),
            'Currency': CURRENCY
        })

    return pd.DataFrame(records)

# =============================================================================
# Generate all tables
# =============================================================================

# Control
RDS_001_Control = generate_rds_001_control()

# Scenario data
RDS_010_Scenario_Summary = generate_rds_010_scenario_summary()
RDS_020_Scenario_By_LOB = generate_rds_020_scenario_by_lob()
RDS_030_Cat_Scenarios = generate_rds_030_cat_scenarios()
RDS_040_Cyber_Scenarios = generate_rds_040_cyber_scenarios()
RDS_050_Syndicate_Defined = generate_rds_050_syndicate_defined()

# Monitoring
RDS_060_Lite_Thresholds = generate_rds_060_lite_thresholds()
RDS_070_Aggregate_Exposure = generate_rds_070_aggregate_exposure()

# Summary statistics
print("=" * 70)
print("RDS - Realistic Disaster Scenarios Data Generator")
print("=" * 70)
print(f"RDS_001_Control: {len(RDS_001_Control)} rows")
print(f"RDS_010_Scenario_Summary: {len(RDS_010_Scenario_Summary)} rows")
print(f"RDS_020_Scenario_By_LOB: {len(RDS_020_Scenario_By_LOB)} rows")
print(f"RDS_030_Cat_Scenarios: {len(RDS_030_Cat_Scenarios)} rows")
print(f"RDS_040_Cyber_Scenarios: {len(RDS_040_Cyber_Scenarios)} rows")
print(f"RDS_050_Syndicate_Defined: {len(RDS_050_Syndicate_Defined)} rows")
print(f"RDS_060_Lite_Thresholds: {len(RDS_060_Lite_Thresholds)} rows")
print(f"RDS_070_Aggregate_Exposure: {len(RDS_070_Aggregate_Exposure)} rows")
print("=" * 70)
print("RDS data generated successfully!")
