# Lloyd's RRA Reporting Scripts

**Reserving Return Annual (RRA) Data Processing and Reporting for Lloyd's of London**

This repository contains Python and R scripts for processing Lloyd's RRA (Reserving Return Annual) forms, generating synthetic data for testing, and creating Power BI reports.

---

## 📋 Overview

The Lloyd's RRA reporting system requires syndicates to submit detailed reserving data across multiple forms. This repository provides:

✅ **Synthetic Data Generation** - Create realistic Lloyd's data for testing
✅ **Form Processing Scripts** - Process all RRA forms (010, 020, 071, 081, 091, 193, 291-295, 391, 910, 990)
✅ **Power BI Integration** - Ready-to-use scripts for Power BI dashboards
✅ **Data Validation** - Built-in validation rules for data quality
✅ **Analysis Functions** - Calculate chain ladder factors, loss ratios, reserve adequacy metrics

---

## 🗂️ Repository Structure

```
Lloyds_Reporting_Dev/
│
├── python_scripts/              # Python implementation
│   ├── data_generation/         # Synthetic data generators
│   │   └── generate_synthetic_lloyds_data.py
│   ├── forms/                   # Form-specific processing scripts
│   │   ├── rra_010_control.py
│   │   ├── rra_193_net_claims.py
│   │   └── rra_291_gross_premium_ibnr.py
│   ├── utils/                   # Utility functions
│   │   └── rra_aggregator.py
│   └── requirements.txt         # Python dependencies
│
├── r_scripts/                   # R implementation
│   ├── data_generation/         # Synthetic data generators
│   │   └── generate_synthetic_lloyds_data.R
│   ├── forms/                   # Form-specific processing scripts
│   │   ├── rra_010_control.R
│   │   └── rra_193_net_claims.R
│   ├── utils/                   # Utility functions
│   │   └── rra_aggregator.R
│   └── install_packages.R       # R package installer
│
├── synthetic_data/              # Generated synthetic data (CSV files)
│
├── Files_for_Claude/            # Specification files
│   └── RRA-specs.xlsx           # Lloyd's RRA specifications
│
├── README.md                    # This file
└── POWER_BI_INTEGRATION_GUIDE.md # Power BI integration guide
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

### 3. Generate Synthetic Data

**Using Python:**
```bash
cd python_scripts/data_generation
python generate_synthetic_lloyds_data.py
```

**Using R:**
```bash
cd r_scripts/data_generation
Rscript generate_synthetic_lloyds_data.R
```

This will create CSV files in the `synthetic_data/` folder.

### 4. Use in Power BI

See the [POWER_BI_INTEGRATION_GUIDE.md](POWER_BI_INTEGRATION_GUIDE.md) for detailed instructions.

---

## 📊 RRA Forms Covered

| Form | Description | Python Script | R Script |
|------|-------------|--------------|----------|
| **010** | Control Data | ✅ | ✅ |
| **020** | Exchange Rates | ✅ Data Gen | ✅ Data Gen |
| **071** | SCOB Mapping | ✅ Data Gen | ✅ Data Gen |
| **081** | Reserving Class Info | ✅ Data Gen | ✅ Data Gen |
| **091** | LPT (Loss Portfolio Transfer) | ✅ Data Gen | ✅ Data Gen |
| **193** | Net Claims Development | ✅ | ✅ |
| **291** | Gross Premium and IBNR | ✅ | ✅ Data Gen |
| **292** | Net Premium and IBNR | ✅ Data Gen | ✅ Data Gen |
| **293** | Outstanding & IBNR (<20 PYoA) | ✅ Data Gen | ✅ Data Gen |
| **294** | Gross IBNR (Catastrophe) | ✅ Data Gen | ✅ Data Gen |
| **295** | ULAE Reserves | ✅ Data Gen | ✅ Data Gen |
| **391** | IELR (Incurred Emerging Loss Ratio) | ✅ Data Gen | ✅ Data Gen |
| **910** | Additional Information | ✅ Data Gen | ✅ Data Gen |
| **990** | Validation Summary | ✅ Data Gen | ✅ Data Gen |

✅ = Full implementation with processing functions
✅ Data Gen = Synthetic data generation available

---

## 💡 Key Features

### Synthetic Data Generation

The data generators create realistic Lloyd's of London data including:

- **10 Syndicates** with realistic syndicate numbers
- **Years of Account** from 2018-2025
- **20 Classes of Business** (Marine, Aviation, Property, Casualty, etc.)
- **Development triangles** with realistic payment patterns
- **IBNR estimates** with high/low ranges
- **Catastrophe events** with realistic loss distributions
- **Currency conversions** for GBP, USD, EUR, CAD, AUD, JPY

### Form Processing

Each form processor includes:

- ✅ Data validation
- ✅ Calculated fields (loss ratios, development factors, etc.)
- ✅ Summary statistics by Year of Account, LOB, Syndicate
- ✅ Power BI compatible output

### Analysis Functions

- **Chain Ladder Analysis** - Calculate age-to-age factors
- **Reserve Adequacy** - IBNR to premium ratios, paid ratios
- **Loss Ratio Trends** - Ultimate and incurred loss ratios
- **Development Patterns** - Claims maturity analysis
- **Portfolio Summaries** - Aggregate across all forms

---

## 📈 Example Use Cases

### 1. Executive Dashboard

```python
from rra_aggregator import RRADataAggregator

aggregator = RRADataAggregator('synthetic_data')
aggregator.load_all_forms()

# Get high-level portfolio metrics
summary = aggregator.get_portfolio_summary()
print(summary)
```

**Output:**
- Total syndicates: 10
- Total capacity: £2.5B
- Total IBNR: £450M
- Average loss ratio: 65%

### 2. Claims Development Analysis

```python
from rra_193_net_claims import calculate_chain_ladder

# Calculate development factors
factors = calculate_chain_ladder(syndicate=2987, lob_code='M1')
print(factors)
```

**Output:**
- Paid LDF 12-24: 1.45
- Paid LDF 24-36: 1.15
- Incurred LDF 12-24: 1.20

### 3. Reserve Monitoring

```r
source('r_scripts/utils/rra_aggregator.R')

forms <- rra_load_all_forms()
indicators <- get_reserve_adequacy_indicators(forms)
print(indicators)
```

**Output:**
- IBNR to Premium ratio: 0.25
- Average paid ratio: 0.68
- ULAE ratio: 0.05

---

## 🔧 Configuration

### Customizing Synthetic Data

Edit the data generation scripts to customize:

```python
# In generate_synthetic_lloyds_data.py

# Change syndicates
self.syndicates = [1234, 5678, 9012]  # Your syndicate numbers

# Change years
self.years_of_account = list(range(2020, 2025))

# Change classes of business
self.classes_of_business = {
    'M1': 'Marine Cargo',
    'A1': 'Aviation',
    # ... add your classes
}
```

### Adjusting Loss Ratios

```python
# More conservative loss ratios
loss_ratio = random.uniform(0.55, 0.70)  # Instead of 0.45-0.85
```

### Adding Custom Validation Rules

```python
# In rra_010_control.py
def validate_rra_010(data_source):
    # Add custom validation
    invalid_capacity = df['Capacity_GBP'] < 10000000  # Min £10M
    validations.append({
        'Rule': 'Minimum Capacity £10M',
        'Status': 'FAIL' if invalid_capacity.any() else 'PASS',
        'Records_Affected': invalid_capacity.sum()
    })
```

---

## 📚 Documentation

- **[POWER_BI_INTEGRATION_GUIDE.md](POWER_BI_INTEGRATION_GUIDE.md)** - Complete Power BI integration guide
- **[Files_for_Claude/RRA-specs.xlsx](Files_for_Claude/RRA-specs.xlsx)** - Lloyd's RRA specifications
- **Python Docstrings** - All functions have detailed docstrings
- **R Comments** - All R functions are documented

---

## 🧪 Testing

### Test Python Scripts

```bash
cd python_scripts/data_generation
python generate_synthetic_lloyds_data.py

cd ../forms
python rra_010_control.py
python rra_193_net_claims.py
python rra_291_gross_premium_ibnr.py

cd ../utils
python rra_aggregator.py
```

### Test R Scripts

```bash
cd r_scripts/data_generation
Rscript generate_synthetic_lloyds_data.R

cd ../forms
Rscript rra_010_control.R
Rscript rra_193_net_claims.R

cd ../utils
Rscript rra_aggregator.R
```

---

## 🤝 Contributing

This is a development repository for Lloyd's RRA reporting. To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-form`)
3. Commit your changes (`git commit -am 'Add new form processing'`)
4. Push to the branch (`git push origin feature/new-form`)
5. Create a Pull Request

---

## ⚠️ Important Notes

### Data Privacy

- This repository uses **synthetic data only**
- Never commit actual Lloyd's syndicate data
- Ensure `.gitignore` excludes sensitive data files

### Lloyd's Specifications

- RRA specifications are subject to change
- Always refer to the latest Lloyd's guidance
- Update scripts when specifications change

### Power BI Limitations

- Python/R scripts don't support scheduled refresh in Power BI Service by default
- Consider using Power BI Dataflows or Azure Functions for production
- Use Power BI Gateway for on-premise refresh

---

## 📝 License

This code is provided as-is for Lloyd's RRA reporting development purposes.

---

## 📧 Support

For questions or issues:

1. Check the [POWER_BI_INTEGRATION_GUIDE.md](POWER_BI_INTEGRATION_GUIDE.md)
2. Review function docstrings and comments
3. Raise an issue in the repository

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

---

## 📊 Sample Output

When you run the data generator, you'll see:

```
============================================================
Generating Synthetic Lloyd's RRA Data
============================================================

✓ Generated RRA 010 Control: 10 records
✓ Generated RRA 020 Exchange Rates: 48 records
✓ Generated RRA 071 SCOB Mapping: 45 records
✓ Generated RRA 081 Reserving Class Info: 200 records
✓ Generated RRA 091 LPT: 6 records
✓ Generated RRA 193 Net Claims: 1,250 records
✓ Generated RRA 291 Gross Premium & IBNR: 350 records
✓ Generated RRA 292 Net Premium & IBNR: 350 records
✓ Generated RRA 293 OS & IBNR: 350 records
✓ Generated RRA 294 Catastrophe IBNR: 80 records
✓ Generated RRA 295 ULAE: 70 records
✓ Generated RRA 391 IELR: 750 records
✓ Generated RRA 910 Additional Info: 10 records
✓ Generated RRA 990 Validation: 10 records

============================================================
All data generated successfully in: synthetic_data
============================================================
```

---

**Version:** 1.0
**Last Updated:** 2024-11-21
**Maintained By:** Lloyd's Development Team

---

Happy Reporting! 📊🎉
