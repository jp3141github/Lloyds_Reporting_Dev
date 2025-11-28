"""
Data Validator
==============

Common validation utilities for Lloyd's regulatory data.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

import pandas as pd
import numpy as np


class ValidationLevel(Enum):
    """Validation result severity levels."""
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'
    PASS = 'PASS'


@dataclass
class ValidationResult:
    """Result of a validation check."""
    check_name: str
    level: ValidationLevel
    message: str
    column: Optional[str] = None
    row_count: int = 0
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'check': self.check_name,
            'level': self.level.value,
            'message': self.message,
            'column': self.column,
            'row_count': self.row_count,
            'details': self.details,
        }


class DataValidator:
    """
    Validate Lloyd's regulatory reporting data.

    Provides comprehensive validation checks for data quality,
    completeness, and regulatory compliance.
    """

    # Required columns by data type
    REQUIRED_COLUMNS = {
        'syndicate_data': ['syndicate', 'year_of_account'],
        'claims_data': ['claim_id', 'incurred_amount', 'paid_amount'],
        'capital_data': ['syndicate', 'fal', 'fis'],
        'solvency_data': ['syndicate', 'scr', 'mcr'],
    }

    # Valid ranges for key metrics
    VALID_RANGES = {
        'syndicate': (1, 9999),
        'year_of_account': (1990, 2030),
        'percentage': (0, 1),
        'ratio': (0, 10),
        'amount': (0, 1e12),
    }

    def __init__(self):
        """Initialize validator."""
        self.results: List[ValidationResult] = []

    def validate(self, df: pd.DataFrame, data_type: Optional[str] = None) -> List[ValidationResult]:
        """
        Run all validation checks on a DataFrame.

        Args:
            df: DataFrame to validate
            data_type: Optional data type for specific checks

        Returns:
            List of validation results
        """
        self.results = []

        # Basic checks
        self._check_empty(df)
        self._check_duplicates(df)
        self._check_null_values(df)

        # Type-specific checks
        if data_type and data_type in self.REQUIRED_COLUMNS:
            self._check_required_columns(df, self.REQUIRED_COLUMNS[data_type])

        # Column-specific checks
        self._check_numeric_columns(df)
        self._check_syndicate_column(df)
        self._check_year_column(df)

        # Add overall result if no issues
        if not self.results:
            self.results.append(ValidationResult(
                check_name='overall',
                level=ValidationLevel.PASS,
                message='All validation checks passed',
            ))

        return self.results

    def _check_empty(self, df: pd.DataFrame):
        """Check if DataFrame is empty."""
        if df.empty:
            self.results.append(ValidationResult(
                check_name='empty_data',
                level=ValidationLevel.ERROR,
                message='DataFrame is empty',
            ))

    def _check_duplicates(self, df: pd.DataFrame):
        """Check for duplicate rows."""
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            self.results.append(ValidationResult(
                check_name='duplicates',
                level=ValidationLevel.WARNING,
                message=f'{dup_count} duplicate rows found',
                row_count=dup_count,
            ))

    def _check_null_values(self, df: pd.DataFrame):
        """Check for null values in each column."""
        for col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                pct = null_count / len(df) * 100
                level = ValidationLevel.ERROR if pct > 50 else ValidationLevel.WARNING
                self.results.append(ValidationResult(
                    check_name='null_values',
                    level=level,
                    message=f'{null_count} null values ({pct:.1f}%)',
                    column=col,
                    row_count=null_count,
                ))

    def _check_required_columns(self, df: pd.DataFrame, required: List[str]):
        """Check for required columns."""
        missing = [col for col in required if col not in df.columns]
        if missing:
            self.results.append(ValidationResult(
                check_name='missing_columns',
                level=ValidationLevel.ERROR,
                message=f'Missing required columns: {missing}',
                details={'missing_columns': missing},
            ))

    def _check_numeric_columns(self, df: pd.DataFrame):
        """Check numeric columns for invalid values."""
        for col in df.select_dtypes(include=[np.number]).columns:
            # Check for negative values where unexpected
            if 'amount' in col.lower() or 'value' in col.lower():
                neg_count = (df[col] < 0).sum()
                if neg_count > 0:
                    self.results.append(ValidationResult(
                        check_name='negative_amounts',
                        level=ValidationLevel.INFO,
                        message=f'{neg_count} negative values',
                        column=col,
                        row_count=neg_count,
                    ))

            # Check for outliers (beyond 3 standard deviations)
            if len(df[col].dropna()) > 0:
                mean = df[col].mean()
                std = df[col].std()
                if std > 0:
                    outliers = ((df[col] - mean).abs() > 3 * std).sum()
                    if outliers > 0:
                        self.results.append(ValidationResult(
                            check_name='outliers',
                            level=ValidationLevel.INFO,
                            message=f'{outliers} potential outliers (>3 std)',
                            column=col,
                            row_count=outliers,
                        ))

    def _check_syndicate_column(self, df: pd.DataFrame):
        """Check syndicate number validity."""
        syndicate_cols = ['syndicate', 'syndicate_number', 'syndicate_id']
        for col in syndicate_cols:
            if col in df.columns:
                min_val, max_val = self.VALID_RANGES['syndicate']
                invalid = ((df[col] < min_val) | (df[col] > max_val)).sum()
                if invalid > 0:
                    self.results.append(ValidationResult(
                        check_name='invalid_syndicate',
                        level=ValidationLevel.ERROR,
                        message=f'{invalid} syndicates outside valid range ({min_val}-{max_val})',
                        column=col,
                        row_count=invalid,
                    ))

    def _check_year_column(self, df: pd.DataFrame):
        """Check year of account validity."""
        year_cols = ['year', 'year_of_account', 'yoa']
        for col in year_cols:
            if col in df.columns:
                min_val, max_val = self.VALID_RANGES['year_of_account']
                invalid = ((df[col] < min_val) | (df[col] > max_val)).sum()
                if invalid > 0:
                    self.results.append(ValidationResult(
                        check_name='invalid_year',
                        level=ValidationLevel.WARNING,
                        message=f'{invalid} years outside typical range ({min_val}-{max_val})',
                        column=col,
                        row_count=invalid,
                    ))

    def check_cross_table_consistency(self, tables: Dict[str, pd.DataFrame]) -> List[ValidationResult]:
        """
        Check consistency across multiple tables.

        Args:
            tables: Dictionary of table name to DataFrame

        Returns:
            List of validation results
        """
        results = []

        # Find common columns across tables
        syndicates_by_table = {}
        years_by_table = {}

        for name, df in tables.items():
            # Extract syndicates
            for col in ['syndicate', 'syndicate_number']:
                if col in df.columns:
                    syndicates_by_table[name] = set(df[col].unique())
                    break

            # Extract years
            for col in ['year', 'year_of_account', 'yoa']:
                if col in df.columns:
                    years_by_table[name] = set(df[col].unique())
                    break

        # Check syndicate consistency
        if len(syndicates_by_table) > 1:
            all_syndicates = set.union(*syndicates_by_table.values())
            for name, syndicates in syndicates_by_table.items():
                missing = all_syndicates - syndicates
                if missing:
                    results.append(ValidationResult(
                        check_name='syndicate_consistency',
                        level=ValidationLevel.INFO,
                        message=f'Table {name} missing syndicates: {sorted(missing)[:5]}...',
                        details={'table': name, 'missing_count': len(missing)},
                    ))

        return results

    def get_summary(self) -> pd.DataFrame:
        """Get validation results as a DataFrame."""
        if not self.results:
            return pd.DataFrame()
        return pd.DataFrame([r.to_dict() for r in self.results])

    def has_errors(self) -> bool:
        """Check if any errors were found."""
        return any(r.level == ValidationLevel.ERROR for r in self.results)

    def has_warnings(self) -> bool:
        """Check if any warnings were found."""
        return any(r.level == ValidationLevel.WARNING for r in self.results)
