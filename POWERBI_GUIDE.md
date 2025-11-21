# Power BI Integration Guide

This guide provides step-by-step instructions for integrating the Solvency II claims processing scripts into Power BI.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Loading Data with Python](#loading-data-with-python)
3. [Loading Data with R](#loading-data-with-r)
4. [Creating Visualizations](#creating-visualizations)
5. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- Power BI Desktop (latest version)
- Python 3.8+ or R 4.0+
- Internet connection for package installation

### Python Setup
1. Install Python from [python.org](https://python.org)
2. Install required packages:
   ```bash
   pip install pandas openpyxl numpy
   ```
3. Configure Python in Power BI:
   - File → Options and settings → Options
   - Python scripting → Set Python home directory
   - Browse to your Python installation

### R Setup
1. Install R from [r-project.org](https://www.r-project.org/)
2. Install RStudio (optional but recommended)
3. Install required packages:
   ```r
   install.packages(c("readxl", "dplyr", "tidyr", "openxlsx"))
   ```
4. Configure R in Power BI:
   - File → Options and settings → Options
   - R scripting → Set R home directory
   - Browse to your R installation

## Loading Data with Python

### Method 1: Using Python Script to Load Data

1. Open Power BI Desktop
2. Click **Get Data** → **More**
3. Search for and select **Python script**
4. Click **Connect**
5. Paste the following script:

```python
import sys
sys.path.append(r'C:\path\to\Lloyds_Reporting_Dev\python_scripts')

from solvency_claims_processor import process_claims_data

# Load and process the data
input_file = r'C:\path\to\synthetic_lloyds_claims_data.xlsx'
output_tables = process_claims_data(input_file, sheet_name='input Sheet')

# Make tables available to Power BI
detailed_claims = output_tables['detailed_claims']
by_syndicate = output_tables['by_syndicate']
by_risk_code = output_tables['by_risk_code']
by_claim_status = output_tables['by_claim_status']
summary = output_tables['summary']
```

6. Click **OK**
7. Select which tables you want to load into Power BI
8. Click **Load**

### Method 2: Using Python for Data Transformation

1. Load your Excel file normally:
   - Get Data → Excel → Select your file
2. In Power Query Editor, select the claims data table
3. Click **Transform** → **Run Python Script**
4. Paste this script:

```python
import sys
sys.path.append(r'C:\path\to\Lloyds_Reporting_Dev\python_scripts')

from solvency_claims_processor import powerbi_transform

# Transform the dataset
dataset = powerbi_transform(dataset)
```

5. Click **OK**
6. Select the transformed table
7. Click **Close & Apply**

## Loading Data with R

### Method 1: Using R Script to Load Data

1. Open Power BI Desktop
2. Click **Get Data** → **More**
3. Search for and select **R script**
4. Click **Connect**
5. Paste the following script:

```r
# Set working directory
setwd('C:/path/to/Lloyds_Reporting_Dev')

# Source the R script
source('r_scripts/solvency_claims_processor.R')

# Load and process the data
input_file <- 'synthetic_data/synthetic_lloyds_claims_data.xlsx'
output_tables <- process_claims_data(input_file)

# Make tables available to Power BI
detailed_claims <- output_tables$detailed_claims
by_syndicate <- output_tables$by_syndicate
by_risk_code <- output_tables$by_risk_code
by_claim_status <- output_tables$by_claim_status
summary <- output_tables$summary
```

6. Click **OK**
7. Select which tables you want to load
8. Click **Load**

### Method 2: Using R for Data Transformation

1. Load your Excel file normally
2. In Power Query Editor, select the claims data table
3. Click **Transform** → **Run R Script**
4. Paste this script:

```r
# Source the R script
source('C:/path/to/Lloyds_Reporting_Dev/r_scripts/solvency_claims_processor.R')

# Transform the dataset
dataset <- powerbi_transform(dataset)
```

5. Click **OK**
6. Select the transformed table
7. Click **Close & Apply**

## Creating Visualizations

### 1. Summary Dashboard

Create a dashboard showing key metrics:

**Card Visuals:**
- Total Number of Claims
- Total Outstanding (Beginning)
- Total Paid to Date
- Total Outstanding (End)
- Total Incurred

**Setup:**
1. Add Card visual
2. Select field from `summary` table
3. Format as needed (currency, number format)

### 2. Claims by Syndicate

**Clustered Bar Chart:**
- **Axis**: Syndicate Number
- **Values**: Total Incurred as at end of period
- **Legend**: Year of Account

**Table Visual:**
- Syndicate Number
- Year of Account
- Number of Claims
- Outstanding Claims Amount (End)
- Total Incurred

### 3. Risk Code Analysis

**Stacked Column Chart:**
- **Axis**: Risk Code
- **Values**: Total Incurred as at end of period
- **Legend**: Claim status at end of period

**Treemap:**
- **Group**: Risk Code
- **Values**: Outstanding Claim amount at end of period

### 4. Time Series Analysis

**Line Chart:**
- **Axis**: Year of Account
- **Values**:
  - Outstanding Claims Amount (Beginning)
  - Outstanding Claims Amount (End)
  - Paid in Year amount
- **Legend**: Multiple values

### 5. Claim Status Distribution

**Pie Chart:**
- **Legend**: Claim status at end of period
- **Values**: Number of Claims

**Donut Chart:**
- **Legend**: Claim status at end of period
- **Values**: Total Incurred as at end of period

### 6. Movement Analysis

**Waterfall Chart:**
- **Category**: Year of Account
- **Y Axis**: Movement in Year
- Shows claims development over time

## Creating Relationships

If you loaded multiple tables, create relationships:

1. Click **Model** view
2. Drag from primary key to foreign key:
   - `detailed_claims[Syndicate Number]` → `by_syndicate[Syndicate Number]`
   - `detailed_claims[Risk Code]` → `by_risk_code[Risk Code]`

3. Ensure relationship type is set correctly (usually Many-to-One)

## Data Refresh

### Manual Refresh
1. Click **Home** → **Refresh**
2. Scripts will re-run and update data

### Scheduled Refresh (Power BI Service)
1. Publish report to Power BI Service
2. Configure gateway for file access
3. Set up scheduled refresh:
   - Dataset settings → Scheduled refresh
   - Set frequency and time
   - Configure data source credentials

**Note**: Python/R scripts require gateway with appropriate runtime installed.

## Sample Measures (DAX)

Add calculated measures for additional insights:

### Average Claim Size
```dax
Average Claim Size =
DIVIDE(
    SUM('detailed_claims'[Total Incurred as at end of period]),
    COUNT('detailed_claims'[Claim Reference])
)
```

### Claims Development Ratio
```dax
Development Ratio =
DIVIDE(
    SUM('detailed_claims'[Outstanding Claim amount as at end of period]),
    SUM('detailed_claims'[Outstanding Claims Amount as at beginning of period])
)
```

### Payment Ratio
```dax
Payment Ratio =
DIVIDE(
    SUM('detailed_claims'[Paid in Year amount]),
    SUM('detailed_claims'[Total Incurred as at end of period])
)
```

### Open Claims Count
```dax
Open Claims =
CALCULATE(
    COUNT('detailed_claims'[Claim Reference]),
    'detailed_claims'[Claim status at end of period] = "Open"
)
```

### Large Claims (>£100k)
```dax
Large Claims Count =
CALCULATE(
    COUNT('detailed_claims'[Claim Reference]),
    'detailed_claims'[Total Incurred as at end of period] > 100000
)
```

## Filtering and Slicers

Add slicers for interactive filtering:

1. **Syndicate Number** - Filter by specific syndicate
2. **Year of Account** - Focus on specific underwriting years
3. **Risk Code** - Analyze specific risk types
4. **Claim Status** - View open vs closed claims
5. **Currency** - Filter by original currency
6. **Date Range** - If using signing dates

## Best Practices

### Performance Optimization
1. **Use Query Folding**: When possible, filter data at source
2. **Reduce Data Volume**: Only import necessary date ranges
3. **Use Aggregations**: Pre-aggregate data for large datasets
4. **Disable Auto Date/Time**: For claim dates
5. **Use Import Mode**: Unless data is extremely large

### Data Refresh Strategy
1. **Incremental Refresh**: For large datasets
   - Configure incremental refresh policy
   - Keep last 2-3 years in detail
   - Aggregate older data
2. **Partition by Year**: Separate tables by year of account
3. **Archive Old Data**: Move closed claims to archive tables

### Report Design
1. **Use Bookmarks**: Create different views
2. **Drill-through Pages**: Detailed claim analysis
3. **Tooltips**: Show additional context on hover
4. **Mobile Layout**: Design for mobile viewing
5. **Performance Analyzer**: Check slow visuals

## Troubleshooting

### Python Script Errors

**Error: "No Python runtime found"**
- Solution: Configure Python in Options → Python scripting
- Verify Python installation with: `python --version`

**Error: "ModuleNotFoundError: No module named 'pandas'"**
- Solution: Install missing packages: `pip install pandas openpyxl`

**Error: "Script execution time exceeded"**
- Solution:
  - Reduce data volume
  - Optimize script performance
  - Increase timeout in Options

### R Script Errors

**Error: "R installation not found"**
- Solution: Install R and configure in Options → R scripting

**Error: "Package not found"**
- Solution: Install packages in R: `install.packages(c("readxl", "dplyr"))`

**Error: "Object 'dataset' not found"**
- Solution: Ensure the input table is named 'dataset' in Power Query

### Data Loading Issues

**Problem: Tables not appearing after script runs**
- Check script output variables match expected names
- Verify script completed without errors
- Check Power BI script output window

**Problem: Data types incorrect**
- Explicitly convert types in script
- Use Power Query to change types after loading

**Problem: Slow refresh times**
- Reduce number of rows processed
- Optimize aggregations
- Use query folding where possible

### Visual Issues

**Problem: Incorrect totals**
- Check for duplicate relationships
- Verify measure calculations
- Use SUM vs SUMX appropriately

**Problem: Missing data in visuals**
- Check filters on visual, page, and report level
- Verify relationships are correct
- Check for blanks in key fields

## Additional Resources

- [Power BI Python Integration Docs](https://docs.microsoft.com/power-bi/connect-data/desktop-python-scripts)
- [Power BI R Integration Docs](https://docs.microsoft.com/power-bi/connect-data/desktop-r-scripts)
- [DAX Guide](https://dax.guide/)
- [Power BI Community](https://community.powerbi.com/)

## Example Report Template

A complete example showing:
- Summary page with key metrics
- Syndicate analysis page
- Risk code breakdown
- Time series trends
- Detailed claim explorer

To use:
1. Load all tables using methods above
2. Create relationships
3. Add visuals as described
4. Apply consistent formatting
5. Test with synthetic data first

## Support

For script-specific issues:
- Review code comments in Python/R scripts
- Check input data format
- Validate calculated fields

For Power BI issues:
- Consult Power BI documentation
- Check Power BI community forums
- Verify data gateway configuration (for scheduled refresh)
