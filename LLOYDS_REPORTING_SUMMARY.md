# Lloyd's Reporting Returns - Complete Analysis & Synthetic Data Generation

## Executive Summary

This document provides a comprehensive overview of the Lloyd's of London regulatory reporting toolkit, explaining what the returns are, how they work, and the complete coverage provided by this repository's synthetic data generators.

**Total Coverage: 175+ tables across 21 major regulatory returns**

---

## What is Market Operations (Systematic Bordereaux, Velonetic Data)?

**Market operations** refers to Lloyd's central processing infrastructure managed by **Velonetic** (formerly Xchanging), which handles all premium and claims transactions. Velonetic processes approximately GBP 117.9 billion in premiums and claims annually, handling 2.3 million premium transactions and 287.1 million messages.

**Systematic bordereaux** are detailed transaction-level reports submitted by coverholders and delegated authorities containing:

### Premium Bordereaux
Policy-by-policy premium accounting with:
- **UMR** (Unique Market Reference) - Lloyd's policy identifier
- **OSN** (Original Signing Number) - Unique inception number
- Gross premium, taxes, commissions
- Lloyd's percentage participation
- Risk location and characteristics

### Claims Bordereaux
Claim-by-claim details with:
- **UCR** (Unique Claim Reference) - Lloyd's claim identifier linked to UMR
- Paid, outstanding, and incurred amounts
- Loss dates, perils, descriptions
- Defence costs and ALAE (Allocated Loss Adjustment Expenses)

These bordereaux follow **Lloyd's Coverholder Reporting Standards v5.2** and are submitted monthly/quarterly to feed syndicate accounting, reserving returns (RRA, ASB), and regulatory reporting.

---

## Synthetic Data Generators

### Existing Coverage (70+ tables)

| Category | Script | Tables | Priority |
|----------|--------|--------|----------|
| RRA Forms | `rra_forms_powerbi.py` | 14 | HIGH |
| FSCS Data | `fscs_data_powerbi.py` | 2 | MEDIUM |
| Liquidity Stress Test | `liquidity_stress_powerbi.py` | 5 | HIGH |
| Solvency II Claims | `solvency_claims_powerbi.py` | 5 | HIGH |
| Solvency II ASB | `solvency_asb_powerbi.py` | 10 | HIGH |
| Solvency II QSR | `solvency_qsr_powerbi.py` | 10 | HIGH |
| AAD Reports | `aad_reports_powerbi.py` | 8 | MEDIUM |
| SAO Addendum | `sao_addendum_powerbi.py` | 3 | MEDIUM |
| RRA Aggregator | `rra_aggregator_powerbi.py` | 5 | MEDIUM |

### New Generators (105+ tables)

| Category | Script | Tables | Priority |
|----------|--------|--------|----------|
| **LCR** (Lloyd's Capital Return) | `lcr_capital_return_powerbi.py` | 14 | **CRITICAL** |
| **SBF** (Syndicate Business Forecast) | `sbf_business_forecast_powerbi.py` | 10 | **CRITICAL** |
| **QMA** (Quarterly Monitoring Return A) | `qma_quarterly_monitoring_powerbi.py` | 10 | HIGH |
| **QMB** (Quarterly Monitoring Return B) | `qmb_performance_monitoring_powerbi.py` | 8 | HIGH |
| **Bordereaux** (Premium/Claims) | `bordereaux_powerbi.py` | 5 | HIGH |
| **ASR** (Annual Solvency Return) | `asr_annual_solvency_powerbi.py` | 12 | **CRITICAL** |
| **QAD** (Quarterly Asset Data) | `qad_quarterly_assets_powerbi.py` | 10 | HIGH |
| **PMDR** (Performance Management Data Return) | `pmdr_monthly_performance_powerbi.py` | 7 | HIGH |
| **RDS** (Realistic Disaster Scenarios) | `rds_disaster_scenarios_powerbi.py` | 8 | **CRITICAL** |
| **SRS** (Syndicate Reinsurance Structure) | `srs_reinsurance_structure_powerbi.py` | 8 | HIGH |
| **SAO** (Statement of Actuarial Opinion) | `sao_actuarial_opinion_powerbi.py` | 8 | HIGH |

---

## 1. LCR - Lloyd's Capital Return (CRITICAL)

**The most important Lloyd's return** - submitted annually as part of capital setting.

### Purpose
The LCR calculates the Syndicate Capital Requirement (SCR) using either the Lloyd's Internal Model (LIM) or Standard Formula approach. It determines how much capital each syndicate must hold.

### Key Components

| Table | Description |
|-------|-------------|
| `LCR_001_Control` | Syndicate metadata and submission control |
| `LCR_010_SCR_Summary` | Overall SCR calculation summary |
| `LCR_020_Premium_Risk` | Premium risk by line of business |
| `LCR_030_Reserve_Risk` | Reserve risk calculations |
| `LCR_040_Cat_Risk_Summary` | Catastrophe risk summary |
| `LCR_041_Cat_By_Peril` | Cat risk breakdown by peril (Wind, EQ, Flood, Terror, Cyber, Pandemic) |
| `LCR_050_Market_Risk` | Market risk (interest rate, equity, property, spread, FX) |
| `LCR_060_Credit_Risk` | Counterparty default risk |
| `LCR_070_Operational_Risk` | Operational risk calculation |
| `LCR_080_Technical_Provisions` | Technical provisions with risk margin |
| `LCR_090_Own_Funds` | Own funds analysis (Tier 1, 2, 3) |
| `LCR_100_Coverage_Ratios` | Capital coverage ratios and adequacy |
| `LCR_110_YOA_Capital` | Year of Account capital allocation |
| `LCR_120_Diversification` | Risk diversification matrix |

### Key Calculations

**SCR Range:** GBP 80-300M per syndicate (typical)
**Coverage Ratios:** 1.2-2.5x (Lloyd's minimum: 1.0x, typical target: 1.35-1.50x)

**Risk Margin Conversion:**
- Solvency II uses 4% Cost of Capital (CoC)
- Lloyd's capital setting uses 6% CoC
- Conversion factor: 1.5x (6%/4%)

---

## 2. SBF - Syndicate Business Forecast (CRITICAL)

**Three-year business plan** required for all syndicates.

### Purpose
The SBF captures the syndicate's business strategy, growth plans, and financial projections for the next three years. It's essential for capacity approval and capital planning.

### Key Components

| Table | Description |
|-------|-------------|
| `SBF_001_Control` | Submission metadata |
| `SBF_010_Income_Statement` | Projected P&L for 3 years |
| `SBF_020_Premium_Forecast` | Premium projections by LOB and geography |
| `SBF_030_Claims_Forecast` | Expected loss ratios and claims costs |
| `SBF_040_Expense_Budget` | Acquisition costs, admin expenses |
| `SBF_050_Capacity_Plan` | Stamp capacity and utilization |
| `SBF_060_Reinsurance_Strategy` | RI program structure and costs |
| `SBF_070_Investment_Income` | Investment return assumptions |
| `SBF_080_Combined_Ratios` | Target combined ratios by LOB |
| `SBF_090_Stress_Scenarios` | Downside scenario analysis |

### Typical Parameters

**Growth Rates:** -5% to +20% annual
**Loss Ratios:** 50-75% by LOB
**Combined Ratios:** 85-102%
**Expense Ratios:** 30-40%

---

## 3. QMA - Quarterly Monitoring Return Part A (HIGH)

**Primary quarterly financial return** - the backbone of Lloyd's monitoring.

### Purpose
QMA provides quarterly financial statements and key metrics to Lloyd's for ongoing monitoring. Submitted within 30 business days of quarter-end.

### Key Components

| Table | Description |
|-------|-------------|
| `QMA_001_Control` | Submission metadata and quarter info |
| `QMA_010_Balance_Sheet` | Quarterly balance sheet |
| `QMA_020_PL_Statement` | Profit & Loss account |
| `QMA_030_Cash_Flow` | Cash flow statement |
| `QMA_040_Technical_Account` | Technical account by LOB |
| `QMA_050_Investment_Portfolio` | Investment holdings and returns |
| `QMA_060_Reinsurance_Assets` | RI recoverable assets |
| `QMA_070_Creditors` | Creditor analysis |
| `QMA_080_Capital_Position` | Capital position and movements |
| `QMA_090_Key_Ratios` | KPIs and performance metrics |

### Submission Timing

- Q1: Due by end of May
- Q2: Due by end of August
- Q3: Due by end of November
- Q4/FY: Due by end of March (following year)

---

## 4. Bordereaux - Delegated Authority Reporting (HIGH)

**Transaction-level reporting** for coverholders and delegated authorities.

### Purpose
Bordereaux capture every premium and claim transaction from delegated authority arrangements, following Lloyd's Coverholder Reporting Standards (CRS) v5.2.

### Key Components

| Table | Description |
|-------|-------------|
| `Premium_Bordereaux` | Policy-level premium transactions (500+ records) |
| `Claims_Bordereaux` | Claim-level details (300+ records) |
| `Risk_Bordereaux` | Risk exposure summary |
| `Coverholder_Summary` | Performance by coverholder |
| `Contract_Performance` | TPA/Coverholder contract metrics |

### Lloyd's Identifiers

**UMR Format:** `B2024A1234567` (Broker prefix + Year + Alpha + Number)
**OSN Format:** `OSN12345678` (Original Signing Number)
**UCR Format:** `B2024A1234567/2024/001` (UMR/Year/Sequence)

### Required CRS v5.2 Fields

- Gross/Net premium amounts
- Lloyd's participation percentage
- Brokerage and commission
- Taxes and levies
- Currency and FX rates
- Risk location codes
- Perils and coverage types
- ALAE and defence costs (claims)

---

## Complete Coverage Summary

### Existing Code (70+ tables)

| Return | Forms/Tables | Status |
|--------|--------------|--------|
| RRA (Reserving Return Annual) | 14 forms | Complete |
| QSR (Quarterly Solvency Return) | 12 forms | Complete |
| ASB (Annual Solvency Balance Sheet) | 5 forms | Complete |
| AAD (Annual Actuarial Data) | 8 forms | Complete |
| SAO Addendum | 3 forms | Complete |
| FSCS | 2 tables | Complete |
| Liquidity Stress Test | 5 components | Complete |
| Claims Processing | 5 aggregations | Complete |

### New Generators (44+ tables)

| Return | Forms/Tables | Status |
|--------|--------------|--------|
| LCR (Lloyd's Capital Return) | 14 tables | **NEW** |
| SBF (Syndicate Business Forecast) | 10 tables | **NEW** |
| QMA (Quarterly Monitoring A) | 10 tables | **NEW** |
| Bordereaux | 5 tables | **NEW** |

### Not Yet Covered

The following returns are NOT covered by this repository:

**Quarterly/Flash Reporting:**
- QMA Delta (Movement analysis)
- QCT (Quarterly Claims Triangles)
- Flash Report (Rapid business metrics)

**Pillar 3 Public Disclosures:**
- ORSA (Own Risk and Solvency Assessment)
- SFCR (Solvency and Financial Condition Report)

**Territory-Specific:**
- US Trust Fund returns
- Canadian Trust Fund returns
- Lloyd's Japan returns
- Lloyd's Singapore returns

**Other:**
- LCM (Lloyd's Capital Model detailed submission)
- Tax returns (US, Canada, Japan, Singapore)
- Market operations reconciliation
- DUA system submissions
- Risk registers
- TCFD/ESG reporting

---

## How to Use in Power BI

### Step 1: Open Power BI
Open Power BI Desktop

### Step 2: Add Python Script
Go to **Get Data** > **More** > **Other** > **Python script**

### Step 3: Paste Script
Copy the entire contents of the desired `.py` file

### Step 4: Select Tables
Select the tables you want from the Navigator

### Step 5: Load Data
Click **Load** to import the data

### Example
```
Get Data > More > Other > Python script
Paste entire file contents from lcr_capital_return_powerbi.py
Select tables: LCR_010_SCR_Summary, LCR_040_Cat_Risk_Summary
Click Load
```

---

## Data Characteristics

All generators use consistent parameters:

- **Syndicates:** 10 sample Lloyd's syndicates (33, 623, 1183, 1910, 2010, 2525, 2791, 2987, 4242, 5000)
- **Years of Account:** 2018-2025
- **Reporting Year:** 2024
- **Currency:** GBP primary, with USD and EUR support
- **Random Seed:** `np.random.seed(42)` for reproducibility

### Lloyd's Identifiers

| Identifier | Format | Example |
|------------|--------|---------|
| Syndicate | 4 digits | 2001 |
| UMR | B + Year + Alpha + 7 digits | B2024A1234567 |
| OSN | OSN + 8 digits | OSN12345678 |
| UCR | UMR/Year/Sequence | B2024A1234567/2024/001 |
| YOA | 4 digit year | 2024 |
| Risk Code | XX999 | PR100 |

---

## Dependencies

All scripts require only standard Power BI Python dependencies:

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
```

No external data files required - all data is synthetically generated.

---

## File Reference

### POWER_BI Folder Scripts

| File | Description | Tables |
|------|-------------|--------|
| `lcr_capital_return_powerbi.py` | Lloyd's Capital Return | 14 |
| `sbf_business_forecast_powerbi.py` | Syndicate Business Forecast | 10 |
| `qma_quarterly_monitoring_powerbi.py` | Quarterly Monitoring A | 10 |
| `qmb_performance_monitoring_powerbi.py` | Quarterly Monitoring B (Performance) | 8 |
| `bordereaux_powerbi.py` | Premium/Claims Bordereaux | 5 |
| `asr_annual_solvency_powerbi.py` | Annual Solvency Return | 12 |
| `qad_quarterly_assets_powerbi.py` | Quarterly Asset Data | 10 |
| `pmdr_monthly_performance_powerbi.py` | Performance Management Data Return | 7 |
| `rds_disaster_scenarios_powerbi.py` | Realistic Disaster Scenarios | 8 |
| `srs_reinsurance_structure_powerbi.py` | Syndicate Reinsurance Structure | 8 |
| `sao_actuarial_opinion_powerbi.py` | Statement of Actuarial Opinion | 8 |
| `rra_forms_powerbi.py` | RRA Forms 010-990 | 14 |
| `fscs_data_powerbi.py` | FSCS Data | 2 |
| `liquidity_stress_powerbi.py` | Liquidity Stress Test | 5 |
| `solvency_claims_powerbi.py` | Solvency II Claims | 5 |
| `solvency_asb_powerbi.py` | Solvency II ASB | 10 |
| `solvency_qsr_powerbi.py` | Solvency II QSR | 10 |
| `aad_reports_powerbi.py` | AAD Reports | 8 |
| `sao_addendum_powerbi.py` | SAO Addendum | 3 |
| `rra_aggregator_powerbi.py` | RRA Aggregator | 5 |

---

## Regulatory Context

### Lloyd's Reporting Calendar

| Return | Frequency | Deadline |
|--------|-----------|----------|
| QMA/QMB | Quarterly | T+30 business days |
| QSR | Quarterly | T+30 business days |
| RRA | Annual | March |
| ASB | Annual | April |
| LCR | Annual | September (capital setting) |
| SBF | Annual | August (business planning) |
| Bordereaux | Monthly/Quarterly | Per contract terms |

### Key Regulatory Bodies

- **Lloyd's Corporation** - Market oversight and capital setting
- **PRA** (Prudential Regulation Authority) - Prudential supervision
- **FCA** (Financial Conduct Authority) - Conduct regulation
- **EIOPA** - European insurance standards (Solvency II)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-11-21 | Initial release with 70+ tables |
| 2.0 | 2024-11-23 | Added LCR, SBF, QMA, Bordereaux (114+ tables) |
| 3.0 | 2025-11-27 | Added ASR, QAD, QMB, PMDR, RDS, SRS, expanded SAO (175+ tables) |

---

**Maintained By:** Lloyd's Development Team
**Last Updated:** 2025-11-27
**Compatibility:** Power BI Desktop, Python 3.7+
