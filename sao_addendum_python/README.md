# SAO Addendum Return 2025 - Python Data Generators

This folder contains Python scripts to generate synthetic Lloyd's of London data for the **SAO Addendum Return 2025**. These scripts are designed to be used directly in **Power BI** as Python data sources.

## Overview

The SAO (Signing Actuary's Opinion) Addendum Return is a mandatory submission for Lloyd's syndicates at year-end. This collection of scripts generates realistic synthetic data for the three main tables required:

1. **090 Specific IBNR** - Specific Incurred But Not Reported reserves
2. **100 Movements and AvE Analysis** - Movements and Actual vs Expected Analysis
3. **SAO Class Mappings** - Mapping of Signing Actuary reserving classes to Lloyd's Lines of Business

## Files

```
sao_addendum_python/
├── README.md                            # This file
├── generate_090_specific_ibnr.py        # 090 Specific IBNR data generator
├── generate_100_movements_ave.py        # 100 Movements and AvE analysis generator
└── generate_sao_class_mappings.py       # SAO Class Mappings generator
```

## Requirements

### Python Packages

- `pandas` (>= 1.3.0)
- `numpy` (>= 1.21.0)

### Installation

```bash
pip install pandas numpy
```

## Usage

### Option 1: Use in Power BI (Recommended)

#### Step 1: Open Power BI Desktop

#### Step 2: Get Data from Python Script

1. Click **Get Data** > **More**
2. Search for and select **Python script**
3. Click **Connect**

#### Step 3: Paste the Script

Copy the contents of one of the generator scripts and paste into the script editor:

- For **090 Specific IBNR**: Copy `generate_090_specific_ibnr.py`
- For **100 Movements and AvE**: Copy `generate_100_movements_ave.py`
- For **SAO Class Mappings**: Copy `generate_sao_class_mappings.py`

#### Step 4: Select the Data Table

Power BI will detect the available dataframes:

- `specific_ibnr` - from the 090 Specific IBNR script
- `movements_ave` and `movements_ave_summary` - from the 100 Movements and AvE script
- `class_mappings` - from the SAO Class Mappings script

Select the table(s) you want to import and click **Load**.

### Option 2: Run Standalone

You can also run the scripts directly from the command line:

```bash
# Generate 090 Specific IBNR data
python generate_090_specific_ibnr.py

# Generate 100 Movements and AvE analysis data
python generate_100_movements_ave.py

# Generate SAO Class Mappings data
python generate_sao_class_mappings.py
```

Each script will display summary statistics and sample data to the console.

## Script Details

### 1. generate_090_specific_ibnr.py

**Output Table**: `specific_ibnr`

**Columns**:
- `Reserving Class` - Reserving class name
- `Lloyd's Cat Code` - CAT code for natural catastrophes or "Non Nat-Cat"
- `Lloyd's Line of Business` - Lloyd's LoB classification
- `Number of losses` - Number of losses associated with the IBNR
- `Underwriting Year` - Year of account (2010-2025)
- `Gross IBNR (£000s)` - Gross IBNR amount in thousands of GBP
- `Net IBNR (£000s)` - Net IBNR amount (post-reinsurance)
- `Comment (optional)` - Optional commentary on the reserve

**Default Records**: 50

**Key Features**:
- Generates specific IBNR entries for both CAT and Non-CAT events
- Realistic lognormal distribution for IBNR amounts
- Net IBNR is 70-95% of gross (accounting for reinsurance)
- More recent underwriting years have higher probability
- Includes realistic actuarial comments

### 2. generate_100_movements_ave.py

**Output Tables**: `movements_ave`, `movements_ave_summary`

**Columns** (movements_ave):
- `Class ID` - Unique class identifier (01-10)
- `Reserving Class` - Reserving class name
- `Lloyd's Line of Business` - Lloyd's LoB classification
- `Underwriting Year` - Year label (2023 & Prior, 2024, 2025)
- `Reporting Year?` - Indicator if current reporting year
- `Ultimate Premium (£000s)` - Ultimate premium estimate
- `Actual vs Expected as % of ultimate premium` - AvE analysis
- `Initial Expected Loss Ratio (IELR) (%)` - Initial expected LR
- `Ultimate Loss Ratio (ULR) (%)` - Ultimate LR estimate
- `Reserves 2024YE (£000s)` - Reserves at 2024 year-end
- `Reserves 2025YE (£000s)` - Reserves at 2025 year-end
- `Syndicate Estimate - 2025YE (£000s)` - Syndicate's reserve estimate

**Default Classes**: 10 (top 10 by reserves)

**Key Features**:
- Covers 3 underwriting years per class (30 records total)
- Realistic loss ratios (50-75% IELR)
- Actual vs Expected varies by year maturity
- Includes both Signing Actuary and Syndicate estimates
- Summary table aggregates by underwriting year

### 3. generate_sao_class_mappings.py

**Output Table**: `class_mappings`

**Columns**:
- `Signing Actuary Reserving Class Name` - Internal reserving class
- `Lloyd's LoB 1` - Primary Lloyd's Line of Business
- `LoB 1: % of Gross Exposure` - Exposure percentage for LoB 1
- `Lloyd's LoB 2` - Secondary Lloyd's LoB (if applicable)
- `LoB 2: % of Gross Exposure` - Exposure percentage for LoB 2
- `Lloyd's LoB 3` - Tertiary Lloyd's LoB (if applicable)
- `LoB 3: % of Gross Exposure` - Exposure percentage for LoB 3
- `Lloyd's LoB 4` - Quaternary Lloyd's LoB (if applicable)
- `LoB 4: % of Gross Exposure` - Exposure percentage for LoB 4

**Default Classes**: 20

**Key Features**:
- Each reserving class maps to 1-4 Lloyd's LoB
- Exposure percentages always sum to 100%
- Primary LoB typically receives 60-100% of exposure
- Intelligent mapping based on class similarity
- Covers major insurance lines (Property, Casualty, Marine, Aviation, etc.)

## Customization

Each script includes parameters you can modify:

### 090 Specific IBNR
```python
specific_ibnr = generate_specific_ibnr_data(num_records=50)  # Change number of records
```

### 100 Movements and AvE
```python
movements_ave = generate_movements_ave_data(num_classes=10)  # Change number of classes
```

### SAO Class Mappings
```python
class_mappings = generate_class_mappings_data(num_classes=20)  # Change number of classes
```

## Data Quality

All scripts include:
- ✅ Fixed random seeds for reproducibility
- ✅ Realistic statistical distributions
- ✅ Data validation and consistency checks
- ✅ Summary statistics output
- ✅ Proper handling of missing/optional fields

## Power BI Integration Tips

### Refresh Data

To refresh the synthetic data in Power BI:
1. Right-click the table in the **Fields** pane
2. Select **Refresh data**

### Create Relationships

You can create relationships between tables:
- Link `movements_ave` to `specific_ibnr` via **Reserving Class**
- Link `movements_ave` to `class_mappings` via **Reserving Class**

### Modify Random Seed

To generate different data on each refresh, change the random seed:

```python
# From this:
np.random.seed(42)

# To this (uses current time):
import time
np.random.seed(int(time.time()))
```

## Reference

Based on the **SAO Addendum Return 2025** template from Lloyd's of London.

For more information on Lloyd's reporting requirements:
- [Lloyd's Reporting Requirements](https://www.lloyds.com/resources-and-services/reporting-rationalisation)
- [Lloyd's Line of Business Mapping Tools](https://www.lloyds.com/resources-and-services/reporting-rationalisation/tpd-reserving)

## Support

For issues or questions:
1. Check the inline code comments in each script
2. Review the summary statistics output
3. Verify your Python environment has the required packages

## License

These scripts are provided as-is for generating synthetic Lloyd's of London data for development and testing purposes.

---

**Last Updated**: 2025-11-21
**Version**: 1.0
**Author**: Claude
