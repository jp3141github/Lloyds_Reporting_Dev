# Power BI Visualization Guide - Simple Reference

**AAD and QAD files have been archived** and are not part of the Power BI workflow.

This guide shows which R and Python files create which visualizations in Power BI after connecting to synthetic data.

---

## 1. Solvency II Claims Processing

### Files:
- **Python**: `powerbi_python_example.py`
- **R**: `powerbi_r_example.R`

### What it creates:
- **5 data tables**: detailed_claims, by_syndicate, by_risk_code, by_claim_status, summary

### Visualizations you can create:
1. **Card visuals** - Total claims, total outstanding, total paid, total incurred
2. **Bar charts** - Claims by syndicate, claims by year of account
3. **Stacked column charts** - Claims by risk code and status
4. **Line charts** - Claims development over time
5. **Pie/Donut charts** - Claim status distribution
6. **Waterfall charts** - Movement in claims
7. **Treemap** - Outstanding amounts by risk code
8. **Table visuals** - Detailed claim information

---

## 2. RRA/RRQ Forms (Lloyd's Reserving Returns)

### Files:
- **Python**: `Python_Scripts/forms/` (rra_010_control.py, rra_193_net_claims.py, rra_291_gross_premium_ibnr.py)
- **R**: `R_Scripts/forms/` (rra_010_control.R, rra_193_net_claims.R)
- **Aggregator**: `utils/rra_aggregator.py` or `utils/rra_aggregator.R`

### What it creates:
- **RRA 010**: Control data and syndicate metadata
- **RRA 193**: Claims development triangles and chain ladder factors
- **RRA 291**: IBNR estimates and loss ratios
- **Portfolio Summary**: Overall metrics across all forms

### Visualizations you can create:
1. **Card visuals** - Total capacity, total IBNR, gross written premium
2. **Bar charts** - GWP by line of business, reserves by syndicate
3. **Line charts** - Loss ratio trends by year
4. **Matrix visuals** - Claims development triangles (rows = accident year, columns = development year)
5. **Heatmaps** - Development factors color-coded
6. **Gauge visuals** - Reserve adequacy ratios
7. **Scatter plots** - Claims maturity vs paid ratio
8. **Table visuals** - Detailed form data

---

## 3. FSCS (Financial Services Compensation Scheme)

### Files:
- **Python**: `FSCS_PowerBI/Python/powerbi_query.py`
- **R**: `FSCS_PowerBI/R/powerbi_query.R`

### What it creates:
- **1 dataset table**: Syndicate-level FSCS data with GWP and BEL

### Visualizations you can create:
1. **Card visuals** - Total GWP, total BEL, number of syndicates
2. **Bar charts** - GWP by syndicate, general vs life business
3. **Stacked bar charts** - GWP breakdown (general + life)
4. **Table visuals** - Syndicate details with managing agent
5. **Pie charts** - General business percentage
6. **Clustered column charts** - GWP vs BEL comparison

---

## 4. Liquidity Stress Testing

### Files:
- **Python**: `python_implementation/liquidity_stress_test.py`
- **R**: `r_implementation/liquidity_stress_test.R`

### What it creates:
- **Capital Position Table**: Solvency ratios by syndicate
- **Liquidity Breakdown Table**: Asset composition (liquid/illiquid/restricted)
- **Cashflow Summary Table**: Inflows and outflows
- **Stress Impact Table**: Baseline vs stressed scenarios
- **Dashboard Summary**: Key metrics

### Visualizations you can create:
1. **Card visuals** - Total FAL, average solvency ratio, number of compliant syndicates
2. **Bar charts** - Solvency ratios by syndicate (horizontal bars)
3. **Stacked bar charts** - Asset composition (liquid, illiquid, restricted %)
4. **Line charts** - Baseline vs stressed liquidity over time
5. **Area charts** - Cashflow projections
6. **Gauge visuals** - Solvency ratio targets
7. **Table visuals** - Risk metrics details

---

## 5. Solvency II QSR (Quarterly Solvency Returns)

### Files:
- **Python**: `Solvency_II_QSR_Reporting/Python/qsr_report_generator.py`
- **R**: `Solvency_II_QSR_Reporting/R/qsr_report_generator.R`

### What it creates:
- **QSR 002**: Balance sheet data
- **QSR 220**: Own funds composition
- **QSR 240**: Technical provisions
- **QSR 440**: Premiums and claims
- **QSR 29x**: Risk module calculations (market, operational, counterparty)
- **QSR 510**: MCR calculation
- **Solvency Ratios**: SCR and MCR coverage

### Visualizations you can create:
1. **Card visuals** - Total own funds, SCR, MCR, solvency ratios
2. **Bar charts** - SCR/MCR coverage ratios by syndicate
3. **Stacked bar charts** - Own funds by tier (Tier 1, 2, 3)
4. **Waterfall charts** - Balance sheet assets and liabilities
5. **Line charts** - Premium and claims trends over quarters
6. **Table visuals** - Technical provisions by line of business
7. **Donut charts** - Risk module composition (market, credit, underwriting)
8. **Gauge visuals** - SCR ratio (target 100%+)

---

## 6. Solvency II ASB (Annual Solvency Returns)

### Files:
- **Python**: `Solvency_II_ASB_Python/powerbi_asb_returns.py`
- **R**: `Solvency_II_ASB_R/powerbi_asb_returns.R`

### What it creates:
- **ASB 245/246/247**: Claims development triangles with reinsurance
- **ASB 248**: Inflation rates by line of business
- **Claims Summary**: Aggregated claims data
- **Development Analysis**: Claims development patterns
- **Metadata**: Syndicate information
- **Lines of Business**: EIOPA classification reference

### Visualizations you can create:
1. **Card visuals** - Total gross claims paid, reinsurance recoveries, RBNS claims
2. **Matrix visuals** - Claims development triangles (multi-year)
3. **Line charts** - Claims settlement patterns by development year
4. **Stacked area charts** - Gross vs net claims over time
5. **Bar charts** - Claims by line of business, claims by currency
6. **Line charts** - Inflation rates (historic vs expected)
7. **Table visuals** - Detailed claims by underwriting year
8. **Heatmaps** - Development factors by line of business

---

## Quick Reference Table

| Module | Python File | R File | Main Visualizations |
|--------|-------------|--------|---------------------|
| **Solvency II Claims** | powerbi_python_example.py | powerbi_r_example.R | Cards, bars, pie charts, waterfalls |
| **RRA/RRQ Forms** | Python_Scripts/utils/rra_aggregator.py | R_Scripts/utils/rra_aggregator.R | Triangles, heatmaps, gauges, trends |
| **FSCS** | FSCS_PowerBI/Python/powerbi_query.py | FSCS_PowerBI/R/powerbi_query.R | Cards, bars, stacked bars, tables |
| **Liquidity Stress** | python_implementation/liquidity_stress_test.py | r_implementation/liquidity_stress_test.R | Bars, stacked bars, line charts |
| **QSR Returns** | Solvency_II_QSR_Reporting/Python/qsr_report_generator.py | Solvency_II_QSR_Reporting/R/qsr_report_generator.R | Waterfalls, stacked bars, gauges |
| **ASB Returns** | Solvency_II_ASB_Python/powerbi_asb_returns.py | Solvency_II_ASB_R/powerbi_asb_returns.R | Triangles, heatmaps, line charts |

---

## How to Use in Power BI

### For Python:
1. Open Power BI Desktop
2. Get Data → More → Python script
3. Copy and paste the Python file contents
4. Update file paths in the script to match your system
5. Click OK and select tables to load
6. Create visualizations by dragging fields to the canvas

### For R:
1. Open Power BI Desktop
2. Get Data → More → R script
3. Copy and paste the R file contents
4. Update file paths in the script to match your system
5. Click OK and select tables to load
6. Create visualizations by dragging fields to the canvas

---

## Notes

- All files use **synthetic data** from the repository
- **AAD and QAD** specification files are now in `Files_for_Claude/Archive_AAD_QAD/` and not used
- Each module is **independent** - you can use them separately or together
- Both **Python and R** versions produce the same visualizations
- More detailed guides available in module-specific folders

---

**Last Updated**: 2025-11-21
**Repository**: Lloyds_Reporting_Dev
