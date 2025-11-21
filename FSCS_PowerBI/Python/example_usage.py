"""
Example Usage of FSCS Data Generator
=====================================

This script demonstrates how to use the fscs_data_generator module
to create synthetic Lloyd's data for testing and development.
"""

from fscs_data_generator import (
    FSCSDataGenerator,
    get_fscs_summary_data,
    get_fscs_detail_data
)
import pandas as pd


def main():
    """Main function demonstrating various usage patterns."""

    print("="*80)
    print("FSCS DATA GENERATOR - EXAMPLE USAGE")
    print("="*80)
    print()

    # Example 1: Generate summary data using convenience function
    print("Example 1: Generate Summary Data")
    print("-" * 80)
    summary_df = get_fscs_summary_data(num_syndicates=5, reporting_year=2024)
    print(summary_df.to_string())
    print()

    # Example 2: Generate detailed transaction data
    print("\nExample 2: Generate Detailed Transaction Data")
    print("-" * 80)
    detail_df = get_fscs_detail_data(num_syndicates=5, reporting_year=2024)
    print(f"Total transactions generated: {len(detail_df)}")
    print(f"Transactions included in FSCS: {detail_df['included_in_fscs'].sum()}")
    print("\nFirst 10 transactions:")
    print(detail_df.head(10).to_string())
    print()

    # Example 3: Using the generator class directly
    print("\nExample 3: Using Generator Class Directly")
    print("-" * 80)
    generator = FSCSDataGenerator(num_syndicates=3, reporting_year=2024)

    # Get full dataset with all fields
    full_data = generator.generate_full_dataset()
    print("Full dataset with calculated fields:")
    print(full_data.to_string())
    print()

    # Example 4: Generate data for multiple years
    print("\nExample 4: Multi-Year Data Generation")
    print("-" * 80)
    multi_year_data = []
    for year in [2022, 2023, 2024]:
        yearly_data = get_fscs_summary_data(num_syndicates=3, reporting_year=year)
        multi_year_data.append(yearly_data)

    combined_df = pd.concat(multi_year_data, ignore_index=True)
    print(combined_df.to_string())
    print()

    # Example 5: Export to Excel (FSCS format)
    print("\nExample 5: Export to Excel")
    print("-" * 80)

    # Generate data
    generator = FSCSDataGenerator(num_syndicates=10, reporting_year=2024)
    summary = generator.generate_fscs_output_format()
    detail = generator.generate_detail_dataset()
    full = generator.generate_full_dataset()

    # Create Excel file with multiple sheets
    output_file = 'FSCS_Synthetic_Data.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # FSCS Summary sheet
        summary.to_excel(writer, sheet_name='FSCS_Summary', index=False)

        # Detailed transactions
        detail.to_excel(writer, sheet_name='Detail_Transactions', index=False)

        # Full dataset with analytics
        full.to_excel(writer, sheet_name='Full_Dataset', index=False)

        # Summary statistics
        stats = pd.DataFrame({
            'Metric': [
                'Total Syndicates',
                'Total GWP (£M)',
                'Total BEL (£M)',
                'Avg GWP per Syndicate (£M)',
                'Avg BEL per Syndicate (£M)'
            ],
            'Value': [
                len(full),
                round(full['gwp_total'].sum() / 1_000_000, 2),
                round(full['bel_total'].sum() / 1_000_000, 2),
                round(full['gwp_total'].mean() / 1_000_000, 2),
                round(full['bel_total'].mean() / 1_000_000, 2)
            ]
        })
        stats.to_excel(writer, sheet_name='Summary_Statistics', index=False)

    print(f"Data exported to: {output_file}")
    print()

    # Example 6: Summary Statistics
    print("\nExample 6: Summary Statistics")
    print("-" * 80)
    print(f"Total GWP General Business: £{full['gwp_general_business'].sum():,.2f}")
    print(f"Total GWP Life Business: £{full['gwp_life_business'].sum():,.2f}")
    print(f"Total BEL General Business: £{full['bel_general_business'].sum():,.2f}")
    print(f"Total BEL Life Business: £{full['bel_life_business'].sum():,.2f}")
    print(f"\nAverage General Business %: {full['general_business_pct'].mean():.2f}%")
    print()


if __name__ == "__main__":
    main()
