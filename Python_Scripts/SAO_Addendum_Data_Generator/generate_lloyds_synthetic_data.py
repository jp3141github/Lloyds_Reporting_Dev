"""
Lloyd's of London SAO Addendum Return - Synthetic Data Generator
================================================================

This script generates synthetic Lloyd's of London data for the SAO Addendum Return 2025.
It creates three main datasets:
1. Specific IBNR data (Form 090)
2. Movements and Actual vs Expected Analysis (Form 100)
3. SAO Class Mappings

The generated data can be used in Power BI for reporting purposes.

Author: Claude AI
Date: 2025-11-21
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


class LloydsSyntheticDataGenerator:
    """Generate synthetic Lloyd's of London data for SAO Addendum Return."""

    def __init__(self, syndicate_number="2060N"):
        """
        Initialize the data generator.

        Args:
            syndicate_number (str): The syndicate number for the report
        """
        self.syndicate_number = syndicate_number

        # Lloyd's Lines of Business
        self.lloyds_lobs = [
            "Fire", "Property Direct", "Property Cat", "Property Cat XL",
            "Property Treaty", "Motor Direct", "Motor XL", "Marine Cargo",
            "Marine Hull", "Energy Offshore", "Energy Onshore", "Aviation Hull",
            "Aviation Liability", "D&O", "Professional Indemnity", "Casualty Treaty",
            "General Liability", "Medical Malpractice", "Product Liability",
            "Cyber", "Credit & Bond", "Political Risk", "Terrorism", "Accident & Health"
        ]

        # Reserving class examples
        self.reserving_classes = [
            "Property Cat XL", "Marine Hull", "D&O US", "Aviation Liability",
            "Professional Indemnity", "Casualty Treaty", "Energy Offshore",
            "Property Direct", "Motor XL", "Cyber Liability", "Political Risk"
        ]

        # CAT codes (examples of historical Lloyd's CAT codes)
        self.cat_codes = [
            "22E",  # Example: Major storm
            "23A",  # Example: Hurricane
            "23B",  # Example: Flood
            "24C",  # Example: Earthquake
            "21D",  # Example: Wildfire
            "Non Nat-Cat"  # Non-natural catastrophe
        ]

    def generate_specific_ibnr(self, num_records=50):
        """
        Generate synthetic Specific IBNR data (Form 090).

        Args:
            num_records (int): Number of IBNR records to generate

        Returns:
            pd.DataFrame: Specific IBNR data
        """
        data = []

        for i in range(num_records):
            # Determine if CAT or Non-CAT
            is_cat = random.random() > 0.3
            cat_code = random.choice([c for c in self.cat_codes if c != "Non Nat-Cat"]) if is_cat else "Non Nat-Cat"

            # Generate random values
            reserving_class = random.choice(self.reserving_classes)
            lloyds_lob = random.choice(self.lloyds_lobs)
            num_losses = random.randint(1, 20)
            underwriting_year = random.choice([2020, 2021, 2022, 2023, 2024, 2025])

            # Generate IBNR amounts (ensure > £1m gross as per requirements)
            gross_ibnr = random.randint(1000, 50000)  # £000s, so 1000-50000 = £1m-£50m
            reinsurance_recovery = random.uniform(0.2, 0.5)  # 20-50% recovery
            net_ibnr = int(gross_ibnr * (1 - reinsurance_recovery))

            # Generate comment
            comments = [
                "Reserved using underlying cedant exposure and loss advice plus assumption on limits losses",
                "Based on market loss estimates and exposure analysis",
                "Actuarial analysis of reported losses and development patterns",
                "Industry loss estimates adjusted for portfolio exposure",
                "Initial reserve pending further loss development",
                ""
            ]
            comment = random.choice(comments)

            data.append({
                'Reserving_Class': reserving_class,
                'Lloyds_CAT_Code': cat_code,
                'Lloyds_Line_of_Business': lloyds_lob,
                'Number_of_Losses': num_losses,
                'Underwriting_Year': underwriting_year,
                'Gross_IBNR_GBP000s': gross_ibnr,
                'Net_IBNR_GBP000s': net_ibnr,
                'Comment': comment
            })

        df = pd.DataFrame(data)
        return df.sort_values(['Reserving_Class', 'Underwriting_Year'])

    def generate_movements_and_ave(self, num_classes=10):
        """
        Generate synthetic Movements and Actual vs Expected Analysis data (Form 100).

        Args:
            num_classes (int): Number of reserving classes to generate

        Returns:
            pd.DataFrame: Movements and AvE analysis data
        """
        data = []

        for class_num in range(1, num_classes + 1):
            class_name = f"Class {class_num:02d}"
            if class_num <= len(self.reserving_classes):
                class_name = self.reserving_classes[class_num - 1]

            lloyds_lob = random.choice(self.lloyds_lobs)

            # Generate data for each underwriting year
            for uw_year, year_label in [(2023, "2023 & Prior"), (2024, "2024"), (2025, "2025")]:
                is_reporting_year = "Yes" if uw_year >= 2024 else "No"

                # Generate ultimate premium
                ultimate_premium = random.randint(5000, 100000)  # £5m to £100m (in £000s)

                # Generate Actual vs Expected (can be positive or negative)
                ave_pct = random.uniform(-15, 10)  # -15% to +10%

                # Generate Initial Expected Loss Ratio
                ielr = random.uniform(55, 75)  # 55% to 75%

                # Generate Ultimate Loss Ratio (should relate to IELR + AvE)
                ulr = ielr + random.uniform(-5, 10)

                # Generate prior year values (2024YE)
                prior_ielr_2024ye = ielr + random.uniform(-3, 3)
                prior_ulr_2024ye = ulr + random.uniform(-5, 5)
                prior_ave_2024ye = ave_pct + random.uniform(-5, 5)

                # Generate current year values (2025YE)
                current_ielr_2025ye = ielr
                current_ulr_2025ye = ulr
                current_ave_2025ye = ave_pct

                # Syndicate estimate
                syndicate_ulr = ulr + random.uniform(-3, 3)

                data.append({
                    'Class_Number': class_num,
                    'Class_Name': class_name,
                    'Lloyds_Line_of_Business': lloyds_lob,
                    'Underwriting_Year': uw_year,
                    'Year_Label': year_label,
                    'Reporting_Year': is_reporting_year,
                    'Ultimate_Premium_GBP000s': ultimate_premium,
                    'ActualVsExpected_Pct_Ultimate_Premium': round(ave_pct, 2),
                    'Initial_Expected_Loss_Ratio_Pct': round(ielr, 2),
                    'Ultimate_Loss_Ratio_Pct_2024YE': round(prior_ulr_2024ye, 2),
                    'Ultimate_Loss_Ratio_Pct_2025YE': round(current_ulr_2025ye, 2),
                    'Syndicate_Estimate_ULR_2025YE': round(syndicate_ulr, 2),
                    'IELR_2024YE': round(prior_ielr_2024ye, 2),
                    'IELR_2025YE': round(current_ielr_2025ye, 2),
                    'AvE_2024YE': round(prior_ave_2024ye, 2),
                    'AvE_2025YE': round(current_ave_2025ye, 2)
                })

        df = pd.DataFrame(data)
        return df.sort_values(['Class_Number', 'Underwriting_Year'])

    def generate_sao_class_mappings(self, num_classes=15):
        """
        Generate synthetic SAO Class Mappings data.

        Args:
            num_classes (int): Number of reserving classes to map

        Returns:
            pd.DataFrame: SAO class mappings data
        """
        data = []

        for i in range(num_classes):
            reserving_class = self.reserving_classes[i % len(self.reserving_classes)]
            if i >= len(self.reserving_classes):
                reserving_class = f"{reserving_class} Sub-{i}"

            # Select up to 4 Lloyd's LoB for this reserving class
            num_lobs = random.randint(1, 4)
            selected_lobs = random.sample(self.lloyds_lobs, num_lobs)

            # Generate exposure percentages that sum to 100%
            exposures = np.random.dirichlet(np.ones(num_lobs)) * 100

            # Pad with None if less than 4 LoB
            while len(selected_lobs) < 4:
                selected_lobs.append(None)
                exposures = np.append(exposures, None)

            data.append({
                'Reserving_Class_Name': reserving_class,
                'Lloyds_LoB_1': selected_lobs[0],
                'LoB_1_Pct_Gross_Exposure': round(exposures[0], 2) if exposures[0] is not None else None,
                'Lloyds_LoB_2': selected_lobs[1],
                'LoB_2_Pct_Gross_Exposure': round(exposures[1], 2) if exposures[1] is not None else None,
                'Lloyds_LoB_3': selected_lobs[2],
                'LoB_3_Pct_Gross_Exposure': round(exposures[2], 2) if exposures[2] is not None else None,
                'Lloyds_LoB_4': selected_lobs[3],
                'LoB_4_Pct_Gross_Exposure': round(exposures[3], 2) if exposures[3] is not None else None
            })

        return pd.DataFrame(data)

    def generate_all_data(self):
        """
        Generate all synthetic data tables.

        Returns:
            dict: Dictionary containing all three dataframes
        """
        print("Generating Specific IBNR data...")
        df_ibnr = self.generate_specific_ibnr(num_records=50)

        print("Generating Movements and AvE analysis data...")
        df_movements = self.generate_movements_and_ave(num_classes=10)

        print("Generating SAO Class Mappings data...")
        df_mappings = self.generate_sao_class_mappings(num_classes=15)

        return {
            'Specific_IBNR': df_ibnr,
            'Movements_and_AvE': df_movements,
            'SAO_Class_Mappings': df_mappings
        }

    def export_to_csv(self, output_dir='output'):
        """
        Generate and export all data to CSV files.

        Args:
            output_dir (str): Directory to save CSV files
        """
        import os

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Generate all data
        data_dict = self.generate_all_data()

        # Export to CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        for table_name, df in data_dict.items():
            filename = f"{output_dir}/{table_name}_{self.syndicate_number}_{timestamp}.csv"
            df.to_csv(filename, index=False)
            print(f"Exported: {filename} ({len(df)} records)")

        print("\nData generation complete!")
        return data_dict

    def export_to_excel(self, output_dir='output'):
        """
        Generate and export all data to a single Excel file with multiple sheets.

        Args:
            output_dir (str): Directory to save Excel file
        """
        import os

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Generate all data
        data_dict = self.generate_all_data()

        # Export to Excel
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{output_dir}/SAO_Addendum_Synthetic_Data_{self.syndicate_number}_{timestamp}.xlsx"

        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            for table_name, df in data_dict.items():
                df.to_excel(writer, sheet_name=table_name, index=False)
                print(f"Added sheet: {table_name} ({len(df)} records)")

        print(f"\nExported: {filename}")
        print("Data generation complete!")
        return data_dict


def main():
    """Main function to generate synthetic Lloyd's data."""
    print("="*70)
    print("Lloyd's of London SAO Addendum Return - Synthetic Data Generator")
    print("="*70)
    print()

    # Initialize generator
    generator = LloydsSyntheticDataGenerator(syndicate_number="2060N")

    # Generate and export data
    print("Generating synthetic data...")
    print()

    # Export to CSV files (for Power BI)
    data_dict = generator.export_to_csv(output_dir='output')

    print()
    print("="*70)

    # Also export to Excel for easy viewing
    generator.export_to_excel(output_dir='output')

    # Display sample data
    print()
    print("="*70)
    print("Sample Data Preview")
    print("="*70)
    print()

    for table_name, df in data_dict.items():
        print(f"\n{table_name} (first 5 rows):")
        print("-"*70)
        print(df.head().to_string())
        print()


if __name__ == "__main__":
    main()
