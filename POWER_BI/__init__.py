"""
Power BI Integration Scripts
============================

Python scripts designed for use as Power BI data sources.
Each script generates synthetic Lloyd's data for regulatory reporting dashboards.

Total Tables Available: 114+

Scripts:
--------
- rra_forms_powerbi: 14 RRA form tables
- lcr_capital_return_powerbi: 14 LCR tables
- sbf_business_forecast_powerbi: 10 SBF tables
- qma_quarterly_monitoring_powerbi: 10 QMA tables
- qmb_performance_monitoring_powerbi: 8 QMB tables
- solvency_claims_powerbi: 5 claims tables
- solvency_qsr_powerbi: 10 QSR tables
- solvency_asb_powerbi: 10 ASB tables
- fscs_data_powerbi: 2 FSCS tables
- liquidity_stress_powerbi: 5 liquidity tables
- bordereaux_powerbi: 5 bordereaux tables
- aad_reports_powerbi: 8 AAD tables
- sao_addendum_powerbi: 3 SAO tables
- rra_aggregator_powerbi: 5 aggregation tables

Usage in Power BI:
------------------
1. Go to Get Data > Python script
2. Copy and paste script contents
3. Select tables to import
4. Click Load

Note: Scripts are self-contained and require only pandas, numpy, datetime, random.
"""

__all__ = []
