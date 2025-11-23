# Lloyd's Reporting Inventory - Codebase Coverage Analysis

## Overview

This document provides a comprehensive comparison between the Lloyd's regulatory reporting requirements (as listed on [Lloyd's Reporting and Disclosure page](https://www.lloyds.com/conducting-business/regulatory-information/solvency-ii/tools-and-resources/syndicate-workstreams/reporting-and-disclosure)) and what is currently implemented in this codebase.

**Analysis Date:** 2024-11-23
**Source:** Lloyd's official documentation, PRA requirements, and codebase audit

---

## Executive Summary

| Status | Count | Description |
|--------|-------|-------------|
| **Fully Implemented** | 12 | Complete Python/R and Power BI support |
| **Partially Implemented** | 4 | Some forms/tables available, gaps remain |
| **Not Implemented** | 15+ | Referenced but not yet built |

---

## Complete Inventory Table

### Legend
- **Status**: FULL = Fully Implemented, PARTIAL = Partially Implemented, NONE = Not Implemented
- **Tables**: Number of forms/tables covered

---

## SOLVENCY II PILLAR 3 RETURNS (Submitted via CMR)

| Return Code | Return Name | Frequency | Status | Tables | Notes |
|-------------|-------------|-----------|--------|--------|-------|
| **QSR** | Quarterly Solvency Return | Quarterly | **FULL** | 12 | `solvency_qsr_powerbi.py`, Python/R scripts |
| **ASR** | Annual Solvency Return (Part A) | Annual | **PARTIAL** | ~10 | Specification file exists (`ASR Return Specifications Annual 2024 2.xlsx`), but only partial implementation. ASR has 50+ forms total. |
| **ASB** | Annual Solvency Balance Sheet (Part B) | Annual | **FULL** | 10 | `Solvency_II_ASB_Python/`, `Solvency_II_ASB_R/`, `solvency_asb_powerbi.py` |
| **QAD** | Quarterly Asset Data | Quarterly | **PARTIAL** | 0 | Specification file exists, referenced in docs, no generator |
| **AAD** | Annual Asset Data | Annual | **FULL** | 8 | `aad_reports_powerbi.py` - Forms 230, 233, 235, 236, 237, 238 |

### QSR Forms Implemented (12 tables)

| Form Code | EIOPA Template | Description | Status |
|-----------|----------------|-------------|--------|
| QSR 002 | S.02.01.02 | Overall Balance Sheet | FULL |
| QSR 220 | S.23.01.01 | Own Funds | FULL |
| QSR 240 | S.17.01.02 | Non-Life Technical Provisions | FULL |
| QSR 280/283 | S.12.01.02 | Life Technical Provisions | FULL |
| QSR 291 | S.41.01.11 | Operational Risk | FULL |
| QSR 292 | S.14.01.10.01 | Market Risk | FULL |
| QSR 293 | S.38.01.10.01 | Counterparty Default Risk | FULL |
| QSR 440 | S.05.01.02.01 | Non-Life Insurance Claims | FULL |
| QSR 450 | S.05.01.02.02 | Life Insurance Information | FULL |
| QSR 510/511 | S.28.01.01 | Minimum Capital Requirement (MCR) | FULL |

### ASR Forms - Status (50+ forms in full specification)

| Form Code | Description | Status |
|-----------|-------------|--------|
| ASR 002 | Balance Sheet | PARTIAL (via QSR) |
| ASR 220 | Own Funds | PARTIAL (via QSR) |
| ASR 225-228 | Variation Analysis | NONE |
| ASR 240-249 | Technical Provisions | PARTIAL |
| ASR 251 | Top Underwriting Risks | NONE |
| ASR 260-269 | Claims Development Triangles | PARTIAL (via ASB) |
| Other forms | 30+ additional forms | NONE |

### AAD Forms Implemented (8 tables)

| Form Code | EIOPA Template | Description | Status |
|-----------|----------------|-------------|--------|
| AAD 230 | S.06.02.01 | Open Market Value of Investments | FULL |
| AAD 233 | S.08.01.01 | Off-Balance Sheet Items | FULL |
| AAD 235 | S.09.01.01 | Derivatives | FULL |
| AAD 236 | S.06.03.01 | Collective Investment Undertakings | FULL |
| AAD 237 | S.10.01.01 | Structured Products | FULL |
| AAD 238 | S.11.01.01 | Securities Lending and Repos | FULL |

### QAD Forms - Status

| Form Code | Description | Status |
|-----------|-------------|--------|
| QAD 230 | Asset Valuation | NONE (spec file exists) |
| QAD 233 | Derivatives | NONE |
| QAD 235 | Derivatives Detail | NONE |
| QAD 236 | Investment Fund Look-Through | NONE |

---

## LLOYD'S RESERVING RETURNS (Submitted via CMR)

| Return Code | Return Name | Frequency | Status | Tables | Notes |
|-------------|-------------|-----------|--------|--------|-------|
| **RRA** | Reserving Return Annual | Annual | **FULL** | 14 | `rra_forms_powerbi.py`, Python/R scripts, full data generators |
| **RRQ** | Reserving Return Quarterly | Quarterly | **FULL** | 14 | Same structure as RRA, quarterly variant |

### RRA/RRQ Forms Implemented (14 forms each)

| Form Code | Description | Python | R | Data |
|-----------|-------------|--------|---|------|
| RRA 010 | Control Data | FULL | FULL | CSV |
| RRA 020 | Exchange Rates | Data only | Data only | CSV |
| RRA 071 | SCOB Mapping | Data only | Data only | CSV |
| RRA 081 | Reserving Class Information | Data only | Data only | CSV |
| RRA 091 | LPT Transfers | Data only | Data only | CSV |
| RRA 193 | Net Claims Development | FULL | FULL | CSV |
| RRA 194 | Gross Claims Development | Data only | Data only | CSV |
| RRA 291 | Gross Premium & IBNR | FULL | FULL | CSV |
| RRA 292 | Net Premium & IBNR | FULL | FULL | CSV |
| RRA 293 | Outstanding & IBNR (<20 PYoA) | Data only | Data only | CSV |
| RRA 294 | Catastrophe IBNR | Data only | Data only | CSV |
| RRA 295 | ULAE Reserves | Data only | Data only | CSV |
| RRA 391 | IELR Analysis | Data only | Data only | CSV |
| RRA 910 | Additional Information | Data only | Data only | CSV |
| RRA 990 | Validation Summary | FULL | FULL | CSV |

---

## QUARTERLY MONITORING RETURNS (Submitted via MDC)

| Return Code | Return Name | Frequency | Status | Tables | Notes |
|-------------|-------------|-----------|--------|--------|-------|
| **QMA** | Quarterly Monitoring Return Part A | Quarterly | **FULL** | 10 | `qma_quarterly_monitoring_powerbi.py` |
| **QMB** | Quarterly Monitoring Return Part B | Quarterly | **NONE** | 0 | Not implemented - class of business analysis |
| **QMA Delta** | Quarterly Movement Analysis | Quarterly | **NONE** | 0 | Not implemented |
| **QMC** | Quarterly Solvency II Balance Sheet | Quarterly | **NONE** | 0 | Not implemented |

### QMA Forms Implemented (10 tables)

| Table Code | Description | Status |
|------------|-------------|--------|
| QMA 001 | Control/Submission Metadata | FULL |
| QMA 002/010 | Balance Sheet | FULL |
| QMA 020 | Profit & Loss Statement | FULL |
| QMA 030 | Cash Flow Statement | FULL |
| QMA 040/104 | Technical Account by LOB | FULL |
| QMA 050 | Investment Portfolio | FULL |
| QMA 060 | Reinsurance Assets | FULL |
| QMA 070 | Creditors Analysis | FULL |
| QMA 080 | Capital Position | FULL |
| QMA 090 | Key Ratios/KPIs | FULL |
| QMA 201 | Asset Side Detail | NONE |
| QMA 205 | Liability Side Detail | NONE |
| QMA 650 | Quarterly Technical Account | NONE |

### QMB Forms - Not Implemented (87+ forms in total)

| Form Range | Description | Status |
|------------|-------------|--------|
| QMB 100 | Pure YoA Technical Account | NONE |
| QMB 105 | Class of Business Detail | NONE |
| QMB 105s | Reinsurance by Currency/YoA | NONE |
| Others | 80+ additional forms | NONE |

---

## LLOYD'S CAPITAL & BUSINESS PLANNING RETURNS

| Return Code | Return Name | Frequency | Status | Tables | Notes |
|-------------|-------------|-----------|--------|--------|-------|
| **LCR** | Lloyd's Capital Return | Annual | **FULL** | 14 | `lcr_capital_return_powerbi.py` |
| **SBF** | Syndicate Business Forecast | Annual | **FULL** | 10 | `sbf_business_forecast_powerbi.py` |
| **LCM** | Lloyd's Capital Model (detailed) | Annual | **NONE** | 0 | Complex internal model submission |
| **LSM** | Lloyd's Standard Model | Annual | **NONE** | 0 | Standard formula variant |
| **ECA** | Economic Capital Assessment | Annual | **NONE** | 0 | Capital assessment process |

### LCR Forms Implemented (14 tables)

| Table Code | Description | Status |
|------------|-------------|--------|
| LCR 001 | Control Data | FULL |
| LCR 010 | SCR Summary | FULL |
| LCR 020 | Premium Risk | FULL |
| LCR 030 | Reserve Risk | FULL |
| LCR 040 | Catastrophe Risk Summary | FULL |
| LCR 041 | Catastrophe Risk by Peril | FULL |
| LCR 050 | Market Risk | FULL |
| LCR 060 | Credit Risk | FULL |
| LCR 070 | Operational Risk | FULL |
| LCR 080 | Technical Provisions | FULL |
| LCR 090 | Own Funds | FULL |
| LCR 100 | Coverage Ratios | FULL |
| LCR 110 | YoA Capital Allocation | FULL |
| LCR 120 | Diversification Matrix | FULL |
| LCR 561 | Net RI/Net Acquisition Costs | NONE |
| LCR 570 | uSCR (consistent with QSR) | NONE |

### SBF Forms Implemented (10 tables)

| Table Code | Description | Status |
|------------|-------------|--------|
| SBF 001 | Control Data | FULL |
| SBF 010 | Income Statement (3-year) | FULL |
| SBF 020 | Premium Forecast | FULL |
| SBF 030 | Claims Forecast | FULL |
| SBF 040 | Expense Budget | FULL |
| SBF 050 | Capacity Plan | FULL |
| SBF 060 | Reinsurance Strategy | FULL |
| SBF 070 | Investment Income | FULL |
| SBF 080 | Combined Ratios | FULL |
| SBF 090 | Stress Scenarios | FULL |
| SBF 420 | Capacity Number | NONE |

---

## PILLAR 3 PUBLIC DISCLOSURES

| Return Code | Return Name | Frequency | Status | Notes |
|-------------|-------------|-----------|--------|-------|
| **SFCR** | Solvency and Financial Condition Report | Annual | **NONE** | Public disclosure document - qualitative |
| **RSR** | Regular Supervisory Report | Annual | **NONE** | Confidential PRA report - qualitative |
| **ORSA** | Own Risk and Solvency Assessment | Annual | **NONE** | Internal risk assessment |

---

## OTHER LLOYD'S RETURNS

| Return Code | Return Name | Frequency | Status | Notes |
|-------------|-------------|-----------|--------|-------|
| **SAO Addendum** | Signing Actuary Opinion Addendum | Annual | **FULL** | `sao_addendum_powerbi.py` - Forms 090, 100, Mappings |
| **FSCS** | Financial Services Compensation Scheme | Annual | **FULL** | `fscs_data_powerbi.py` |
| **Liquidity Stress** | Liquidity Stress Test | Periodic | **FULL** | `liquidity_stress_powerbi.py` |
| **Bordereaux** | Premium/Claims Bordereaux (CRS v5.2) | Monthly/Quarterly | **FULL** | `bordereaux_powerbi.py` |
| **GQD** | Gross Quarterly Data | Quarterly | **NONE** | Not implemented |
| **Flash Report** | Rapid Business Metrics | Monthly | **NONE** | Not implemented |
| **QCT** | Quarterly Claims Triangles | Quarterly | **NONE** | Not implemented |

---

## TERRITORY-SPECIFIC RETURNS (Not Implemented)

| Return | Territory | Status | Notes |
|--------|-----------|--------|-------|
| US Trust Fund Returns | USA | NONE | US regulatory filing |
| Canadian Trust Fund Returns | Canada | NONE | Canadian regulatory filing |
| Lloyd's Japan Returns | Japan | NONE | Japanese regulatory filing |
| Lloyd's Singapore Returns | Singapore | NONE | Singapore regulatory filing |
| NAIC Returns | USA | NONE | US state-level reporting |
| Situs Reporting | USA | NONE | US surplus lines |
| TRIA Returns | USA | NONE | Terrorism insurance reporting |
| Tax Returns (Multi) | Various | NONE | Tax compliance |

---

## GOVERNANCE & ESG RETURNS (Not Implemented)

| Return | Status | Notes |
|--------|--------|-------|
| TCFD/Climate Risk Disclosure | NONE | Climate risk reporting |
| ESG Reporting | NONE | Environmental, Social, Governance |
| Risk Registers | NONE | Internal risk management |
| DUA System Submissions | NONE | Delegated Underwriting Authority |

---

## SUMMARY BY STATUS

### FULLY IMPLEMENTED (12 Returns)

| Return | Tables | Primary Files |
|--------|--------|---------------|
| QSR | 12 | `solvency_qsr_powerbi.py`, `Solvency_II_QSR_Reporting/` |
| ASB | 10 | `solvency_asb_powerbi.py`, `Solvency_II_ASB_Python/` |
| AAD | 8 | `aad_reports_powerbi.py` |
| RRA | 14 | `rra_forms_powerbi.py`, `python_scripts/forms/` |
| RRQ | 14 | Same as RRA (quarterly variant) |
| QMA | 10 | `qma_quarterly_monitoring_powerbi.py` |
| LCR | 14 | `lcr_capital_return_powerbi.py` |
| SBF | 10 | `sbf_business_forecast_powerbi.py` |
| SAO Addendum | 3 | `sao_addendum_powerbi.py` |
| FSCS | 2 | `fscs_data_powerbi.py` |
| Liquidity Stress | 5 | `liquidity_stress_powerbi.py` |
| Bordereaux | 5 | `bordereaux_powerbi.py` |

**Total Fully Implemented Tables: 107+**

### PARTIALLY IMPLEMENTED (4 Returns)

| Return | Implemented | Missing | Gap |
|--------|-------------|---------|-----|
| ASR | ~10 forms (via QSR/ASB) | 40+ forms | Variation analysis, risk detail, comprehensive disclosure |
| QAD | 0 (spec only) | 6 forms | Full quarterly asset data |
| RRA Processors | 5 forms with processors | 9 forms need processors | Form-specific validation and calculations |
| QMA Detail | 10 basic forms | 77+ detail forms | QMA201, 205, 650, full detail |

### NOT IMPLEMENTED (15+ Returns)

| Category | Returns |
|----------|---------|
| Monitoring | QMB, QMA Delta, QMC, GQD, QCT, Flash |
| Capital | LCM (detailed), LSM, ECA |
| Disclosure | SFCR, RSR, ORSA |
| Territory | US, Canada, Japan, Singapore returns |
| Other | Tax, TCFD/ESG, Risk Registers, DUA |

---

## RECOMMENDATIONS

### High Priority (Regulatory Critical)
1. **QAD Generator** - Complete the quarterly asset data return
2. **ASR Forms** - Add remaining 40+ annual solvency forms
3. **QMB Generator** - Class of business analysis forms

### Medium Priority (Operational Value)
4. **SFCR Template** - Public disclosure document structure
5. **LCM Detailed** - Full internal model submission
6. **QMA Detail Forms** - Forms 201, 205, 650

### Lower Priority (Specialist Use)
7. Territory-specific returns (US, Canada, etc.)
8. Tax reporting integrations
9. ESG/TCFD frameworks

---

## Sources

- [Lloyd's Reporting and Disclosure](https://www.lloyds.com/conducting-business/regulatory-information/solvency-ii/tools-and-resources/syndicate-workstreams/reporting-and-disclosure)
- [Lloyd's Business Timetable](https://www.lloyds.com/tools-and-systems/business-timetable)
- [Lloyd's QMA Information](https://www.lloyds.com/market-resources/reporting-rationalisation/qma)
- [Lloyd's Solvency II Technical Provisions Guidance 2024](https://assets.lloyds.com/media/fd04de25-80f8-4d72-a0c3-8af9bc6cece7/Lloyd's%20Solvency%20II%20Technical%20Provisions%20Guidance%20-%202024.pdf)
- [PRA Solvency II Reporting PS3/24](https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/review-of-solvency-ii-reporting-disclosure-phase-2-near-final-policy-statement)
- [Lloyd's SFCR 2024](https://assets.lloyds.com/media-651c0e64-c1d0-4f97-90f7-883c69fe2ef2/598c5a1d-4d9f-4886-ab45-fdddac2861ff/SFCR%202024%20-%20FINAL%20(PwC%20Signed).pdf)

---

**Document Version:** 1.0
**Created:** 2024-11-23
**Maintained By:** Lloyd's Development Team
