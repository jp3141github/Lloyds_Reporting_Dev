# Implementation Roadmap

This document outlines the gaps between what's currently implemented and what's planned, along with a prioritized action plan for closing these gaps.

---

## Executive Summary

Based on the comprehensive codebase audit (2025-11-21), the repository has:
- ✅ **4 fully implemented modules** (Solvency II QSR, Solvency II ASB, FSCS, Liquidity)
- ⚠️ **1 partially implemented module** (RRA/RRQ - Python complete, R partial)
- 📋 **11 missing RRA form processors** (only 3 of 14 forms have dedicated processors)

**Priority:** Focus on achieving Python/R parity for RRA/RRQ, then add missing form processors, then enhance testing and documentation infrastructure.

---

## Gap Analysis

### 1. RRA/RRQ Module - R Implementation Gaps

**Status:** Python has full RRQ/RRA support; R has partial support

#### Missing R Scripts:

| Component | Python (✅) | R (❌) | Impact | Priority |
|-----------|------------|--------|--------|----------|
| `rra_291_gross_premium_ibnr.R` | ✅ 300 lines | ❌ Missing | Medium | **P1** |
| `unified_form_processor.R` | ✅ 395 lines | ❌ Missing | High | **P1** |
| `generate_unified_lloyds_data.R` | ✅ 396 lines | ❌ Missing | High | **P1** |

**Impact:**
- R users cannot process RRQ data (quarterly returns)
- R users cannot leverage unified RRQ/RRA auto-detection
- R users cannot generate quarterly synthetic data
- Breaks advertised "dual language parity" for RRA/RRQ module

---

### 2. RRA Form Processors - Missing Scripts

**Status:** Only 3 of 14 RRA forms have dedicated processing scripts

#### Implemented Processors:

| Form | Description | Python | R |
|------|-------------|--------|---|
| **010** | Control Data | ✅ | ✅ |
| **193** | Net Claims Development | ✅ | ✅ |
| **291** | Gross Premium and IBNR | ✅ | ❌ |

#### Missing Processors (Data Exists, No Processor):

| Form | Description | Data Exists | Priority |
|------|-------------|-------------|----------|
| **020** | Exchange Rates | ✅ CSV | **P2** |
| **071** | SCOB Mapping | ✅ CSV | **P2** |
| **081** | Reserving Class Info | ✅ CSV | **P2** |
| **091** | LPT (Loss Portfolio Transfer) | ✅ CSV | **P3** |
| **292** | Net Premium and IBNR | ✅ CSV | **P2** |
| **293** | Outstanding & IBNR (<20 PYoA) | ✅ CSV | **P2** |
| **294** | Gross IBNR (Catastrophe) | ✅ CSV | **P2** |
| **295** | ULAE Reserves | ✅ CSV | **P3** |
| **391** | IELR (Incurred Emerging Loss Ratio) | ✅ CSV | **P2** |
| **910** | Additional Information | ✅ CSV | **P3** |
| **990** | Validation Summary | ✅ CSV | **P1** |

**Impact:**
- Users must manually process 11 of 14 forms
- Limited actuarial analysis capabilities for forms without processors
- No validation or quality checks for unprocessed forms
- Cannot demonstrate comprehensive RRA processing capability

**Note:** While `rra_aggregator.py` and `rra_aggregator.R` can load and aggregate all forms, individual form processors provide:
- Form-specific validation rules
- Actuarial calculations (chain ladder, loss ratios, etc.)
- Data quality checks
- Regulatory compliance validation

---

### 3. Testing Infrastructure

**Status:** No formal testing framework

#### Missing Components:

| Component | Status | Priority |
|-----------|--------|----------|
| Unit tests for Python modules | ❌ | **P1** |
| Unit tests for R modules | ❌ | **P1** |
| Integration tests | ❌ | **P2** |
| Data validation test suite | ❌ | **P2** |
| CI/CD pipeline (GitHub Actions) | ❌ | **P2** |
| Test coverage reporting | ❌ | **P3** |

**Impact:**
- No automated regression testing
- Difficult to refactor with confidence
- Cannot verify correctness systematically
- Not production-ready

---

### 4. Documentation Infrastructure

**Status:** Comprehensive markdown documentation exists, but no documentation site

#### Current State:
- ✅ 7 root-level markdown guides
- ✅ 10+ module-specific READMEs
- ✅ Power BI integration guides
- ❌ No searchable documentation site
- ❌ No API documentation (auto-generated from docstrings)

#### Planned Enhancements:

| Component | Status | Priority |
|-----------|--------|----------|
| MkDocs or Quarto documentation site | ❌ | **P2** |
| Auto-generated API docs from docstrings | ❌ | **P3** |
| Tutorial videos or notebooks | ❌ | **P3** |
| Architecture diagrams | ❌ | **P3** |

---

### 5. Advanced Actuarial Methods

**Status:** Basic chain ladder implemented, advanced methods missing

#### Implemented:
- ✅ Chain ladder (age-to-age factors)
- ✅ Loss ratio calculations
- ✅ IBNR estimates

#### Missing:

| Method | Use Case | Priority |
|--------|----------|----------|
| Bornhuetter-Ferguson | IBNR for immature years | **P2** |
| Cape Cod | Industry benchmarking | **P2** |
| Bootstrap simulations | Reserve uncertainty | **P3** |
| Mack method | Standard error of reserves | **P3** |
| GLM reserving | Granular reserve modeling | **P3** |

---

## Prioritized Action Plan

### Phase 1: Achieve R Parity (Critical for "Dual Language" Claim)

**Timeline:** 2-3 weeks
**Priority:** P1
**Owner:** TBD

#### Tasks:

1. **Create `r_scripts/forms/rra_291_gross_premium_ibnr.R`**
   - Port from Python version (300 lines)
   - Test against synthetic data
   - Verify parity with Python output
   - **Effort:** 2-3 days

2. **Create `r_scripts/forms/unified_form_processor.R`**
   - Port from Python version (395 lines)
   - Implement RRQ/RRA auto-detection
   - Test with both RRA and RRQ data
   - **Effort:** 3-4 days

3. **Create `r_scripts/data_generation/generate_unified_lloyds_data.R`**
   - Port from Python version (396 lines)
   - Support RRQ quarterly generation
   - Test all four quarters + annual
   - **Effort:** 3-4 days

4. **Integration Testing**
   - Verify R and Python produce identical outputs
   - Test all RRQ quarters (Q1-Q4)
   - Test RRA annual generation
   - **Effort:** 2 days

**Success Criteria:**
- R can generate RRQ data for all four quarters
- R can process RRQ and RRA data with auto-detection
- R output matches Python output (within floating point tolerance)
- Updated README reflects full parity

---

### Phase 2: Add Missing RRA Form Processors (Completeness)

**Timeline:** 4-6 weeks
**Priority:** P2
**Owner:** TBD

#### Group 1: High-Value Forms (P1-P2)

**Forms 292, 293, 294 (Premium/IBNR family):**
- Similar structure to Form 291 (already implemented)
- Can reuse chain ladder and IBNR calculation logic
- **Effort:** 3-4 days per form (Python + R)

**Form 391 (IELR):**
- Important for loss ratio monitoring
- Requires time-series analysis
- **Effort:** 4-5 days (Python + R)

**Form 990 (Validation Summary):**
- Critical for data quality
- Cross-form validation rules
- **Effort:** 5-6 days (Python + R)

#### Group 2: Reference Data Forms (P2)

**Forms 020, 071, 081 (Exchange Rates, SCOB Mapping, Class Info):**
- Simpler processors (mostly validation and lookups)
- Low computational complexity
- **Effort:** 2-3 days per form (Python + R)

#### Group 3: Specialized Forms (P3)

**Forms 091, 295, 910 (LPT, ULAE, Additional Info):**
- Less frequently used
- Specialized business logic
- **Effort:** 3-4 days per form (Python + R)

**Task Breakdown:**

| Week | Tasks | Forms |
|------|-------|-------|
| 1-2 | Forms 292, 293, 294 | Premium/IBNR family |
| 3 | Form 391 | IELR |
| 4 | Form 990 | Validation |
| 5 | Forms 020, 071, 081 | Reference data |
| 6 | Forms 091, 295, 910 | Specialized |

**Success Criteria:**
- All 14 RRA forms have dedicated processors
- Both Python and R implementations
- Validation rules implemented
- Documented in DETAILED_DOCUMENTATION.md

---

### Phase 3: Testing Infrastructure (Production Readiness)

**Timeline:** 2-3 weeks
**Priority:** P1-P2
**Owner:** TBD

#### Week 1: Unit Testing Framework

**Python:**
```bash
# Setup pytest structure
tests/
├─ __init__.py
├─ test_rra_forms/
│  ├─ test_rra_010.py
│  ├─ test_rra_193.py
│  └─ test_rra_291.py
├─ test_solvency_ii/
│  ├─ test_claims_processor.py
│  ├─ test_asb_returns.py
│  └─ test_qsr_generator.py
├─ test_fscs/
│  └─ test_data_generator.py
└─ test_liquidity/
   └─ test_stress_test.py
```

**R:**
```bash
# Setup testthat structure
tests/
├─ testthat/
│  ├─ test_rra_010.R
│  ├─ test_rra_193.R
│  ├─ test_rra_291.R
│  ├─ test_solvency_claims.R
│  └─ test_liquidity.R
└─ testthat.R
```

**Effort:** 5-6 days

#### Week 2: Integration Tests & CI/CD

**GitHub Actions Workflow:**
```yaml
name: CI

on: [push, pull_request]

jobs:
  test-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r python_scripts/requirements.txt pytest
      - name: Run tests
        run: pytest tests/

  test-r:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up R
        uses: r-lib/actions/setup-r@v2
      - name: Install dependencies
        run: Rscript r_scripts/install_packages.R
      - name: Run tests
        run: Rscript -e 'testthat::test_dir("tests/testthat")'
```

**Effort:** 3-4 days

#### Week 3: Coverage & Quality

- Set up coverage.py for Python
- Set up covr for R
- Add code quality checks (flake8, lintr)
- Document testing procedures

**Effort:** 2-3 days

**Success Criteria:**
- >80% code coverage for core modules
- CI/CD passes on all commits
- Automated testing on PRs
- Coverage badges in README

---

### Phase 4: Documentation Site (Discoverability)

**Timeline:** 1-2 weeks
**Priority:** P2
**Owner:** TBD

#### Option 1: MkDocs (Recommended)

**Structure:**
```
docs/
├─ index.md                 # Home (current README content)
├─ getting-started/
│  ├─ installation.md
│  ├─ quickstart.md
│  └─ prerequisites.md
├─ modules/
│  ├─ rra-rrq.md
│  ├─ solvency-ii.md
│  ├─ fscs.md
│  └─ liquidity.md
├─ guides/
│  ├─ power-bi-integration.md
│  ├─ synthetic-data.md
│  └─ validation.md
├─ api/
│  ├─ python/
│  └─ r/
└─ contributing.md

mkdocs.yml                  # MkDocs configuration
```

**Deployment:**
- GitHub Pages (free)
- Auto-deploy on push to main
- Custom domain (optional): docs.lloyds-reporting.dev

**Effort:** 5-7 days

#### Option 2: Quarto (Alternative)

- Better for mixing code/docs
- Native R support
- More academic/publication feel

**Effort:** 6-8 days

**Success Criteria:**
- Searchable documentation site
- Auto-deployed on commit
- Mobile-friendly
- API documentation auto-generated from docstrings

---

### Phase 5: Advanced Features (Enhancements)

**Timeline:** Ongoing
**Priority:** P3
**Owner:** TBD

#### Advanced Actuarial Methods

**Bornhuetter-Ferguson (Python + R):**
```python
def bornhuetter_ferguson(paid_triangle, reported_triangle,
                         apriori_loss_ratio, earned_premium):
    """
    Calculate IBNR using Bornhuetter-Ferguson method

    BF IBNR = (Apriori Ultimate - Reported) × % Unreported
    """
    # Implementation
    pass
```

**Effort per method:** 3-4 days (Python + R)

#### Power BI Template Files (.pbit)

- Create reusable Power BI templates
- Pre-configured visuals and DAX measures
- Parameterized connections

**Effort:** 5-7 days per module

#### API Endpoints (Optional - for web integration)

**Flask (Python) or Plumber (R):**
```python
from flask import Flask, jsonify
from python_scripts.solvency_claims_processor import process_claims_data

app = Flask(__name__)

@app.route('/api/v1/solvency-claims', methods=['POST'])
def process_claims():
    # Process uploaded claims file
    return jsonify(results)
```

**Effort:** 2-3 weeks

---

## Implementation Schedule

### Q1 2025 (Jan-Mar)

| Week | Phase | Deliverables |
|------|-------|--------------|
| 1-3 | Phase 1 | R parity for RRQ/RRA |
| 4-6 | Phase 2 (partial) | Forms 292, 293, 294, 391 |
| 7-9 | Phase 2 (partial) | Forms 990, 020, 071, 081 |
| 10-12 | Phase 3 | Testing infrastructure |

### Q2 2025 (Apr-Jun)

| Week | Phase | Deliverables |
|------|-------|--------------|
| 1-2 | Phase 2 (complete) | Forms 091, 295, 910 |
| 3-4 | Phase 4 | Documentation site |
| 5-8 | Phase 5 | Advanced actuarial methods |
| 9-12 | Phase 5 | Power BI templates |

---

## Resource Requirements

### Development Time

| Phase | Python Dev | R Dev | DevOps | Docs | Total |
|-------|------------|-------|--------|------|-------|
| Phase 1 | 5 days | 8 days | - | 1 day | 14 days |
| Phase 2 | 15 days | 15 days | - | 3 days | 33 days |
| Phase 3 | 5 days | 3 days | 4 days | 2 days | 14 days |
| Phase 4 | 2 days | - | 2 days | 7 days | 11 days |
| Phase 5 | 10 days | 10 days | 3 days | 2 days | 25 days |
| **Total** | **37 days** | **36 days** | **9 days** | **15 days** | **97 days** |

### Skills Required

- **Python Developer:** pandas, numpy, actuarial methods
- **R Developer:** tidyverse, R6, actuarial methods
- **DevOps:** GitHub Actions, testing frameworks
- **Technical Writer:** MkDocs, API documentation
- **Optional:** Actuary (for advanced methods validation)

---

## Success Metrics

### Code Quality
- ✅ Python/R parity for all modules (100%)
- ✅ Test coverage >80%
- ✅ CI/CD passing on all branches
- ✅ Zero critical security vulnerabilities (Dependabot)

### Documentation
- ✅ Searchable documentation site live
- ✅ All functions documented with examples
- ✅ Power BI integration guides for all modules
- ✅ <5 minutes from clone to first successful run

### Functionality
- ✅ All 14 RRA forms have processors (Python + R)
- ✅ RRQ and RRA fully supported in both languages
- ✅ All synthetic data generators working
- ✅ All modules Power BI ready

### Community
- ✅ 3+ external contributors (via GitHub)
- ✅ 10+ stars on GitHub
- ✅ Featured in Lloyd's/actuarial newsletters (stretch goal)

---

## Risk Mitigation

### Risk 1: R Development Capacity
**Risk:** Limited R developers available
**Mitigation:**
- Prioritize R parity for most critical modules first
- Consider auto-transpiling Python to R (experimental)
- Document Python implementation thoroughly for R developers

### Risk 2: Lloyd's Specification Changes
**Risk:** Lloyd's updates RRA/RRQ specs mid-implementation
**Mitigation:**
- Monitor Lloyd's regulatory updates monthly
- Build modular, easily updateable code
- Version control spec files in `Files_for_Claude/`

### Risk 3: Scope Creep
**Risk:** Additional features requested during implementation
**Mitigation:**
- Stick to phased approach
- Document feature requests in GitHub Issues
- Prioritize ruthlessly (P1 → P2 → P3)

### Risk 4: Testing Overhead
**Risk:** Testing takes longer than development
**Mitigation:**
- Write tests incrementally with each feature
- Focus on critical path coverage first
- Use property-based testing for complex logic

---

## Next Steps

1. **Review this roadmap** with stakeholders
2. **Assign owners** to each phase
3. **Create GitHub Project** to track progress
4. **Set up GitHub Issues** for each task
5. **Begin Phase 1** (R parity for RRQ/RRA)

---

## Appendix: Quick Wins (Weekend Projects)

For quick progress, these can be tackled independently:

### Quick Win 1: Form 020 (Exchange Rates) - 4 hours
- Simple validation (currency codes, rates > 0)
- Historical rate tracking
- Both Python + R

### Quick Win 2: Form 071 (SCOB Mapping) - 4 hours
- Validate SCOB code consistency
- Mapping table integrity checks
- Both Python + R

### Quick Win 3: CI/CD Basic Setup - 3 hours
- GitHub Actions workflow
- Python pytest on push
- R testthat on push

### Quick Win 4: README Badges - 1 hour
- Add shields.io badges
- License, Python version, R version
- CI/CD status

### Quick Win 5: Contributing Guide - 2 hours
- CONTRIBUTING.md
- Code of conduct
- PR template

---

**Document Version:** 1.0
**Last Updated:** 2025-11-21
**Next Review:** 2025-12-21
**Owner:** Lloyd's Development Team
