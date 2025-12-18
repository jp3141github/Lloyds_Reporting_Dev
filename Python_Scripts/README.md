# Lloyd's Synthetic Data Generator - Python Scripts

> **DEPRECATED (V2.0)**: This directory is deprecated as of V2.0 (December 2024).
>
> **For new development, please use:**
> - `python_scripts/` - Primary Python module for RRA/RRQ forms
> - `python_scripts/data_generation/` - Unified data generators
> - `python_scripts/forms/` - Form processors
>
> This directory is preserved for backward compatibility. Contents have been archived to `archive/v1.2.0/`.

---

This folder contains legacy Python scripts for generating synthetic Lloyd's of London insurance data for SCR (Solvency Capital Requirement) reporting.

## Files

### 1. `generate_lloyds_synthetic_data.py`
Comprehensive data generator that can be run standalone or imported as a module.

**Features:**
- Generates realistic Lloyd's syndicate data
- Creates SCR impact metrics (uSCR and 1SCR)
- Produces loss ratio validation data
- Supports CSV export
- Configurable number of syndicates and random seed

**Usage:**

```bash
# Run directly
python generate_lloyds_synthetic_data.py

# Or import as module
from generate_lloyds_synthetic_data import generate_all_data
data = generate_all_data(num_syndicates=25, seed=42, save_to_csv=True)
```

### 2. `powerbi_lloyds_data.py`
Optimized script for use in Power BI's Python script data source.

**Usage in Power BI:**
1. Open Power BI Desktop
2. Home → Get Data → More → Python script
3. Copy and paste the entire `powerbi_lloyds_data.py` script
4. Click OK
5. Select tables to import:
   - `syndicate_master`
   - `scr_impact_data`
   - `loss_ratio_data`

## Output Tables

### 1. Syndicate Master
Reference data for Lloyd's syndicates.

| Column | Description |
|--------|-------------|
| SyndicateNumber | Lloyd's syndicate number (e.g., 2001, 2988) |
| SyndicateName | Syndicate business name |
| ManagingAgent | Managing agent code |
| PrimaryBusinessClass | Main line of business |
| YearOfAccount | Year of account (2025) |
| Active | Active status (boolean) |
| StampCapacity_GBPm | Stamp capacity in £m |

### 2. SCR Impact Data
Tracks changes in uSCR (ultimate SCR) and 1SCR (1-year SCR).

| Column | Description |
|--------|-------------|
| SyndicateNumber | Lloyd's syndicate number |
| SubmissionType | Latest LCR / Latest SBF / Movement / Movement % |
| SBFVersion | Version identifier |
| SubmissionDate | Submission date |
| uSCR_GBPm | Ultimate SCR in £m |
| 1SCR_GBPm | 1-year SCR in £m |
| SCR_Ratio | Ratio of 1SCR to uSCR |

### 3. Loss Ratio Data
Plan vs Modelled loss ratios on Net Net basis.

| Column | Description |
|--------|-------------|
| SyndicateNumber | Lloyd's syndicate number |
| RowLabel | (A) 2024 LCR / (B) 2025 LCR / (C) 2025 SBF / (D) Movement |
| ReportingPeriod | Year of Account or Delta |
| SubmissionDate | Submission date |
| PlanLossRatio_NetNet | Planned loss ratio (net of RI, net of acq costs) |
| ModelledLossRatio_NetNet | Modelled loss ratio |
| SelfUplift_pct | Self-uplift percentage (modelled - plan) |
| SyndicateComments | Commentary on changes |

## Requirements

```bash
pip install pandas numpy openpyxl
```

## Customization

Edit these parameters in the scripts:

```python
# Number of syndicates to generate
num_syndicates = 25

# Random seed for reproducibility
seed = 42

# Save to CSV files
save_to_csv = True
output_dir = './output'
```

## Data Characteristics

The synthetic data generator creates realistic Lloyd's data with:

- **Syndicate Numbers**: Authentic Lloyd's syndicate numbering (2001-6200, 1176-4242)
- **Business Classes**: Property, Marine, Aviation, Cyber, Reinsurance, etc.
- **SCR Values**: 35-50% of stamp capacity with realistic movements
- **Loss Ratios**: Vary by business class (55-80% range)
- **Regulatory Compliance**: Modelled LR ≥ Plan LR (per Lloyd's guidance)
- **Temporal Changes**: Realistic movement patterns between submissions

## Example Output

```
Generated 25 syndicates
SCR Impact Data: 100 records (4 per syndicate)
Loss Ratio Data: 100 records (4 per syndicate)
```

## Support

For issues or questions, refer to the main repository documentation or the template file:
`Files_for_Claude/2025 SCR New SBF no LCR Template.xlsx`
