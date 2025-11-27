# CLAUDE.md - AI Assistant Context

This file provides context for AI assistants working with the Lloyds_Reporting_Dev codebase.

## Project Overview

**Lloyds_Reporting_Dev** is a comprehensive regulatory reporting toolkit for Lloyd's of London insurance syndicates. It provides synthetic data generation, form processing, and Power BI integration for 175+ reporting tables across 21 major regulatory returns.

## Quick Reference

### Key Directories

| Directory | Purpose |
|-----------|---------|
| `python_scripts/` | Core RRA/RRQ form processors and data generators |
| `python_scripts/forms/` | Individual form processor modules |
| `python_scripts/data_generation/` | Synthetic data generators |
| `QRTs/` | Quantitative Reporting Template generators (Solvency II) |
| `OTH/` | Non-standard regulatory templates |
| `POWER_BI/` | 24 Power BI integration scripts |
| `Solvency_II_QSR_Reporting/` | Quarterly Solvency Reporting |
| `Solvency_II_ASB_Python/` | Annual Solvency Balance Sheet |
| `FSCS_PowerBI/` | Financial Services Compensation Scheme |
| `Files_for_Claude/` | Regulatory Excel specs and QRT templates (reference) |
| `synthetic_data*/` | Generated test data directories |
| `data/` | Syndicate liquidity data |

### Key Files

| File | Purpose |
|------|---------|
| `python_scripts/solvency_claims_processor.py` | Main claims processing logic |
| `python_scripts/forms/unified_form_processor.py` | RRQ/RRA auto-detection processor |
| `python_scripts/data_generation/generate_unified_lloyds_data.py` | Unified data generator |
| `QRTs/__init__.py` | QRT module with `generate_all_qrts()` |
| `lloyds_reporting/config.py` | Shared constants and configuration |

### Running Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Generate RRA data
cd python_scripts/data_generation
python generate_unified_lloyds_data.py --type RRA --year 2024

# Generate RRQ data (quarterly)
python generate_unified_lloyds_data.py --type RRQ --year 2024 --quarter Q2

# Generate all QRT templates
python -c "from QRTs import generate_all_qrts; print(generate_all_qrts().keys())"
```

### Common Tasks

**1. Process Claims Data:**
```python
from python_scripts.solvency_claims_processor import process_claims_data
tables = process_claims_data("synthetic_data/synthetic_lloyds_claims_data.xlsx")
```

**2. Generate QRT Templates:**
```python
from QRTs import generate_all_qrts
all_templates = generate_all_qrts()  # Returns dict of DataFrames
```

**3. Use Form Processor:**
```python
from python_scripts.forms.unified_form_processor import UnifiedFormProcessor
processor = UnifiedFormProcessor()
results = processor.process_all_forms('synthetic_data_rra_2024/')
```

## Architecture Notes

### Data Flow
```
Synthetic Generators → Form Processors → Power BI Scripts → Excel/CSV Outputs
```

### Language Parity
- Most modules have parallel Python and R implementations
- Python is primary; R mirrors core functionality
- R files are in corresponding `*_R/` or `r_*/` directories

### Naming Conventions
- Form codes: `rra_XXX` (Annual), `rrq_XXX` (Quarterly)
- QRT codes: `irXXXX` (e.g., `ir0201` = Balance Sheet)
- Syndicates: 4-digit numbers (e.g., 2001, 2987)

## Regulatory Context

### Lloyd's Returns
| Return | Frequency | Forms |
|--------|-----------|-------|
| RRA | Annual | 14 forms (010-990) |
| RRQ | Quarterly | 4 forms (010, 020, 193, 291) |
| LCR | Annual | Lloyd's Capital Return |
| SBF | Annual | Syndicate Business Forecast |
| QMA/QMB | Quarterly | Quarterly Monitoring |

### Solvency II Returns
| Return | Frequency | Description |
|--------|-----------|-------------|
| QSR | Quarterly | Quarterly Solvency Return (17 forms) |
| ASB | Annual | Annual Solvency Balance Sheet |
| AAD | Annual | Annual Actuarial Data |

### Key Actuarial Concepts
- **IBNR**: Incurred But Not Reported reserves
- **Chain Ladder**: Development pattern method
- **YoA**: Year of Account
- **LOB**: Line of Business
- **SCR**: Solvency Capital Requirement
- **MCR**: Minimum Capital Requirement

## Code Style

### Python
- Use pandas DataFrames for all tabular data
- Random seed: 42 for reproducibility
- Type hints encouraged but not enforced
- Docstrings for public functions

### Constants
- Import from `lloyds_reporting/config.py`
- Use SCREAMING_SNAKE_CASE for constants
- Document regulatory sources in comments

## Testing

```bash
# Run tests (when implemented)
pytest tests/ -v

# Run specific test file
pytest tests/test_generators.py -v

# Run with coverage
pytest --cov=python_scripts --cov-report=html
```

## Common Issues

### Import Errors
If imports fail, ensure you're in the repo root:
```bash
cd /path/to/Lloyds_Reporting_Dev
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Missing Dependencies
```bash
pip install pandas numpy openpyxl xlrd
```

### Excel File Errors
Use `openpyxl` for `.xlsx` files, `xlrd` for `.xls` files.

## Documentation

- `README.md` - Main overview
- `QUICKSTART.md` - 5-minute guide
- `DETAILED_DOCUMENTATION.md` - Technical deep-dive
- `IMPLEMENTATION_ROADMAP.md` - Planned enhancements
- Module-specific READMEs in each directory

## Version Info

- **Version**: 1.2.0
- **Python**: >=3.7
- **Last Updated**: 2025-11-27
