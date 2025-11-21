# Power BI Integration Guide - R QSR Reports

This guide explains how to use the R QSR report scripts in Power BI.

## Prerequisites

1. **R Installation**: Ensure R 4.0+ is installed on your system
2. **Required Packages**: Install the following R packages:
   ```r
   install.packages(c("dplyr", "tidyr"))
   ```
3. **Power BI Desktop**: Ensure R scripting is enabled in Power BI Desktop

## Setup in Power BI

### 1. Configure R in Power BI

1. Open Power BI Desktop
2. Go to **File > Options and settings > Options**
3. Select **R scripting** under Global
4. Set your R installation directory (e.g., `C:\Program Files\R\R-4.x.x\bin\x64`)
5. Choose your R IDE (optional)
6. Click OK

### 2. Generate Synthetic Data (One-Time Setup)

Before using the reports in Power BI, generate the synthetic data:

```r
setwd("Solvency_II_QSR_Reporting/R")
source("synthetic_data_generator.R")
generate_all_data(num_syndicates = 15)
```

Or from command line:
```bash
cd Solvency_II_QSR_Reporting/R
Rscript synthetic_data_generator.R
```

This will create CSV files in the `Data` folder:
- `synthetic_balance_sheet.csv`
- `synthetic_own_funds.csv`
- `synthetic_technical_provisions.csv`
- `synthetic_premiums_claims.csv`
- `synthetic_investments.csv`
- `synthetic_scr_calculation.csv`
- `synthetic_mcr_calculation.csv`

## Using R Scripts in Power BI

### Method 1: Import Data Using R Script

1. In Power BI Desktop, click **Get Data**
2. Select **More... > Other > R script**
3. Click **Connect**
4. Paste one of the following scripts:

#### Example: Load Balance Sheet (QSR 002)

```r
# Set working directory
setwd("C:/path/to/Solvency_II_QSR_Reporting/R")

# Source the QSR report generator
source("qsr_report_generator.R")

# Generate the report
dataset <- get_balance_sheet(data_dir = '../Data/')
```

#### Example: Load Own Funds (QSR 220)

```r
setwd("C:/path/to/Solvency_II_QSR_Reporting/R")
source("qsr_report_generator.R")
dataset <- get_own_funds(data_dir = '../Data/')
```

#### Example: Load Solvency Ratios

```r
setwd("C:/path/to/Solvency_II_QSR_Reporting/R")
source("qsr_report_generator.R")
dataset <- get_solvency_ratios(data_dir = '../Data/')
```

5. Click **OK**
6. Power BI will execute the R script and show available datasets
7. Select the dataset and click **Load**

### Method 2: Transform Data Using R Script

1. Load your raw data into Power BI (from CSV or database)
2. Select the table in **Query Editor**
3. Go to **Transform > Run R script**
4. Add transformation logic:

```r
# Load required libraries
library(dplyr)

# Set working directory
setwd("C:/path/to/Solvency_II_QSR_Reporting/R")

# Source the report generator
source("qsr_report_generator.R")

# Create generator instance
generator <- QSRReportGenerator(data_dir = '../Data/')
generator$load_data()

# Transform to QSR format
dataset <- generator$generate_qsr002_balance_sheet()
```

## Available Reports

### QSR 002 - Balance Sheet
```r
source("qsr_report_generator.R")
dataset <- get_balance_sheet(data_dir = '../Data/')
```

### QSR 220 - Own Funds
```r
source("qsr_report_generator.R")
dataset <- get_own_funds(data_dir = '../Data/')
```

### QSR 240 - Technical Provisions
```r
source("qsr_report_generator.R")
dataset <- get_technical_provisions(data_dir = '../Data/')
```

### QSR 440 - Premiums and Claims
```r
source("qsr_report_generator.R")
dataset <- get_premiums_claims(data_dir = '../Data/')
```

### Solvency Ratios Summary
```r
source("qsr_report_generator.R")
dataset <- get_solvency_ratios(data_dir = '../Data/')
```

## Sample Power BI Workflow

### Step 1: Load All QSR Reports

Create separate queries for each report:

1. **Balance Sheet Query**
   - Get Data > R script
   - Use `get_balance_sheet()` function
   - Name: "QSR_002_Balance_Sheet"

2. **Own Funds Query**
   - Get Data > R script
   - Use `get_own_funds()` function
   - Name: "QSR_220_Own_Funds"

3. **Solvency Ratios Query**
   - Get Data > R script
   - Use `get_solvency_ratios()` function
   - Name: "Solvency_Ratios"

### Step 2: Create Relationships

In the **Model** view, create relationships between tables:
- Link tables by `Syndicate` field
- Link tables by `Reporting_Date` field

### Step 3: Build Visualizations

Create dashboards with:
- **SCR/MCR Coverage Ratios**: Bar charts showing solvency ratios by syndicate
- **Own Funds Composition**: Stacked bar charts showing Tier 1, 2, 3 breakdown
- **Technical Provisions**: Tables showing provisions by line of business
- **Balance Sheet**: Waterfall charts for assets and liabilities
- **Premiums vs Claims**: Line charts showing trends over time
- **Combined Ratio Analysis**: KPI cards and trend charts

### Step 4: Add Slicers

Add slicers for:
- Syndicate selection
- Reporting date
- Line of business
- Risk module

## Advanced: Custom Data Pipeline

For production use, create a custom data pipeline:

```r
# custom_pipeline.R
library(dplyr)

# Load your actual data from database or files
load_actual_data <- function() {
  # Replace with your actual data loading logic
  balance_sheet <- read.csv("your_balance_sheet.csv")
  own_funds <- read.csv("your_own_funds.csv")
  # ... load other data sources

  return(list(
    balance_sheet = balance_sheet,
    own_funds = own_funds,
    # ... other data
  ))
}

# Process and transform to QSR format
process_qsr_reports <- function() {
  source("qsr_report_generator.R")

  # Load actual data
  data <- load_actual_data()

  # Create generator with custom data
  generator <- QSRReportGenerator(data_dir = '../Data/')
  reports <- generator$generate_all_reports()

  return(reports)
}

# Use in Power BI
dataset <- process_qsr_reports()$QSR002_Balance_Sheet
```

## Refreshing Data

### Manual Refresh
1. Click **Refresh** in Power BI Desktop
2. The R scripts will re-execute and reload data

### Scheduled Refresh (Power BI Service)
1. Publish report to Power BI Service
2. Configure gateway with R runtime
3. Set up scheduled refresh
4. Ensure all R packages are installed on the gateway server

## Troubleshooting

### Issue: "R script error"
- **Solution**: Check R path in Power BI options
- Verify R is installed correctly: Open R console and test
- Ensure 64-bit version of R is installed if using 64-bit Power BI

### Issue: "Package not found"
- **Solution**: Install required packages:
  ```r
  install.packages(c("dplyr", "tidyr"))
  ```
- Verify installation: `library(dplyr)` should work in R console

### Issue: "Data not loading"
- **Solution**: Run `synthetic_data_generator.R` first to create data files
- Check that CSV files exist in the Data directory
- Verify working directory path is correct

### Issue: "setwd() errors"
- **Solution**: Use absolute paths with forward slashes
- Example: `setwd("C:/Users/YourName/Solvency_II_QSR_Reporting/R")`
- Avoid spaces in paths, or use quotes properly

### Issue: "Cannot source file"
- **Solution**: Ensure `qsr_report_generator.R` is in the working directory
- Check file permissions
- Use `list.files()` to verify files are accessible

## Best Practices

1. **Use Absolute Paths**: Always use absolute paths for data directories
2. **Test in R Console First**: Test your scripts in R console before using in Power BI
3. **Separate Queries**: Create separate queries for each report type
4. **Cache Data**: Store processed data to avoid re-running generators
5. **Error Handling**: Add tryCatch blocks for robustness:
   ```r
   tryCatch({
     dataset <- get_balance_sheet()
   }, error = function(e) {
     cat("Error:", e$message, "\n")
     dataset <- data.frame()
   })
   ```
6. **Version Control**: Keep track of R and package versions
7. **Documentation**: Document any custom transformations

## Example Dashboard Measures (DAX)

Even when using R for data import, you can use DAX for calculations:

### Total Own Funds
```dax
Total Own Funds = SUM(QSR_220_Own_Funds[R0120_Total_Own_Funds])
```

### Average SCR Ratio
```dax
Avg SCR Ratio = AVERAGE(Solvency_Ratios[SCR_Ratio])
```

### Combined Ratio
```dax
Combined Ratio =
    DIVIDE(
        SUM(QSR_440_Premiums_Claims[Claims_Incurred_Net]) + SUM(QSR_440_Premiums_Claims[Expenses_Incurred]),
        SUM(QSR_440_Premiums_Claims[Premiums_Earned_Net]),
        0
    ) * 100
```

### Number of Compliant Syndicates (SCR > 100%)
```dax
Compliant Syndicates =
    COUNTROWS(
        FILTER(
            Solvency_Ratios,
            Solvency_Ratios[SCR_Ratio] >= 100
        )
    )
```

## R-Specific Visualizations

You can also create R-based visualizations in Power BI:

### Example: Custom R Visual for Risk Distribution

```r
# Load data (Power BI provides 'dataset' variable)
library(ggplot2)

# Create risk distribution plot
ggplot(dataset, aes(x = Syndicate, y = SCR, fill = Syndicate)) +
  geom_bar(stat = "identity") +
  theme_minimal() +
  labs(title = "SCR by Syndicate",
       x = "Syndicate",
       y = "Solvency Capital Requirement (£)") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
```

## Performance Optimization

For large datasets:

1. **Use data.table instead of dplyr** for faster processing:
   ```r
   library(data.table)
   dt <- fread("large_file.csv")
   ```

2. **Filter early** to reduce data size:
   ```r
   dataset <- dataset %>%
     filter(Reporting_Date >= as.Date("2024-01-01"))
   ```

3. **Use sampling** for development/testing:
   ```r
   dataset <- dataset %>% sample_n(1000)
   ```

## Support

For issues or questions:
1. Check R script logs in Power BI
2. Test scripts independently in R console
3. Verify data file formats and locations
4. Review Power BI R integration documentation
5. Check R package versions: `packageVersion("dplyr")`

## Comparison: R vs Python

| Feature | R | Python |
|---------|---|--------|
| Learning Curve | Moderate (statistical focus) | Easier (general purpose) |
| Performance | Good with data.table | Good with pandas |
| Visualization | Excellent (ggplot2) | Good (matplotlib) |
| Power BI Integration | Native support | Native support |
| Package Ecosystem | Strong for statistics | Strong for general ML/Data |

Choose based on your team's expertise and existing infrastructure.

---

**Note**: This implementation uses synthetic data. Replace the data source with your actual Lloyd's syndicate data by modifying the data loading functions in `qsr_report_generator.R`.
