"""
Lloyd's QAD (Quarterly Asset Data) - Power BI Synthetic Data Generator
======================================================================

Generates synthetic data for QAD forms (quarterly version of AAD).

Forms Covered:
- QAD 230: Asset Valuation (S.06.02.01)
- QAD 233: Derivatives (S.08.01.01)
- QAD 235: Derivatives Income (S.09.01.01)
- QAD 236: Collective Investment Look-Through (S.06.03.01)
- QAD 237: Securities Lending (S.10.01.01)
- QAD 238: Assets as Collateral (S.11.01.01)

Note: QAD is submitted quarterly via CMR. Due to data volume, it's an
asynchronous return with playback summaries.

Usage in Power BI:
    Get Data > Python script > Paste entire file contents

Author: Lloyd's Reporting Development Team
Version: 1.0
Date: 2024-11-23
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# =============================================================================
# CONFIGURATION
# =============================================================================

SYNDICATES = [33, 623, 1183, 1910, 2010, 2525, 2791, 2987, 4242, 5000]
REPORTING_YEAR = 2024
QUARTER = 3  # Q1, Q2, Q3, or Q4

# Quarter end dates
QUARTER_ENDS = {
    1: '03-31', 2: '06-30', 3: '09-30', 4: '12-31'
}
AS_AT_DATE = f'{REPORTING_YEAR}-{QUARTER_ENDS[QUARTER]}'

# CIC (Complementary Identification Code) categories
CIC_CODES = {
    'Government bonds': ['11', '12', '13', '14', '15', '16', '17', '18', '19'],
    'Corporate bonds': ['21', '22', '23', '24', '25', '26', '27', '28', '29'],
    'Equities': ['31', '32', '33', '34'],
    'Collective investments': ['41', '42', '43', '44', '45', '46', '47', '48', '49'],
    'Structured notes': ['51', '52', '53', '54', '55', '56', '57', '58', '59'],
    'Collateralised securities': ['61', '62', '63', '64', '65', '66', '67', '68', '69'],
    'Cash': ['71', '72', '79'],
    'Mortgages and loans': ['81', '82', '83', '84', '85', '86', '87', '88', '89'],
    'Property': ['91', '92', '93', '94', '95', '96', '99'],
    'Derivatives': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                   'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'C1', 'C2', 'D1', 'D2', 'E1', 'E2', 'F1', 'F2']
}

# ID Code Types
ID_CODE_TYPES = ['ISIN', 'CUSIP', 'SEDOL', 'Bloomberg', 'LMIF', 'Internal']

# Countries
COUNTRIES = ['GB', 'US', 'DE', 'FR', 'JP', 'CH', 'NL', 'IE', 'LU', 'CA', 'AU']

# NACE Codes (industry sectors)
NACE_CODES = ['K64', 'K65', 'K66', 'C10', 'C20', 'D35', 'F41', 'G46', 'H49', 'J61', 'M69']

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_isin():
    """Generate a random ISIN"""
    country = random.choice(['GB', 'US', 'DE', 'FR', 'JP', 'CH'])
    chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    check = random.randint(0, 9)
    return f"{country}{chars}{check}"

def generate_cusip():
    """Generate a random CUSIP"""
    chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    check = random.randint(0, 9)
    return f"{chars}{check}"

def generate_lmif_code():
    """Generate Lloyd's Managed Investment Fund code"""
    return f"LMIF{random.randint(1000, 9999)}"

# =============================================================================
# QAD 230 - ASSET VALUATION (S.06.02.01)
# =============================================================================

def generate_qad_230():
    """Generate detailed asset valuation at security level"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        num_securities = int(np.random.uniform(200, 500))

        for i in range(num_securities):
            asset_category = random.choice(list(CIC_CODES.keys()))
            if asset_category == 'Derivatives':
                continue  # Derivatives in separate form

            cic_code = random.choice(CIC_CODES[asset_category])
            country = random.choice(COUNTRIES)
            id_type = random.choice(['ISIN', 'CUSIP', 'SEDOL', 'Internal'])

            if id_type == 'ISIN':
                id_code = generate_isin()
            elif id_type == 'CUSIP':
                id_code = generate_cusip()
            else:
                id_code = f"{id_type[:3].upper()}{random.randint(100000, 999999)}"

            par_value = np.random.uniform(100, 10000) * scale * 1e3
            market_value = par_value * np.random.uniform(0.9, 1.15)
            accrued_interest = market_value * np.random.uniform(0, 0.03) if 'bond' in asset_category.lower() else 0

            row = {
                'syndicate': syn,
                'as_at_date': AS_AT_DATE,
                'quarter': f'Q{QUARTER}',
                'reporting_year': REPORTING_YEAR,
                'asset_id': f'AST-{syn}-{i+1:05d}',
                'id_code': id_code,
                'id_code_type': id_type,
                'asset_category': asset_category,
                'cic_code': f'{country}{cic_code}',
                'currency': random.choice(['GBP', 'USD', 'EUR', 'JPY', 'CHF']),
                'country_of_issue': country,
                'issuer_name': f'Issuer {random.randint(1, 500)}',
                'issuer_sector': random.choice(NACE_CODES),
                'issuer_group': f'Group {random.randint(1, 100)}',
                'external_rating': random.choice(['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-', 'NR']),
                'nominated_ecai': random.choice(['S&P', 'Moodys', 'Fitch', 'AM Best']),
                'credit_quality_step': random.randint(0, 6),
                'par_amount': par_value,
                'acquisition_cost': par_value * np.random.uniform(0.95, 1.05),
                'solvency_ii_value': market_value,
                'accrued_interest': accrued_interest,
                'total_value': market_value + accrued_interest,
                'maturity_date': f'{random.randint(2025, 2054)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}' if 'bond' in asset_category.lower() else None,
                'coupon_rate': np.random.uniform(0.5, 6.0) if 'bond' in asset_category.lower() else None,
                'duration': np.random.uniform(1, 15) if 'bond' in asset_category.lower() else None,
                'unit_quantity': np.random.uniform(1000, 100000) if asset_category == 'Equities' else None,
                'unit_price': market_value / np.random.uniform(1000, 100000) if asset_category == 'Equities' else None
            }
            data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# QAD 233 - DERIVATIVES (S.08.01.01)
# =============================================================================

def generate_qad_233():
    """Generate derivatives positions"""
    data = []
    derivative_types = ['Futures', 'Options', 'Swaps', 'Forwards', 'Credit derivatives']
    purposes = ['Hedging', 'Efficient portfolio management', 'Reducing risk']

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        num_derivatives = int(np.random.uniform(20, 80))

        for i in range(num_derivatives):
            deriv_type = random.choice(derivative_types)
            notional = np.random.uniform(5, 100) * scale * 1e6
            market_value = notional * np.random.uniform(-0.1, 0.1)

            # Determine CIC code based on type
            if deriv_type == 'Futures':
                cic = 'A1'
            elif deriv_type == 'Options':
                cic = random.choice(['B1', 'B2', 'B3'])
            elif deriv_type == 'Swaps':
                cic = random.choice(['D1', 'D2'])
            elif deriv_type == 'Forwards':
                cic = random.choice(['E1', 'E2'])
            else:
                cic = random.choice(['F1', 'F2'])

            row = {
                'syndicate': syn,
                'as_at_date': AS_AT_DATE,
                'quarter': f'Q{QUARTER}',
                'derivative_id': f'DRV-{syn}-{i+1:04d}',
                'id_code': f'DRV{generate_isin()}',
                'id_code_type': 'Internal',
                'derivative_type': deriv_type,
                'cic_code': f'GB{cic}',
                'counterparty_name': f'Bank {random.randint(1, 50)}',
                'counterparty_code': f'LEI{random.randint(10000000, 99999999)}',
                'counterparty_rating': random.choice(['AA+', 'AA', 'AA-', 'A+', 'A', 'A-']),
                'counterparty_group': f'Banking Group {random.randint(1, 20)}',
                'contract_currency': random.choice(['GBP', 'USD', 'EUR']),
                'notional_amount': notional,
                'purchase_price': abs(market_value) * np.random.uniform(0.8, 1.2),
                'solvency_ii_value': market_value,
                'underlying_asset_category': random.choice(['Interest rate', 'Equity', 'Currency', 'Credit', 'Commodity']),
                'underlying_asset': f'Underlying {random.randint(1, 100)}',
                'strike_price': np.random.uniform(80, 120) if deriv_type == 'Options' else None,
                'maturity_date': f'{random.randint(2025, 2030)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}',
                'trigger_event': 'None' if deriv_type != 'Credit derivatives' else 'Default',
                'use_of_derivative': random.choice(purposes),
                'delta': np.random.uniform(0.3, 0.9) if deriv_type == 'Options' else 1.0,
                'hedge_effectiveness': np.random.uniform(80, 100) if 'Hedging' in purposes else None
            }
            data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# QAD 235 - DERIVATIVES INCOME (S.09.01.01)
# =============================================================================

def generate_qad_235():
    """Generate derivatives income analysis"""
    data = []
    derivative_types = ['Futures', 'Options', 'Swaps', 'Forwards', 'Credit derivatives']

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        for deriv_type in derivative_types:
            num_transactions = int(np.random.uniform(5, 20))
            total_notional = np.random.uniform(50, 300) * scale * 1e6

            realised_pnl = total_notional * np.random.uniform(-0.05, 0.08)
            unrealised_pnl = total_notional * np.random.uniform(-0.03, 0.05)

            row = {
                'syndicate': syn,
                'as_at_date': AS_AT_DATE,
                'quarter': f'Q{QUARTER}',
                'derivative_type': deriv_type,
                'number_of_contracts': num_transactions,
                'total_notional_opening': total_notional * 0.9,
                'new_contracts_notional': total_notional * 0.3,
                'matured_contracts_notional': total_notional * 0.2,
                'total_notional_closing': total_notional,
                'realised_gains': max(realised_pnl, 0),
                'realised_losses': abs(min(realised_pnl, 0)),
                'net_realised_pnl': realised_pnl,
                'unrealised_gains': max(unrealised_pnl, 0),
                'unrealised_losses': abs(min(unrealised_pnl, 0)),
                'net_unrealised_pnl': unrealised_pnl,
                'total_pnl': realised_pnl + unrealised_pnl,
                'premium_received': abs(realised_pnl) * 0.1 if deriv_type == 'Options' else 0,
                'premium_paid': abs(realised_pnl) * 0.05 if deriv_type == 'Options' else 0
            }
            data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# QAD 236 - COLLECTIVE INVESTMENT LOOK-THROUGH (S.06.03.01)
# =============================================================================

def generate_qad_236():
    """Generate CIU look-through data"""
    data = []
    fund_types = ['Equity fund', 'Bond fund', 'Mixed fund', 'Money market fund',
                  'Real estate fund', 'Alternative fund', 'Infrastructure fund']

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        num_funds = int(np.random.uniform(15, 40))

        for i in range(num_funds):
            fund_type = random.choice(fund_types)
            is_lmif = random.random() < 0.3  # 30% are Lloyd's Managed Investment Funds

            total_value = np.random.uniform(5, 50) * scale * 1e6

            # Look-through allocation
            equity_pct = np.random.uniform(0, 0.8) if 'Equity' in fund_type or 'Mixed' in fund_type else 0
            bond_pct = np.random.uniform(0, 0.8) if 'Bond' in fund_type or 'Mixed' in fund_type else 0
            property_pct = np.random.uniform(0, 0.3) if 'Real estate' in fund_type else 0
            cash_pct = 1 - equity_pct - bond_pct - property_pct
            if cash_pct < 0:
                total = equity_pct + bond_pct + property_pct
                equity_pct /= total
                bond_pct /= total
                property_pct /= total
                cash_pct = 0

            row = {
                'syndicate': syn,
                'as_at_date': AS_AT_DATE,
                'quarter': f'Q{QUARTER}',
                'fund_id': f'CIU-{syn}-{i+1:04d}',
                'fund_name': f'{fund_type} Fund {i+1}',
                'fund_manager': f'Asset Manager {random.randint(1, 30)}',
                'id_code': generate_lmif_code() if is_lmif else generate_isin(),
                'id_code_type': 'LMIF' if is_lmif else 'ISIN',
                'cic_code': 'GBXL39' if is_lmif else f'GB4{random.randint(1, 9)}',
                'level_of_look_through': 'O' if is_lmif else random.choice(['1', '2', '3']),
                'fund_currency': random.choice(['GBP', 'USD', 'EUR']),
                'country_of_issue': random.choice(COUNTRIES),
                'fund_type': fund_type,
                'total_solvency_ii_value': total_value,
                'units_held': np.random.uniform(10000, 500000),
                'unit_nav': total_value / np.random.uniform(10000, 500000),
                # Look-through allocation
                'equity_allocation_pct': equity_pct * 100,
                'bond_allocation_pct': bond_pct * 100,
                'property_allocation_pct': property_pct * 100,
                'cash_allocation_pct': cash_pct * 100,
                'equity_value': total_value * equity_pct,
                'bond_value': total_value * bond_pct,
                'property_value': total_value * property_pct,
                'cash_value': total_value * cash_pct,
                # Risk metrics
                'average_credit_quality': random.randint(1, 5),
                'average_duration': np.random.uniform(2, 8) if bond_pct > 0 else None,
                'is_lmif': is_lmif
            }
            data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# QAD 237 - SECURITIES LENDING (S.10.01.01)
# =============================================================================

def generate_qad_237():
    """Generate securities lending and repo data"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        num_transactions = int(np.random.uniform(5, 25))

        for i in range(num_transactions):
            transaction_type = random.choice(['Securities lending', 'Repo', 'Reverse repo'])
            collateral_value = np.random.uniform(10, 100) * scale * 1e6

            row = {
                'syndicate': syn,
                'as_at_date': AS_AT_DATE,
                'quarter': f'Q{QUARTER}',
                'transaction_id': f'SL-{syn}-{i+1:04d}',
                'transaction_type': transaction_type,
                'counterparty_name': f'Prime Broker {random.randint(1, 20)}',
                'counterparty_lei': f'LEI{random.randint(10000000, 99999999)}',
                'counterparty_rating': random.choice(['AA+', 'AA', 'AA-', 'A+', 'A']),
                'security_lent_id': generate_isin(),
                'security_lent_type': random.choice(['Government bond', 'Corporate bond', 'Equity']),
                'security_lent_value': collateral_value * 0.95,
                'collateral_received_type': random.choice(['Cash', 'Government bond', 'Letter of credit']),
                'collateral_received_value': collateral_value,
                'haircut_pct': np.random.uniform(2, 10),
                'collateralisation_ratio': (collateral_value / (collateral_value * 0.95)) * 100,
                'start_date': f'{REPORTING_YEAR}-{random.randint(1,9):02d}-{random.randint(1,28):02d}',
                'maturity_date': f'{REPORTING_YEAR + random.randint(0,1)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}',
                'open_maturity': random.choice([True, False]),
                'fee_rate_bps': np.random.uniform(5, 50),
                'income_ytd': collateral_value * 0.95 * (np.random.uniform(5, 50) / 10000) * (QUARTER / 4)
            }
            data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# QAD 238 - ASSETS AS COLLATERAL (S.11.01.01)
# =============================================================================

def generate_qad_238():
    """Generate assets held as collateral"""
    data = []
    collateral_purposes = ['Derivatives margin', 'Securities lending', 'Repo',
                          'Reinsurance deposit', 'Letter of credit backing']

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)
        num_collateral = int(np.random.uniform(10, 40))

        for i in range(num_collateral):
            purpose = random.choice(collateral_purposes)
            collateral_value = np.random.uniform(5, 50) * scale * 1e6

            row = {
                'syndicate': syn,
                'as_at_date': AS_AT_DATE,
                'quarter': f'Q{QUARTER}',
                'collateral_id': f'COL-{syn}-{i+1:04d}',
                'asset_id': generate_isin(),
                'asset_type': random.choice(['Government bond', 'Corporate bond', 'Cash', 'Equity']),
                'cic_code': f'GB{random.randint(11, 79)}',
                'collateral_holder': f'Counterparty {random.randint(1, 50)}',
                'collateral_holder_lei': f'LEI{random.randint(10000000, 99999999)}',
                'collateral_purpose': purpose,
                'underlying_transaction': f'TXN-{random.randint(10000, 99999)}',
                'par_value': collateral_value * 0.98,
                'market_value': collateral_value,
                'haircut_applied_pct': np.random.uniform(0, 15),
                'value_after_haircut': collateral_value * (1 - np.random.uniform(0, 0.15)),
                'currency': random.choice(['GBP', 'USD', 'EUR']),
                'country_of_custody': random.choice(['GB', 'US', 'LU', 'IE']),
                'custodian_name': f'Custodian Bank {random.randint(1, 10)}',
                'collateral_posted_date': f'{REPORTING_YEAR}-{random.randint(1,12):02d}-{random.randint(1,28):02d}',
                'release_date': None if random.random() < 0.7 else f'{REPORTING_YEAR + 1}-{random.randint(1,12):02d}-{random.randint(1,28):02d}',
                'is_rehypothecatable': random.choice([True, False])
            }
            data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# QAD SUMMARY
# =============================================================================

def generate_qad_summary():
    """Generate QAD summary by syndicate"""
    data = []

    for syn in SYNDICATES:
        scale = np.random.uniform(0.8, 1.5)

        total_investments = np.random.uniform(400, 1200) * scale * 1e6

        row = {
            'syndicate': syn,
            'as_at_date': AS_AT_DATE,
            'quarter': f'Q{QUARTER}',
            'reporting_year': REPORTING_YEAR,
            # Asset totals
            'government_bonds': total_investments * np.random.uniform(0.3, 0.5),
            'corporate_bonds': total_investments * np.random.uniform(0.2, 0.4),
            'equities': total_investments * np.random.uniform(0.05, 0.15),
            'collective_investments': total_investments * np.random.uniform(0.1, 0.2),
            'cash_equivalents': total_investments * np.random.uniform(0.05, 0.1),
            'derivatives_net': np.random.uniform(-10, 20) * scale * 1e6,
            'other_assets': total_investments * np.random.uniform(0.02, 0.05),
            'total_investments': total_investments,
            # Securities lending
            'securities_lent_value': np.random.uniform(20, 100) * scale * 1e6,
            'collateral_received': np.random.uniform(22, 110) * scale * 1e6,
            'securities_lending_income': np.random.uniform(0.1, 0.5) * scale * 1e6,
            # Collateral posted
            'collateral_posted_value': np.random.uniform(30, 150) * scale * 1e6,
            # CIU look-through
            'ciu_count': int(np.random.uniform(15, 40)),
            'ciu_total_value': total_investments * np.random.uniform(0.1, 0.2),
            'ciu_lmif_value': total_investments * np.random.uniform(0.03, 0.08),
            # Derivatives summary
            'derivatives_count': int(np.random.uniform(20, 80)),
            'derivatives_notional': np.random.uniform(200, 800) * scale * 1e6,
            'derivatives_market_value': np.random.uniform(-10, 20) * scale * 1e6
        }
        data.append(row)

    return pd.DataFrame(data)

# =============================================================================
# GENERATE ALL TABLES
# =============================================================================

# QAD Forms
QAD_230_Asset_Valuation = generate_qad_230()
QAD_233_Derivatives = generate_qad_233()
QAD_235_Derivatives_Income = generate_qad_235()
QAD_236_CIU_Look_Through = generate_qad_236()
QAD_237_Securities_Lending = generate_qad_237()
QAD_238_Assets_Collateral = generate_qad_238()

# Summary
QAD_Summary = generate_qad_summary()

# Print confirmation
print(f"QAD Quarterly Asset Data Q{QUARTER} {REPORTING_YEAR}")
print(f"Generated for {len(SYNDICATES)} syndicates")
print(f"Tables: QAD_230, QAD_233, QAD_235, QAD_236, QAD_237, QAD_238, QAD_Summary")
print(f"Total: 7 tables covering all QAD forms")
