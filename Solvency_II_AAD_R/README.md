# Solvency II AAD Returns - R Implementation for Power BI

This directory contains R scripts for generating and transforming Solvency II Pillar 3 Annual Assets Data (AAD) returns for Lloyd's of London, designed for use with Power BI.

## Overview

The AAD return consists of several templates that insurance companies must submit to regulators:

- **AAD230 (S.06.02.01)**: List of assets
- **AAD233 (S.08.01.01)**: Open derivatives
- **AAD235 (S.09.01.01)**: Income/gains and losses in the period
- **AAD236 (S.06.03.01)**: Collective Investment Undertakings - Look-through
- **AAD237 (S.10.01.01)**: Loans and mortgages
- **AAD238 (S.11.01.01)**: Property holdings

## Files

### Data Generation
- `synthetic_data_generator.R` - Generates synthetic Lloyd's of London style data for testing

### Power BI Transformers
- `powerbi_aad230_transformer.R` - Complete transformer for AAD230 with validations
- `powerbi_all_aad_transformers.R` - Combined transformer for all AAD tables

## Installation

### Prerequisites
- R 4.0 or higher
- Required R packages: dplyr, tidyr, lubridate

### Install Required Packages

```R
install.packages(c("dplyr", "tidyr", "lubridate"))
```

## Usage

### Step 1: Generate Synthetic Data

First, generate synthetic Lloyd's data for testing:

```R
# In R or RStudio
source("synthetic_data_generator.R")

# Generate all datasets
datasets <- main()

# This creates a 'synthetic_data/' directory with CSV files
```

This will create:
- AAD230_Assets.csv (1,000 asset records)
- AAD233_Derivatives.csv (100 derivative records)
- AAD235_Income.csv (12 income category records)
- AAD236_CIU_Lookthrough.csv (50 fund records)
- AAD237_Loans_Mortgages.csv (200 loan records)
- AAD238_Property.csv (100 property records)

### Step 2: Use in Power BI

#### Option A: Direct R Script in Power BI

1. Open Power BI Desktop
2. Go to **Get Data** > **More** > **Other** > **R script**
3. Paste the contents of `synthetic_data_generator.R`
4. Click OK to execute
5. Select which tables to import

#### Option B: Transform Existing Data with AAD230 Transformer

1. Load your source data into Power BI (CSV, Excel, database, etc.)
2. Select the query in Power Query Editor
3. Go to **Transform** > **Run R Script**
4. Copy the contents of `powerbi_aad230_transformer.R`
5. Paste into the script editor
6. Click OK

#### Option C: Use the Combined Transformer

1. Load your source data into Power BI
2. Select the query in Power Query Editor
3. Go to **Transform** > **Run R Script**
4. Paste this code:

```R
# Specify which table to transform
table_type <- "AAD230"  # Change to AAD233, AAD235, etc.

# Then paste the contents of powerbi_all_aad_transformers.R
source("powerbi_all_aad_transformers.R")
```

5. The transformer will:
   - Map your columns to the correct EIOPA reference codes
   - Apply data validations
   - Format dates and numeric fields
   - Calculate derived fields
   - Provide validation warnings and errors

#### Option D: Import Pre-Generated Data

1. Run the synthetic data generator locally
2. In Power BI, go to **Get Data** > **Text/CSV**
3. Navigate to the `synthetic_data/` folder
4. Import the relevant CSV file(s)
5. (Optional) Apply transformers for additional validation

## Data Structure

### AAD230 - List of Assets

Key fields:
- Portfolio (L/NL/RF)
- Asset ID Code (ISIN, SEDOL, CUSIP, or internal)
- Issuer information (name, code, sector, country)
- Financial data (quantity, price, total Solvency II amount)
- Maturity date, duration, credit quality

### AAD233 - Open Derivatives

Key fields:
- Derivative ID Code
- Counterparty information
- Contract details (type, notional amount, currency)
- Premium paid/received
- Maturity date, valuation method

### AAD235 - Income/Gains and Losses

Aggregated by asset category:
- Dividends
- Interest income
- Rent
- Net gains/losses
- Unrealised gains/losses

### AAD236 - CIU Look-through

Key fields:
- Investment fund codes
- CIU identification
- Underlying asset categories
- Total Solvency II amounts
- Level of look-through

### AAD237 - Loans and Mortgages

Key fields:
- Loan identification and type
- Borrower information
- Original and outstanding amounts
- Interest rate, maturity date
- Collateral value, LTV ratio (calculated)

### AAD238 - Property

Key fields:
- Property identification and type
- Location (country)
- Purchase price and current valuation
- Rental income and occupancy rate
- Rental yield and capital appreciation (calculated)

## Validation Rules

The AAD230 transformer includes comprehensive validations:

- **Required fields**: Asset ID, Portfolio, Total Solvency II Amount
- **Data types**: Numeric fields, dates, categorical codes
- **Value ranges**: Valid portfolio codes, CIC codes, rating codes
- **Business rules**:
  - No duplicate Asset IDs
  - Fund Number required for RF portfolio
  - Valid ISIN/SEDOL/CUSIP formats
  - Positive amounts where applicable

Validation errors and warnings are printed to the R script output in Power BI.

## Customization

### Modifying Field Mappings

Each transformer function has a mapping section. Update these to match your source data:

```R
output_df <- dataset %>%
  mutate(
    C0060_Portfolio = Portfolio,  # Change 'Portfolio' to your column name
    C0040_Asset_ID_Code = Asset_ID_Code,
    # ... add or modify mappings
  )
```

### Adding Custom Validations

Add validation logic to check specific business rules:

```R
# Check for custom condition
custom_check <- dataset %>%
  filter(your_condition) %>%
  nrow()

if (custom_check > 0) {
  cat(sprintf("Warning: Custom validation failed for %d records\n", custom_check))
}
```

### Adjusting Synthetic Data Volume

Modify the number of records generated:

```R
datasets <- generate_all_datasets(num_assets = 5000)  # Increase from default 1000
```

## Power BI Integration Tips

1. **R Environment**: Ensure Power BI is configured to use the correct R installation
   - Go to **File** > **Options and settings** > **Options** > **R scripting**
   - Set the R home directory
   - Ensure required packages are installed in that R environment

2. **Performance**: For large datasets (>100K rows), consider:
   - Pre-processing data outside Power BI
   - Using data.table package for faster operations
   - Optimizing R scripts with vectorization
   - Using incremental refresh in Power BI

3. **Refresh**: R scripts in Power BI re-execute on each data refresh

4. **Debugging**:
   - Use `cat()` or `print()` statements to output diagnostics
   - Check the R script output window in Power BI for messages
   - Test scripts in RStudio first before using in Power BI

5. **Security**: When using real data, ensure compliance with data protection regulations

## Package Dependencies

The scripts use the following R packages:
- **dplyr**: Data manipulation and transformation
- **tidyr**: Data tidying and reshaping
- **lubridate**: Date and time handling

All packages are available from CRAN:

```R
install.packages(c("dplyr", "tidyr", "lubridate"))
```

## Example Workflow

Here's a complete example workflow:

### 1. Generate Test Data

```R
# In R or RStudio
source("synthetic_data_generator.R")
datasets <- main()
```

### 2. Load in Power BI

```R
# In Power BI R Script data source
source("synthetic_data_generator.R")
datasets <- generate_all_datasets(num_assets = 1000)

# Return the AAD230 dataset
AAD230_Assets <- datasets$AAD230_Assets
```

### 3. Transform the Data

```R
# In Power BI R Transform script
# The 'dataset' variable contains your loaded data

source("powerbi_aad230_transformer.R")

# The 'result' variable is automatically returned
```

### 4. Create Visualizations

Now you can create Power BI visualizations using the transformed data:
- Total Solvency II Amount by Portfolio
- Asset allocation by CIC code
- Top issuers by exposure
- Currency breakdown
- Maturity profile over time

## Troubleshooting

### Common Issues

1. **"Package not found" error**
   - Install the missing package in your R environment
   - Use: `install.packages("package_name")`

2. **"Object not found" error**
   - Check that your source data columns match the expected names
   - Modify the transformer mappings if needed

3. **Date format issues**
   - Ensure dates are in YYYY-MM-DD or standard R date format
   - Use lubridate functions to parse different date formats

4. **Performance issues**
   - Reduce the size of test datasets
   - Use data.table for faster operations
   - Pre-aggregate data before importing to Power BI

## Reference Documents

Based on:
- Solvency II Pillar 3 - AAD Return Specifications Annual 2024
- EIOPA reporting guidelines
- Lloyd's of London reporting requirements

## Support

For issues or questions:
1. Check the R script output in Power BI for error messages
2. Review the EIOPA reference codes in the specifications
3. Verify your source data structure matches expected format
4. Test scripts in RStudio before using in Power BI

## License

This implementation is for internal use with Lloyd's of London regulatory reporting.
