"""
Base Data Connector
===================

Common data connection functionality shared between Power BI and KNIME.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

import pandas as pd
import numpy as np


class DataConnector:
    """
    Base data connector for Lloyd's regulatory reporting integrations.

    Provides common data generation and retrieval functionality
    used by both Power BI and KNIME connectors.
    """

    # Supported data categories
    CATEGORIES = {
        'rra': 'Reserving Return Annual',
        'rrq': 'Reserving Return Quarterly',
        'qsr': 'Quarterly Solvency Return',
        'asb': 'Annual Solvency Balance Sheet',
        'lcr': "Lloyd's Capital Return",
        'sbf': 'Syndicate Business Forecast',
        'qma': 'Quarterly Monitoring A',
        'fscs': 'Financial Services Compensation Scheme',
        'liquidity': 'Liquidity Stress Testing',
        'claims': 'Claims Development Analysis',
    }

    # Default configuration
    DEFAULT_CONFIG = {
        'random_seed': 42,
        'base_year': 2024,
        'num_syndicates': 10,
        'years_of_history': 10,
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize data connector.

        Args:
            config: Optional configuration overrides
        """
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        self._setup_random_seed()
        self._datasets: Dict[str, pd.DataFrame] = {}
        self._generation_time: Optional[datetime] = None

    def _setup_random_seed(self):
        """Set random seed for reproducibility."""
        np.random.seed(self.config['random_seed'])

    def get_categories(self) -> Dict[str, str]:
        """Get available data categories."""
        return self.CATEGORIES.copy()

    def generate_syndicates(self, count: Optional[int] = None) -> List[int]:
        """Generate syndicate numbers."""
        count = count or self.config['num_syndicates']
        # Use standard Lloyd's syndicate number ranges
        syndicates = [2987, 33, 1183, 2791, 623, 4242, 5000, 1910, 2010, 2525]
        if count <= len(syndicates):
            return syndicates[:count]
        # Generate additional random syndicates
        extra = np.random.choice(range(1000, 9999), count - len(syndicates), replace=False)
        return syndicates + list(extra)

    def generate_years_of_account(self, years_back: Optional[int] = None) -> List[int]:
        """Generate years of account."""
        years = years_back or self.config['years_of_history']
        base = self.config['base_year']
        return list(range(base - years + 1, base + 1))

    def generate_classes_of_business(self) -> Dict[str, str]:
        """Generate Lloyd's classes of business."""
        return {
            'A1': 'Direct Accident & Health',
            'A2': 'Reinsurance Accident & Health',
            'B1': 'Direct Motor (Comprehensive)',
            'B2': 'Direct Motor (Non-Comprehensive)',
            'B3': 'Reinsurance Motor',
            'C1': 'Direct Aviation',
            'C2': 'Reinsurance Aviation',
            'D1': 'Direct Marine Hull',
            'D2': 'Direct Marine Cargo',
            'D3': 'Reinsurance Marine',
            'E1': 'Direct Property',
            'E2': 'Reinsurance Property Treaty',
            'E3': 'Reinsurance Property Facultative',
            'F1': 'Direct Third Party Liability',
            'F2': 'Reinsurance Third Party Liability',
            'G1': 'Direct Professional Indemnity',
            'G2': 'Reinsurance Professional Indemnity',
            'H1': 'Direct Pecuniary Loss',
            'H2': 'Reinsurance Pecuniary Loss',
            'S1': 'Direct Life',
            'S2': 'Reinsurance Life',
        }

    def generate_currency_amounts(self, base: float, count: int,
                                   volatility: float = 0.3) -> np.ndarray:
        """Generate random currency amounts."""
        return np.random.lognormal(
            mean=np.log(base),
            sigma=volatility,
            size=count
        ).round(2)

    def generate_percentages(self, mean: float = 0.5, std: float = 0.15,
                             count: int = 1) -> np.ndarray:
        """Generate random percentages (0-1 range)."""
        values = np.random.normal(mean, std, count)
        return np.clip(values, 0, 1).round(4)

    def generate_development_factors(self, years: int = 10) -> np.ndarray:
        """Generate claims development factors."""
        # Typical development pattern
        factors = np.array([0.20, 0.35, 0.50, 0.65, 0.75, 0.85, 0.92, 0.96, 0.98, 1.00])
        if years <= len(factors):
            return factors[:years]
        # Extend with 1.0 for additional years
        return np.concatenate([factors, np.ones(years - len(factors))])

    def create_metadata(self, table_name: str, df: pd.DataFrame) -> Dict[str, Any]:
        """Create metadata for a dataset."""
        return {
            'table_name': table_name,
            'row_count': len(df),
            'column_count': len(df.columns),
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'memory_bytes': df.memory_usage(deep=True).sum(),
            'generated_at': datetime.now().isoformat(),
            'config': self.config,
        }

    def get_schema(self, df: pd.DataFrame) -> Dict[str, str]:
        """Get schema (column types) for a DataFrame."""
        type_map = {
            'int64': 'INTEGER',
            'int32': 'INTEGER',
            'float64': 'DOUBLE',
            'float32': 'FLOAT',
            'object': 'STRING',
            'bool': 'BOOLEAN',
            'datetime64[ns]': 'DATETIME',
        }
        schema = {}
        for col, dtype in df.dtypes.items():
            dtype_str = str(dtype)
            schema[col] = type_map.get(dtype_str, 'STRING')
        return schema

    def validate_category(self, category: str) -> bool:
        """Check if a category is valid."""
        return category.lower() in self.CATEGORIES

    def filter_by_syndicate(self, df: pd.DataFrame, syndicates: List[int]) -> pd.DataFrame:
        """Filter DataFrame by syndicate numbers."""
        syndicate_cols = ['syndicate', 'syndicate_number', 'syndicate_id', 'SyndicateNumber']
        for col in syndicate_cols:
            if col in df.columns:
                return df[df[col].isin(syndicates)]
        return df

    def filter_by_year(self, df: pd.DataFrame, years: List[int]) -> pd.DataFrame:
        """Filter DataFrame by years."""
        year_cols = ['year', 'year_of_account', 'yoa', 'YoA', 'Year']
        for col in year_cols:
            if col in df.columns:
                return df[df[col].isin(years)]
        return df

    def aggregate_by_column(self, df: pd.DataFrame, group_col: str,
                            agg_cols: List[str], agg_func: str = 'sum') -> pd.DataFrame:
        """Aggregate DataFrame by column."""
        if group_col not in df.columns:
            return df
        agg_cols = [c for c in agg_cols if c in df.columns]
        if not agg_cols:
            return df
        return df.groupby(group_col)[agg_cols].agg(agg_func).reset_index()

    def merge_datasets(self, left: pd.DataFrame, right: pd.DataFrame,
                       on: List[str], how: str = 'inner') -> pd.DataFrame:
        """Merge two datasets."""
        common_cols = [c for c in on if c in left.columns and c in right.columns]
        if not common_cols:
            return left
        return pd.merge(left, right, on=common_cols, how=how)

    def to_dict(self) -> Dict[str, Any]:
        """Convert connector state to dictionary."""
        return {
            'config': self.config,
            'categories': self.CATEGORIES,
            'datasets_loaded': list(self._datasets.keys()),
            'generation_time': self._generation_time.isoformat() if self._generation_time else None,
        }
