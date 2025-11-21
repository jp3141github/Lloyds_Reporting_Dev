# R Implementation - Lloyd's Liquidity Stress Test

This folder contains the R implementation for processing Lloyd's Liquidity Stress Test data for Power BI integration.

## Files

- `liquidity_stress_test.R` - Main R module with R6 class implementation
- `POWERBI_INTEGRATION.md` - Detailed guide for using in Power BI
- `syndicate_2001_analysis.xlsx` - Example output for Syndicate 2001
- `all_syndicates_analysis.xlsx` - Example output for all syndicates

## Quick Start

### 1. Install Dependencies

```r
install.packages(c("dplyr", "tidyr", "jsonlite", "readr", "openxlsx", "R6", "ggplot2"))
```

### 2. Run Standalone

```bash
cd ..  # Go to repository root
Rscript r_implementation/liquidity_stress_test.R
```

### 3. Source as Module

```r
source("r_implementation/liquidity_stress_test.R")

# Initialize
lst <- LiquidityStressTest$new("data")
lst$load_data()

# Get all output tables
tables <- lst$calculate_rra_output_tables()

# Generate dashboard
summary <- lst$create_dashboard_summary()
print(summary)
```

## Main Class: LiquidityStressTest

### Initialization

```r
lst <- LiquidityStressTest$new(data_path = "../data")
```

**Parameters:**
- `data_path` (character): Path to directory containing syndicate data

### Methods

#### load_data(syndicate_number = NULL)
Load syndicate data from CSV files.

**Parameters:**
- `syndicate_number` (integer, optional): Load specific syndicate. If NULL, loads all.

**Returns:**
- list: List containing loaded data frames

**Example:**
```r
# Load all syndicates
lst$load_data()

# Load specific syndicate
data <- lst$load_data(syndicate_number = 2001)
```

#### calculate_capital_position_table(syndicate_number = NULL)
Generate capital position summary.

**Returns:**
- data.frame: Capital position with FAL, FIS, uSCR, uECA, ratios

**Example:**
```r
capital <- lst$calculate_capital_position_table()
print(capital[, c('syndicate_name', 'solvency_ratio')])
```

#### calculate_liquidity_breakdown_table(syndicate_number = NULL, date = NULL)
Generate asset and liquidity breakdown.

**Parameters:**
- `syndicate_number` (integer, optional): Filter by syndicate
- `date` (character, optional): Filter by date (YYYY-MM-DD)

**Returns:**
- data.frame: Liquidity breakdown by asset type

**Example:**
```r
liquidity <- lst$calculate_liquidity_breakdown_table(date = "2024-12-31")
print(liquidity[, c('syndicate_number', 'liquid_pct', 'illiquid_pct')])
```

#### calculate_cashflow_summary_table(syndicate_number = NULL)
Generate cashflow summary.

**Returns:**
- data.frame: Cashflow details with cumulative totals

**Example:**
```r
cashflow <- lst$calculate_cashflow_summary_table(syndicate_number = 2001)
print(cashflow[, c('date', 'closing_free_funds', 'total_movements')])
```

#### calculate_stress_impact_table(syndicate_number = NULL)
Generate stress test impact analysis.

**Returns:**
- data.frame: Baseline vs stressed scenarios

**Example:**
```r
stress <- lst$calculate_stress_impact_table()
print(stress[, c('syndicate_number', 'date', 'liquidity_gap', 'stressed_closing_funds')])
```

#### create_dashboard_summary(syndicate_number = NULL)
Create executive dashboard summary.

**Returns:**
- data.frame: High-level metrics and stress test results

**Example:**
```r
summary <- lst$create_dashboard_summary()
print(summary[, c('syndicate_name', 'solvency_ratio', 'stress_test_pass')])
```

#### export_to_excel(output_path, syndicate_number = NULL)
Export all tables to Excel workbook.

**Parameters:**
- `output_path` (character): Path for output Excel file
- `syndicate_number` (integer, optional): Filter by syndicate

**Example:**
```r
lst$export_to_excel("my_analysis.xlsx", syndicate_number = 2001)
```

## Power BI Functions

These wrapper functions are designed for use directly in Power BI R visuals.

### get_capital_position(dataset)

```r
source("liquidity_stress_test.R")

# In Power BI, 'dataset' is automatically provided
result <- get_capital_position(dataset)
```

### get_liquidity_breakdown(dataset)

```r
source("liquidity_stress_test.R")

result <- get_liquidity_breakdown(dataset)
```

### get_stress_impact(cashflow_dataset, stress_dataset)

```r
source("liquidity_stress_test.R")

result <- get_stress_impact(cashflow_dataset, stress_dataset)
```

## Example Workflows

### 1. Generate All RRA Tables

```r
library(dplyr)
library(readr)

source("r_implementation/liquidity_stress_test.R")

lst <- LiquidityStressTest$new("data")
lst$load_data()

# Get all tables
tables <- lst$calculate_rra_output_tables()

# Access individual tables
capital <- tables$capital_position
liquidity <- tables$liquidity_breakdown
cashflow <- tables$cashflow_summary
stress <- tables$stress_impact

# Save each table
write_csv(capital, "capital_position.csv")
write_csv(liquidity, "liquidity_breakdown.csv")
write_csv(cashflow, "cashflow_summary.csv")
write_csv(stress, "stress_impact.csv")
```

### 2. Analyze Single Syndicate

```r
library(dplyr)

source("r_implementation/liquidity_stress_test.R")

lst <- LiquidityStressTest$new("data")

# Load specific syndicate
data <- lst$load_data(syndicate_number = 2001)

# Generate analysis
capital <- lst$calculate_capital_position_table(syndicate_number = 2001)
stress <- lst$calculate_stress_impact_table(syndicate_number = 2001)

# Check stress test result
min_liquidity <- min(stress$stressed_closing_funds)
if (min_liquidity > 0) {
  cat("✓ Stress test PASSED\n")
} else {
  cat("✗ Stress test FAILED - liquidity shortfall detected\n")
}
```

### 3. Compare All Syndicates with Visualization

```r
library(dplyr)
library(ggplot2)

source("r_implementation/liquidity_stress_test.R")

lst <- LiquidityStressTest$new("data")
lst$load_data()

summary <- lst$create_dashboard_summary()

# Plot solvency ratios
ggplot(summary, aes(x = reorder(syndicate_name, solvency_ratio), y = solvency_ratio)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  geom_hline(yintercept = 1.0, color = "red", linetype = "dashed", size = 1) +
  coord_flip() +
  labs(
    title = "Syndicate Solvency Comparison",
    x = "Syndicate",
    y = "Solvency Ratio"
  ) +
  theme_minimal()

ggsave("solvency_comparison.png", width = 12, height = 6)
```

### 4. Export Comprehensive Report

```r
source("r_implementation/liquidity_stress_test.R")

lst <- LiquidityStressTest$new("data")
lst$load_data()

# Export for each syndicate
for (synd_num in unique(lst$metadata$syndicate_number)) {
  lst$export_to_excel(
    paste0("syndicate_", synd_num, "_report.xlsx"),
    syndicate_number = synd_num
  )
}

# Export combined report
lst$export_to_excel("all_syndicates_report.xlsx")
```

### 5. Time Series Analysis

```r
library(dplyr)
library(ggplot2)
library(tidyr)

source("r_implementation/liquidity_stress_test.R")

lst <- LiquidityStressTest$new("data")
lst$load_data()

# Get cashflow data
cashflow <- lst$calculate_cashflow_summary_table()

# Plot free funds over time for all syndicates
ggplot(cashflow, aes(x = date, y = closing_free_funds, color = as.factor(syndicate_number), group = syndicate_number)) +
  geom_line(size = 1) +
  geom_point(size = 2) +
  labs(
    title = "Free Funds Over Time by Syndicate",
    x = "Date",
    y = "Closing Free Funds (£)",
    color = "Syndicate"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
```

## Data Structure

### Input Data Expected

The module expects the following CSV files in the data directory:

1. **all_syndicates_metadata.csv**
   - syndicate_number, syndicate_name, managing_agent
   - syndicate_fal, syndicate_fis, syndicate_uscr, syndicate_ueca
   - scenario_type, gross_loss_estimate, net_loss_estimate
   - us_funding_requirement, etc.

2. **all_syndicates_assets.csv**
   - syndicate_number, date
   - us_trust_funds, other_trust_funds, other_restricted_assets
   - reinsurance_recoverables, reinsurer_urp_unearned, other_illiquid_assets
   - closing_free_funds, other_liquid_assets

3. **all_syndicates_cashflow.csv**
   - syndicate_number, date
   - opening_free_funds, closing_free_funds
   - premium_income, claims_paid, reinsurance_recoveries
   - All cashflow line items

4. **all_syndicates_stress.csv**
   - syndicate_number, date
   - stress_scenario_impact, cumulative_stress_impact

### Output Data Structure

All methods return data frames (tibbles) with consistent column naming:
- Snake_case for column names
- Currency values as integers (GBP)
- Ratios as numerics
- Dates as characters (YYYY-MM-DD)

## Performance Tips

1. **Load data once**: Call `load_data()` once and reuse the object
2. **Filter early**: Use syndicate_number parameter to reduce data size
3. **Use dplyr**: Leverage dplyr's efficient operations
4. **Cache results**: Save processed tables to CSV for repeated use

```r
# Good - load once
lst <- LiquidityStressTest$new("data")
lst$load_data()
table1 <- lst$calculate_capital_position_table()
table2 <- lst$calculate_stress_impact_table()

# Less efficient - creates multiple objects
lst1 <- LiquidityStressTest$new("data")
table1 <- lst1$calculate_capital_position_table()

lst2 <- LiquidityStressTest$new("data")
table2 <- lst2$calculate_stress_impact_table()
```

## Error Handling

The module includes basic error handling:

```r
tryCatch({
  lst <- LiquidityStressTest$new("data")
  lst$load_data()
}, error = function(e) {
  message("Error loading data: ", e$message)
})
```

## Integration with Power BI

See [POWERBI_INTEGRATION.md](POWERBI_INTEGRATION.md) for:
- Step-by-step Power BI setup
- Example R visuals with ggplot2
- Performance optimization
- Troubleshooting guide

## Testing

Run the module directly to test:

```bash
Rscript liquidity_stress_test.R
```

Or in R console:
```r
source("liquidity_stress_test.R")
```

This will:
1. Load all syndicate data
2. Generate dashboard summary
3. Export example analysis files

## Requirements

- R 4.0 or higher
- Required packages:
  - dplyr >= 1.0.0
  - tidyr >= 1.1.0
  - jsonlite >= 1.7.0
  - readr >= 2.0.0
  - openxlsx >= 4.2.0
  - R6 >= 2.5.0
  - ggplot2 >= 3.3.0 (for visualizations)

Install with:
```r
install.packages(c("dplyr", "tidyr", "jsonlite", "readr", "openxlsx", "R6", "ggplot2"))
```

## R6 Class Benefits

This implementation uses R6 for object-oriented programming:

- **State management**: Data persists in the object
- **Method chaining**: Multiple operations on same object
- **Memory efficiency**: Load data once, use multiple times
- **Familiar syntax**: Similar to Python classes

Example:
```r
# Create object
lst <- LiquidityStressTest$new("data")

# Load data (stored in object)
lst$load_data()

# Access methods (use stored data)
capital <- lst$calculate_capital_position_table()
stress <- lst$calculate_stress_impact_table()

# Access stored data directly if needed
head(lst$metadata)
```

## Version History

- **v1.0** (2024-11) - Initial release
  - Capital position calculations
  - Liquidity breakdown analysis
  - Cashflow summaries
  - Stress test impact analysis
  - Excel export functionality
  - Power BI integration functions
  - R6 class implementation
  - ggplot2 visualization examples
