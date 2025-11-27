"""
Solvency II ASB (Annual Solvency Balance Sheet) - Python
========================================================

Python implementation for Solvency II ASB returns generation.

Available Modules:
------------------
- synthetic_data_generator: Generate synthetic ASB data
- powerbi_asb_returns: Power BI integration for ASB returns
- export_to_excel: Excel export functionality

Usage:
------
    from Solvency_II_ASB_Python import SyntheticDataGenerator, ASBReturnsProcessor

    # Generate data
    gen = SyntheticDataGenerator()
    data = gen.generate_all_data()

    # Process for ASB returns
    processor = ASBReturnsProcessor()
    asb_245 = processor.process_asb_245(data)
"""

__all__ = []
