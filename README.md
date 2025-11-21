# Lloyds_Reporting_Dev

End-to-end Lloyd's of London regulatory reporting toolkit, with **Python + R** implementations for:

- Lloyd's **Reserving Return Annual (RRA)** and **Reserving Return Quarterly (RRQ)** forms
- **Solvency II Pillar 3** - QSR (Quarterly) and ASB (Annual) returns
- **FSCS** (Financial Services Compensation Scheme) data generation
- **Liquidity stress testing** for Lloyd's syndicates
- **Power BI integration** across all modules

The repo is designed as a reusable sandbox for regulatory reporting, MI and prototyping, not tied to any real syndicate data.

---

## Features at a glance

- 🔁 **Dual language**: mirrored Python and R implementations for core components
- 🧪 **Full synthetic data**: RRA/RRQ forms, Solvency II claims, FSCS, and liquidity datasets
- 📊 **Power BI ready**: example Python/R scripts and integration guides for all modules
- 📦 **Regulatory templates wired in**: Lloyd's & Solvency II spec Excel files included as references
- 📈 **Actuarial methods**: claims triangles, chain ladder, IBNR ranges, ultimate LR trends, liquidity gap analysis

---

## Repository structure

```text
Lloyds_Reporting_Dev/
├─ README.md                     # This file
├─ DETAILED_DOCUMENTATION.md     # Comprehensive technical documentation
├─ IMPLEMENTATION_ROADMAP.md     # Planned enhancements and gaps
├─ QUICKSTART.md                 # 5-minute Solvency II claims quickstart
├─ POWERBI_GUIDE.md              # Power BI guide – Solvency II claims
├─ POWER_BI_INTEGRATION_GUIDE.md # Power BI guide – RRA & FSCS
├─ RRQ_RRA_USAGE_GUIDE.md        # RRQ and RRA usage guide
├─ RRQ_vs_RRA_COMPARISON.md      # Comparison of RRQ vs RRA
├─ SOLVENCY_II_ASB_README.md     # Solvency II ASB returns documentation
├─ powerbi_python_example.py     # Python Solvency II example for Power BI
├─ powerbi_r_example.R           # R Solvency II example for Power BI
│
├─ Files_for_Claude/             # Regulatory Excel specs (reference only)
│    ├─ FSCS data - template for completion 2.xlsx
│    ├─ Liquidity Stress Test Template_December 2024.xlsx
│    ├─ RRA-specs.xlsx
│    ├─ RRQ-specs.xlsx
│    ├─ Solvency II Pillar 3 - AAD Return Specifications Annual 2024.xlsx
│    ├─ Solvency II Pillar 3 - ASB Return Specifications Annual 2024.xlsx
│    ├─ Solvency II Pillar 3 - QAD Return Specifications Q3 2025.xlsx
│    ├─ Solvency II Pillar 3 - QSR Return Specifications Q3 2025.xlsx
│    └─ Solvency II Pillar 3 - Risk and Claim Reporting templates
│
├─ python_scripts/               # RRA/RRQ + Solvency II claims – Python
│    ├─ requirements.txt
│    ├─ solvency_claims_processor.py
│    ├─ forms/
│    │    ├─ rra_010_control.py
│    │    ├─ rra_193_net_claims.py
│    │    ├─ rra_291_gross_premium_ibnr.py
│    │    └─ unified_form_processor.py    # RRQ/RRA auto-detection
│    ├─ utils/
│    │    └─ rra_aggregator.py
│    └─ data_generation/
│         ├─ generate_synthetic_lloyds_data.py
│         └─ generate_unified_lloyds_data.py  # RRQ/RRA unified generator
│
├─ r_scripts/                    # R equivalents (partial parity - see roadmap)
│    ├─ install_packages.R
│    ├─ solvency_claims_processor.R
│    ├─ forms/
│    │    ├─ rra_010_control.R
│    │    └─ rra_193_net_claims.R
│    ├─ utils/
│    │    └─ rra_aggregator.R
│    └─ data_generation/
│         └─ generate_synthetic_lloyds_data.R
│
├─ FSCS_PowerBI/                 # FSCS data generation (Python + R - full parity)
│    ├─ README.md
│    ├─ Python/
│    │    ├─ fscs_data_generator.py
│    │    ├─ powerbi_query.py
│    │    ├─ example_usage.py
│    │    └─ requirements.txt
│    └─ R/
│         ├─ fscs_data_generator.R
│         ├─ powerbi_query.R
│         ├─ example_usage.R
│         └─ install_packages.R
│
├─ python_implementation/        # Liquidity stress test – Python
│    ├─ README.md
│    ├─ liquidity_stress_test.py
│    ├─ POWERBI_INTEGRATION.md
│    ├─ syndicate_2001_analysis.xlsx
│    └─ all_syndicates_analysis.xlsx
│
├─ r_implementation/             # Liquidity stress test – R (full parity)
│    ├─ README.md
│    ├─ liquidity_stress_test.R
│    └─ POWERBI_INTEGRATION.md
│
├─ Solvency_II_ASB_Python/       # Solvency II ASB – Python
│    ├─ README.md
│    ├─ synthetic_data_generator.py
│    ├─ powerbi_asb_returns.py
│    └─ export_to_excel.py
│
├─ Solvency_II_ASB_R/            # Solvency II ASB – R (full parity)
│    ├─ README.md
│    ├─ synthetic_data_generator.R
│    ├─ powerbi_asb_returns.R
│    └─ export_to_excel.R
│
├─ Solvency_II_QSR_Reporting/    # Solvency II QSR – Python + R (full parity)
│    ├─ README.md
│    ├─ Python/
│    │    ├─ qsr_report_generator.py
│    │    ├─ synthetic_data_generator.py
│    │    └─ POWERBI_GUIDE.md
│    ├─ R/
│    │    ├─ qsr_report_generator.R
│    │    ├─ synthetic_data_generator.R
│    │    └─ POWERBI_GUIDE.md
│    └─ Data/                    # 17 generated QSR CSV files
│
├─ data/                         # Liquidity synthetic data and generator
│    ├─ README.md
│    ├─ generate_synthetic_data.py
│    ├─ all_syndicates_metadata.csv
│    ├─ all_syndicates_assets.csv
│    ├─ all_syndicates_cashflow.csv
│    ├─ all_syndicates_stress.csv
│    └─ syndicate_2001/ ... syndicate_2005/  # 5 syndicates with full data
│
└─ synthetic_data/               # RRA + Solvency II claims synthetic data
     ├─ generate_synthetic_data.py
     ├─ synthetic_lloyds_claims_data.xlsx
     └─ All 14 RRA form CSV files (010, 020, 071, 081, 091, 193, 291-295, 391, 910, 990)

# Plus generated quarterly data directories:
synthetic_data_rra_2024/         # RRA 2024 annual data
synthetic_data_rrq_2024_q1/      # RRQ Q1 2024 data
synthetic_data_rrq_2024_q2/      # RRQ Q2 2024 data
synthetic_data_rrq_2024_q3/      # RRQ Q3 2024 data
synthetic_data_rrq_2024_q4/      # RRQ Q4 2024 data
```

---

## Getting started

### Prerequisites
- **Python ≥ 3.7** with: pandas, numpy, openpyxl, xlrd
- **R ≥ 4.0** with: dplyr, tidyr, readr, lubridate, openxlsx, ggplot2, R6, writexl
- **Power BI Desktop**
- **Excel**

### Install Python dependencies

```bash
cd python_scripts
pip install -r requirements.txt

cd ../FSCS_PowerBI/Python
pip install -r requirements.txt
```

Or install globally:

```bash
pip install pandas numpy openpyxl xlrd matplotlib seaborn scipy statsmodels
```

### Install R dependencies

Run once:

```R
source("r_scripts/install_packages.R")
source("FSCS_PowerBI/R/install_packages.R")
```

---

## Quick starts

### 1. Solvency II claims processing (Python)

```python
from pathlib import Path
from python_scripts.solvency_claims_processor import process_claims_data, export_to_excel

REPO_PATH = Path(r"YOUR_LOCAL_PATH_TO_REPO")
input_file = REPO_PATH / "synthetic_data" / "synthetic_lloyds_claims_data.xlsx"

tables = process_claims_data(input_file)

# Optional: export to Excel
export_to_excel(
    tables,
    REPO_PATH / "outputs" / "solvency_claims_output.xlsx"
)
```

**Outputs** (all DataFrames):
- `detailed_claims`
- `by_syndicate`
- `by_risk_code`
- `by_claim_status`
- `summary`

In Power BI, use `powerbi_python_example.py` or `powerbi_r_example.R` as script templates.

---

### 2. RRA/RRQ forms + synthetic data

**Generate RRA (Annual) data:**

```bash
cd python_scripts/data_generation
python generate_unified_lloyds_data.py --type RRA --year 2024
```

**Generate RRQ (Quarterly) data:**

```bash
cd python_scripts/data_generation

# Single quarter
python generate_unified_lloyds_data.py --type RRQ --year 2024 --quarter Q2

# All four quarters
python generate_unified_lloyds_data.py --all-quarters --year 2024
```

**Process forms:**

```python
# Python
from python_scripts.forms.rra_010_control import validate_rra_010
from python_scripts.forms.rra_193_net_claims import calculate_chain_ladder
from python_scripts.forms.rra_291_gross_premium_ibnr import analyze_ibnr
from python_scripts.forms.unified_form_processor import UnifiedFormProcessor

# Auto-detects RRQ vs RRA
processor = UnifiedFormProcessor()
results = processor.process_all_forms('synthetic_data_rra_2024/')
```

**R equivalent:**

```R
# R (Note: R implementation has partial parity - see IMPLEMENTATION_ROADMAP.md)
source('r_scripts/forms/rra_010_control.R')
source('r_scripts/forms/rra_193_net_claims.R')
source('r_scripts/utils/rra_aggregator.R')
```

---

### 3. FSCS Power BI module

**Python:**

```python
from FSCS_PowerBI.Python.fscs_data_generator import FSCSDataGenerator

gen = FSCSDataGenerator(seed=123)
summary, detail = gen.generate_all(
    num_syndicates=10,
    start_year=2018,
    end_year=2025
)
```

Use `FSCS_PowerBI/Python/powerbi_query.py` directly inside Power BI's Python script connector.

**R:** See `FSCS_PowerBI/R/example_usage.R` for analogous usage.

---

### 4. Liquidity stress testing

**Python** (`python_implementation/liquidity_stress_test.py`):

```python
from python_implementation.liquidity_stress_test import LiquidityStressTest

lst = LiquidityStressTest('data')
lst.load_data()

# Generate analysis tables
capital = lst.calculate_capital_position_table()
liquidity = lst.calculate_liquidity_breakdown_table()
cashflow = lst.calculate_cashflow_summary_table()
stress = lst.calculate_stress_impact_table()
summary = lst.create_dashboard_summary()

# Export to Excel
lst.export_to_excel('liquidity_analysis.xlsx')
```

**R:** `r_implementation/liquidity_stress_test.R` provides an R6 class with the same API and ggplot2 visualization hooks.

---

### 5. Solvency II QSR returns

**Python:**

```python
from Solvency_II_QSR_Reporting.Python.qsr_report_generator import QSRReportGenerator

generator = QSRReportGenerator()
generator.generate_synthetic_data()
reports = generator.generate_all_reports()
generator.export_to_excel('qsr_output.xlsx')
```

**R:** See `Solvency_II_QSR_Reporting/R/qsr_report_generator.R` for R6 class implementation.

---

### 6. Solvency II ASB returns

**Python:**

```python
from Solvency_II_ASB_Python.synthetic_data_generator import SyntheticDataGenerator
from Solvency_II_ASB_Python.powerbi_asb_returns import ASBReturnsProcessor

# Generate data
gen = SyntheticDataGenerator()
data = gen.generate_all_data()

# Process for ASB returns
processor = ASBReturnsProcessor()
asb_245 = processor.process_asb_245(data)
asb_246 = processor.process_asb_246(data)
```

**R:** See `Solvency_II_ASB_R/` for equivalent R implementation.

---

## Power BI integration

There are multiple integration guides:
- **[POWERBI_GUIDE.md](POWERBI_GUIDE.md)** – Solvency II claims
- **[POWER_BI_INTEGRATION_GUIDE.md](POWER_BI_INTEGRATION_GUIDE.md)** – RRA and FSCS
- **[python_implementation/POWERBI_INTEGRATION.md](python_implementation/POWERBI_INTEGRATION.md)** – Liquidity (Python)
- **[r_implementation/POWERBI_INTEGRATION.md](r_implementation/POWERBI_INTEGRATION.md)** – Liquidity (R)
- **[Solvency_II_QSR_Reporting/Python/POWERBI_GUIDE.md](Solvency_II_QSR_Reporting/Python/POWERBI_GUIDE.md)** – QSR (Python)
- **[Solvency_II_QSR_Reporting/R/POWERBI_GUIDE.md](Solvency_II_QSR_Reporting/R/POWERBI_GUIDE.md)** – QSR (R)

All include:
- Step-by-step script connector instructions (Python + R)
- Performance tips
- Example visuals (triangles, time series, KPIs)
- DAX snippets for common metrics

---

## Implementation status

### ✅ Fully implemented (Python + R parity)
- **Solvency II QSR** - Complete quarterly reporting (17 forms)
- **Solvency II ASB** - Complete annual reporting (ASB 245/246/247/248)
- **FSCS** - Full data generation and Power BI integration
- **Liquidity stress testing** - Complete analysis and reporting

### ⚠️ Partially implemented (Python complete, R gaps)
- **RRA/RRQ forms** - Python has 3 form processors + unified processor; R has 2 form processors
- **Unified RRQ/RRA generator** - Python only (R has RRA-only generator)

### 📋 Planned enhancements
- Complete R parity for RRA/RRQ processing
- Add remaining RRA form processors (020, 071, 081, 091, 292-295, 391, 910, 990)
- Unit testing suite
- CI/CD with GitHub Actions
- MkDocs or Quarto documentation site
- Additional actuarial methods (Bornhuetter-Ferguson, Cape Cod)

See **[IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)** for detailed action plan.

---

## Documentation

### Core guides
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute quick start
- **[DETAILED_DOCUMENTATION.md](DETAILED_DOCUMENTATION.md)** - Comprehensive technical documentation
- **[RRQ_RRA_USAGE_GUIDE.md](RRQ_RRA_USAGE_GUIDE.md)** - Complete RRQ and RRA guide
- **[RRQ_vs_RRA_COMPARISON.md](RRQ_vs_RRA_COMPARISON.md)** - Comparison of RRQ vs RRA

### Module-specific
- **[SOLVENCY_II_ASB_README.md](SOLVENCY_II_ASB_README.md)** - ASB returns guide
- **[Solvency_II_QSR_Reporting/README.md](Solvency_II_QSR_Reporting/README.md)** - QSR returns guide
- **[FSCS_PowerBI/README.md](FSCS_PowerBI/README.md)** - FSCS guide
- **[data/README.md](data/README.md)** - Liquidity data guide

---

## Status and notes

This is a **synthetic, non-production training and prototyping repo**. Key notes:

- All data is synthetic and compliant with GDPR
- Not tied to any real Lloyd's syndicate
- Designed for learning, MI prototyping, and interview preparation
- Scripts follow Lloyd's regulatory specifications as of 2024-2025
- Always validate against latest Lloyd's guidance for production use

---

## Contributing

Contributions via issues and PRs are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

---

## License

This code is provided as-is for Lloyd's of London regulatory reporting purposes.

---

**Version:** 1.2
**Last Updated:** 2025-11-21
**Maintained By:** Lloyd's Development Team
**Compatibility:** Power BI Desktop, Python 3.7+, R 4.0+
