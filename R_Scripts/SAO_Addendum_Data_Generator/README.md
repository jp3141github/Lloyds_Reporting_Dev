# Lloyd's SAO Addendum Return - Synthetic Data Generator (R)

## Overview

This R script generates synthetic Lloyd's of London data for the **SAO Addendum Return 2025**. The script creates realistic insurance data across three main reporting areas:

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

### R Version
- R 4.0.0 or higher

### Required Packages
```r
install.packages(c("dplyr", "tidyr", "openxlsx"))
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jp3141github/Lloyds_Reporting_Dev.git
cd Lloyds_Reporting_Dev/R_Scripts/SAO_Addendum_Data_Generator
```

2. Install dependencies in R:
```r
install.packages(c("dplyr", "tidyr", "openxlsx"))
```

## Usage

### Basic Usage

Run the script in R or RStudio:

```r
source("generate_lloyds_synthetic_data.R")
main()
```

This will create an `output` directory with:
- Three CSV files (one per dataset)
- One Excel file containing all datasets as separate sheets

### Using in Power BI

#### Method 1: Import CSV Files

1. Run the R script to generate CSV files
2. In Power BI Desktop:
   - Click **Get Data** → **Text/CSV**
   - Navigate to the `output` folder
   - Select the CSV file you want to import
   - Repeat for each dataset

#### Method 2: Use R Script in Power BI

Power BI can run R scripts directly:

1. In Power BI Desktop, go to **Get Data** → **R script**
2. Paste the following code:

```r
# Set working directory to script location
setwd("C:/path/to/Lloyds_Reporting_Dev/R_Scripts/SAO_Addendum_Data_Generator")

# Source the script
source("generate_lloyds_synthetic_data.R")

# Generate data
set.seed(42)
Specific_IBNR <- generate_specific_ibnr(num_records = 50)
Movements_and_AvE <- generate_movements_and_ave(num_classes = 10)
SAO_Class_Mappings <- generate_sao_class_mappings(num_classes = 15)
```

3. Power BI will detect the three dataframes and allow you to load them

### Interactive Usage

You can run individual functions interactively:

```r
# Source the script
source("generate_lloyds_synthetic_data.R")

# Generate specific datasets
df_ibnr <- generate_specific_ibnr(num_records = 100)
df_movements <- generate_movements_and_ave(num_classes = 15)
df_mappings <- generate_sao_class_mappings(num_classes = 20)

# View data
head(df_ibnr)
head(df_movements)
head(df_mappings)

# Export to CSV
export_to_csv(output_dir = "my_output")

# Export to Excel
export_to_excel(output_dir = "my_output")
```

### Command Line Usage

You can also run the script from command line:

```bash
Rscript generate_lloyds_synthetic_data.R
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
| Lloyds_LoB_3 | Tertiary LoB | NA |
| LoB_3_Pct_Gross_Exposure | Tertiary exposure % | NA |
| Lloyds_LoB_4 | Quaternary LoB | NA |
| LoB_4_Pct_Gross_Exposure | Quaternary exposure % | NA |

## Configuration

You can customize the data generation by modifying the script parameters:

```r
# Change syndicate number (at top of script)
SYNDICATE_NUMBER <- "1234N"

# Generate more/fewer records
df_ibnr <- generate_specific_ibnr(num_records = 100)
df_movements <- generate_movements_and_ave(num_classes = 15)
df_mappings <- generate_sao_class_mappings(num_classes = 20)

# Change random seed for different data
set.seed(123)
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

## Function Reference

### generate_specific_ibnr(num_records)
Generates Specific IBNR data (Form 090).

**Parameters:**
- `num_records` (integer): Number of IBNR records to generate (default: 50)

**Returns:** Data frame with IBNR data

### generate_movements_and_ave(num_classes)
Generates Movements and AvE analysis data (Form 100).

**Parameters:**
- `num_classes` (integer): Number of reserving classes (default: 10)

**Returns:** Data frame with movements and AvE data

### generate_sao_class_mappings(num_classes)
Generates SAO Class Mappings data.

**Parameters:**
- `num_classes` (integer): Number of reserving classes to map (default: 15)

**Returns:** Data frame with class mappings

### export_to_csv(output_dir)
Generates all datasets and exports to CSV files.

**Parameters:**
- `output_dir` (string): Output directory path (default: "output")

**Returns:** List containing all three data frames

### export_to_excel(output_dir)
Generates all datasets and exports to a single Excel file.

**Parameters:**
- `output_dir` (string): Output directory path (default: "output")

**Returns:** List containing all three data frames

## Troubleshooting

### Package Installation Issues
If you have trouble installing packages, try:
```r
install.packages(c("dplyr", "tidyr", "openxlsx"), dependencies = TRUE)
```

### Permission Errors
If you get permission errors when creating the output directory, specify a different location:
```r
export_to_csv(output_dir = "C:/path/to/writable/directory")
```

### Power BI R Issues
Ensure Power BI is configured to use the correct R installation:
1. File → Options and settings → Options
2. R scripting → Set R home directory
3. Ensure the required packages are installed in that R installation

### Memory Issues
For very large datasets, consider generating in batches:
```r
# Generate smaller batches
df1 <- generate_specific_ibnr(num_records = 25)
df2 <- generate_specific_ibnr(num_records = 25)
df_combined <- rbind(df1, df2)
```

## Best Practices

### For Power BI Integration

1. **Save CSV files**: Always save to CSV first, then import to Power BI
2. **Data types**: Power BI will auto-detect data types; verify they're correct
3. **Refresh**: Set up scheduled refresh if regenerating data regularly
4. **Relationships**: Create relationships between tables in Power BI model

### For Reproducibility

1. **Fixed seed**: Use `set.seed()` for reproducible results
2. **Document changes**: Comment any modifications to default parameters
3. **Version control**: Track script versions in Git

## Performance

Typical generation times (on standard laptop):
- 50 IBNR records: < 1 second
- 10 classes (30 records) movements: < 1 second
- 15 class mappings: < 1 second
- Total with export: < 5 seconds

For larger datasets (100+ records), generation time scales linearly.

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

## Additional Resources

- [Lloyd's Reporting Rationalisation](https://www.lloyds.com/resources-and-services/reporting-rationalisation)
- [Power BI R Integration](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-r-scripts)
- [dplyr Documentation](https://dplyr.tidyverse.org/)
- [openxlsx Documentation](https://ycphs.github.io/openxlsx/)
