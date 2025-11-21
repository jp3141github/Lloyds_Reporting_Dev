# Lloyd's Synthetic Data Generator - R Scripts

This folder contains R scripts for generating synthetic Lloyd's of London insurance data for SCR (Solvency Capital Requirement) reporting.

## Files

### 1. `generate_lloyds_synthetic_data.R`
Comprehensive data generator that can be run standalone or sourced as functions.

**Features:**
- Generates realistic Lloyd's syndicate data
- Creates SCR impact metrics (uSCR and 1SCR)
- Produces loss ratio validation data
- Supports CSV export
- Configurable number of syndicates and random seed

**Usage:**

```r
# Source the script
source("generate_lloyds_synthetic_data.R")

# Generate data
data <- generate_all_data(
  num_syndicates = 25,
  seed = 42,
  save_to_csv = TRUE,
  output_dir = "./output"
)

# Access individual tables
syndicate_master <- data$syndicate_master
scr_impact <- data$scr_impact_data
loss_ratios <- data$loss_ratio_data
```

### 2. `powerbi_lloyds_data.R`
Optimized script for use in Power BI's R script data source.

**Usage in Power BI:**
1. Open Power BI Desktop
2. Home → Get Data → More → R script
3. Copy and paste the entire `powerbi_lloyds_data.R` script
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
| Active | Active status (logical) |
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
| X1SCR_GBPm | 1-year SCR in £m (Note: X prefix for R naming) |
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

```r
# Install required packages
install.packages("dplyr")

# The script will attempt to install dplyr automatically if missing
```

## Customization

Edit these parameters in the scripts:

```r
# Number of syndicates to generate
NUM_SYNDICATES <- 25

# Random seed for reproducibility
RANDOM_SEED <- 42

# For standalone script
data <- generate_all_data(
  num_syndicates = 25,
  seed = 42,
  save_to_csv = TRUE,
  output_dir = "./output"
)
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
Generating synthetic Lloyd's data for 25 syndicates...

============================================================
DATA GENERATION COMPLETE
============================================================

Syndicate Master: 25 syndicates
SCR Impact Data: 100 records
Loss Ratio Data: 100 records
```

## Working with the Data

```r
# Load the data
source("generate_lloyds_synthetic_data.R")
data <- generate_all_data(num_syndicates = 20)

# Filter for specific syndicate
library(dplyr)
syndicate_2001 <- data$scr_impact_data %>%
  filter(SyndicateNumber == 2001)

# Analyze loss ratios by business class
loss_summary <- data$loss_ratio_data %>%
  left_join(data$syndicate_master, by = "SyndicateNumber") %>%
  group_by(PrimaryBusinessClass, RowLabel) %>%
  summarise(
    avg_plan = mean(PlanLossRatio_NetNet),
    avg_modelled = mean(ModelledLossRatio_NetNet)
  )
```

## Support

For issues or questions, refer to the main repository documentation or the template file:
`Files_for_Claude/2025 SCR New SBF no LCR Template.xlsx`
