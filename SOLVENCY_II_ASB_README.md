# Solvency II Pillar 3 - ASB Returns Implementation

This repository contains Python and R implementations for generating Lloyd's of London Solvency II Pillar 3 ASB (Annual Solvency and Balance Sheet) returns with synthetic data for Power BI reporting.

## Overview

Based on the **Solvency II Pillar 3 - ASB Return Specifications Annual 2024** Excel file, these scripts generate synthetic insurance data that matches the Lloyd's reporting requirements for:

- **ASB 245/246/247** (S.19.01.01): Non-Life Insurance Claims Information
- **ASB 248** (S.19.01.01): Non-Life Insurance Claims Information - Inflation Rates

## Repository Structure

```
.
├── Solvency_II_ASB_Python/          # Python implementation
│   ├── README.md                     # Python documentation
│   ├── synthetic_data_generator.py  # Core data generator
│   ├── powerbi_asb_returns.py       # Power BI integration script
│   └── export_to_excel.py           # Excel export utility
│
├── Solvency_II_ASB_R/               # R implementation
│   ├── README.md                     # R documentation
│   ├── synthetic_data_generator.R   # Core data generator
│   ├── powerbi_asb_returns.R        # Power BI integration script
│   └── export_to_excel.R            # Excel export utility
│
└── Files_for_Claude/
    └── Solvency II Pillar 3 - ASB Return Specifications Annual 2024.xlsx
```

## Quick Start

### Python Version

**Requirements:**
```bash
pip install pandas numpy openpyxl
```

**Generate Data:**
```bash
cd Solvency_II_ASB_Python
python synthetic_data_generator.py
```

**Use in Power BI:**
1. Open Power BI Desktop
2. Get Data > Python script
3. Copy contents of `powerbi_asb_returns.py`
4. Select desired tables

### R Version

**Requirements:**
```r
install.packages(c("tidyverse", "writexl"))
```

**Generate Data:**
```r
cd Solvency_II_ASB_R
source("synthetic_data_generator.R")
all_data <- generate_all_asb_data()
```

**Use in Power BI:**
1. Open Power BI Desktop
2. Get Data > R script
3. Copy contents of `powerbi_asb_returns.R`
4. Select desired tables

## Data Tables Generated

### 1. ASB 245/246/247 - Claims Data

Non-Life Insurance Claims Information with development triangles:

- **Dimensions**: Currency, Line of Business, Underwriting Year, Development Year
- **Measures**:
  - Gross Claims Paid
  - Reinsurance Recoveries
  - Best Estimate Claims Provisions (Gross & Reinsurance)
  - Discounting adjustments
  - RBNS (Reported But Not Settled) claims

### 2. ASB 248 - Inflation Rates

Claims inflation information by line of business:

- **Dimensions**: Currency, Line of Business, Underwriting Year
- **Measures**:
  - Historic inflation rates (Total, External, Endogenous)
  - Expected inflation rates (Total, External, Endogenous)

### 3. Supporting Tables

- **Metadata**: Syndicate information and generation details
- **Lines of Business**: EIOPA classification reference
- **Claims Summary**: Aggregated by year and line of business
- **Development Analysis**: Claims development patterns

## Features

### Synthetic Data Characteristics

- **Realistic Claims Development**: Models how claims settle over 10+ years
- **Multi-Currency Support**: GBP, USD, EUR
- **12 Lines of Business**: Following EIOPA classifications
- **Reinsurance Modeling**: 10-40% of gross claims
- **Inflation Patterns**: Varying by line of business (1.5-4.5% range)
- **Reproducible**: Fixed random seeds for consistent results

### Lines of Business (EIOPA)

| Code | Description |
|------|-------------|
| LOB01 | Medical expense insurance |
| LOB02 | Income protection insurance |
| LOB03 | Workers compensation insurance |
| LOB04 | Motor vehicle liability insurance |
| LOB05 | Other motor insurance |
| LOB06 | Marine, aviation and transport insurance |
| LOB07 | Fire and other damage to property insurance |
| LOB08 | General liability insurance |
| LOB09 | Credit and suretyship insurance |
| LOB10 | Legal expenses insurance |
| LOB11 | Assistance |
| LOB12 | Miscellaneous financial loss |

## Power BI Integration

Both Python and R implementations are designed for seamless Power BI integration:

### Using Python in Power BI

1. **Configure Python in Power BI**:
   - File > Options > Python scripting
   - Set Python installation path
   - Install required packages

2. **Load Data**:
   - Get Data > Python script
   - Paste `powerbi_asb_returns.py`
   - Select tables to import

3. **Available Tables**:
   - ASB_245_246_247_Claims
   - ASB_248_InflationRates
   - Metadata
   - LinesOfBusiness
   - Claims_Summary
   - Development_Analysis

### Using R in Power BI

1. **Configure R in Power BI**:
   - File > Options > R scripting
   - Set R installation path
   - Install required packages in R

2. **Load Data**:
   - Get Data > R script
   - Paste `powerbi_asb_returns.R`
   - Select tables to import

3. **Same tables available as Python version**

## Configuration

Both implementations support customization via configuration parameters:

```python
# Python
SYNDICATE_NUMBER = '1234'
SYNDICATE_NAME = 'Your Syndicate Name'
START_YEAR = 2015
END_YEAR = 2024
CLAIMS_RECORDS = 500
INFLATION_RECORDS = 200
```

```r
# R
SYNDICATE_NUMBER <- "1234"
SYNDICATE_NAME <- "Your Syndicate Name"
START_YEAR <- 2015
END_YEAR <- 2024
CLAIMS_RECORDS <- 500
INFLATION_RECORDS <- 200
```

## Export Options

### CSV Export
Both implementations can export to CSV for manual Power BI import or other uses.

### Excel Export
Generate multi-sheet Excel workbooks matching Lloyd's specifications:

**Python:**
```python
from export_to_excel import export_asb_returns_to_excel
export_asb_returns_to_excel('output.xlsx')
```

**R:**
```r
source("export_to_excel.R")
export_asb_returns_to_excel("output.xlsx")
```

## Use Cases

1. **Power BI Report Development**: Create and test ASB return dashboards without real data
2. **Training**: Learn Solvency II reporting requirements
3. **System Testing**: Validate data pipelines and transformations
4. **Template Creation**: Build reusable Power BI templates for ASB returns
5. **Data Quality Checks**: Test validation rules and business logic

## Data Specifications

### ASB 245/246/247 Schema

| Column | Type | Description |
|--------|------|-------------|
| Currency | String | GBP/USD/EUR |
| LineOfBusiness | String | LOB01-LOB12 |
| UnderwritingYear | Integer | 2015-2024 |
| DevelopmentYear | Integer | 0-10 years |
| GrossClaimPaid | Numeric | Claims paid (000s) |
| ReinsuranceRecoveries | Numeric | Reins recoveries (000s) |
| GrossUndiscountedBEClaimsProvisions | Numeric | Best estimate provisions |
| DiscountingGrossBEClaimsProvisions | Numeric | Discounting adjustment |
| ... | ... | See detailed READMEs |

### ASB 248 Schema

| Column | Type | Description |
|--------|------|-------------|
| Currency | String | GBP/USD/EUR |
| LineOfBusiness | String | LOB01-LOB12 |
| UnderwritingYear | Integer | 2015-2024 |
| HistoricInflationRateTotal | Numeric | Historic rate % |
| ExpectedInflationRateTotal | Numeric | Expected rate % |
| ... | ... | See detailed READMEs |

## Compliance & Standards

- **EIOPA Guidelines**: Follows European Insurance and Occupational Pensions Authority standards
- **Solvency II Directive**: Complies with EU insurance regulation requirements
- **Lloyd's Specifications**: Based on official ASB return templates
- **S.19.01.01**: Implements the Non-Life Insurance Claims QRT template

## Important Notes

- **Synthetic Data Only**: All generated data is synthetic and for testing/demonstration purposes
- **Not for Regulatory Submission**: Do not use for actual regulatory reporting
- **Development Patterns**: Claims development follows realistic but simplified patterns
- **Random Seed**: Default seed (42) ensures reproducibility across runs
- **Monetary Units**: All values in thousands (000s)

## Documentation

- **Python README**: `/Solvency_II_ASB_Python/README.md` - Detailed Python documentation
- **R README**: `/Solvency_II_ASB_R/README.md` - Detailed R documentation
- **Original Spec**: `/Files_for_Claude/Solvency II Pillar 3 - ASB Return Specifications Annual 2024.xlsx`

## Choosing Between Python and R

Both implementations are functionally equivalent:

**Choose Python if:**
- You're more comfortable with Python/pandas
- Your team uses Python for data analysis
- You want to integrate with other Python tools

**Choose R if:**
- You're more comfortable with R/tidyverse
- Your team uses R for statistical analysis
- You prefer R's syntax for data manipulation

**Both provide:**
- Identical data structures
- Same configuration options
- Power BI compatibility
- CSV and Excel export

## Support & Contribution

For questions, issues, or contributions:
1. Check the detailed READMEs in each implementation folder
2. Review the original Excel specification file
3. Consult EIOPA Solvency II guidelines
4. Refer to Lloyd's reporting documentation

## Version History

- **v1.0** (2024): Initial implementation
  - Python and R data generators
  - Power BI integration scripts
  - Excel export utilities
  - Complete documentation

## License

This code is provided for educational and development purposes. Always consult with compliance and regulatory teams before using any synthetic data generation tools in production environments.

---

**Note**: This implementation is based on the Annual 2024 ASB Return Specifications. Always ensure you're using the most current Lloyd's specifications for your reporting period.
