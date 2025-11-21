# Power BI Script: AAD230 - List of Assets (S.06.02.01) Transformer
# This script transforms raw asset data into the AAD230 return format for Power BI
#
# Usage in Power BI:
# 1. Import your asset data
# 2. Run this script as an R transformation
# 3. The output will be the formatted AAD230 table

library(dplyr)
library(tidyr)
library(lubridate)

#' Transform raw asset data into AAD230 format
transform_aad230 <- function(dataset) {
  # Define the AAD230 schema based on Solvency II specifications
  aad230_columns <- c(
    'C0060_Portfolio' = 'Portfolio',
    'C0070_Fund_Number' = 'Fund_Number',
    'C0090_Asset_Held_Unit_Linked' = 'Asset_Held_Unit_Linked',
    'C0040_Asset_ID_Code' = 'Asset_ID_Code',
    'C0050_Asset_ID_Code_Type' = 'Asset_ID_Code_Type',
    'C0100_Asset_Pledged_Collateral' = 'Asset_Pledged_Collateral',
    'C0190_Item_Title' = 'Item_Title',
    'C0200_Issuer_Name' = 'Issuer_Name',
    'C0210_Issuer_Code' = 'Issuer_Code',
    'C0220_Type_Issuer_Code' = 'Type_Issuer_Code',
    'C0230_Issuer_Sector' = 'Issuer_Sector',
    'C0240_Issuer_Group' = 'Issuer_Group',
    'C0250_Issuer_Group_Code' = 'Issuer_Group_Code',
    'C0260_Type_Issuer_Group_Code' = 'Type_Issuer_Group_Code',
    'C0270_Issuer_Country' = 'Issuer_Country',
    'C0110_Country_Custody' = 'Country_Custody',
    'C0280_Currency' = 'Currency',
    'C0290_CIC' = 'CIC',
    'C0310_Holdings_Related_Undertakings' = 'Holdings_Related_Undertakings',
    'C0320_External_Rating' = 'External_Rating',
    'C0330_Nominated_ECAI' = 'Nominated_ECAI',
    'C0360_Duration' = 'Duration',
    'C0130_Quantity' = 'Quantity',
    'C0140_Par_Amount' = 'Par_Amount',
    'C0370_Unit_Solvency_II_Price' = 'Unit_Solvency_II_Price',
    'C0380_Unit_Pct_Par_Amount_Price' = 'Unit_Pct_Par_Amount_Price',
    'C0150_Valuation_Method' = 'Valuation_Method',
    'C0160_Acquisition_Value' = 'Acquisition_Value',
    'C0170_Total_Solvency_II_Amount' = 'Total_Solvency_II_Amount',
    'C0390_Maturity_Date' = 'Maturity_Date',
    'C0180_Accrued_Interest' = 'Accrued_Interest',
    'C0180_Market_Value_Non_FIS' = 'Market_Value_Non_FIS',
    'C0180_Market_Value_FIS' = 'Market_Value_FIS',
    'C0080_Matching_Portfolio_Numbers' = 'Matching_Portfolio_Numbers',
    'C0120_Custodian' = 'Custodian',
    'C0300_Infrastructure_Investment' = 'Infrastructure_Investment',
    'C0340_Credit_Quality_Step' = 'Credit_Quality_Step',
    'C0350_Internal_Rating' = 'Internal_Rating',
    'C0292_SCR_Calc_Approach_CIU' = 'SCR_Calc_Approach_CIU',
    'Asset_Liquidity' = 'Asset_Liquidity',
    'Fund_Redemption_Frequency' = 'Fund_Redemption_Frequency',
    'Trust_Fund_Name' = 'Trust_Fund_Name'
  )

  # Rename columns to EIOPA codes
  output_df <- dataset
  for (eiopa_code in names(aad230_columns)) {
    source_col <- aad230_columns[eiopa_code]
    if (source_col %in% colnames(dataset)) {
      output_df[[eiopa_code]] <- dataset[[source_col]]
    } else {
      output_df[[eiopa_code]] <- NA
    }
  }

  # Select only the EIOPA coded columns
  output_df <- output_df %>%
    select(all_of(names(aad230_columns)))

  # Apply data validations and transformations
  valid_portfolios <- c('L', 'NL', 'RF', 'OIF', 'SF', 'G')
  output_df <- output_df %>%
    mutate(
      # Portfolio validation
      C0060_Portfolio = ifelse(C0060_Portfolio %in% valid_portfolios, C0060_Portfolio, 'NL'),

      # Y/N validations
      C0090_Asset_Held_Unit_Linked = ifelse(C0090_Asset_Held_Unit_Linked %in% c('Y', 'N'), C0090_Asset_Held_Unit_Linked, 'N'),
      C0100_Asset_Pledged_Collateral = ifelse(C0100_Asset_Pledged_Collateral %in% c('Y', 'N'), C0100_Asset_Pledged_Collateral, 'N'),
      C0310_Holdings_Related_Undertakings = ifelse(C0310_Holdings_Related_Undertakings %in% c('Y', 'N'), C0310_Holdings_Related_Undertakings, 'N'),
      C0300_Infrastructure_Investment = ifelse(C0300_Infrastructure_Investment %in% c('Y', 'N'), C0300_Infrastructure_Investment, 'N'),

      # Numeric conversions
      C0070_Fund_Number = as.numeric(C0070_Fund_Number),
      C0360_Duration = as.numeric(C0360_Duration),
      C0130_Quantity = as.numeric(C0130_Quantity),
      C0140_Par_Amount = as.numeric(C0140_Par_Amount),
      C0370_Unit_Solvency_II_Price = as.numeric(C0370_Unit_Solvency_II_Price),
      C0380_Unit_Pct_Par_Amount_Price = as.numeric(C0380_Unit_Pct_Par_Amount_Price),
      C0160_Acquisition_Value = as.numeric(C0160_Acquisition_Value),
      C0170_Total_Solvency_II_Amount = as.numeric(C0170_Total_Solvency_II_Amount),
      C0180_Accrued_Interest = as.numeric(C0180_Accrued_Interest),
      C0180_Market_Value_Non_FIS = as.numeric(C0180_Market_Value_Non_FIS),
      C0180_Market_Value_FIS = as.numeric(C0180_Market_Value_FIS),
      C0080_Matching_Portfolio_Numbers = as.numeric(C0080_Matching_Portfolio_Numbers),
      C0340_Credit_Quality_Step = as.numeric(C0340_Credit_Quality_Step),

      # Date conversion
      C0390_Maturity_Date = as.Date(C0390_Maturity_Date)
    )

  # Calculate Total Solvency II Amount if missing
  output_df <- output_df %>%
    mutate(
      C0170_Total_Solvency_II_Amount = ifelse(
        is.na(C0170_Total_Solvency_II_Amount),
        C0130_Quantity * C0370_Unit_Solvency_II_Price,
        C0170_Total_Solvency_II_Amount
      )
    )

  return(output_df)
}

#' Validate AAD230 data against business rules
validate_aad230 <- function(df) {
  cat("Validation Results:\n")
  cat("===================\n\n")

  errors <- character(0)
  warnings <- character(0)

  # Check for duplicate Asset IDs
  duplicate_ids <- df %>%
    group_by(C0040_Asset_ID_Code) %>%
    filter(n() > 1) %>%
    pull(C0040_Asset_ID_Code) %>%
    unique()

  if (length(duplicate_ids) > 0) {
    errors <- c(errors, sprintf("Duplicate Asset ID Codes found: %s", paste(duplicate_ids, collapse = ", ")))
  }

  # Check for required fields
  required_fields <- c('C0040_Asset_ID_Code', 'C0050_Asset_ID_Code_Type', 'C0170_Total_Solvency_II_Amount')

  for (field in required_fields) {
    null_count <- sum(is.na(df[[field]]))
    if (null_count > 0) {
      errors <- c(errors, sprintf("Required field %s has %d null values", field, null_count))
    }
  }

  # Check Fund Number for RF portfolio
  rf_no_fund <- df %>%
    filter(C0060_Portfolio == 'RF', is.na(C0070_Fund_Number)) %>%
    nrow()

  if (rf_no_fund > 0) {
    warnings <- c(warnings, sprintf("RF Portfolio entries without Fund Number: %d records", rf_no_fund))
  }

  # Check for negative values
  negative_sii <- sum(df$C0170_Total_Solvency_II_Amount < 0, na.rm = TRUE)
  if (negative_sii > 0) {
    warnings <- c(warnings, sprintf("Total Solvency II Amount has %d negative values", negative_sii))
  }

  # Print results
  if (length(errors) > 0) {
    cat("ERRORS:\n")
    for (error in errors) {
      cat(sprintf("  - %s\n", error))
    }
  }

  if (length(warnings) > 0) {
    cat("\nWARNINGS:\n")
    for (warning in warnings) {
      cat(sprintf("  - %s\n", warning))
    }
  }

  if (length(errors) == 0 && length(warnings) == 0) {
    cat("All validations passed!\n")
  }

  cat("\n")
}

#' Generate summary statistics
add_summary_statistics <- function(df) {
  cat("Summary Statistics:\n")
  cat("===================\n\n")

  cat(sprintf("Total Records: %d\n", nrow(df)))
  cat(sprintf("Total Solvency II Amount: %.2f\n", sum(df$C0170_Total_Solvency_II_Amount, na.rm = TRUE)))
  cat(sprintf("Total Acquisition Value: %.2f\n", sum(df$C0160_Acquisition_Value, na.rm = TRUE)))

  cat("\nBy Portfolio:\n")
  portfolio_summary <- df %>%
    group_by(C0060_Portfolio) %>%
    summarise(Total_SII_Amount = sum(C0170_Total_Solvency_II_Amount, na.rm = TRUE)) %>%
    arrange(desc(Total_SII_Amount))
  print(portfolio_summary)

  cat("\nBy CIC:\n")
  cic_summary <- df %>%
    group_by(C0290_CIC) %>%
    summarise(Total_SII_Amount = sum(C0170_Total_Solvency_II_Amount, na.rm = TRUE)) %>%
    arrange(desc(Total_SII_Amount)) %>%
    head(10)
  print(cic_summary)

  cat(sprintf("\nUnique Issuers: %d\n", n_distinct(df$C0200_Issuer_Name)))
  cat(sprintf("Unique Currencies: %d\n", n_distinct(df$C0280_Currency)))
}

# Main execution for Power BI
# Power BI provides the 'dataset' variable automatically

# Transform the data
result <- transform_aad230(dataset)

# Validate the output
validate_aad230(result)

# Generate summary statistics
add_summary_statistics(result)

# The 'result' variable is automatically returned to Power BI
