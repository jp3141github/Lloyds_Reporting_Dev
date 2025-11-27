"""
Lloyd's Reporting Configuration and Constants
==============================================

This module contains shared constants, configuration values, and reference data
used across the Lloyd's reporting toolkit. Centralizing these values ensures
consistency and makes maintenance easier.

Usage:
------
    from lloyds_reporting.config import SYNDICATES, CLASSES_OF_BUSINESS
    from lloyds_reporting.config import DevelopmentFactors, CapitalRatios

Sections:
---------
1. Random Seeds and Reproducibility
2. Syndicate Information
3. Classes of Business (LOB)
4. Risk and Catastrophe Codes
5. Currency Configuration
6. Development Patterns and Factors
7. Capital and Solvency Ratios
8. Date and Period Configuration
9. RRA/RRQ Form Configuration
10. QRT Template Configuration
"""

from datetime import datetime
from typing import Dict, List, Tuple

# =============================================================================
# 1. RANDOM SEEDS AND REPRODUCIBILITY
# =============================================================================

# Standard random seed for reproducible synthetic data generation
# Used across all generators for consistent test data
RANDOM_SEED: int = 42


# =============================================================================
# 2. SYNDICATE INFORMATION
# =============================================================================

# Primary syndicate list for RRA/RRQ reporting
# These are realistic Lloyd's syndicate numbers used in synthetic data
SYNDICATES_PRIMARY: List[int] = [
    2987, 33, 1183, 2791, 623, 4242, 5000, 1910, 2010, 2525
]

# Alternative syndicate list for claims data
# Used in synthetic_data/generate_synthetic_data.py
SYNDICATES_CLAIMS: List[int] = [
    123, 456, 789, 1001, 2468, 3579, 4321, 5678
]

# Syndicate details for liquidity reporting
# Used in data/generate_synthetic_data.py
SYNDICATES_LIQUIDITY: List[Dict[str, str]] = [
    {"number": 2001, "name": "Alpha Syndicate", "agent": "Alpha Managing Agents Ltd"},
    {"number": 2002, "name": "Beta Syndicate", "agent": "Beta Insurance Management"},
    {"number": 2003, "name": "Gamma Syndicate", "agent": "Gamma Underwriting Ltd"},
    {"number": 2004, "name": "Delta Syndicate", "agent": "Delta Risk Services"},
    {"number": 2005, "name": "Epsilon Syndicate", "agent": "Epsilon Capital Management"},
]

# Default syndicate for single-syndicate operations
DEFAULT_SYNDICATE: int = 2001


# =============================================================================
# 3. CLASSES OF BUSINESS (LOB)
# =============================================================================

# Lloyd's Syndicate Classes of Business (SCOB)
# Reference: Lloyd's Market Bulletin Y5381
CLASSES_OF_BUSINESS: Dict[str, str] = {
    'A1': 'Direct Accident & Health',
    'A2': 'Accident & Health Reinsurance',
    'D1': 'Direct Motor (Private Car)',
    'D2': 'Direct Motor (Commercial)',
    'E1': 'Energy Offshore',
    'E2': 'Energy Onshore',
    'F1': 'Fire & Other Damage - Direct',
    'F2': 'Fire & Other Damage - Reinsurance',
    'M1': 'Marine Cargo',
    'M2': 'Marine Hull',
    'M3': 'Marine Liability',
    'N1': 'Non-Marine Property Treaty',
    'N2': 'Non-Marine Property Facultative',
    'P1': 'Professional Indemnity',
    'P2': 'Public & Products Liability',
    'T1': 'Third Party Liability - Direct',
    'T2': 'Third Party Liability - Reinsurance',
    'V1': 'Aviation',
    'W1': 'Political Risk & Contingency',
    'X1': 'Catastrophe Reinsurance',
}

# Solvency II Risk Codes
# Reference: Delegated Regulation (EU) 2015/35
SOLVENCY_II_RISK_CODES: Dict[str, str] = {
    '1': 'Accident & Health',
    '2': 'Motor (Third Party Liability)',
    '3': 'Motor (Other Classes)',
    '4': 'Marine, Aviation, Transport',
    '5': 'Fire & Other Property Damage',
    '6': 'Third Party Liability',
    '7': 'Credit & Suretyship',
    '8': 'Legal Expenses',
    '9': 'Assistance',
    '1E': 'Life',
    '1T': 'Life Treaty',
    '2E': 'Accident Treaty',
    '2T': 'Accident & Health Treaty',
    '3E': 'Motor Treaty',
    '3T': 'Motor Other Treaty',
    '4E': 'Marine Aviation Transport Treaty',
    '4T': 'Marine Treaty',
    '5T': 'Property Treaty',
    '6T': 'Third Party Liability Treaty',
    '7T': 'Credit Treaty',
    '8T': 'Legal Expenses Treaty',
    'AO': 'Aviation Other',
    'AP': 'Aviation Passengers',
    'AW': 'Aviation War',
    'cf': 'Casualty Fire',
}


# =============================================================================
# 4. RISK AND CATASTROPHE CODES
# =============================================================================

# Internal risk classification codes
RISK_CODES: Dict[str, str] = {
    'RC01': 'Attritional',
    'RC02': 'Large Loss',
    'RC03': 'Catastrophe - Natural',
    'RC04': 'Catastrophe - Man-made',
    'RC05': 'Reserve Development',
}

# Catastrophe event codes
# Reference: Lloyd's Realistic Disaster Scenarios (RDS)
CATASTROPHE_CODES: Dict[str, str] = {
    # Natural catastrophes
    'NAT01': 'Hurricane - USA',
    'NAT02': 'Earthquake - Japan',
    'NAT03': 'Flood - Europe',
    'NAT04': 'Windstorm - Europe',
    'NAT05': 'Wildfire - USA',
    # Man-made catastrophes
    'MAN01': 'Cyber Attack',
    'MAN02': 'Industrial Accident',
    'MAN03': 'Aviation Accident',
}

# Development pattern classifications
DEVELOPMENT_PATTERNS: List[str] = [
    'Short Tail',    # 1-3 years to ultimate
    'Medium Tail',   # 3-7 years to ultimate
    'Long Tail',     # 7+ years to ultimate
]

# Actuarial methods
ACTUARIAL_METHODS: List[str] = [
    'Chain Ladder',
    'BF Method',           # Bornhuetter-Ferguson
    'Cape Cod',
    'Expected Loss Ratio',
]


# =============================================================================
# 5. CURRENCY CONFIGURATION
# =============================================================================

# Primary reporting currencies
CURRENCIES: List[str] = ['GBP', 'USD', 'EUR', 'CAD', 'AUD', 'JPY', 'CHF']

# Base currency for Lloyd's reporting
BASE_CURRENCY: str = 'GBP'

# Base exchange rates (against GBP)
# Reference: Lloyd's exchange rates as at 2024-12-31
BASE_EXCHANGE_RATES: Dict[str, float] = {
    'GBP': 1.00,
    'USD': 1.27,
    'EUR': 1.17,
    'CAD': 1.72,
    'AUD': 1.95,
    'JPY': 188.5,
    'CHF': 1.12,
}


# =============================================================================
# 6. DEVELOPMENT PATTERNS AND FACTORS
# =============================================================================

class DevelopmentFactors:
    """
    Claims development factors and patterns.

    These factors represent typical development patterns for Lloyd's
    claims data. Based on industry standards and Lloyd's market data.
    """

    # Initial development factor at inception
    # Represents proportion of ultimate claims recognized at development year 0
    INITIAL_FACTOR: float = 0.20

    # Annual development increment
    # Typical year-over-year development for medium-tail business
    ANNUAL_INCREMENT: float = 0.15

    # Maximum development factor (claims fully developed)
    MAX_FACTOR: float = 1.0

    # Development year ranges by tail type
    SHORT_TAIL_YEARS: int = 3
    MEDIUM_TAIL_YEARS: int = 7
    LONG_TAIL_YEARS: int = 15

    # Typical loss ratio ranges by development stage
    INITIAL_LOSS_RATIO_RANGE: Tuple[float, float] = (0.45, 0.85)
    ULTIMATE_LOSS_RATIO_RANGE: Tuple[float, float] = (0.55, 0.75)

    @classmethod
    def calculate_factor(cls, development_year: int) -> float:
        """Calculate development factor for a given development year."""
        return min(cls.MAX_FACTOR, cls.INITIAL_FACTOR + (development_year * cls.ANNUAL_INCREMENT))


# =============================================================================
# 7. CAPITAL AND SOLVENCY RATIOS
# =============================================================================

class CapitalRatios:
    """
    Lloyd's and Solvency II capital ratio parameters.

    Reference:
    - Lloyd's Minimum Standards MS7 (Capital)
    - Solvency II Delegated Regulation
    """

    # Funds in Syndicate (FIS) as percentage of Funds at Lloyd's (FAL)
    # Typical range: 80-95%
    FIS_TO_FAL_RANGE: Tuple[float, float] = (0.80, 0.95)

    # Undiscounted SCR as percentage of FAL
    # Typical range: 60-85%
    USCR_TO_FAL_RANGE: Tuple[float, float] = (0.60, 0.85)

    # Undiscounted ECA as percentage of FAL
    # Typical range: 10-20%
    UECA_TO_FAL_RANGE: Tuple[float, float] = (0.10, 0.20)

    # FAL range (GBP millions)
    FAL_RANGE_GBP: Tuple[int, int] = (100_000_000, 500_000_000)

    # Solvency coverage ratio targets
    LLOYDS_MINIMUM_COVERAGE: float = 1.0    # 100%
    LLOYDS_TARGET_COVERAGE: float = 1.35    # 135%
    LLOYDS_STRONG_COVERAGE: float = 1.50    # 150%

    # Risk margin cost of capital rates
    SOLVENCY_II_COC_RATE: float = 0.04      # 4% (Solvency II standard)
    LLOYDS_COC_RATE: float = 0.06           # 6% (Lloyd's standard)


class LiquidityRatios:
    """
    Lloyd's liquidity stress test parameters.

    Reference: Lloyd's Liquidity Risk Framework
    """

    # Asset allocation ranges as percentage of FAL

    # Restricted assets (US Trust Funds, etc.)
    US_TRUST_FUNDS_RANGE: Tuple[float, float] = (0.20, 0.30)
    OTHER_TRUST_FUNDS_RANGE: Tuple[float, float] = (0.05, 0.10)
    OTHER_RESTRICTED_RANGE: Tuple[float, float] = (0.02, 0.05)

    # Illiquid assets
    REINSURANCE_RECOVERABLES_RANGE: Tuple[float, float] = (0.15, 0.25)
    REINSURER_URP_RANGE: Tuple[float, float] = (0.08, 0.12)
    OTHER_ILLIQUID_RANGE: Tuple[float, float] = (0.02, 0.05)

    # Liquid assets
    FREE_FUNDS_RANGE: Tuple[float, float] = (0.15, 0.25)
    OTHER_LIQUID_RANGE: Tuple[float, float] = (0.05, 0.15)

    # 1-in-200 stress scenario parameters
    GROSS_LOSS_MULTIPLIER_RANGE: Tuple[float, float] = (1.5, 2.5)  # x FAL
    REINSURANCE_RECOVERY_RANGE: Tuple[float, float] = (0.40, 0.70)  # of gross loss
    DISPUTED_RECOVERY_RANGE: Tuple[float, float] = (0.15, 0.30)  # of RI recovery


class ReserveRatios:
    """
    Reserve and IBNR parameters.
    """

    # ULAE (Unallocated Loss Adjustment Expenses) ratio range
    ULAE_RATIO_RANGE: Tuple[float, float] = (0.03, 0.08)

    # Internal vs external cost split for ULAE
    ULAE_INTERNAL_SPLIT: float = 0.60
    ULAE_EXTERNAL_SPLIT: float = 0.40

    # Reinsurance recovery ranges
    RI_RECOVERY_RANGE: Tuple[float, float] = (0.10, 0.25)

    # Retention ratios (Net/Gross premium)
    RETENTION_RATIO_RANGE: Tuple[float, float] = (0.75, 0.90)


# =============================================================================
# 8. DATE AND PERIOD CONFIGURATION
# =============================================================================

# Current reporting year
CURRENT_YEAR: int = datetime.now().year

# Years of Account range for reporting
YEARS_OF_ACCOUNT: List[int] = list(range(2018, CURRENT_YEAR + 2))

# Quarters for quarterly reporting
QUARTERS: List[str] = ['Q1', 'Q2', 'Q3', 'Q4']

# Quarter end dates (month, day)
QUARTER_END_DATES: Dict[str, Tuple[int, int]] = {
    'Q1': (3, 31),
    'Q2': (6, 30),
    'Q3': (9, 30),
    'Q4': (12, 31),
}

# Reporting periods for liquidity analysis
LIQUIDITY_QUARTERS: List[str] = [
    '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30', '2025-12-31'
]


# =============================================================================
# 9. RRA/RRQ FORM CONFIGURATION
# =============================================================================

# RRA form codes and descriptions
RRA_FORMS: Dict[str, str] = {
    '010': 'Control Data',
    '020': 'Exchange Rates',
    '071': 'SCOB Mapping',
    '081': 'Reserving Class Information',
    '091': 'LPT Data',
    '193': 'Net Claims Development',
    '291': 'Gross Premium and IBNR',
    '292': 'Net Premium and IBNR',
    '293': 'Outstanding & IBNR by PYoA',
    '294': 'Catastrophe IBNR',
    '295': 'ULAE',
    '391': 'IELR',
    '910': 'Additional Information',
    '990': 'Validation Summary',
}

# RRQ form codes (subset of RRA)
RRQ_FORMS: Dict[str, str] = {
    '010': 'Control Data',
    '020': 'Exchange Rates',
    '193': 'Net Claims Development',
    '291': 'Gross Premium and IBNR',
}

# Form validation statuses
VALIDATION_STATUSES: List[str] = [
    'Pass',
    'Pass with Warnings',
    'Review Required',
]

# Return types
RETURN_TYPES: List[str] = ['RRA', 'RRQ']


# =============================================================================
# 10. QRT TEMPLATE CONFIGURATION
# =============================================================================

# QRT template prefixes and their categories
QRT_CATEGORIES: Dict[str, str] = {
    'IR01': 'Basic Information',
    'IR02': 'Balance Sheet',
    'IR03': 'Off-Balance Sheet',
    'IR05': 'Premiums, Claims, Expenses',
    'IR06': 'Assets',
    'IR08': 'Derivatives',
    'IR09': 'Income/Gains/Losses',
    'IR12': 'Life Technical Provisions',
    'IR16': 'Non-Life Annuities',
    'IR17': 'Non-Life Technical Provisions',
    'IR18': 'Non-Life Cash Flows',
    'IR19': 'Non-Life Claims',
    'IR20': 'Claims Development',
    'IR21': 'Underwriting Risk',
    'IR22': 'LTG Measures',
    'IR23': 'Own Funds',
    'IR24': 'Participations',
    'IR25': 'SCR Overview',
    'IR26': 'SCR Risk Modules',
    'IR27': 'Catastrophe Risk',
    'IR28': 'MCR',
    'IR30': 'Reinsurance',
    'IR32': 'Group Scope',
    'IR33': 'Individual Requirements',
    'IR34': 'Other Undertakings',
    'IR35': 'Group Technical Provisions',
    'IR36': 'Intra-Group Transactions',
}


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Seeds
    'RANDOM_SEED',

    # Syndicates
    'SYNDICATES_PRIMARY',
    'SYNDICATES_CLAIMS',
    'SYNDICATES_LIQUIDITY',
    'DEFAULT_SYNDICATE',

    # Classes of Business
    'CLASSES_OF_BUSINESS',
    'SOLVENCY_II_RISK_CODES',

    # Risk codes
    'RISK_CODES',
    'CATASTROPHE_CODES',
    'DEVELOPMENT_PATTERNS',
    'ACTUARIAL_METHODS',

    # Currency
    'CURRENCIES',
    'BASE_CURRENCY',
    'BASE_EXCHANGE_RATES',

    # Factors and Ratios
    'DevelopmentFactors',
    'CapitalRatios',
    'LiquidityRatios',
    'ReserveRatios',

    # Dates
    'CURRENT_YEAR',
    'YEARS_OF_ACCOUNT',
    'QUARTERS',
    'QUARTER_END_DATES',
    'LIQUIDITY_QUARTERS',

    # Forms
    'RRA_FORMS',
    'RRQ_FORMS',
    'VALIDATION_STATUSES',
    'RETURN_TYPES',

    # QRTs
    'QRT_CATEGORIES',
]
