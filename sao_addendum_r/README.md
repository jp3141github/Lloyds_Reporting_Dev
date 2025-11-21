# SAO Addendum Return 2025 - R Data Generators

This folder contains R scripts to generate synthetic Lloyd's of London data for the **SAO Addendum Return 2025**. These scripts are designed to be used directly in **Power BI** as R data sources.

## Overview

The SAO (Signing Actuary's Opinion) Addendum Return is a mandatory submission for Lloyd's syndicates at year-end. This collection of scripts generates realistic synthetic data for the three main tables required:

1. **090 Specific IBNR** - Specific Incurred But Not Reported reserves
2. **100 Movements and AvE Analysis** - Movements and Actual vs Expected Analysis
3. **SAO Class Mappings** - Mapping of Signing Actuary reserving classes to Lloyd's Lines of Business

## Files

```
sao_addendum_r/
├── README.md                            # This file
├── generate_090_specific_ibnr.R         # 090 Specific IBNR data generator
├── generate_100_movements_ave.R         # 100 Movements and AvE analysis generator
└── generate_sao_class_mappings.R        # SAO Class Mappings generator
```

## Requirements

### R Installation

- **R version**: >= 4.0.0
- **No additional packages required** - all scripts use base R only

### Power BI R Integration

Ensure R is configured in Power BI:

1. Go to **File** > **Options and settings** > **Options**
2. Navigate to **R scripting**
3. Verify the R installation directory is set correctly

## Usage

### Option 1: Use in Power BI (Recommended)

#### Step 1: Open Power BI Desktop

#### Step 2: Get Data from R Script

1. Click **Get Data** > **More**
2. Search for and select **R script**
3. Click **Connect**

#### Step 3: Paste the Script

Copy the contents of one of the generator scripts and paste into the script editor:

- For **090 Specific IBNR**: Copy `generate_090_specific_ibnr.R`
- For **100 Movements and AvE**: Copy `generate_100_movements_ave.R`
- For **SAO Class Mappings**: Copy `generate_sao_class_mappings.R`

#### Step 4: Select the Data Table

Power BI will detect the available data frames:

- `specific_ibnr` - from the 090 Specific IBNR script
- `movements_ave` and `movements_ave_summary` - from the 100 Movements and AvE script
- `class_mappings` - from the SAO Class Mappings script

Select the table(s) you want to import and click **Load**.

### Option 2: Run in RStudio or R Console

You can also run the scripts directly from RStudio or the R console:

```r
# Generate 090 Specific IBNR data
source("generate_090_specific_ibnr.R")

# Generate 100 Movements and AvE analysis data
source("generate_100_movements_ave.R")

# Generate SAO Class Mappings data
source("generate_sao_class_mappings.R")
```

Each script will display summary statistics and sample data to the console.

## Script Details

### 1. generate_090_specific_ibnr.R

**Output Table**: `specific_ibnr`

**Columns**:
- `Reserving Class` - Reserving class name
- `Lloyd's Cat Code` - CAT code for natural catastrophes or "Non Nat-Cat"
- `Lloyd's Line of Business` - Lloyd's LoB classification
- `Number of losses` - Number of losses associated with the IBNR
- `Underwriting Year` - Year of account (2010-2025)
- `Gross IBNR (£000s)` - Gross IBNR amount in thousands of GBP
- `Net IBNR (£000s)` - Net IBNR amount (post-reinsurance)
- `Comment (optional)` - Optional commentary on the reserve

**Default Records**: 50

**Key Features**:
- Generates specific IBNR entries for both CAT and Non-CAT events
- Realistic lognormal distribution for IBNR amounts
- Net IBNR is 70-95% of gross (accounting for reinsurance)
- More recent underwriting years have higher probability
- Includes realistic actuarial comments

**Example Output**:
```
================================================================================
SAO Addendum Return - 090 Specific IBNR Summary
================================================================================
Total Records: 50
Total Gross IBNR: £XXX,XXX k
Total Net IBNR: £XXX,XXX k
Underwriting Years: 2010 - 2025
Number of CAT Events: XX
Number of Non Nat-Cat Events: XX
```

### 2. generate_100_movements_ave.R

**Output Tables**: `movements_ave`, `movements_ave_summary`

**Columns** (movements_ave):
- `Class ID` - Unique class identifier (01-10)
- `Reserving Class` - Reserving class name
- `Lloyd's Line of Business` - Lloyd's LoB classification
- `Underwriting Year` - Year label (2023 & Prior, 2024, 2025)
- `Reporting Year?` - Indicator if current reporting year (1 or 0)
- `Ultimate Premium (£000s)` - Ultimate premium estimate
- `Actual vs Expected as % of ultimate premium` - AvE analysis
- `Initial Expected Loss Ratio (IELR) (%)` - Initial expected LR
- `Ultimate Loss Ratio (ULR) (%)` - Ultimate LR estimate
- `Reserves 2024YE (£000s)` - Reserves at 2024 year-end
- `Reserves 2025YE (£000s)` - Reserves at 2025 year-end
- `Syndicate Estimate - 2025YE (£000s)` - Syndicate's reserve estimate

**Default Classes**: 10 (top 10 by reserves)

**Key Features**:
- Covers 3 underwriting years per class (30 records total)
- Realistic loss ratios (50-75% IELR)
- Actual vs Expected varies by year maturity
- Includes both Signing Actuary and Syndicate estimates
- Summary table aggregates by underwriting year

**Example Output**:
```
================================================================================
SAO Addendum Return - 100 Movements and AvE Analysis Summary
================================================================================
Total Classes: 10
Total Records: 30
Total Ultimate Premium: £XXX,XXX k
Total Reserves (2025YE): £XXX,XXX k
```

### 3. generate_sao_class_mappings.R

**Output Table**: `class_mappings`

**Columns**:
- `Signing Actuary Reserving Class Name` - Internal reserving class
- `Lloyd's LoB 1` - Primary Lloyd's Line of Business
- `LoB 1: % of Gross Exposure` - Exposure percentage for LoB 1
- `Lloyd's LoB 2` - Secondary Lloyd's LoB (if applicable)
- `LoB 2: % of Gross Exposure` - Exposure percentage for LoB 2
- `Lloyd's LoB 3` - Tertiary Lloyd's LoB (if applicable)
- `LoB 3: % of Gross Exposure` - Exposure percentage for LoB 3
- `Lloyd's LoB 4` - Quaternary Lloyd's LoB (if applicable)
- `LoB 4: % of Gross Exposure` - Exposure percentage for LoB 4

**Default Classes**: 20

**Key Features**:
- Each reserving class maps to 1-4 Lloyd's LoB
- Exposure percentages always sum to exactly 100%
- Primary LoB typically receives 60-100% of exposure
- Intelligent mapping based on class similarity
- Covers major insurance lines (Property, Casualty, Marine, Aviation, etc.)
- Automatic validation of exposure percentages

**Example Output**:
```
================================================================================
SAO Addendum Return - SAO Class Mappings Summary
================================================================================
Total Reserving Classes: 20
Classes mapping to 1 LoB: X
Classes mapping to 2 LoB: X
Classes mapping to 3 LoB: X
Classes mapping to 4 LoB: X
```

## Customization

Each script includes parameters you can modify:

### 090 Specific IBNR
```r
specific_ibnr <- generate_specific_ibnr_data(num_records = 50)  # Change number of records
```

### 100 Movements and AvE
```r
movements_ave <- generate_movements_ave_data(num_classes = 10)  # Change number of classes
```

### SAO Class Mappings
```r
class_mappings <- generate_class_mappings_data(num_classes = 20)  # Change number of classes
```

## Data Quality

All scripts include:
- ✅ Fixed random seeds for reproducibility (`set.seed()`)
- ✅ Realistic statistical distributions
- ✅ Data validation and consistency checks
- ✅ Summary statistics output
- ✅ Proper handling of missing/optional fields
- ✅ No external package dependencies (base R only)

## Power BI Integration Tips

### Refresh Data

To refresh the synthetic data in Power BI:
1. Right-click the table in the **Fields** pane
2. Select **Refresh data**

### Create Relationships

You can create relationships between tables:
- Link `movements_ave` to `specific_ibnr` via **Reserving Class**
- Link `movements_ave` to `class_mappings` via **Signing Actuary Reserving Class Name**

### Performance Optimization

R scripts in Power BI are executed each time the data is refreshed. For better performance:
- Keep the number of records reasonable (default values are optimized)
- Use the default parameters unless you need more data
- Consider caching data if frequent refreshes are needed

### Modify Random Seed

To generate different data on each refresh, change the random seed:

```r
# From this:
set.seed(42)

# To this (uses current time):
set.seed(as.numeric(Sys.time()))
```

## Troubleshooting

### R Script Not Executing in Power BI

**Issue**: Power BI shows an error when trying to run R scripts.

**Solutions**:
1. Verify R is installed correctly
2. Check R path in Power BI options (File > Options > R scripting)
3. Ensure you have sufficient permissions to execute R scripts
4. Try running the script in RStudio first to verify it works

### Data Not Appearing

**Issue**: Script runs but no data tables appear in Power BI.

**Solutions**:
1. Ensure the script creates a data frame (not a list or other object)
2. Verify the variable names match what Power BI expects
3. Check that `stringsAsFactors = FALSE` is set in data.frame() calls

### Column Names with Special Characters

**Issue**: Column names with spaces or special characters cause issues.

**Solutions**:
- The scripts use `check.names = FALSE` to preserve column names
- Power BI should handle these correctly when importing R data frames
- If issues persist, you can modify column names to remove special characters

## Comparison: R vs Python Scripts

Both implementations generate identical data structures:

| Feature | R Scripts | Python Scripts |
|---------|-----------|----------------|
| **Dependencies** | None (base R only) | pandas, numpy |
| **Performance** | Fast | Fast |
| **Readability** | Functional style | Object-oriented |
| **Power BI Integration** | Native support | Native support |
| **Reproducibility** | `set.seed()` | `np.random.seed()` |

**Recommendation**: Choose based on your team's expertise and existing Power BI setup.

## Reference

Based on the **SAO Addendum Return 2025** template from Lloyd's of London.

For more information on Lloyd's reporting requirements:
- [Lloyd's Reporting Requirements](https://www.lloyds.com/resources-and-services/reporting-rationalisation)
- [Lloyd's Line of Business Mapping Tools](https://www.lloyds.com/resources-and-services/reporting-rationalisation/tpd-reserving)
- [Catastrophe Codes](https://www.lloyds.com/resources-and-services/claims-for-market-participants/catastrophe-portal/catastrophe-codes/)

## Additional Resources

### R Documentation

- [R Data Frames](https://www.rdocumentation.org/packages/base/versions/3.6.2/topics/data.frame)
- [R Random Number Generation](https://www.rdocumentation.org/packages/base/versions/3.6.2/topics/Random)

### Power BI R Integration

- [Use R in Power BI](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-r-scripts)
- [Create R visuals in Power BI](https://docs.microsoft.com/en-us/power-bi/create-reports/desktop-r-visuals)

## Support

For issues or questions:
1. Check the inline code comments in each script
2. Review the summary statistics output
3. Verify your R installation and Power BI configuration
4. Run the scripts in RStudio to test independently

## License

These scripts are provided as-is for generating synthetic Lloyd's of London data for development and testing purposes.

---

**Last Updated**: 2025-11-21
**Version**: 1.0
**Author**: Claude
