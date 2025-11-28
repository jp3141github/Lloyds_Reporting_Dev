"""
Lloyd's Reporting Integrations
==============================

Integration modules for external BI and analytics platforms.

Submodules:
-----------
- powerbi: Power BI Desktop and Service integration
- knime: KNIME Analytics Platform integration
- shared: Common utilities (data connectors, validators, export managers)

Usage:
------
    from integrations.powerbi import PowerBIConnector
    from integrations.knime import KNIMEConnector
    from integrations.shared import DataConnector, DataValidator, ExportManager
"""

__all__ = ['powerbi', 'knime', 'shared']
