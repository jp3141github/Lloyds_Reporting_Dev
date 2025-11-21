# Lloyd's Reporting Suite - Detailed Technical Documentation

This document provides comprehensive technical documentation for developers implementing or extending the Lloyd's Reporting Suite.

**For a quick overview, see [README.md](README.md)**.

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Module Details](#module-details)
   - [RRA/RRQ Processing](#rrq-processing)
   - [Solvency II Claims](#solvency-ii-claims)
   - [Solvency II QSR](#solvency-ii-qsr)
   - [Solvency II ASB](#solvency-ii-asb)
   - [FSCS Data Generation](#fscs-data-generation)
   - [Liquidity Stress Testing](#liquidity-stress-testing)
3. [Data Schemas](#data-schemas)
4. [Validation Rules](#validation-rules)
5. [Power BI Integration Details](#power-bi-integration-details)
6. [Configuration & Customization](#configuration--customization)
7. [Troubleshooting](#troubleshooting)
8. [API Reference](#api-reference)

---

## System Architecture

### Design Principles

The Lloyd's Reporting Suite follows these core principles:

1. **Dual-language parity**: Core functionality available in both Python and R
2. **Synthetic data first**: All modules include comprehensive synthetic data generators
3. **Power BI native**: Scripts designed for seamless Power BI integration
4. **Modular design**: Each regulatory requirement is a self-contained module
5. **Validation-first**: Built-in validation rules for data quality

### Repository Structure

```
Lloyds_Reporting_Dev/
│
├─ python_scripts/              # Python implementations
│  ├─ forms/                    # RRA form processors
│  ├─ utils/                    # Utility functions
│  ├─ data_generation/          # Data generators
│  └─ solvency_claims_processor.py
│
├─ r_scripts/                   # R implementations
│  ├─ forms/                    # RRA form processors (R)
│  ├─ utils/                    # Utility functions (R)
│  └─ data_generation/          # Data generators (R)
│
├─ FSCS_PowerBI/               # FSCS module (Python + R)
├─ Solvency_II_ASB_Python/     # Solvency II ASB (Python)
├─ Solvency_II_ASB_R/          # Solvency II ASB (R)
├─ Solvency_II_QSR_Reporting/  # Solvency II QSR (Python + R)
├─ python_implementation/      # Liquidity stress test (Python)
├─ r_implementation/           # Liquidity stress test (R)
│
├─ data/                       # Liquidity synthetic data
├─ synthetic_data/             # RRA synthetic data
├─ synthetic_data_rra_2024/    # RRA 2024 data
└─ synthetic_data_rrq_2024_qN/ # RRQ quarterly data
```

### Technology Stack

**Python:**
- pandas (data manipulation)
- numpy (numerical computing)
- openpyxl, xlrd (Excel I/O)
- matplotlib, seaborn (visualization)
- scipy, statsmodels (statistical methods)

**R:**
- tidyverse (data manipulation: dplyr, tidyr, readr)
- lubridate (date handling)
- openxlsx, writexl (Excel I/O)
- ggplot2 (visualization)
- R6 (object-oriented programming)

---

## Module Details

### RRA/RRQ Processing

#### Overview

The RRA (Reserving Return Annual) and RRQ (Reserving Return Quarterly) modules process Lloyd's regulatory reserving data across 14 forms.

#### Supported Forms

| Form | Description | Frequency | Python | R |
|------|-------------|-----------|--------|---|
| **010** | Control Data | Annual/Quarterly | ✅ | ✅ |
| **020** | Exchange Rates | Annual/Quarterly | 📊 Data only | 📊 Data only |
| **071** | SCOB Mapping | Annual/Quarterly | 📊 Data only | 📊 Data only |
| **081** | Reserving Class Info | Annual/Quarterly | 📊 Data only | 📊 Data only |
| **091** | LPT (Loss Portfolio Transfer) | Annual/Quarterly | 📊 Data only | 📊 Data only |
| **193** | Net Claims Development | Annual/Quarterly | ✅ | ✅ |
| **291** | Gross Premium and IBNR | Annual/Quarterly | ✅ | ⚠️ Planned |
| **292** | Net Premium and IBNR | Annual/Quarterly | 📊 Data only | 📊 Data only |
| **293** | Outstanding & IBNR | Annual/Quarterly | 📊 Data only | 📊 Data only |
| **294** | Gross IBNR (Catastrophe) | Annual/Quarterly | 📊 Data only | 📊 Data only |
| **295** | ULAE Reserves | Annual/Quarterly | 📊 Data only | 📊 Data only |
| **391** | IELR (Incurred Emerging Loss Ratio) | Annual/Quarterly | 📊 Data only | 📊 Data only |
| **910** | Additional Information | Annual/Quarterly | 📊 Data only | 📊 Data only |
| **990** | Validation Summary | Annual/Quarterly | 📊 Data only | 📊 Data only |

**Legend:**
- ✅ = Full processor implemented
- 📊 = Synthetic data exists, no dedicated processor yet
- ⚠️ = Planned (see IMPLEMENTATION_ROADMAP.md)

#### RRA vs RRQ Differences

| Aspect | RRA (Annual) | RRQ (Quarterly) |
|--------|-------------|-----------------|
| **Frequency** | Once per year | Q1, Q2, Q3, Q4 |
| **History** | 7 years | 3 years (current + 2 prior) |
| **Scope** | All 14 forms | 11 forms (excludes some reference data) |
| **Detail Level** | Comprehensive | Focused (current year emphasis) |
| **Submission** | January | Within 30 days of quarter end |

#### Form 010: Control Data

**Purpose:** Master control data for syndicates, years of account, and classes of business.

**Python Implementation:** `python_scripts/forms/rra_010_control.py`

**Key Functions:**
```python
def load_rra_010(data_source):
    """
    Load Form 010 control data

    Args:
        data_source (str): Path to CSV file or directory

    Returns:
        pd.DataFrame: Control data with columns:
            - Syndicate_Number
            - Year_of_Account
            - LOB_Code (Line of Business)
            - Class_Description
            - Capacity_GBP
            - Active_Flag
    """
    pass

def validate_rra_010(data_source):
    """
    Validate Form 010 data against Lloyd's rules

    Validation Rules:
        1. Syndicate numbers must be 3-4 digits
        2. Years of account must be valid (YYYY format)
        3. LOB codes must match Lloyd's SCOB mapping
        4. Capacity must be positive
        5. No duplicate syndicate/YOA/LOB combinations

    Returns:
        pd.DataFrame: Validation report
    """
    pass
```

**R Implementation:** `r_scripts/forms/rra_010_control.R`

```r
load_rra_010 <- function(data_source) {
  # R equivalent
}

validate_rra_010 <- function(data_source) {
  # R equivalent with same validation rules
}
```

#### Form 193: Net Claims Development

**Purpose:** Claims development triangles for net (after reinsurance) claims.

**Python Implementation:** `python_scripts/forms/rra_193_net_claims.py`

**Key Functions:**
```python
def calculate_chain_ladder(syndicate, lob_code, triangle_type='paid'):
    """
    Calculate chain ladder age-to-age factors

    Args:
        syndicate (int): Syndicate number
        lob_code (str): Line of business code
        triangle_type (str): 'paid' or 'incurred'

    Returns:
        dict: {
            'paid_12_24': float,   # 12-24 month development factor
            'paid_24_36': float,   # 24-36 month development factor
            ...
            'tail_factor': float,  # Tail factor
            'ultimate': float      # Ultimate loss estimate
        }
    """
    pass

def analyze_development_patterns(data_source):
    """
    Analyze claims development patterns across all syndicates

    Returns:
        pd.DataFrame: Development statistics by LOB
    """
    pass
```

**Actuarial Methods:**
- **Chain Ladder:** Age-to-age development factors
- **Volume-weighted averages:** For stable estimates
- **Tail factors:** Extrapolation beyond last observed development period
- **IBNR estimates:** Ultimate - Reported

#### Form 291: Gross Premium and IBNR

**Purpose:** Gross (before reinsurance) premium and IBNR analysis.

**Python Implementation:** `python_scripts/forms/rra_291_gross_premium_ibnr.py`

**Key Functions:**
```python
def analyze_ibnr(data_source):
    """
    Analyze IBNR (Incurred But Not Reported) reserves

    Calculations:
        - IBNR_High: Upper bound estimate
        - IBNR_Low: Lower bound estimate
        - IBNR_Best: Best estimate (typically average of high/low)
        - IBNR_Range: High - Low (measure of uncertainty)

    Returns:
        pd.DataFrame: IBNR analysis by syndicate/YOA/LOB
    """
    pass

def calculate_premium_ratios(data_source):
    """
    Calculate key premium-based ratios

    Ratios:
        - Loss Ratio: Incurred / Earned Premium
        - Combined Ratio: (Incurred + Expenses) / Earned Premium
        - Ultimate Loss Ratio: Ultimate / Earned Premium

    Returns:
        pd.DataFrame: Ratio analysis
    """
    pass
```

#### Unified Form Processor

**Purpose:** Auto-detect and process both RRQ and RRA data.

**Python Implementation:** `python_scripts/forms/unified_form_processor.py`

```python
class UnifiedFormProcessor:
    """
    Process RRQ or RRA data with automatic detection

    The processor automatically detects whether data is RRQ or RRA
    based on file naming conventions and data structure.
    """

    def detect_return_type(self, data_path):
        """
        Detect if data is RRQ or RRA

        Detection Logic:
            1. Check directory/file names for 'rrq' or 'rra'
            2. Examine data range (3 years = RRQ, 7 years = RRA)
            3. Check for form exclusions (some forms RRA-only)

        Returns:
            str: 'RRQ' or 'RRA'
        """
        pass

    def process_all_forms(self, data_path):
        """
        Process all forms in the data directory

        Returns:
            dict: {
                'return_type': 'RRQ' or 'RRA',
                'forms': {
                    '010': pd.DataFrame,
                    '193': pd.DataFrame,
                    '291': pd.DataFrame,
                    ...
                },
                'validation': pd.DataFrame
            }
        """
        pass
```

**R Implementation:** ⚠️ Planned (see IMPLEMENTATION_ROADMAP.md)

#### RRA Aggregator

**Purpose:** Aggregate and summarize across all RRA forms.

**Python Implementation:** `python_scripts/utils/rra_aggregator.py`

```python
class RRADataAggregator:
    """
    Aggregate RRA data across all forms for portfolio-level analysis
    """

    def __init__(self, data_directory):
        self.data_directory = data_directory
        self.forms = {}

    def load_all_forms(self):
        """Load all 14 RRA forms from directory"""
        pass

    def get_portfolio_summary(self):
        """
        Get portfolio-level summary

        Returns:
            dict: {
                'total_syndicates': int,
                'total_capacity_gbp': float,
                'total_ibnr': float,
                'total_outstanding': float,
                'avg_loss_ratio': float,
                'reserve_adequacy': str  # 'Adequate', 'Deficient', 'Redundant'
            }
        """
        pass

    def get_reserve_adequacy_indicators(self):
        """
        Calculate reserve adequacy indicators

        Indicators:
            - Reserve Development: Favorable/Unfavorable
            - IBNR as % of Outstanding
            - Loss Ratio Trends
            - Chain Ladder Stability

        Returns:
            pd.DataFrame: Indicators by syndicate/LOB
        """
        pass
```

**R Implementation:** `r_scripts/utils/rra_aggregator.R` (equivalent functionality)

---

### Solvency II Claims

#### Overview

Process Lloyd's claims data for Solvency II Pillar 3 reporting requirements.

#### Input Data Schema

**Required Columns:**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `Syndicate_Number` | int | Syndicate number | 2987 |
| `Claim_Reference` | str | Unique claim ID | CLM-2024-001 |
| `UMR` | str | Unique Market Reference | B0123ABC456789 |
| `Risk_Code` | str | Lloyd's risk code | 111 (Property) |
| `Year_of_Account` | int | Underwriting year | 2023 |
| `Claim_Status_BoP` | str | Status at beginning of period | Open |
| `Claim_Status_EoP` | str | Status at end of period | Open |
| `Outstanding_BoP` | float | Outstanding at beginning | 500000.00 |
| `Outstanding_EoP` | float | Outstanding at end | 450000.00 |
| `Paid_to_Date` | float | Cumulative paid | 250000.00 |
| `Paid_in_Year` | float | Paid during period | 50000.00 |

#### Processing Pipeline

**Python Implementation:** `python_scripts/solvency_claims_processor.py`

```python
def process_claims_data(input_file):
    """
    Process Solvency II claims data

    Processing Steps:
        1. Load and validate input data
        2. Calculate derived fields
        3. Aggregate by multiple dimensions
        4. Generate summary statistics

    Args:
        input_file (str): Path to Excel/CSV file

    Returns:
        dict: {
            'detailed_claims': pd.DataFrame,    # Full detail with calculated fields
            'by_syndicate': pd.DataFrame,       # Aggregated by syndicate/YOA
            'by_risk_code': pd.DataFrame,       # Aggregated by risk code
            'by_claim_status': pd.DataFrame,    # Aggregated by status
            'summary': pd.DataFrame             # Overall statistics
        }
    """
    pass
```

**Calculated Fields:**

```python
# Total Incurred
df['Total_Incurred_BoP'] = df['Outstanding_BoP'] + df['Paid_to_Date'] - df['Paid_in_Year']
df['Total_Incurred_EoP'] = df['Outstanding_EoP'] + df['Paid_to_Date']

# Movement in Year
df['Movement_in_Year'] = df['Total_Incurred_EoP'] - df['Total_Incurred_BoP']

# Reserve Movement
df['Reserve_Movement'] = df['Outstanding_EoP'] - df['Outstanding_BoP']
```

#### Output Tables

**1. Detailed Claims:**
- All input columns
- Plus calculated fields (Total Incurred, Movement, Reserve Movement)

**2. By Syndicate:**
```
Syndicate_Number | Year_of_Account | Claim_Count | Total_Incurred | Total_Paid | Avg_Claim_Size
2987            | 2023            | 45          | 12500000       | 5200000    | 277777.78
```

**3. By Risk Code:**
```
Risk_Code | Risk_Description | Claim_Count | Total_Outstanding | Total_Paid
111       | Property         | 120         | 8500000          | 6200000
```

**4. By Claim Status:**
```
Status_BoP | Status_EoP | Claim_Count | Total_Movement
Open       | Open       | 80          | -500000
Open       | Closed     | 25          | 250000
```

**5. Summary:**
```
Total_Claims | Total_Incurred | Total_Outstanding | Total_Paid | Avg_Claim_Size
250          | 45000000       | 18000000         | 27000000   | 180000
```

---

### Solvency II QSR

#### Overview

Generate Solvency II Quarterly Solvency Reporting (QSR) returns with 17 regulatory forms.

#### Implemented Forms

| Form | Description | Category |
|------|-------------|----------|
| **QSR002** | Balance Sheet | Assets & Liabilities |
| **QSR220** | Own Funds | Capital |
| **QSR240** | Technical Provisions | Liabilities |
| **QSR291** | Non-Life Insurance Risk | SCR |
| **QSR292** | Market Risk | SCR |
| **QSR293** | Counterparty Default Risk | SCR |
| **QSR440** | Premiums & Claims | Income Statement |
| **QSR510** | MCR Calculation | Capital Requirements |
| **SCR_Summary** | SCR Summary | Capital Requirements |
| **Solvency_Ratio** | Solvency Ratio Analysis | KPIs |

Plus 8 additional synthetic data forms for balance sheet, investments, MCR, own funds, premiums, SCR, and technical provisions.

#### Python Implementation

**File:** `Solvency_II_QSR_Reporting/Python/qsr_report_generator.py`

```python
class QSRReportGenerator:
    """
    Generate Solvency II QSR reports

    This class provides comprehensive QSR reporting functionality including:
    - Synthetic data generation
    - Report generation for all 17 forms
    - Excel export with proper formatting
    - Power BI integration
    """

    def __init__(self, reporting_date=None):
        self.reporting_date = reporting_date or pd.Timestamp.now()
        self.data = {}

    def generate_synthetic_data(self):
        """Generate synthetic QSR data for all forms"""
        pass

    def generate_all_reports(self):
        """
        Generate all QSR reports

        Returns:
            dict: {
                'QSR002': pd.DataFrame,
                'QSR220': pd.DataFrame,
                ...
            }
        """
        pass

    def calculate_solvency_ratio(self):
        """
        Calculate Solvency Capital Ratio

        SCR Coverage Ratio = Eligible Own Funds / SCR
        MCR Coverage Ratio = Eligible Own Funds / MCR

        Returns:
            dict: {
                'scr_coverage': float,
                'mcr_coverage': float,
                'status': str  # 'Compliant', 'Warning', 'Breach'
            }
        """
        pass

    def export_to_excel(self, output_path):
        """Export all reports to Excel workbook with multiple sheets"""
        pass
```

#### R Implementation

**File:** `Solvency_II_QSR_Reporting/R/qsr_report_generator.R`

Equivalent R6 class implementation with full parity.

---

### Solvency II ASB

#### Overview

Generate Solvency II Annual Supervisory Basis (ASB) returns including claims information and inflation analysis.

#### Implemented Forms

| Form | Description |
|------|-------------|
| **ASB 245** | Claims Information - Gross |
| **ASB 246** | Claims Information - Net |
| **ASB 247** | Claims Information - Reinsurance Recoveries |
| **ASB 248** | Inflation Assumptions |

#### Data Structure

**Claims Information (ASB 245/246/247):**
- Claims development triangles (accident year x development year)
- Split by line of business
- Gross, Net, and Reinsurance views
- Paid and Incurred triangles

**Inflation (ASB 248):**
- Inflation assumptions by line of business
- Short-term vs. long-term rates
- Basis for assumptions (market data, expert judgment, etc.)

#### Python Implementation

**File:** `Solvency_II_ASB_Python/powerbi_asb_returns.py`

```python
class ASBReturnsProcessor:
    """Process ASB returns for Power BI"""

    def process_asb_245(self, claims_data):
        """
        Process ASB 245 - Gross Claims Information

        Returns:
            pd.DataFrame: Claims triangle with columns:
                - Accident_Year
                - Development_Year
                - Line_of_Business
                - Paid_Claims
                - Incurred_Claims
        """
        pass

    def process_asb_246(self, claims_data):
        """Process ASB 246 - Net Claims Information"""
        pass

    def process_asb_247(self, claims_data):
        """Process ASB 247 - Reinsurance Recoveries"""
        pass

    def process_asb_248(self, inflation_data):
        """
        Process ASB 248 - Inflation Assumptions

        Returns:
            pd.DataFrame: Inflation curves with columns:
                - Line_of_Business
                - Period (Short/Long-term)
                - Inflation_Rate
                - Basis
        """
        pass
```

---

### FSCS Data Generation

#### Overview

Generate Financial Services Compensation Scheme (FSCS) data for Lloyd's syndicates.

#### Data Schema

**Summary Level:**
```
Syndicate_Number | Year | Gross_Written_Premium | FSCS_Levy | Levy_Rate
2987            | 2024 | 50000000             | 125000    | 0.0025
```

**Detail Level:**
```
Syndicate | Year | Class_of_Business | Premium_GBP | Levy_GBP | Levy_Rate
2987      | 2024 | Property          | 20000000    | 50000    | 0.0025
2987      | 2024 | Marine            | 15000000    | 37500    | 0.0025
```

#### Python Implementation

**File:** `FSCS_PowerBI/Python/fscs_data_generator.py`

```python
class FSCSDataGenerator:
    """
    Generate FSCS data for Lloyd's syndicates

    The FSCS levy is calculated as a percentage of gross written premium
    for each syndicate and class of business.
    """

    def __init__(self, seed=None):
        self.seed = seed
        if seed:
            np.random.seed(seed)

    def generate_all(self, num_syndicates=10, start_year=2018, end_year=2025):
        """
        Generate complete FSCS dataset

        Args:
            num_syndicates (int): Number of syndicates
            start_year (int): Start year
            end_year (int): End year

        Returns:
            tuple: (summary_df, detail_df)
        """
        pass

    def calculate_levy(self, premium, levy_rate=0.0025):
        """
        Calculate FSCS levy

        Default levy rate: 0.25% (0.0025)

        Args:
            premium (float): Gross written premium
            levy_rate (float): Levy rate

        Returns:
            float: Levy amount
        """
        return premium * levy_rate
```

---

### Liquidity Stress Testing

#### Overview

Comprehensive liquidity stress test analysis for Lloyd's syndicates, aligned with Lloyd's liquidity stress test template.

#### Analysis Components

**1. Capital Position:**
- Funds at Lloyd's (FAL)
- Funds in Syndicate (FIS)
- Underwriting SCR (uSCR)
- Underwriting ECA (uECA)
- Solvency ratios (SCR, ECA)

**2. Liquidity Breakdown:**
- Restricted Assets (US Trust Funds, Other Trust Funds)
- Illiquid Assets (Reinsurance Recoverables)
- Liquid Assets / Free Funds
- Quarterly projections

**3. Cashflow Analysis:**
- Operating cash flows (premiums, claims, expenses)
- Non-operating cash flows (investment income, member transactions)
- Net cashflow by quarter

**4. Stress Test Impact:**
- Baseline vs. stressed scenarios
- Liquidity gaps
- US funding requirements
- Disputed reinsurance recoveries
- 1-in-200 year event modeling

#### Python Implementation

**File:** `python_implementation/liquidity_stress_test.py`

```python
class LiquidityStressTest:
    """
    Liquidity stress test analysis for Lloyd's syndicates

    Implements Lloyd's liquidity stress test template requirements.
    """

    def __init__(self, data_directory):
        self.data_directory = data_directory
        self.syndicates = []

    def load_data(self):
        """Load data for all syndicates"""
        pass

    def calculate_capital_position_table(self):
        """
        Calculate capital position table

        Returns:
            pd.DataFrame: Capital position with columns:
                - Syndicate
                - FAL (Funds at Lloyd's)
                - FIS (Funds in Syndicate)
                - uSCR (Underwriting SCR)
                - uECA (Underwriting ECA)
                - SCR_Coverage (FAL / uSCR)
                - ECA_Coverage (FAL / uECA)
        """
        pass

    def calculate_liquidity_breakdown_table(self):
        """
        Calculate liquidity breakdown by quarter

        Returns:
            pd.DataFrame: Liquidity breakdown with columns:
                - Syndicate
                - Quarter
                - Restricted_Assets
                - Illiquid_Assets
                - Liquid_Assets
                - Free_Funds
        """
        pass

    def calculate_stress_impact_table(self):
        """
        Calculate stress test impact

        Scenarios:
            - 1-in-200 year event
            - US Windstorm
            - Disputed reinsurance recoveries
            - Liquidity gap

        Returns:
            pd.DataFrame: Stress impact with columns:
                - Syndicate
                - Scenario
                - Baseline_Liquidity
                - Stressed_Liquidity
                - Liquidity_Gap
                - Gap_Percentage
        """
        pass

    def create_dashboard_summary(self):
        """
        Create executive dashboard summary

        Returns:
            list[dict]: Dashboard data for each syndicate:
                {
                    'syndicate_number': int,
                    'syndicate_name': str,
                    'scr_coverage': float,
                    'eca_coverage': float,
                    'liquid_assets': float,
                    'stress_test_pass': bool,
                    'max_liquidity_gap': float
                }
        """
        pass

    def export_to_excel(self, output_path):
        """
        Export all tables to Excel workbook

        Creates sheets:
            - Capital Position
            - Liquidity Breakdown
            - Cashflow Summary
            - Stress Impact
            - Dashboard
        """
        pass
```

#### R Implementation

**File:** `r_implementation/liquidity_stress_test.R`

Equivalent R6 class with ggplot2 visualizations.

---

## Data Schemas

### RRA Forms Data Schema

#### Form 010: Control Data
```csv
Syndicate_Number,Year_of_Account,LOB_Code,Class_Description,Capacity_GBP,Active_Flag
2987,2023,M1,Marine Cargo,50000000,TRUE
2987,2023,A1,Aviation,30000000,TRUE
```

#### Form 193: Net Claims Development
```csv
Syndicate_Number,Year_of_Account,LOB_Code,Development_Period,Paid_Claims,Incurred_Claims
2987,2021,M1,12,1500000,2000000
2987,2021,M1,24,2500000,2800000
2987,2021,M1,36,3200000,3200000
```

#### Form 291: Gross Premium and IBNR
```csv
Syndicate_Number,Year_of_Account,LOB_Code,Gross_Premium,Earned_Premium,IBNR_High,IBNR_Low,IBNR_Best
2987,2023,M1,5000000,4500000,800000,600000,700000
```

### Solvency II Claims Schema

```csv
Syndicate_Number,Claim_Reference,UMR,Risk_Code,Year_of_Account,Claim_Status_BoP,Claim_Status_EoP,Outstanding_BoP,Outstanding_EoP,Paid_to_Date,Paid_in_Year
2987,CLM-2024-001,B0123ABC456789,111,2023,Open,Open,500000,450000,250000,50000
```

---

## Validation Rules

### RRA Form 010 Validation

```python
# Rule 1: Syndicate number must be 3-4 digits
invalid_syndicate = df['Syndicate_Number'] < 100 or df['Syndicate_Number'] > 9999

# Rule 2: Year of account must be valid
invalid_year = df['Year_of_Account'] < 2015 or df['Year_of_Account'] > current_year

# Rule 3: Capacity must be positive
invalid_capacity = df['Capacity_GBP'] <= 0

# Rule 4: No duplicate syndicate/YOA/LOB combinations
duplicates = df.duplicated(subset=['Syndicate_Number', 'Year_of_Account', 'LOB_Code'])
```

### Solvency II Claims Validation

```python
# Rule 1: Paid must be non-negative
invalid_paid = df['Paid_in_Year'] < 0

# Rule 2: Outstanding must be non-negative
invalid_outstanding = (df['Outstanding_BoP'] < 0) | (df['Outstanding_EoP'] < 0)

# Rule 3: Total Incurred consistency check
incurred_check = abs(
    (df['Outstanding_EoP'] + df['Paid_to_Date']) -
    (df['Outstanding_BoP'] + df['Paid_to_Date'] - df['Paid_in_Year'] + df['Paid_in_Year'])
) > 0.01

# Rule 4: Claim Reference must be unique
invalid_claim_ref = df.duplicated(subset=['Claim_Reference'])
```

---

## Power BI Integration Details

### Python Script Setup in Power BI

1. **Get Data → More → Python script**
2. **Set Python executable path** (Edit Settings → Python scripting)
3. **Paste script** from appropriate `powerbi_*.py` file
4. **Select tables** to import
5. **Transform data** if needed
6. **Close & Apply**

### R Script Setup in Power BI

1. **Get Data → More → R script**
2. **Set R executable path** (Edit Settings → R scripting)
3. **Paste script** from appropriate `powerbi_*.R` file
4. **Select data frames** to import
5. **Transform data** if needed
6. **Close & Apply**

### Common DAX Measures

**Average Claim Size:**
```dax
Average Claim Size =
DIVIDE(
    SUM('Claims'[Total_Incurred]),
    DISTINCTCOUNT('Claims'[Claim_Reference])
)
```

**Loss Ratio:**
```dax
Loss Ratio =
DIVIDE(
    SUM('Claims'[Incurred]),
    SUM('Premium'[Earned_Premium])
)
```

**Development Ratio:**
```dax
Development Ratio 12-24 =
DIVIDE(
    CALCULATE(SUM('Triangle'[Paid]), 'Triangle'[Development_Period] = 24),
    CALCULATE(SUM('Triangle'[Paid]), 'Triangle'[Development_Period] = 12)
)
```

---

## Configuration & Customization

### Customizing Synthetic Data

**Modify syndicates:**
```python
# In generate_synthetic_lloyds_data.py
self.syndicates = [1234, 5678, 9012]  # Your syndicate numbers
```

**Modify years:**
```python
self.years_of_account = list(range(2020, 2025))
```

**Modify classes of business:**
```python
self.classes_of_business = {
    'M1': 'Marine Cargo',
    'A1': 'Aviation',
    'P1': 'Property',
    # ... add your classes
}
```

### Customizing Validation Rules

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

### Customizing Stress Scenarios

```python
# In data/generate_synthetic_data.py
def generate_stress_scenario():
    # Customize stress parameters
    us_windstorm_loss_multiple = 2.5  # 250% of baseline
    disputed_ri_recovery_rate = 0.3   # 30% recovery
    liquidity_gap_threshold = 0.15     # 15% of liquid assets
```

---

## Troubleshooting

### Common Issues

**Issue 1: "Module not found" error**
```bash
# Solution: Install required packages
pip install -r python_scripts/requirements.txt
# Or for R:
Rscript r_scripts/install_packages.R
```

**Issue 2: "File not found" error**
```python
# Solution: Use absolute paths
from pathlib import Path
REPO_PATH = Path(__file__).parent.parent  # Adjust as needed
input_file = REPO_PATH / "synthetic_data" / "file.csv"
```

**Issue 3: Power BI Python/R script timeout**
```
# Solution: Reduce data size or optimize script
# For large datasets, consider:
# 1. Pre-aggregate data
# 2. Filter to recent years only
# 3. Use Power Query for heavy transformations
# 4. Import pre-processed CSV instead of running full script
```

**Issue 4: Excel file corruption**
```python
# Solution: Use openpyxl engine explicitly
df.to_excel('output.xlsx', engine='openpyxl')
```

---

## API Reference

### Python Modules

**`python_scripts.solvency_claims_processor`**
- `process_claims_data(input_file)` → dict
- `export_to_excel(tables, output_file)` → None

**`python_scripts.forms.rra_010_control`**
- `load_rra_010(data_source)` → pd.DataFrame
- `validate_rra_010(data_source)` → pd.DataFrame

**`python_scripts.forms.rra_193_net_claims`**
- `calculate_chain_ladder(syndicate, lob_code, triangle_type)` → dict
- `analyze_development_patterns(data_source)` → pd.DataFrame

**`python_scripts.utils.rra_aggregator`**
- `RRADataAggregator(data_directory)` → instance
  - `.load_all_forms()` → None
  - `.get_portfolio_summary()` → dict
  - `.get_reserve_adequacy_indicators()` → pd.DataFrame

**`FSCS_PowerBI.Python.fscs_data_generator`**
- `FSCSDataGenerator(seed)` → instance
  - `.generate_all(num_syndicates, start_year, end_year)` → tuple

**`python_implementation.liquidity_stress_test`**
- `LiquidityStressTest(data_directory)` → instance
  - `.load_data()` → None
  - `.calculate_capital_position_table()` → pd.DataFrame
  - `.create_dashboard_summary()` → list[dict]

### R Modules

**`r_scripts/solvency_claims_processor.R`**
- `process_claims_data(input_file)` → list
- `export_to_excel(tables, output_file)` → NULL

**`r_scripts/forms/rra_010_control.R`**
- `load_rra_010(data_source)` → data.frame
- `validate_rra_010(data_source)` → data.frame

**`FSCS_PowerBI/R/fscs_data_generator.R`**
- `FSCSDataGenerator$new(seed)` → R6 instance
  - `$generate_all(num_syndicates, start_year, end_year)` → list

---

**Document Version:** 1.0
**Last Updated:** 2025-11-21
**For roadmap and gaps, see:** [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)
