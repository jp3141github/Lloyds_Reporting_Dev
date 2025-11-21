# Lloyd's Liquidity Stress Test - Power BI Implementation

This repository contains Python and R implementations for processing Lloyd's of London Liquidity Stress Test data for use in Power BI to generate RRA (Reserve Return Annual) form outputs.

## 📁 Repository Structure

```
Lloyds_Reporting_Dev/
├── Files_for_Claude/
│   └── Liquidity Stress Test Template_December 2024.xlsx  # Original template
├── data/
│   ├── generate_synthetic_data.py                         # Synthetic data generator
│   ├── syndicate_XXXX/                                    # Individual syndicate data
│   │   ├── metadata.json
│   │   ├── assets_liquidity.csv
│   │   ├── cashflow.csv
│   │   └── stress_scenario.csv
│   ├── all_syndicates_metadata.csv                        # Combined datasets
│   ├── all_syndicates_assets.csv
│   ├── all_syndicates_cashflow.csv
│   └── all_syndicates_stress.csv
├── python_implementation/
│   ├── liquidity_stress_test.py                           # Python module
│   ├── POWERBI_INTEGRATION.md                             # Power BI Python guide
│   ├── syndicate_2001_analysis.xlsx                       # Example output
│   └── all_syndicates_analysis.xlsx                       # Example output
└── r_implementation/
    ├── liquidity_stress_test.R                            # R module
    ├── POWERBI_INTEGRATION.md                             # Power BI R guide
    ├── syndicate_2001_analysis.xlsx                       # Example output
    └── all_syndicates_analysis.xlsx                       # Example output
```

## 🎯 Features

### Data Generation
- **Synthetic Lloyd's Data**: Realistic synthetic data generator for testing
- **5 Sample Syndicates**: Complete datasets for Alpha, Beta, Gamma, Delta, and Epsilon syndicates
- **Multiple Time Periods**: Quarterly projections from Dec 2024 to Dec 2025
- **Stress Scenarios**: 1-in-200 year event modeling (US Windstorm)

### Analysis Components

1. **Capital Position Analysis**
   - Funds at Lloyd's (FAL)
   - Funds in Syndicate (FIS)
   - Underwriting SCR (uSCR)
   - Underwriting ECA (uECA)
   - Solvency ratios

2. **Liquidity Breakdown**
   - Restricted Assets (US Trust Funds, Other Trust Funds)
   - Illiquid Assets (Reinsurance Recoverables)
   - Liquid Assets / Free Funds
   - Quarterly projections

3. **Cashflow Analysis**
   - Operating cash flows
   - Non-operating cash flows
   - Premium income and claims paid
   - Investment income
   - Member transactions

4. **Stress Test Impact**
   - Baseline vs stressed scenarios
   - Liquidity gaps
   - US funding requirements
   - Disputed reinsurance recoveries

## 🚀 Quick Start

### 1. Generate Synthetic Data

```bash
cd Lloyds_Reporting_Dev
python3 data/generate_synthetic_data.py
```

This creates:
- 5 individual syndicate folders with complete data
- Combined CSV files for all syndicates

### 2. Python Implementation

#### Run Standalone Analysis

```bash
cd Lloyds_Reporting_Dev
python3 python_implementation/liquidity_stress_test.py
```

#### Use in Power BI

See [python_implementation/POWERBI_INTEGRATION.md](python_implementation/POWERBI_INTEGRATION.md) for detailed instructions.

**Quick Example:**
```python
from liquidity_stress_test import LiquidityStressTest

lst = LiquidityStressTest('data')
lst.load_data()

# Generate dashboard summary
summary = lst.create_dashboard_summary()
print(summary)

# Export to Excel
lst.export_to_excel('output.xlsx')
```

### 3. R Implementation

#### Run Standalone Analysis

```bash
cd Lloyds_Reporting_Dev
Rscript r_implementation/liquidity_stress_test.R
```

#### Use in Power BI

See [r_implementation/POWERBI_INTEGRATION.md](r_implementation/POWERBI_INTEGRATION.md) for detailed instructions.

**Quick Example:**
```r
source("r_implementation/liquidity_stress_test.R")

lst <- LiquidityStressTest$new("data")
lst$load_data()

# Generate dashboard summary
summary <- lst$create_dashboard_summary()
print(summary)

# Export to Excel
lst$export_to_excel("output.xlsx")
```

## 📊 Output Tables for RRA Forms

Both implementations generate the following tables required for RRA reporting:

1. **Capital Position Table**
   - Syndicate identification
   - Capital metrics (FAL, FIS, uSCR, uECA)
   - Solvency and coverage ratios

2. **Liquidity Breakdown Table**
   - Asset classification by liquidity
   - Quarterly projections
   - Percentage breakdowns

3. **Cashflow Summary Table**
   - Operating and non-operating cashflows
   - Cumulative metrics
   - Free funds movements

4. **Stress Impact Analysis Table**
   - Baseline vs stressed positions
   - Liquidity gaps
   - Minimum liquidity positions
   - Stress test pass/fail indicators

5. **Dashboard Summary**
   - Executive overview
   - Key risk metrics
   - Stress scenario details

## 📦 Dependencies

### Python Requirements
```bash
pip install pandas openpyxl numpy
```

### R Requirements
```r
install.packages(c("dplyr", "tidyr", "jsonlite", "readr", "openxlsx", "R6", "ggplot2"))
```

## 🔧 Power BI Integration

### Python in Power BI
1. Enable Python scripting in Power BI Desktop
2. Import CSV data files or use Python to load data
3. Create Python visuals with the provided functions
4. Use pre-calculated tables for better performance

### R in Power BI
1. Enable R scripting in Power BI Desktop
2. Import CSV data files or use R to load data
3. Create R visuals with ggplot2 visualizations
4. Use pre-calculated tables for better performance

See the respective POWERBI_INTEGRATION.md files for detailed examples.

## 📈 Example Use Cases

### 1. Regulatory Reporting
- Generate quarterly RRA submissions
- Track capital and liquidity positions
- Document stress test results

### 2. Risk Management
- Monitor syndicate solvency ratios
- Analyze liquidity under stress
- Identify funding gaps

### 3. Executive Dashboards
- High-level summary metrics
- Multi-syndicate comparisons
- Trend analysis over time

### 4. Scenario Planning
- Test different stress scenarios
- Model US funding requirements
- Evaluate reinsurance disputes

## 🔍 Data Schema

### Metadata Fields
- `syndicate_number`, `syndicate_name`, `managing_agent`
- `syndicate_fal`, `syndicate_fis`, `syndicate_uscr`, `syndicate_ueca`
- `scenario_type`, `gross_loss_estimate`, `net_loss_estimate`
- `us_funding_requirement`, `disputed_recoveries`

### Asset Data Fields
- `date`, `syndicate_number`
- `us_trust_funds`, `other_trust_funds`, `other_restricted_assets`
- `reinsurance_recoverables`, `reinsurer_urp_unearned`, `other_illiquid_assets`
- `closing_free_funds`, `other_liquid_assets`

### Cashflow Fields
- `date`, `syndicate_number`
- `opening_free_funds`, `closing_free_funds`
- `premium_income`, `claims_paid`, `reinsurance_recoveries`
- `operating_expenses`, `investment_income`
- `total_operating_cashflow`, `total_non_operating_cashflow`

### Stress Scenario Fields
- `date`, `syndicate_number`
- `stress_scenario_impact`, `cumulative_stress_impact`

## 🧪 Testing the Implementation

### Test Python Implementation
```bash
python3 python_implementation/liquidity_stress_test.py
```

Expected output:
- Console output showing syndicate summary
- Two Excel files created in python_implementation/

### Test R Implementation
```bash
Rscript r_implementation/liquidity_stress_test.R
```

Expected output:
- Console output showing syndicate summary
- Two Excel files created in r_implementation/

## 📝 Customization

### Add More Syndicates
Edit `data/generate_synthetic_data.py`:
```python
SYNDICATES = [
    {"number": 2006, "name": "Your Syndicate", "agent": "Your Managing Agent"},
    # ... add more
]
```

### Modify Stress Scenarios
Edit the `generate_stress_scenario()` function in `generate_synthetic_data.py`:
- Change loss multiples
- Adjust reinsurance recovery rates
- Modify US funding requirements
- Add additional peril types

### Custom Calculations
Both Python and R implementations support custom calculations:
- Extend the LiquidityStressTest class
- Add new methods for specific analyses
- Create custom output tables

## 🐛 Troubleshooting

### Common Issues

**Python: "ModuleNotFoundError: No module named 'pandas'"**
```bash
pip install pandas openpyxl
```

**R: "Error: package 'dplyr' not found"**
```r
install.packages("dplyr")
```

**Power BI: "Python/R script error"**
- Check that Python/R paths are set correctly in Power BI options
- Verify all dependencies are installed
- Use absolute paths for file locations
- Check script for syntax errors

**Data not loading**
- Verify file paths are correct
- Check that CSV files exist in data/ folder
- Ensure file permissions allow reading

## 📚 Additional Resources

- [Lloyd's of London Website](https://www.lloyds.com/)
- [Power BI Python Documentation](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-python-visuals)
- [Power BI R Documentation](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-r-visuals)
- [RRA Form Specifications](https://www.lloyds.com/conducting-business/solvency-ii)

## 📄 License

This implementation is provided as-is for Lloyd's syndicate reporting purposes.

## 🤝 Contributing

To contribute improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## ⚠️ Important Notes

- **Synthetic Data**: The included data is synthetically generated for demonstration purposes
- **Production Use**: Replace synthetic data with actual syndicate data
- **Validation**: Always validate outputs against official Lloyd's requirements
- **Security**: Do not commit sensitive syndicate data to version control
- **Compliance**: Ensure all reporting meets Lloyd's regulatory standards

## 📞 Support

For issues or questions:
1. Check the POWERBI_INTEGRATION.md guides
2. Review troubleshooting section
3. Examine example outputs in the implementation folders

---

**Version**: 1.0
**Last Updated**: November 2024
**Compatibility**: Power BI Desktop, Python 3.7+, R 4.0+
