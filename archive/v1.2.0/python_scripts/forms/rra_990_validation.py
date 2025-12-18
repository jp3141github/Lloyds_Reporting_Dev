"""
RRA 990 Validation Summary Form - Power BI Python Script
This script performs cross-form validation checks across all RRA forms
"""

import pandas as pd
import numpy as np
from pathlib import Path


def validate_all_forms(data_directory='../../synthetic_data'):
    """
    Perform comprehensive validation across all RRA forms

    Parameters:
    -----------
    data_directory : str
        Directory containing all RRA form CSV files

    Returns:
    --------
    pandas.DataFrame
        Validation results with status for each rule
    """

    validation_results = []
    data_dir = Path(data_directory)

    # Rule 1: Check all required files exist
    required_forms = ['010', '020', '071', '081', '091', '193', '291', '292',
                     '293', '294', '295', '391', '910']

    for form in required_forms:
        file_path = data_dir / f'rra_{form}*.csv'
        files = list(data_dir.glob(f'rra_{form}*.csv'))

        validation_results.append({
            'Rule_ID': f'FILE_{form}',
            'Rule_Description': f'Form {form} file exists',
            'Status': 'PASS' if len(files) > 0 else 'FAIL',
            'Severity': 'Critical',
            'Records_Affected': 0 if len(files) > 0 else 1,
            'Details': f'Found {len(files)} file(s)' if len(files) > 0 else 'File not found'
        })

    # Rule 2: Cross-form consistency - Syndicate numbers
    try:
        df_010 = pd.read_csv(data_dir / 'rra_010_control.csv')
        df_193 = pd.read_csv(data_dir / 'rra_193_net_claims.csv')
        df_291 = pd.read_csv(data_dir / 'rra_291_gross_premium_ibnr.csv')

        syndicates_010 = set(df_010['Syndicate_Number'].unique())
        syndicates_193 = set(df_193['Syndicate_Number'].unique())
        syndicates_291 = set(df_291['Syndicate_Number'].unique())

        # Check if all syndicates in 193 and 291 are in 010
        orphan_193 = syndicates_193 - syndicates_010
        orphan_291 = syndicates_291 - syndicates_010

        validation_results.append({
            'Rule_ID': 'XREF_SYN_193',
            'Rule_Description': 'All syndicates in Form 193 must exist in Form 010',
            'Status': 'PASS' if len(orphan_193) == 0 else 'FAIL',
            'Severity': 'High',
            'Records_Affected': len(orphan_193),
            'Details': f'Orphan syndicates: {orphan_193}' if orphan_193 else 'All syndicates valid'
        })

        validation_results.append({
            'Rule_ID': 'XREF_SYN_291',
            'Rule_Description': 'All syndicates in Form 291 must exist in Form 010',
            'Status': 'PASS' if len(orphan_291) == 0 else 'FAIL',
            'Severity': 'High',
            'Records_Affected': len(orphan_291),
            'Details': f'Orphan syndicates: {orphan_291}' if orphan_291 else 'All syndicates valid'
        })

    except Exception as e:
        validation_results.append({
            'Rule_ID': 'XREF_SYN',
            'Rule_Description': 'Cross-form syndicate validation',
            'Status': 'ERROR',
            'Severity': 'Critical',
            'Records_Affected': 0,
            'Details': str(e)
        })

    # Rule 3: Net vs Gross consistency (Form 292 vs 291)
    try:
        df_291 = pd.read_csv(data_dir / 'rra_291_gross_premium_ibnr.csv')
        df_292 = pd.read_csv(data_dir / 'rra_292_net_premium_ibnr.csv')

        # Merge on key dimensions
        merged = df_291.merge(
            df_292,
            on=['Syndicate_Number', 'Year_of_Account', 'LOB_Code'],
            how='inner',
            suffixes=('_Gross', '_Net')
        )

        # Check: Net amounts should be <= Gross amounts
        invalid_premium = merged[merged['Net_Written_Premium'] > merged['Gross_Written_Premium']]
        invalid_claims = merged[merged['Paid_Claims_Net'] > merged['Paid_Claims_Gross']]

        validation_results.append({
            'Rule_ID': 'NET_LE_GROSS_PREM',
            'Rule_Description': 'Net Premium must be ≤ Gross Premium',
            'Status': 'PASS' if len(invalid_premium) == 0 else 'FAIL',
            'Severity': 'Critical',
            'Records_Affected': len(invalid_premium),
            'Details': f'{len(invalid_premium)} violations found' if len(invalid_premium) > 0 else 'All records valid'
        })

        validation_results.append({
            'Rule_ID': 'NET_LE_GROSS_CLAIMS',
            'Rule_Description': 'Net Claims must be ≤ Gross Claims',
            'Status': 'PASS' if len(invalid_claims) == 0 else 'FAIL',
            'Severity': 'Critical',
            'Records_Affected': len(invalid_claims),
            'Details': f'{len(invalid_claims)} violations found' if len(invalid_claims) > 0 else 'All records valid'
        })

    except FileNotFoundError:
        validation_results.append({
            'Rule_ID': 'NET_GROSS_CHECK',
            'Rule_Description': 'Net vs Gross validation',
            'Status': 'SKIPPED',
            'Severity': 'High',
            'Records_Affected': 0,
            'Details': 'Form 291 or 292 not found'
        })

    # Rule 4: IBNR range validation
    try:
        df_291 = pd.read_csv(data_dir / 'rra_291_gross_premium_ibnr.csv')

        invalid_range = df_291[
            (df_291['IBNR_Low'] > df_291['IBNR_Best_Estimate']) |
            (df_291['IBNR_Best_Estimate'] > df_291['IBNR_High'])
        ]

        validation_results.append({
            'Rule_ID': 'IBNR_RANGE',
            'Rule_Description': 'IBNR Low ≤ Best ≤ High',
            'Status': 'PASS' if len(invalid_range) == 0 else 'FAIL',
            'Severity': 'High',
            'Records_Affected': len(invalid_range),
            'Details': f'{len(invalid_range)} violations found' if len(invalid_range) > 0 else 'All IBNR ranges valid'
        })

    except FileNotFoundError:
        pass

    # Rule 5: Data completeness - no null key fields
    for form_num, key_fields in [('010', ['Syndicate_Number']),
                                   ('193', ['Syndicate_Number', 'Year_of_Account', 'LOB_Code']),
                                   ('291', ['Syndicate_Number', 'Year_of_Account', 'LOB_Code'])]:
        try:
            df = pd.read_csv(data_dir / f'rra_{form_num}_*.csv')
            null_records = df[key_fields].isnull().any(axis=1).sum()

            validation_results.append({
                'Rule_ID': f'COMP_{form_num}',
                'Rule_Description': f'Form {form_num} key fields completeness',
                'Status': 'PASS' if null_records == 0 else 'FAIL',
                'Severity': 'Critical',
                'Records_Affected': null_records,
                'Details': f'{null_records} records with null key fields' if null_records > 0 else 'All key fields populated'
            })

        except FileNotFoundError:
            pass

    # Convert to DataFrame
    df_validation = pd.DataFrame(validation_results)

    # Add validation timestamp
    df_validation['Validation_Timestamp'] = pd.Timestamp.now()

    # Sort by severity and status
    severity_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
    status_order = {'FAIL': 0, 'ERROR': 1, 'PASS': 2, 'SKIPPED': 3}

    df_validation['Severity_Order'] = df_validation['Severity'].map(severity_order)
    df_validation['Status_Order'] = df_validation['Status'].map(status_order)

    df_validation = df_validation.sort_values(['Severity_Order', 'Status_Order'])
    df_validation = df_validation.drop(columns=['Severity_Order', 'Status_Order'])

    return df_validation


def get_validation_summary(data_directory='../../synthetic_data'):
    """
    Get high-level validation summary statistics

    Returns:
    --------
    dict
        Summary statistics
    """

    df = validate_all_forms(data_directory)

    summary = {
        'Total_Rules': len(df),
        'Rules_Passed': len(df[df['Status'] == 'PASS']),
        'Rules_Failed': len(df[df['Status'] == 'FAIL']),
        'Rules_Error': len(df[df['Status'] == 'ERROR']),
        'Rules_Skipped': len(df[df['Status'] == 'SKIPPED']),
        'Critical_Failures': len(df[(df['Status'] == 'FAIL') & (df['Severity'] == 'Critical')]),
        'High_Failures': len(df[(df['Status'] == 'FAIL') & (df['Severity'] == 'High')]),
        'Total_Records_Affected': df['Records_Affected'].sum(),
        'Validation_Status': 'PASS' if len(df[df['Status'] == 'FAIL']) == 0 else 'FAIL'
    }

    return summary


def export_validation_report(data_directory='../../synthetic_data', output_file='rra_990_validation.csv'):
    """
    Export validation results to CSV

    Parameters:
    -----------
    data_directory : str
        Directory containing RRA forms
    output_file : str
        Output CSV filename
    """

    df_validation = validate_all_forms(data_directory)
    df_validation.to_csv(output_file, index=False)
    print(f"Validation report exported to: {output_file}")

    return df_validation


# For use in Power BI
# df = validate_all_forms()


if __name__ == "__main__":
    print("Running RRA Form 990 Validation...")
    print("="*80)

    try:
        # Run validation
        df = validate_all_forms()

        # Print summary
        summary = get_validation_summary()
        print("\nValidation Summary:")
        print("="*80)
        for key, value in summary.items():
            print(f"{key}: {value}")

        # Print detailed results
        print("\n" + "="*80)
        print("Detailed Validation Results:")
        print("="*80)
        print(df.to_string(index=False))

        # Export to CSV
        print("\n" + "="*80)
        export_validation_report()

    except Exception as e:
        print(f"Validation failed with error: {e}")
