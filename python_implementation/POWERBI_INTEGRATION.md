# Power BI Integration Guide - Python

This guide explains how to use the Lloyd's Liquidity Stress Test Python scripts in Power BI.

## Prerequisites

1. **Enable Python in Power BI Desktop**
   - Go to File → Options and settings → Options
   - Navigate to Python scripting
   - Set your Python installation directory
   - Ensure pandas is installed: `pip install pandas openpyxl`

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

### Step 2: Create Python Visual

1. Add a Python visual to your report canvas
2. Drag fields from your imported tables into the visual's "Values" field well
3. Click the Python script editor

### Step 3: Use the Functions

#### Example 1: Capital Position Dashboard

```python
# Use the 'dataset' variable that Power BI provides
import pandas as pd
import sys
sys.path.append('path/to/Lloyds_Reporting_Dev/python_implementation')

from liquidity_stress_test import get_capital_position

# Process the data
result = get_capital_position(dataset)

# Create visualization
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.barh(result['syndicate_name'], result['solvency_ratio'])
plt.xlabel('Solvency Ratio')
plt.title('Syndicate Solvency Ratios')
plt.axvline(x=1.0, color='r', linestyle='--', label='Minimum Required')
plt.legend()
plt.tight_layout()
plt.show()
```

#### Example 2: Liquidity Breakdown

```python
import pandas as pd
import sys
sys.path.append('path/to/Lloyds_Reporting_Dev/python_implementation')

from liquidity_stress_test import get_liquidity_breakdown

# Process the data
result = get_liquidity_breakdown(dataset)

# Filter to most recent date
recent = result[result['date'] == result['date'].max()]

# Create stacked bar chart
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 6))

syndicates = recent['syndicate_number'].unique()
x = range(len(syndicates))

ax.bar(x, recent['restricted_pct'], label='Restricted Assets')
ax.bar(x, recent['illiquid_pct'], bottom=recent['restricted_pct'], label='Illiquid Assets')
ax.bar(x, recent['liquid_pct'], bottom=recent['restricted_pct'] + recent['illiquid_pct'], label='Liquid Assets')

ax.set_xticks(x)
ax.set_xticklabels(syndicates)
ax.set_ylabel('Percentage (%)')
ax.set_title('Asset Composition by Syndicate')
ax.legend()
plt.tight_layout()
plt.show()
```

#### Example 3: Stress Test Analysis

```python
import pandas as pd
import sys
sys.path.append('path/to/Lloyds_Reporting_Dev/python_implementation')

from liquidity_stress_test import LiquidityStressTest

# Initialize
lst = LiquidityStressTest('path/to/data')
lst.load_data()

# Get stress impact
stress_impact = lst.calculate_stress_impact_table()

# Filter for specific syndicate
synd_2001 = stress_impact[stress_impact['syndicate_number'] == 2001]

# Plot baseline vs stressed liquidity
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(synd_2001['date'], synd_2001['closing_free_funds'], marker='o', label='Baseline')
plt.plot(synd_2001['date'], synd_2001['stressed_closing_funds'], marker='s', label='Stressed')
plt.axhline(y=0, color='r', linestyle='--', label='Zero Liquidity')
plt.xlabel('Date')
plt.ylabel('Free Funds (£)')
plt.title('Liquidity Position - Baseline vs Stress Scenario')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## Method 2: Run Python Script in Power Query

1. Go to "Transform Data" → "Get Data" → "Other" → "Blank Query"
2. Open Advanced Editor
3. Use this template:

```python
let
    Source = Python.Execute(
        "import pandas as pd#(lf)" &
        "import sys#(lf)" &
        "sys.path.append('path/to/Lloyds_Reporting_Dev/python_implementation')#(lf)" &
        "#(lf)" &
        "from liquidity_stress_test import LiquidityStressTest#(lf)" &
        "#(lf)" &
        "lst = LiquidityStressTest('path/to/data')#(lf)" &
        "lst.load_data()#(lf)" &
        "summary = lst.create_dashboard_summary()#(lf)"
    ),
    summary = Source{[Name="summary"]}[Value]
in
    summary
```

## Method 3: Create Custom Python Tables

Create calculated tables using Python:

1. Click "Modeling" → "New Table"
2. Use DAX to define a calculated table
3. Or use "New Table (Python)" if available

## Tips for Best Performance

1. **Pre-process Data**: Run the Python scripts once to create the output tables, then import the results as CSV
2. **Use Filters**: Apply syndicate or date filters before running Python scripts
3. **Cache Results**: Store processed data in Power BI tables rather than re-running scripts
4. **Incremental Refresh**: Set up incremental refresh for large datasets

## Common Issues

### Issue: Module not found
**Solution**: Ensure the path to the Python implementation folder is correct in `sys.path.append()`

### Issue: Slow performance
**Solution**: Pre-calculate the tables and import them as CSV files instead of running Python scripts on the fly

### Issue: Python visual not showing
**Solution**:
- Check Python installation in Options
- Verify pandas is installed
- Check for errors in the Python script editor

## Example Dashboard Layout

Recommended visuals for a complete dashboard:

1. **Executive Summary** (Card visuals)
   - Total FAL across all syndicates
   - Average solvency ratio
   - Number of syndicates passing stress test

2. **Capital Position** (Python visual - bar chart)
   - Solvency ratios by syndicate

3. **Liquidity Breakdown** (Python visual - stacked bar)
   - Asset composition by type

4. **Stress Impact** (Python visual - line chart)
   - Baseline vs stressed liquidity over time

5. **Risk Metrics** (Table visual)
   - Detailed metrics from dashboard summary

## Advanced: Create Power BI Dataset

For repeated use, create a dedicated Power BI dataset:

1. Run the Python script to generate all output tables
2. Import all CSVs into Power BI
3. Create relationships between tables
4. Publish to Power BI Service
5. Set up scheduled refresh

This allows multiple reports to use the same processed data without re-running Python scripts.
