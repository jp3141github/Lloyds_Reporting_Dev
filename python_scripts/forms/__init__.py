"""
RRA/RRQ Form Processors
=======================

V2.0: Complete form processor module for Lloyd's regulatory returns.
Updated to include all active forms per Lloyd's RRA/RRQ Instructions V1.6 (March 2025).

Available RRA Forms:
--------------------
- rra_010_control: Control data and syndicate metadata
- rra_020_exchange_rates: Exchange rates for currency conversion
- rra_071_scob_mapping: SCOB to Solvency II LOB mapping
- rra_081_reserving_class: Reserving class definitions
- rra_091_lpt_data: Loss Portfolio Transfer data
- rra_193_net_claims: Net claims development with chain ladder
- rra_291_gross_premium_ibnr: Gross premium and IBNR estimates
- rra_292_net_premium_ibnr: Net premium and IBNR with RI analysis
- rra_293_outstanding_ibnr_pyoa: Outstanding & IBNR by Prior YoA
- rra_294_catastrophe_ibnr: Catastrophe event IBNR
- rra_295_ulae: Unallocated Loss Adjustment Expenses
- rra_391_ielr: Initial Expected Loss Ratios
- rra_591_reinsurance_structure: Syndicate reinsurance program structure (NEW V2)
- rra_910_additional_info: Additional information and notes
- rra_990_validation: Cross-form validation summary

Available RRQ Forms:
--------------------
- rrq_191_gross_claims: Gross claims development (NEW V2)
- rrq_192_claims_triangles: Claims triangles summary (NEW V2)

Unified Processor:
------------------
- unified_form_processor: Auto-detection processor for RRQ/RRA

Usage:
------
    from python_scripts.forms import UnifiedFormProcessor
    processor = UnifiedFormProcessor()
    results = processor.process_all_forms('synthetic_data_rra_2024/')

    # Or use individual form processors:
    from python_scripts.forms import process_rra_591, validate_rra_591
    df = process_rra_591('path/to/data.csv')
    validation = validate_rra_591('path/to/data.csv')
"""

# Form 010 - Control Data
from .rra_010_control import process_rra_010, validate_rra_010, get_control_summary

# Form 020 - Exchange Rates (V2)
from .rra_020_exchange_rates import process_rra_020, validate_rra_020, get_exchange_rate_summary

# Form 071 - SCOB Mapping (V2)
from .rra_071_scob_mapping import process_rra_071, validate_rra_071, get_scob_summary

# Form 081 - Reserving Class Information (V2)
from .rra_081_reserving_class import process_rra_081, validate_rra_081, get_reserving_class_summary

# Form 091 - LPT Data (V2)
from .rra_091_lpt_data import process_rra_091, validate_rra_091, get_lpt_summary

# Form 193 - Net Claims Development
from .rra_193_net_claims import process_rra_193, create_development_triangle, calculate_chain_ladder

# Form 291 - Gross Premium and IBNR
from .rra_291_gross_premium_ibnr import process_rra_291, get_ibnr_summary_by_yoa, get_ibnr_range_analysis

# Form 292 - Net Premium and IBNR
from .rra_292_net_premium_ibnr import process_rra_292, get_ri_recovery_analysis, compare_net_vs_gross

# Form 293 - Outstanding & IBNR by PYoA (V2)
from .rra_293_outstanding_ibnr_pyoa import process_rra_293, validate_rra_293, get_pyoa_summary

# Form 294 - Catastrophe IBNR (V2)
from .rra_294_catastrophe_ibnr import process_rra_294, validate_rra_294, get_catastrophe_summary

# Form 295 - ULAE (V2)
from .rra_295_ulae import process_rra_295, validate_rra_295, get_ulae_summary

# Form 391 - IELR (V2)
from .rra_391_ielr import process_rra_391, validate_rra_391, get_ielr_summary

# Form 591 - Syndicate Reinsurance Structure (NEW V2)
from .rra_591_reinsurance_structure import (
    process_rra_591,
    validate_rra_591,
    get_reinsurance_summary,
    get_reinsurer_exposure
)

# Form 910 - Additional Information (V2)
from .rra_910_additional_info import process_rra_910, validate_rra_910, get_additional_info_summary

# Form 990 - Validation Summary
from .rra_990_validation import validate_all_forms, get_validation_summary, export_validation_report

# RRQ Form 191 - Gross Claims Development (NEW V2)
from .rrq_191_gross_claims import (
    process_rrq_191,
    validate_rrq_191,
    create_gross_development_triangle,
    calculate_gross_development_factors,
    get_gross_claims_summary
)

# RRQ Form 192 - Claims Triangles Summary (NEW V2)
from .rrq_192_claims_triangles import (
    process_rrq_192,
    validate_rrq_192,
    get_triangle_summary_by_method,
    get_development_pattern_analysis,
    compare_gross_net_triangles
)

# Unified processor
from .unified_form_processor import UnifiedFormProcessor

__all__ = [
    # Form 010
    'process_rra_010',
    'validate_rra_010',
    'get_control_summary',
    # Form 020 (V2)
    'process_rra_020',
    'validate_rra_020',
    'get_exchange_rate_summary',
    # Form 071 (V2)
    'process_rra_071',
    'validate_rra_071',
    'get_scob_summary',
    # Form 081 (V2)
    'process_rra_081',
    'validate_rra_081',
    'get_reserving_class_summary',
    # Form 091 (V2)
    'process_rra_091',
    'validate_rra_091',
    'get_lpt_summary',
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
    # Form 293 (V2)
    'process_rra_293',
    'validate_rra_293',
    'get_pyoa_summary',
    # Form 294 (V2)
    'process_rra_294',
    'validate_rra_294',
    'get_catastrophe_summary',
    # Form 295 (V2)
    'process_rra_295',
    'validate_rra_295',
    'get_ulae_summary',
    # Form 391 (V2)
    'process_rra_391',
    'validate_rra_391',
    'get_ielr_summary',
    # Form 591 (NEW V2)
    'process_rra_591',
    'validate_rra_591',
    'get_reinsurance_summary',
    'get_reinsurer_exposure',
    # Form 910 (V2)
    'process_rra_910',
    'validate_rra_910',
    'get_additional_info_summary',
    # Form 990
    'validate_all_forms',
    'get_validation_summary',
    'export_validation_report',
    # RRQ Form 191 (NEW V2)
    'process_rrq_191',
    'validate_rrq_191',
    'create_gross_development_triangle',
    'calculate_gross_development_factors',
    'get_gross_claims_summary',
    # RRQ Form 192 (NEW V2)
    'process_rrq_192',
    'validate_rrq_192',
    'get_triangle_summary_by_method',
    'get_development_pattern_analysis',
    'compare_gross_net_triangles',
    # Unified processor
    'UnifiedFormProcessor',
]

# Module version
__version__ = '2.0.0'
