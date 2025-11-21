"""
Power BI Integration Script for Lloyd's Synthetic Data
=======================================================
This script is designed to be used directly in Power BI's Python script data source.

HOW TO USE IN POWER BI:
-----------------------
1. Open Power BI Desktop
2. Get Data -> More -> Python script
3. Copy and paste this entire script
4. Click OK
5. Power BI will show available tables: syndicate_master, scr_impact_data, loss_ratio_data
6. Select the tables you want to import

CUSTOMIZATION:
--------------
- Change num_syndicates to generate more/fewer syndicates
- Change seed value for different random data
- Adjust date ranges in the generation functions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def set_random_seed(seed=42):
    """Set random seed for reproducibility"""
    random.seed(seed)
    np.random.seed(seed)


def generate_syndicate_master(num_syndicates=20):
    """Generate master list of Lloyd's syndicates"""
    syndicate_numbers = [
        2001, 2003, 2010, 2014, 2020, 2025, 2030, 2035, 2040, 2050,
        2988, 3000, 3010, 3020, 3500, 4000, 4001, 5000, 5001, 5500,
        6000, 6100, 6200, 1176, 1200, 1234, 2791, 2987, 3624, 4242
    ][:num_syndicates]

    syndicate_names = [
        "Global Property & Casualty", "Marine & Energy", "Professional Indemnity",
        "Reinsurance Division", "Aviation Underwriters", "Cyber & Technology",
        "Political Risk & Credit", "Specialty Lines", "Catastrophe Re",
        "Lloyd's Core Consortium", "Treaty Reinsurance", "Casualty Direct",
        "Motor & Transport", "Trade Credit", "Medical Malpractice",
        "D&O and Financial Lines", "Property Facultative", "Energy Offshore",
        "Aerospace", "Marine Hull", "Marine Cargo", "Construction & Engineering",
        "Terrorism Re", "Parametric Solutions", "Agriculture", "Life Re",
        "Warranty & Indemnity", "Environmental Liability", "Bloodstock & Livestock",
        "Fine Art & Specie"
    ][:num_syndicates]

    managing_agents = [
        f"Managing Agent {chr(65 + i % 26)}{chr(65 + (i // 26) % 26)}"
        for i in range(num_syndicates)
    ]

    business_classes = [
        "Property", "Marine", "Professional Indemnity", "Reinsurance", "Aviation",
        "Cyber", "Political Risk", "Specialty", "Catastrophe", "Multi-class"
    ]

    df = pd.DataFrame({
        'SyndicateNumber': syndicate_numbers,
        'SyndicateName': syndicate_names,
        'ManagingAgent': managing_agents,
        'PrimaryBusinessClass': [random.choice(business_classes) for _ in range(num_syndicates)],
        'YearOfAccount': [2025] * num_syndicates,
        'Active': [True] * num_syndicates,
        'StampCapacity_GBPm': np.random.uniform(50, 2000, num_syndicates).round(1)
    })

    return df


def generate_scr_impact_data(syndicates_df):
    """Generate SCR impact data showing uSCR and 1SCR changes"""
    records = []

    for _, syndicate in syndicates_df.iterrows():
        syndicate_no = syndicate['SyndicateNumber']
        capacity = syndicate['StampCapacity_GBPm']

        base_uscr = capacity * np.random.uniform(0.35, 0.50)
        base_1scr = base_uscr * np.random.uniform(0.85, 0.95)

        records.append({
            'SyndicateNumber': syndicate_no,
            'SubmissionType': 'Latest LCR',
            'SBFVersion': 'LCR_2024_v1',
            'SubmissionDate': datetime(2024, 10, 15) + timedelta(days=random.randint(0, 30)),
            'uSCR_GBPm': round(base_uscr, 2),
            '1SCR_GBPm': round(base_1scr, 2),
            'SCR_Ratio': round(base_1scr / base_uscr, 4)
        })

        sbf_uscr = base_uscr * np.random.uniform(0.98, 1.08)
        sbf_1scr = base_1scr * np.random.uniform(0.98, 1.08)

        records.append({
            'SyndicateNumber': syndicate_no,
            'SubmissionType': 'Latest SBF',
            'SBFVersion': 'SBF_2025_v2',
            'SubmissionDate': datetime(2025, 1, 15) + timedelta(days=random.randint(0, 30)),
            'uSCR_GBPm': round(sbf_uscr, 2),
            '1SCR_GBPm': round(sbf_1scr, 2),
            'SCR_Ratio': round(sbf_1scr / sbf_uscr, 4)
        })

        movement_uscr = sbf_uscr - base_uscr
        movement_1scr = sbf_1scr - base_1scr

        records.append({
            'SyndicateNumber': syndicate_no,
            'SubmissionType': 'Movement',
            'SBFVersion': 'Delta',
            'SubmissionDate': datetime(2025, 1, 15),
            'uSCR_GBPm': round(movement_uscr, 2),
            '1SCR_GBPm': round(movement_1scr, 2),
            'SCR_Ratio': round((movement_1scr / movement_uscr) if movement_uscr != 0 else 0, 4)
        })

        movement_pct_uscr = (movement_uscr / base_uscr * 100) if base_uscr != 0 else 0
        movement_pct_1scr = (movement_1scr / base_1scr * 100) if base_1scr != 0 else 0

        records.append({
            'SyndicateNumber': syndicate_no,
            'SubmissionType': 'Movement %',
            'SBFVersion': 'Delta %',
            'SubmissionDate': datetime(2025, 1, 15),
            'uSCR_GBPm': round(movement_pct_uscr, 2),
            '1SCR_GBPm': round(movement_pct_1scr, 2),
            'SCR_Ratio': None
        })

    return pd.DataFrame(records)


def generate_loss_ratio_data(syndicates_df):
    """Generate loss ratio data (Plan vs Modelled, Net Net basis)"""
    records = []

    for _, syndicate in syndicates_df.iterrows():
        syndicate_no = syndicate['SyndicateNumber']
        business_class = syndicate['PrimaryBusinessClass']

        base_loss_ratios = {
            'Property': (0.65, 0.72),
            'Marine': (0.68, 0.75),
            'Professional Indemnity': (0.70, 0.78),
            'Reinsurance': (0.72, 0.80),
            'Aviation': (0.66, 0.73),
            'Cyber': (0.62, 0.70),
            'Political Risk': (0.60, 0.68),
            'Specialty': (0.65, 0.73),
            'Catastrophe': (0.55, 0.65),
            'Multi-class': (0.67, 0.74)
        }

        plan_base, model_base = base_loss_ratios.get(business_class, (0.65, 0.72))

        # (A) 2024 LCR submission
        plan_2024 = plan_base + np.random.uniform(-0.03, 0.03)
        model_2024 = model_base + np.random.uniform(-0.03, 0.03)
        self_uplift_2024 = model_2024 - plan_2024

        records.append({
            'SyndicateNumber': syndicate_no,
            'RowLabel': '(A) 2024: LCR submission',
            'ReportingPeriod': '2024 YOA',
            'SubmissionDate': datetime(2024, 10, 1),
            'PlanLossRatio_NetNet': round(plan_2024, 4),
            'ModelledLossRatio_NetNet': round(model_2024, 4),
            'SelfUplift_pct': round(self_uplift_2024 * 100, 2),
            'SyndicateComments': 'Initial 2024 YOA submission'
        })

        # (B) 2025 LCR submission
        plan_2025_lcr = plan_2024 + np.random.uniform(-0.02, 0.04)
        model_2025_lcr = model_2024 + np.random.uniform(-0.02, 0.04)
        self_uplift_2025_lcr = model_2025_lcr - plan_2025_lcr

        records.append({
            'SyndicateNumber': syndicate_no,
            'RowLabel': '(B) 2025: LCR submission',
            'ReportingPeriod': '2025 YOA',
            'SubmissionDate': datetime(2025, 10, 1),
            'PlanLossRatio_NetNet': round(plan_2025_lcr, 4),
            'ModelledLossRatio_NetNet': round(model_2025_lcr, 4),
            'SelfUplift_pct': round(self_uplift_2025_lcr * 100, 2),
            'SyndicateComments': 'Initial 2025 YOA submission'
        })

        # (C) 2025 Updated for resubmitted SBF
        plan_increase = np.random.uniform(0.01, 0.05)
        plan_2025_sbf = plan_2025_lcr + plan_increase
        model_adjustment = np.random.uniform(0.005, 0.04)
        model_2025_sbf = model_2025_lcr + model_adjustment

        if model_2025_sbf < plan_2025_sbf:
            model_2025_sbf = plan_2025_sbf + np.random.uniform(0.01, 0.03)
            comment = 'Modelled LR adjusted to align with increased plan'
        else:
            comment = 'Plan increase driven by pricing environment'

        self_uplift_2025_sbf = model_2025_sbf - plan_2025_sbf

        records.append({
            'SyndicateNumber': syndicate_no,
            'RowLabel': '(C) 2025: Updated for resubmitted SBF',
            'ReportingPeriod': '2025 YOA',
            'SubmissionDate': datetime(2025, 11, 15),
            'PlanLossRatio_NetNet': round(plan_2025_sbf, 4),
            'ModelledLossRatio_NetNet': round(model_2025_sbf, 4),
            'SelfUplift_pct': round(self_uplift_2025_sbf * 100, 2),
            'SyndicateComments': comment
        })

        # (D) Movement
        plan_movement = plan_2025_sbf - plan_2024
        model_movement = model_2025_sbf - model_2024
        uplift_movement = self_uplift_2025_sbf - self_uplift_2024

        if uplift_movement < -0.01:
            movement_comment = 'Self-uplift decrease reflects market hardening'
        else:
            movement_comment = 'Movement within expected range'

        records.append({
            'SyndicateNumber': syndicate_no,
            'RowLabel': '(D) Movement: (C) - (A)',
            'ReportingPeriod': 'Delta',
            'SubmissionDate': datetime(2025, 11, 15),
            'PlanLossRatio_NetNet': round(plan_movement, 4),
            'ModelledLossRatio_NetNet': round(model_movement, 4),
            'SelfUplift_pct': round(uplift_movement * 100, 2),
            'SyndicateComments': movement_comment
        })

    return pd.DataFrame(records)


# ============================================================================
# MAIN EXECUTION - This runs when script is loaded in Power BI
# ============================================================================

# Set parameters here
NUM_SYNDICATES = 25
RANDOM_SEED = 42

# Initialize random seed
set_random_seed(RANDOM_SEED)

# Generate all data tables
syndicate_master = generate_syndicate_master(NUM_SYNDICATES)
scr_impact_data = generate_scr_impact_data(syndicate_master)
loss_ratio_data = generate_loss_ratio_data(syndicate_master)

# Power BI will automatically detect these DataFrames and make them available
# as separate tables to import
print(f"Generated {len(syndicate_master)} syndicates")
print(f"Generated {len(scr_impact_data)} SCR impact records")
print(f"Generated {len(loss_ratio_data)} loss ratio records")
