# Power BI Integration Guide for Lloyd's RRA Reporting

This guide explains how to use the Python and R scripts in Power BI for Lloyd's Reserving Return Annual (RRA) reporting.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Using Python Scripts in Power BI](#using-python-scripts-in-power-bi)
5. [Using R Scripts in Power BI](#using-r-scripts-in-power-bi)
6. [Available Forms and Scripts](#available-forms-and-scripts)
7. [Example Power BI Visualizations](#example-power-bi-visualizations)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This repository contains:
- **Synthetic data generators** (Python and R) to create realistic Lloyd's RRA data
- **Form processing scripts** for each RRA form (010, 020, 071, 081, 091, 193, 291, 292, 293, 294, 295, 391, 910, 990)
- **Aggregation utilities** to combine and analyze data across forms
- **Power BI ready scripts** that can be used directly in Power BI Desktop

### Repository Structure

```
Lloyds_Reporting_Dev/
├── python_scripts/
│   ├── data_generation/
│   │   └── generate_synthetic_lloyds_data.py
│   ├── forms/
│   │   ├── rra_010_control.py
│   │   ├── rra_193_net_claims.py
│   │   └── rra_291_gross_premium_ibnr.py
│   └── utils/
│       └── rra_aggregator.py
├── r_scripts/
│   ├── data_generation/
│   │   └── generate_synthetic_lloyds_data.R
│   ├── forms/
│   │   ├── rra_010_control.R
│   │   └── rra_193_net_claims.R
│   └── utils/
│       └── rra_aggregator.R
├── synthetic_data/
│   └── (Generated CSV files)
└── POWER_BI_INTEGRATION_GUIDE.md (this file)
```

---

## Prerequisites

### For Python Scripts

1. **Python 3.8 or higher** installed
2. Required packages (install via `pip install -r requirements.txt`):
   - pandas
   - numpy
   - openpyxl

### For R Scripts

1. **R 4.0 or higher** installed
2. Required packages (install via `install.packages(c("dplyr", "tidyr", "readr", "lubridate"))`):
   - dplyr
   - tidyr
   - readr
   - lubridate

### Power BI Configuration

1. **Power BI Desktop** (latest version)
2. Enable Python/R scripting:
   - Go to **File → Options and settings → Options**
   - Navigate to **Python scripting** or **R scripting**
   - Set the Python/R home directory

---

## Quick Start

### Step 1: Generate Synthetic Data

**Using Python:**
```bash
cd python_scripts/data_generation
python generate_synthetic_lloyds_data.py
```

**Using R:**
```bash
cd r_scripts/data_generation
Rscript generate_synthetic_lloyds_data.R
```

This will create synthetic Lloyd's data in the `synthetic_data/` folder.

### Step 2: Import Data into Power BI

1. Open Power BI Desktop
2. Click **Get Data → Text/CSV**
3. Navigate to the `synthetic_data/` folder
4. Select the CSV files you need (e.g., `rra_010_control.csv`, `rra_193_net_claims.csv`)
5. Click **Load**

### Step 3: Apply Python/R Scripts

See the detailed sections below for applying scripts to specific forms.

---

## Using Python Scripts in Power BI

### Method 1: Python Script Data Source

1. In Power BI, click **Get Data → More → Python script**
2. Enter the following script:

```python
import sys
sys.path.append(r'C:\path\to\Lloyds_Reporting_Dev\python_scripts\forms')

from rra_010_control import process_rra_010

# Process the data
df = process_rra_010(data_source=r'C:\path\to\Lloyds_Reporting_Dev\synthetic_data\rra_010_control.csv')
```

3. Click **OK**
4. Select the `df` table from the Navigator
5. Click **Load**

### Method 2: Transform Existing Data with Python

1. Load your CSV data first (e.g., `rra_193_net_claims.csv`)
2. In the **Power Query Editor**, select the table
3. Click **Transform → Run Python script**
4. Enter the following:

```python
import sys
sys.path.append(r'C:\path\to\Lloyds_Reporting_Dev\python_scripts\forms')

from rra_193_net_claims import process_rra_193
import pandas as pd

# 'dataset' is the input dataframe from Power BI
# Save it to a temporary CSV
dataset.to_csv('temp_input.csv', index=False)

# Process with our function
df = process_rra_193('temp_input.csv')
```

5. Click **OK**
6. Select the output table

### Method 3: Python Visual (for ad-hoc analysis)

1. Add a **Python visual** to your report
2. Drag fields into the Python visual
3. Click the Python editor icon
4. Write your Python code:

```python
import matplotlib.pyplot as plt
import seaborn as sns

# 'dataset' contains the data from the fields you dragged
plt.figure(figsize=(10, 6))
dataset.groupby('Year_of_Account')['Total_Incurred'].sum().plot(kind='bar')
plt.title('Total Incurred by Year of Account')
plt.ylabel('Total Incurred (GBP)')
plt.xlabel('Year of Account')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

---

## Using R Scripts in Power BI

### Method 1: R Script Data Source

1. In Power BI, click **Get Data → More → R script**
2. Enter the following script:

```r
source('C:/path/to/Lloyds_Reporting_Dev/r_scripts/forms/rra_010_control.R')

# Process the data
df <- process_rra_010(data_source = 'C:/path/to/Lloyds_Reporting_Dev/synthetic_data/rra_010_control.csv')
```

3. Click **OK**
4. Select the `df` table
5. Click **Load**

### Method 2: Transform Existing Data with R

1. Load your CSV data first
2. In the **Power Query Editor**, select the table
3. Click **Transform → Run R script**
4. Enter the following:

```r
source('C:/path/to/Lloyds_Reporting_Dev/r_scripts/forms/rra_193_net_claims.R')

# 'dataset' is the input dataframe from Power BI
df <- process_rra_193_from_dataframe(dataset)
```

5. Click **OK**

### Method 3: R Visual (for ad-hoc visualizations)

1. Add an **R visual** to your report
2. Drag fields into the R visual
3. Click the R editor icon
4. Write your R code:

```r
library(ggplot2)

# 'dataset' contains the data from the fields you dragged
ggplot(dataset, aes(x = Year_of_Account, y = Total_Incurred)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  theme_minimal() +
  labs(title = "Total Incurred by Year of Account",
       x = "Year of Account",
       y = "Total Incurred (GBP)") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
```

---

## Available Forms and Scripts

### RRA 010 - Control Data

**Python:** `python_scripts/forms/rra_010_control.py`
**R:** `r_scripts/forms/rra_010_control.R`

**Functions:**
- `process_rra_010()` - Process control data
- `get_control_summary()` - Get summary statistics
- `validate_rra_010()` - Validate data quality

**Use case:** Syndicate metadata, submission tracking

### RRA 193 - Net Claims Development

**Python:** `python_scripts/forms/rra_193_net_claims.py`
**R:** `r_scripts/forms/rra_193_net_claims.R`

**Functions:**
- `process_rra_193()` - Process claims triangles
- `create_development_triangle()` - Create development triangles
- `calculate_chain_ladder()` - Calculate chain ladder factors
- `get_claims_summary_by_yoa()` - YoA summary
- `get_claims_summary_by_lob()` - LOB summary

**Use case:** Claims development analysis, reserve adequacy

### RRA 291 - Gross Premium and IBNR

**Python:** `python_scripts/forms/rra_291_gross_premium_ibnr.py`

**Functions:**
- `process_rra_291()` - Process gross premium and IBNR
- `get_ibnr_summary_by_yoa()` - IBNR by year
- `get_ibnr_summary_by_lob()` - IBNR by line of business
- `get_ibnr_range_analysis()` - Analyze IBNR uncertainty
- `get_ultimate_loss_ratio_trend()` - Loss ratio trends

**Use case:** IBNR estimation, loss ratio analysis

### RRA Aggregator (All Forms)

**Python:** `python_scripts/utils/rra_aggregator.py`
**R:** `r_scripts/utils/rra_aggregator.R`

**Functions:**
- `load_all_forms()` / `rra_load_all_forms()` - Load all RRA data
- `get_portfolio_summary()` - Overall portfolio metrics
- `get_syndicate_profile()` - Individual syndicate analysis
- `get_lob_analysis()` - Line of business performance
- `get_reserve_adequacy_indicators()` - Reserve health metrics

**Use case:** Executive dashboards, portfolio oversight

---

## Example Power BI Visualizations

### Example 1: Executive Dashboard

**Data Source:** Use the aggregator to load all forms

**Python Script:**
```python
import sys
sys.path.append(r'C:\path\to\Lloyds_Reporting_Dev\python_scripts\utils')

from rra_aggregator import RRADataAggregator

aggregator = RRADataAggregator(output_dir=r'C:\path\to\Lloyds_Reporting_Dev\synthetic_data')
aggregator.load_all_forms()

# Get portfolio summary
df = aggregator.get_portfolio_summary()
```

**Visualizations:**
- Card visual: Total Capacity
- Card visual: Total IBNR
- Bar chart: Gross Written Premium by LOB
- Line chart: Loss Ratio trend by Year of Account

### Example 2: Claims Development Triangle

**Data Source:** RRA 193

**Python Script:**
```python
from rra_193_net_claims import create_development_triangle

# Create triangle for a specific syndicate and LOB
df = create_development_triangle(
    data_source=r'C:\path\to\synthetic_data\rra_193_net_claims.csv',
    metric='Total_Incurred',
    syndicate=2987,
    lob_code='M1'
)
```

**Visualization:**
- Matrix visual showing development triangle
- Heatmap for development factors

### Example 3: Reserve Adequacy Monitoring

**Data Source:** Multiple forms via aggregator

**R Script:**
```r
source('C:/path/to/r_scripts/utils/rra_aggregator.R')

forms <- rra_load_all_forms('C:/path/to/synthetic_data')
df <- get_reserve_adequacy_indicators(forms)
```

**Visualizations:**
- Gauge visuals for key ratios
- Trend lines for IBNR to Premium ratio
- Scatter plot: Claims maturity vs Paid Ratio

---

## Troubleshooting

### Issue: "Python/R script error"

**Solution:**
1. Check that Python/R is correctly configured in Power BI Options
2. Verify the path to your scripts is correct
3. Ensure all required packages are installed

### Issue: "Module not found"

**Solution:**
1. Check that `sys.path.append()` points to the correct directory
2. Verify Python/R packages are installed in the correct environment
3. In Power BI Options, ensure the Python/R home directory is set correctly

### Issue: "File not found"

**Solution:**
1. Use absolute paths (e.g., `C:\path\to\file.csv`) instead of relative paths
2. Check that synthetic data has been generated
3. Verify file permissions

### Issue: "Data refresh fails"

**Solution:**
1. Python/R scripts don't support scheduled refresh in Power BI Service by default
2. Consider using Power BI Dataflows or Azure Functions for automated refresh
3. For on-premise refresh, use Power BI Gateway with Python/R configured

### Issue: "Performance is slow"

**Solution:**
1. Load only necessary columns from CSV files
2. Use Power Query to filter data before applying Python/R scripts
3. Consider pre-processing large datasets and saving results
4. Use DirectQuery instead of Import mode for very large datasets

---

## Best Practices

1. **Version Control:** Keep scripts in version control (Git)
2. **Documentation:** Comment your code extensively
3. **Error Handling:** Add try-catch blocks in production scripts
4. **Performance:** Filter data in Power Query before applying scripts
5. **Modularity:** Use functions for reusable logic
6. **Testing:** Test scripts with sample data before deploying to Power BI
7. **Security:** Don't hardcode credentials; use parameters
8. **Refresh:** Be aware of Power BI Service limitations with Python/R

---

## Next Steps

1. Generate your synthetic data
2. Import data into Power BI
3. Create your first dashboard using the control form
4. Explore claims development triangles
5. Build reserve adequacy monitoring reports
6. Customize scripts for your specific needs

---

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the script documentation
- Consult the Lloyd's RRA reporting specifications

---

## License

This code is provided as-is for Lloyd's RRA reporting purposes.

---

**Document Version:** 1.0
**Last Updated:** 2024-11-21
