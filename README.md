# Lloyd's of London Reporting Suite

**Comprehensive Data Processing and Reporting Tools for Lloyd's of London**

This repository contains Python and R scripts for processing Lloyd's regulatory reporting requirements, including RRA (Reserving Return Annual) forms, FSCS data generation, and Solvency II Pillar 3 claims reporting.

---

## 📋 Overview

A complete suite of tools for Lloyd's of London regulatory reporting:

✅ **RRA Reporting Scripts** - Process all RRA forms (010, 020, 071, 081, 091, 193, 291-295, 391, 910, 990)
✅ **FSCS Data Generator** - Financial Services Compensation Scheme data processing
✅ **Solvency II Claims Processing** - Pillar 3 claims reporting automation
✅ **Synthetic Data Generation** - Create realistic Lloyd's data for testing
✅ **Power BI Integration** - Ready-to-use scripts for Power BI dashboards
✅ **Data Validation** - Built-in validation rules for data quality

---

## 🗂️ Repository Structure

```
Lloyds_Reporting_Dev/
│
├── python_scripts/              # Python implementations
│   ├── data_generation/         # Synthetic data generators
│   │   └── generate_synthetic_lloyds_data.py
│   ├── forms/                   # RRA form-specific processing scripts
│   │   ├── rra_010_control.py
│   │   ├── rra_193_net_claims.py
│   │   └── rra_291_gross_premium_ibnr.py
│   ├── utils/                   # Utility functions
│   │   └── rra_aggregator.py
│   ├── solvency_claims_processor.py  # Solvency II claims processor
│   └── requirements.txt         # Python dependencies
│
├── r_scripts/                   # R implementations
│   ├── data_generation/         # Synthetic data generators
│   │   └── generate_synthetic_lloyds_data.R
│   ├── forms/                   # RRA form-specific processing scripts
│   │   ├── rra_010_control.R
│   │   └── rra_193_net_claims.R
│   ├── utils/                   # Utility functions
│   │   └── rra_aggregator.R
│   ├── solvency_claims_processor.R  # Solvency II claims processor
│   └── install_packages.R       # R package installer
│
├── FSCS_PowerBI/                # FSCS data generator
│   ├── Python/                  # Python implementation
│   │   ├── fscs_data_generator.py
│   │   ├── powerbi_query.py
│   │   └── example_usage.py
│   └── R/                       # R implementation
│       ├── fscs_data_generator.R
│       ├── powerbi_query.R
│       └── example_usage.R
│
├── synthetic_data/              # Generated synthetic data
│   ├── [RRA CSV files]
│   ├── generate_synthetic_data.py
│   └── synthetic_lloyds_claims_data.xlsx
│
├── Files_for_Claude/            # Specification files
│   └── RRA-specs.xlsx           # Lloyd's RRA specifications
│
├── README.md                    # This file
├── POWER_BI_INTEGRATION_GUIDE.md # Power BI integration guide
├── POWERBI_GUIDE.md             # Solvency II Power BI guide
├── QUICKSTART.md                # Quick start guide
├── powerbi_python_example.py    # Example Power BI Python script
└── powerbi_r_example.R          # Example Power BI R script
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/jp3141github/Lloyds_Reporting_Dev.git
cd Lloyds_Reporting_Dev
```

### 2. Install Dependencies

**For Python:**
```bash
cd python_scripts
pip install -r requirements.txt
```

**For R:**
```bash
cd r_scripts
Rscript install_packages.R
```

### 3. Choose Your Use Case

#### A. RRA Reporting
```bash
# Generate synthetic RRA data
cd python_scripts/data_generation
python generate_synthetic_lloyds_data.py

# Process RRA forms
cd ../forms
python rra_010_control.py
python rra_193_net_claims.py
python rra_291_gross_premium_ibnr.py
```

#### B. FSCS Data Generation
```python
from FSCS_PowerBI.Python.fscs_data_generator import FSCSDataGenerator

generator = FSCSDataGenerator()
data = generator.generate_fscs_data(num_syndicates=10)
```

#### C. Solvency II Claims Processing
```python
from solvency_claims_processor import process_claims_data, export_to_excel

output_tables = process_claims_data('synthetic_data/synthetic_lloyds_claims_data.xlsx')
export_to_excel(output_tables, 'claims_output.xlsx')
```

---

## 📊 Features by Module

### 1. RRA Reporting Scripts

Process all Lloyd's RRA (Reserving Return Annual) forms with comprehensive data validation and analysis.

**Supported Forms:**

| Form | Description | Python | R |
|------|-------------|--------|---|
| **010** | Control Data | ✅ | ✅ |
| **020** | Exchange Rates | ✅ | ✅ |
| **071** | SCOB Mapping | ✅ | ✅ |
| **081** | Reserving Class Info | ✅ | ✅ |
| **091** | LPT (Loss Portfolio Transfer) | ✅ | ✅ |
| **193** | Net Claims Development | ✅ | ✅ |
| **291** | Gross Premium and IBNR | ✅ | ✅ |
| **292** | Net Premium and IBNR | ✅ | ✅ |
| **293** | Outstanding & IBNR (<20 PYoA) | ✅ | ✅ |
| **294** | Gross IBNR (Catastrophe) | ✅ | ✅ |
| **295** | ULAE Reserves | ✅ | ✅ |
| **391** | IELR (Incurred Emerging Loss Ratio) | ✅ | ✅ |
| **910** | Additional Information | ✅ | ✅ |
| **990** | Validation Summary | ✅ | ✅ |

**Key Features:**
- Chain ladder analysis with age-to-age factors
- Reserve adequacy metrics
- Loss ratio calculations
- Development pattern analysis
- Portfolio-level aggregations

### 2. FSCS Data Generator

Generate Financial Services Compensation Scheme data for Power BI reporting.

**Features:**
- Syndicate-level FSCS contribution calculations
- Premium-based levy computations
- Historical trend analysis
- Power BI integration ready
- Supports both Python and R

**Example Usage:**
```python
from FSCS_PowerBI.Python.fscs_data_generator import FSCSDataGenerator

gen = FSCSDataGenerator()
data = gen.generate_fscs_data(
    num_syndicates=10,
    years=range(2020, 2025),
    levy_rate=0.0025
)
```

### 3. Solvency II Claims Processing

Automate processing of Lloyd's claims data for Solvency II Pillar 3 reporting.

**Data Processing:**
- Data validation and cleansing
- Calculated fields (Total Incurred, Movement in Year, Reserve Movement)
- Multiple aggregation views

**Output Tables:**
1. **Detailed Claims** - Complete processed dataset with calculated fields
2. **By Syndicate** - Aggregated by syndicate and year of account
3. **By Risk Code** - Breakdown by risk classification
4. **By Claim Status** - Analysis by claim status
5. **Summary** - Overall statistics across all syndicates

**Example Usage:**
```python
from solvency_claims_processor import process_claims_data, export_to_excel

# Process claims data
output = process_claims_data('synthetic_data/synthetic_lloyds_claims_data.xlsx')

# Export to Excel
export_to_excel(output, 'solvency_ii_output.xlsx')

# Access specific tables
print(output['summary'])
print(output['by_syndicate'])
```

**Input Data Requirements:**
- Syndicate Number
- Claim Reference
- UMR (Unique Market Reference)
- Risk Code
- Year of Account
- Claim status (beginning/end of period)
- Outstanding Claims Amount
- Paid to Date Amount
- Paid in Year amount

---

## 💡 Synthetic Data Generation

All modules include synthetic data generators for testing and development:

### RRA Synthetic Data
- **10 Syndicates** with realistic syndicate numbers
- **Years of Account** from 2018-2025
- **20 Classes of Business** (Marine, Aviation, Property, Casualty, etc.)
- **Development triangles** with realistic payment patterns
- **IBNR estimates** with high/low ranges
- **Currency conversions** for GBP, USD, EUR, CAD, AUD, JPY

### Claims Synthetic Data
- **500+ claims** across 8 syndicates
- **Multiple risk codes** and years (2015-2024)
- **Realistic monetary amounts**
- **Various claim statuses**
- **Reference lookup tables**

---

## 🔌 Power BI Integration

All scripts are designed for seamless Power BI integration.

### Quick Integration Steps:

1. **Open Power BI Desktop**
2. **Get Data → More → Python script** (or R script)
3. **Load the appropriate script**
4. **Refresh data as needed**

See detailed guides:
- [POWER_BI_INTEGRATION_GUIDE.md](POWER_BI_INTEGRATION_GUIDE.md) - RRA and FSCS integration
- [POWERBI_GUIDE.md](POWERBI_GUIDE.md) - Solvency II integration
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide

### Example Power BI Scripts:
- `powerbi_python_example.py` - Python example for Power BI
- `powerbi_r_example.R` - R example for Power BI

---

## 📈 Example Use Cases

### Executive Dashboard
```python
from rra_aggregator import RRADataAggregator

aggregator = RRADataAggregator('synthetic_data')
aggregator.load_all_forms()
summary = aggregator.get_portfolio_summary()
```

### Claims Development Analysis
```python
from rra_193_net_claims import calculate_chain_ladder

factors = calculate_chain_ladder(syndicate=2987, lob_code='M1')
print(f"Paid LDF 12-24: {factors['paid_12_24']}")
```

### Reserve Monitoring
```r
source('r_scripts/utils/rra_aggregator.R')

forms <- rra_load_all_forms()
indicators <- get_reserve_adequacy_indicators(forms)
```

### Solvency II Reporting
```python
from solvency_claims_processor import process_claims_data

output = process_claims_data('synthetic_data/synthetic_lloyds_claims_data.xlsx')
print(output['by_risk_code'])
```

---

## 🧪 Testing

### Test All Python Scripts
```bash
# RRA scripts
cd python_scripts/data_generation
python generate_synthetic_lloyds_data.py

cd ../forms
python rra_010_control.py
python rra_193_net_claims.py
python rra_291_gross_premium_ibnr.py

# Solvency II
cd ..
python solvency_claims_processor.py

# FSCS
cd ../FSCS_PowerBI/Python
python example_usage.py
```

### Test All R Scripts
```bash
# Install packages first
cd r_scripts
Rscript install_packages.R

# RRA scripts
cd data_generation
Rscript generate_synthetic_lloyds_data.R

cd ../forms
Rscript rra_010_control.R
Rscript rra_193_net_claims.R

# Solvency II
cd ..
Rscript solvency_claims_processor.R

# FSCS
cd ../FSCS_PowerBI/R
Rscript example_usage.R
```

---

## ⚠️ Important Notes

### Data Privacy
- This repository uses **synthetic data only**
- Never commit actual Lloyd's syndicate data
- Ensure `.gitignore` excludes sensitive data files
- Comply with GDPR and data protection regulations

### Lloyd's Specifications
- RRA specifications are subject to change
- Always refer to the latest Lloyd's guidance
- Update scripts when specifications change
- See `Files_for_Claude/RRA-specs.xlsx` for current specs

### Power BI Limitations
- Python/R scripts don't support scheduled refresh in Power BI Service by default
- Consider using Power BI Dataflows or Azure Functions for production
- Use Power BI Gateway for on-premise refresh

---

## 🔧 Configuration

### Customizing Synthetic Data

```python
# In generate_synthetic_lloyds_data.py
self.syndicates = [1234, 5678, 9012]  # Your syndicate numbers
self.years_of_account = list(range(2020, 2025))
self.classes_of_business = {
    'M1': 'Marine Cargo',
    'A1': 'Aviation',
    # ... add your classes
}
```

### Adjusting Validation Rules

```python
# In rra_010_control.py
def validate_rra_010(data_source):
    invalid_capacity = df['Capacity_GBP'] < 10000000  # Min £10M
    validations.append({
        'Rule': 'Minimum Capacity £10M',
        'Status': 'FAIL' if invalid_capacity.any() else 'PASS',
        'Records_Affected': invalid_capacity.sum()
    })
```

---

## 🤝 Contributing

This is a development repository for Lloyd's reporting. To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

---

## 📚 Documentation

- **[POWER_BI_INTEGRATION_GUIDE.md](POWER_BI_INTEGRATION_GUIDE.md)** - RRA & FSCS Power BI guide
- **[POWERBI_GUIDE.md](POWERBI_GUIDE.md)** - Solvency II Power BI guide
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[Files_for_Claude/RRA-specs.xlsx](Files_for_Claude/RRA-specs.xlsx)** - Lloyd's RRA specifications
- **Python Docstrings** - All functions have detailed docstrings
- **R Comments** - All R functions are documented

---

## 📝 License

This code is provided as-is for Lloyd's of London regulatory reporting purposes.

---

## 📧 Support

For questions or issues:

1. Check the documentation files listed above
2. Review function docstrings and comments
3. Verify all required packages are installed
4. Raise an issue in the repository

---

## 🎯 Roadmap

Future enhancements:

- [ ] Add more advanced actuarial methods (Bornhuetter-Ferguson, Cape Cod)
- [ ] Create Power BI template files (.pbit)
- [ ] Add data quality dashboards
- [ ] Implement automated testing suite
- [ ] Add export to Excel functionality
- [ ] Create SQL database schema for data storage
- [ ] Add API endpoints for data access
- [ ] Enhanced validation rules
- [ ] Real-time data refresh capabilities

---

## 📊 Version History

- **v1.0** (2024-11): Initial release
  - RRA reporting scripts (Python & R)
  - FSCS data generator
  - Power BI integration
  - Synthetic data generators

- **v1.1** (2025-11): Solvency II addition
  - Solvency II Pillar 3 claims processing
  - Enhanced Power BI integration
  - Additional synthetic data generators
  - Comprehensive documentation

---

**Version:** 1.1
**Last Updated:** 2025-11-21
**Maintained By:** Lloyd's Development Team

---

Happy Reporting! 📊
