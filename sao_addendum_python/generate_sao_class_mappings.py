"""
SAO Addendum Return - SAO Class Mappings Data Generator
========================================================
This script generates synthetic Lloyd's of London data for the SAO Class Mappings table.
Maps Signing Actuary Reserving Classes to Lloyd's Lines of Business.
Compatible with Power BI as a Python data source.

Usage in Power BI:
1. Get Data > More > Python script
2. Copy and paste this script
3. Select the 'class_mappings' table

Author: Claude
Date: 2025-11-21
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(456)

def generate_class_mappings_data(num_classes=20):
    """
    Generate synthetic SAO Class Mappings data.

    Maps Signing Actuary Reserving Classes to Lloyd's Lines of Business (Lloyd's LoB).
    Each reserving class can map to up to 4 Lloyd's LoB with associated exposure percentages.

    Parameters:
    -----------
    num_classes : int
        Number of reserving classes to generate

    Returns:
    --------
    pandas.DataFrame
        Synthetic class mappings data
    """

    # Define comprehensive list of Signing Actuary Reserving Classes
    reserving_classes = [
        'Property Treaty', 'Property Direct', 'Property Cat XL', 'Property Facultative',
        'Casualty Treaty', 'Casualty Direct', 'Casualty XL', 'Casualty Facultative',
        'Marine Hull', 'Marine Cargo', 'Marine Liability', 'Marine Energy',
        'Aviation Hull', 'Aviation Liability', 'Aviation Reinsurance',
        'Energy Offshore', 'Energy Onshore', 'Energy Liability',
        'Professional Indemnity', 'D&O US', 'D&O UK', 'D&O Europe',
        'Cyber Direct', 'Cyber Treaty', 'Motor Direct', 'Motor Fleet',
        'Credit & Surety', 'Political Risk', 'Terrorism',
        'Accident & Health', 'Medical Malpractice', 'Product Liability'
    ]

    # Define Lloyd's Lines of Business
    lloyds_lobs = [
        'Property Treaty', 'Property Direct', 'Property Cat XL', 'Property Facultative',
        'Casualty Treaty', 'Casualty Direct', 'D&O', 'Professional Indemnity',
        'Marine Hull', 'Marine Cargo', 'Marine Liability', 'Energy Offshore',
        'Aviation', 'Cyber', 'Motor', 'Credit & Surety',
        'Political Risk', 'Terrorism', 'Accident & Health',
        'Medical Malpractice', 'Product Liability', 'Environmental'
    ]

    # Predefined mappings (some reserving classes map cleanly to one LoB)
    primary_mappings = {
        'Property Treaty': 'Property Treaty',
        'Property Direct': 'Property Direct',
        'Property Cat XL': 'Property Cat XL',
        'Casualty Treaty': 'Casualty Treaty',
        'Marine Hull': 'Marine Hull',
        'Marine Cargo': 'Marine Cargo',
        'Aviation Hull': 'Aviation',
        'Aviation Liability': 'Aviation',
        'Energy Offshore': 'Energy Offshore',
        'Professional Indemnity': 'Professional Indemnity',
        'D&O US': 'D&O',
        'D&O UK': 'D&O',
        'D&O Europe': 'D&O',
        'Cyber Direct': 'Cyber',
        'Cyber Treaty': 'Cyber',
        'Motor Direct': 'Motor',
        'Motor Fleet': 'Motor',
        'Credit & Surety': 'Credit & Surety',
        'Political Risk': 'Political Risk',
        'Terrorism': 'Terrorism',
        'Accident & Health': 'Accident & Health',
        'Medical Malpractice': 'Medical Malpractice',
        'Product Liability': 'Product Liability'
    }

    data = []

    # Ensure we don't exceed available classes
    num_classes = min(num_classes, len(reserving_classes))

    for res_class in reserving_classes[:num_classes]:
        # Get primary LoB mapping
        primary_lob = primary_mappings.get(res_class, np.random.choice(lloyds_lobs))

        # Determine number of LoB mappings (1-4)
        # Most classes map to 1-2 LoB, fewer to 3-4
        num_lobs = np.random.choice([1, 2, 3, 4], p=[0.40, 0.35, 0.15, 0.10])

        # Generate exposure percentages
        if num_lobs == 1:
            exposures = [100.0]
            lobs = [primary_lob]
        else:
            # Primary LoB gets majority of exposure
            primary_exposure = round(np.random.uniform(60, 85), 1)
            remaining_exposure = 100.0 - primary_exposure

            # Distribute remaining exposure among secondary LoB
            secondary_exposures = _distribute_exposure(remaining_exposure, num_lobs - 1)
            exposures = [primary_exposure] + secondary_exposures

            # Select secondary LoB (different from primary)
            available_lobs = [lob for lob in lloyds_lobs if lob != primary_lob]
            secondary_lobs = np.random.choice(available_lobs, size=num_lobs-1, replace=False)
            lobs = [primary_lob] + list(secondary_lobs)

        # Ensure exposures sum to 100%
        exposures = _normalize_exposures(exposures)

        record = {
            'Signing Actuary Reserving Class Name': res_class,
            "Lloyd's LoB 1": lobs[0] if len(lobs) > 0 else '',
            'LoB 1: % of Gross Exposure': exposures[0] if len(exposures) > 0 else 0.0,
            "Lloyd's LoB 2": lobs[1] if len(lobs) > 1 else '',
            'LoB 2: % of Gross Exposure': exposures[1] if len(exposures) > 1 else 0.0,
            "Lloyd's LoB 3": lobs[2] if len(lobs) > 2 else '',
            'LoB 3: % of Gross Exposure': exposures[2] if len(exposures) > 2 else 0.0,
            "Lloyd's LoB 4": lobs[3] if len(lobs) > 3 else '',
            'LoB 4: % of Gross Exposure': exposures[3] if len(exposures) > 3 else 0.0
        }

        data.append(record)

    df = pd.DataFrame(data)

    return df


def _distribute_exposure(total_exposure, num_parts):
    """
    Distribute exposure percentage among multiple LoB.

    Parameters:
    -----------
    total_exposure : float
        Total exposure to distribute
    num_parts : int
        Number of parts to divide into

    Returns:
    --------
    list
        List of exposure percentages
    """
    if num_parts == 1:
        return [round(total_exposure, 1)]

    # Generate random splits
    splits = np.random.dirichlet(np.ones(num_parts)) * total_exposure
    return [round(s, 1) for s in splits]


def _normalize_exposures(exposures):
    """
    Ensure exposures sum to exactly 100%.

    Parameters:
    -----------
    exposures : list
        List of exposure percentages

    Returns:
    --------
    list
        Normalized exposure percentages
    """
    total = sum(exposures)
    if total == 0:
        return exposures

    # Normalize to 100%
    normalized = [e / total * 100 for e in exposures]

    # Round and adjust to ensure sum is exactly 100%
    rounded = [round(e, 1) for e in normalized]
    diff = 100.0 - sum(rounded)

    # Add difference to largest component
    if diff != 0:
        max_idx = rounded.index(max(rounded))
        rounded[max_idx] = round(rounded[max_idx] + diff, 1)

    return rounded


# Generate the data
class_mappings = generate_class_mappings_data(num_classes=20)

# Display summary statistics
print("=" * 80)
print("SAO Addendum Return - SAO Class Mappings Summary")
print("=" * 80)
print(f"Total Reserving Classes: {len(class_mappings)}")
lob2_col = "Lloyd's LoB 2"
lob3_col = "Lloyd's LoB 3"
lob4_col = "Lloyd's LoB 4"
num_1_lob = (class_mappings[lob2_col] == '').sum()
num_2_lob = ((class_mappings[lob2_col] != '') & (class_mappings[lob3_col] == '')).sum()
num_3_lob = ((class_mappings[lob3_col] != '') & (class_mappings[lob4_col] == '')).sum()
num_4_lob = (class_mappings[lob4_col] != '').sum()
print(f"Classes mapping to 1 LoB: {num_1_lob}")
print(f"Classes mapping to 2 LoB: {num_2_lob}")
print(f"Classes mapping to 3 LoB: {num_3_lob}")
print(f"Classes mapping to 4 LoB: {num_4_lob}")
print("=" * 80)
print("\nSample Mappings:")
print(class_mappings.head(10).to_string(index=False))
print("\n")

# Verify all exposures sum to 100%
print("Exposure Validation:")
for idx, row in class_mappings.iterrows():
    total_exposure = (
        row['LoB 1: % of Gross Exposure'] +
        row['LoB 2: % of Gross Exposure'] +
        row['LoB 3: % of Gross Exposure'] +
        row['LoB 4: % of Gross Exposure']
    )
    if abs(total_exposure - 100.0) > 0.1:
        print(f"WARNING: {row['Signing Actuary Reserving Class Name']} total exposure = {total_exposure}%")

print("All exposures validated successfully!\n")

# This table will be available in Power BI
# Power BI will automatically detect the 'class_mappings' dataframe
