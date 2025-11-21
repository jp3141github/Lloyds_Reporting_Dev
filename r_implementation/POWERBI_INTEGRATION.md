# Power BI Integration Guide - R

This guide explains how to use the Lloyd's Liquidity Stress Test R scripts in Power BI.

## Prerequisites

1. **Enable R in Power BI Desktop**
   - Go to File → Options and settings → Options
   - Navigate to R scripting
   - Set your R installation directory
   - Ensure required packages are installed:
     ```r
     install.packages(c("dplyr", "tidyr", "jsonlite", "readr", "openxlsx", "R6"))
     ```

2. **Data Files**
   - Upload the CSV files from the `data/` folder to your Power BI model
   - Or connect directly to the file location

## Method 1: Import Data into Power BI

### Step 1: Load the CSV Files

1. Click "Get Data" → "Text/CSV"
2. Import the following files:
   - `all_syndicates_metadata.csv`
   - `all_syndicates_assets.csv`
   - `all_syndicates_cashflow.csv`
   - `all_syndicates_stress.csv`

### Step 2: Create R Visual

1. Add an R visual to your report canvas
2. Drag fields from your imported tables into the visual's "Values" field well
3. Click the R script editor

### Step 3: Use the Functions

#### Example 1: Capital Position Dashboard

```r
# Power BI provides the 'dataset' variable
library(dplyr)
library(ggplot2)

source("path/to/Lloyds_Reporting_Dev/r_implementation/liquidity_stress_test.R")

# Process the data
result <- get_capital_position(dataset)

# Create visualization
ggplot(result, aes(x = reorder(syndicate_name, solvency_ratio), y = solvency_ratio)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  geom_hline(yintercept = 1.0, color = "red", linetype = "dashed", size = 1) +
  coord_flip() +
  labs(
    title = "Syndicate Solvency Ratios",
    x = "Syndicate",
    y = "Solvency Ratio"
  ) +
  theme_minimal()
```

#### Example 2: Liquidity Breakdown

```r
library(dplyr)
library(ggplot2)
library(tidyr)

source("path/to/Lloyds_Reporting_Dev/r_implementation/liquidity_stress_test.R")

# Process the data
result <- get_liquidity_breakdown(dataset)

# Filter to most recent date
recent <- result %>%
  filter(date == max(date))

# Reshape for stacked bar chart
plot_data <- recent %>%
  select(syndicate_number, restricted_pct, illiquid_pct, liquid_pct) %>%
  pivot_longer(cols = c(restricted_pct, illiquid_pct, liquid_pct),
               names_to = "asset_type",
               values_to = "percentage")

# Create stacked bar chart
ggplot(plot_data, aes(x = as.factor(syndicate_number), y = percentage, fill = asset_type)) +
  geom_bar(stat = "identity") +
  scale_fill_manual(
    values = c("restricted_pct" = "#E74C3C", "illiquid_pct" = "#F39C12", "liquid_pct" = "#27AE60"),
    labels = c("Restricted", "Illiquid", "Liquid")
  ) +
  labs(
    title = "Asset Composition by Syndicate",
    x = "Syndicate Number",
    y = "Percentage (%)",
    fill = "Asset Type"
  ) +
  theme_minimal()
```

#### Example 3: Stress Test Analysis

```r
library(dplyr)
library(ggplot2)
library(R6)

source("path/to/Lloyds_Reporting_Dev/r_implementation/liquidity_stress_test.R")

# Initialize
lst <- LiquidityStressTest$new("path/to/data")
lst$load_data()

# Get stress impact
stress_impact <- lst$calculate_stress_impact_table()

# Filter for specific syndicate
synd_2001 <- stress_impact %>%
  filter(syndicate_number == 2001)

# Reshape for plotting
plot_data <- synd_2001 %>%
  select(date, closing_free_funds, stressed_closing_funds) %>%
  pivot_longer(cols = c(closing_free_funds, stressed_closing_funds),
               names_to = "scenario",
               values_to = "funds")

# Plot baseline vs stressed liquidity
ggplot(plot_data, aes(x = date, y = funds, color = scenario, group = scenario)) +
  geom_line(size = 1) +
  geom_point(size = 3) +
  geom_hline(yintercept = 0, color = "red", linetype = "dashed", size = 1) +
  scale_color_manual(
    values = c("closing_free_funds" = "#2ECC71", "stressed_closing_funds" = "#E74C3C"),
    labels = c("Baseline", "Stressed")
  ) +
  labs(
    title = "Liquidity Position - Baseline vs Stress Scenario",
    x = "Date",
    y = "Free Funds (£)",
    color = "Scenario"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
```

## Method 2: Run R Script in Power Query

1. Go to "Transform Data" → "Get Data" → "Other" → "Blank Query"
2. Open Advanced Editor
3. Use this template:

```m
let
    Source = R.Execute(
        "library(dplyr)#(lf)" &
        "library(readr)#(lf)" &
        "library(R6)#(lf)" &
        "#(lf)" &
        "source('path/to/Lloyds_Reporting_Dev/r_implementation/liquidity_stress_test.R')#(lf)" &
        "#(lf)" &
        "lst <- LiquidityStressTest$new('path/to/data')#(lf)" &
        "lst$load_data()#(lf)" &
        "summary <- lst$create_dashboard_summary()#(lf)"
    ),
    summary = Source{[Name="summary"]}[Value]
in
    summary
```

## Method 3: Direct Data Import with R

Use R to load and transform data directly:

1. Click "Get Data" → "More" → "Other" → "R Script"
2. Enter the following script:

```r
library(R6)
source("path/to/Lloyds_Reporting_Dev/r_implementation/liquidity_stress_test.R")

lst <- LiquidityStressTest$new("path/to/data")
lst$load_data()

# Create all output tables
capital_position <- lst$calculate_capital_position_table()
liquidity_breakdown <- lst$calculate_liquidity_breakdown_table()
cashflow_summary <- lst$calculate_cashflow_summary_table()
stress_impact <- lst$calculate_stress_impact_table()
dashboard_summary <- lst$create_dashboard_summary()
```

3. Power BI will show all resulting data frames
4. Select the tables you want to import

## Tips for Best Performance

1. **Pre-process Data**: Run the R scripts once to create the output tables, then import the results as CSV
2. **Use Filters**: Apply syndicate or date filters before running R scripts
3. **Cache Results**: Store processed data in Power BI tables rather than re-running scripts
4. **Vectorized Operations**: R's dplyr package is optimized for large datasets

## Common Issues

### Issue: Package not found
**Solution**: Install required packages:
```r
install.packages(c("dplyr", "tidyr", "jsonlite", "readr", "openxlsx", "R6", "ggplot2"))
```

### Issue: Source file not found
**Solution**: Use absolute paths instead of relative paths in `source()` function

### Issue: R visual not showing
**Solution**:
- Check R installation in Options
- Verify all required packages are installed
- Check for errors in the R script editor
- Ensure R is added to PATH environment variable

### Issue: Data frame not appearing in Power Query
**Solution**: Make sure the last line of your R script is the data frame name (no semicolon)

## Example Dashboard Layout

Recommended visuals for a complete dashboard:

1. **Executive Summary** (Card visuals)
   - Total FAL across all syndicates
   - Average solvency ratio
   - Number of syndicates passing stress test

2. **Capital Position** (R visual - ggplot2 bar chart)
   - Solvency ratios by syndicate

3. **Liquidity Breakdown** (R visual - stacked bar)
   - Asset composition by type

4. **Stress Impact** (R visual - line chart)
   - Baseline vs stressed liquidity over time

5. **Risk Metrics** (Table visual)
   - Detailed metrics from dashboard summary

## Advanced: Interactive Filtering

Create slicers that work with R visuals:

1. Create a slicer for syndicate number
2. In your R visual, use the filtered dataset:

```r
# Power BI automatically filters 'dataset' based on slicers
library(dplyr)
library(ggplot2)

source("path/to/Lloyds_Reporting_Dev/r_implementation/liquidity_stress_test.R")

lst <- LiquidityStressTest$new("path/to/data")
lst$cashflow_data <- dataset

result <- lst$calculate_cashflow_summary_table()

ggplot(result, aes(x = date, y = closing_free_funds)) +
  geom_line(color = "steelblue", size = 1) +
  geom_point(size = 3) +
  labs(
    title = "Free Funds Over Time",
    x = "Date",
    y = "Closing Free Funds (£)"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
```

## Performance Optimization

For large datasets, consider:

1. **Pre-aggregate data** in Power Query before passing to R
2. **Use data.table** package instead of dplyr for better performance:
   ```r
   library(data.table)
   dt <- as.data.table(dataset)
   ```
3. **Limit rows** using Top N filter in Power BI before R script runs
4. **Cache intermediate results** in Power BI tables

## Publishing to Power BI Service

When publishing reports with R visuals:

1. Ensure R runtime is available on Power BI Service (Personal Gateway required)
2. Install all required packages on the gateway machine
3. Use absolute paths or environment variables for file locations
4. Test with Personal Gateway before publishing to shared workspace
