"""
Lloyd's Python Scripts Package
==============================

Core RRA/RRQ form processors and data generators for Lloyd's regulatory reporting.

Submodules:
-----------
- forms: Individual form processor modules (RRA 010, 193, 291, 292, 990)
- utils: Utility functions and aggregators
- data_generation: Synthetic data generators

Main Module:
------------
- solvency_claims_processor: Claims data processing and validation
"""

from . import forms
from . import utils
from . import data_generation

__all__ = [
    'forms',
    'utils',
    'data_generation',
]
