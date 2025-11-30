# Solvency II AAD Returns - Python Implementation for Power BI

This directory contains Python scripts for generating and transforming Solvency II Pillar 3 Annual Assets Data (AAD) returns for Lloyd's of London, designed for use with Power BI.

## Overview

The AAD return consists of several templates that insurance companies must submit to regulators:

- **AAD230 (S.06.02.01)**: List of assets
- **AAD233 (S.08.01.01)**: Open derivatives
- **AAD235 (S.09.01.01)**: Income/gains and losses in the period
- **AAD236 (S.06.03.01)**: Collective Investment Undertakings - Look-through
- **AAD237 (S.10.01.01)**: Loans and mortgages
- **AAD238 (S.11.01.01)**: Property holdings

## Files

### Data Generation
- `synthetic_data_generator.py` - Generates synthetic Lloyd's of London style data for testing

### Power BI Transformers
- `powerbi_aad230_transformer.py` - Transforms assets data into AAD230 format
- `powerbi_aad233_transformer.py` - Transforms derivatives data into AAD233 format
- `powerbi_aad235_transformer.py` - Transforms income/gains data into AAD235 format
- `powerbi_aad236_transformer.py` - Transforms CIU data into AAD236 format
- `powerbi_aad237_transformer.py` - Transforms loans/mortgages data into AAD237 format
- `powerbi_aad238_transformer.py` - Transforms property data into AAD238 format

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Required Packages

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Generate Synthetic Data

First, generate synthetic Lloyd's data for testing:

```bash
python synthetic_data_generator.py
```

This will create a `synthetic_data/` directory with CSV files containing:
- AAD230_Assets.csv (1,000 asset records)
- AAD233_Derivatives.csv (100 derivative records)
- AAD235_Income.csv (12 income category records)
- AAD236_CIU_Lookthrough.csv (50 fund records)
- AAD237_Loans_Mortgages.csv (200 loan records)
- AAD238_Property.csv (100 property records)

### Step 2: Use in Power BI

#### Option A: Direct Python Script in Power BI

1. Open Power BI Desktop
2. Go to **Get Data** > **More** > **Other** > **Python script**
3. Paste the contents of `synthetic_data_generator.py` or load your own data
4. Click OK to execute

#### Option B: Transform Existing Data

1. Load your source data into Power BI (CSV, Excel, database, etc.)
2. Select the query in Power Query Editor
3. Go to **Transform** > **Run Python Script**
4. Copy the appropriate transformer script (e.g., `powerbi_aad230_transformer.py`)
5. Paste into the script editor
6. Click OK

The transformer will:
- Map your columns to the correct EIOPA reference codes
- Apply data validations
- Format dates and numeric fields
- Calculate derived fields
- Provide validation warnings and errors

#### Option C: Import Pre-Generated Data

1. Run the synthetic data generator locally
2. In Power BI, go to **Get Data** > **Text/CSV**
3. Navigate to the `synthetic_data/` folder
4. Import the relevant CSV file(s)
5. (Optional) Apply transformers for additional validation

## Data Structure

### AAD230 - List of Assets

Key fields:
- Portfolio (L/NL/RF)
- Asset ID Code (ISIN, SEDOL, CUSIP, or internal)
- Issuer information (name, code, sector, country)
- Financial data (quantity, price, total Solvency II amount)
- Maturity date, duration, credit quality

### AAD233 - Open Derivatives

Key fields:
- Derivative ID Code
- Counterparty information
- Contract details (type, notional amount, currency)
- Premium paid/received
- Maturity date, valuation method

### AAD235 - Income/Gains and Losses

Aggregated by asset category:
- Dividends
- Interest income
- Rent
- Net gains/losses
- Unrealised gains/losses

### AAD236 - CIU Look-through

Key fields:
- Investment fund codes
- CIU identification
- Underlying asset categories
- Total Solvency II amounts
- Level of look-through

### AAD237 - Loans and Mortgages

Key fields:
- Loan identification and type
- Borrower information
- Original and outstanding amounts
- Interest rate, maturity date
- Collateral value, LTV ratio

### AAD238 - Property

Key fields:
- Property identification and type
- Location (country)
- Purchase price and current valuation
- Rental income and occupancy rate
- Rental yield and capital appreciation

## Validation Rules

Each transformer includes built-in validations based on Solvency II specifications:

- **Required fields**: Asset ID, Portfolio, Total Solvency II Amount
- **Data types**: Numeric fields, dates, categorical codes
- **Value ranges**: Valid portfolio codes, CIC codes, rating codes
- **Business rules**:
  - No duplicate Asset IDs
  - Fund Number required for RF portfolio
  - Valid ISIN/SEDOL/CUSIP formats
  - Positive amounts where applicable

Validation errors and warnings are printed to the Power BI script output.

## Customization

### Modifying Field Mappings

Each transformer has a dictionary defining the mapping between source columns and EIOPA codes:

```python
aad230_columns = {
    'C0060_Portfolio': 'Portfolio',
    'C0040_Asset_ID_Code': 'Asset_ID_Code',
    # ... add or modify mappings
}
```

Update these mappings to match your source data structure.

### Adding Custom Validations

Add validation functions to check specific business rules:

```python
def custom_validation(df):
    # Your validation logic
    if condition:
        validation_results['errors'].append("Error message")
    return validation_results
```

### Adjusting Synthetic Data Volume

Modify the number of records generated:

```python
generator = LloydsDataGenerator(num_records=5000)  # Increase from default 1000
```

## Power BI Integration Tips

1. **Python Environment**: Ensure Power BI is configured to use the correct Python installation
   - Go to **File** > **Options and settings** > **Options** > **Python scripting**
   - Set the Python home directory

2. **Performance**: For large datasets (>100K rows), consider:
   - Pre-processing data outside Power BI
   - Using incremental refresh
   - Optimizing Python scripts for vectorization

3. **Refresh**: Python scripts in Power BI re-execute on each data refresh

4. **Security**: When using real data, ensure compliance with data protection regulations

## Reference Documents

Based on:
- Solvency II Pillar 3 - AAD Return Specifications Annual 2024
- EIOPA reporting guidelines
- Lloyd's of London reporting requirements

## Support

For issues or questions:
1. Check the validation output in Power BI script results
2. Review the EIOPA reference codes in the specifications
3. Verify your source data structure matches expected format

## License

This implementation is for internal use with Lloyd's of London regulatory reporting.
