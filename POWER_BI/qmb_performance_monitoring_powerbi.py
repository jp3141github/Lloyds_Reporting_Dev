# Quarterly Monitoring Return Part B (QMB) - Power BI Data Generator
# Performance Monitoring - Class-by-Class Actual vs Plan
#
# QMB is the early warning system for Lloyd's Performance Management:
# - Compares quarterly actual performance to SBF plan
# - Class-by-class ultimate loss ratio (ULR) tracking
# - Premium/claims/expense movements
# - Rate adequacy monitoring
# - Flags deteriorating classes for intervention
#
# Key relationships:
# - SBF -> QMB (plan vs actual comparison)
# - QMB -> PMDR (QMB aggregates monthly PMDR data)
# - QMB -> RRQ/RRA (reserve movements feed into reserving returns)
#
# Submitted quarterly, ~30 business days after quarter-end
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
QUARTERS = ['Q1', 'Q2', 'Q3', 'Q4']
QUARTER_ENDS = {
    'Q1': datetime(2024, 3, 31),
    'Q2': datetime(2024, 6, 30),
    'Q3': datetime(2024, 9, 30),
    'Q4': datetime(2024, 12, 31)
}
CURRENCY = 'GBP'

# Lloyd's risk codes (reserving classes)
RISK_CODES = [
    ('A1', 'Property D&F - Direct'),
    ('A2', 'Property D&F - Facultative'),
    ('A3', 'Property Commercial - Direct'),
    ('B1', 'Casualty - General Liability'),
    ('B2', 'Casualty - Professional Liability'),
    ('B3', 'Casualty - Financial Lines D&O'),
    ('B4', 'Casualty - Financial Lines PI'),
    ('C1', 'Marine Hull'),
    ('C2', 'Marine Cargo'),
    ('C3', 'Marine Liability'),
    ('D1', 'Energy Offshore'),
    ('D2', 'Energy Onshore'),
    ('E1', 'Aviation Hull'),
    ('E2', 'Aviation Liability'),
    ('F1', 'Motor - UK'),
    ('F2', 'Motor - International'),
    ('G1', 'Accident & Health'),
    ('H1', 'Credit & Surety'),
    ('I1', 'Cyber'),
    ('J1', 'Political Risk & Terror'),
    ('K1', 'Property Treaty XL'),
    ('K2', 'Property Treaty Pro-Rata'),
    ('L1', 'Casualty Treaty XL'),
    ('L2', 'Casualty Treaty Pro-Rata'),
    ('M1', 'Specialty - Contingency'),
    ('M2', 'Specialty - Livestock')
]

# Performance status flags
PERFORMANCE_STATUS = ['On Track', 'Monitor', 'Concern', 'Action Required']

# =============================================================================
# QMB_001_Control - Submission metadata
# =============================================================================
def generate_qmb_001_control():
    records = []
    for syn in SYNDICATES:
        for quarter in QUARTERS:
            quarter_end = QUARTER_ENDS[quarter]
            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Quarter': quarter,
                'QuarterEnd': quarter_end,
                'SubmissionDeadline': quarter_end + timedelta(days=30),
                'SubmissionDate': quarter_end + timedelta(days=np.random.randint(25, 30)),
                'ManagingAgent': f'MA{syn % 100:03d}',
                'ReportType': 'QMB',
                'ReturnVersion': '2024.1',
                'Status': 'Final',
                'SBF_Version': f'SBF_2024_V{np.random.randint(1, 3)}',
                'Currency': CURRENCY
            })
    return pd.DataFrame(records)

# =============================================================================
# QMB_010_Performance_Summary - High-level syndicate performance vs plan
# =============================================================================
def generate_qmb_010_performance_summary():
    records = []
    for syn in SYNDICATES:
        # SBF plan figures (annual targets)
        plan_gwp = np.random.uniform(250, 700)
        plan_ulr = np.random.uniform(60, 75)
        plan_expense_ratio = np.random.uniform(30, 38)
        plan_combined = plan_ulr + plan_expense_ratio

        for q_idx, quarter in enumerate(QUARTERS):
            # YTD actual (cumulates through year)
            ytd_pct = (q_idx + 1) * 0.25
            ytd_gwp = plan_gwp * ytd_pct * np.random.uniform(0.90, 1.10)

            # ULR drifts from plan
            ulr_drift = np.random.uniform(-5, 8)
            actual_ulr = plan_ulr + ulr_drift + (q_idx * np.random.uniform(-1, 2))

            # Expense ratio relatively stable
            actual_expense = plan_expense_ratio * np.random.uniform(0.95, 1.05)
            actual_combined = actual_ulr + actual_expense

            # Performance status based on deviation
            combined_variance = actual_combined - plan_combined
            if combined_variance < 2:
                status = 'On Track'
            elif combined_variance < 5:
                status = 'Monitor'
            elif combined_variance < 10:
                status = 'Concern'
            else:
                status = 'Action Required'

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Quarter': quarter,
                'QuarterEnd': QUARTER_ENDS[quarter],
                # Plan (full year)
                'Plan_GWP_GBP_M': round(plan_gwp, 2),
                'Plan_ULR_Pct': round(plan_ulr, 1),
                'Plan_Expense_Ratio_Pct': round(plan_expense_ratio, 1),
                'Plan_Combined_Ratio_Pct': round(plan_combined, 1),
                # YTD Actual
                'YTD_GWP_GBP_M': round(ytd_gwp, 2),
                'YTD_GWP_Pct_of_Plan': round((ytd_gwp / (plan_gwp * ytd_pct)) * 100, 1),
                'Actual_ULR_Pct': round(actual_ulr, 1),
                'Actual_Expense_Ratio_Pct': round(actual_expense, 1),
                'Actual_Combined_Ratio_Pct': round(actual_combined, 1),
                # Variance
                'ULR_Variance_Pct': round(actual_ulr - plan_ulr, 1),
                'Combined_Variance_Pct': round(combined_variance, 1),
                # Status
                'Performance_Status': status,
                'Requires_Action': 'Yes' if status in ['Concern', 'Action Required'] else 'No',
                'Currency': CURRENCY
            })
    return pd.DataFrame(records)

# =============================================================================
# QMB_020_Class_Performance - Class-by-class performance vs SBF
# =============================================================================
def generate_qmb_020_class_performance():
    records = []

    for syn in SYNDICATES:
        # Generate random subset of classes for this syndicate
        num_classes = np.random.randint(8, 18)
        syn_classes = np.random.choice(len(RISK_CODES), num_classes, replace=False)

        for class_idx in syn_classes:
            risk_code, risk_name = RISK_CODES[class_idx]

            # SBF plan for this class
            plan_gwp = np.random.uniform(10, 80)
            plan_nep = plan_gwp * np.random.uniform(0.85, 0.95)
            plan_ulr = np.random.uniform(55, 80)
            plan_ielr = plan_ulr - np.random.uniform(0, 5)  # Initial Expected LR

            for q_idx, quarter in enumerate(QUARTERS):
                ytd_pct = (q_idx + 1) * 0.25

                # YTD actual
                actual_gwp = plan_gwp * ytd_pct * np.random.uniform(0.85, 1.15)
                actual_nep = actual_gwp * np.random.uniform(0.85, 0.95)

                # ULR development (can deteriorate through year)
                ulr_drift = np.random.uniform(-8, 12)
                actual_ulr = plan_ulr + ulr_drift + (q_idx * np.random.uniform(-1, 3))

                # Ultimate loss (NEP * ULR)
                plan_ult_loss = plan_nep * (plan_ulr / 100)
                actual_ult_loss = actual_nep * (actual_ulr / 100)

                # Prior year development (positive = adverse)
                prior_year_dev = np.random.uniform(-3, 5)

                # Status based on ULR variance
                ulr_variance = actual_ulr - plan_ulr
                if ulr_variance < 3:
                    status = 'On Track'
                elif ulr_variance < 7:
                    status = 'Monitor'
                elif ulr_variance < 12:
                    status = 'Concern'
                else:
                    status = 'Action Required'

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'Risk_Code': risk_code,
                    'Risk_Name': risk_name,
                    # SBF Plan (full year)
                    'Plan_GWP_GBP_M': round(plan_gwp, 2),
                    'Plan_NEP_GBP_M': round(plan_nep, 2),
                    'Plan_IELR_Pct': round(plan_ielr, 1),
                    'Plan_ULR_Pct': round(plan_ulr, 1),
                    'Plan_Ultimate_Loss_GBP_M': round(plan_ult_loss, 2),
                    # YTD Actual
                    'YTD_GWP_GBP_M': round(actual_gwp, 2),
                    'YTD_NEP_GBP_M': round(actual_nep, 2),
                    'Actual_ULR_Pct': round(actual_ulr, 1),
                    'Actual_Ultimate_Loss_GBP_M': round(actual_ult_loss, 2),
                    # Variance and development
                    'GWP_Variance_Pct': round(((actual_gwp / (plan_gwp * ytd_pct)) - 1) * 100, 1) if plan_gwp * ytd_pct > 0 else 0,
                    'ULR_Variance_Pct': round(ulr_variance, 1),
                    'Prior_Year_Dev_Pct': round(prior_year_dev, 1),
                    # Status
                    'Performance_Status': status,
                    'Currency': CURRENCY
                })
    return pd.DataFrame(records)

# =============================================================================
# QMB_030_ULR_Movement - Ultimate Loss Ratio movement analysis
# =============================================================================
def generate_qmb_030_ulr_movement():
    records = []

    for syn in SYNDICATES:
        num_classes = np.random.randint(8, 15)
        syn_classes = np.random.choice(len(RISK_CODES), num_classes, replace=False)

        for class_idx in syn_classes:
            risk_code, risk_name = RISK_CODES[class_idx]

            # Starting ULR (beginning of year)
            opening_ulr = np.random.uniform(55, 75)

            for q_idx, quarter in enumerate(QUARTERS):
                # ULR movements during quarter
                large_loss = np.random.uniform(0, 5) if np.random.random() < 0.3 else 0
                cat_loss = np.random.uniform(0, 3) if np.random.random() < 0.2 else 0
                attritional = np.random.uniform(-2, 3)
                reserve_movement = np.random.uniform(-3, 4)
                rate_change_impact = np.random.uniform(-2, 1)
                mix_change = np.random.uniform(-1, 1)

                # Calculate closing ULR
                total_movement = large_loss + cat_loss + attritional + reserve_movement + rate_change_impact + mix_change
                closing_ulr = opening_ulr + total_movement

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'Risk_Code': risk_code,
                    'Risk_Name': risk_name,
                    'Opening_ULR_Pct': round(opening_ulr, 1),
                    # Movement components
                    'Large_Loss_Impact_Pct': round(large_loss, 1),
                    'Cat_Loss_Impact_Pct': round(cat_loss, 1),
                    'Attritional_Movement_Pct': round(attritional, 1),
                    'Reserve_Development_Pct': round(reserve_movement, 1),
                    'Rate_Change_Impact_Pct': round(rate_change_impact, 1),
                    'Mix_Change_Impact_Pct': round(mix_change, 1),
                    'Total_Movement_Pct': round(total_movement, 1),
                    'Closing_ULR_Pct': round(closing_ulr, 1),
                    'Currency': CURRENCY
                })

                # Closing becomes next quarter's opening
                opening_ulr = closing_ulr

    return pd.DataFrame(records)

# =============================================================================
# QMB_040_Premium_Movement - Premium vs plan tracking
# =============================================================================
def generate_qmb_040_premium_movement():
    records = []

    for syn in SYNDICATES:
        num_classes = np.random.randint(8, 15)
        syn_classes = np.random.choice(len(RISK_CODES), num_classes, replace=False)

        for class_idx in syn_classes:
            risk_code, risk_name = RISK_CODES[class_idx]

            # SBF plan premium (annual)
            plan_gwp = np.random.uniform(15, 80)

            for q_idx, quarter in enumerate(QUARTERS):
                ytd_pct = (q_idx + 1) * 0.25

                # Plan YTD (even distribution assumed)
                plan_ytd = plan_gwp * ytd_pct

                # Actual with variance
                actual_ytd = plan_ytd * np.random.uniform(0.85, 1.15)

                # Components of variance
                new_business = (actual_ytd - plan_ytd) * np.random.uniform(0.3, 0.5) if actual_ytd > plan_ytd else 0
                lost_business = (plan_ytd - actual_ytd) * np.random.uniform(0.3, 0.5) if actual_ytd < plan_ytd else 0
                rate_change = (actual_ytd - plan_ytd) * np.random.uniform(0.2, 0.4)
                timing_diff = (actual_ytd - plan_ytd) - new_business + lost_business - rate_change

                # Project full year based on run rate
                if ytd_pct > 0:
                    projected_fy = actual_ytd / ytd_pct
                else:
                    projected_fy = plan_gwp

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'Risk_Code': risk_code,
                    'Risk_Name': risk_name,
                    # Plan vs Actual
                    'Plan_FY_GWP_GBP_M': round(plan_gwp, 2),
                    'Plan_YTD_GWP_GBP_M': round(plan_ytd, 2),
                    'Actual_YTD_GWP_GBP_M': round(actual_ytd, 2),
                    'Variance_GBP_M': round(actual_ytd - plan_ytd, 2),
                    'Variance_Pct': round(((actual_ytd / plan_ytd) - 1) * 100, 1) if plan_ytd > 0 else 0,
                    # Variance components
                    'New_Business_GBP_M': round(new_business, 2),
                    'Lost_Business_GBP_M': round(lost_business, 2),
                    'Rate_Change_GBP_M': round(rate_change, 2),
                    'Timing_Diff_GBP_M': round(timing_diff, 2),
                    # Projection
                    'Projected_FY_GWP_GBP_M': round(projected_fy, 2),
                    'Projected_vs_Plan_Pct': round(((projected_fy / plan_gwp) - 1) * 100, 1),
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# QMB_050_Rate_Adequacy - Rate change and adequacy monitoring
# =============================================================================
def generate_qmb_050_rate_adequacy():
    records = []

    for syn in SYNDICATES:
        num_classes = np.random.randint(8, 15)
        syn_classes = np.random.choice(len(RISK_CODES), num_classes, replace=False)

        for class_idx in syn_classes:
            risk_code, risk_name = RISK_CODES[class_idx]

            # SBF assumed rate change
            plan_rate_change = np.random.uniform(-2, 8)

            for quarter in QUARTERS:
                # Actual rate achieved
                actual_rate_change = plan_rate_change * np.random.uniform(0.7, 1.3) + np.random.uniform(-2, 2)

                # RARC (Risk Adjusted Rate Change) - accounting for exposure changes
                exposure_change = np.random.uniform(-3, 3)
                rarc = actual_rate_change - exposure_change

                # Required rate change to hit target ULR
                required_rate = np.random.uniform(2, 10)

                # Adequacy assessment
                rate_gap = actual_rate_change - required_rate
                if rate_gap >= 0:
                    adequacy_status = 'Adequate'
                elif rate_gap >= -3:
                    adequacy_status = 'Marginal'
                else:
                    adequacy_status = 'Inadequate'

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'Risk_Code': risk_code,
                    'Risk_Name': risk_name,
                    # Rate change analysis
                    'Plan_Rate_Change_Pct': round(plan_rate_change, 1),
                    'Actual_Rate_Change_Pct': round(actual_rate_change, 1),
                    'Exposure_Change_Pct': round(exposure_change, 1),
                    'RARC_Pct': round(rarc, 1),
                    # Adequacy
                    'Required_Rate_Change_Pct': round(required_rate, 1),
                    'Rate_Gap_Pct': round(rate_gap, 1),
                    'Adequacy_Status': adequacy_status,
                    # Cumulative
                    'Cumulative_Rate_Change_3Yr_Pct': round(actual_rate_change * 3 + np.random.uniform(-5, 10), 1),
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# QMB_060_Early_Warning - Classes flagged for attention
# =============================================================================
def generate_qmb_060_early_warning():
    records = []

    warning_types = [
        ('ULR_DETERIORATION', 'ULR deteriorating vs plan'),
        ('RATE_INADEQUATE', 'Rate change below required'),
        ('VOLUME_OVERRUN', 'Premium volume exceeds plan significantly'),
        ('VOLUME_SHORTFALL', 'Premium volume below plan significantly'),
        ('LARGE_LOSS', 'Large loss activity above expected'),
        ('CAT_EXPOSURE', 'Cat exposure increasing'),
        ('PRIOR_YEAR_DEV', 'Adverse prior year development'),
        ('MIX_SHIFT', 'Business mix shifting unfavorably')
    ]

    for syn in SYNDICATES:
        for quarter in QUARTERS:
            # Generate 2-5 warnings per syndicate per quarter
            num_warnings = np.random.randint(2, 6)

            for _ in range(num_warnings):
                risk_code, risk_name = RISK_CODES[np.random.randint(0, len(RISK_CODES))]
                warning_type, warning_desc = warning_types[np.random.randint(0, len(warning_types))]

                # Severity
                severity = np.random.choice(['Low', 'Medium', 'High', 'Critical'], p=[0.3, 0.4, 0.2, 0.1])

                # Financial impact
                if severity == 'Critical':
                    impact = np.random.uniform(5, 20)
                elif severity == 'High':
                    impact = np.random.uniform(2, 8)
                elif severity == 'Medium':
                    impact = np.random.uniform(0.5, 3)
                else:
                    impact = np.random.uniform(0.1, 1)

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'Risk_Code': risk_code,
                    'Risk_Name': risk_name,
                    'Warning_Type': warning_type,
                    'Warning_Description': warning_desc,
                    'Severity': severity,
                    'Estimated_Impact_GBP_M': round(impact, 2),
                    'Impact_On_ULR_Pct': round(impact / np.random.uniform(50, 150) * 100, 1),
                    'Action_Required': 'Yes' if severity in ['High', 'Critical'] else 'No',
                    'Status': np.random.choice(['New', 'Under Review', 'Action Taken', 'Resolved']),
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# QMB_070_Prior_Year_Development - Prior year reserve movements
# =============================================================================
def generate_qmb_070_prior_year_development():
    records = []
    prior_years = [2019, 2020, 2021, 2022, 2023]

    for syn in SYNDICATES:
        for quarter in QUARTERS:
            for py in prior_years:
                # Development direction tends to be consistent
                base_dev = np.random.uniform(-5, 8)  # Syndicate tendency

                # Development amount
                dev_pct = base_dev + np.random.uniform(-2, 2)
                original_ult = np.random.uniform(50, 200)
                dev_amount = original_ult * (dev_pct / 100)

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'Prior_Year': py,
                    'Years_Developed': REPORTING_YEAR - py,
                    'Opening_Ultimate_GBP_M': round(original_ult, 2),
                    'Development_GBP_M': round(dev_amount, 2),
                    'Development_Pct': round(dev_pct, 1),
                    'Closing_Ultimate_GBP_M': round(original_ult + dev_amount, 2),
                    'Development_Type': 'Adverse' if dev_amount > 0 else 'Favorable',
                    'Cumulative_Dev_Since_Close_Pct': round(dev_pct * (REPORTING_YEAR - py) * 0.3, 1),
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# QMB_080_Action_Tracker - Management actions and status
# =============================================================================
def generate_qmb_080_action_tracker():
    records = []

    action_types = [
        'Rate increase mandate',
        'Portfolio review',
        'Exposure reduction',
        'Reinsurance purchase',
        'Reserve strengthening',
        'Underwriting guideline update',
        'Class exit consideration',
        'New business hold'
    ]

    for syn in SYNDICATES:
        # 3-8 actions per syndicate
        num_actions = np.random.randint(3, 9)

        for action_id in range(1, num_actions + 1):
            risk_code, risk_name = RISK_CODES[np.random.randint(0, len(RISK_CODES))]
            action = np.random.choice(action_types)

            # Random quarter when action was raised
            raised_quarter = np.random.choice(QUARTERS)

            # Status progression
            q_idx = QUARTERS.index(raised_quarter)
            if q_idx == 3:
                status = np.random.choice(['Open', 'In Progress'])
            else:
                status = np.random.choice(['Open', 'In Progress', 'Complete', 'Closed'], p=[0.1, 0.3, 0.4, 0.2])

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Action_ID': f'{syn}_{REPORTING_YEAR}_{action_id:03d}',
                'Risk_Code': risk_code,
                'Risk_Name': risk_name,
                'Action_Type': action,
                'Raised_Quarter': raised_quarter,
                'Target_Completion': QUARTERS[min(q_idx + 1, 3)],
                'Status': status,
                'Owner': f'Underwriter_{np.random.randint(1, 20)}',
                'Expected_Impact_GBP_M': round(np.random.uniform(0.5, 5), 2),
                'Actual_Impact_GBP_M': round(np.random.uniform(0.3, 4), 2) if status in ['Complete', 'Closed'] else None,
                'Comments': f'Action raised due to {"adverse" if np.random.random() < 0.5 else "concerning"} performance trends',
                'Currency': CURRENCY
            })

    return pd.DataFrame(records)

# =============================================================================
# Generate all tables
# =============================================================================

# Control
QMB_001_Control = generate_qmb_001_control()

# Performance analysis
QMB_010_Performance_Summary = generate_qmb_010_performance_summary()
QMB_020_Class_Performance = generate_qmb_020_class_performance()
QMB_030_ULR_Movement = generate_qmb_030_ulr_movement()
QMB_040_Premium_Movement = generate_qmb_040_premium_movement()
QMB_050_Rate_Adequacy = generate_qmb_050_rate_adequacy()

# Monitoring and actions
QMB_060_Early_Warning = generate_qmb_060_early_warning()
QMB_070_Prior_Year_Development = generate_qmb_070_prior_year_development()
QMB_080_Action_Tracker = generate_qmb_080_action_tracker()

# Summary statistics
print("=" * 70)
print("QMB - Quarterly Monitoring Part B (Performance) Data Generator")
print("=" * 70)
print(f"QMB_001_Control: {len(QMB_001_Control)} rows")
print(f"QMB_010_Performance_Summary: {len(QMB_010_Performance_Summary)} rows")
print(f"QMB_020_Class_Performance: {len(QMB_020_Class_Performance)} rows")
print(f"QMB_030_ULR_Movement: {len(QMB_030_ULR_Movement)} rows")
print(f"QMB_040_Premium_Movement: {len(QMB_040_Premium_Movement)} rows")
print(f"QMB_050_Rate_Adequacy: {len(QMB_050_Rate_Adequacy)} rows")
print(f"QMB_060_Early_Warning: {len(QMB_060_Early_Warning)} rows")
print(f"QMB_070_Prior_Year_Development: {len(QMB_070_Prior_Year_Development)} rows")
print(f"QMB_080_Action_Tracker: {len(QMB_080_Action_Tracker)} rows")
print("=" * 70)
print("QMB data generated successfully!")
