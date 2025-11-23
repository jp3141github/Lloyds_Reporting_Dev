# Power BI Data Scripts for Lloyd's Regulatory Reporting

This folder contains comprehensive Python scripts designed for use as Power BI data sources. Each script generates synthetic Lloyd's of London data for various regulatory reporting requirements.

## Overview

**Total Tables Available: 114+**

### Core Regulatory Returns (NEW)

| Category | Script | Tables | Priority |
|----------|--------|--------|----------|
| **LCR** (Lloyd's Capital Return) | `lcr_capital_return_powerbi.py` | 14 | CRITICAL |
| **SBF** (Syndicate Business Forecast) | `sbf_business_forecast_powerbi.py` | 10 | CRITICAL |
| **QMA** (Quarterly Monitoring A) | `qma_quarterly_monitoring_powerbi.py` | 10 | HIGH |
| **Bordereaux** (Premium/Claims) | `bordereaux_powerbi.py` | 5 | HIGH |

### Existing Returns

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

---

## NEW: Core Regulatory Returns

### 10. LCR - Lloyd's Capital Return (`lcr_capital_return_powerbi.py`)

**THE MOST IMPORTANT Lloyd's Return** - Annual capital setting submission.

| Table | Description |
|-------|-------------|
| `LCR_001_Control` | Syndicate metadata and submission control |
| `LCR_010_SCR_Summary` | Overall SCR calculation summary |
| `LCR_020_Premium_Risk` | Premium risk by line of business |
| `LCR_030_Reserve_Risk` | Reserve risk calculations |
| `LCR_040_Cat_Risk_Summary` | Catastrophe risk summary |
| `LCR_041_Cat_By_Peril` | Cat risk by peril (Wind, EQ, Flood, Terror, Cyber, Pandemic) |
| `LCR_050_Market_Risk` | Market risk (IR, Equity, Property, Spread, FX) |
| `LCR_060_Credit_Risk` | Counterparty default risk |
| `LCR_070_Operational_Risk` | Operational risk calculation |
| `LCR_080_Technical_Provisions` | TP with risk margin (4% to 6% CoC conversion) |
| `LCR_090_Own_Funds` | Own funds analysis (Tier 1, 2, 3) |
| `LCR_100_Coverage_Ratios` | Capital coverage ratios and adequacy |
| `LCR_110_YOA_Capital` | Year of Account capital allocation |
| `LCR_120_Diversification` | Risk diversification matrix |

**Key Calculations:**
- SCR Range: GBP 80-300M per syndicate
- Coverage Ratios: 1.2-2.5x (Lloyd's minimum: 1.0x, target: 1.35-1.50x)
- Risk Margin: 4% CoC (Solvency II) to 6% CoC (Lloyd's) conversion

### 11. SBF - Syndicate Business Forecast (`sbf_business_forecast_powerbi.py`)

**Three-year business plan** required for all syndicates.

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

**Typical Parameters:**
- Growth Rates: -5% to +20% annual
- Loss Ratios: 50-75% by LOB
- Combined Ratios: 85-102%

### 12. QMA - Quarterly Monitoring Return Part A (`qma_quarterly_monitoring_powerbi.py`)

**Primary quarterly financial return** - backbone of Lloyd's monitoring.

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

**Submission Timing:** T+30 business days after quarter-end

### 13. Bordereaux - Premium & Claims (`bordereaux_powerbi.py`)

**Transaction-level reporting** for delegated authorities - following Lloyd's CRS v5.2.

| Table | Description |
|-------|-------------|
| `Premium_Bordereaux` | Policy-level premium transactions (500+ records) |
| `Claims_Bordereaux` | Claim-level details (300+ records) |
| `Risk_Bordereaux` | Risk exposure summary |
| `Coverholder_Summary` | Performance by coverholder |
| `Contract_Performance` | TPA/Coverholder contract metrics |

**Lloyd's Identifiers Generated:**
- UMR Format: `B2024A1234567` (Broker + Year + Alpha + Number)
- OSN Format: `OSN12345678` (Original Signing Number)
- UCR Format: `B2024A1234567/2024/001` (UMR/Year/Sequence)

**CRS v5.2 Fields Include:** Gross/Net premium, Lloyd's participation %, brokerage, commission, taxes, ALAE, defence costs, currencies, FX rates

---

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
