# V2 Changelog

## Version 2.0.0 (2025-12-18)

Major update to align with Lloyd's RRA/RRQ Instructions V1.6 (March 2025).

### Breaking Changes

- `RRQ_FORMS` dictionary structure changed - now split into `RRQ_FORMS`, `RRQ_FORMS_Q1_Q3`, and `RRQ_FORMS_Q4`

### New Forms Added

#### RRA Forms
- **Form 591 - Syndicate Reinsurance Structure**: Captures syndicate reinsurance program structure and arrangements (confirmed active 2025)

#### RRQ Forms
- **Form 191 - Gross Claims Development**: Gross claims development triangles for quarterly reporting
- **Form 192 - Claims Triangles Summary**: Summary claims triangle data for quarterly monitoring

### New Form Processors

All form processors now have dedicated modules in `python_scripts/forms/`:

| Form | Module | Status |
|------|--------|--------|
| 020 | `rra_020_exchange_rates.py` | NEW |
| 071 | `rra_071_scob_mapping.py` | NEW |
| 081 | `rra_081_reserving_class.py` | NEW |
| 091 | `rra_091_lpt_data.py` | NEW |
| 293 | `rra_293_outstanding_ibnr_pyoa.py` | NEW |
| 294 | `rra_294_catastrophe_ibnr.py` | NEW |
| 295 | `rra_295_ulae.py` | NEW |
| 391 | `rra_391_ielr.py` | NEW |
| 591 | `rra_591_reinsurance_structure.py` | NEW |
| 910 | `rra_910_additional_info.py` | NEW |
| 191 | `rrq_191_gross_claims.py` | NEW |
| 192 | `rrq_192_claims_triangles.py` | NEW |

### Configuration Updates

#### `lloyds_reporting/config.py`

1. **RRA_FORMS**: Added Form 591 "Syndicate Reinsurance Structure"
2. **RRQ_FORMS**: Updated to include Forms 081, 091, 191, 192
3. **RRQ_FORMS_Q1_Q3**: New quarterly-specific form dictionary
4. **RRQ_FORMS_Q4**: New Q4-specific form dictionary with additional forms

### Archive

Previous V1.2.0 code has been archived to `archive/v1.2.0/`:
- `python_scripts/` - Original form processors
- `lloyds_reporting/` - Original configuration
- `QRTs/` - Original QRT templates
- `Python_Scripts/` - Legacy directory
- `R_Scripts/` - Legacy R scripts
- `python_implementation/` - Liquidity stress test module
- `r_implementation/` - R liquidity stress test module

### Regulatory References

- Lloyd's RRA Instructions V1.6 (March 2025)
- Lloyd's RRQ Instructions V1.6 (March 2025)
- Form 591 confirmed active per Lloyd's fact-check (December 2024)

### Unified Data Generator Updates

The unified data generator (`python_scripts/data_generation/generate_unified_lloyds_data.py`) now generates all forms:

**New Generator Methods:**
- `generate_scob_mapping()` - Form 071
- `generate_reserving_class()` - Form 081
- `generate_lpt_data()` - Form 091
- `generate_net_premium_ibnr()` - Form 292
- `generate_outstanding_ibnr_pyoa()` - Form 293
- `generate_catastrophe_ibnr()` - Form 294
- `generate_ulae()` - Form 295
- `generate_ielr()` - Form 391
- `generate_reinsurance_structure()` - Form 591 (NEW)
- `generate_additional_info()` - Form 910
- `generate_validation_summary()` - Form 990
- `generate_gross_claims_rrq()` - RRQ Form 191 (NEW)
- `generate_claims_triangles_rrq()` - RRQ Form 192 (NEW)

### Legacy Directory Deprecation

The following directories are now deprecated with notices added to their READMEs:
- `Python_Scripts/` → Use `python_scripts/` instead
- `R_Scripts/` → Use `r_scripts/` instead

### Resolved Issues

1. ~~Synthetic data generators: Need to add data generation for new forms~~ - COMPLETE
2. ~~Legacy directories: Python_Scripts/, R_Scripts/ should be fully deprecated~~ - COMPLETE (deprecation notices added)
3. ~~Unified generator: needs expansion to all forms~~ - COMPLETE

---

## Migration Guide

### Updating RRQ Form References

```python
# Old (V1.x)
from lloyds_reporting.config import RRQ_FORMS

# New (V2.0)
from lloyds_reporting.config import RRQ_FORMS, RRQ_FORMS_Q1_Q3, RRQ_FORMS_Q4

# For quarterly-aware processing:
def get_forms_for_quarter(quarter: str) -> dict:
    if quarter == 'Q4':
        return RRQ_FORMS_Q4
    return RRQ_FORMS_Q1_Q3
```

### Using New Form Processors

```python
# Form 591 - Reinsurance Structure
from python_scripts.forms import process_rra_591, validate_rra_591
df = process_rra_591('path/to/data.csv')
validation_results = validate_rra_591('path/to/data.csv')

# RRQ Form 191 - Gross Claims
from python_scripts.forms import process_rrq_191, create_gross_development_triangle
df = process_rrq_191('path/to/data.csv')
triangle = create_gross_development_triangle('path/to/data.csv', syndicate=2001)
```
