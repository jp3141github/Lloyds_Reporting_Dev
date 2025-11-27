"""
SAO Addendum (Statement of Actuarial Opinion) - Python
======================================================

Python implementation for SAO Addendum return data generation.

Available Modules:
------------------
- generate_sao_class_mappings: Class mappings data generation
- generate_090_specific_ibnr: Specific IBNR data (Form 090)
- generate_100_movements_ave: Movements and Actual vs Expected (Form 100)

Usage:
------
    from sao_addendum_python import (
        generate_class_mappings_data,
        generate_specific_ibnr_data,
        generate_movements_ave_data
    )

    # Generate SAO class mappings
    mappings = generate_class_mappings_data()

    # Generate specific IBNR
    ibnr = generate_specific_ibnr_data()

    # Generate movements analysis
    movements = generate_movements_ave_data()
"""

__all__ = []
