"""
Lloyd's of London Synthetic Data Generator
===========================================
This script generates synthetic SCR (Solvency Capital Requirement) data
for Lloyd's syndicates, matching the structure of the SCR SBF template.

Output Tables:
1. scr_impact_data: Impact on uSCR and 1SCR metrics
2. loss_ratio_data: Plan vs Modelled loss ratios
3. syndicate_master: Syndicate reference data

Usage:
    python generate_lloyds_synthetic_data.py

    Or import as a module:
    from generate_lloyds_synthetic_data import generate_all_data
    data = generate_all_data(num_syndicates=20, seed=42)
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
    """
    Generate master list of Lloyd's syndicates with reference data

    Returns:
        DataFrame with syndicate reference information
    """
    # Realistic Lloyd's syndicate numbers (typically 4 digits, some 3 digits)
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


def generate_scr_impact_data(syndicates_df, num_versions_per_syndicate=3):
    """
    Generate SCR impact data showing uSCR and 1SCR changes

    Returns:
        DataFrame with SCR impact metrics
    """
    records = []

    for _, syndicate in syndicates_df.iterrows():
        syndicate_no = syndicate['SyndicateNumber']
        capacity = syndicate['StampCapacity_GBPm']

        # Base SCR values (typically 35-50% of stamp capacity)
        base_uscr = capacity * np.random.uniform(0.35, 0.50)
        base_1scr = base_uscr * np.random.uniform(0.85, 0.95)  # 1SCR typically lower than uSCR

        # Latest LCR submission
        records.append({
            'SyndicateNumber': syndicate_no,
            'SubmissionType': 'Latest LCR',
            'SBFVersion': 'LCR_2024_v1',
            'SubmissionDate': datetime(2024, 10, 15) + timedelta(days=random.randint(0, 30)),
            'uSCR_GBPm': round(base_uscr, 2),
            '1SCR_GBPm': round(base_1scr, 2),
            'SCR_Ratio': round(base_1scr / base_uscr, 4)
        })

        # Latest SBF submission (with some variation)
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

        # Calculate movements
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

        # Movement percentage
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

    df = pd.DataFrame(records)
    return df


def generate_loss_ratio_data(syndicates_df):
    """
    Generate loss ratio data (Plan vs Modelled, Net Net basis)

    Returns:
        DataFrame with loss ratio validation data
    """
    records = []

    for _, syndicate in syndicates_df.iterrows():
        syndicate_no = syndicate['SyndicateNumber']
        business_class = syndicate['PrimaryBusinessClass']

        # Base loss ratios vary by business class
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

        # (C) 2025 Updated for resubmitted SBF (plan increases by 1-5%)
        plan_increase = np.random.uniform(0.01, 0.05)
        plan_2025_sbf = plan_2025_lcr + plan_increase

        # Model may or may not increase proportionally
        model_adjustment = np.random.uniform(0.005, 0.04)
        model_2025_sbf = model_2025_lcr + model_adjustment

        # Ensure modelled >= plan (per Lloyd's guidance)
        if model_2025_sbf < plan_2025_sbf:
            model_2025_sbf = plan_2025_sbf + np.random.uniform(0.01, 0.03)
            comment = 'Modelled LR adjusted to align with increased plan, reflecting updated risk outlook'
        else:
            comment = 'Plan increase driven by pricing environment; model updated for emerging trends'

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

        # (D) Movement: (C) - (A)
        plan_movement = plan_2025_sbf - plan_2024
        model_movement = model_2025_sbf - model_2024
        uplift_movement = self_uplift_2025_sbf - self_uplift_2024

        if uplift_movement < -0.01:  # Decrease in self-uplift > 1%
            movement_comment = 'Self-uplift decrease reflects market hardening and improved risk selection'
        else:
            movement_comment = 'Movement within expected range based on business plan revisions'

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

    df = pd.DataFrame(records)
    return df


def generate_all_data(num_syndicates=20, seed=42, save_to_csv=False, output_dir='./'):
    """
    Generate all synthetic Lloyd's data tables

    Args:
        num_syndicates: Number of syndicates to generate
        seed: Random seed for reproducibility
        save_to_csv: Whether to save data to CSV files
        output_dir: Directory to save CSV files

    Returns:
        Dictionary containing all generated DataFrames
    """
    set_random_seed(seed)

    print(f"Generating synthetic Lloyd's data for {num_syndicates} syndicates...")

    # Generate data
    syndicate_master = generate_syndicate_master(num_syndicates)
    scr_impact = generate_scr_impact_data(syndicate_master)
    loss_ratio = generate_loss_ratio_data(syndicate_master)

    data = {
        'syndicate_master': syndicate_master,
        'scr_impact_data': scr_impact,
        'loss_ratio_data': loss_ratio
    }

    # Print summary
    print("\n" + "="*60)
    print("DATA GENERATION COMPLETE")
    print("="*60)
    print(f"\nSyndicate Master: {len(syndicate_master)} syndicates")
    print(f"SCR Impact Data: {len(scr_impact)} records")
    print(f"Loss Ratio Data: {len(loss_ratio)} records")

    # Save to CSV if requested
    if save_to_csv:
        import os
        os.makedirs(output_dir, exist_ok=True)

        for name, df in data.items():
            filepath = os.path.join(output_dir, f"{name}.csv")
            df.to_csv(filepath, index=False)
            print(f"\nSaved: {filepath}")

    return data


if __name__ == "__main__":
    # Generate data and save to CSV
    data = generate_all_data(
        num_syndicates=25,
        seed=42,
        save_to_csv=True,
        output_dir='./output'
    )

    # Display sample data
    print("\n" + "="*60)
    print("SAMPLE DATA PREVIEW")
    print("="*60)

    print("\n1. SYNDICATE MASTER (first 5):")
    print(data['syndicate_master'].head())

    print("\n2. SCR IMPACT DATA (first 10):")
    print(data['scr_impact_data'].head(10))

    print("\n3. LOSS RATIO DATA (first 10):")
    print(data['loss_ratio_data'].head(10))
