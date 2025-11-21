# Lloyd's of London Synthetic Data Generator

This repository contains Python and R scripts for generating synthetic Lloyd's of London insurance data for SCR (Solvency Capital Requirement) reporting and analysis in Power BI.

## Overview

These scripts generate synthetic data matching the structure required by the **2025 SCR New SBF no LCR Template** for Lloyd's syndicates. The data includes:

- **Syndicate reference data** (managing agents, business classes, capacity)
- **SCR impact metrics** (uSCR and 1SCR movements)
- **Loss ratio validation** (Plan vs Modelled loss ratios)

## Repository Structure

```
Lloyds_Reporting_Dev/
├── Python_Scripts/
│   ├── generate_lloyds_synthetic_data.py    # Standalone Python generator
│   ├── powerbi_lloyds_data.py               # Power BI Python script
│   └── README.md                             # Python documentation
├── R_Scripts/
│   ├── generate_lloyds_synthetic_data.R     # Standalone R generator
│   ├── powerbi_lloyds_data.R                # Power BI R script
│   └── README.md                             # R documentation
├── Files_for_Claude/
│   └── 2025 SCR New SBF no LCR Template.xlsx # Source template
└── SYNTHETIC_DATA_README.md                  # This file
```

## Quick Start

### Python

```bash
# Install dependencies
pip install pandas numpy openpyxl

# Run the generator
cd Python_Scripts
python generate_lloyds_synthetic_data.py

# Output will be in Python_Scripts/output/
```

### R

```r
# Install dependencies
install.packages("dplyr")

# Run the generator
setwd("R_Scripts")
source("generate_lloyds_synthetic_data.R")
```

## Power BI Integration

### Using Python in Power BI

1. Open Power BI Desktop
2. **Home** → **Get Data** → **More** → **Python script**
3. Copy and paste `Python_Scripts/powerbi_lloyds_data.py`
4. Click **OK**
5. Select the tables you want:
   - `syndicate_master`
   - `scr_impact_data`
   - `loss_ratio_data`
6. Click **Load**

### Using R in Power BI

1. Open Power BI Desktop
2. **Home** → **Get Data** → **More** → **R script**
3. Copy and paste `R_Scripts/powerbi_lloyds_data.R`
4. Click **OK**
5. Select the tables you want:
   - `syndicate_master`
   - `scr_impact_data`
   - `loss_ratio_data`
6. Click **Load**

## Generated Data Structure

### 1. Syndicate Master (Reference Data)
- 25 realistic Lloyd's syndicates (configurable)
- Syndicate numbers: 1176-6200 range
- Business classes: Property, Marine, Aviation, Cyber, etc.
- Stamp capacity: £50m - £2,000m

### 2. SCR Impact Data (100 records for 25 syndicates)
Four records per syndicate:
- **Latest LCR**: Most recent Lloyd's Capital Return submission
- **Latest SBF**: Most recent Solvency Business Forecast
- **Movement £**: Absolute change in SCR values
- **Movement %**: Percentage change in SCR values

### 3. Loss Ratio Data (100 records for 25 syndicates)
Four records per syndicate:
- **(A) 2024 LCR**: Historical baseline
- **(B) 2025 LCR**: Initial 2025 submission
- **(C) 2025 SBF**: Updated forecast with plan increases
- **(D) Movement**: Change from (A) to (C)

## Key Features

### Realistic Data Characteristics

- **Regulatory Compliance**: Modelled loss ratios ≥ Plan loss ratios (per Lloyd's guidance)
- **Business Class Variation**: Different loss ratio ranges by class
  - Catastrophe Re: 55-65%
  - Property: 65-72%
  - Professional Indemnity: 70-78%
  - Reinsurance: 72-80%
- **SCR Scaling**: uSCR typically 35-50% of stamp capacity
- **Temporal Realism**: Date-based submissions with realistic movements

### Customization Options

Both Python and R scripts support:
- **Number of syndicates**: Adjust `num_syndicates` parameter
- **Random seed**: Change for different data sets
- **CSV export**: Save tables to files
- **Date ranges**: Modify submission dates

### Example Customization

**Python:**
```python
data = generate_all_data(
    num_syndicates=50,    # Generate 50 syndicates
    seed=123,             # Different random data
    save_to_csv=True,
    output_dir='./my_data'
)
```

**R:**
```r
data <- generate_all_data(
  num_syndicates = 50,
  seed = 123,
  save_to_csv = TRUE,
  output_dir = "./my_data"
)
```

## Use Cases

### 1. Power BI Dashboard Development
- Create SCR tracking dashboards
- Build loss ratio analysis reports
- Develop syndicate performance visualizations

### 2. Testing and Development
- Test data pipelines without real data
- Validate calculation logic
- Demo reporting capabilities

### 3. Training and Education
- Train staff on Lloyd's reporting
- Demonstrate regulatory requirements
- Practice data analysis techniques

## Data Validation

The synthetic data includes:
- ✅ Valid Lloyd's syndicate numbering
- ✅ Realistic SCR values and movements
- ✅ Compliant loss ratio relationships
- ✅ Appropriate business class characteristics
- ✅ Temporal consistency in submissions
- ✅ Commentary explaining key changes

## Lloyd's Terminology

- **SCR**: Solvency Capital Requirement
- **uSCR**: Ultimate SCR (full run-off perspective)
- **1SCR**: One-year SCR (12-month view)
- **LCR**: Lloyd's Capital Return
- **SBF**: Solvency Business Forecast
- **YOA**: Year of Account
- **Net Net**: Net of reinsurance, net of acquisition costs
- **Self-uplift**: Difference between modelled and plan loss ratios

## Requirements

### Python
- Python 3.7+
- pandas
- numpy
- openpyxl

### R
- R 4.0+
- dplyr

### Power BI
- Power BI Desktop (latest version)
- Python or R integration enabled in Power BI settings

## Notes

- This is **synthetic data** for development and testing purposes only
- Data does not represent any real Lloyd's syndicates
- Adjust parameters to match your specific needs
- Review generated data before use in production environments

## Support

For questions or issues:
1. Check the README files in Python_Scripts/ or R_Scripts/
2. Review the source template: `Files_for_Claude/2025 SCR New SBF no LCR Template.xlsx`
3. Refer to Lloyd's official guidance documents

## License

This synthetic data generator is provided as-is for development and testing purposes.

---

**Generated Data Examples:**

| SyndicateNumber | SyndicateName | StampCapacity_GBPm | PrimaryBusinessClass |
|-----------------|---------------|--------------------|----------------------|
| 2001 | Global Property & Casualty | 875.3 | Property |
| 2003 | Marine & Energy | 1456.7 | Marine |
| 2988 | Catastrophe Re | 1823.4 | Catastrophe |

| SyndicateNumber | SubmissionType | uSCR_GBPm | 1SCR_GBPm | SCR_Ratio |
|-----------------|----------------|-----------|-----------|-----------|
| 2001 | Latest LCR | 368.45 | 326.71 | 0.8868 |
| 2001 | Latest SBF | 385.12 | 338.94 | 0.8801 |
| 2001 | Movement | 16.67 | 12.23 | 0.7336 |
| 2001 | Movement % | 4.52 | 3.74 | - |
