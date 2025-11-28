# Lloyd's SAO Addendum Return - Synthetic Data Generator (Python)

## Overview

This Python script generates synthetic Lloyd's of London data for the **SAO Addendum Return 2025**. The script creates realistic insurance data across three main reporting areas:

1. **Specific IBNR (Form 090)** - Specific Incurred But Not Reported reserves
2. **Movements and Actual vs Expected Analysis (Form 100)** - Loss development and ratio analysis
3. **SAO Class Mappings** - Mapping of reserving classes to Lloyd's Lines of Business

## Features

- Generates realistic synthetic Lloyd's insurance data
- Outputs data in multiple formats (CSV, Excel)
- Ready for import into Power BI
- Configurable number of records per dataset
- Reproducible results with random seed
- Comprehensive data validation

## Requirements

### Python Version
- Python 3.7 or higher

### Required Packages
```bash
pip install pandas numpy openpyxl
```

Or install from requirements file:
```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jp3141github/Lloyds_Reporting_Dev.git
cd Lloyds_Reporting_Dev/Python_Scripts/SAO_Addendum_Data_Generator
```

2. Install dependencies:
```bash
pip install pandas numpy openpyxl
```

## Usage

### Basic Usage

Run the script to generate all datasets:

```bash
python generate_lloyds_synthetic_data.py
```

This will create an `output` directory with:
- Three CSV files (one per dataset)
- One Excel file containing all datasets as separate sheets

### Using in Power BI

#### Method 1: Import CSV Files

1. Run the Python script to generate CSV files
2. In Power BI Desktop:
   - Click **Get Data** → **Text/CSV**
   - Navigate to the `output` folder
   - Select the CSV file you want to import
   - Repeat for each dataset

#### Method 2: Use Python Script in Power BI

Power BI can run Python scripts directly:

1. In Power BI Desktop, go to **Get Data** → **Python script**
2. Paste the following code:

```python
import sys
import os

# Add the script directory to path
script_dir = r'C:\path\to\Lloyds_Reporting_Dev\Python_Scripts\SAO_Addendum_Data_Generator'
sys.path.append(script_dir)

# Import and run
from generate_lloyds_synthetic_data import LloydsSyntheticDataGenerator

# Generate data
generator = LloydsSyntheticDataGenerator(syndicate_number="2060N")
data_dict = generator.generate_all_data()

# Make dataframes available to Power BI
Specific_IBNR = data_dict['Specific_IBNR']
Movements_and_AvE = data_dict['Movements_and_AvE']
SAO_Class_Mappings = data_dict['SAO_Class_Mappings']
```

3. Power BI will detect the three dataframes and allow you to load them

### Programmatic Usage

You can also use the script as a module in your own Python code:

```python
from generate_lloyds_synthetic_data import LloydsSyntheticDataGenerator

# Initialize generator
generator = LloydsSyntheticDataGenerator(syndicate_number="2060N")

# Generate all data
data_dict = generator.generate_all_data()

# Access individual dataframes
df_ibnr = data_dict['Specific_IBNR']
df_movements = data_dict['Movements_and_AvE']
df_mappings = data_dict['SAO_Class_Mappings']

# Or generate specific datasets
df_ibnr = generator.generate_specific_ibnr(num_records=100)
df_movements = generator.generate_movements_and_ave(num_classes=15)
df_mappings = generator.generate_sao_class_mappings(num_classes=20)

# Export to files
generator.export_to_csv(output_dir='my_output')
generator.export_to_excel(output_dir='my_output')
```

## Output Data Structure

### 1. Specific IBNR (Form 090)

| Column Name | Description | Example |
|------------|-------------|---------|
| Reserving_Class | Insurance class | "Property Cat XL" |
| Lloyds_CAT_Code | Catastrophe code | "22E" or "Non Nat-Cat" |
| Lloyds_Line_of_Business | Lloyd's LoB | "Property Cat XL" |
| Number_of_Losses | Count of losses | 5 |
| Underwriting_Year | Year | 2023 |
| Gross_IBNR_GBP000s | Gross IBNR in £000s | 15000 |
| Net_IBNR_GBP000s | Net IBNR in £000s | 9500 |
| Comment | Optional notes | "Based on market loss..." |

### 2. Movements and AvE Analysis (Form 100)

| Column Name | Description | Example |
|------------|-------------|---------|
| Class_Number | Class sequence | 1 |
| Class_Name | Class name | "Property Cat XL" |
| Lloyds_Line_of_Business | Lloyd's LoB | "Property Cat" |
| Underwriting_Year | Year | 2024 |
| Year_Label | Year description | "2024" |
| Reporting_Year | Is reporting year? | "Yes" |
| Ultimate_Premium_GBP000s | Premium in £000s | 50000 |
| ActualVsExpected_Pct_Ultimate_Premium | AvE % | -2.5 |
| Initial_Expected_Loss_Ratio_Pct | IELR % | 65.0 |
| Ultimate_Loss_Ratio_Pct_2024YE | ULR 2024YE % | 67.5 |
| Ultimate_Loss_Ratio_Pct_2025YE | ULR 2025YE % | 68.2 |
| Syndicate_Estimate_ULR_2025YE | Syndicate ULR % | 69.0 |

### 3. SAO Class Mappings

| Column Name | Description | Example |
|------------|-------------|---------|
| Reserving_Class_Name | Reserving class | "Property Cat XL" |
| Lloyds_LoB_1 | Primary LoB | "Property Cat" |
| LoB_1_Pct_Gross_Exposure | Primary exposure % | 75.5 |
| Lloyds_LoB_2 | Secondary LoB | "Property Cat XL" |
| LoB_2_Pct_Gross_Exposure | Secondary exposure % | 24.5 |
| Lloyds_LoB_3 | Tertiary LoB | NULL |
| LoB_3_Pct_Gross_Exposure | Tertiary exposure % | NULL |
| Lloyds_LoB_4 | Quaternary LoB | NULL |
| LoB_4_Pct_Gross_Exposure | Quaternary exposure % | NULL |

## Configuration

You can customize the data generation by modifying parameters:

```python
# Change syndicate number
generator = LloydsSyntheticDataGenerator(syndicate_number="1234N")

# Generate more/fewer records
df_ibnr = generator.generate_specific_ibnr(num_records=100)
df_movements = generator.generate_movements_and_ave(num_classes=15)
df_mappings = generator.generate_sao_class_mappings(num_classes=20)

# Change random seed for different data
np.random.seed(123)
random.seed(123)
```

## Data Characteristics

The synthetic data includes:

- **IBNR Records**: 50 records by default, with amounts > £1m (as per Lloyd's requirements)
- **Reserving Classes**: 10 classes by default, with 3 underwriting years each (2023, 2024, 2025)
- **Class Mappings**: 15 classes by default, each mapping to 1-4 Lloyd's Lines of Business
- **Realistic Ranges**:
  - Loss ratios: 55-75%
  - Premium: £5m - £100m per class
  - Actual vs Expected: -15% to +10%
  - Reinsurance recovery: 20-50%

## Troubleshooting

### Import Errors
If you get import errors, ensure all packages are installed:
```bash
pip install pandas numpy openpyxl --upgrade
```

### Permission Errors
If you get permission errors when creating the output directory, run with appropriate permissions or specify a different output directory:
```python
generator.export_to_csv(output_dir='/path/to/writable/directory')
```

### Power BI Python Issues
Ensure Power BI is configured to use the correct Python installation:
1. File → Options and settings → Options
2. Python scripting → Set Python home directory

## License

This script is provided as-is for generating synthetic test data for Lloyd's reporting purposes.

## Support

For issues or questions:
- Open an issue on GitHub: https://github.com/jp3141github/Lloyds_Reporting_Dev/issues
- Check Lloyd's documentation: https://www.lloyds.com/resources-and-services/reporting-rationalisation

## Version History

- **v1.0.0** (2025-11-21): Initial release
  - Specific IBNR generation
  - Movements and AvE analysis
  - SAO Class Mappings
  - CSV and Excel export
