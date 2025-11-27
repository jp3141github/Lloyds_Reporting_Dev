"""
Solvency II QSR (Quarterly Solvency Return) - Python
====================================================

Python implementation for Solvency II QSR returns generation.

Available Modules:
------------------
- qsr_report_generator: Main QSR report generator
- synthetic_data_generator: Generate synthetic QSR data
- report_generator_extended: Extended report variants

Usage:
------
    from Solvency_II_QSR_Reporting.Python import QSRReportGenerator

    generator = QSRReportGenerator()
    generator.generate_synthetic_data()
    reports = generator.generate_all_reports()
    generator.export_to_excel('qsr_output.xlsx')
"""

__all__ = []
