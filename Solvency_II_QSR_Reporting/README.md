# Solvency II QSR Reporting for Lloyd's of London

Comprehensive Python and R scripts for generating Solvency II Quarterly Solvency Return (QSR) reports from Lloyd's of London syndicate data, designed for seamless integration with Power BI.

## Overview

This project provides production-ready scripts to:
- Generate synthetic Lloyd's of London syndicate data for testing and development
- Transform raw syndicate data into standardized Solvency II QSR return formats
- Integrate seamlessly with Power BI for reporting and visualization
- Support both Python and R implementations for maximum flexibility

## Solvency II QSR Returns Covered

Based on the **Q3 2025 QSR Return Specifications**, this implementation covers:

| QSR Return | Description | EIOPA Reference |
|------------|-------------|-----------------|
| **QSR 002** | Overall Balance Sheet | S.02.01.02 |
| **QSR 220** | Own Funds | S.23.01.01 |
| **QSR 240** | Non-Life Technical Provisions | S.17.01.02 |
| **QSR 280/283** | Life Technical Provisions | S.12.01.02 |
| **QSR 291** | Operational Risk | S.41.01.11 |
| **QSR 292** | Market Risk | S.14.01.10.01 |
| **QSR 293** | Counterparty Default Risk | S.38.01.10.01 |
| **QSR 440** | Non-Life Insurance Claims Information | S.05.01.02.01 |
| **QSR 450** | Life Insurance Information | S.05.01.02.02 |
| **QSR 510/511** | Minimum Capital Requirement (MCR) | S.28.01.01 |

Additional reports:
- **SCR Summary**: Comprehensive Solvency Capital Requirement breakdown
- **Solvency Ratio Report**: SCR and MCR coverage ratios with surplus calculations

## Project Structure

```
Solvency_II_QSR_Reporting/
├── README.md                          # This file
├── Python/
│   ├── synthetic_data_generator.py    # Generate synthetic Lloyd's data
│   ├── qsr_report_generator.py        # Transform data to QSR formats
│   └── POWERBI_GUIDE.md               # Power BI integration guide (Python)
├── R/
│   ├── synthetic_data_generator.R     # Generate synthetic Lloyd's data (R)
│   ├── qsr_report_generator.R         # Transform data to QSR formats (R)
│   └── POWERBI_GUIDE.md               # Power BI integration guide (R)
└── Data/
    ├── synthetic_balance_sheet.csv    # Generated data files
    ├── synthetic_own_funds.csv
    ├── synthetic_technical_provisions.csv
    ├── synthetic_premiums_claims.csv
    ├── synthetic_investments.csv
    ├── synthetic_scr_calculation.csv
    ├── synthetic_mcr_calculation.csv
    └── [QSR report outputs]           # Generated QSR returns
```

## Quick Start

### Python Implementation

#### Prerequisites
```bash
pip install pandas numpy openpyxl
```

#### Generate Synthetic Data
```bash
cd Solvency_II_QSR_Reporting/Python
python synthetic_data_generator.py
```

#### Generate QSR Reports
```bash
python qsr_report_generator.py
```

#### Use in Power BI
See `Python/POWERBI_GUIDE.md` for detailed integration instructions.

Example:
```python
# In Power BI Python script
import sys
sys.path.append(r'C:\path\to\Solvency_II_QSR_Reporting\Python')
from qsr_report_generator import get_solvency_ratios
dataset = get_solvency_ratios()
```

### R Implementation

#### Prerequisites
```r
install.packages(c("dplyr", "tidyr"))
```

#### Generate Synthetic Data
```r
setwd("Solvency_II_QSR_Reporting/R")
source("synthetic_data_generator.R")
generate_all_data(num_syndicates = 15)
```

#### Generate QSR Reports
```r
source("qsr_report_generator.R")
main()
```

#### Use in Power BI
See `R/POWERBI_GUIDE.md` for detailed integration instructions.

Example:
```r
# In Power BI R script
setwd("C:/path/to/Solvency_II_QSR_Reporting/R")
source("qsr_report_generator.R")
dataset <- get_solvency_ratios()
```

## Features

### Synthetic Data Generation

Generates realistic Lloyd's of London syndicate data including:

- **Balance Sheet Items**
  - Assets (Investments, Receivables, Cash, etc.)
  - Liabilities (Technical Provisions, Payables, etc.)
  - Excess of Assets over Liabilities (Own Funds)

- **Own Funds Components**
  - Members' Contributions (FIS)
  - Reconciliation Reserve
  - Subordinated Liabilities
  - Tier 1/2/3 classification

- **Technical Provisions**
  - Best Estimate (Gross, Net, Recoverable)
  - Risk Margin
  - Split by Line of Business

- **Premiums and Claims**
  - Written and Earned Premiums
  - Claims Incurred
  - Expense data
  - Loss, Expense, and Combined Ratios

- **Capital Requirements**
  - SCR calculation with risk modules
  - MCR calculation with floors and caps
  - Diversification benefits

- **Investment Portfolio**
  - Multiple asset classes
  - Geographical diversification
  - Solvency II valuations

### QSR Report Generation

Transforms raw data into standardized QSR formats:

- **Standardized Field Naming**: Follows EIOPA row/column references (e.g., R0010, C0010)
- **Validation Compliance**: Implements key validation rules from specifications
- **Power BI Optimized**: Direct integration with Power BI data models
- **Flexible Architecture**: Easy to extend with custom calculations

### Power BI Integration

Both Python and R implementations provide:

- **Direct Data Import**: Use scripts as Power BI data sources
- **Data Transformation**: Apply QSR formatting in Query Editor
- **Incremental Refresh**: Support for large datasets
- **Pre-built Functions**: Ready-to-use functions for each QSR return
- **Example Dashboards**: Sample DAX measures for common KPIs

## Data Flow

```
┌─────────────────────────────┐
│  Source Data (CSV/Database) │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Synthetic Data Generator   │  ◄── For testing/development
│  (Python or R)              │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Raw Lloyd's Data           │
│  - Balance Sheet            │
│  - Own Funds                │
│  - Technical Provisions     │
│  - Premiums/Claims          │
│  - SCR/MCR Calculations     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  QSR Report Generator       │
│  (Python or R)              │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Standardized QSR Returns   │
│  - QSR 002 (Balance Sheet)  │
│  - QSR 220 (Own Funds)      │
│  - QSR 240 (Tech Provisions)│
│  - QSR 440 (Premiums/Claims)│
│  - QSR 510 (MCR)            │
│  - Solvency Ratios          │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Power BI Dashboard         │
│  - Solvency Ratio Analysis  │
│  - Own Funds Composition    │
│  - Risk Module Breakdown    │
│  - Technical Provisions     │
│  - Premium/Claims Trends    │
└─────────────────────────────┘
```

## Customization

### Using Your Own Data

Replace synthetic data with actual Lloyd's data:

**Python:**
```python
# In qsr_report_generator.py, modify load_data():
def load_data(self):
    # Load from your database
    import pyodbc
    conn = pyodbc.connect('your_connection_string')
    self.data['balance_sheet'] = pd.read_sql("SELECT * FROM balance_sheet", conn)
    # ... load other tables
```

**R:**
```r
# In qsr_report_generator.R, modify load_data():
load_data <- function() {
  # Load from your database
  library(odbc)
  con <- dbConnect(odbc(), "your_connection")
  data_store$balance_sheet <<- dbReadTable(con, "balance_sheet")
  # ... load other tables
}
```

### Adding Custom Validations

Implement validation rules from the specifications:

**Python:**
```python
def validate_qsr002(df):
    # Example: Goodwill should be zero
    if (df['R0010_Goodwill'] != 0).any():
        raise ValueError("Validation Error: Goodwill must be zero")
    return df
```

**R:**
```r
validate_qsr002 <- function(df) {
  # Example: Goodwill should be zero
  if (any(df$R0010_Goodwill != 0)) {
    stop("Validation Error: Goodwill must be zero")
  }
  return(df)
}
```

### Adding New QSR Returns

Extend the generators with new return types:

1. Add data generation function in `synthetic_data_generator`
2. Add transformation function in `qsr_report_generator`
3. Add to `generate_all_reports()` function
4. Document in README

## Validation Rules Implemented

Key validation rules from the QSR specifications:

| Rule | Description | Implementation |
|------|-------------|----------------|
| V00201 | Goodwill = 0 | Enforced in data generation |
| V00202 | Deferred Acquisition Costs = 0 | Enforced in data generation |
| V22001 | Members' Contributions >= 0 | Validated in generation |
| V24001 | Technical Provisions >= 0 | Validated in generation |
| MCR Cap/Floor | MCR between 25%-45% of SCR | Implemented in MCR calculation |

## Example Use Cases

### 1. Quarterly Regulatory Reporting
Generate all required QSR returns for submission to Lloyd's:
```bash
python qsr_report_generator.py
# Outputs all QSR returns to Data/ folder
```

### 2. Solvency Monitoring Dashboard
Create real-time solvency monitoring in Power BI:
- SCR/MCR ratios by syndicate
- Trend analysis over time
- Alert when ratios fall below thresholds

### 3. Capital Planning
Model capital requirements under different scenarios:
- Adjust risk parameters in synthetic data generator
- Re-run SCR calculations
- Compare capital requirements

### 4. Training and Development
Use synthetic data for:
- Training new team members
- Testing new analytics
- Developing custom reports

## Performance Considerations

### Large Datasets

For syndicates with extensive historical data:

**Python:**
- Use `pandas.read_csv(chunksize=10000)` for large files
- Consider `dask` for out-of-memory processing
- Use `data.to_parquet()` for faster I/O

**R:**
- Use `data.table::fread()` for faster reading
- Consider `arrow` package for large datasets
- Use `feather` format for R-Python interoperability

### Power BI Optimization

- Enable query folding where possible
- Use incremental refresh for time-series data
- Pre-aggregate at appropriate granularity
- Consider DirectQuery for very large datasets

## Troubleshooting

### Common Issues

**Issue: Module/Package not found**
- Python: `pip install pandas numpy openpyxl`
- R: `install.packages(c("dplyr", "tidyr"))`

**Issue: Data files not found**
- Run synthetic data generator first
- Check Data/ directory exists
- Verify file paths in scripts

**Issue: Power BI script errors**
- Test scripts independently first
- Check Python/R paths in Power BI options
- Use absolute paths, not relative

**Issue: Validation errors**
- Review QSR specifications document
- Check data quality in source files
- Verify calculation logic

## Compliance and Validation

This implementation is based on:
- **Solvency II Pillar 3 - QSR Return Specifications Q3 2025**
- EIOPA Reporting Guidelines
- Lloyd's Syndicate Reporting Requirements

**Important**: This is a development tool. All outputs should be reviewed and validated by qualified actuaries and regulatory compliance teams before submission.

## Contributing

To extend this project:

1. Add new return types in both Python and R
2. Implement additional validation rules
3. Enhance synthetic data realism
4. Add automated testing
5. Create example Power BI dashboards

## License

[Specify your license here]

## Support

For issues or questions:
- Review the Power BI guides in Python/ and R/ folders
- Check the source Excel specifications
- Test scripts independently before Power BI integration
- Verify all prerequisites are installed

## Version History

- **v1.0** (2025-11-21): Initial release
  - Python and R implementations
  - Synthetic data generators
  - 10 major QSR returns
  - Power BI integration guides

## Acknowledgments

Based on:
- Solvency II Pillar 3 QSR Return Specifications Q3 2025
- Lloyd's of London reporting requirements
- EIOPA reporting guidelines

---

**Disclaimer**: This implementation uses synthetic data for demonstration purposes. When using with actual Lloyd's syndicate data, ensure all regulatory requirements, data governance policies, and validation procedures are followed.
