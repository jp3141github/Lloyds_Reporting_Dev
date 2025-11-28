"""
Power BI Integration Module
===========================

Comprehensive Power BI integration for Lloyd's regulatory reporting.

Components:
-----------
- PowerBIConnector: Main data connector class
- DatasetGenerator: Generate Power BI-ready datasets
- ScriptBuilder: Build Power BI Python/R scripts dynamically

Usage in Power BI Desktop:
--------------------------
1. Get Data > Python script
2. Paste the generated script
3. Select tables to import

Usage from Python:
------------------
    from integrations.powerbi import PowerBIConnector, DatasetGenerator

    # Generate all datasets
    connector = PowerBIConnector()
    datasets = connector.generate_all_datasets()

    # Export for Power BI
    connector.export_for_powerbi('output/')
"""

from .connector import PowerBIConnector
from .dataset_generator import DatasetGenerator
from .script_builder import ScriptBuilder

__all__ = [
    'PowerBIConnector',
    'DatasetGenerator',
    'ScriptBuilder',
]
