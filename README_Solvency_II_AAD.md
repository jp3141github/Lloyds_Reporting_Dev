# Solvency II Pillar 3 - AAD Returns for Power BI

This repository contains Python and R implementations for generating and transforming Solvency II Pillar 3 Annual Assets Data (AAD) returns for Lloyd's of London, designed for seamless integration with Microsoft Power BI.

## Overview

The **Annual Assets Data (AAD)** return is a critical regulatory submission required under Solvency II Pillar 3 reporting. This implementation provides:

1. **Synthetic data generators** to create realistic Lloyd's of London style test data
2. **Power BI transformation scripts** to convert raw data into regulatory AAD return formats
3. **Validation logic** to ensure compliance with EIOPA specifications
4. **Support for both Python and R** to accommodate different organizational preferences

## AAD Return Templates

This implementation covers all six AAD return templates:

| Template | EIOPA Code | Description |
|----------|------------|-------------|
| AAD230 | S.06.02.01 | List of assets (bonds, equities, cash, etc.) |
| AAD233 | S.08.01.01 | Open derivatives (swaps, options, futures) |
| AAD235 | S.09.01.01 | Income, gains and losses by asset category |
| AAD236 | S.06.03.01 | Collective Investment Undertakings (CIU) look-through |
| AAD237 | S.10.01.01 | Loans and mortgages |
| AAD238 | S.11.01.01 | Property holdings |

## Repository Structure

```
├── Solvency_II_AAD_Python/          # Python implementation
│   ├── synthetic_data_generator.py   # Generate test data
│   ├── powerbi_aad230_transformer.py # AAD230 transformer
│   ├── powerbi_aad233_transformer.py # AAD233 transformer
│   ├── powerbi_aad235_transformer.py # AAD235 transformer
│   ├── powerbi_aad236_transformer.py # AAD236 transformer
│   ├── powerbi_aad237_transformer.py # AAD237 transformer
│   ├── powerbi_aad238_transformer.py # AAD238 transformer
│   ├── requirements.txt              # Python dependencies
│   └── README.md                     # Python documentation
│
├── Solvency_II_AAD_R/               # R implementation
│   ├── synthetic_data_generator.R    # Generate test data
│   ├── powerbi_aad230_transformer.R  # AAD230 transformer
│   ├── powerbi_all_aad_transformers.R # Combined transformers
│   └── README.md                     # R documentation
│
└── Files_for_Claude/
    └── Solvency II Pillar 3 - AAD Return Specifications Annual 2024.xlsx
```

## Quick Start

### Option 1: Python Implementation

#### 1. Install Dependencies

```bash
cd Solvency_II_AAD_Python
pip install -r requirements.txt
```

#### 2. Generate Synthetic Data

```bash
python synthetic_data_generator.py
```

This creates a `synthetic_data/` directory with CSV files for all AAD tables.

#### 3. Use in Power BI

**Method A: Load synthetic data**
- Open Power BI Desktop
- Get Data > Python script
- Run `synthetic_data_generator.py`
- Select the tables to import

**Method B: Transform existing data**
- Load your data into Power BI
- In Power Query Editor, select your query
- Transform > Run Python Script
- Paste the appropriate `powerbi_aadXXX_transformer.py` script

### Option 2: R Implementation

#### 1. Install Dependencies

```R
install.packages(c("dplyr", "tidyr", "lubridate"))
```

#### 2. Generate Synthetic Data

```R
source("Solvency_II_AAD_R/synthetic_data_generator.R")
datasets <- main()
```

#### 3. Use in Power BI

**Method A: Load synthetic data**
- Open Power BI Desktop
- Get Data > R script
- Run `synthetic_data_generator.R`
- Select the tables to import

**Method B: Transform existing data**
- Load your data into Power BI
- In Power Query Editor, select your query
- Transform > Run R Script
- Paste the `powerbi_aad230_transformer.R` script

## Features

### Synthetic Data Generation

Both implementations generate realistic Lloyd's of London insurance data:

- **1,000 asset records** with proper ISIN/SEDOL/CUSIP codes
- **100 derivative contracts** including swaps, options, and futures
- **12 income categories** with P&L data
- **50 investment funds** with look-through details
- **200 loan/mortgage records** with LTV calculations
- **100 property holdings** with rental yield metrics

### Data Transformation

The transformers provide:

- **Column mapping** to EIOPA reference codes (C0040, C0060, etc.)
- **Data type validation** (numeric, date, categorical)
- **Business rule validation** (required fields, value ranges, cross-field checks)
- **Calculated fields** (Total Solvency II Amount, LTV ratios, rental yields)
- **Validation reporting** (errors and warnings printed to script output)

### Validation Rules

Key validations include:

- ✓ No duplicate Asset IDs
- ✓ Required fields populated (Asset ID, Portfolio, Total SII Amount)
- ✓ Valid portfolio codes (L, NL, RF, OIF, SF, G)
- ✓ Valid ID code formats (ISIN: 12 chars, SEDOL: 7 chars, CUSIP: 9 chars)
- ✓ Fund Number required for RF (Ring-Fenced Fund) portfolio
- ✓ Positive amounts where applicable
- ✓ Valid date formats and ranges

## Power BI Integration

### Configuring Python in Power BI

1. Open Power BI Desktop
2. Go to **File** > **Options and settings** > **Options**
3. Select **Python scripting**
4. Set your Python home directory
5. Ensure pandas, numpy, and openpyxl are installed

### Configuring R in Power BI

1. Open Power BI Desktop
2. Go to **File** > **Options and settings** > **Options**
3. Select **R scripting**
4. Set your R home directory
5. Ensure dplyr, tidyr, and lubridate are installed

### Using the Scripts

#### For Data Generation:
1. Get Data > More > Other > Python script (or R script)
2. Paste the synthetic data generator script
3. Click OK
4. Select which tables to load
5. Transform data as needed

#### For Data Transformation:
1. Load your source data (CSV, Excel, database, etc.)
2. Select the query in Power Query Editor
3. Transform > Run Python Script (or Run R Script)
4. Paste the appropriate transformer script
5. Review validation output
6. Click OK to apply transformation

### Performance Considerations

- **Small datasets (<10K rows)**: Scripts run quickly in Power BI
- **Medium datasets (10K-100K rows)**: Consider pre-processing
- **Large datasets (>100K rows)**: Recommended to transform outside Power BI and import results

## Use Cases

### 1. Regulatory Reporting
Generate compliant AAD returns for submission to regulators (PRA, EIOPA, Lloyd's).

### 2. Testing & Development
Use synthetic data to test Power BI reports before connecting to production systems.

### 3. Data Quality Checks
Validate source data against Solvency II specifications before submission.

### 4. Training & Documentation
Train analysts on AAD return structure and requirements using realistic test data.

## Customization

### Modifying Field Mappings

If your source data has different column names, update the mapping dictionaries in the transformer scripts:

**Python:**
```python
aad230_columns = {
    'C0060_Portfolio': 'Portfolio',  # Change to your column name
    'C0040_Asset_ID_Code': 'AssetID',  # Example: your column is 'AssetID'
    # ...
}
```

**R:**
```R
output_df <- dataset %>%
  mutate(
    C0060_Portfolio = Your_Portfolio_Column,  # Change to your column name
    # ...
  )
```

### Adding Custom Validations

Add business-specific validation rules:

**Python:**
```python
def custom_validation(df):
    # Your logic here
    if condition:
        validation_results['warnings'].append("Custom warning message")
```

**R:**
```R
custom_check <- dataset %>%
  filter(your_condition) %>%
  nrow()

if (custom_check > 0) {
  cat("Custom warning message\n")
}
```

## Sample Visualizations

Once data is loaded and transformed in Power BI, you can create:

- **Asset Allocation Dashboard**: Breakdown by CIC code, portfolio, currency
- **Solvency II Value Trends**: Time series of total SII amounts
- **Issuer Concentration**: Top 20 issuers by exposure
- **Maturity Profile**: Asset maturities over time
- **Credit Quality Distribution**: Assets by credit rating
- **Derivative Exposure**: Notional amounts by counterparty
- **Income Analysis**: Dividends, interest, and gains by asset category
- **Property Portfolio**: Geographic distribution and rental yields

## Regulatory Compliance

This implementation is based on:

- **Solvency II Pillar 3 - AAD Return Specifications Annual 2024**
- **EIOPA Reporting Guidelines**
- **Lloyd's of London Reporting Requirements**

The code follows EIOPA taxonomy and validation rules as specified in the official documentation.

## Testing

### Python Tests

```bash
cd Solvency_II_AAD_Python
python synthetic_data_generator.py

# Verify output
ls synthetic_data/
# Should show: AAD230_Assets.csv, AAD233_Derivatives.csv, etc.
```

### R Tests

```R
source("Solvency_II_AAD_R/synthetic_data_generator.R")
datasets <- main()

# Verify output
list.files("synthetic_data/")
# Should show: AAD230_Assets.csv, AAD233_Derivatives.csv, etc.
```

## Troubleshooting

### Common Issues

**Python:**
- **ModuleNotFoundError**: Install missing packages with `pip install package_name`
- **Encoding errors**: Ensure CSV files are UTF-8 encoded
- **Date parsing errors**: Check date format matches expected YYYY-MM-DD

**R:**
- **Package not found**: Install with `install.packages("package_name")`
- **Object not found**: Check column names match transformer expectations
- **Date format issues**: Use lubridate functions to parse dates

**Power BI:**
- **Script timeout**: Reduce dataset size or increase timeout in Power BI options
- **Permission errors**: Ensure Power BI has access to Python/R installation
- **Memory errors**: Process data in batches or pre-aggregate

## Support & Documentation

- **Python README**: `Solvency_II_AAD_Python/README.md`
- **R README**: `Solvency_II_AAD_R/README.md`
- **EIOPA Specifications**: `Files_for_Claude/Solvency II Pillar 3 - AAD Return Specifications Annual 2024.xlsx`

## Contributing

For issues, enhancements, or questions about this implementation, please contact the Risk Reporting team.

## License

This implementation is for internal use with Lloyd's of London regulatory reporting.

---

## Summary

This repository provides a complete solution for generating and transforming Solvency II AAD returns in Power BI:

✓ **Two language options** (Python and R) for maximum flexibility
✓ **Synthetic data generation** for testing and development
✓ **All six AAD templates** (230, 233, 235, 236, 237, 238)
✓ **Comprehensive validation** against EIOPA specifications
✓ **Production-ready** for regulatory reporting
✓ **Well-documented** with examples and troubleshooting guides

Start with the synthetic data generators to understand the data structure, then adapt the transformers to your organization's source systems for production use.
