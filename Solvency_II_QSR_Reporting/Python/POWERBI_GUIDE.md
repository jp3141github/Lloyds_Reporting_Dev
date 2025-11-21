# Power BI Integration Guide - Python QSR Reports

This guide explains how to use the Python QSR report scripts in Power BI.

## Prerequisites

1. **Python Installation**: Ensure Python 3.8+ is installed on your system
2. **Required Packages**: Install the following packages:
   ```bash
   pip install pandas numpy openpyxl
   ```
3. **Power BI Desktop**: Ensure Python scripting is enabled in Power BI Desktop

## Setup in Power BI

### 1. Configure Python in Power BI

1. Open Power BI Desktop
2. Go to **File > Options and settings > Options**
3. Select **Python scripting** under Global
4. Set your Python installation directory
5. Click OK

### 2. Generate Synthetic Data (One-Time Setup)

Before using the reports in Power BI, generate the synthetic data:

```bash
cd Solvency_II_QSR_Reporting/Python
python synthetic_data_generator.py
```

This will create CSV files in the `Data` folder:
- `synthetic_balance_sheet.csv`
- `synthetic_own_funds.csv`
- `synthetic_technical_provisions.csv`
- `synthetic_premiums_claims.csv`
- `synthetic_investments.csv`
- `synthetic_scr_calculation.csv`
- `synthetic_mcr_calculation.csv`

## Using Python Scripts in Power BI

### Method 1: Import Data Using Python Script

1. In Power BI Desktop, click **Get Data**
2. Select **More... > Other > Python script**
3. Click **Connect**
4. Paste one of the following scripts:

#### Example: Load Balance Sheet (QSR 002)

```python
import sys
sys.path.append(r'C:\path\to\Solvency_II_QSR_Reporting\Python')

from qsr_report_generator import QSRReportGenerator

generator = QSRReportGenerator(data_dir=r'C:\path\to\Solvency_II_QSR_Reporting\Data/')
generator.load_data()
dataset = generator.generate_qsr002_balance_sheet()
```

#### Example: Load Own Funds (QSR 220)

```python
import sys
sys.path.append(r'C:\path\to\Solvency_II_QSR_Reporting\Python')

from qsr_report_generator import get_own_funds

dataset = get_own_funds()
```

#### Example: Load Solvency Ratios

```python
import sys
sys.path.append(r'C:\path\to\Solvency_II_QSR_Reporting\Python')

from qsr_report_generator import get_solvency_ratios

dataset = get_solvency_ratios()
```

5. Click **OK**
6. Power BI will execute the script and show available datasets
7. Select the dataset and click **Load**

### Method 2: Transform Data Using Python Script

1. Load your raw data into Power BI (from CSV or database)
2. Select the table in **Query Editor**
3. Go to **Transform > Run Python script**
4. Add transformation logic:

```python
import sys
sys.path.append(r'C:\path\to\Solvency_II_QSR_Reporting\Python')

from qsr_report_generator import QSRReportGenerator

# Assuming 'dataset' contains your data
# Transform it to QSR format
generator = QSRReportGenerator(data_dir=r'C:\path\to\Solvency_II_QSR_Reporting\Data/')
generator.load_data()
dataset = generator.generate_qsr002_balance_sheet()
```

## Available Reports

### QSR 002 - Balance Sheet
```python
from qsr_report_generator import get_balance_sheet
dataset = get_balance_sheet()
```

### QSR 220 - Own Funds
```python
from qsr_report_generator import get_own_funds
dataset = get_own_funds()
```

### QSR 240 - Technical Provisions
```python
from qsr_report_generator import get_technical_provisions
dataset = get_technical_provisions()
```

### QSR 440 - Premiums and Claims
```python
from qsr_report_generator import get_premiums_claims
dataset = get_premiums_claims()
```

### Solvency Ratios Summary
```python
from qsr_report_generator import get_solvency_ratios
dataset = get_solvency_ratios()
```

## Sample Power BI Workflow

### Step 1: Load All QSR Reports

Create separate queries for each report:

1. **Balance Sheet Query**
   - Get Data > Python script
   - Use `get_balance_sheet()` function
   - Name: "QSR_002_Balance_Sheet"

2. **Own Funds Query**
   - Get Data > Python script
   - Use `get_own_funds()` function
   - Name: "QSR_220_Own_Funds"

3. **Solvency Ratios Query**
   - Get Data > Python script
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

### Step 4: Add Slicers

Add slicers for:
- Syndicate selection
- Reporting date
- Line of business
- Risk module

## Refreshing Data

### Manual Refresh
1. Click **Refresh** in Power BI Desktop
2. The Python scripts will re-execute and reload data

### Scheduled Refresh (Power BI Service)
1. Publish report to Power BI Service
2. Configure gateway with Python runtime
3. Set up scheduled refresh

## Troubleshooting

### Issue: "Python script error"
- **Solution**: Check Python path in Power BI options
- Verify all packages are installed: `pip list`

### Issue: "Module not found"
- **Solution**: Ensure the path in `sys.path.append()` is correct
- Use absolute paths with `r'...'` prefix

### Issue: "Data not loading"
- **Solution**: Run `synthetic_data_generator.py` first to create data files
- Check that CSV files exist in the Data directory

### Issue: "Encoding errors"
- **Solution**: Ensure CSV files are UTF-8 encoded
- Use `encoding='utf-8'` when reading CSVs

## Best Practices

1. **Use Absolute Paths**: Always use absolute paths for data directories
2. **Cache Data**: Store processed data to avoid re-running generators
3. **Separate Queries**: Create separate queries for each report type
4. **Incremental Refresh**: For large datasets, use Power BI incremental refresh
5. **Error Handling**: Add try-except blocks in Python scripts
6. **Documentation**: Document any custom transformations

## Example Dashboard Measures (DAX)

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

## Support

For issues or questions:
1. Check Python script logs
2. Verify data file formats
3. Review Power BI Python integration documentation
4. Test scripts independently before using in Power BI

---

**Note**: This implementation uses synthetic data. Replace the data source with your actual Lloyd's syndicate data by modifying the data loading functions in `qsr_report_generator.py`.
