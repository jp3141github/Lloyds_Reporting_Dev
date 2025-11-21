"""
Excel Export Utility for Solvency II ASB Returns
Exports synthetic data to Excel format matching Lloyd's specifications
"""

import pandas as pd
from datetime import datetime
from synthetic_data_generator import LloydsDataGenerator


def export_asb_returns_to_excel(output_filename='ASB_Returns_Output.xlsx',
                                  syndicate_number='1234',
                                  syndicate_name='Example Marine & Energy Syndicate'):
    """
    Export ASB returns data to Excel file.

    Parameters:
    -----------
    output_filename : str
        Output Excel filename
    syndicate_number : str
        Lloyd's syndicate number
    syndicate_name : str
        Name of the syndicate
    """

    # Generate data
    generator = LloydsDataGenerator(
        syndicate_number=syndicate_number,
        syndicate_name=syndicate_name,
        start_year=2015,
        end_year=2024
    )

    all_data = generator.generate_all_data(claims_records=500, inflation_records=200)

    # Create Excel writer
    with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:

        # Cover sheet
        cover_data = pd.DataFrame({
            'Field': [
                'Return Type',
                'Syndicate Number',
                'Syndicate Name',
                'Reporting Period',
                'Currency',
                'Generation Date',
                'Status'
            ],
            'Value': [
                'Solvency II Pillar 3 - ASB Returns',
                syndicate_number,
                syndicate_name,
                f'Annual {datetime.now().year}',
                'Multi-currency',
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Synthetic Data for Testing'
            ]
        })
        cover_data.to_excel(writer, sheet_name='Cover_Sheet', index=False)

        # ASB 245/246/247 - Claims Data
        claims_df = all_data['ASB_245_246_247']
        claims_df.to_excel(writer, sheet_name='ASB_245_246_247_Claims', index=False)

        # ASB 248 - Inflation Rates
        inflation_df = all_data['ASB_248']
        inflation_df.to_excel(writer, sheet_name='ASB_248_InflationRates', index=False)

        # Summary by Line of Business
        lob_summary = claims_df.groupby(['LineOfBusiness']).agg({
            'GrossClaimPaid': 'sum',
            'ReinsuranceRecoveries': 'sum',
            'GrossUndiscountedBEClaimsProvisions': 'sum',
            'GrossRBNS': 'sum'
        }).reset_index()
        lob_summary.to_excel(writer, sheet_name='Summary_by_LOB', index=False)

        # Summary by Underwriting Year
        year_summary = claims_df.groupby(['UnderwritingYear']).agg({
            'GrossClaimPaid': 'sum',
            'ReinsuranceRecoveries': 'sum',
            'GrossUndiscountedBEClaimsProvisions': 'sum',
            'GrossRBNS': 'sum'
        }).reset_index()
        year_summary.to_excel(writer, sheet_name='Summary_by_Year', index=False)

        # Development year analysis
        dev_analysis = claims_df.groupby(['DevelopmentYear']).agg({
            'GrossClaimPaid': ['mean', 'sum', 'count'],
            'ReinsuranceRecoveries': 'sum'
        }).reset_index()
        dev_analysis.columns = ['DevelopmentYear', 'AvgGrossClaimPaid',
                                 'TotalGrossClaimPaid', 'ClaimCount',
                                 'TotalReinsuranceRecoveries']
        dev_analysis.to_excel(writer, sheet_name='Development_Analysis', index=False)

        # Lines of Business reference
        lob_ref = pd.DataFrame([
            {'Code': k, 'Description': v}
            for k, v in generator.LINES_OF_BUSINESS.items()
        ])
        lob_ref.to_excel(writer, sheet_name='LOB_Reference', index=False)

    print(f"Excel file exported successfully: {output_filename}")
    print(f"Sheets created:")
    print("  - Cover_Sheet")
    print("  - ASB_245_246_247_Claims")
    print("  - ASB_248_InflationRates")
    print("  - Summary_by_LOB")
    print("  - Summary_by_Year")
    print("  - Development_Analysis")
    print("  - LOB_Reference")


if __name__ == '__main__':
    export_asb_returns_to_excel(
        output_filename='ASB_Returns_Synthetic_Data.xlsx',
        syndicate_number='1234',
        syndicate_name='Example Marine & Energy Syndicate'
    )
