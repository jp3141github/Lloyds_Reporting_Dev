# Solvency II Pillar 3 - Claims Reporting Automation

This repository contains Python and R scripts to automate the processing of Lloyd's of London claims data for Solvency II Pillar 3 reporting, specifically for RRA (Reserve Return Annual) forms.

## Overview

The scripts transform raw claims data into the required output tables for regulatory reporting, including:
- Detailed claims analysis
- Aggregations by syndicate and year of account
- Aggregations by risk code
- Aggregations by claim status
- Summary reports

## Repository Structure

```
Lloyds_Reporting_Dev/
├── python_scripts/
│   └── solvency_claims_processor.py    # Python implementation
├── r_scripts/
│   └── solvency_claims_processor.R     # R implementation
├── synthetic_data/
│   ├── generate_synthetic_data.py      # Data generator
│   └── synthetic_lloyds_claims_data.xlsx  # Sample data
├── Files_for_Claude/
│   └── [Original template file]
└── README.md
```

## Features

### Data Processing
- **Data Validation**: Ensures all required columns are present and properly formatted
- **Calculated Fields**:
  - Total Incurred as at end of period
  - Movement in Year
  - Reserve Movement
- **Multiple Aggregation Views**:
  - By Syndicate Number and Year of Account
  - By Risk Code
  - By Claim Status
  - Overall Summary

### Synthetic Data
The repository includes a synthetic data generator that creates realistic Lloyd's of London claims data with:
- 500+ sample claims across 8 syndicates
- Multiple risk codes and years of account (2015-2024)
- Realistic monetary amounts
- Various claim statuses
- Reference lookup tables

## Getting Started

### Prerequisites

#### For Python:
```bash
pip install pandas openpyxl numpy
```

#### For R:
```r
install.packages(c("readxl", "dplyr", "tidyr", "openxlsx"))
```

### Using the Python Script

#### Standalone Usage:
```python
from solvency_claims_processor import process_claims_data, export_to_excel

# Process the data
output_tables = process_claims_data('synthetic_data/synthetic_lloyds_claims_data.xlsx')

# Export results
export_to_excel(output_tables, 'claims_output.xlsx')
```

#### Power BI Integration:
1. Open Power BI Desktop
2. Get Data → More → Python script
3. Paste the script content or load the file
4. Use the `powerbi_transform()` function

### Using the R Script

#### Standalone Usage:
```r
source('r_scripts/solvency_claims_processor.R')

# Process the data
output_tables <- process_claims_data('synthetic_data/synthetic_lloyds_claims_data.xlsx')

# Export results
export_to_excel(output_tables, 'claims_output.xlsx')
```

#### Power BI Integration:
1. Open Power BI Desktop
2. Get Data → More → R script
3. Load your data and use `powerbi_transform(dataset)`

## Power BI Integration

See [POWERBI_GUIDE.md](POWERBI_GUIDE.md) for detailed instructions on integrating these scripts with Power BI.

## Input Data Format

The input Excel file should contain the following columns:

| Column Name | Type | Description |
|------------|------|-------------|
| Syndicate Number | Integer | Lloyd's syndicate number |
| Claim Reference | Text | Unique claim identifier |
| UMR | Text | Unique Market Reference |
| Risk Code | Text | Classification of risk type |
| Year of Account | Integer | Underwriting year |
| Original Currency | Text | Currency code (ISO) |
| Claim status at beginning of period | Text | Open/Closed/Reported in year |
| Claim status at end of period | Text | Open/Closed/Reported in year |
| Outstanding Claims Amount as at beginning of period | Number | Reserve amount at start |
| Paid to Date Amount | Number | Cumulative payments |
| Paid in Year amount | Number | Payments during period |
| Outstanding Claim amount as at end of period | Number | Reserve amount at end |
| Part VII Indicator | Text | Y/N indicator |
| Original Signing Number | Text | Contract signing reference |
| Original Signing Date | Date | Date of signing |
| UCR | Text | Optional reference |
| COR | Text | Optional reference |

## Output Tables

### 1. Detailed Claims
Complete processed dataset with all calculated fields

### 2. By Syndicate
Aggregated view showing totals for each syndicate and year of account

### 3. By Risk Code
Breakdown of claims by risk classification

### 4. By Claim Status
Analysis of claims by their current status

### 5. Summary
Overall summary statistics across all syndicates

## Generating New Synthetic Data

To create fresh synthetic data:

```bash
cd synthetic_data
python3 generate_synthetic_data.py
```

This will generate a new `synthetic_lloyds_claims_data.xlsx` file with 500 claims.

## Calculated Metrics

The scripts automatically calculate:

- **Total Incurred**: `Paid to Date + Outstanding at End`
- **Movement in Year**: `(Outstanding End - Outstanding Beginning) + Paid in Year`
- **Reserve Movement**: `Outstanding End - Outstanding Beginning`

## Risk Codes Reference

The synthetic data includes standard Lloyd's risk codes:
- 1-9: Primary risk classes
- 1E-8T: Treaty and extended classes
- AO, AP, AW: Aviation classes
- cf: Casualty Fire

## Testing

Use the provided synthetic data to test the scripts before applying to production data:

```python
# Python
output = process_claims_data('synthetic_data/synthetic_lloyds_claims_data.xlsx')
print(output['summary'])
```

```r
# R
output <- process_claims_data('synthetic_data/synthetic_lloyds_claims_data.xlsx')
print(output$summary)
```

## Compliance and Data Security

- This code is designed for internal reporting purposes
- Ensure compliance with GDPR and data protection regulations
- Do not commit actual claims data to version control
- Use synthetic data for testing and development

## Support and Maintenance

For issues or enhancements:
1. Review the code documentation
2. Check input data format matches requirements
3. Verify all required packages are installed
4. Consult Power BI integration guide for visualization issues

## License

Internal use only - Lloyd's of London regulatory reporting

## Version History

- v1.0 (2025-11): Initial release with Python and R implementations
  - Complete data processing pipeline
  - Power BI integration
  - Synthetic data generator
  - Multiple aggregation views

## Authors

Created for Lloyd's of London Solvency II reporting requirements
