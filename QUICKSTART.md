# Quick Start Guide

Get up and running with the Solvency II Claims Processing scripts in 5 minutes.

## Step 1: Clone the Repository

```bash
git clone https://github.com/jp3141github/Lloyds_Reporting_Dev.git
cd Lloyds_Reporting_Dev
```

## Step 2: Choose Your Language

### Option A: Python

1. **Install Python dependencies:**
   ```bash
   pip install -r python_scripts/requirements.txt
   ```

2. **Test with synthetic data:**
   ```bash
   cd python_scripts
   python3 -c "
   from solvency_claims_processor import process_claims_data
   output = process_claims_data('../synthetic_data/synthetic_lloyds_claims_data.xlsx')
   print('Success! Generated', len(output['by_syndicate']), 'syndicate records')
   "
   ```

### Option B: R

1. **Install R packages:**
   ```r
   source('r_scripts/install_packages.R')
   ```

2. **Test with synthetic data:**
   ```r
   source('r_scripts/solvency_claims_processor.R')
   output <- process_claims_data('synthetic_data/synthetic_lloyds_claims_data.xlsx')
   cat('Success! Generated', nrow(output$by_syndicate), 'syndicate records\n')
   ```

## Step 3: Load into Power BI

### Quick Method (Python):

1. Open Power BI Desktop
2. **Get Data** → **Python script**
3. Paste this code (update paths):

```python
import sys
sys.path.append(r'C:\path\to\Lloyds_Reporting_Dev\python_scripts')

from solvency_claims_processor import process_claims_data

# Use the synthetic data
input_file = r'C:\path\to\Lloyds_Reporting_Dev\synthetic_data\synthetic_lloyds_claims_data.xlsx'
output_tables = process_claims_data(input_file)

# Export tables for Power BI
detailed_claims = output_tables['detailed_claims']
by_syndicate = output_tables['by_syndicate']
by_risk_code = output_tables['by_risk_code']
summary = output_tables['summary']
```

4. Click **OK** and select the tables you want
5. Click **Load**

### Quick Method (R):

1. Open Power BI Desktop
2. **Get Data** → **R script**
3. Paste this code (update paths):

```r
source('C:/path/to/Lloyds_Reporting_Dev/r_scripts/solvency_claims_processor.R')

# Use the synthetic data
output_tables <- process_claims_data('C:/path/to/Lloyds_Reporting_Dev/synthetic_data/synthetic_lloyds_claims_data.xlsx')

# Export tables for Power BI
detailed_claims <- output_tables$detailed_claims
by_syndicate <- output_tables$by_syndicate
by_risk_code <- output_tables$by_risk_code
summary <- output_tables$summary
```

4. Click **OK** and select the tables you want
5. Click **Load**

## Step 4: Create Your First Visual

1. Add a **Card** visual for Total Claims:
   - Select `summary` table
   - Drag `Total Number of Claims` to the visual

2. Add a **Bar Chart** for Syndicates:
   - Select `by_syndicate` table
   - **Axis**: Syndicate Number
   - **Values**: Total Incurred as at end of period

3. Add a **Table** for detailed view:
   - Select `detailed_claims` table
   - Add columns: Claim Reference, Syndicate Number, Risk Code, Total Incurred

## Step 5: Using Your Own Data

Replace the synthetic data with your actual claims data:

1. Ensure your Excel file has the same structure as `synthetic_data/synthetic_lloyds_claims_data.xlsx`
2. Required columns (see README.md for full list):
   - Syndicate Number
   - Claim Reference
   - Year of Account
   - Outstanding amounts
   - Paid amounts
3. Update the `input_file` path in your Power BI script
4. Refresh the data

## Common Issues

### "Module not found" (Python)
```bash
pip install pandas openpyxl numpy
```

### "Package not found" (R)
```r
install.packages(c("readxl", "dplyr", "tidyr", "openxlsx"))
```

### "Python runtime not found" (Power BI)
- Go to: File → Options → Python scripting
- Set Python home directory to your Python installation

### "R installation not found" (Power BI)
- Go to: File → Options → R scripting
- Set R home directory to your R installation

## What's Included

- **500 synthetic claims** across 8 syndicates
- **10 years of data** (2015-2024)
- **Multiple risk codes** and claim statuses
- **Realistic amounts** totaling ~£80M outstanding

## Next Steps

1. Review [README.md](README.md) for detailed documentation
2. Check [POWERBI_GUIDE.md](POWERBI_GUIDE.md) for advanced Power BI features
3. Customize the scripts for your specific needs
4. Create dashboards and reports

## Example Output

When you run the scripts successfully, you'll get:

```
=== Summary Report ===
Total Number of Claims: 500
Number of Syndicates: 8
Total Outstanding (Beginning): £81,019,056
Total Paid to Date: £59,433,657
Total Outstanding (End): £36,131,409

=== By Syndicate ===
Syndicate | Year | Claims | Outstanding | Total Incurred
123       | 2023 | 45     | £2,456,789  | £8,234,567
456       | 2023 | 38     | £1,987,654  | £6,543,210
...
```

## Support

- **Documentation**: See README.md and POWERBI_GUIDE.md
- **Sample Data**: Use synthetic_lloyds_claims_data.xlsx for testing
- **Issues**: Check the troubleshooting section in POWERBI_GUIDE.md

---

**Ready to start?** Jump to Step 1 above!
