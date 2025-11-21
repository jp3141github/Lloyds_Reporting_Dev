# RRQ and RRA Usage Guide

## Quick Start Guide for Both Return Types

This guide shows you how to use the unified scripts to generate and process both RRQ (quarterly) and RRA (annual) Lloyd's returns.

---

## 📊 Generation Examples

### Generate RRA (Annual) Data

```bash
cd python_scripts/data_generation

# Generate RRA for 2024
python generate_unified_lloyds_data.py --type RRA --year 2024

# Output: synthetic_data_rra_2024/
# - All 14 forms
# - Years of Account: 2018-2024 (7 years)
# - As At Date: 2024-12-31
```

### Generate RRQ (Quarterly) Data

```bash
# Generate Q2 2024 RRQ
python generate_unified_lloyds_data.py --type RRQ --year 2024 --quarter Q2

# Output: synthetic_data_rrq_2024_q2/
# - 11 forms (Q1-Q3) or 14 forms (Q4)
# - Years of Account: 2022-2024 (3 years only)
# - As At Date: 2024-06-30
```

### Generate All Four Quarters

```bash
# Generate Q1, Q2, Q3, Q4 all at once
python generate_unified_lloyds_data.py --all-quarters --year 2024

# Output: Creates 4 separate directories:
# - synthetic_data_rrq_2024_q1/
# - synthetic_data_rrq_2024_q2/
# - synthetic_data_rrq_2024_q3/
# - synthetic_data_rrq_2024_q4/
```

---

## 📁 Output Directory Structure

```
Lloyds_Reporting_Dev/
├── synthetic_data_rra_2024/           # RRA 2024
│   ├── rra_010_control.csv
│   ├── rra_193_net_claims.csv        (1,400 records - all years)
│   ├── rra_291_gross_premium_ibnr.csv
│   └── ... (all 14 forms)
│
├── synthetic_data_rrq_2024_q1/        # RRQ Q1 2024
│   ├── rrq_010_control.csv
│   ├── rrq_193_net_claims.csv        (300 records - 3 years only)
│   ├── rrq_291_gross_premium_ibnr.csv
│   └── ... (11 forms, 081/391/910 not included)
│
├── synthetic_data_rrq_2024_q2/        # RRQ Q2 2024
│   └── ... (same as Q1)
│
├── synthetic_data_rrq_2024_q3/        # RRQ Q3 2024
│   └── ... (same as Q1)
│
└── synthetic_data_rrq_2024_q4/        # RRQ Q4 2024
    └── ... (all 14 forms, includes 081/391/910)
```

---

## 🔄 Processing Data - Unified Approach

### Automatic Detection

The unified processor automatically detects whether data is RRQ or RRA:

```python
from unified_form_processor import process_unified_rrq_rra

# Works with both RRQ and RRA data!
df_rra = process_unified_rrq_rra('synthetic_data_rra_2024/rra_193_net_claims.csv', '193')
df_rrq = process_unified_rrq_rra('synthetic_data_rrq_2024_q2/rrq_193_net_claims.csv', '193')

# Check which type
print(df_rra['Data_Scope'].iloc[0])  # Output: 'RRA'
print(df_rrq['Data_Scope'].iloc[0])  # Output: 'RRQ'
print(df_rrq['Quarterly_Period'].iloc[0])  # Output: 'Q2 2024'
```

### Quarter-over-Quarter Comparison (RRQ only)

```python
from unified_form_processor import UnifiedFormProcessor

processor = UnifiedFormProcessor('.')

# Compare Q2 vs Q1
comparison = processor.compare_quarters(
    current_data='synthetic_data_rrq_2024_q2/rrq_193_net_claims.csv',
    prior_data='synthetic_data_rrq_2024_q1/rrq_193_net_claims.csv',
    form='193'
)

# Find significant movements
significant = comparison[comparison['Significant_Movement'] == True]
print(f"Found {len(significant)} significant movements (>10% change)")
```

---

## 📈 Power BI Usage

### Load RRA Data

```python
# Power BI Python Script Source

import sys
sys.path.append(r'C:\path\to\python_scripts\forms')
from unified_form_processor import process_unified_rrq_rra

# Process RRA data
df = process_unified_rrq_rra(
    r'C:\path\to\synthetic_data_rra_2024\rra_193_net_claims.csv',
    '193'
)

# df is available for Power BI visualizations
```

### Load RRQ Data

```python
# Power BI Python Script Source

import sys
sys.path.append(r'C:\path\to\python_scripts\forms')
from unified_form_processor import process_unified_rrq_rra

# Process RRQ data
df = process_unified_rrq_rra(
    r'C:\path\to\synthetic_data_rrq_2024_q2\rrq_193_net_claims.csv',
    '193'
)

# df automatically includes quarterly context
```

### Combined RRQ + RRA Dashboard

```python
# Power BI Python Script Source

import pandas as pd
import sys
sys.path.append(r'C:\path\to\python_scripts\forms')
from unified_form_processor import process_unified_rrq_rra

# Load multiple quarters and annual
files = [
    ('Q1 2024', r'C:\...\synthetic_data_rrq_2024_q1\rrq_193_net_claims.csv'),
    ('Q2 2024', r'C:\...\synthetic_data_rrq_2024_q2\rrq_193_net_claims.csv'),
    ('Q3 2024', r'C:\...\synthetic_data_rrq_2024_q3\rrq_193_net_claims.csv'),
    ('Q4 2024', r'C:\...\synthetic_data_rrq_2024_q4\rrq_193_net_claims.csv'),
    ('Annual 2024', r'C:\...\synthetic_data_rra_2024\rra_193_net_claims.csv'),
]

dfs = []
for label, path in files:
    temp_df = process_unified_rrq_rra(path, '193')
    dfs.append(temp_df)

# Combine all
df = pd.concat(dfs, ignore_index=True)

# Now you can compare quarterly progression vs annual
```

---

## 📊 Power BI Dashboard Examples

### Example 1: Quarterly Progression View

**Visual 1: Card - Total IBNR by Quarter**
- Slicer: Quarter (Q1, Q2, Q3, Q4, Annual)
- Measure: Sum of IBNR_Reserve

**Visual 2: Line Chart - IBNR Trend**
- X-axis: Quarterly_Period
- Y-axis: Sum of IBNR_Reserve
- Legend: LOB_Code

**Visual 3: Table - Quarter over Quarter Movement**
```python
# Use the comparison dataframe
comparison = processor.compare_quarters(current, prior, '193')
# Show: YoA, LOB, IBNR_Movement, Paid_Movement
```

### Example 2: RRQ vs RRA Reconciliation

**Visual 1: Stacked Bar - YoA Coverage**
- X-axis: Year_of_Account
- Y-axis: Count of records
- Legend: Data_Scope (RRQ / RRA)
- Shows which years are in RRQ (2022-2024) vs RRA (2018-2024)

**Visual 2: Development Triangle - RRQ Subset**
- Matrix with Development_Year as columns
- Year_of_Account as rows
- Values: Total_Incurred
- Filter: Data_Scope = 'RRQ'

**Visual 3: Development Triangle - RRA Full**
- Same structure
- Filter: Data_Scope = 'RRA'
- Shows complete development history

---

## 🔍 Data Comparison: RRQ vs RRA

### Record Count Comparison

```python
import pandas as pd

# Load both
df_rra = pd.read_csv('synthetic_data_rra_2024/rra_193_net_claims.csv')
df_rrq = pd.read_csv('synthetic_data_rrq_2024_q2/rrq_193_net_claims.csv')

print("Form 193 Comparison:")
print(f"RRA: {len(df_rra)} records")
print(f"RRQ: {len(df_rrq)} records")
print(f"Reduction: {(1 - len(df_rrq)/len(df_rra))*100:.1f}%")

# Typical output:
# RRA: 1,400 records
# RRQ: 300 records
# Reduction: 78.6%
```

### Years of Account Scope

```python
print("RRA Years:", sorted(df_rra['Year_of_Account'].unique()))
print("RRQ Years:", sorted(df_rrq['Year_of_Account'].unique()))

# Typical output:
# RRA Years: [2018, 2019, 2020, 2021, 2022, 2023, 2024]  # 7 years
# RRQ Years: [2022, 2023, 2024]                          # 3 years only
```

### Development Depth

```python
print("RRA Max Dev Year:", df_rra['Development_Year'].max())
print("RRQ Max Dev Year:", df_rrq['Development_Year'].max())

# Typical output:
# RRA Max Dev Year: 6  # Full development history
# RRQ Max Dev Year: 2  # Limited to recent development
```

---

## 🎯 Common Use Cases

### Use Case 1: Quarterly Board Pack

**Goal:** Show Q2 2024 position to the board

**Steps:**
1. Generate Q2 RRQ data
2. Load into Power BI
3. Create dashboard showing:
   - Current quarter IBNR (2022-2024 YoA)
   - Movement vs Q1
   - New business (2024 YoA)

```bash
python generate_unified_lloyds_data.py --type RRQ --year 2024 --quarter Q2
```

### Use Case 2: Year-End Comprehensive Analysis

**Goal:** Full reserve review at year-end

**Steps:**
1. Generate RRA data (all historical years)
2. Load into Power BI
3. Create dashboard showing:
   - Complete development triangles (2018-2024)
   - Long-term loss ratio trends
   - Reserve adequacy across all years

```bash
python generate_unified_lloyds_data.py --type RRA --year 2024
```

### Use Case 3: Quarterly Trend Analysis

**Goal:** Track how reserves are developing throughout the year

**Steps:**
1. Generate all four quarters
2. Load all into Power BI
3. Create trending dashboard:
   - Q1 → Q2 → Q3 → Q4 progression
   - Highlight significant movements
   - Compare to annual (RRA)

```bash
python generate_unified_lloyds_data.py --all-quarters --year 2024
```

### Use Case 4: Reconcile Q4 RRQ to RRA

**Goal:** Ensure Q4 quarterly aligns with annual

**Steps:**
1. Generate both Q4 RRQ and RRA
2. Load both
3. Reconcile differences (scope, forms)

```bash
python generate_unified_lloyds_data.py --type RRQ --year 2024 --quarter Q4
python generate_unified_lloyds_data.py --type RRA --year 2024
```

**Note:** Q4 RRQ (3 years) vs RRA (7 years) - focus on recent years alignment

---

## 🔄 Migration from Legacy RRA-Only Code

### Option 1: Keep Separate (Recommended for existing dashboards)

```
# Old RRA code
python_scripts/data_generation/generate_synthetic_lloyds_data.py  # RRA only

# New unified code
python_scripts/data_generation/generate_unified_lloyds_data.py   # RRQ + RRA
```

### Option 2: Switch to Unified (Recommended for new projects)

**Before (RRA only):**
```python
from rra_193_net_claims import process_rra_193
df = process_rra_193('rra_193_net_claims.csv')
```

**After (RRQ + RRA):**
```python
from unified_form_processor import process_unified_rrq_rra
df = process_unified_rrq_rra('rrq_193_net_claims.csv', '193')  # Auto-detects
df = process_unified_rrq_rra('rra_193_net_claims.csv', '193')  # Also works!
```

---

## 📋 Checklist for New Quarter

When a new quarter arrives:

- [ ] Generate new quarter RRQ data
  ```bash
  python generate_unified_lloyds_data.py --type RRQ --year 2024 --quarter Q3
  ```

- [ ] Update Power BI data sources to point to new quarter

- [ ] Run quarter-over-quarter comparison
  ```python
  comparison = processor.compare_quarters(q3_data, q2_data, '193')
  ```

- [ ] Review significant movements (>10% change)

- [ ] Update board pack with Q3 position

- [ ] (Q4 only) Generate RRA and reconcile
  ```bash
  python generate_unified_lloyds_data.py --type RRA --year 2024
  ```

---

## 💡 Best Practices

### 1. Naming Conventions

✅ **Good:**
- `synthetic_data_rrq_2024_q2/` - Clear, includes type and period
- `rrq_193_net_claims.csv` - Prefixed with return type
- `rra_291_gross_premium_ibnr.csv` - Consistent naming

❌ **Bad:**
- `data/` - Unclear
- `claims.csv` - No context
- `2024_q2.csv` - Missing form/type info

### 2. Version Control

✅ Keep generated data separate from code:
```
/code/
  python_scripts/
  r_scripts/
/data/
  synthetic_data_rrq_2024_q1/
  synthetic_data_rrq_2024_q2/
  synthetic_data_rra_2024/
```

### 3. Documentation

✅ Document which quarter/year is in production:
```markdown
# Current Production Data
- RRQ Q2 2024: Live in dashboard
- RRQ Q3 2024: Under review
- RRA 2024: Scheduled for January 2025
```

### 4. Testing

✅ Test with sample data before production:
```bash
# Generate small test dataset
python generate_unified_lloyds_data.py --type RRQ --year 2024 --quarter Q1

# Verify record counts
python -c "import pandas as pd; print(len(pd.read_csv('synthetic_data_rrq_2024_q1/rrq_193_net_claims.csv')))"
```

---

## 🚨 Troubleshooting

### Issue: "Quarter parameter required for RRQ"

**Solution:**
```bash
# Wrong:
python generate_unified_lloyds_data.py --type RRQ --year 2024

# Right:
python generate_unified_lloyds_data.py --type RRQ --year 2024 --quarter Q2
```

### Issue: "Unexpected number of records in RRQ"

**Check:**
```python
df = pd.read_csv('rrq_193_net_claims.csv')
print(f"Years: {sorted(df['Year_of_Account'].unique())}")
print(f"Expected: [2022, 2023, 2024]")  # For 2024 RRQ
```

### Issue: "Q4 RRQ missing forms 081, 391, 910"

**Verify:**
```python
import os
files = os.listdir('synthetic_data_rrq_2024_q4/')
print(files)
# Should include: rrq_081_, rrq_391_, rrq_910_
```

### Issue: "Quarter comparison showing all movements as significant"

**Check:**
- Ensure both files are from consecutive quarters
- Verify data has not been regenerated (random seed changed)
- Check movement threshold (default 10%)

---

## 📚 Additional Resources

- **[RRQ_vs_RRA_COMPARISON.md](RRQ_vs_RRA_COMPARISON.md)** - Detailed comparison
- **[README.md](README.md)** - Main project documentation
- **[POWER_BI_INTEGRATION_GUIDE.md](POWER_BI_INTEGRATION_GUIDE.md)** - Power BI guide

---

## 🎓 Learning Path

1. ✅ Start with RRA (simpler, no quarter complexity)
2. ✅ Generate single quarter RRQ (e.g., Q2)
3. ✅ Compare RRA vs RRQ data volumes
4. ✅ Generate all four quarters
5. ✅ Build quarter-over-quarter comparison
6. ✅ Create combined RRQ/RRA dashboard

---

**Version:** 1.0
**Last Updated:** 2024-11-21
**Status:** Production Ready
