# Raw Transactional Data for Lloyd's Reporting

This folder contains granular transactional-level synthetic data that can be aggregated via ETL tools (KNIME, Alteryx) to produce the Power BI outputs in `exports/powerbi/`.

## Data Files

| File | Records | Description |
|------|---------|-------------|
| `syndicates.csv` | 10 | Reference data for Lloyd's syndicates |
| `exchange_rates.csv` | 108 | Currency exchange rates by year/type |
| `policies.csv` | 5,000 | Policy master data with premium info |
| `claim_transactions.csv` | 1,433 | Individual claim payment/reserve transactions |
| `premium_transactions.csv` | 20,000 | Premium bookings by policy/period |
| `asset_holdings.csv` | 2,213 | Asset positions by syndicate/quarter |
| `reserve_movements.csv` | 2,400 | Technical provisions and IBNR movements |
| `risk_exposures.csv` | 2,400 | SCR risk components by syndicate/LOB |

## Schema Overview

### 1. syndicates.csv (Reference Data)
- `Syndicate_Number`: Unique syndicate identifier (e.g., 2987, 33)
- `Managing_Agent`: Managing agent name
- `LEI`: Legal Entity Identifier
- `Undertaking_Name`: Full syndicate name
- `Status`: Reporting status (Approved, Draft, Submitted)

### 2. exchange_rates.csv (Reference Data)
- `Year_of_Account`: Year
- `Currency`: Currency code (GBP, USD, EUR, etc.)
- `Exchange_Rate_GBP`: Rate to GBP
- `Rate_Type`: Average or Closing
- `Rate_Date`: Date of rate

### 3. policies.csv (Master Data)
- `Policy_ID`: Unique policy identifier
- `Syndicate_Number`: Syndicate
- `Year_of_Account`: Year of account
- `LOB_Code`: Line of business code (A1, A2, D1, D2, E1)
- `LOB_Name`: Line of business description
- `Currency`: Transaction currency
- `Inception_Date`, `Expiry_Date`: Policy period
- `Gross_Written_Premium`, `Net_Written_Premium`: Premium amounts
- `Risk_Code`: Risk classification (1-9)
- `Country`: Risk location

### 4. claim_transactions.csv (Transactional)
- `Transaction_ID`: Unique transaction ID
- `Claim_Reference`: Claim number (CLMxxxxxx)
- `Syndicate_Number`, `Year_of_Account`: Claim allocation
- `Risk_Code`, `Currency`, `Status`: Claim attributes
- `Transaction_Type`: Payment type
- `Transaction_Date`, `Loss_Date`, `Report_Date`: Key dates
- `Amount`: Payment amount
- `Outstanding_Amount`, `Incurred_Amount`: Reserves
- `LOB_Code`, `Country`: Classification
- `Reinsurance_Recovery`: RI recovery amount

### 5. premium_transactions.csv (Transactional)
- `Transaction_ID`: Unique transaction ID
- `Policy_ID`: Link to policy
- `Syndicate_Number`, `Year_of_Account`, `LOB_Code`: Classification
- `Transaction_Type`: Written_Premium
- `Transaction_Date`, `Quarter`: Timing
- `Gross_Amount`, `Net_Amount`: Premium amounts
- `Ceding_Commission`: Commission paid
- `Earned_Premium`, `Unearned_Premium`: Earning pattern

### 6. asset_holdings.csv (Position Data)
- `Asset_ID`: Unique asset ID
- `Syndicate_Number`: Syndicate
- `Reporting_Date`, `Quarter`: Position date
- `Asset_Type`: Asset classification
- `Asset_Category`: Liquid/Illiquid
- `Currency`, `ISIN`, `Issuer`: Asset details
- `Market_Value`, `Book_Value`: Valuations
- `Credit_Rating`, `Duration`, `Yield`: Risk metrics

### 7. reserve_movements.csv (Transactional)
- `Reserve_ID`: Unique reserve ID
- `Syndicate_Number`, `LOB_Code`: Classification
- `Valuation_Date`, `Quarter`: Timing
- `Reserve_Type`: BEL, Risk_Margin, Reinsurance_Recoverables, IBNR
- `Movement_Type`: Revaluation
- `Amount`: Reserve amount
- `Discounted`, `Confidence_Level`: Technical details

### 8. risk_exposures.csv (Transactional)
- `Exposure_ID`: Unique exposure ID
- `Syndicate_Number`, `LOB_Code`: Classification
- `Exposure_Date`, `Quarter`: Timing
- `Risk_Type`: Premium_Risk, Reserve_Risk, Cat_Risk, Market_Risk, etc.
- `Risk_Category`: Underwriting/Non_Underwriting
- `Gross_Exposure`, `Net_Exposure`: Exposure amounts
- `SCR_Contribution`: Capital requirement
- `Diversification_Benefit`: Diversification credit

## ETL Aggregation Mappings

### Claims Aggregations
```
claim_transactions -> Claims_DetailedClaims
  GROUP BY: Claim_Reference
  AGGREGATE: SUM(Amount) as Paid_Amount, FIRST(Outstanding_Amount), FIRST(Incurred_Amount)

claim_transactions -> Claims_BySyndicate
  GROUP BY: Syndicate_Number
  AGGREGATE: COUNT(DISTINCT Claim_Reference), SUM(Amount), SUM(Outstanding_Amount), SUM(Incurred_Amount)

claim_transactions -> Claims_ByRiskCode
  GROUP BY: Risk_Code
  AGGREGATE: COUNT(DISTINCT Claim_Reference), SUM(Incurred_Amount)

claim_transactions -> Claims_ByStatus
  GROUP BY: Status
  AGGREGATE: COUNT(DISTINCT Claim_Reference), SUM(Outstanding_Amount), SUM(Amount)
```

### Premium Aggregations
```
premium_transactions -> RRA_291_GrossPremiumIBNR
  GROUP BY: Syndicate_Number, Year_of_Account, LOB_Code
  AGGREGATE: SUM(Gross_Amount) as Gross_Written_Premium, SUM(Earned_Premium), etc.

premium_transactions -> SBF_PremiumForecast
  GROUP BY: Syndicate_Number, Year_of_Account
  AGGREGATE: SUM(Gross_Amount), SUM(Net_Amount)
```

### Asset Aggregations
```
asset_holdings -> Liquidity_AssetBreakdown
  GROUP BY: Syndicate_Number, Quarter
  AGGREGATE: SUM(Market_Value) WHERE Asset_Category='Liquid' as Liquid_Assets, etc.

asset_holdings -> QRT_IR0201_Balance_Sheet
  GROUP BY: Syndicate_Number
  AGGREGATE: SUM(Market_Value) by Asset_Type
```

### Reserve Aggregations
```
reserve_movements -> QSR_TechnicalProvisions
  GROUP BY: Syndicate_Number, LOB_Code
  AGGREGATE: SUM(Amount) WHERE Reserve_Type='Best_Estimate_Liabilities', etc.
```

### Risk Aggregations
```
risk_exposures -> LCR_SCR_Summary
  GROUP BY: Syndicate_Number
  PIVOT: Risk_Type
  AGGREGATE: SUM(SCR_Contribution)
```

## KNIME Workflow Example

1. **File Reader** nodes for each CSV
2. **Joiner** to link policies to claims/premiums
3. **GroupBy** to aggregate by required dimensions
4. **Pivot** for matrix reports
5. **Column Rename** to match target schema
6. **CSV Writer** to output Power BI files

## Alteryx Workflow Example

1. **Input Data** tools for each CSV
2. **Join** to link related tables
3. **Summarize** to aggregate with Sum/Count
4. **Cross Tab** for pivot operations
5. **Select** to rename columns
6. **Output Data** to write Power BI CSVs

## Regenerating Data

```bash
cd python_scripts/data_generation
python generate_raw_transactional_data.py --output-dir ../../raw_data --exports-dir ../../exports/powerbi
```

## Validation

```bash
python python_scripts/data_generation/validate_aggregations.py
```

## Notes

- Random seed: 42 (for reproducibility)
- All amounts are in transaction currency
- Dates are in ISO format (YYYY-MM-DD)
- Syndicates: 2987, 33, 1183, 2791, 623, 4242, 5000, 1910, 2010, 2525
- Lines of Business: A1, A2, D1, D2, E1
- Currencies: GBP, USD, EUR, CAD, AUD, JPY, CHF
