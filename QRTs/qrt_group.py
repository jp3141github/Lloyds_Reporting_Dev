"""
PRA/BoE QRT Generator - Group Templates (IR32-35)
=================================================
Actuarial-focused group reporting templates for Solvency II reporting.

Templates:
- IR3201: Undertakings in the Scope of the Group
- IR3301: Insurance and Reinsurance Individual Requirements
- IR3401: Other Regulated and Non-Regulated Financial Undertakings
- IR3501: Contribution to Group Technical Provisions
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random
from typing import Dict, List

from .qrt_balance_sheet import (
    UNDERTAKINGS, REPORTING_DATE, COUNTRIES,
    random_amount, random_percentage, generate_lei
)

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


# ============================================================================
# IR3201 - Undertakings in the Scope of the Group
# ============================================================================

def generate_ir3201_group_scope():
    """
    IR3201 - Undertakings in the Scope of the Group
    List of all undertakings within the group scope.
    """
    data = []

    group_entities = [
        ('Insurance', 'UK Subsidiary', 'GB', 100, 'Full'),
        ('Insurance', 'US Branch', 'US', 100, 'Full'),
        ('Insurance', 'German Subsidiary', 'DE', 100, 'Full'),
        ('Insurance', 'French Subsidiary', 'FR', 80, 'Proportional'),
        ('Insurance', 'Irish Subsidiary', 'IE', 60, 'Proportional'),
        ('Reinsurance', 'Bermuda Reinsurer', 'BM', 100, 'Full'),
        ('Reinsurance', 'Luxembourg Reinsurer', 'LU', 75, 'Proportional'),
        ('Holding', 'Parent Holding Co', 'GB', 100, 'Full'),
        ('Asset Manager', 'Investment Manager', 'GB', 100, 'Sectoral Rules'),
        ('Service Company', 'Services Ltd', 'GB', 100, 'Full'),
    ]

    for undertaking in UNDERTAKINGS[:2]:  # Just for top 2 groups
        for entity_type, entity_name, country, ownership, consolidation in group_entities:
            row = {
                'Group_LEI': undertaking['lei'],
                'Group_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Entity_LEI': generate_lei(),
                'Entity_Name': f"{undertaking['name']} - {entity_name}",
                'Entity_Type': entity_type,
                'Country_Of_Incorporation': country,
                'Supervisory_Authority': 'PRA' if country == 'GB' else f'{country} Regulator',
                'Ownership_Percentage': ownership,
                'Voting_Rights': ownership,
                'Consolidation_Method': consolidation,
                'Inclusion_In_Group_SCR': 'Yes' if consolidation in ['Full', 'Proportional'] else 'No',
                'Solvency_Regime': 'Solvency II' if country in ['GB', 'DE', 'FR', 'IE', 'LU'] else 'Equivalent',
                'Total_Assets': random_amount(50_000_000, 500_000_000),
                'Total_Liabilities': random_amount(30_000_000, 400_000_000),
                'Own_Funds': random_amount(20_000_000, 150_000_000),
                'SCR': random_amount(10_000_000, 100_000_000),
                'MCR': random_amount(3_000_000, 35_000_000),
                'Eligible_OF_For_Group': random_amount(15_000_000, 120_000_000),
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR3301 - Insurance and Reinsurance Individual Requirements
# ============================================================================

def generate_ir3301_individual_requirements():
    """
    IR3301 - Insurance and Reinsurance Individual Requirements
    Individual capital requirements for each group entity.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        entities = [
            ('Solo Entity', 100),
            ('UK Subsidiary', 100),
            ('US Branch', 100),
            ('European Subsidiary', 80),
            ('Reinsurance Subsidiary', 100),
        ]

        for entity_name, ownership in entities:
            scr = random_amount(20_000_000, 150_000_000)
            mcr = scr * np.random.uniform(0.25, 0.35)
            of = scr * np.random.uniform(1.20, 1.80)

            row = {
                'Group_LEI': undertaking['lei'],
                'Group_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Entity_LEI': generate_lei(),
                'Entity_Name': f"{undertaking['name']} - {entity_name}",
                'Ownership_Percentage': ownership,
                # Own Funds
                'Tier_1_Unrestricted': of * np.random.uniform(0.70, 0.85),
                'Tier_1_Restricted': of * np.random.uniform(0.05, 0.10),
                'Tier_2': of * np.random.uniform(0.05, 0.15),
                'Tier_3': of * np.random.uniform(0, 0.05),
                'Total_Own_Funds': of,
                'Eligible_OF_For_SCR': of,
                'Eligible_OF_For_MCR': of * np.random.uniform(0.90, 0.98),
                # Capital Requirements
                'SCR': scr,
                'MCR': mcr,
                # Ratios
                'SCR_Ratio': round(of / scr * 100, 2),
                'MCR_Ratio': round(of * 0.95 / mcr * 100, 2),
                # Contribution to Group
                'Contribution_To_Group_OF': of * ownership / 100,
                'Contribution_To_Group_SCR': scr * ownership / 100,
                # Status
                'Solvency_Status': 'Compliant' if of / scr > 1.0 else 'Non-Compliant',
                'MCR_Status': 'Compliant' if of * 0.95 / mcr > 1.0 else 'Non-Compliant',
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR3401 - Other Regulated and Non-Regulated Financial Undertakings
# ============================================================================

def generate_ir3401_other_undertakings():
    """
    IR3401 - Other Regulated and Non-Regulated Financial Undertakings
    Capital requirements for non-insurance financial entities in the group.
    """
    data = []

    other_entities = [
        ('Bank', 'Banking Subsidiary', 'GB', 'CRD IV/CRR'),
        ('Asset Manager', 'Investment Management Co', 'GB', 'MIFID II'),
        ('Pension Trustee', 'Staff Pension Trustee', 'GB', 'IORP II'),
        ('SPV', 'Securitisation Vehicle', 'IE', 'Securitisation Regulation'),
        ('Holding', 'Intermediate Holding Co', 'LU', 'None'),
        ('Service Company', 'Group Services Ltd', 'GB', 'None'),
    ]

    for undertaking in UNDERTAKINGS[:3]:
        for entity_type, entity_name, country, regime in other_entities:
            capital_req = random_amount(5_000_000, 50_000_000) if regime != 'None' else 0
            own_funds = capital_req * np.random.uniform(1.10, 1.50) if capital_req > 0 else random_amount(1_000_000, 10_000_000)

            row = {
                'Group_LEI': undertaking['lei'],
                'Group_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Entity_LEI': generate_lei(),
                'Entity_Name': f"{undertaking['name']} - {entity_name}",
                'Entity_Type': entity_type,
                'Country': country,
                'Regulatory_Regime': regime,
                'Ownership_Percentage': random.choice([100, 100, 100, 80, 75, 60]),
                'Total_Assets': random_amount(20_000_000, 200_000_000),
                'Total_Liabilities': random_amount(10_000_000, 150_000_000),
                'Own_Funds': own_funds,
                'Sectoral_Capital_Requirement': capital_req,
                'Surplus_Deficit': own_funds - capital_req,
                'Contribution_To_Group_OF': own_funds * np.random.uniform(0.80, 1.0),
                'Contribution_To_Group_SCR': capital_req,
                'Deduction_From_Group_OF': random_amount(0, 5_000_000),
                'Treatment_In_Group_Solvency': 'Sectoral Rules' if regime != 'None' else 'Deduction',
            }
            data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# IR3501 - Contribution to Group Technical Provisions
# ============================================================================

def generate_ir3501_group_tp_contribution():
    """
    IR3501 - Contribution to Group Technical Provisions
    Technical provisions contribution from each group entity.
    """
    data = []

    for undertaking in UNDERTAKINGS:
        entities = [
            ('Solo Entity', 100, 'Non-Life'),
            ('UK Subsidiary', 100, 'Non-Life'),
            ('Life Subsidiary', 100, 'Life'),
            ('European Branch', 80, 'Non-Life'),
            ('Reinsurance Entity', 100, 'Reinsurance'),
        ]

        for entity_name, ownership, business_type in entities:
            if business_type == 'Life':
                tp = random_amount(50_000_000, 300_000_000)
            else:
                tp = random_amount(100_000_000, 500_000_000)

            bel = tp * np.random.uniform(0.90, 0.96)
            rm = tp - bel

            row = {
                'Group_LEI': undertaking['lei'],
                'Group_Name': undertaking['name'],
                'Reporting_Date': REPORTING_DATE,
                'Entity_LEI': generate_lei(),
                'Entity_Name': f"{undertaking['name']} - {entity_name}",
                'Business_Type': business_type,
                'Ownership_Percentage': ownership,
                # Gross TP
                'Gross_TP': tp,
                'Gross_BEL': bel,
                'Gross_Risk_Margin': rm,
                # Reinsurance Recoverables
                'RI_Recoverables_BEL': bel * np.random.uniform(0.10, 0.25),
                'RI_Recoverables_RM': rm * np.random.uniform(0.05, 0.15),
                'Total_RI_Recoverables': (bel + rm) * np.random.uniform(0.10, 0.23),
                # Net TP
                'Net_TP': tp * np.random.uniform(0.75, 0.88),
                'Net_BEL': bel * np.random.uniform(0.75, 0.90),
                'Net_Risk_Margin': rm * np.random.uniform(0.85, 0.95),
                # Contribution
                'Contribution_Percentage': ownership,
                'Contribution_To_Group_Gross_TP': tp * ownership / 100,
                'Contribution_To_Group_Net_TP': tp * np.random.uniform(0.75, 0.88) * ownership / 100,
                'Contribution_To_Group_RM': rm * ownership / 100,
                # Intra-Group Eliminations
                'Intra_Group_RI_Ceded': random_amount(0, tp * 0.15),
                'Intra_Group_RI_Assumed': random_amount(0, tp * 0.10),
                'Net_Intra_Group': random_amount(-tp * 0.05, tp * 0.05),
            }
            data.append(row)

    return pd.DataFrame(data)


# Export all functions
__all__ = [
    'generate_ir3201_group_scope',
    'generate_ir3301_individual_requirements',
    'generate_ir3401_other_undertakings',
    'generate_ir3501_group_tp_contribution',
]
