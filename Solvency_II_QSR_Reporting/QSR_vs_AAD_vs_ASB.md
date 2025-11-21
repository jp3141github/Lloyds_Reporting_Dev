# Lloyd's Solvency II Reporting: QSR vs AAD vs ASB

## Overview of Lloyd's Solvency II Reporting Framework

Lloyd's of London syndicates must submit different regulatory returns depending on the reporting frequency:

### Reporting Frequencies

| Frequency | Return Types | Purpose |
|-----------|-------------|---------|
| **Quarterly** | QSR (Quarterly Solvency Return) | Monitor ongoing solvency position |
| **Annual** | AAD (Annual Actuarial Data) + ASB (Annual Solvency Balance Sheet) | Comprehensive year-end reporting |

## QSR - Quarterly Solvency Return

**Submitted**: Every quarter (Q1, Q2, Q3, Q4)
**Due**: Within 4-6 weeks after quarter end

### QSR Returns (20 templates):

| Return | Description | EIOPA Ref |
|--------|-------------|-----------|
| QSR 010 | Control Page | - |
| QSR 030 | Basic Information - General | S.01.02.01 |
| QSR 031 | Quantitative Reporting Templates | S.01.01.02 |
| QSR 002 | Overall Balance Sheet | S.02.01.02 |
| QSR 204 | Members Providing Capital (FIS) | - |
| QSR 210 | Solvency II Balance Sheet Reconciliation | - |
| QSR 220 | Own Funds | S.23.01.01 |
| QSR 240 | Non-Life Technical Provisions | S.17.01.02 |
| QSR 280 | Life Technical Provisions | S.12.01.02 |
| QSR 283 | Life Technical Provisions (alternative) | S.12.01.02 |
| QSR 291 | Operational Risk | S.41.01.11 |
| QSR 292 | Market Risk | S.14.01.10.01 |
| QSR 293 | Counterparty Default Risk | S.38.01.10.01 |
| QSR 440 | Non-Life Insurance Claims | S.05.01.02.01 |
| QSR 450 | Life Insurance Information | S.05.01.02.02 |
| QSR 510 | Minimum Capital Requirement - Non-Life | S.28.01.01 |
| QSR 511 | Minimum Capital Requirement - Life | S.28.01.01 |
| QSR 923 | [Description varies] | - |
| QSR 990 | Additional Information | - |

**Focus Areas:**
- Current solvency position
- Balance sheet (assets and liabilities)
- Own funds composition and tiers
- Technical provisions
- SCR and MCR calculations
- High-level premiums and claims data

## AAD - Annual Actuarial Data

**Submitted**: Once per year (year-end)
**Due**: Within 14 weeks after year end

### AAD Returns (8 main templates):

| Return | Description | EIOPA Ref |
|--------|-------------|-----------|
| AAD 010 | Control Page | - |
| AAD 230 | Open Market Value of Investments | S.06.02.01 |
| AAD 233 | Off-Balance Sheet Items | S.08.01.01 |
| AAD 235 | Derivatives | S.09.01.01 |
| AAD 236 | Collective Investments Undertakings | S.06.03.01 |
| AAD 237 | Structured Products | S.10.01.01 |
| AAD 238 | Securities Lending and Repos | S.11.01.01 |
| AAD 990 | Additional Information | - |

**Focus Areas:**
- Detailed investment breakdowns
- Derivative positions and exposures
- Off-balance sheet items
- Collective investment holdings
- Structured product analysis
- Securities lending activities

## ASB - Annual Solvency Balance Sheet

**Submitted**: Once per year (year-end)
**Due**: Within 14 weeks after year end

### ASB Returns (4 main templates):

| Return | Description | EIOPA Ref |
|--------|-------------|-----------|
| ASB 010 | Control Page | - |
| ASB 245 | Non-Life Claims - Gross | S.19.01.01 |
| ASB 246 | Non-Life Claims - Reinsurers Share | S.19.01.01 |
| ASB 247 | Non-Life Claims - Net | S.19.01.01 |
| ASB 248 | Non-Life Claims - Total | S.19.01.01 |
| ASB 910 | [Description] | - |
| ASB 990 | Additional Information | - |

**Focus Areas:**
- Claims development triangles
- Claims by accident year and development year
- Gross, net, and reinsurers' share
- Ultimate claims estimates
- Claims provisions analysis

## Key Differences: Quarterly vs Annual

### 1. **Granularity**

| Aspect | Quarterly (QSR) | Annual (AAD + ASB) |
|--------|----------------|-------------------|
| Detail Level | High-level summary | Detailed breakdowns |
| Line of Business | Aggregated categories | Full granularity |
| Time Series | Current quarter | Full historical development |
| Investments | Summary by class | Individual security level |

### 2. **Data Requirements**

**QSR (Quarterly)**
- Current period balances
- Premium/claims for the quarter
- Point-in-time SCR/MCR
- Technical provisions as of quarter-end

**AAD (Annual)**
- Complete investment portfolio details
- All derivative contracts
- Off-balance sheet commitments
- Detailed fund holdings

**ASB (Annual)**
- Claims triangles (10+ years)
- Development patterns
- Ultimate loss estimates
- IBNR calculations by year

### 3. **Validation Complexity**

| Return Type | Validation Rules | Cross-Checks |
|-------------|------------------|--------------|
| QSR | ~50-100 rules | Internal consistency |
| AAD | ~100-200 rules | Cross-reference to QSR |
| ASB | ~80-150 rules | Triangle consistency |

### 4. **Submission Timing**

```
January: QSR Q4 (previous year)
April: QSR Q1 + AAD + ASB (previous year-end)
July: QSR Q2
October: QSR Q3
```

### 5. **Use Cases**

**QSR**
- Ongoing solvency monitoring
- Regulatory early warning
- Management MI
- Capital planning

**AAD + ASB**
- Comprehensive regulatory review
- SFCR (Solvency & Financial Condition Report) support
- Supervisory risk assessment
- Market discipline (public disclosure)

## Data Flow Comparison

### Quarterly Flow (QSR)
```
Source Systems → Aggregation → QSR Templates → Validation → Submission
```

### Annual Flow (AAD + ASB)
```
Source Systems → Detailed Extraction →
   ├─> Investment System → AAD Templates
   ├─> Claims System → ASB Triangles
   └─> Aggregation → Cross-validation → Submission
```

## Technical Implementation Differences

### QSR Implementation
```python
# High-level aggregations
balance_sheet = aggregate_quarterly_balances()
own_funds = calculate_own_funds()
scr = calculate_scr_quarterly()
```

### AAD Implementation
```python
# Detailed investment data
investments_omv = get_investment_details()  # Security-level
derivatives = get_all_derivatives()  # Contract-level
collective_funds = get_fund_holdings()  # Holding-level
```

### ASB Implementation
```python
# Claims triangles
claims_triangles = build_claims_triangle(
    accident_years=range(2014, 2025),
    development_years=range(0, 11)
)
```

## Overlap Between Returns

Some QSR returns are also submitted annually (with more detail):

| Return | Quarterly | Annual | Key Difference |
|--------|-----------|--------|----------------|
| Balance Sheet | QSR 002 | AAD includes 230 details | Annual has investment details |
| Technical Provisions | QSR 240/280 | Same | Usually identical |
| Own Funds | QSR 220 | Same | Usually identical |
| Premiums/Claims | QSR 440/450 | ASB 245-248 | Annual has development triangles |

## Integration Strategy

To handle both QSR and Annual returns efficiently:

### 1. **Shared Data Model**
- Common balance sheet structure
- Shared syndicate/LOB dimensions
- Consistent date handling

### 2. **Frequency-Specific Modules**
- QSR module: Aggregated data
- AAD module: Investment details
- ASB module: Claims triangles

### 3. **Report Factory Pattern**
```python
class SolvencyReportGenerator:
    def generate_qsr(self, quarter, year)
    def generate_aad(self, year)
    def generate_asb(self, year)
```

### 4. **Validation Framework**
```python
class ReportValidator:
    def validate_qsr(self, report)
    def validate_aad(self, report)
    def validate_asb(self, report)
    def cross_validate(self, qsr, aad, asb)
```

## Recommended Implementation Approach

For this project, I will extend the existing QSR code to handle:

1. **Enhanced Data Generator**
   - Add investment details for AAD
   - Add claims triangles for ASB
   - Support both quarterly and annual periods

2. **Unified Report Generator**
   - Base class for common functionality
   - QSR-specific subclass
   - AAD-specific subclass
   - ASB-specific subclass

3. **Power BI Integration**
   - Separate queries for QSR vs Annual
   - Combined dashboards showing trends
   - Year-over-year comparisons

4. **Documentation**
   - Updated guides for annual returns
   - Examples for both frequencies
   - Validation rule documentation

## Summary Table

| Feature | QSR | AAD | ASB |
|---------|-----|-----|-----|
| Frequency | Quarterly | Annual | Annual |
| Returns | 20 | 8 | 7 |
| Complexity | Medium | High | High |
| Detail Level | Summary | Detailed | Detailed |
| Investment Data | Aggregated | Security-level | N/A |
| Claims Data | Period totals | N/A | Development triangles |
| Typical Size | ~100 MB | ~500 MB | ~200 MB |
| Processing Time | ~1-2 hours | ~4-8 hours | ~2-4 hours |

---

**Next**: I will now extend the Python and R code to support all three return types (QSR, AAD, ASB) with a unified architecture.
