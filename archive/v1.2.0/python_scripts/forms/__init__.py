"""
RRA/RRQ Form Processors
=======================

Individual form processor modules for Lloyd's regulatory returns.

Available Forms:
----------------
- rra_010_control: Control data and syndicate metadata
- rra_193_net_claims: Net claims development with chain ladder
- rra_291_gross_premium_ibnr: Gross premium and IBNR estimates
- rra_292_net_premium_ibnr: Net premium and IBNR with RI analysis
- rra_990_validation: Cross-form validation summary
- unified_form_processor: Auto-detection processor for RRQ/RRA

Usage:
------
    from python_scripts.forms import UnifiedFormProcessor
    processor = UnifiedFormProcessor()
    results = processor.process_all_forms('synthetic_data_rra_2024/')
"""

from .rra_010_control import process_rra_010, validate_rra_010, get_control_summary
from .rra_193_net_claims import process_rra_193, create_development_triangle, calculate_chain_ladder
from .rra_291_gross_premium_ibnr import process_rra_291, get_ibnr_summary_by_yoa, get_ibnr_range_analysis
from .rra_292_net_premium_ibnr import process_rra_292, get_ri_recovery_analysis, compare_net_vs_gross
from .rra_990_validation import validate_all_forms, get_validation_summary, export_validation_report
from .unified_form_processor import UnifiedFormProcessor

__all__ = [
    # Form 010
    'process_rra_010',
    'validate_rra_010',
    'get_control_summary',
    # Form 193
    'process_rra_193',
    'create_development_triangle',
    'calculate_chain_ladder',
    # Form 291
    'process_rra_291',
    'get_ibnr_summary_by_yoa',
    'get_ibnr_range_analysis',
    # Form 292
    'process_rra_292',
    'get_ri_recovery_analysis',
    'compare_net_vs_gross',
    # Form 990
    'validate_all_forms',
    'get_validation_summary',
    'export_validation_report',
    # Unified processor
    'UnifiedFormProcessor',
]
