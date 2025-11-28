"""
KNIME Connector
===============

Main connector class for KNIME Analytics Platform integration.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import json
import os
import sys

# Add parent paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from lloyds_reporting.config import RANDOM_SEED
    np.random.seed(RANDOM_SEED)
except ImportError:
    np.random.seed(42)


class KNIMEConnector:
    """
    KNIME Analytics Platform data connector for Lloyd's regulatory reporting.

    Generates and manages datasets optimized for KNIME workflow consumption.
    Supports both Python Script nodes and external file-based data exchange.

    Attributes:
        datasets (Dict[str, pd.DataFrame]): Generated datasets
        metadata (Dict[str, Any]): Dataset metadata
        knime_types (Dict[str, str]): KNIME data type mappings

    Example:
        >>> connector = KNIMEConnector()
        >>> datasets = connector.generate_all_datasets()
        >>> connector.export_for_knime('knime_data/')

    KNIME Python Script Usage:
        # In a KNIME Python Script node:
        from integrations.knime import KNIMEConnector

        connector = KNIMEConnector()
        output_table = connector.get_dataset('RRA_010_Control')
    """

    # KNIME data type mappings
    KNIME_TYPE_MAP = {
        'int64': 'Long',
        'int32': 'Integer',
        'float64': 'Double',
        'float32': 'Double',
        'object': 'String',
        'bool': 'Boolean',
        'datetime64[ns]': 'Date and Time',
        'category': 'String',
    }

    # Available dataset categories
    CATEGORIES = {
        'rra': 'RRA Forms (Reserving Return Annual)',
        'rrq': 'RRQ Forms (Reserving Return Quarterly)',
        'qsr': 'QSR (Quarterly Solvency Return)',
        'asb': 'ASB (Annual Solvency Balance Sheet)',
        'lcr': 'LCR (Lloyd\'s Capital Return)',
        'sbf': 'SBF (Syndicate Business Forecast)',
        'qma': 'QMA (Quarterly Monitoring)',
        'fscs': 'FSCS (Financial Services Compensation)',
        'liquidity': 'Liquidity Stress Testing',
        'claims': 'Claims Analysis',
    }

    def __init__(self, seed: int = 42):
        """
        Initialize the KNIME connector.

        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        np.random.seed(seed)
        self.datasets: Dict[str, pd.DataFrame] = {}
        self.metadata: Dict[str, Any] = {
            'generated_at': datetime.now().isoformat(),
            'seed': seed,
            'version': '1.2.0',
            'platform': 'KNIME',
        }

    def generate_all_datasets(self, categories: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
        """
        Generate all datasets for KNIME.

        Args:
            categories: List of categories to generate. If None, generates all.

        Returns:
            Dictionary of dataset name to DataFrame
        """
        # Use the same generator as Power BI but with KNIME-specific optimizations
        from ..powerbi.dataset_generator import DatasetGenerator

        gen = DatasetGenerator(seed=self.seed)

        if categories is None:
            categories = list(self.CATEGORIES.keys())

        for category in categories:
            if category not in self.CATEGORIES:
                print(f"Warning: Unknown category '{category}', skipping")
                continue

            print(f"Generating {self.CATEGORIES[category]}...")

            if category == 'rra':
                self._add_datasets(gen.generate_rra_forms(), 'RRA')
            elif category == 'rrq':
                self._add_datasets(gen.generate_rrq_forms(), 'RRQ')
            elif category == 'qsr':
                self._add_datasets(gen.generate_qsr_data(), 'QSR')
            elif category == 'asb':
                self._add_datasets(gen.generate_asb_data(), 'ASB')
            elif category == 'lcr':
                self._add_datasets(gen.generate_lcr_data(), 'LCR')
            elif category == 'sbf':
                self._add_datasets(gen.generate_sbf_data(), 'SBF')
            elif category == 'qma':
                self._add_datasets(gen.generate_qma_data(), 'QMA')
            elif category == 'fscs':
                self._add_datasets(gen.generate_fscs_data(), 'FSCS')
            elif category == 'liquidity':
                self._add_datasets(gen.generate_liquidity_data(), 'Liquidity')
            elif category == 'claims':
                self._add_datasets(gen.generate_claims_data(), 'Claims')

        self.metadata['datasets'] = list(self.datasets.keys())
        self.metadata['total_records'] = sum(len(df) for df in self.datasets.values())

        print(f"\nGenerated {len(self.datasets)} datasets with {self.metadata['total_records']:,} total records")
        return self.datasets

    def _add_datasets(self, data: Dict[str, pd.DataFrame], prefix: str):
        """Add datasets with prefix."""
        for name, df in data.items():
            self.datasets[f'{prefix}_{name}'] = self._optimize_for_knime(df)

    def _optimize_for_knime(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Optimize DataFrame for KNIME compatibility.

        - Converts column names to KNIME-friendly format
        - Handles missing values appropriately
        - Ensures compatible data types
        """
        # Copy to avoid modifying original
        df = df.copy()

        # Ensure column names are strings and KNIME-compatible
        df.columns = [str(col).replace(' ', '_').replace('-', '_') for col in df.columns]

        # Handle missing values
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].fillna('')
            elif df[col].dtype in ['float64', 'float32']:
                # Keep NaN for numeric columns (KNIME handles these)
                pass

        return df

    def get_dataset(self, name: str) -> pd.DataFrame:
        """
        Get a specific dataset by name.

        Args:
            name: Dataset name

        Returns:
            DataFrame

        Raises:
            KeyError: If dataset not found
        """
        if name not in self.datasets:
            raise KeyError(f"Dataset '{name}' not found. Available: {list(self.datasets.keys())}")
        return self.datasets[name]

    def get_knime_schema(self, df: pd.DataFrame) -> List[Dict[str, str]]:
        """
        Get KNIME-compatible schema for a DataFrame.

        Args:
            df: DataFrame to analyze

        Returns:
            List of column specifications
        """
        schema = []
        for col in df.columns:
            dtype = str(df[col].dtype)
            knime_type = self.KNIME_TYPE_MAP.get(dtype, 'String')
            schema.append({
                'name': col,
                'type': knime_type,
                'pandas_type': dtype,
            })
        return schema

    def export_for_knime(self, output_dir: str, format: str = 'csv') -> List[str]:
        """
        Export datasets for KNIME workflow consumption.

        Args:
            output_dir: Output directory path
            format: Output format ('csv', 'parquet', 'json', 'arff')

        Returns:
            List of exported file paths
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        exported_files = []

        for name, df in self.datasets.items():
            if format == 'csv':
                file_path = output_path / f"{name}.csv"
                df.to_csv(file_path, index=False)
            elif format == 'parquet':
                file_path = output_path / f"{name}.parquet"
                df.to_parquet(file_path, index=False)
            elif format == 'json':
                file_path = output_path / f"{name}.json"
                df.to_json(file_path, orient='records', date_format='iso')
            elif format == 'arff':
                file_path = output_path / f"{name}.arff"
                self._export_arff(df, file_path, name)
            else:
                raise ValueError(f"Unsupported format: {format}")

            exported_files.append(str(file_path))

        # Export metadata
        meta_path = output_path / "_knime_metadata.json"
        self.metadata['export_format'] = format
        self.metadata['exported_files'] = [Path(f).name for f in exported_files]
        with open(meta_path, 'w') as f:
            json.dump(self.metadata, f, indent=2, default=str)
        exported_files.append(str(meta_path))

        # Export schema definitions
        schema_path = output_path / "_knime_schemas.json"
        schemas = {name: self.get_knime_schema(df) for name, df in self.datasets.items()}
        with open(schema_path, 'w') as f:
            json.dump(schemas, f, indent=2)
        exported_files.append(str(schema_path))

        print(f"Exported {len(exported_files)} files to {output_dir}")
        return exported_files

    def _export_arff(self, df: pd.DataFrame, file_path: Path, relation_name: str):
        """Export DataFrame in ARFF format for KNIME/Weka compatibility."""
        with open(file_path, 'w') as f:
            # Write header
            f.write(f"@RELATION {relation_name}\n\n")

            # Write attribute definitions
            for col in df.columns:
                dtype = str(df[col].dtype)
                if dtype in ['int64', 'int32']:
                    f.write(f"@ATTRIBUTE {col} INTEGER\n")
                elif dtype in ['float64', 'float32']:
                    f.write(f"@ATTRIBUTE {col} REAL\n")
                else:
                    f.write(f"@ATTRIBUTE {col} STRING\n")

            # Write data
            f.write("\n@DATA\n")
            for _, row in df.iterrows():
                values = []
                for val in row:
                    if pd.isna(val):
                        values.append('?')
                    elif isinstance(val, str):
                        values.append(f"'{val}'")
                    else:
                        values.append(str(val))
                f.write(','.join(values) + '\n')

    def get_workflow_config(self) -> Dict[str, Any]:
        """
        Generate KNIME workflow configuration.

        Returns:
            Configuration dictionary for KNIME workflow setup
        """
        return {
            'lloyds_reporting': {
                'version': '1.2.0',
                'datasets': list(self.datasets.keys()),
                'categories': list(self.CATEGORIES.keys()),
                'python_version': '3.9+',
                'dependencies': ['pandas', 'numpy'],
                'seed': self.seed,
            },
            'data_sources': [
                {
                    'name': name,
                    'rows': len(df),
                    'columns': list(df.columns),
                    'schema': self.get_knime_schema(df),
                }
                for name, df in self.datasets.items()
            ],
        }

    def generate_python_script(self, dataset_name: str) -> str:
        """
        Generate a Python script for use in KNIME Python Script node.

        Args:
            dataset_name: Name of dataset to generate

        Returns:
            Python script as string
        """
        from .python_nodes import PythonNodeScripts
        return PythonNodeScripts.get_data_loader_script(dataset_name)


# KNIME Python Script node helper functions
def get_lloyds_data(category: str = 'rra') -> Dict[str, pd.DataFrame]:
    """
    Helper function for KNIME Python Script nodes.

    Usage in KNIME:
        from integrations.knime.connector import get_lloyds_data
        datasets = get_lloyds_data('rra')
        output_table = datasets['RRA_010_Control']
    """
    connector = KNIMEConnector()
    return connector.generate_all_datasets([category])


def get_single_dataset(dataset_name: str) -> pd.DataFrame:
    """
    Get a single dataset for KNIME.

    Usage in KNIME:
        from integrations.knime.connector import get_single_dataset
        output_table = get_single_dataset('RRA_010_Control')
    """
    connector = KNIMEConnector()
    connector.generate_all_datasets()
    return connector.get_dataset(dataset_name)
