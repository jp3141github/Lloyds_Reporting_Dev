"""
Synthetic Data Generators
=========================

Data generation modules for Lloyd's regulatory reporting testing.

Available Generators:
---------------------
- generate_synthetic_lloyds_data: RRA forms data generator
- generate_unified_lloyds_data: Unified RRQ/RRA data generator

Usage:
------
    from python_scripts.data_generation import LloydsDataGenerator, UnifiedLloydsDataGenerator

    # Generate RRA data
    generator = LloydsDataGenerator(output_dir='synthetic_data')
    generator.generate_all_data()

    # Generate unified RRQ/RRA data
    unified = UnifiedLloydsDataGenerator(return_type='RRQ', year=2024, quarter='Q2')
    unified.generate_all_data()
"""

from .generate_synthetic_lloyds_data import LloydsDataGenerator
from .generate_unified_lloyds_data import UnifiedLloydsDataGenerator

__all__ = [
    'LloydsDataGenerator',
    'UnifiedLloydsDataGenerator',
]
