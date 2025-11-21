# Lloyd's Reporting Development - RRA Premium Processing

This repository contains Python and R scripts for processing Solvency II Pillar 3 Risk and Claims Reporting data, specifically for generating Reserve Return Annual (RRA) forms required by Lloyd's of London.

## 📁 Repository Structure

```
Lloyds_Reporting_Dev/
├── python_scripts/          # Python scripts for Power BI
│   └── rra_premium_processing.py
├── r_scripts/              # R scripts for Power BI
│   └── rra_premium_processing.R
├── synthetic_data/         # Synthetic Lloyd's data for testing
│   ├── generate_synthetic_data.py
│   ├── synthetic_lloyds_premium_data.csv
│   ├── synthetic_lloyds_premium_data.xlsx
│   └── rra_premium_outputs.xlsx
└── Files_for_Claude/       # Source templates and specifications
    └── Solvency II Pillar 3 - Risk and Claim Reporting - Step B premium template.xlsx
```

## 🎯 Purpose

These scripts convert the Solvency II Pillar 3 Premium Reporting template into automated data processing pipelines that can be integrated with Power BI to produce RRA output tables.

### Input Data Structure

The scripts expect premium data with the following columns:
- **Syndicate Number**: Lloyd's syndicate identifier
- **UMR**: Unique Market Reference
- **Insured Country**: Country of the insured party
- **Risk Location**: Geographic location of the risk
- **Insured Name**: Name of the insured entity
- **Insured - Policyholder Type**: Classification (RETAIL, BUSINESS, CORPORATE, COMMERCIAL)
- **Risk Code**: Lloyd's risk classification code
- **Risk / Certificate Reference**: Unique risk identifier
- **Original Currency**: Currency of the policy
- **Sum Insured**: Total insured amount
- **Gross Annual Premium in Period**: Premium amount
- **YOA**: Year of Account
- **Part VII Indicator**: Part VII transfer flag (Y/N)
- **Original Signing Number**: Policy signing reference
- **Original Signing Date**: Date of policy signing

### Output Tables Generated

Both Python and R scripts generate the following RRA output tables:

1. **Premium Summary By Syndicate**: Aggregated premium data by syndicate and year
2. **Premium By Risk Code**: Premium breakdown by risk classification
3. **Geographic Analysis**: Premium distribution by country with market share
4. **Policyholder Type Analysis**: Analysis by retail vs business segments
5. **Currency Analysis**: Currency exposure breakdown
6. **Part VII Analysis**: Part VII transfer analysis
7. **Detailed Risk Register**: Complete risk-level data with calculated metrics

## 🐍 Python Implementation

### Requirements

```bash
pip install pandas numpy openpyxl
```

### Usage

#### Standalone Execution

```python
# Run the script directly
python python_scripts/rra_premium_processing.py
```

#### Power BI Integration

**Method 1: Python Visual**
1. Add a Python visual to your Power BI report
2. Drag the required data fields into the visual
3. Use the following script:

```python
# The 'dataset' variable contains your data from Power BI
import sys
sys.path.append('path/to/python_scripts')
from rra_premium_processing import RRAPremiumProcessor

processor = RRAPremiumProcessor(dataset)
result = processor.create_premium_summary_by_syndicate()

# Power BI will automatically visualize the result
print(result)
```

**Method 2: Power Query Python Script**
1. Go to Transform Data → New Source → Python script
2. Use the following code:

```python
import pandas as pd
from rra_premium_processing import RRAPremiumProcessor

# Load your data
premium_data = pd.read_csv('your_data_path.csv')

# Process
processor = RRAPremiumProcessor(premium_data)
outputs = processor.generate_all_outputs()

# Return desired output
Premium_Summary = outputs['Premium_Summary_By_Syndicate']
Geographic_Analysis = outputs['Geographic_Analysis']
```

### Python Functions Reference

```python
# Initialize processor
processor = RRAPremiumProcessor(premium_data)

# Generate individual outputs
syndicate_summary = processor.create_premium_summary_by_syndicate()
risk_analysis = processor.create_premium_by_risk_code()
geo_analysis = processor.create_geographic_analysis()
type_analysis = processor.create_policyholder_type_analysis()
currency_analysis = processor.create_currency_analysis()
part_vii = processor.create_part_vii_analysis()
risk_register = processor.create_detailed_risk_register()

# Generate all outputs at once
all_outputs = processor.generate_all_outputs()

# Export to Excel
processor.export_to_excel('output_file.xlsx')
```

## 📊 R Implementation

### Requirements

```r
install.packages(c("dplyr", "tidyr", "readr", "writexl", "lubridate"))
```

### Usage

#### Standalone Execution

```r
# Run the script
Rscript r_scripts/rra_premium_processing.R
```

#### Power BI Integration

**Method 1: R Visual**
1. Enable R visuals in Power BI (File → Options → R scripting)
2. Add an R visual to your report
3. Drag data fields into the visual
4. Use the following script:

```r
# The 'dataset' variable contains your data from Power BI
source('path/to/r_scripts/rra_premium_processing.R')

result <- create_premium_summary_by_syndicate(dataset)
print(result)

# Create visualizations
library(ggplot2)
ggplot(result, aes(x=YOA, y=`Total Premium`, fill=factor(`Syndicate Number`))) +
  geom_bar(stat="identity") +
  theme_minimal()
```

**Method 2: Power Query R Script**
1. Go to Transform Data → New Source → R script
2. Use the following code:

```r
library(readr)
source('path/to/r_scripts/rra_premium_processing.R')

# Load your data
premium_data <- read_csv('your_data_path.csv')

# Generate outputs
outputs <- generate_all_rra_outputs(premium_data)

# Return desired output
Premium_Summary <- outputs$Premium_Summary_By_Syndicate
```

### R Functions Reference

```r
# Source the script
source('r_scripts/rra_premium_processing.R')

# Generate individual outputs
syndicate_summary <- create_premium_summary_by_syndicate(premium_data)
risk_analysis <- create_premium_by_risk_code(premium_data)
geo_analysis <- create_geographic_analysis(premium_data)
type_analysis <- create_policyholder_type_analysis(premium_data)
currency_analysis <- create_currency_analysis(premium_data)
part_vii <- create_part_vii_analysis(premium_data)
risk_register <- create_detailed_risk_register(premium_data)

# Generate all outputs
all_outputs <- generate_all_rra_outputs(premium_data)

# Export to Excel
export_rra_outputs(premium_data, 'output_file.xlsx')
```

## 📦 Synthetic Data

The repository includes synthetic Lloyd's of London premium data for testing purposes.

### Generate New Synthetic Data

```python
python synthetic_data/generate_synthetic_data.py
```

This will create:
- `synthetic_lloyds_premium_data.csv` - 1,000 realistic premium records
- `synthetic_lloyds_premium_data.xlsx` - Same data in Excel format with summary sheet

### Synthetic Data Characteristics

- **1,000 premium records** across 10 syndicates
- **5 years of account** (2021-2025)
- **4 policyholder types**: RETAIL, BUSINESS, CORPORATE, COMMERCIAL
- **18 countries** including UK, US, EU, and Asia-Pacific
- **7 currencies**: GBP, USD, EUR, JPY, CHF, AUD, CAD
- **15 risk codes** following Lloyd's classifications
- **Realistic premium ranges**:
  - Retail: £5,000 - £100,000
  - Business: £50,000 - £500,000
  - Corporate: £500,000 - £5,000,000
  - Commercial: £100,000 - £1,000,000

## 🔧 Power BI Setup Guide

### Python Configuration

1. **Install Python** (if not already installed)
   - Download from [python.org](https://www.python.org/)
   - Ensure Python is added to PATH

2. **Configure Power BI**
   - File → Options and settings → Options
   - Python scripting → Set Python home directory
   - Install required packages: `pip install pandas numpy openpyxl`

3. **Enable Python visuals**
   - File → Options and settings → Options
   - Preview features → Enable Python visuals

### R Configuration

1. **Install R** (if not already installed)
   - Download from [r-project.org](https://www.r-project.org/)

2. **Install RStudio** (optional but recommended)
   - Download from [rstudio.com](https://www.rstudio.com/)

3. **Configure Power BI**
   - File → Options and settings → Options
   - R scripting → Set R home directory
   - Install required packages in R console

4. **Enable R visuals**
   - File → Options and settings → Options
   - Preview features → Enable R visuals

## 📈 Example Outputs

The scripts generate comprehensive RRA tables. Here's a sample of the **Premium Summary By Syndicate**:

| Syndicate Number | YOA  | Total Premium | Average Premium | Number of Risks | Total Sum Insured | Unique UMRs |
|------------------|------|---------------|-----------------|-----------------|-------------------|-------------|
| 623              | 2021 | 13,945,477.21 | 820,322.19      | 17              | 182,003,500       | 17          |
| 623              | 2022 | 12,285,044.54 | 534,132.37      | 23              | 150,141,600       | 23          |
| 1234             | 2021 | 15,234,567.89 | 678,123.45      | 22              | 195,876,543       | 22          |

**Geographic Analysis** includes market share calculations:

| Country        | YOA  | Total Premium | Premium Share % |
|----------------|------|---------------|-----------------|
| UNITED KINGDOM | 2024 | 45,678,901.23 | 20.53%          |
| UNITED STATES  | 2024 | 38,765,432.10 | 17.42%          |
| GERMANY        | 2024 | 25,432,109.87 | 11.43%          |

## 🎓 Lloyd's Reporting Context

### What is RRA?

The **Reserve Return Annual (RRA)** is a key regulatory reporting requirement for Lloyd's syndicates under Solvency II Pillar 3. It provides:

- Detailed reserving information by class of business
- Geographic and currency exposure analysis
- Historical claims development data
- Part VII transfer tracking

### Solvency II Pillar 3

Solvency II is the EU's insurance regulatory framework with three pillars:
- **Pillar 1**: Quantitative requirements (capital requirements)
- **Pillar 2**: Qualitative requirements (governance)
- **Pillar 3**: Disclosure requirements (transparency and reporting)

### Part VII Transfers

Part VII of the UK Financial Services and Markets Act 2000 allows insurance business transfers between entities. The scripts track these transfers through the Part VII Indicator field.

## 🔍 Data Quality Checks

Both scripts include built-in validation:

- ✅ Required column verification
- ✅ Data type validation
- ✅ Numeric field range checks
- ✅ Unique identifier validation (UMR)
- ✅ Date format validation

## 🤝 Contributing

This is a development repository for Lloyd's reporting automation. To contribute:

1. Test scripts with your own data
2. Report issues or enhancement requests
3. Submit pull requests with improvements

## 📝 Notes

- **Data Privacy**: The synthetic data is completely fictional and does not represent any real Lloyd's syndicates or policies
- **Regulatory Compliance**: Always verify outputs against Lloyd's reporting specifications
- **Performance**: Scripts are optimized for datasets up to 100,000 records. For larger datasets, consider chunking or parallel processing
- **Currency Conversion**: Scripts do not perform currency conversion. Use external exchange rate data for GBP equivalency calculations

## 📞 Support

For questions about Lloyd's reporting requirements, consult:
- Lloyd's Market Reporting team
- Your syndicate's managing agent
- Lloyd's Performance Management website

## 📄 License

This project is provided as-is for Lloyd's market participants and developers working with Solvency II reporting requirements.

---

**Last Updated**: November 2025
**Version**: 1.0
**Solvency II Pillar 3 Reporting Period**: Annual Returns
