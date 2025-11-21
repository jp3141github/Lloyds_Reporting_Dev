# Synthetic Lloyd's Data

This folder contains synthetically generated Lloyd's of London syndicate data for testing and demonstration purposes.

## ⚠️ Important Notice

**This data is completely synthetic and for demonstration purposes only.**

- Do NOT use for actual regulatory reporting
- Replace with real syndicate data for production use
- Data follows realistic patterns but is randomly generated

## Files Structure

```
data/
├── generate_synthetic_data.py          # Data generator script
├── syndicate_XXXX/                     # Individual syndicate folders
│   ├── metadata.json                   # Syndicate metadata
│   ├── assets_liquidity.csv            # Asset breakdown by quarter
│   ├── cashflow.csv                    # Cashflow analysis
│   └── stress_scenario.csv             # Stress test data
├── all_syndicates_metadata.csv         # Combined metadata
├── all_syndicates_assets.csv           # Combined assets data
├── all_syndicates_cashflow.csv         # Combined cashflow data
└── all_syndicates_stress.csv           # Combined stress data
```

## Generated Syndicates

| Number | Name | Managing Agent |
|--------|------|----------------|
| 2001 | Alpha Syndicate | Alpha Managing Agents Ltd |
| 2002 | Beta Syndicate | Beta Insurance Management |
| 2003 | Gamma Syndicate | Gamma Underwriting Ltd |
| 2004 | Delta Syndicate | Delta Risk Services |
| 2005 | Epsilon Syndicate | Epsilon Capital Management |

## Data Specifications

### Metadata (metadata.json / all_syndicates_metadata.csv)

**Syndicate Information:**
- `syndicate_number` (int): Unique syndicate identifier
- `syndicate_name` (str): Syndicate name
- `managing_agent` (str): Managing agent name
- `qma_date` (str): QMA reference date (2024-12-31)
- `date_completed` (str): Date of completion

**Capital Position:**
- `syndicate_fal` (int): Funds at Lloyd's (£100M - £500M)
- `syndicate_fis` (int): Funds in Syndicate (80-95% of FAL)
- `syndicate_uscr` (int): Underwriting SCR (60-85% of FAL)
- `syndicate_ueca` (int): Underwriting ECA (10-20% of FAL)

**Stress Scenario:**
- `scenario_type` (str): Type of stress scenario (e.g., "US Windstorm")
- `loss_occurrence_date` (str): Date of loss event (2025-02-15)
- `gross_loss_estimate` (int): 1-in-200 gross loss (1.5x - 2.5x FAL)
- `reinsurance_recovery_estimate` (int): Expected recoveries (40-70% of gross)
- `net_loss_estimate` (int): Net loss after recoveries
- `us_funding_requirement` (int): US trust fund requirement
- `total_disputed_recoveries` (int): Total disputed amount
- `disputed_60_days` (int): Amount disputed for 60 days
- `disputed_90_days` (int): Amount disputed for 90 days

### Assets Data (assets_liquidity.csv)

**Columns:**
- `syndicate_number` (int): Syndicate identifier
- `date` (str): Quarter end date (YYYY-MM-DD)

**Restricted Assets:**
- `us_trust_funds` (int): US regulatory trust funds (20-30% of FAL)
- `other_trust_funds` (int): Other regulatory trust funds (5-10% of FAL)
- `other_restricted_assets` (int): Other restricted assets (2-5% of FAL)
- `restricted_assets_total` (int): Sum of above

**Illiquid Assets:**
- `reinsurance_recoverables` (int): Reinsurance recoverables (15-25% of FAL)
- `reinsurer_urp_unearned` (int): Reinsurer's share of URP (8-12% of FAL)
- `other_illiquid_assets` (int): Other illiquid assets (2-5% of FAL)
- `illiquid_assets_total` (int): Sum of above

**Liquid Assets:**
- `closing_free_funds` (int): Closing free funds (15-25% of FAL)
- `other_liquid_assets` (int): Other liquid assets (5-15% of FAL)
- `liquid_assets_total` (int): Sum of above

**Time Periods:**
- 2024-12-31 (baseline)
- 2025-03-31 (Q1 projection)
- 2025-06-30 (Q2 projection)
- 2025-09-30 (Q3 projection)
- 2025-12-31 (Q4 projection)

### Cashflow Data (cashflow.csv)

**Columns:**
- `syndicate_number` (int): Syndicate identifier
- `date` (str): Quarter end date
- `opening_free_funds` (int): Opening free funds balance

**Operating Cashflows:**
- `premium_income` (int): Premium receipts (15-30% of FAL per quarter)
- `reinsurance_recoveries` (int): Reinsurance recoveries (5-15% of FAL)
- `reinsurance_deposits` (int): Deposit movements (-5% to +5% of FAL)
- `trust_fund_flows` (int): Trust fund inflows/outflows (-2% to +2%)
- `claims_paid` (int): Claims payments (negative, -10% to -25% of FAL)
- `acquisition_costs` (int): Acquisition costs (negative, -3% to -8%)
- `reinsurance_premium` (int): Reinsurance premiums (negative, -5% to -12%)
- `operating_expenses` (int): Operating expenses (negative, -2% to -5%)
- `total_operating_cashflow` (int): Sum of operating items

**Non-Operating Cashflows:**
- `investment_income` (int): Investment returns (2-5% of FAL)
- `deposits_to_from_fal` (int): FAL movements (-5% to +5%)
- `member_transactions` (int): Member distributions/contributions (-3% to +3%)
- `total_non_operating_cashflow` (int): Sum of non-operating items

**Summary:**
- `total_movements` (int): Total cashflow movements
- `closing_free_funds` (int): Closing free funds balance

**Cumulative Metrics (added by analysis):**
- `cumulative_premium_income` (int)
- `cumulative_claims_paid` (int)
- `cumulative_total_movements` (int)

### Stress Data (stress_scenario.csv)

**Columns:**
- `syndicate_number` (int): Syndicate identifier
- `date` (str): Quarter end date
- `stress_scenario_impact` (int): Impact on cashflow for that quarter
- `cumulative_stress_impact` (int): Cumulative impact to date

**Stress Timeline:**
- Q1 2025 (2024-12-31): Initial payments (20% of net loss)
- Q2 2025 (2025-03-31): Major funding + payments (30% of net loss + US funding)
- Q3 2025 (2025-06-30): Continued payments (25% of net loss)
- Q4 2025 (2025-09-30): Further payments (15% of net loss)
- Q1 2026 (2025-12-31): Final payments (10% of net loss)

## Data Generation Logic

### Capital Position
```
FAL: Random £100M - £500M
FIS: 80-95% of FAL
uSCR: 60-85% of FAL
uECA: 10-20% of FAL
```

### Stress Scenario
```
Gross Loss: 1.5x - 2.5x FAL
Reinsurance Recovery: 40-70% of Gross Loss
Net Loss: Gross Loss - Recovery
US Funding: 30% of Recovery (simplified)
Disputed: 15-30% of Recovery
```

### Quarterly Variation
- Asset values vary ±5% around baseline
- Cashflows vary based on ranges specified above
- Stress impacts distributed over 5 quarters

## Regenerating Data

To regenerate with different random values:

```bash
python3 generate_synthetic_data.py
```

To modify syndicates or parameters:

1. Edit `generate_synthetic_data.py`
2. Modify the `SYNDICATES` list to add/remove syndicates
3. Adjust percentage ranges in generation functions
4. Run the script to regenerate

### Example: Add New Syndicate

```python
SYNDICATES = [
    # ... existing syndicates ...
    {"number": 2006, "name": "Zeta Syndicate", "agent": "Zeta Management Ltd"},
]
```

### Example: Change FAL Range

```python
def generate_capital_position(syndicate_number):
    # Change from 100-500M to 200-1000M
    fal = np.random.randint(200_000_000, 1_000_000_000)
    # ... rest of function
```

## Using the Data

### Python
```python
import pandas as pd

# Load metadata
metadata = pd.read_csv('data/all_syndicates_metadata.csv')

# Load assets
assets = pd.read_csv('data/all_syndicates_assets.csv')

# Load specific syndicate
synd_2001_metadata = pd.read_json('data/syndicate_2001/metadata.json')
```

### R
```r
library(readr)
library(jsonlite)

# Load metadata
metadata <- read_csv("data/all_syndicates_metadata.csv")

# Load assets
assets <- read_csv("data/all_syndicates_assets.csv")

# Load specific syndicate
synd_2001_metadata <- fromJSON("data/syndicate_2001/metadata.json")
```

### Power BI
1. Get Data → Text/CSV
2. Navigate to `data/` folder
3. Select `all_syndicates_*.csv` files
4. Load into Power BI model

## Data Quality Checks

The synthetic data includes:
- ✓ Realistic value ranges based on Lloyd's market
- ✓ Consistent relationships (e.g., FIS < FAL)
- ✓ Proper quarterly progression
- ✓ Mathematically correct calculations
- ✓ Stress scenarios that test liquidity

The synthetic data does NOT include:
- ✗ Real syndicate information
- ✗ Actual market correlations
- ✗ Historical loss patterns
- ✗ Specific underwriting classes
- ✗ Real reinsurance programs

## Replacing with Real Data

To use real syndicate data:

1. **Match the CSV format** exactly (same column names and types)
2. **Preserve the folder structure** (syndicate_XXXX folders)
3. **Ensure data integrity** (no missing values, correct types)
4. **Validate calculations** (totals, ratios, etc.)
5. **Test with one syndicate** before full deployment

### CSV Format Requirements

**Metadata CSV:**
```csv
syndicate_number,syndicate_name,managing_agent,qma_date,syndicate_fal,...
2001,"Alpha Syndicate","Alpha Managing Agents Ltd",2024-12-31,299900595,...
```

**Assets CSV:**
```csv
syndicate_number,date,us_trust_funds,other_trust_funds,...
2001,2024-12-31,75000000,25000000,...
```

**Cashflow CSV:**
```csv
syndicate_number,date,opening_free_funds,premium_income,...
2001,2024-12-31,50000000,75000000,...
```

**Stress CSV:**
```csv
syndicate_number,date,stress_scenario_impact,cumulative_stress_impact
2001,2024-12-31,-50000000,-50000000
```

## Security Note

⚠️ **Do not commit real syndicate data to version control**

If using real data:
- Add `data/*_real.csv` to `.gitignore`
- Use separate folder for sensitive data
- Encrypt files if storing in cloud
- Follow Lloyd's data protection policies

## Support

For questions about:
- Data structure: See this README
- Data generation: See `generate_synthetic_data.py` source code
- Analysis: See `python_implementation/README.md` or `r_implementation/README.md`
- Power BI: See respective `POWERBI_INTEGRATION.md` files
