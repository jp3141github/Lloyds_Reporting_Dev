"""
FSCS (Financial Services Compensation Scheme) - Python
======================================================

Python implementation for FSCS data generation and Power BI integration.

Available Modules:
------------------
- fscs_data_generator: Main FSCS data generator
- powerbi_query: Power BI integration script
- example_usage: Usage examples

Usage:
------
    from FSCS_PowerBI.Python import FSCSDataGenerator

    gen = FSCSDataGenerator(seed=123)
    summary, detail = gen.generate_all(
        num_syndicates=10,
        start_year=2018,
        end_year=2025
    )
"""

__all__ = []
