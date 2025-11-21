# Solvency II ASB Returns - Python Implementation

This folder contains Python scripts for generating Lloyd's of London Solvency II Pillar 3 ASB (Annual Solvency and Balance Sheet) returns with synthetic data for Power BI reporting.

## Overview

The ASB returns include:
- **ASB 245/246/247** (S.19.01.01): Non-Life Insurance Claims Information
- **ASB 248** (S.19.01.01): Non-Life Insurance Claims Information - Inflation Rates

## Files

### 1. `synthetic_data_generator.py`
Core module for generating synthetic Lloyd's insurance data.

**Features:**
- Generates realistic claims data with development patterns
- Supports multiple currencies (GBP, USD, EUR)
- Covers 12 Lines of Business (EIOPA classifications)
- Configurable underwriting year ranges
- Reproducible results with random seed

**Usage:**
```python
from synthetic_data_generator import LloydsDataGenerator

generator = LloydsDataGenerator(
    syndicate_number='1234',
    syndicate_name='Example Marine & Energy Syndicate',
    start_year=2015,
    end_year=2024
)

# Generate all data
all_data = generator.generate_all_data()

# Save to CSV
all_data['ASB_245_246_247'].to_csv('claims_data.csv', index=False)
all_data['ASB_248'].to_csv('inflation_data.csv', index=False)
```

### 2. `powerbi_asb_returns.py`
Power BI integration script that can be used directly as a Python data source in Power BI.

**Power BI Setup:**
1. Open Power BI Desktop
2. Go to **Get Data > More > Other > Python script**
3. Copy and paste the contents of `powerbi_asb_returns.py`
4. Click **OK**
5. Select the tables you want to load:
   - `ASB_245_246_247_Claims` - Main claims data
   - `ASB_248_InflationRates` - Inflation rates
   - `Metadata` - Generation metadata
   - `LinesOfBusiness` - Reference table
   - `Claims_Summary` - Aggregated summary
   - `Development_Analysis` - Development year analysis

**Configuration:**
Edit the configuration section in the script to customize:
```python
SYNDICATE_NUMBER = '1234'
SYNDICATE_NAME = 'Your Syndicate Name'
START_YEAR = 2015
END_YEAR = 2024
CLAIMS_RECORDS = 500
INFLATION_RECORDS = 200
```

### 3. `export_to_excel.py`
Exports synthetic data to Excel format matching Lloyd's specifications.

**Usage:**
```python
from export_to_excel import export_asb_returns_to_excel

export_asb_returns_to_excel(
    output_filename='ASB_Returns_Output.xlsx',
    syndicate_number='1234',
    syndicate_name='Example Syndicate'
)
```

**Output Sheets:**
- Cover_Sheet
- ASB_245_246_247_Claims
- ASB_248_InflationRates
- Summary_by_LOB
- Summary_by_Year
- Development_Analysis
- LOB_Reference

## Data Specifications

### ASB 245/246/247 - Claims Data

| Column | Description | Type |
|--------|-------------|------|
| Currency | Reporting currency (GBP, USD, EUR) | String |
| LineOfBusiness | EIOPA LoB code (LOB01-LOB12) | String |
| UnderwritingYear | Year when policy was underwritten | Integer |
| DevelopmentYear | Years since underwriting (0-10) | Integer |
| GrossClaimPaid | Total claims paid before reinsurance | Numeric |
| ReinsuranceRecoveries | Recoveries from reinsurers | Numeric |
| GrossUndiscountedBEClaimsProvisions | Gross best estimate provisions | Numeric |
| DiscountingGrossBEClaimsProvisions | Discounting adjustment | Numeric |
| UndiscountedBEClaimsProvisionsReinsRecoverable | Reinsurance best estimate | Numeric |
| DiscountingBEClaimsProvisionsReinsRecoverable | Reins discounting | Numeric |
| GrossRBNS | Reported But Not Settled claims | Numeric |
| ReinsuranceRBNS | Reinsurance RBNS | Numeric |
| DiscountingRBNS | RBNS discounting | Numeric |
| DiscountingReinsuranceRBNS | Reins RBNS discounting | Numeric |

### ASB 248 - Inflation Rates

| Column | Description | Type |
|--------|-------------|------|
| Currency | Reporting currency | String |
| LineOfBusiness | EIOPA LoB code | String |
| UnderwritingYear | Underwriting year | Integer |
| HistoricInflationRateTotal | Total historic inflation % | Numeric |
| HistoricInflationRateExternal | External inflation % | Numeric |
| HistoricInflationRateEndogenous | Endogenous inflation % | Numeric |
| ExpectedInflationRateTotal | Expected total inflation % | Numeric |
| ExpectedInflationRateExternal | Expected external inflation % | Numeric |
| ExpectedInflationRateEndogenous | Expected endogenous inflation % | Numeric |

## Lines of Business (EIOPA Classifications)

- **LOB01**: Medical expense insurance
- **LOB02**: Income protection insurance
- **LOB03**: Workers compensation insurance
- **LOB04**: Motor vehicle liability insurance
- **LOB05**: Other motor insurance
- **LOB06**: Marine, aviation and transport insurance
- **LOB07**: Fire and other damage to property insurance
- **LOB08**: General liability insurance
- **LOB09**: Credit and suretyship insurance
- **LOB10**: Legal expenses insurance
- **LOB11**: Assistance
- **LOB12**: Miscellaneous financial loss

## Requirements

```bash
pip install pandas numpy openpyxl
```

## Example Workflow

### Generate and Export Data
```bash
# Generate data and export to Excel
python export_to_excel.py

# Or run the generator standalone
python synthetic_data_generator.py
```

### Use in Power BI
1. Open the `powerbi_asb_returns.py` script
2. Adjust configuration parameters
3. Copy the entire script
4. In Power BI: Get Data > Python script
5. Paste the script and load desired tables

## Notes

- All monetary values are in thousands
- Data is synthetic and for demonstration/testing purposes only
- Random seed is set for reproducibility
- Claims develop over time following realistic patterns
- Reinsurance recoveries are modeled as 10-40% of gross claims
- Inflation rates vary by line of business and currency

## Support

For questions or issues, refer to the main repository documentation or the original Excel specifications in the `Files_for_Claude` folder.
