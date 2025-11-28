"""
Power BI Connector
==================

Main connector class for Power BI integration with Lloyd's reporting data.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Any
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


class PowerBIConnector:
    """
    Power BI data connector for Lloyd's regulatory reporting.

    Generates and manages datasets optimized for Power BI consumption.

    Attributes:
        datasets (Dict[str, pd.DataFrame]): Generated datasets
        metadata (Dict[str, Any]): Dataset metadata

    Example:
        >>> connector = PowerBIConnector()
        >>> datasets = connector.generate_all_datasets()
        >>> connector.export_for_powerbi('output/')
    """

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
        'qrt': 'QRT Templates (Solvency II)',
        'claims': 'Claims Analysis',
    }

    def __init__(self, seed: int = 42):
        """
        Initialize the Power BI connector.

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
        }

    def generate_all_datasets(self, categories: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
        """
        Generate all datasets for Power BI.

        Args:
            categories: List of categories to generate. If None, generates all.

        Returns:
            Dictionary of dataset name to DataFrame
        """
        if categories is None:
            categories = list(self.CATEGORIES.keys())

        for category in categories:
            if category not in self.CATEGORIES:
                print(f"Warning: Unknown category '{category}', skipping")
                continue

            print(f"Generating {self.CATEGORIES[category]}...")

            if category == 'rra':
                self._generate_rra_datasets()
            elif category == 'rrq':
                self._generate_rrq_datasets()
            elif category == 'qsr':
                self._generate_qsr_datasets()
            elif category == 'asb':
                self._generate_asb_datasets()
            elif category == 'lcr':
                self._generate_lcr_datasets()
            elif category == 'sbf':
                self._generate_sbf_datasets()
            elif category == 'qma':
                self._generate_qma_datasets()
            elif category == 'fscs':
                self._generate_fscs_datasets()
            elif category == 'liquidity':
                self._generate_liquidity_datasets()
            elif category == 'qrt':
                self._generate_qrt_datasets()
            elif category == 'claims':
                self._generate_claims_datasets()

        self.metadata['datasets'] = list(self.datasets.keys())
        self.metadata['total_records'] = sum(len(df) for df in self.datasets.values())

        print(f"\nGenerated {len(self.datasets)} datasets with {self.metadata['total_records']:,} total records")
        return self.datasets

    def _generate_rra_datasets(self):
        """Generate RRA form datasets."""
        from .dataset_generator import DatasetGenerator
        gen = DatasetGenerator(seed=self.seed)

        rra_data = gen.generate_rra_forms()
        for name, df in rra_data.items():
            self.datasets[f'RRA_{name}'] = df

    def _generate_rrq_datasets(self):
        """Generate RRQ form datasets."""
        from .dataset_generator import DatasetGenerator
        gen = DatasetGenerator(seed=self.seed)

        rrq_data = gen.generate_rrq_forms()
        for name, df in rrq_data.items():
            self.datasets[f'RRQ_{name}'] = df

    def _generate_qsr_datasets(self):
        """Generate QSR datasets."""
        from .dataset_generator import DatasetGenerator
        gen = DatasetGenerator(seed=self.seed)

        qsr_data = gen.generate_qsr_data()
        for name, df in qsr_data.items():
            self.datasets[f'QSR_{name}'] = df

    def _generate_asb_datasets(self):
        """Generate ASB datasets."""
        from .dataset_generator import DatasetGenerator
        gen = DatasetGenerator(seed=self.seed)

        asb_data = gen.generate_asb_data()
        for name, df in asb_data.items():
            self.datasets[f'ASB_{name}'] = df

    def _generate_lcr_datasets(self):
        """Generate LCR datasets."""
        from .dataset_generator import DatasetGenerator
        gen = DatasetGenerator(seed=self.seed)

        lcr_data = gen.generate_lcr_data()
        for name, df in lcr_data.items():
            self.datasets[f'LCR_{name}'] = df

    def _generate_sbf_datasets(self):
        """Generate SBF datasets."""
        from .dataset_generator import DatasetGenerator
        gen = DatasetGenerator(seed=self.seed)

        sbf_data = gen.generate_sbf_data()
        for name, df in sbf_data.items():
            self.datasets[f'SBF_{name}'] = df

    def _generate_qma_datasets(self):
        """Generate QMA datasets."""
        from .dataset_generator import DatasetGenerator
        gen = DatasetGenerator(seed=self.seed)

        qma_data = gen.generate_qma_data()
        for name, df in qma_data.items():
            self.datasets[f'QMA_{name}'] = df

    def _generate_fscs_datasets(self):
        """Generate FSCS datasets."""
        from .dataset_generator import DatasetGenerator
        gen = DatasetGenerator(seed=self.seed)

        fscs_data = gen.generate_fscs_data()
        for name, df in fscs_data.items():
            self.datasets[f'FSCS_{name}'] = df

    def _generate_liquidity_datasets(self):
        """Generate liquidity stress testing datasets."""
        from .dataset_generator import DatasetGenerator
        gen = DatasetGenerator(seed=self.seed)

        liq_data = gen.generate_liquidity_data()
        for name, df in liq_data.items():
            self.datasets[f'Liquidity_{name}'] = df

    def _generate_qrt_datasets(self):
        """Generate QRT template datasets."""
        try:
            from QRTs import generate_all_qrts
            qrt_data = generate_all_qrts()
            for name, df in qrt_data.items():
                self.datasets[f'QRT_{name}'] = df
        except ImportError:
            print("  Warning: QRTs module not available")

    def _generate_claims_datasets(self):
        """Generate claims analysis datasets."""
        from .dataset_generator import DatasetGenerator
        gen = DatasetGenerator(seed=self.seed)

        claims_data = gen.generate_claims_data()
        for name, df in claims_data.items():
            self.datasets[f'Claims_{name}'] = df

    def export_for_powerbi(self, output_dir: str, format: str = 'csv') -> List[str]:
        """
        Export datasets in Power BI-ready format.

        Args:
            output_dir: Output directory path
            format: Output format ('csv', 'excel', 'json')

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
            elif format == 'excel':
                file_path = output_path / f"{name}.xlsx"
                df.to_excel(file_path, index=False)
            elif format == 'json':
                file_path = output_path / f"{name}.json"
                df.to_json(file_path, orient='records', date_format='iso')
            else:
                raise ValueError(f"Unsupported format: {format}")

            exported_files.append(str(file_path))

        # Export metadata
        meta_path = output_path / "_metadata.json"
        with open(meta_path, 'w') as f:
            json.dump(self.metadata, f, indent=2, default=str)
        exported_files.append(str(meta_path))

        print(f"Exported {len(exported_files)} files to {output_dir}")
        return exported_files

    def get_dataset_info(self) -> pd.DataFrame:
        """
        Get information about all generated datasets.

        Returns:
            DataFrame with dataset information
        """
        info = []
        for name, df in self.datasets.items():
            info.append({
                'Dataset': name,
                'Rows': len(df),
                'Columns': len(df.columns),
                'Memory_MB': df.memory_usage(deep=True).sum() / 1024 / 1024,
                'Column_Names': ', '.join(df.columns[:5]) + ('...' if len(df.columns) > 5 else ''),
            })
        return pd.DataFrame(info)

    def get_powerbi_script(self, datasets: Optional[List[str]] = None) -> str:
        """
        Generate a Power BI Python script for the specified datasets.

        Args:
            datasets: List of dataset names. If None, includes all.

        Returns:
            Python script string for Power BI
        """
        from .script_builder import ScriptBuilder
        builder = ScriptBuilder()
        return builder.build_script(datasets or list(self.datasets.keys()))


# Convenience function for Power BI scripts
def get_all_data() -> Dict[str, pd.DataFrame]:
    """
    Convenience function to get all datasets.

    Usage in Power BI:
        # import pandas as pd
        # exec(open('path/to/connector.py').read())
        # datasets = get_all_data()
    """
    connector = PowerBIConnector()
    return connector.generate_all_datasets()
