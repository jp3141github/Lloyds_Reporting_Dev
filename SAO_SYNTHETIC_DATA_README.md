# Lloyd's SAO Addendum Return - Synthetic Data Generators

## Overview

This repository contains **Python** and **R** scripts to generate synthetic Lloyd's of London data for the **SAO (Signing Actuary Opinion) Addendum Return 2025**. These scripts create realistic insurance data that can be imported into Power BI for reporting and analysis purposes.

## What Data is Generated?

The scripts generate synthetic data for three key reporting areas required by Lloyd's:

### 1. **Form 090: Specific IBNR**
Specific Incurred But Not Reported (IBNR) reserves for:
- Natural catastrophe events (with Lloyd's CAT codes)
- Non-natural catastrophe events
- Split by reserving class and underwriting year
- Gross and net IBNR amounts (in £000s)

### 2. **Form 100: Movements and Actual vs Expected Analysis**
Loss development and ratio analysis including:
- Top 10 reserving classes by net reserves
- Ultimate premium and loss ratios
- Actual vs Expected (AvE) analysis
- Initial Expected Loss Ratio (IELR) and Ultimate Loss Ratio (ULR)
- Year-over-year comparisons (2024YE vs 2025YE)

### 3. **SAO Class Mappings**
Mapping of Signing Actuary reserving classes to Lloyd's Lines of Business:
- Up to 4 Lloyd's LoB per reserving class
- Percentage of gross exposure for each LoB
- Totals to 100% per reserving class

## Repository Structure

```
Lloyds_Reporting_Dev/
├── Python_Scripts/
│   └── SAO_Addendum_Data_Generator/
│       ├── generate_lloyds_synthetic_data.py  # Python script
│       ├── requirements.txt                    # Python dependencies
│       ├── README.md                          # Python documentation
│       └── output/                            # Generated data files
│
├── R_Scripts/
│   └── SAO_Addendum_Data_Generator/
│       ├── generate_lloyds_synthetic_data.R   # R script
│       ├── README.md                          # R documentation
│       └── output/                            # Generated data files
│
├── Files_for_Claude/
│   └── SAO Addendum Return 2025.xlsx          # Template Excel file
│
└── SAO_SYNTHETIC_DATA_README.md              # This file
```

## Quick Start

### Option 1: Python (Recommended for Power BI)

1. **Install Python 3.7+** and required packages:
   ```bash
   cd Python_Scripts/SAO_Addendum_Data_Generator
   pip install -r requirements.txt
   ```

2. **Generate data**:
   ```bash
   python generate_lloyds_synthetic_data.py
   ```

3. **Import to Power BI**:
   - Data is saved in the `output` folder
   - Use **Get Data → Text/CSV** to import CSV files
   - Or use **Get Data → Python script** to run directly in Power BI

### Option 2: R

1. **Install R 4.0+** and required packages:
   ```r
   install.packages(c("dplyr", "tidyr", "openxlsx"))
   ```

2. **Generate data**:
   ```r
   cd R_Scripts/SAO_Addendum_Data_Generator
   Rscript generate_lloyds_synthetic_data.R
   ```

3. **Import to Power BI**:
   - Data is saved in the `output` folder
   - Use **Get Data → Text/CSV** to import CSV files
   - Or use **Get Data → R script** to run directly in Power BI

## Output Files

Both scripts generate the same output in the `output` folder:

### CSV Files (for Power BI import):
- `Specific_IBNR_2060N_[timestamp].csv`
- `Movements_and_AvE_2060N_[timestamp].csv`
- `SAO_Class_Mappings_2060N_[timestamp].csv`

### Excel File (for easy viewing):
- `SAO_Addendum_Synthetic_Data_2060N_[timestamp].xlsx`
  - Contains all three datasets as separate sheets

## Using in Power BI

### Method 1: Import CSV Files (Simplest)

1. Run the Python or R script to generate CSV files
2. Open Power BI Desktop
3. Click **Get Data** → **Text/CSV**
4. Navigate to the `output` folder
5. Select and import each CSV file
6. Create relationships between tables as needed

### Method 2: Python Script in Power BI

1. In Power BI Desktop: **Get Data** → **Python script**
2. Paste this code (update the path):

```python
import sys
sys.path.append(r'C:\path\to\Lloyds_Reporting_Dev\Python_Scripts\SAO_Addendum_Data_Generator')

from generate_lloyds_synthetic_data import LloydsSyntheticDataGenerator

generator = LloydsSyntheticDataGenerator(syndicate_number="2060N")
data_dict = generator.generate_all_data()

Specific_IBNR = data_dict['Specific_IBNR']
Movements_and_AvE = data_dict['Movements_and_AvE']
SAO_Class_Mappings = data_dict['SAO_Class_Mappings']
```

3. Power BI will detect the three dataframes
4. Select all three and click **Load**

### Method 3: R Script in Power BI

1. In Power BI Desktop: **Get Data** → **R script**
2. Paste this code (update the path):

```r
setwd("C:/path/to/Lloyds_Reporting_Dev/R_Scripts/SAO_Addendum_Data_Generator")
source("generate_lloyds_synthetic_data.R")

set.seed(42)
Specific_IBNR <- generate_specific_ibnr(num_records = 50)
Movements_and_AvE <- generate_movements_and_ave(num_classes = 10)
SAO_Class_Mappings <- generate_sao_class_mappings(num_classes = 15)
```

3. Power BI will detect the three dataframes
4. Select all three and click **Load**

## Data Characteristics

The synthetic data includes realistic values based on Lloyd's market standards:

| Characteristic | Range/Values |
|---------------|--------------|
| **IBNR Amounts** | £1m - £50m (gross) |
| **Reinsurance Recovery** | 20% - 50% |
| **Loss Ratios** | 55% - 75% |
| **Ultimate Premium** | £5m - £100m per class |
| **Actual vs Expected** | -15% to +10% |
| **Underwriting Years** | 2020-2025 |
| **Number of Losses** | 1-20 per event |
| **Lloyd's CAT Codes** | 22E, 23A, 23B, 24C, 21D, Non Nat-Cat |

## Customization

Both scripts can be customized to generate different amounts of data:

### Python:
```python
generator = LloydsSyntheticDataGenerator(syndicate_number="1234N")
df_ibnr = generator.generate_specific_ibnr(num_records=100)
df_movements = generator.generate_movements_and_ave(num_classes=15)
df_mappings = generator.generate_sao_class_mappings(num_classes=20)
```

### R:
```r
SYNDICATE_NUMBER <- "1234N"  # Modify at top of script
df_ibnr <- generate_specific_ibnr(num_records = 100)
df_movements <- generate_movements_and_ave(num_classes = 15)
df_mappings <- generate_sao_class_mappings(num_classes = 20)
```

## Lloyd's Lines of Business

The scripts include the following Lloyd's Lines of Business (LoB):

- Fire
- Property Direct
- Property Cat
- Property Cat XL
- Property Treaty
- Motor Direct
- Motor XL
- Marine Cargo
- Marine Hull
- Energy Offshore
- Energy Onshore
- Aviation Hull
- Aviation Liability
- D&O (Directors & Officers)
- Professional Indemnity
- Casualty Treaty
- General Liability
- Medical Malpractice
- Product Liability
- Cyber
- Credit & Bond
- Political Risk
- Terrorism
- Accident & Health

## Sample Reserving Classes

The scripts include these example reserving classes:

- Property Cat XL
- Marine Hull
- D&O US
- Aviation Liability
- Professional Indemnity
- Casualty Treaty
- Energy Offshore
- Property Direct
- Motor XL
- Cyber Liability
- Political Risk

## Validation

The generated data adheres to Lloyd's requirements:

- ✅ Specific IBNR entries have gross amounts > £1m
- ✅ Class mappings total to 100% gross exposure
- ✅ Data split by underwriting year (no "2020 & Prior" groupings)
- ✅ Natural catastrophe events include Lloyd's CAT codes
- ✅ Non-natural catastrophes marked as "Non Nat-Cat"
- ✅ All monetary amounts in £000s
- ✅ Movements analysis covers top 10 classes by net reserves

## Power BI Report Suggestions

Once you've imported the data into Power BI, consider creating these visualizations:

### For Specific IBNR:
- **Waterfall chart**: IBNR by underwriting year
- **Stacked bar chart**: Gross vs Net IBNR by reserving class
- **Map**: Geographic distribution (if you add location data)
- **Table**: Detailed IBNR listing with drill-through

### For Movements and AvE:
- **Line chart**: Ultimate Loss Ratio trends by underwriting year
- **Bar chart**: Actual vs Expected by class
- **Scatter plot**: IELR vs ULR analysis
- **KPI cards**: Total premium, average loss ratio, AvE summary

### For Class Mappings:
- **Treemap**: Reserving class exposure distribution
- **Sankey diagram**: Flow from reserving classes to Lloyd's LoB
- **Matrix**: Cross-tab of classes and LoB
- **Pie chart**: LoB exposure breakdown

## Documentation

For detailed usage instructions, see:
- **Python**: `Python_Scripts/SAO_Addendum_Data_Generator/README.md`
- **R**: `R_Scripts/SAO_Addendum_Data_Generator/README.md`

## Support and Resources

### Lloyd's Resources:
- [Lloyd's Reporting Rationalisation](https://www.lloyds.com/resources-and-services/reporting-rationalisation)
- [Lloyd's CAT Codes](https://www.lloyds.com/resources-and-services/claims-for-market-participants/catastrophe-portal/catastrophe-codes/)
- [TPD Reserving Tools](https://www.lloyds.com/market-resources/reporting-rationalisation/tpd-reserving)

### Power BI Resources:
- [Power BI Python Integration](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-python-scripts)
- [Power BI R Integration](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-r-scripts)

### Repository:
- [GitHub Issues](https://github.com/jp3141github/Lloyds_Reporting_Dev/issues)

## Troubleshooting

### Python Issues:
```bash
# If pandas/numpy errors
pip install --upgrade pandas numpy openpyxl

# If Power BI can't find Python
# File → Options → Python scripting → Set Python home directory
```

### R Issues:
```r
# If package errors
install.packages(c("dplyr", "tidyr", "openxlsx"), dependencies = TRUE)

# If Power BI can't find R
# File → Options → R scripting → Set R home directory
```

### Common Issues:
1. **Permission denied**: Run script with appropriate permissions or change output directory
2. **Module not found**: Ensure all dependencies are installed
3. **Encoding errors**: CSV files use UTF-8 encoding; ensure Power BI uses same
4. **Date formatting**: Power BI may auto-detect dates; verify column types

## License

This project is provided as-is for generating synthetic test data for Lloyd's of London reporting purposes.

## Version History

- **v1.0.0** (2025-11-21): Initial release
  - Python and R implementations
  - Three main datasets (IBNR, Movements/AvE, Class Mappings)
  - CSV and Excel export
  - Power BI integration support

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Disclaimer

This synthetic data is for **testing and demonstration purposes only**. It does not represent actual Lloyd's syndicate data and should not be used for regulatory reporting or business decision-making.

---

**Questions?** Open an issue on [GitHub](https://github.com/jp3141github/Lloyds_Reporting_Dev/issues)
