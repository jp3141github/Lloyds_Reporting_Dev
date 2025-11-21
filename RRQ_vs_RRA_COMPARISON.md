# RRQ vs RRA: Comparison and Differences

## Overview

Lloyd's of London requires syndicates to submit reserving data through two complementary returns:

- **RRA** (Reserving Return Annual) - Comprehensive annual submission
- **RRQ** (Reserving Return Quarterly) - Streamlined quarterly submission

This document explains the key differences and how the code handles both.

---

## Key Differences

### 1. Reporting Frequency

| Return | Frequency | Submission Periods |
|--------|-----------|-------------------|
| **RRA** | Annual | Once per year (typically year-end) |
| **RRQ** | Quarterly | Q1, Q2, Q3, Q4 (every quarter) |

### 2. Form Coverage

#### RRA Forms (Annual Only)
All forms are submitted annually, including:

| Form | Description | RRA | RRQ |
|------|-------------|-----|-----|
| **010** | Control Data | ✅ Annual | ✅ Quarterly |
| **020** | Exchange Rates | ✅ Annual | ✅ Quarterly |
| **071** | SCOB Mapping | ✅ Annual | ✅ Quarterly |
| **081** | Reserving Class Info | ✅ Annual | ⚠️ Q4 Only |
| **091** | LPT (Loss Portfolio Transfer) | ✅ Annual | ✅ Quarterly |
| **193** | Net Claims Development | ✅ Annual | ✅ Quarterly (Current + Prior 2 YoA) |
| **291** | Gross Premium & IBNR | ✅ Annual | ✅ Quarterly |
| **292** | Net Premium & IBNR | ✅ Annual | ✅ Quarterly |
| **293** | Outstanding & IBNR (<20 PYoA) | ✅ Annual | ✅ Quarterly |
| **294** | Gross IBNR (Catastrophe) | ✅ Annual | ✅ Quarterly |
| **295** | ULAE Reserves | ✅ Annual | ✅ Quarterly |
| **391** | IELR (Incurred Emerging Loss Ratio) | ✅ Annual | ⚠️ Q4 Only |
| **910** | Additional Information | ✅ Annual | ⚠️ Q4 Only |
| **990** | Validation Summary | ✅ Annual | ✅ Quarterly |

**Legend:**
- ✅ Required
- ⚠️ Required only in Q4 (year-end quarterly submission)
- ❌ Not required

### 3. Data Scope Differences

#### RRA (Annual)
- **Historical Depth:** All years of account from inception
- **Development Triangles:** Complete development history (e.g., 10+ years)
- **Detail Level:** Full granularity across all dimensions
- **Analysis:** Comprehensive ultimate analysis

#### RRQ (Quarterly)
- **Historical Depth:** Current year + prior 2-3 years of account
- **Development Triangles:** Limited to recent development (current + 2 prior YoA)
- **Detail Level:** Focused on material changes and current position
- **Analysis:** Incremental changes since last quarter

### 4. Timing and Deadlines

| Return | Submission Deadline | Covers Period |
|--------|-------------------|---------------|
| **RRQ Q1** | ~45 days after Q1 end | January 1 - March 31 |
| **RRQ Q2** | ~45 days after Q2 end | April 1 - June 30 |
| **RRQ Q3** | ~45 days after Q3 end | July 1 - September 30 |
| **RRQ Q4** | ~60 days after Q4 end | October 1 - December 31 |
| **RRA** | ~90 days after year end | Full year (January 1 - December 31) |

**Note:** Q4 RRQ often aligns with RRA and may have additional forms.

---

## Data Structure Differences

### Example: Form 193 (Net Claims)

**RRA Scope:**
```
Syndicate 2987
├── YoA 2015 (Development years 0-8)
├── YoA 2016 (Development years 0-7)
├── YoA 2017 (Development years 0-6)
├── YoA 2018 (Development years 0-5)
├── YoA 2019 (Development years 0-4)
├── YoA 2020 (Development years 0-3)
├── YoA 2021 (Development years 0-2)
├── YoA 2022 (Development years 0-1)
└── YoA 2023 (Development year 0)
```

**RRQ Scope (Q2 2024):**
```
Syndicate 2987
├── YoA 2022 (Development years 0-1)
├── YoA 2023 (Development years 0-1)
└── YoA 2024 (Development year 0) ← Current year
```

---

## Code Implementation Strategy

### Unified Architecture

The code uses a **unified architecture** with configuration-based switching:

```python
# Configuration determines RRQ vs RRA behavior
config = {
    'return_type': 'RRQ',  # or 'RRA'
    'reporting_quarter': 'Q2',  # for RRQ only
    'reporting_year': 2024,
    'yoa_scope': 'limited',  # 'limited' for RRQ, 'full' for RRA
}
```

### Form Filtering

```python
# Forms required by return type and quarter
RRQ_FORMS_ALL_QUARTERS = ['010', '020', '071', '091', '193', '291', '292', '293', '294', '295', '990']
RRQ_FORMS_Q4_ONLY = ['081', '391', '910']
RRA_FORMS_ALL = ['010', '020', '071', '081', '091', '193', '291', '292', '293', '294', '295', '391', '910', '990']
```

### Data Scoping

```python
def get_yoa_scope(return_type, reporting_year, quarter=None):
    """Determine which years of account to include"""
    if return_type == 'RRA':
        # RRA: All years from first to current
        return range(first_yoa, reporting_year + 1)
    elif return_type == 'RRQ':
        # RRQ: Current + prior 2 years
        return range(reporting_year - 2, reporting_year + 1)
```

---

## Quarterly Calendar and Progression

### Q1 2024 (Jan-Mar)
- **As At Date:** March 31, 2024
- **YoA in Scope:** 2022, 2023, 2024
- **Focus:** Q1 emergence, early 2024 YoA estimates

### Q2 2024 (Apr-Jun)
- **As At Date:** June 30, 2024
- **YoA in Scope:** 2022, 2023, 2024
- **Focus:** Mid-year position, 2024 YoA development

### Q3 2024 (Jul-Sep)
- **As At Date:** September 30, 2024
- **YoA in Scope:** 2022, 2023, 2024
- **Focus:** Pre-year-end position

### Q4 2024 (Oct-Dec) + RRA 2024
- **As At Date:** December 31, 2024
- **YoA in Scope (RRQ):** 2022, 2023, 2024
- **YoA in Scope (RRA):** 2015-2024 (all years)
- **Focus:** Year-end position, comprehensive analysis
- **Note:** Q4 RRQ + RRA often submitted together

---

## Use Cases

### When to Use RRA
- ✅ Annual business planning and budgeting
- ✅ Comprehensive reserve adequacy testing
- ✅ Historical trend analysis (10+ years)
- ✅ Regulatory annual submissions
- ✅ Audit and external reporting
- ✅ Long-term development pattern analysis

### When to Use RRQ
- ✅ Quarterly management reporting
- ✅ Recent reserve movement monitoring
- ✅ Current year tracking
- ✅ Interim regulatory submissions
- ✅ Board quarterly updates
- ✅ Quick turnaround analysis

---

## Data Volume Comparison

### Typical Record Counts (Single Syndicate)

| Form | RRA Records | RRQ Records | Reduction |
|------|-------------|-------------|-----------|
| **193** | ~1,400 | ~150 | 89% |
| **291** | ~350 | ~50 | 86% |
| **292** | ~350 | ~50 | 86% |
| **391** | ~1,350 | N/A (Q4 only) | N/A |
| **Total** | ~4,000+ | ~400-500 | 87% |

**RRQ is typically 85-90% smaller than RRA due to limited historical scope.**

---

## Validation Differences

### RRA Validations
- ✅ Complete development pattern consistency
- ✅ Cross-year reconciliation
- ✅ Ultimate loss ratio trends
- ✅ Long-tail reserve adequacy
- ✅ Historical restatement checks

### RRQ Validations
- ✅ Quarter-over-quarter movement checks
- ✅ Current year plausibility
- ✅ Material change explanations
- ✅ Consistency with prior quarter
- ✅ Year-to-date accumulation

---

## Integration Approach

### Option 1: Separate Processes
```
RRA Process ─────► RRA Database ─────► Annual Reports
RRQ Process ─────► RRQ Database ─────► Quarterly Reports
```

**Pros:** Clear separation, independent validation
**Cons:** Duplicate code, potential inconsistencies

### Option 2: Unified Process (Recommended)
```
Unified Process ─────► Combined Database ─────┬─► RRA Views
                                               └─► RRQ Views
```

**Pros:** Single codebase, consistent methodology, easier maintenance
**Cons:** More complex configuration

---

## Code Examples

### Generate RRA Data
```python
from generate_unified_lloyds_data import UnifiedLloydsDataGenerator

generator = UnifiedLloydsDataGenerator(
    return_type='RRA',
    reporting_year=2024,
    output_dir='synthetic_data/rra_2024'
)
generator.generate_all_data()
```

### Generate RRQ Data
```python
generator = UnifiedLloydsDataGenerator(
    return_type='RRQ',
    reporting_year=2024,
    reporting_quarter='Q2',
    output_dir='synthetic_data/rrq_2024_q2'
)
generator.generate_all_data()
```

### Process Either Type
```python
from unified_form_processor import process_form_193

# Automatically detects RRQ vs RRA from data
df = process_form_193('synthetic_data/rrq_2024_q2/rra_193_net_claims.csv')
```

---

## Migration Path

### Phase 1: Current State
- RRA implementation complete ✅
- RRQ not yet implemented

### Phase 2: Extend to RRQ (This Update)
- Add RRQ configuration support
- Implement quarterly scoping
- Create quarter-specific generators
- Update form processors

### Phase 3: Unified Reporting
- Combined dashboards
- Quarter-over-quarter analysis
- Quarterly vs Annual comparison views
- Integrated validation

---

## Power BI Implications

### Separate Dashboards
- **RRA Dashboard:** Annual comprehensive view
- **RRQ Dashboard:** Quarterly monitoring view

### Combined Dashboard
- **Filter by Return Type:** RRQ vs RRA
- **Filter by Quarter:** Q1, Q2, Q3, Q4
- **Year-over-Year:** Compare Q2 2024 vs Q2 2023
- **Quarter Progression:** Track Q1→Q2→Q3→Q4

---

## Best Practices

### 1. Consistent Methodology
✅ Use the same actuarial methods for both RRA and RRQ
✅ Apply consistent assumptions
✅ Reconcile differences when they arise

### 2. Incremental Updates
✅ RRQ should be incremental updates to prior quarter
✅ Material changes should be explained
✅ Q4 RRQ should reconcile to RRA

### 3. Data Lineage
✅ Track which quarter data comes from
✅ Maintain version history
✅ Document restated quarters

### 4. Efficiency
✅ Automate RRQ generation where possible
✅ Reuse RRA code with configuration
✅ Minimize manual adjustments

---

## Summary Table

| Aspect | RRA | RRQ |
|--------|-----|-----|
| **Frequency** | Annual | Quarterly |
| **Forms** | All 14 forms | 11 forms (Q1-Q3), 14 forms (Q4) |
| **YoA Scope** | All historical | Current + 2 prior |
| **Development** | Complete triangles | Limited triangles |
| **Detail** | Comprehensive | Focused on changes |
| **Deadline** | ~90 days post year-end | ~45 days post quarter-end |
| **Data Volume** | 100% | ~15% of RRA |
| **Use Case** | Annual planning, audit | Quarterly monitoring |
| **Validation** | Extensive historical | Movement-based |

---

## Next Steps

1. ✅ Understand differences between RRQ and RRA
2. ⏳ Extend code to support both return types
3. ⏳ Generate RRQ synthetic data for all quarters
4. ⏳ Create quarterly comparison reports
5. ⏳ Update Power BI dashboards for RRQ/RRA combined view

---

**Document Version:** 1.0
**Last Updated:** 2024-11-21
**Status:** Initial documentation for RRQ implementation
