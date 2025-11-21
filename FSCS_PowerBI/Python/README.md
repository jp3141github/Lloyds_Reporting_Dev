# Python Implementation - FSCS Data Generator

This directory contains the Python implementation of the FSCS data generator for Lloyd's syndicates.

## Files

- **`fscs_data_generator.py`**: Core data generation module with FSCSDataGenerator class
- **`powerbi_query.py`**: Self-contained script for Power BI Python data source
- **`example_usage.py`**: Comprehensive examples demonstrating all features
- **`requirements.txt`**: Python package dependencies

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computing
- `openpyxl`: Excel file handling

## Usage

### 1. Basic Usage - Summary Data

```python
from fscs_data_generator import get_fscs_summary_data

# Generate FSCS summary data for 10 syndicates
summary = get_fscs_summary_data(num_syndicates=10, reporting_year=2024)
print(summary)
```

### 2. Generate Detailed Transaction Data

```python
from fscs_data_generator import get_fscs_detail_data

# Generate detailed transaction-level data
detail = get_fscs_detail_data(num_syndicates=10, reporting_year=2024)
print(f"Generated {len(detail)} transactions")
print(detail.head())
```

### 3. Using the Generator Class

```python
from fscs_data_generator import FSCSDataGenerator

# Create generator instance
generator = FSCSDataGenerator(
    num_syndicates=15,
    reporting_year=2024,
    random_seed=42  # For reproducibility
)

# Generate different data formats
fscs_output = generator.generate_fscs_output_format()
full_data = generator.generate_full_dataset()
detail_data = generator.generate_detail_dataset()
```

### 4. Export to Excel

```python
from fscs_data_generator import FSCSDataGenerator
import pandas as pd

generator = FSCSDataGenerator(num_syndicates=10, reporting_year=2024)

# Generate all data types
summary = generator.generate_fscs_output_format()
detail = generator.generate_detail_dataset()
full = generator.generate_full_dataset()

# Export to Excel with multiple sheets
with pd.ExcelWriter('FSCS_Data.xlsx', engine='openpyxl') as writer:
    summary.to_excel(writer, sheet_name='FSCS_Summary', index=False)
    detail.to_excel(writer, sheet_name='Transactions', index=False)
    full.to_excel(writer, sheet_name='Full_Data', index=False)
```

## Power BI Integration

### Method 1: Using powerbi_query.py (Recommended)

1. Open Power BI Desktop
2. Go to **Home** > **Get Data** > **More**
3. Search for and select **Python script**
4. Click **Connect**
5. Copy the entire contents of `powerbi_query.py`
6. Paste into the script window
7. Click **OK**
8. Select the `dataset` table in the navigator
9. Click **Load**

### Method 2: Custom Query

If you want more control, create your own Power BI query:

```python
import pandas as pd
import numpy as np
from datetime import date
import random

# Copy the generate_fscs_data function from powerbi_query.py
# Or import from fscs_data_generator if it's in your Python path

# Generate data
dataset = generate_fscs_data(num_syndicates=15, reporting_year=2024)

# dataset will be automatically loaded into Power BI
```

### Power BI Configuration

Before using Python scripts in Power BI:

1. **Install Python**: Ensure Python 3.8+ is installed
2. **Configure Power BI**:
   - File > Options and settings > Options
   - Python scripting section
   - Set Python home directory (e.g., `C:\Python311`)
3. **Install packages**: Run `pip install pandas numpy openpyxl`
4. **Restart Power BI** after configuration

## API Reference

### FSCSDataGenerator Class

```python
class FSCSDataGenerator:
    """
    Generates synthetic Lloyd's syndicate data for FSCS reporting.

    Parameters
    ----------
    num_syndicates : int, default=10
        Number of syndicates to generate data for
    reporting_year : int, default=2024
        Year for which the data is being reported
    random_seed : int, default=42
        Seed for reproducibility
    """
```

#### Methods

##### `generate_syndicate_numbers()`
Returns a list of realistic Lloyd's syndicate numbers (4-digit numbers in range 2000-6000).

##### `generate_gross_written_premium(business_type='general')`
Generates GWP values for specified business type.

**Parameters:**
- `business_type`: 'general' or 'life'

**Returns:** numpy.array of premium values

##### `generate_best_estimate_liabilities(gwp_values, business_type='general')`
Generates BEL values correlated with GWP.

**Parameters:**
- `gwp_values`: Array of GWP values
- `business_type`: 'general' or 'life'

**Returns:** numpy.array of liability values

##### `generate_full_dataset()`
Generates complete dataset with all fields and calculated columns.

**Returns:** pandas.DataFrame

##### `generate_fscs_output_format()`
Generates data in exact FSCS submission format.

**Returns:** pandas.DataFrame

##### `generate_detail_dataset()`
Generates detailed transaction-level data (50-200 contracts per syndicate).

**Returns:** pandas.DataFrame

### Convenience Functions

```python
def get_fscs_summary_data(num_syndicates=10, reporting_year=2024):
    """Generate FSCS summary data."""

def get_fscs_detail_data(num_syndicates=10, reporting_year=2024):
    """Generate detailed transaction data."""
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
python example_usage.py
```

This will:
1. Generate summary data
2. Generate detailed transaction data
3. Demonstrate generator class usage
4. Create multi-year datasets
5. Export to Excel
6. Display summary statistics

## Common Issues

### ImportError: No module named 'pandas'

**Solution**: Install dependencies with `pip install -r requirements.txt`

### Power BI can't find Python

**Solution**:
1. Verify Python is installed: `python --version`
2. Configure Python path in Power BI Options
3. Use full path to Python executable

### Data values seem unrealistic

**Solution**:
- Adjust parameters in the generator
- Modify distribution parameters in the generation functions
- Use different random_seed values

### Unicode/Encoding Errors

**Solution**:
```python
# Add at top of script
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

## Performance

- **Summary data** (10 syndicates): < 1 second
- **Detail data** (10 syndicates, ~1000 contracts): < 2 seconds
- **Excel export** (10 syndicates): < 5 seconds

For larger datasets:
- 100 syndicates: ~10 seconds
- 1000 syndicates: ~2 minutes

## Customization Examples

### Adjust Premium Ranges

```python
# Edit in fscs_data_generator.py
def generate_gross_written_premium(self, business_type='general'):
    if business_type == 'general':
        min_value = 5_000_000    # Lower minimum
        max_value = 1_000_000_000  # Higher maximum
        mean = 200_000_000        # Higher mean
```

### Change BEL Multipliers

```python
# Edit in fscs_data_generator.py
def generate_best_estimate_liabilities(self, gwp_values, business_type='general'):
    if business_type == 'general':
        multiplier = np.random.uniform(2.0, 4.0, self.num_syndicates)  # Higher range
```

### Add Custom Fields

```python
generator = FSCSDataGenerator(num_syndicates=10)
df = generator.generate_full_dataset()

# Add custom fields
df['year_of_account'] = 2024
df['stamp_capacity'] = df['gwp_total'] * 1.2
df['risk_rating'] = np.random.choice(['A', 'B', 'C'], len(df))
```

## Best Practices

1. **Use consistent random seeds** for reproducible results
2. **Validate data** before using in reports
3. **Document assumptions** when sharing with others
4. **Export to Excel** for easy sharing and review
5. **Test with small datasets** first (5-10 syndicates)

## Integration with Other Tools

### Jupyter Notebooks

```python
# In Jupyter cell
from fscs_data_generator import FSCSDataGenerator
import matplotlib.pyplot as plt

generator = FSCSDataGenerator(num_syndicates=20)
df = generator.generate_full_dataset()

# Visualize
df.plot(x='syndicate_number', y=['gwp_general_business', 'gwp_life_business'],
        kind='bar', figsize=(12, 6))
plt.title('GWP by Syndicate')
plt.show()
```

### Streamlit Dashboard

```python
import streamlit as st
from fscs_data_generator import get_fscs_summary_data

st.title('FSCS Data Generator')

num_syndicates = st.slider('Number of Syndicates', 5, 50, 10)
year = st.selectbox('Reporting Year', [2022, 2023, 2024])

if st.button('Generate Data'):
    data = get_fscs_summary_data(num_syndicates, year)
    st.dataframe(data)
```

## Version Compatibility

- **Python 3.8**: Minimum version
- **Python 3.9-3.11**: Fully tested
- **Python 3.12**: Compatible (recommended)

## Support

For Python-specific issues:
1. Check requirements.txt versions
2. Verify pandas/numpy installation
3. Review example_usage.py for correct usage patterns
4. Test with standalone Python before Power BI integration

---

**Next Steps**: After testing the Python implementation, refer to the main README for Power BI integration instructions.
