# R Implementation - FSCS Data Generator

This directory contains the R implementation of the FSCS data generator for Lloyd's syndicates.

## Files

- **`fscs_data_generator.R`**: Core data generation module with FSCSDataGenerator function
- **`powerbi_query.R`**: Self-contained script for Power BI R data source
- **`example_usage.R`**: Comprehensive examples demonstrating all features
- **`install_packages.R`**: Automated package installation script

## Installation

### Prerequisites

- R 4.0 or higher
- RStudio (optional but recommended)

### Install Dependencies

```r
# Option 1: Use the automated installation script
source("install_packages.R")

# Option 2: Manual installation
install.packages(c("dplyr", "tibble", "lubridate", "writexl"))
```

Required packages:
- `dplyr`: Data manipulation
- `tibble`: Modern data frames
- `lubridate`: Date/time handling
- `writexl`: Excel export (no Java dependency)

## Usage

### 1. Basic Usage - Summary Data

```r
# Source the generator
source("fscs_data_generator.R")

# Generate FSCS summary data for 10 syndicates
summary <- get_fscs_summary_data(num_syndicates = 10, reporting_year = 2024)
print(summary)
```

### 2. Generate Detailed Transaction Data

```r
source("fscs_data_generator.R")

# Generate detailed transaction-level data
detail <- get_fscs_detail_data(num_syndicates = 10, reporting_year = 2024)
cat(sprintf("Generated %d transactions\n", nrow(detail)))
print(head(detail))
```

### 3. Using the Generator Function

```r
source("fscs_data_generator.R")

# Create generator instance
generator <- FSCSDataGenerator(
  num_syndicates = 15,
  reporting_year = 2024,
  random_seed = 42  # For reproducibility
)

# Generate different data formats
fscs_output <- generator$generate_fscs_output_format()
full_data <- generator$generate_full_dataset()
detail_data <- generator$generate_detail_dataset()
```

### 4. Export to Excel

```r
library(writexl)
source("fscs_data_generator.R")

generator <- FSCSDataGenerator(num_syndicates = 10, reporting_year = 2024)

# Generate all data types
summary <- generator$generate_fscs_output_format()
detail <- generator$generate_detail_dataset()
full <- generator$generate_full_dataset()

# Create list for Excel export
excel_data <- list(
  "FSCS_Summary" = summary,
  "Transactions" = detail,
  "Full_Data" = full
)

# Export to Excel
write_xlsx(excel_data, "FSCS_Data.xlsx")
```

## Power BI Integration

### Method 1: Using powerbi_query.R (Recommended)

1. Open Power BI Desktop
2. Go to **Home** > **Get Data** > **More**
3. Search for and select **R script**
4. Click **Connect**
5. Copy the entire contents of `powerbi_query.R`
6. Paste into the script window
7. Click **OK**
8. Select the `dataset` table in the navigator
9. Click **Load**

### Method 2: Custom Query

Create your own Power BI query:

```r
library(dplyr)
library(tibble)
library(lubridate)

# Source the generator
source("path/to/fscs_data_generator.R")

# Generate data
dataset <- get_fscs_summary_data(num_syndicates = 15, reporting_year = 2024)

# dataset will be automatically loaded into Power BI
```

### Power BI Configuration

Before using R scripts in Power BI:

1. **Install R**: Download from [CRAN](https://cran.r-project.org/)
2. **Install Required Packages**: Run `source("install_packages.R")`
3. **Configure Power BI**:
   - File > Options and settings > Options
   - R scripting section
   - Set R installation directory (e.g., `C:\Program Files\R\R-4.3.2`)
4. **Restart Power BI** after configuration

### Testing R Configuration

```r
# Test in R console first
source("powerbi_query.R")
print(dataset)
```

## API Reference

### FSCSDataGenerator Function

```r
FSCSDataGenerator <- function(num_syndicates = 10,
                              reporting_year = 2024,
                              random_seed = 42)
```

**Parameters:**
- `num_syndicates`: Number of syndicates to generate data for
- `reporting_year`: Year for which the data is being reported
- `random_seed`: Seed for reproducibility

**Returns:** A list containing generator functions

#### Returned Functions

##### `generate_syndicate_numbers()`
Returns a vector of realistic Lloyd's syndicate numbers (4-digit numbers in range 2000-6000).

##### `generate_gross_written_premium(business_type = 'general')`
Generates GWP values for specified business type.

**Parameters:**
- `business_type`: 'general' or 'life'

**Returns:** Numeric vector of premium values

##### `generate_best_estimate_liabilities(gwp_values, business_type = 'general')`
Generates BEL values correlated with GWP.

**Parameters:**
- `gwp_values`: Numeric vector of GWP values
- `business_type`: 'general' or 'life'

**Returns:** Numeric vector of liability values

##### `generate_full_dataset()`
Generates complete dataset with all fields and calculated columns.

**Returns:** tibble

##### `generate_fscs_output_format()`
Generates data in exact FSCS submission format.

**Returns:** tibble

##### `generate_detail_dataset()`
Generates detailed transaction-level data (50-200 contracts per syndicate).

**Returns:** tibble

### Convenience Functions

```r
get_fscs_summary_data <- function(num_syndicates = 10, reporting_year = 2024)
# Generate FSCS summary data

get_fscs_detail_data <- function(num_syndicates = 10, reporting_year = 2024)
# Generate detailed transaction data
```

## Data Specifications

### Premium Generation

- **General Business**: Log-normal distribution
  - Mean: £150M
  - Range: £10M - £500M
  - ~20% syndicates may have zero GWP

- **Life Business**: Log-normal distribution
  - Mean: £30M
  - Range: £1M - £100M
  - ~20% syndicates may have zero GWP

### Liability Generation

- **General Business BEL**: 1.5x - 3.0x of GWP (±20% variation)
- **Life Business BEL**: 3.0x - 8.0x of GWP (±20% variation)
- For zero GWP: BEL ranges from £0 - £5M

### Detail Data

Each syndicate generates 50-200 contracts with:
- 70% General business, 30% Life business
- Various business classes (Property, Casualty, Marine, Aviation, Energy, etc.)
- Random inception and expiry dates
- 90% are protected contracts
- 85% have eligible claimants
- Territory distribution (UK, EEA, Worldwide)

## Testing

Run the example script to test all functionality:

```bash
Rscript example_usage.R
```

Or in R console:

```r
source("example_usage.R")
```

This will:
1. Generate summary data
2. Generate detailed transaction data
3. Demonstrate generator usage
4. Create multi-year datasets
5. Export to Excel
6. Display summary statistics
7. Perform analytical aggregations

## Common Issues

### Package Installation Errors

**Error**: "package 'dplyr' is not available"

**Solution**:
```r
# Ensure CRAN mirror is set
options(repos = c(CRAN = "https://cran.r-project.org"))
install.packages("dplyr")
```

### Power BI can't find R

**Solution**:
1. Verify R is installed: Open R console and check version
2. Configure R path in Power BI Options
3. Use the R home directory (not bin folder)
   - Correct: `C:\Program Files\R\R-4.3.2`
   - Incorrect: `C:\Program Files\R\R-4.3.2\bin`

### RGL or RJava Errors

**Solution**: This package uses `writexl` which has no Java dependencies. If you encounter RJava errors:
```r
# Use writexl instead of xlsx or openxlsx
install.packages("writexl")
library(writexl)
```

### Locale/Date Format Issues

**Solution**:
```r
# Set locale if needed
Sys.setlocale("LC_TIME", "English")

# Or use explicit date formats
format(date_column, "%Y-%m-%d")
```

### Tibble vs Data Frame

The generator returns tibbles (modern data frames). If you need traditional data frames:
```r
result <- as.data.frame(generator$generate_full_dataset())
```

## Performance

- **Summary data** (10 syndicates): < 1 second
- **Detail data** (10 syndicates, ~1000 contracts): < 3 seconds
- **Excel export** (10 syndicates): < 5 seconds

For larger datasets:
- 100 syndicates: ~15 seconds
- 1000 syndicates: ~3 minutes

## Customization Examples

### Adjust Premium Ranges

```r
# Edit in fscs_data_generator.R
generate_gross_written_premium <- function(business_type = 'general') {
  if (business_type == 'general') {
    min_value <- 5000000        # Lower minimum
    max_value <- 1000000000     # Higher maximum
    mean_log <- log(200000000)  # Higher mean
  }
  # ... rest of function
}
```

### Change BEL Multipliers

```r
# Edit in fscs_data_generator.R
generate_best_estimate_liabilities <- function(gwp_values, business_type = 'general') {
  if (business_type == 'general') {
    multiplier <- runif(params$num_syndicates, 2.0, 4.0)  # Higher range
  }
  # ... rest of function
}
```

### Add Custom Fields

```r
generator <- FSCSDataGenerator(num_syndicates = 10)
df <- generator$generate_full_dataset()

# Add custom fields using dplyr
df <- df %>%
  mutate(
    year_of_account = 2024,
    stamp_capacity = gwp_total * 1.2,
    risk_rating = sample(c('A', 'B', 'C'), n(), replace = TRUE)
  )
```

## Best Practices

1. **Use consistent random seeds** for reproducible results
2. **Source the script** at the beginning of your analysis
3. **Test with small datasets** first (5-10 syndicates)
4. **Use tibbles** for better printing and subsetting
5. **Export to Excel** for easy sharing and review
6. **Document assumptions** when sharing with others

## Integration with Other Tools

### RMarkdown Reports

```r
---
title: "FSCS Data Analysis"
output: html_document
---

```{r setup}
source("fscs_data_generator.R")
library(dplyr)
library(ggplot2)
```

```{r generate}
generator <- FSCSDataGenerator(num_syndicates = 20)
df <- generator$generate_full_dataset()
```

```{r analysis}
df %>%
  ggplot(aes(x = syndicate_number, y = gwp_total / 1e6)) +
  geom_col() +
  labs(title = "Total GWP by Syndicate", y = "GWP (£M)")
```
```

### Shiny Dashboard

```r
library(shiny)
source("fscs_data_generator.R")

ui <- fluidPage(
  titlePanel("FSCS Data Generator"),
  sidebarLayout(
    sidebarPanel(
      sliderInput("num_syndicates", "Number of Syndicates", 5, 50, 10),
      selectInput("year", "Reporting Year", c(2022, 2023, 2024)),
      actionButton("generate", "Generate Data")
    ),
    mainPanel(
      tableOutput("data_table")
    )
  )
)

server <- function(input, output) {
  data <- eventReactive(input$generate, {
    get_fscs_summary_data(input$num_syndicates, as.integer(input$year))
  })

  output$data_table <- renderTable({
    data()
  })
}

shinyApp(ui = ui, server = server)
```

### Data Pipeline Example

```r
library(dplyr)
library(writexl)
source("fscs_data_generator.R")

# Generate data for multiple years
years <- 2022:2024
all_data <- lapply(years, function(year) {
  get_fscs_summary_data(num_syndicates = 10, reporting_year = year)
}) %>% bind_rows()

# Perform analysis
analysis <- all_data %>%
  group_by(`Reporting Year`) %>%
  summarise(
    Total_GWP = sum(`GWP General Business (£)` + `GWP Life Business (£)`),
    Avg_Syndicate_GWP = mean(`GWP General Business (£)` + `GWP Life Business (£)`),
    .groups = 'drop'
  )

# Export results
write_xlsx(list(
  "Raw_Data" = all_data,
  "Analysis" = analysis
), "FSCS_Multi_Year_Analysis.xlsx")
```

## Advanced Usage

### Parallel Processing

```r
library(parallel)
library(dplyr)
source("fscs_data_generator.R")

# Generate data for multiple scenarios in parallel
scenarios <- expand.grid(
  num_syndicates = c(10, 20, 30),
  year = 2022:2024
)

# Use mclapply (Unix/Mac) or parLapply (Windows)
results <- mclapply(1:nrow(scenarios), function(i) {
  get_fscs_summary_data(
    scenarios$num_syndicates[i],
    scenarios$year[i]
  )
}, mc.cores = 4)

combined <- bind_rows(results)
```

### Custom Validation

```r
validate_fscs_data <- function(df) {
  checks <- list(
    all_positive = all(df$`GWP General Business (£)` >= 0),
    all_syndicates_valid = all(df$`Syndicate Number` >= 1 & df$`Syndicate Number` <= 9999),
    no_missing = !any(is.na(df))
  )

  if (all(unlist(checks))) {
    cat("✓ All validation checks passed\n")
    return(TRUE)
  } else {
    cat("✗ Validation failed:\n")
    print(checks)
    return(FALSE)
  }
}

# Use validation
data <- get_fscs_summary_data(10, 2024)
validate_fscs_data(data)
```

## Version Compatibility

- **R 4.0**: Minimum version
- **R 4.1-4.3**: Fully tested
- **R 4.4**: Compatible (recommended)

### Package Versions

```r
# Check your package versions
packageVersion("dplyr")     # >= 1.0.0
packageVersion("tibble")    # >= 3.0.0
packageVersion("lubridate") # >= 1.7.0
packageVersion("writexl")   # >= 1.4.0
```

## Troubleshooting

### Script Hangs or Runs Slowly

```r
# Check if you're generating too many contracts
# Reduce num_syndicates or add progress monitoring
generator <- FSCSDataGenerator(num_syndicates = 5)  # Start small
```

### Memory Issues with Large Datasets

```r
# For very large datasets, generate in batches
generate_batches <- function(total_syndicates, batch_size = 100) {
  batches <- ceiling(total_syndicates / batch_size)
  results <- list()

  for (i in 1:batches) {
    n <- min(batch_size, total_syndicates - (i-1) * batch_size)
    results[[i]] <- get_fscs_summary_data(n, 2024)
  }

  bind_rows(results)
}
```

## Support

For R-specific issues:
1. Check package installations with `library(package_name)`
2. Verify R version with `R.version`
3. Review example_usage.R for correct usage patterns
4. Test in R/RStudio before Power BI integration

## Useful Resources

- [dplyr documentation](https://dplyr.tidyverse.org/)
- [R for Data Science](https://r4ds.had.co.nz/)
- [Power BI R Integration](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-r-scripts)

---

**Next Steps**: After testing the R implementation, refer to the main README for Power BI integration instructions.
