# FSCS Data Generator for Power BI

This project provides both **Python** and **R** implementations for generating synthetic Lloyd's of London insurance data for Financial Services Compensation Scheme (FSCS) reporting. The scripts are designed to be used directly in Power BI for creating RRA (Reserve Return Annual) forms.

## Overview

The Financial Services Compensation Scheme (FSCS) requires Lloyd's syndicates to report specific information about protected contracts with eligible claimants. This tool generates realistic synthetic data for:

- **Gross Written Premiums (GWP)** - General Business
- **Gross Written Premiums (GWP)** - Life Business
- **Best Estimate Liabilities (BEL)** - General Business
- **Best Estimate Liabilities (BEL)** - Life Business

## Project Structure

```
FSCS_PowerBI/
├── Python/
│   ├── fscs_data_generator.py    # Main data generation module
│   ├── powerbi_query.py           # Power BI Python query script
│   ├── example_usage.py           # Usage examples and testing
│   ├── requirements.txt           # Python dependencies
│   └── README.md                  # Python-specific documentation
├── R/
│   ├── fscs_data_generator.R      # Main data generation module
│   ├── powerbi_query.R            # Power BI R query script
│   ├── example_usage.R            # Usage examples and testing
│   ├── install_packages.R         # R package installation script
│   └── README.md                  # R-specific documentation
└── README.md                      # This file
```

## Features

### Data Generation

- **Realistic Lloyd's Syndicate Numbers**: 4-digit numbers in the typical Lloyd's range (2000-6000)
- **Log-normal Distribution**: Premium values follow realistic insurance industry distributions
- **Correlated Liabilities**: Best Estimate Liabilities are generated as realistic multiples of premiums
- **Business Mix**: Syndicates can write general business, life business, or both
- **Transaction Detail**: Detailed contract-level data that aggregates to summary totals
- **Reproducible**: Seeded random number generation ensures consistent results

### Output Formats

1. **FSCS Summary Format**: Ready for regulatory submission
2. **Full Dataset**: Includes all calculated fields and analytics
3. **Detail Transactions**: Contract-level data for detailed analysis
4. **Excel Export**: Multi-sheet workbooks with summary statistics

## Quick Start

### For Python Users

```python
# Install dependencies
pip install -r Python/requirements.txt

# Generate data in Python
from fscs_data_generator import get_fscs_summary_data

# Get summary data
data = get_fscs_summary_data(num_syndicates=10, reporting_year=2024)
print(data)
```

### For R Users

```r
# Install dependencies
source("R/install_packages.R")

# Generate data in R
source("R/fscs_data_generator.R")

# Get summary data
data <- get_fscs_summary_data(num_syndicates=10, reporting_year=2024)
print(data)
```

## Power BI Integration

### Using Python in Power BI

1. Open Power BI Desktop
2. Go to **Get Data** > **More** > **Other** > **Python script**
3. Copy the contents of `Python/powerbi_query.py`
4. Paste into the script window and click **OK**
5. Select the `dataset` table and click **Load**

### Using R in Power BI

1. Open Power BI Desktop
2. Go to **Get Data** > **More** > **Other** > **R script**
3. Copy the contents of `R/powerbi_query.R`
4. Paste into the script window and click **OK**
5. Select the `dataset` table and click **Load**

**Note**: Ensure Python/R is configured in Power BI options before using scripts.

## Data Schema

### FSCS Summary Output

| Column | Type | Description |
|--------|------|-------------|
| Syndicate Number | Integer | Lloyd's syndicate identifier (4 digits) |
| Reporting Year | Integer | Year of reporting (e.g., 2024) |
| Reporting Date | Date | End of reporting period (31-Dec-YYYY) |
| GWP General Business (£) | Decimal | Gross written premium for general business |
| GWP Life Business (£) | Decimal | Gross written premium for life business |
| BEL General Business (£) | Decimal | Best estimate liabilities for general business |
| BEL Life Business (£) | Decimal | Best estimate liabilities for life business |
| Notes | String | Explanation of data scope |

### Detail Transaction Output

| Column | Type | Description |
|--------|------|-------------|
| syndicate_number | Integer | Lloyd's syndicate identifier |
| contract_id | String | Unique contract identifier |
| business_type | String | 'General' or 'Life' |
| business_class | String | Line of business classification |
| inception_date | Date | Contract start date |
| expiry_date | Date | Contract end date |
| gwp | Decimal | Contract gross written premium |
| bel | Decimal | Contract best estimate liability |
| currency | String | Currency code (GBP) |
| protected_contract | Boolean | Whether contract is FSCS protected |
| eligible_claimant | Boolean | Whether claimant is eligible |
| territory | String | Geographic territory |
| included_in_fscs | Boolean | Included in FSCS reporting |

## Data Quality and Assumptions

The synthetic data generator makes the following assumptions based on Lloyd's market characteristics:

### Premium Ranges

- **General Business**: £10M - £500M per syndicate
- **Life Business**: £1M - £100M per syndicate
- **Distribution**: Log-normal (typical for insurance)

### Best Estimate Liabilities

- **General Business**: 1.5x - 3.0x annual GWP
- **Life Business**: 3.0x - 8.0x annual GWP
- **Variation**: ±20% randomness

### Business Mix

- ~20% of syndicates may not write certain business types
- 90% of contracts are protected
- 85% of claimants are eligible
- Only protected contracts with eligible claimants are included in FSCS totals

## Regulatory Context

### FSCS Reporting Requirements

This template aligns with:

- **EIOPA Template References**:
  - S.05.01.01 (Premiums)
  - S.17.01.01 (Technical Provisions)
  - S.12.01.01 (Life Technical Provisions)

- **ASR (Annual Solvency Return) References**:
  - ASR240, ASR241, ASR280, ASR283 (General business)
  - ASR440, ASR450 (Premiums)

### Reporting Period

Data is generated for the year ending **31 December 2024** by default, but can be configured for any year.

## Customization

### Adjusting Parameters

Both Python and R implementations support customization:

```python
# Python
generator = FSCSDataGenerator(
    num_syndicates=20,        # Number of syndicates
    reporting_year=2024,      # Reporting year
    random_seed=42            # For reproducibility
)
```

```r
# R
generator <- FSCSDataGenerator(
  num_syndicates = 20,
  reporting_year = 2024,
  random_seed = 42
)
```

### Modifying Distributions

Edit the generation functions in either implementation to adjust:
- Premium ranges and distributions
- BEL multipliers
- Business mix percentages
- Contract characteristics

## Testing

Both implementations include example usage scripts:

```bash
# Python
cd Python
python example_usage.py

# R
cd R
Rscript example_usage.R
```

## Requirements

### Python

- Python 3.8+
- pandas >= 2.0.0
- numpy >= 1.24.0
- openpyxl >= 3.1.0

### R

- R 4.0+
- dplyr
- tibble
- lubridate
- writexl

## Troubleshooting

### Power BI Python/R Not Configured

**Error**: "Python/R scripting is not enabled"

**Solution**:
1. Go to File > Options and settings > Options
2. Select Python/R scripting
3. Set the Python/R installation directory
4. Restart Power BI Desktop

### Missing Dependencies

**Python**: Run `pip install -r requirements.txt`

**R**: Run `source("install_packages.R")`

### Data Not Appearing in Power BI

Ensure the output variable is named:
- Python: `dataset`
- R: `dataset`

Power BI looks for these specific variable names.

## Use Cases

1. **Power BI Report Development**: Test FSCS reports with realistic data
2. **Data Pipeline Testing**: Validate ETL processes before production
3. **Training and Demos**: Demonstrate FSCS reporting without sensitive data
4. **Analytics Development**: Build analytical models on representative data
5. **Regulatory Dry Runs**: Practice FSCS submission processes

## Limitations

- This is **synthetic data** for testing purposes only
- Not suitable for actual regulatory submission
- Does not include all regulatory validation rules
- Simplified business logic compared to actual Lloyd's operations

## Contributing

To contribute to this project:

1. Test both Python and R implementations
2. Validate data quality and distributions
3. Suggest improvements via pull requests
4. Report issues with specific examples

## License

This project is provided for internal Lloyd's reporting development and testing purposes.

## Support

For questions or issues:

1. Check the implementation-specific READMEs in Python/ and R/ folders
2. Review example_usage scripts for detailed examples
3. Consult Power BI documentation for scripting setup

## Version History

- **v1.0** (2024-11-21): Initial release
  - Python and R implementations
  - Power BI integration scripts
  - FSCS summary and detail data generation
  - Example usage and documentation

---

**Note**: This tool generates synthetic data for development and testing. Always use actual regulatory data for official FSCS submissions.
