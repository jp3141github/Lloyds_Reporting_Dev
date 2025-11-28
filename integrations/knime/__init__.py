"""
KNIME Analytics Platform Integration
=====================================

Comprehensive KNIME integration for Lloyd's regulatory reporting.

Components:
-----------
- KNIMEConnector: Main data connector class for KNIME workflows
- WorkflowBuilder: Generate KNIME workflow configurations
- PythonNodes: Pre-built Python node scripts for KNIME

Usage in KNIME:
---------------
1. Add a Python Script node
2. Import the connector module
3. Use the provided functions to generate data

Usage from Python:
------------------
    from integrations.knime import KNIMEConnector

    connector = KNIMEConnector()
    datasets = connector.generate_all_datasets()
    connector.export_for_knime('output/')
"""

from .connector import KNIMEConnector
from .workflow_builder import WorkflowBuilder
from .python_nodes import PythonNodeScripts

__all__ = [
    'KNIMEConnector',
    'WorkflowBuilder',
    'PythonNodeScripts',
]
