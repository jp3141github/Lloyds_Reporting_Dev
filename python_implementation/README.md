# Python Implementation - Lloyd's Liquidity Stress Test

This folder contains the Python implementation for processing Lloyd's Liquidity Stress Test data for Power BI integration.

## Files

- `liquidity_stress_test.py` - Main Python module with all analysis functions
- `POWERBI_INTEGRATION.md` - Detailed guide for using in Power BI
- `syndicate_2001_analysis.xlsx` - Example output for Syndicate 2001
- `all_syndicates_analysis.xlsx` - Example output for all syndicates

## Quick Start

### 1. Install Dependencies

```bash
pip install pandas openpyxl numpy
```

### 2. Run Standalone

```bash
cd ..  # Go to repository root
python3 python_implementation/liquidity_stress_test.py
```

### 3. Import as Module

```python
import sys
sys.path.append('path/to/python_implementation')

from liquidity_stress_test import LiquidityStressTest

# Initialize
lst = LiquidityStressTest('path/to/data')
lst.load_data()

# Get all output tables
tables = lst.calculate_rra_output_tables()

# Generate dashboard
summary = lst.create_dashboard_summary()
print(summary)
```

## Main Class: LiquidityStressTest

### Initialization

```python
lst = LiquidityStressTest(data_path='../data')
```

**Parameters:**
- `data_path` (str): Path to directory containing syndicate data

### Methods

#### load_data(syndicate_number=None)
Load syndicate data from CSV files.

**Parameters:**
- `syndicate_number` (int, optional): Load specific syndicate. If None, loads all.

**Returns:**
- dict: Dictionary containing loaded dataframes

**Example:**
```python
# Load all syndicates
lst.load_data()

# Load specific syndicate
data = lst.load_data(syndicate_number=2001)
```

#### calculate_capital_position_table(syndicate_number=None)
Generate capital position summary.

**Returns:**
- pd.DataFrame: Capital position with FAL, FIS, uSCR, uECA, ratios

**Example:**
```python
capital = lst.calculate_capital_position_table()
print(capital[['syndicate_name', 'solvency_ratio']])
```

#### calculate_liquidity_breakdown_table(syndicate_number=None, date=None)
Generate asset and liquidity breakdown.

**Parameters:**
- `syndicate_number` (int, optional): Filter by syndicate
- `date` (str, optional): Filter by date (YYYY-MM-DD)

**Returns:**
- pd.DataFrame: Liquidity breakdown by asset type

**Example:**
```python
liquidity = lst.calculate_liquidity_breakdown_table(date='2024-12-31')
print(liquidity[['syndicate_number', 'liquid_pct', 'illiquid_pct']])
```

#### calculate_cashflow_summary_table(syndicate_number=None)
Generate cashflow summary.

**Returns:**
- pd.DataFrame: Cashflow details with cumulative totals

**Example:**
```python
cashflow = lst.calculate_cashflow_summary_table(syndicate_number=2001)
print(cashflow[['date', 'closing_free_funds', 'total_movements']])
```

#### calculate_stress_impact_table(syndicate_number=None)
Generate stress test impact analysis.

**Returns:**
- pd.DataFrame: Baseline vs stressed scenarios

**Example:**
```python
stress = lst.calculate_stress_impact_table()
print(stress[['syndicate_number', 'date', 'liquidity_gap', 'stressed_closing_funds']])
```

#### create_dashboard_summary(syndicate_number=None)
Create executive dashboard summary.

**Returns:**
- pd.DataFrame: High-level metrics and stress test results

**Example:**
```python
summary = lst.create_dashboard_summary()
print(summary[['syndicate_name', 'solvency_ratio', 'stress_test_pass']])
```

#### export_to_excel(output_path, syndicate_number=None)
Export all tables to Excel workbook.

**Parameters:**
- `output_path` (str): Path for output Excel file
- `syndicate_number` (int, optional): Filter by syndicate

**Example:**
```python
lst.export_to_excel('my_analysis.xlsx', syndicate_number=2001)
```

## Power BI Functions

These wrapper functions are designed for use directly in Power BI Python visuals.

### get_capital_position(dataset)

```python
from liquidity_stress_test import get_capital_position

# In Power BI, 'dataset' is automatically provided
result = get_capital_position(dataset)
```

### get_liquidity_breakdown(dataset)

```python
from liquidity_stress_test import get_liquidity_breakdown

result = get_liquidity_breakdown(dataset)
```

### get_stress_impact(cashflow_dataset, stress_dataset)

```python
from liquidity_stress_test import get_stress_impact

result = get_stress_impact(cashflow_dataset, stress_dataset)
```

## Example Workflows

### 1. Generate All RRA Tables

```python
from liquidity_stress_test import LiquidityStressTest

lst = LiquidityStressTest('../data')
lst.load_data()

# Get all tables
tables = lst.calculate_rra_output_tables()

# Access individual tables
capital = tables['capital_position']
liquidity = tables['liquidity_breakdown']
cashflow = tables['cashflow_summary']
stress = tables['stress_impact']

# Save each table
capital.to_csv('capital_position.csv', index=False)
liquidity.to_csv('liquidity_breakdown.csv', index=False)
cashflow.to_csv('cashflow_summary.csv', index=False)
stress.to_csv('stress_impact.csv', index=False)
```

### 2. Analyze Single Syndicate

```python
from liquidity_stress_test import LiquidityStressTest

lst = LiquidityStressTest('../data')

# Load specific syndicate
data = lst.load_data(syndicate_number=2001)

# Generate analysis
capital = lst.calculate_capital_position_table(syndicate_number=2001)
stress = lst.calculate_stress_impact_table(syndicate_number=2001)

# Check stress test result
min_liquidity = stress['stressed_closing_funds'].min()
if min_liquidity > 0:
    print("✓ Stress test PASSED")
else:
    print("✗ Stress test FAILED - liquidity shortfall detected")
```

### 3. Compare All Syndicates

```python
from liquidity_stress_test import LiquidityStressTest
import matplotlib.pyplot as plt

lst = LiquidityStressTest('../data')
lst.load_data()

summary = lst.create_dashboard_summary()

# Plot solvency ratios
plt.figure(figsize=(12, 6))
plt.barh(summary['syndicate_name'], summary['solvency_ratio'])
plt.axvline(x=1.0, color='r', linestyle='--', label='Minimum')
plt.xlabel('Solvency Ratio')
plt.title('Syndicate Solvency Comparison')
plt.legend()
plt.tight_layout()
plt.savefig('solvency_comparison.png')
```

### 4. Export Comprehensive Report

```python
from liquidity_stress_test import LiquidityStressTest

lst = LiquidityStressTest('../data')
lst.load_data()

# Export for each syndicate
for synd_num in lst.metadata['syndicate_number'].unique():
    lst.export_to_excel(
        f'syndicate_{synd_num}_report.xlsx',
        syndicate_number=synd_num
    )

# Export combined report
lst.export_to_excel('all_syndicates_report.xlsx')
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

All methods return pandas DataFrames with consistent column naming:
- Snake_case for column names
- Currency values as integers (GBP)
- Ratios as floats
- Dates as strings (YYYY-MM-DD)

## Performance Tips

1. **Load data once**: Call `load_data()` once and reuse the object
2. **Filter early**: Use syndicate_number parameter to reduce data size
3. **Cache results**: Save processed tables to CSV for repeated use
4. **Use chunking**: For very large datasets, process in chunks

```python
# Good - load once
lst = LiquidityStressTest('../data')
lst.load_data()
table1 = lst.calculate_capital_position_table()
table2 = lst.calculate_stress_impact_table()

# Less efficient - loads data twice
lst1 = LiquidityStressTest('../data')
table1 = lst1.calculate_capital_position_table()

lst2 = LiquidityStressTest('../data')
table2 = lst2.calculate_stress_impact_table()
```

## Error Handling

The module includes basic error handling:

```python
try:
    lst = LiquidityStressTest('../data')
    lst.load_data()
except FileNotFoundError as e:
    print(f"Data files not found: {e}")
except Exception as e:
    print(f"Error processing data: {e}")
```

## Integration with Power BI

See [POWERBI_INTEGRATION.md](POWERBI_INTEGRATION.md) for:
- Step-by-step Power BI setup
- Example Python visuals
- Performance optimization
- Troubleshooting guide

## Testing

Run the module directly to test:

```bash
python3 liquidity_stress_test.py
```

This will:
1. Load all syndicate data
2. Generate dashboard summary
3. Export example analysis files

## Requirements

- Python 3.7 or higher
- pandas >= 1.3.0
- openpyxl >= 3.0.0
- numpy >= 1.20.0

Install with:
```bash
pip install pandas>=1.3.0 openpyxl>=3.0.0 numpy>=1.20.0
```

## Version History

- **v1.0** (2024-11) - Initial release
  - Capital position calculations
  - Liquidity breakdown analysis
  - Cashflow summaries
  - Stress test impact analysis
  - Excel export functionality
  - Power BI integration functions
