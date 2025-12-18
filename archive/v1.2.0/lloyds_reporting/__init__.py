"""
Lloyd's Reporting Development Package
=====================================

A comprehensive regulatory reporting toolkit for Lloyd's of London insurance syndicates.

Modules:
--------
- config: Shared constants and configuration
- (additional modules to be added)

Usage:
------
    from lloyds_reporting.config import SYNDICATES, CLASSES_OF_BUSINESS
    from lloyds_reporting import config

Version: 1.2.0
"""

__version__ = "1.2.0"
__author__ = "Lloyd's Development Team"

from . import config

__all__ = [
    "config",
    "__version__",
]
