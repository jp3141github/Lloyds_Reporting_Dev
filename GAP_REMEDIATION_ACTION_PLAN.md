# Lloyd's Reporting Gap Remediation Action Plan

## Executive Summary

This action plan addresses the 6 key gaps identified in the Lloyd's reporting codebase inventory:

| Gap | Current State | Target State | Priority | Est. Effort |
|-----|---------------|--------------|----------|-------------|
| **ASR** | ~10 forms (via QSR/ASB) | 50+ forms | **CRITICAL** | 8-10 weeks |
| **QAD** | Spec file only | 6 forms complete | **HIGH** | 2-3 weeks |
| **QMB** | None | 87+ forms | **HIGH** | 10-12 weeks |
| **SFCR/RSR** | None | Template structure | **MEDIUM** | 4-5 weeks |
| **Territory Returns** | None | 4 territories | **MEDIUM** | 6-8 weeks |
| **LCM/LSM** | None | Full submission | **HIGH** | 6-8 weeks |

**Total Estimated Effort: 36-46 weeks (9-12 months)**

---

## Gap 1: ASR (Annual Solvency Return) - CRITICAL

### Current State
- ~10 forms partially covered via QSR and ASB implementations
- ASR specification file exists: `Solvency II Pillar 3 - ASR Return Specifications Annual 2024 2.xlsx`
- Missing: 40+ forms including variation analysis, risk reporting, comprehensive disclosure

### Target State
Complete implementation of all 50+ ASR forms aligned with EIOPA Solvency II templates.

### Required Forms (Grouped by Function)

#### Group 1: Balance Sheet & Own Funds (Already Partially Done)
| Form | EIOPA Template | Description | Status | Action |
|------|----------------|-------------|--------|--------|
| ASR 002 | S.02.01.02 | Balance Sheet | PARTIAL | Extend from QSR |
| ASR 220 | S.23.01.01 | Own Funds | PARTIAL | Extend from QSR |
| ASR 221-224 | S.23.02-05 | Own Funds Detail | NONE | **NEW** |

#### Group 2: Technical Provisions (Priority)
| Form | EIOPA Template | Description | Status | Action |
|------|----------------|-------------|--------|--------|
| ASR 240 | S.17.01.02 | Non-Life TP by LoB | PARTIAL | Extend |
| ASR 241-244 | S.17.02-03 | Non-Life TP Detail | NONE | **NEW** |
| ASR 280-283 | S.12.01-02 | Life TP | PARTIAL | Extend |

#### Group 3: Variation Analysis (NEW - Critical)
| Form | EIOPA Template | Description | Status | Action |
|------|----------------|-------------|--------|--------|
| ASR 225 | S.29.01 | Excess Assets over Liabilities | NONE | **NEW** |
| ASR 226 | S.29.02 | Excess Assets - Detail | NONE | **NEW** |
| ASR 227 | S.29.03 | Variation Analysis - Investment | NONE | **NEW** |
| ASR 228 | S.29.04 | Variation Analysis - TP | NONE | **NEW** |

#### Group 4: Premiums, Claims & Expenses
| Form | EIOPA Template | Description | Status | Action |
|------|----------------|-------------|--------|--------|
| ASR 440 | S.05.01.02.01 | Non-Life Premium/Claims | PARTIAL | Extend |
| ASR 441 | S.05.02 | Premium by Country | NONE | **NEW** |

#### Group 5: Claims Development Triangles
| Form | EIOPA Template | Description | Status | Action |
|------|----------------|-------------|--------|--------|
| ASR 260-269 | S.19.01 | Claims Development | PARTIAL via ASB | Review/Extend |

#### Group 6: Risk Reporting (NEW)
| Form | EIOPA Template | Description | Status | Action |
|------|----------------|-------------|--------|--------|
| ASR 251 | S.21.01 | Top Underwriting Risks | NONE | **NEW** |
| ASR 252 | S.21.02 | Risk Distribution | NONE | **NEW** |
| ASR 253 | S.21.03 | Non-Life Distribution | NONE | **NEW** |

#### Group 7: SCR & MCR
| Form | EIOPA Template | Description | Status | Action |
|------|----------------|-------------|--------|--------|
| ASR 290 | S.25.01 | SCR - Standard Formula | NONE | **NEW** |
| ASR 291 | S.25.02 | SCR - Partial IM | NONE | **NEW** |
| ASR 292 | S.25.03 | SCR - Full IM | NONE | **NEW** |
| ASR 510 | S.28.01 | MCR - Non-Life | PARTIAL | Extend |

#### Group 8: Reinsurance
| Form | EIOPA Template | Description | Status | Action |
|------|----------------|-------------|--------|--------|
| ASR 300-310 | S.30-31 | Reinsurance Program | NONE | **NEW** |

### Implementation Plan

#### Phase ASR-1: Core Forms Extension (Weeks 1-3)
**Deliverables:**
1. `asr_002_balance_sheet.py` - Extended balance sheet with full disclosure
2. `asr_220_own_funds.py` - Own funds with tier breakdown
3. `asr_240_tp_nonlife.py` - Non-life technical provisions
4. `asr_280_tp_life.py` - Life technical provisions

**Technical Approach:**
```python
# asr_reports_powerbi.py - Main ASR generator
class ASRReportGenerator:
    def __init__(self, syndicate_id, reporting_year):
        self.syndicate = syndicate_id
        self.year = reporting_year
        self.qsr_data = load_qsr_data()  # Reuse QSR data
        self.asb_data = load_asb_data()  # Reuse ASB data

    def generate_asr_002(self): pass
    def generate_asr_220_224(self): pass
    def generate_asr_240_244(self): pass
    # ... 50+ form methods
```

**Effort:** 3 weeks (2 developers)

#### Phase ASR-2: Variation Analysis (Weeks 4-5)
**Deliverables:**
1. `asr_225_excess_assets.py` - Excess of assets over liabilities
2. `asr_226_228_variation.py` - Variation analysis forms

**Calculation Logic:**
- Compare opening vs closing balance sheet
- Analyze drivers of change: investment returns, TP movements, FX, etc.
- Link to QMA movements

**Effort:** 2 weeks (1 developer)

#### Phase ASR-3: Risk Reporting (Weeks 6-7)
**Deliverables:**
1. `asr_251_top_risks.py` - Top 20 underwriting risks
2. `asr_252_253_risk_distribution.py` - Risk distribution by SII LoB

**Data Requirements:**
- Link to bordereaux for policy-level data
- Aggregate by risk code, geography, peril

**Effort:** 2 weeks (1 developer)

#### Phase ASR-4: SCR Disclosure (Weeks 8-9)
**Deliverables:**
1. `asr_290_292_scr.py` - SCR forms (Standard Formula, Partial IM, Full IM)
2. Link to existing LCR SCR calculations

**Effort:** 2 weeks (1 developer)

#### Phase ASR-5: Integration & Testing (Week 10)
**Deliverables:**
1. `asr_complete_powerbi.py` - Unified Power BI generator
2. R equivalents for all Python scripts
3. Validation suite
4. Documentation

**Effort:** 1 week (2 developers)

### Dependencies
- QSR implementation (complete)
- ASB implementation (complete)
- LCR implementation (complete for SCR data)

### Success Criteria
- [ ] All 50+ ASR forms have generators
- [ ] Python and R parity
- [ ] Power BI integration tested
- [ ] Cross-form validation rules implemented
- [ ] Documentation complete

---

## Gap 2: QAD (Quarterly Asset Data) - HIGH

### Current State
- Specification file exists: `Solvency II Pillar 3 - QAD Return Specifications Q3 2025.xlsx`
- AAD (Annual) is fully implemented with 8 forms
- QAD quarterly equivalent not implemented

### Target State
Complete QAD implementation mirroring AAD structure for quarterly reporting.

### Required Forms

| Form | EIOPA Template | Description | Status | Action |
|------|----------------|-------------|--------|--------|
| QAD 230 | S.06.02.01 | Asset Valuation | NONE | **NEW** |
| QAD 233 | S.08.01.01 | Derivatives | NONE | **NEW** |
| QAD 235 | S.09.01.01 | Derivatives Income | NONE | **NEW** |
| QAD 236 | S.06.03.01 | Look-Through CIUs | NONE | **NEW** |
| QAD 237 | S.10.01.01 | Securities Lending | NONE | **NEW** |
| QAD 238 | S.11.01.01 | Assets Held as Collateral | NONE | **NEW** |

### Implementation Plan

#### Phase QAD-1: Clone AAD Structure (Week 1)
**Approach:** Copy AAD implementation with quarterly parameters

```python
# qad_reports_powerbi.py
# Clone from aad_reports_powerbi.py with:
# - Quarterly date parameters
# - Q1/Q2/Q3/Q4 period handling
# - Quarterly validation rules

class QADReportGenerator(AADReportGenerator):
    def __init__(self, syndicate_id, quarter, year):
        super().__init__(syndicate_id, year)
        self.quarter = quarter
        self.as_at_date = self._get_quarter_end(quarter, year)

    def _get_quarter_end(self, q, y):
        quarter_ends = {1: '03-31', 2: '06-30', 3: '09-30', 4: '12-31'}
        return f"{y}-{quarter_ends[q]}"
```

**Effort:** 1 week (1 developer)

#### Phase QAD-2: Quarterly Specifics (Week 2)
**Deliverables:**
1. Quarter-end date handling
2. FX rate source (Lloyd's quarterly bulletin rates)
3. Lloyd's Managed Investment Fund (LMIF) templates
4. Asynchronous return handling (playback summaries)

**Effort:** 1 week (1 developer)

#### Phase QAD-3: R Parity & Testing (Week 3)
**Deliverables:**
1. `qad_reports.R` - R equivalent
2. Validation against AAD
3. Power BI integration
4. Documentation

**Effort:** 1 week (1 developer)

### Key Technical Requirements

**LMIF (Lloyd's Managed Investment Fund) Handling:**
```python
# Per Lloyd's guidance:
# - Level of look-through = "O"
# - CIC = "XL39"
# - Valuation in GBP only
# - Standard templates for LMIF funds

LMIF_TEMPLATE = {
    'level_of_look_through': 'O',
    'cic_code': 'XL39',
    'currency': 'GBP',
    'issuer_sector': 'NACE code required'  # GICS no longer accepted
}
```

### Dependencies
- AAD implementation (complete) - can clone directly

### Success Criteria
- [ ] All 6 QAD forms implemented
- [ ] Quarter-end date handling for Q1-Q4
- [ ] LMIF templates complete
- [ ] Reconciles to AAD annual submission
- [ ] Python/R parity

---

## Gap 3: QMB (Quarterly Monitoring Part B) - HIGH

### Current State
- QMA (Part A) fully implemented with 10 tables
- QMB not implemented
- QMB is submitted via MDC platform

### Target State
Complete QMB implementation covering class of business analysis by pure year of account.

### Understanding QMB Structure

**Key Difference from QMA:**
- QMA = Reporting years (syndicates with open years)
- QMB = Pure underwriting years (last 5 active underwriting years)

### Required Forms (87+ total, prioritized below)

#### Priority 1: Core Performance Forms
| Form | Description | Status | Action |
|------|-------------|--------|--------|
| QMB 100 | Pure YoA Technical Account | NONE | **NEW** |
| QMB 105 | Premiums/Claims/Expenses by CoB/Currency/YoA | NONE | **NEW** |
| QMB 105s | Reinsurance by Currency/YoA | NONE | **NEW** |

#### Priority 2: Class of Business Detail
| Form | Description | Status | Action |
|------|-------------|--------|--------|
| QMB 110-119 | Lloyd's Risk Code breakdown | NONE | **NEW** |
| QMB 120-129 | Distribution channel analysis | NONE | **NEW** |

#### Priority 3: Year of Account Analysis
| Form | Description | Status | Action |
|------|-------------|--------|--------|
| QMB 200-219 | YoA performance by quarter | NONE | **NEW** |
| QMB 220-239 | YoA claims development | NONE | **NEW** |

### Implementation Plan

#### Phase QMB-1: Core Structure (Weeks 1-3)
**Deliverables:**
1. `qmb_100_technical_account.py` - Pure YoA technical account
2. `qmb_105_cob_analysis.py` - Class of business breakdown
3. `qmb_105s_reinsurance.py` - RI by currency/YoA

**Data Model:**
```python
# QMB requires granular data by:
# - Pure Year of Account (2020, 2021, 2022, 2023, 2024)
# - Lloyd's Risk Code (PR100, PP200, etc.)
# - Distribution Channel (Open Market, Coverholder, Lineslip)
# - Currency (GBP, USD, EUR, etc.)
# - Quarter (Q1-Q4)

class QMBDataGenerator:
    def __init__(self, syndicate_id, quarter, year):
        self.syndicate = syndicate_id
        self.quarter = quarter
        self.year = year
        self.active_yoas = self._get_active_yoas()  # Last 5 years

    def _get_active_yoas(self):
        return list(range(self.year - 4, self.year + 1))

    def generate_qmb_100(self):
        """Pure YoA Technical Account"""
        data = []
        for yoa in self.active_yoas:
            row = {
                'syndicate': self.syndicate,
                'yoa': yoa,
                'gross_premium': self._calc_gwp(yoa),
                'ri_premium': self._calc_ri_premium(yoa),
                'net_premium': self._calc_nwp(yoa),
                'claims_paid': self._calc_claims_paid(yoa),
                'claims_outstanding': self._calc_os(yoa),
                'acquisition_costs': self._calc_acq_costs(yoa),
                'admin_expenses': self._calc_admin(yoa),
                # ... etc
            }
            data.append(row)
        return pd.DataFrame(data)
```

**Effort:** 3 weeks (2 developers)

#### Phase QMB-2: Risk Code Breakdown (Weeks 4-6)
**Deliverables:**
1. `qmb_110_risk_code.py` - Lloyd's Risk Code analysis
2. Integration with Risk Code mapping file
3. Distribution channel breakdown

**Risk Code Integration:**
```python
# Use existing mapping file
RISK_CODE_FILE = 'Files_for_Claude/Risk-code-mapping-and-descriptions-04062025.xlsx'

def load_risk_codes():
    return pd.read_excel(RISK_CODE_FILE)

def generate_qmb_110(syndicate, quarter, year):
    risk_codes = load_risk_codes()
    # Generate data by risk code...
```

**Effort:** 3 weeks (1 developer)

#### Phase QMB-3: YoA Development (Weeks 7-9)
**Deliverables:**
1. `qmb_200_yoa_performance.py` - YoA performance tracking
2. `qmb_220_yoa_claims.py` - Claims development by YoA

**Effort:** 3 weeks (1 developer)

#### Phase QMB-4: Integration (Weeks 10-12)
**Deliverables:**
1. `qmb_complete_powerbi.py` - Unified generator
2. R equivalents
3. Link to QMA for consistency checks
4. MDC format export
5. Documentation

**Effort:** 3 weeks (2 developers)

### Key Technical Considerations

**MDC Format Requirements:**
- QMB is submitted via MDC (Market Data Collection) platform
- Different format from CMR (Core Market Returns)
- May need specific export format

**Consistency with SBF:**
- QMB tracks actual performance
- SBF tracks forecast performance
- Need reconciliation views

### Dependencies
- QMA implementation (complete)
- Risk Code mapping file (exists)
- SBF implementation (complete for comparison)

### Success Criteria
- [ ] QMB 100, 105, 105s implemented
- [ ] Risk code breakdown complete
- [ ] YoA analysis forms complete
- [ ] Links to QMA for reconciliation
- [ ] Python/R parity
- [ ] MDC export format support

---

## Gap 4: SFCR/RSR - MEDIUM

### Current State
- No implementation
- Lloyd's publishes market-wide SFCR annually
- RSR requirement ceased 31 December 2023

### Target State
Template structure generator for SFCR content collection from syndicates.

### SFCR Structure (Required Sections)

Based on Solvency II Delegated Regulation Article 290-298:

| Section | Chapter | Description | Content Type |
|---------|---------|-------------|--------------|
| A | Business and Performance | Business overview, underwriting, investment | Qualitative + Data |
| B | System of Governance | Board structure, risk management, internal controls | Qualitative |
| C | Risk Profile | Underwriting, market, credit, liquidity, operational | Qualitative + Data |
| D | Valuation for Solvency | Assets, technical provisions, other liabilities | Data-heavy |
| E | Capital Management | Own funds, SCR, MCR | Data-heavy |
| - | Annexes | QRT templates (public subset) | Data |

### Note on RSR
**RSR is no longer required** - The requirement to submit the RSR ceased on 31 December 2023 per HMT Statutory Instrument. No implementation needed.

### Implementation Plan

#### Phase SFCR-1: Template Structure (Weeks 1-2)
**Deliverables:**
1. `sfcr_template_generator.py` - Markdown/DOCX template generator
2. Section placeholders with data hooks

```python
# sfcr_template_generator.py

class SFCRTemplateGenerator:
    def __init__(self, syndicate_id, year):
        self.syndicate = syndicate_id
        self.year = year

    def generate_section_a(self):
        """Business and Performance"""
        return {
            'a1_business': self._business_overview(),
            'a2_underwriting': self._underwriting_performance(),
            'a3_investment': self._investment_performance(),
            'a4_other': self._other_activities(),
            'a5_outlook': self._outlook_commentary()
        }

    def _underwriting_performance(self):
        # Pull from QMA/QMB data
        qma_data = load_qma_data(self.syndicate, self.year)
        return {
            'gwp': qma_data['gwp'],
            'nwp': qma_data['nwp'],
            'claims_ratio': qma_data['claims_ratio'],
            'combined_ratio': qma_data['combined_ratio'],
            'commentary': '[INSERT COMMENTARY]'
        }
```

**Effort:** 2 weeks (1 developer)

#### Phase SFCR-2: Data Integration (Weeks 3-4)
**Deliverables:**
1. Section D (Valuation) - Link to ASR/QSR data
2. Section E (Capital) - Link to LCR data
3. Annex QRTs - Public subset generation

**Public QRT Templates:**
- S.02.01.02 - Balance Sheet
- S.05.01.02 - Premiums, claims, expenses
- S.17.01.02 - Non-life technical provisions
- S.19.01.21 - Non-life claims development
- S.23.01.01 - Own funds
- S.25.01.21 - SCR

**Effort:** 2 weeks (1 developer)

#### Phase SFCR-3: Output Formats (Week 5)
**Deliverables:**
1. Markdown output (for Git version control)
2. DOCX output (for editing)
3. PDF generation (for publication)
4. XHTML for web publication

**Effort:** 1 week (1 developer)

### Key Technical Considerations

**Qualitative vs Quantitative:**
- Sections A, B, C are primarily qualitative (text)
- Sections D, E are primarily quantitative (data)
- Template should clearly mark what is auto-generated vs manual input

**Lloyd's Market Level:**
- SFCR is published at Lloyd's market level, not individual syndicate
- Syndicates contribute data which Lloyd's aggregates
- Our tool focuses on syndicate contribution, not market aggregation

### Dependencies
- QSR implementation (complete) - Section D data
- LCR implementation (complete) - Section E data
- ASR implementation (needed) - Full disclosure data

### Success Criteria
- [ ] Template structure for all 5 sections
- [ ] Auto-population of quantitative data
- [ ] Clear markers for manual input sections
- [ ] Multiple output format support
- [ ] Public QRT annex generation

---

## Gap 5: Territory Returns - MEDIUM

### Current State
- No territory-specific returns implemented
- Focus has been on UK/Lloyd's market level

### Target State
Support for US, Canada, Japan, Singapore regulatory requirements.

### Territory Requirements Summary

| Territory | Key Returns | Trust Fund | Regulatory Body |
|-----------|-------------|------------|-----------------|
| **USA** | US Situs, NAIC, TRIA | Lloyd's American Trust Fund (LATF) | State regulators |
| **Canada** | Canadian Situs | Lloyd's Canadian Trust Fund (LCTF) | OSFI/Provincial |
| **Japan** | Japan returns | Japan deposits | FSA Japan |
| **Singapore** | Singapore policies | Lloyd's Asia Trust | MAS |

### US Returns

#### US Situs Business
- Premium allocation by US state
- Surplus lines compliance
- US Trust Fund contributions

#### NAIC Returns
- NAIC annual statement format
- State-by-state filing requirements
- Surplus lines tax reporting

#### TRIA (Terrorism Risk Insurance Act)
- Terrorism insurance reporting
- TRIA certification
- Federal share calculations

### Implementation Plan

#### Phase TERR-1: US Situs (Weeks 1-3)
**Deliverables:**
1. `us_situs_reporting.py` - US situs premium allocation
2. State code mapping
3. Surplus lines tax calculation

```python
# us_situs_reporting.py

US_STATES = [
    'AL', 'AK', 'AZ', ..., 'WY'  # 50 states + DC + territories
]

class USSitusGenerator:
    def __init__(self, syndicate_id, year):
        self.syndicate = syndicate_id
        self.year = year

    def allocate_premium_by_state(self, policy_data):
        """Allocate premium to US states based on risk location"""
        state_allocation = {}
        for policy in policy_data:
            if policy['risk_location_country'] == 'US':
                state = policy['risk_location_state']
                state_allocation[state] = (
                    state_allocation.get(state, 0) +
                    policy['premium']
                )
        return state_allocation

    def calculate_surplus_lines_tax(self, state, premium):
        """Calculate state-specific surplus lines tax"""
        tax_rates = load_surplus_lines_rates()
        return premium * tax_rates.get(state, 0.03)
```

**Effort:** 3 weeks (1 developer)

#### Phase TERR-2: Canada (Weeks 4-5)
**Deliverables:**
1. `canadian_situs_reporting.py` - Canadian situs reporting
2. Provincial allocation
3. LCTF contribution calculations

**Effort:** 2 weeks (1 developer)

#### Phase TERR-3: Asia Pacific (Weeks 6-8)
**Deliverables:**
1. `japan_reporting.py` - Japan FSA requirements
2. `singapore_reporting.py` - MAS requirements
3. Asia trust fund allocations

**Effort:** 3 weeks (1 developer)

### Key Technical Considerations

**Crystal Platform:**
- Lloyd's Crystal provides territory-specific guidance
- Implementation should reference Crystal for rules

**Trust Fund Calculations:**
- Each territory has trust fund requirements
- Premium must be allocated to correct trust fund
- Maintain minimum balances

**Currency:**
- US: USD
- Canada: CAD
- Japan: JPY
- Singapore: SGD

### Dependencies
- Bordereaux implementation (complete) - Source of policy-level data
- Risk location coding in source data

### Success Criteria
- [ ] US state-by-state premium allocation
- [ ] Surplus lines tax calculations
- [ ] Canadian provincial reporting
- [ ] Japan FSA basic returns
- [ ] Singapore MAS basic returns
- [ ] Trust fund contribution calculations

---

## Gap 6: LCM/LSM (Capital Model Submissions) - HIGH

### Current State
- LCR implemented (high-level capital return)
- No detailed LCM (Lloyd's Catastrophe Model) submission
- No LSM (Lloyd's Standard Model) implementation

### Target State
Full support for both internal model (LCM) and standard model (LSM) capital submissions.

### Understanding LCM vs LSM

| Aspect | LCM (Internal Model) | LSM (Standard Model) |
|--------|---------------------|----------------------|
| **Users** | Most syndicates with approved internal models | SIABs, new entrants, smaller syndicates |
| **Approach** | Proprietary syndicate model | Lloyd's-provided standard formula |
| **Complexity** | High (1000+ parameters) | Medium (standardized templates) |
| **Submission** | Via MDC with supporting docs | Via SecureShare with LCR |

### LCM Components

#### Catastrophe Model Outputs
| Component | Description |
|-----------|-------------|
| Cat losses by peril | Wind, EQ, Flood, etc. |
| Exceedance probability curve | EP curve by peril |
| Aggregate loss distributions | AEP/OEP by return period |
| Sensitivity tests | +10% cat risk impact |

#### Required Forms
| Form | Description |
|------|-------------|
| LCM 313 | Catastrophe risk summary |
| LCM 314 | Peril-by-peril breakdown |
| LCM 315 | Regional exposure analysis |
| LCM 316 | Sensitivity results |

### LSM Components

Based on Lloyd's Standard Model Instructions:

| Risk Module | Calculation Basis |
|-------------|-------------------|
| Market Risk | Solvency II Standard Formula |
| Counterparty Default | Solvency II Standard Formula |
| Insurance Risk | Lloyd's bespoke methodology |
| Operational Risk | Lloyd's bespoke methodology |

### Implementation Plan

#### Phase LCM-1: Catastrophe Model Interface (Weeks 1-3)
**Deliverables:**
1. `lcm_cat_model.py` - Catastrophe model output generator
2. EP curve generation
3. Peril breakdown

```python
# lcm_cat_model.py

class LCMCatModelGenerator:
    def __init__(self, syndicate_id, year):
        self.syndicate = syndicate_id
        self.year = year

    def generate_ep_curve(self, peril):
        """Generate exceedance probability curve"""
        return_periods = [10, 25, 50, 100, 200, 250, 500, 1000]
        losses = []
        for rp in return_periods:
            loss = self._calculate_loss_at_rp(peril, rp)
            losses.append({
                'return_period': rp,
                'exceedance_prob': 1/rp,
                'aep_loss': loss['aep'],
                'oep_loss': loss['oep']
            })
        return pd.DataFrame(losses)

    def generate_form_313(self):
        """LCM Form 313 - Cat Risk Summary"""
        perils = ['NA_Hurricane', 'NA_Earthquake', 'EU_Windstorm',
                  'JP_Typhoon', 'JP_Earthquake', 'Flood', 'Terror', 'Cyber']

        summary = []
        for peril in perils:
            ep = self.generate_ep_curve(peril)
            summary.append({
                'peril': peril,
                'gross_100yr': ep[ep['return_period']==100]['aep_loss'].values[0],
                'net_100yr': self._apply_ri(peril, 100),
                'gross_250yr': ep[ep['return_period']==250]['aep_loss'].values[0],
                'net_250yr': self._apply_ri(peril, 250)
            })
        return pd.DataFrame(summary)
```

**Effort:** 3 weeks (1 developer)

#### Phase LCM-2: LSM Standard Formula (Weeks 4-6)
**Deliverables:**
1. `lsm_standard_model.py` - Full LSM implementation
2. Market risk (SII Standard Formula)
3. Insurance risk (Lloyd's method)
4. Operational risk (Lloyd's method)

**LSM Template Structure:**
```python
# lsm_standard_model.py

class LSMStandardModel:
    def __init__(self, syndicate_id, yoa, sbf_data):
        self.syndicate = syndicate_id
        self.yoa = yoa
        self.sbf = sbf_data  # Must align with SBF submission

    def calculate_market_risk(self):
        """Solvency II Standard Formula for Market Risk"""
        return {
            'interest_rate_risk': self._ir_risk(),
            'equity_risk': self._equity_risk(),
            'property_risk': self._property_risk(),
            'spread_risk': self._spread_risk(),
            'currency_risk': self._fx_risk(),
            'concentration_risk': self._concentration_risk(),
            'total_market_scr': self._aggregate_market_scr()
        }

    def calculate_insurance_risk(self):
        """Lloyd's bespoke Insurance Risk calculation"""
        return {
            'premium_risk': self._premium_risk_lloyds(),
            'reserve_risk': self._reserve_risk_lloyds(),
            'cat_risk': self._cat_risk_lloyds(),
            'total_insurance_scr': self._aggregate_insurance_scr()
        }

    def calculate_operational_risk(self):
        """Lloyd's bespoke Operational Risk"""
        # Based on premium and technical provisions
        op_premium = self.sbf['gwp'] * 0.03  # 3% of premium
        op_tp = self.sbf['technical_provisions'] * 0.003  # 0.3% of TP
        return max(op_premium, op_tp)

    def generate_lsm_return(self):
        """Complete LSM submission"""
        return {
            'market_risk': self.calculate_market_risk(),
            'cpd_risk': self.calculate_counterparty_risk(),
            'insurance_risk': self.calculate_insurance_risk(),
            'operational_risk': self.calculate_operational_risk(),
            'diversification': self._calculate_diversification(),
            'total_scr': self._aggregate_total_scr()
        }
```

**Effort:** 3 weeks (1 developer)

#### Phase LCM-3: Consistency & Validation (Weeks 7-8)
**Deliverables:**
1. LCR↔LSM consistency checks
2. SBF↔LSM premium reconciliation
3. QSR↔LSM risk margin check
4. SecureShare export format

**Consistency Rules:**
- Risk margin in LSM must match LCR and QSR
- Premium in LSM must match SBF
- Cat risk inputs must match LCM submission

**Effort:** 2 weeks (1 developer)

### Key Technical Considerations

**LSM Submission:**
- Upload to SecureShare "MRC Syndicate Capital Setting" folder
- Naming: `SYXXXX_EDY_SBFZ_LSM_YOA.xlsx`
- Due 3 days after SBF submission

**Currency:**
- All figures in GBP thousands
- Use Q2 FX rates for pre-year-end submissions

### Dependencies
- LCR implementation (complete)
- SBF implementation (complete)
- QSR implementation (complete for risk margin)

### Success Criteria
- [ ] LCM cat model forms (313-316) implemented
- [ ] EP curve generation
- [ ] LSM full implementation
- [ ] SII Standard Formula for Market/CPD risk
- [ ] Lloyd's method for Insurance/Op risk
- [ ] Consistency validation with LCR, SBF, QSR
- [ ] SecureShare export format

---

## Resource Requirements

### Development Team

| Role | FTE | Duration | Total |
|------|-----|----------|-------|
| Python Developer | 2 | 12 months | 24 person-months |
| R Developer | 1 | 8 months | 8 person-months |
| Actuarial SME | 0.5 | 6 months | 3 person-months |
| QA/Testing | 1 | 4 months | 4 person-months |
| Documentation | 0.5 | 3 months | 1.5 person-months |
| **Total** | - | - | **40.5 person-months** |

### Skills Required

| Skill | Gap Area |
|-------|----------|
| Solvency II expertise | ASR, SFCR, QAD |
| Actuarial methods | LCM, LSM |
| Lloyd's market knowledge | QMB, Territory |
| Python/pandas | All |
| R/tidyverse | All (parity) |
| Power BI | All |

---

## Timeline Summary

```
Month 1-2:   QAD (complete)
Month 2-4:   ASR Phase 1-2 (core forms, variation analysis)
Month 3-5:   QMB Phase 1-2 (core forms, risk codes)
Month 4-5:   SFCR (template structure)
Month 5-6:   ASR Phase 3-4 (risk, SCR)
Month 6-8:   QMB Phase 3-4 (YoA, integration)
Month 7-8:   LCM/LSM Phase 1-2 (cat model, standard formula)
Month 8-10:  Territory Returns (US, Canada)
Month 9-10:  LCM/LSM Phase 3 (validation)
Month 10-12: Territory Returns (Asia), Integration testing
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Lloyd's spec changes | Monitor market bulletins monthly |
| Scope creep | Strict prioritization, defer P3 items |
| R developer availability | Prioritize Python, R as secondary |
| Actuarial complexity | Engage external SME for LCM/LSM |
| Testing coverage | Automated validation suite early |

---

## Success Metrics

### Completion Targets

| Milestone | Target Date | Metric |
|-----------|-------------|--------|
| QAD Complete | Month 2 | 6/6 forms |
| ASR Complete | Month 6 | 50/50 forms |
| QMB Complete | Month 8 | 87/87 forms |
| SFCR Complete | Month 5 | 5/5 sections |
| Territory Complete | Month 12 | 4/4 territories |
| LCM/LSM Complete | Month 10 | Full submission |

### Quality Targets

- [ ] 100% Python/R parity for all new implementations
- [ ] >90% test coverage for core calculations
- [ ] All forms validated against Lloyd's specifications
- [ ] Zero critical defects in production

---

## Appendix: File Structure

```
Lloyds_Reporting_Dev/
├── POWER_BI/
│   ├── asr_reports_powerbi.py          # NEW - 50+ forms
│   ├── qad_reports_powerbi.py          # NEW - 6 forms
│   ├── qmb_reports_powerbi.py          # NEW - 87+ forms
│   ├── lcm_cat_model_powerbi.py        # NEW
│   └── lsm_standard_model_powerbi.py   # NEW
├── python_scripts/
│   ├── solvency_ii/
│   │   ├── asr/
│   │   │   ├── asr_002_balance_sheet.py
│   │   │   ├── asr_220_own_funds.py
│   │   │   ├── asr_225_228_variation.py
│   │   │   └── ...
│   │   ├── qad/
│   │   │   └── qad_reports.py
│   │   └── qmb/
│   │       ├── qmb_100_technical.py
│   │       ├── qmb_105_cob.py
│   │       └── ...
│   ├── capital/
│   │   ├── lcm_cat_model.py            # NEW
│   │   └── lsm_standard_model.py       # NEW
│   ├── territory/
│   │   ├── us_situs_reporting.py       # NEW
│   │   ├── canadian_reporting.py       # NEW
│   │   ├── japan_reporting.py          # NEW
│   │   └── singapore_reporting.py      # NEW
│   └── disclosure/
│       └── sfcr_template.py            # NEW
├── r_scripts/
│   └── [Mirror Python structure]
└── tests/
    ├── test_asr/
    ├── test_qad/
    ├── test_qmb/
    └── ...
```

---

## Sources

- [Lloyd's Reporting and Disclosure](https://www.lloyds.com/conducting-business/regulatory-information/solvency-ii/tools-and-resources/syndicate-workstreams/reporting-and-disclosure)
- [Lloyd's Business Timetable](https://www.lloyds.com/tools-and-systems/business-timetable)
- [Lloyd's Standard Model Instructions](https://assets.lloyds.com/media/53e1f74e-c873-4af8-ae57-7dc2df1c695d/Lloyd's%20Standard%20Model%20Instructions.pdf)
- [Lloyd's Capital Guidance February 2024](https://assets.lloyds.com/media/0a5cc3b2-8b60-4585-8db8-0cca63ec037e/Lloyd's%20Capital%20Guidance%20-%20February%202024.pdf)
- [ECA Process Guidance Manual 2024](https://assets.lloyds.com/media/b29dc3a4-2f2f-4d9e-8a2f-765d634d1267/ECA%20Process%20Guidance%20Manual_2025_Lloyds.com.pdf)
- [PRA PS3/24 Solvency II Reporting](https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/review-of-solvency-ii-reporting-disclosure-phase-2-near-final-policy-statement)
- [Lloyd's QMA Transformation](https://www.lloyds.com/market-resources/reporting-rationalisation/qma)
- [Lloyd's CMR Guidebook](https://assets.lloyds.com/assets/pdf-core-market-returns-cmr-cmr-guidebook/1/CMR-Guidebook.pdf)

---

**Document Version:** 1.0
**Created:** 2024-11-23
**Status:** APPROVED FOR IMPLEMENTATION
