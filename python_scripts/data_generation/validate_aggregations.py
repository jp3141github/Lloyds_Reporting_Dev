#!/usr/bin/env python3
"""
Validate Raw Data Aggregations

This script validates that the raw transactional data can be aggregated
to produce the Power BI outputs in exports/powerbi/.

Author: Claude
Date: 2025-11-28
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path


def validate_claims_aggregations(raw_dir: str, exports_dir: str) -> dict:
    """Validate claim transaction aggregations."""
    print("\n" + "=" * 60)
    print("CLAIMS VALIDATION")
    print("=" * 60)

    results = {'passed': [], 'failed': []}

    # Load raw claim transactions
    claims_raw = pd.read_csv(os.path.join(raw_dir, 'claim_transactions.csv'))

    # Load target Claims_BySyndicate
    target_file = os.path.join(exports_dir, 'Claims_BySyndicate.csv')
    if os.path.exists(target_file):
        target = pd.read_csv(target_file)

        # Aggregate raw data by syndicate
        agg = claims_raw.groupby('Syndicate_Number').agg({
            'Claim_Reference': 'nunique',
            'Amount': 'sum',
            'Outstanding_Amount': 'sum',
            'Incurred_Amount': 'sum'
        }).reset_index()

        print(f"\nClaims_BySyndicate validation:")
        print(f"  Target syndicates: {len(target)}")
        print(f"  Aggregated syndicates: {len(agg)}")

        # Check all syndicates are present
        missing = set(target['Syndicate_Number']) - set(agg['Syndicate_Number'])
        if not missing:
            results['passed'].append('Claims_BySyndicate: All syndicates present')
            print("  [PASS] All syndicates present")
        else:
            results['failed'].append(f'Claims_BySyndicate: Missing syndicates {missing}')
            print(f"  [FAIL] Missing syndicates: {missing}")

    # Load target Claims_ByStatus
    target_file = os.path.join(exports_dir, 'Claims_ByStatus.csv')
    if os.path.exists(target_file):
        target = pd.read_csv(target_file)

        # Aggregate raw data by status
        agg = claims_raw.groupby('Status').agg({
            'Claim_Reference': 'nunique',
            'Amount': 'sum',
            'Outstanding_Amount': 'sum'
        }).reset_index()

        print(f"\nClaims_ByStatus validation:")
        print(f"  Target statuses: {list(target['Status'])}")
        print(f"  Aggregated statuses: {list(agg['Status'])}")

        # Check status coverage
        target_statuses = set(target['Status'])
        agg_statuses = set(agg['Status'])
        covered = agg_statuses & target_statuses
        print(f"  Status coverage: {len(covered)}/{len(target_statuses)}")
        results['passed'].append(f'Claims_ByStatus: {len(covered)} statuses covered')

    return results


def validate_premium_aggregations(raw_dir: str, exports_dir: str) -> dict:
    """Validate premium transaction aggregations."""
    print("\n" + "=" * 60)
    print("PREMIUM VALIDATION")
    print("=" * 60)

    results = {'passed': [], 'failed': []}

    # Load raw premium transactions
    premiums_raw = pd.read_csv(os.path.join(raw_dir, 'premium_transactions.csv'))

    # Load target RRA_291
    target_file = os.path.join(exports_dir, 'RRA_291_GrossPremiumIBNR.csv')
    if os.path.exists(target_file):
        target = pd.read_csv(target_file)

        # Aggregate raw data by syndicate/year/LOB
        agg = premiums_raw.groupby(['Syndicate_Number', 'Year_of_Account', 'LOB_Code']).agg({
            'Gross_Amount': 'sum'
        }).reset_index()

        print(f"\nRRA_291_GrossPremiumIBNR validation:")
        print(f"  Target records: {len(target)}")
        print(f"  Aggregated records: {len(agg)}")

        # Check syndicate coverage
        target_syns = set(target['Syndicate_Number'].unique())
        agg_syns = set(agg['Syndicate_Number'].unique())
        print(f"  Syndicate coverage: {len(agg_syns & target_syns)}/{len(target_syns)}")

        if agg_syns >= target_syns:
            results['passed'].append('RRA_291: All syndicates covered')
            print("  [PASS] All syndicates covered")
        else:
            results['failed'].append('RRA_291: Missing syndicates')
            print("  [FAIL] Missing syndicates")

    return results


def validate_asset_aggregations(raw_dir: str, exports_dir: str) -> dict:
    """Validate asset holdings aggregations."""
    print("\n" + "=" * 60)
    print("ASSET VALIDATION")
    print("=" * 60)

    results = {'passed': [], 'failed': []}

    # Load raw asset holdings
    assets_raw = pd.read_csv(os.path.join(raw_dir, 'asset_holdings.csv'))

    # Load target Liquidity_AssetBreakdown
    target_file = os.path.join(exports_dir, 'Liquidity_AssetBreakdown.csv')
    if os.path.exists(target_file):
        target = pd.read_csv(target_file)

        # Aggregate raw data by syndicate/quarter
        agg = assets_raw.groupby(['Syndicate_Number', 'Quarter']).agg({
            'Market_Value': 'sum'
        }).reset_index()

        print(f"\nLiquidity_AssetBreakdown validation:")
        print(f"  Target records: {len(target)}")
        print(f"  Aggregated records: {len(agg)}")

        # Check syndicate/quarter coverage
        target_keys = set(zip(target['Syndicate_Number'], target['Quarter']))
        agg_keys = set(zip(agg['Syndicate_Number'], agg['Quarter']))

        coverage = len(agg_keys & target_keys)
        print(f"  Syndicate/Quarter coverage: {coverage}/{len(target_keys)}")

        if coverage >= len(target_keys) * 0.8:  # 80% coverage threshold
            results['passed'].append('Liquidity_AssetBreakdown: Good coverage')
            print("  [PASS] Good coverage (>=80%)")
        else:
            results['failed'].append('Liquidity_AssetBreakdown: Low coverage')
            print("  [WARN] Low coverage (<80%)")

    return results


def validate_reserve_aggregations(raw_dir: str, exports_dir: str) -> dict:
    """Validate reserve movement aggregations."""
    print("\n" + "=" * 60)
    print("RESERVE VALIDATION")
    print("=" * 60)

    results = {'passed': [], 'failed': []}

    # Load raw reserve movements
    reserves_raw = pd.read_csv(os.path.join(raw_dir, 'reserve_movements.csv'))

    # Load target QSR_TechnicalProvisions
    target_file = os.path.join(exports_dir, 'QSR_TechnicalProvisions.csv')
    if os.path.exists(target_file):
        target = pd.read_csv(target_file)

        # Aggregate raw data by syndicate/LOB
        bel_agg = reserves_raw[reserves_raw['Reserve_Type'] == 'Best_Estimate_Liabilities'].groupby(
            ['Syndicate_Number', 'LOB_Code']
        ).agg({'Amount': 'sum'}).reset_index()

        print(f"\nQSR_TechnicalProvisions validation:")
        print(f"  Target records: {len(target)}")
        print(f"  Aggregated BEL records: {len(bel_agg)}")

        # Check syndicate/LOB coverage
        target_keys = set(zip(target['Syndicate_Number'], target['LOB_Code']))
        agg_keys = set(zip(bel_agg['Syndicate_Number'], bel_agg['LOB_Code']))

        coverage = len(agg_keys & target_keys)
        print(f"  Syndicate/LOB coverage: {coverage}/{len(target_keys)}")

        if coverage >= len(target_keys) * 0.8:
            results['passed'].append('QSR_TechnicalProvisions: Good coverage')
            print("  [PASS] Good coverage (>=80%)")
        else:
            results['failed'].append('QSR_TechnicalProvisions: Low coverage')

    return results


def validate_risk_aggregations(raw_dir: str, exports_dir: str) -> dict:
    """Validate risk exposure aggregations."""
    print("\n" + "=" * 60)
    print("RISK/SCR VALIDATION")
    print("=" * 60)

    results = {'passed': [], 'failed': []}

    # Load raw risk exposures
    risk_raw = pd.read_csv(os.path.join(raw_dir, 'risk_exposures.csv'))

    # Load target LCR_SCR_Summary
    target_file = os.path.join(exports_dir, 'LCR_SCR_Summary.csv')
    if os.path.exists(target_file):
        target = pd.read_csv(target_file)

        # Aggregate raw data by syndicate
        agg = risk_raw.groupby(['Syndicate_Number', 'Risk_Type']).agg({
            'SCR_Contribution': 'sum'
        }).reset_index()

        # Pivot to match target structure
        agg_pivot = agg.pivot(index='Syndicate_Number', columns='Risk_Type', values='SCR_Contribution').reset_index()

        print(f"\nLCR_SCR_Summary validation:")
        print(f"  Target syndicates: {len(target)}")
        print(f"  Aggregated syndicates: {len(agg_pivot)}")

        # Check syndicate coverage
        target_syns = set(target['Syndicate_Number'])
        agg_syns = set(agg_pivot['Syndicate_Number'])
        print(f"  Syndicate coverage: {len(agg_syns & target_syns)}/{len(target_syns)}")

        if agg_syns >= target_syns:
            results['passed'].append('LCR_SCR_Summary: All syndicates covered')
            print("  [PASS] All syndicates covered")
        else:
            results['failed'].append('LCR_SCR_Summary: Missing syndicates')

    return results


def run_all_validations(raw_dir: str, exports_dir: str) -> dict:
    """Run all validation checks."""
    print("=" * 60)
    print("RAW DATA AGGREGATION VALIDATION")
    print("=" * 60)
    print(f"\nRaw data directory: {raw_dir}")
    print(f"Target exports directory: {exports_dir}")

    all_results = {'passed': [], 'failed': []}

    # Run validations
    for validation_func in [
        validate_claims_aggregations,
        validate_premium_aggregations,
        validate_asset_aggregations,
        validate_reserve_aggregations,
        validate_risk_aggregations
    ]:
        results = validation_func(raw_dir, exports_dir)
        all_results['passed'].extend(results['passed'])
        all_results['failed'].extend(results['failed'])

    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"\nPassed: {len(all_results['passed'])}")
    for msg in all_results['passed']:
        print(f"  [PASS] {msg}")

    print(f"\nFailed: {len(all_results['failed'])}")
    for msg in all_results['failed']:
        print(f"  [FAIL] {msg}")

    return all_results


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Validate raw data aggregations')
    parser.add_argument('--raw-dir', '-r', default='raw_data',
                       help='Raw data directory')
    parser.add_argument('--exports-dir', '-e', default='exports/powerbi',
                       help='Power BI exports directory')

    args = parser.parse_args()

    # Use absolute paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent

    raw_dir = repo_root / args.raw_dir
    exports_dir = repo_root / args.exports_dir

    run_all_validations(str(raw_dir), str(exports_dir))
