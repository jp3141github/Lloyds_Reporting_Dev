# Solvency II ASB Returns - R Implementation

This folder contains R scripts for generating Lloyd's of London Solvency II Pillar 3 ASB (Annual Solvency and Balance Sheet) returns with synthetic data for Power BI reporting.

## Overview

The ASB returns include:
- **ASB 245/246/247** (S.19.01.01): Non-Life Insurance Claims Information
- **ASB 248** (S.19.01.01): Non-Life Insurance Claims Information - Inflation Rates

## Files

### 1. `synthetic_data_generator.R`
Core module for generating synthetic Lloyd's insurance data.

**Features:**
- Generates realistic claims data with development patterns
- Supports multiple currencies (GBP, USD, EUR)
- Covers 12 Lines of Business (EIOPA classifications)
- Configurable underwriting year ranges
- Reproducible results with random seed

**Usage:**
```r
source("synthetic_data_generator.R")

# Generate all data
all_data <- generate_all_asb_data(
  syndicate_number = "1234",
  syndicate_name = "Example Marine & Energy Syndicate",
  start_year = 2015,
  end_year = 2024,
  claims_records = 500,
  inflation_records = 200
)

# Save to CSV
write_csv(all_data$ASB_245_246_247, "claims_data.csv")
write_csv(all_data$ASB_248, "inflation_data.csv")
```

**Individual Functions:**
```r
# Generate claims data only
claims_data <- generate_asb_245_246_247_data(
  num_records = 500,
  syndicate_number = "1234",
  start_year = 2015,
  end_year = 2024
)

# Generate inflation data only
inflation_data <- generate_asb_248_data(
  num_records = 200,
  syndicate_number = "1234",
  start_year = 2015,
  end_year = 2024
)
```

### 2. `powerbi_asb_returns.R`
Power BI integration script that can be used directly as an R data source in Power BI.

**Power BI Setup:**
1. Open Power BI Desktop
2. Go to **Get Data > More > Other > R script**
3. Copy and paste the contents of `powerbi_asb_returns.R`
4. Click **OK**
5. Select the tables you want to load:
   - `ASB_245_246_247_Claims` - Main claims data
   - `ASB_248_InflationRates` - Inflation rates
   - `Metadata` - Generation metadata
   - `LinesOfBusiness` - Reference table
   - `Claims_Summary` - Aggregated summary
   - `Development_Analysis` - Development year analysis

**Configuration:**
Edit the configuration section at the top of the script:
```r
SYNDICATE_NUMBER <- "1234"
SYNDICATE_NAME <- "Your Syndicate Name"
START_YEAR <- 2015
END_YEAR <- 2024
CLAIMS_RECORDS <- 500
INFLATION_RECORDS <- 200
```

### 3. `export_to_excel.R`
Exports synthetic data to Excel format matching Lloyd's specifications.

**Usage:**
```r
source("export_to_excel.R")

export_asb_returns_to_excel(
  output_filename = "ASB_Returns_Output.xlsx",
  syndicate_number = "1234",
  syndicate_name = "Example Syndicate",
  start_year = 2015,
  end_year = 2024
)
```

**Output Sheets:**
- Cover_Sheet
- ASB_245_246_247_Claims
- ASB_248_InflationRates
- Summary_by_LOB
- Summary_by_Year
- Development_Analysis
- LOB_Reference

## Data Specifications

### ASB 245/246/247 - Claims Data

| Column | Description | Type |
|--------|-------------|------|
| Currency | Reporting currency (GBP, USD, EUR) | Character |
| LineOfBusiness | EIOPA LoB code (LOB01-LOB12) | Character |
| UnderwritingYear | Year when policy was underwritten | Integer |
| DevelopmentYear | Years since underwriting (0-10) | Integer |
| GrossClaimPaid | Total claims paid before reinsurance | Numeric |
| ReinsuranceRecoveries | Recoveries from reinsurers | Numeric |
| GrossUndiscountedBEClaimsProvisions | Gross best estimate provisions | Numeric |
| DiscountingGrossBEClaimsProvisions | Discounting adjustment | Numeric |
| UndiscountedBEClaimsProvisionsReinsRecoverable | Reinsurance best estimate | Numeric |
| DiscountingBEClaimsProvisionsReinsRecoverable | Reins discounting | Numeric |
| GrossRBNS | Reported But Not Settled claims | Numeric |
| ReinsuranceRBNS | Reinsurance RBNS | Numeric |
| DiscountingRBNS | RBNS discounting | Numeric |
| DiscountingReinsuranceRBNS | Reins RBNS discounting | Numeric |

### ASB 248 - Inflation Rates

| Column | Description | Type |
|--------|-------------|------|
| Currency | Reporting currency | Character |
| LineOfBusiness | EIOPA LoB code | Character |
| UnderwritingYear | Underwriting year | Integer |
| HistoricInflationRateTotal | Total historic inflation % | Numeric |
| HistoricInflationRateExternal | External inflation % | Numeric |
| HistoricInflationRateEndogenous | Endogenous inflation % | Numeric |
| ExpectedInflationRateTotal | Expected total inflation % | Numeric |
| ExpectedInflationRateExternal | Expected external inflation % | Numeric |
| ExpectedInflationRateEndogenous | Expected endogenous inflation % | Numeric |

## Lines of Business (EIOPA Classifications)

- **LOB01**: Medical expense insurance
- **LOB02**: Income protection insurance
- **LOB03**: Workers compensation insurance
- **LOB04**: Motor vehicle liability insurance
- **LOB05**: Other motor insurance
- **LOB06**: Marine, aviation and transport insurance
- **LOB07**: Fire and other damage to property insurance
- **LOB08**: General liability insurance
- **LOB09**: Credit and suretyship insurance
- **LOB10**: Legal expenses insurance
- **LOB11**: Assistance
- **LOB12**: Miscellaneous financial loss

## Requirements

### R Packages

```r
install.packages(c("tidyverse", "writexl"))
```

### Power BI R Configuration

1. Install R on your system (https://cran.r-project.org/)
2. In Power BI Desktop:
   - Go to **File > Options and settings > Options**
   - Navigate to **R scripting**
   - Set your R installation directory
   - Install required packages in R

## Example Workflows

### Generate and Export Data in R

```r
# Load the data generator
source("synthetic_data_generator.R")

# Generate data
all_data <- generate_all_asb_data(
  syndicate_number = "5678",
  syndicate_name = "Marine Insurance Syndicate",
  start_year = 2018,
  end_year = 2024
)

# View summaries
print(head(all_data$ASB_245_246_247))
print(head(all_data$ASB_248))
print(all_data$Metadata)

# Save to CSV
write_csv(all_data$ASB_245_246_247, "my_claims_data.csv")
write_csv(all_data$ASB_248, "my_inflation_data.csv")
```

### Export to Excel

```r
source("export_to_excel.R")

# Export with custom parameters
export_asb_returns_to_excel(
  output_filename = "My_ASB_Returns.xlsx",
  syndicate_number = "5678",
  syndicate_name = "Marine Insurance Syndicate"
)
```

### Use in Power BI

1. Open `powerbi_asb_returns.R`
2. Adjust the configuration variables at the top
3. Copy the entire script
4. In Power BI: **Get Data > R script**
5. Paste and run
6. Select desired tables to import

## Data Characteristics

- **Monetary Values**: All amounts are in thousands
- **Data Type**: Synthetic data for demonstration/testing only
- **Reproducibility**: Fixed random seed ensures consistent results
- **Claims Development**: Models realistic claim settlement patterns over 10 years
- **Reinsurance**: Modeled as 10-40% of gross claims
- **Inflation Rates**: Vary by line of business and currency (1.5-4.5% range)
- **Best Estimate Provisions**: Include both gross and reinsurance perspectives
- **RBNS**: Reported But Not Settled claims with appropriate discounting

## Comparison with Python Version

Both Python and R implementations produce identical data structures and are fully compatible with Power BI. Choose based on your preference:

- **Python**: Better for users familiar with pandas/Python ecosystem
- **R**: Better for users familiar with tidyverse/R ecosystem

Both versions support:
- Direct Power BI integration
- CSV export
- Excel export
- Identical column names and data types
- Same configuration options

## Support

For questions or issues, refer to:
- Main repository documentation
- Original Excel specifications in `Files_for_Claude` folder
- Power BI R scripting documentation

## Notes

- Ensure R is properly configured in Power BI before using R scripts
- The `tidyverse` package is required for all scripts
- The `writexl` package is required for Excel export
- All scripts use `set.seed()` for reproducible random data generation
- Data follows EIOPA Solvency II reporting standards
