# Power BI Data Scripts for Lloyd's Regulatory Reporting

This folder contains comprehensive Python scripts designed for use as Power BI data sources. Each script generates synthetic Lloyd's of London data for various regulatory reporting requirements.

## Overview

**Total Tables Available: 70+**

| Category | Script | Tables |
|----------|--------|--------|
| RRA Forms | `rra_forms_powerbi.py` | 14 |
| FSCS Data | `fscs_data_powerbi.py` | 2 |
| Liquidity Stress Test | `liquidity_stress_powerbi.py` | 5 |
| Solvency II Claims | `solvency_claims_powerbi.py` | 5 |
| Solvency II ASB | `solvency_asb_powerbi.py` | 10 |
| Solvency II QSR | `solvency_qsr_powerbi.py` | 10 |
| AAD Reports | `aad_reports_powerbi.py` | 8 |
| SAO Addendum | `sao_addendum_powerbi.py` | 3 |
| RRA Aggregator | `rra_aggregator_powerbi.py` | 5 |

## How to Use in Power BI

1. Open Power BI Desktop
2. Go to **Get Data** > **More** > **Other** > **Python script**
3. Copy and paste the contents of the desired script
4. Click **OK** to execute
5. Select the tables you want to import from the Navigator
6. Click **Load** to add the data to your model

## Script Details

### 1. RRA Forms (`rra_forms_powerbi.py`)

Generates all 14 RRA (Reserving Return Annual) forms:

| Table | Description |
|-------|-------------|
| `rra_010` | Control data and syndicate metadata |
| `rra_020` | Exchange rates |
| `rra_071` | SCOB Mapping (Solvency II Classes of Business) |
| `rra_081` | Reserving class information |
| `rra_091` | Lloyd's Pension Trust (LPT) transfers |
| `rra_193` | Net Claims Development |
| `rra_291` | Gross Premium and IBNR |
| `rra_292` | Net Premium and IBNR |
| `rra_293` | Outstanding IBNR by previous years of account |
| `rra_294` | Catastrophe IBNR |
| `rra_295` | ULAE (Unallocated Loss Adjustment Expenses) |
| `rra_391` | IELR (Initial Expected Loss Ratio) |
| `rra_910` | Additional information |
| `rra_990` | Validation Summary |

### 2. FSCS Data (`fscs_data_powerbi.py`)

Financial Services Compensation Scheme data:

| Table | Description |
|-------|-------------|
| `fscs_summary` | Summary FSCS data by syndicate |
| `fscs_detail` | Detailed transaction-level FSCS data |

### 3. Liquidity Stress Test (`liquidity_stress_powerbi.py`)

Liquidity and capital stress testing data:

| Table | Description |
|-------|-------------|
| `capital_position` | Capital Position summary |
| `liquidity_breakdown` | Asset & Liquidity Breakdown |
| `cashflow_summary` | Cashflow Summary |
| `stress_impact` | Stress Test Impact analysis |
| `dashboard_summary` | Executive Dashboard Summary |

### 4. Solvency II Claims (`solvency_claims_powerbi.py`)

Claims processing and aggregation:

| Table | Description |
|-------|-------------|
| `detailed_claims` | Full claims detail |
| `by_syndicate` | Claims aggregated by Syndicate |
| `by_risk_code` | Claims aggregated by Risk Code |
| `by_claim_status` | Claims aggregated by Claim Status |
| `summary` | Overall claims summary |

### 5. Solvency II ASB (`solvency_asb_powerbi.py`)

Annual Solvency Balance Sheet returns:

| Table | Description |
|-------|-------------|
| `ASB_245_246_247_Claims` | Claims Information (Gross/Net/Reinsurance) |
| `ASB_248_InflationRates` | Inflation rates by LOB |
| `Claims_Summary` | Aggregated claims summary |
| `Development_Analysis` | Development year analysis |
| `Metadata` | Generation metadata |
| `LinesOfBusiness` | Reference table of LOB codes |
| `ASB245_Claims_Gross` | Gross claims (detailed) |
| `ASB246_Claims_Reinsurance` | Reinsurance claims |
| `ASB247_Claims_Net` | Net claims |
| `ASB_Development_Factors` | Development factors analysis |

### 6. Solvency II QSR (`solvency_qsr_powerbi.py`)

Quarterly Solvency Return reports:

| Table | Description |
|-------|-------------|
| `QSR002_Balance_Sheet` | S.02.01.02 Balance Sheet |
| `QSR220_Own_Funds` | S.23.01.01 Own Funds |
| `QSR240_Technical_Provisions` | S.17.01.02 Non-Life Technical Provisions |
| `QSR440_Premiums_Claims` | S.05.01.02.01 Premiums & Claims |
| `QSR291_Operational_Risk` | S.41.01.11 Operational Risk |
| `QSR292_Market_Risk` | S.14.01.10.01 Market Risk |
| `QSR293_Counterparty_Risk` | S.38.01.10.01 Counterparty Default Risk |
| `QSR510_MCR` | S.28.01.01 MCR Calculation |
| `SCR_Summary` | SCR with all risk modules |
| `Solvency_Ratio_Report` | Solvency coverage ratios |

### 7. AAD Reports (`aad_reports_powerbi.py`)

Annual Actuarial Data reports:

| Table | Description |
|-------|-------------|
| `AAD230_Open_Market_Value` | Open market value report (S.06.02.01) |
| `AAD230_Summary_By_Category` | OMV Summary by asset category |
| `AAD233_Off_Balance_Sheet` | Off-balance sheet items (S.08.01.01) |
| `AAD235_Derivatives` | Derivatives report (S.09.01.01) |
| `AAD235_Derivatives_Summary` | Derivatives risk summary |
| `AAD236_Collective_Investments` | Collective investments (S.06.03.01) |
| `AAD237_Structured_Products` | Structured products (S.10.01.01) |
| `AAD238_Securities_Lending` | Securities lending (S.11.01.01) |

### 8. SAO Addendum (`sao_addendum_powerbi.py`)

Signing Actuary Opinion Addendum Return:

| Table | Description |
|-------|-------------|
| `specific_ibnr` | 090 Specific IBNR data |
| `movements_ave` | 100 Movements and Actual vs Expected Analysis |
| `movements_ave_summary` | 100 Summary statistics |

### 9. RRA Aggregator (`rra_aggregator_powerbi.py`)

Portfolio-level analysis and aggregation:

| Table | Description |
|-------|-------------|
| `portfolio_summary` | Overall portfolio metrics across forms |
| `lob_analysis` | Performance by Line of Business |
| `yoa_development_summary` | Development patterns by year of account |
| `reserve_adequacy_indicators` | Reserve adequacy metrics |
| `syndicate_profile` | Individual syndicate profiles |

## Data Characteristics

- **Syndicates**: 10 sample Lloyd's syndicates (realistic numbers: 33, 623, 1183, 1910, 2010, 2525, 2791, 2987, 4242, 5000)
- **Years of Account**: 2018-2025
- **Reporting Year**: 2024
- **Currency**: Primarily GBP with multi-currency support (USD, EUR)
- **Random Seed**: All scripts use `np.random.seed(42)` for reproducibility

## Dependencies

All scripts require only standard Power BI Python dependencies:
- `pandas`
- `numpy`
- `datetime`
- `random`

No external data files are required - all data is synthetically generated.

## Notes

- Data is synthetic and for testing/development purposes only
- All monetary values are in the appropriate currency (GBP unless otherwise specified)
- Scripts can be modified to adjust data volumes, date ranges, or syndicate lists
- Each script is self-contained and can be used independently
