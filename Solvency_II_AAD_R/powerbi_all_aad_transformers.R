# Power BI Script: All AAD Transformers
# Comprehensive transformer for all AAD return tables (230, 233, 235, 236, 237, 238)
#
# Usage: Set the 'table_type' variable to specify which transformation to run

library(dplyr)
library(tidyr)
library(lubridate)

# ============================================================================
# AAD230 - List of Assets (S.06.02.01)
# ============================================================================

transform_aad230 <- function(dataset) {
  # See powerbi_aad230_transformer.R for full implementation
  # This is a simplified version for the combined script

  output_df <- dataset %>%
    mutate(
      C0060_Portfolio = Portfolio,
      C0040_Asset_ID_Code = Asset_ID_Code,
      C0050_Asset_ID_Code_Type = Asset_ID_Code_Type,
      C0170_Total_Solvency_II_Amount = as.numeric(Total_Solvency_II_Amount),
      C0280_Currency = Currency,
      C0200_Issuer_Name = Issuer_Name
    )

  return(output_df)
}

# ============================================================================
# AAD233 - Open Derivatives (S.08.01.01)
# ============================================================================

transform_aad233 <- function(dataset) {
  output_df <- dataset %>%
    mutate(
      C0060_Portfolio = Portfolio,
      C0040_Derivative_ID_Code = Derivative_ID_Code,
      C0130_Notional_Amount = as.numeric(Notional_Amount),
      C0260_Counterparty_Name = Counterparty_Name,
      C0110_Use_Derivative = Use_Derivative,
      C0140_Buyer_Seller = Buyer_Seller
    ) %>%
    mutate(
      C0110_Use_Derivative = ifelse(C0110_Use_Derivative %in% c('MI', 'MA', 'EPM'), C0110_Use_Derivative, 'MI'),
      C0140_Buyer_Seller = ifelse(C0140_Buyer_Seller %in% c('B', 'S'), C0140_Buyer_Seller, 'B')
    )

  return(output_df)
}

# ============================================================================
# AAD235 - Income/Gains and Losses (S.09.01.01)
# ============================================================================

transform_aad235 <- function(dataset) {
  output_df <- dataset %>%
    mutate(
      C0040_Asset_Category = Asset_Category,
      C0070_Dividends = as.numeric(Dividends),
      C0080_Interest = as.numeric(Interest),
      C0090_Rent = as.numeric(Rent),
      C0100_Net_Gains_Losses = as.numeric(Net_Gains_Losses),
      C0110_Unrealised_Gains_Losses = as.numeric(Unrealised_Gains_Losses),
      C0050_Portfolio = Portfolio
    ) %>%
    group_by(C0040_Asset_Category, C0050_Portfolio) %>%
    summarise(
      C0070_Dividends = sum(C0070_Dividends, na.rm = TRUE),
      C0080_Interest = sum(C0080_Interest, na.rm = TRUE),
      C0090_Rent = sum(C0090_Rent, na.rm = TRUE),
      C0100_Net_Gains_Losses = sum(C0100_Net_Gains_Losses, na.rm = TRUE),
      C0110_Unrealised_Gains_Losses = sum(C0110_Unrealised_Gains_Losses, na.rm = TRUE),
      .groups = 'drop'
    )

  return(output_df)
}

# ============================================================================
# AAD236 - CIU Look-through (S.06.03.01)
# ============================================================================

transform_aad236 <- function(dataset) {
  output_df <- dataset %>%
    mutate(
      Investment_Fund_Code = Investment_Fund_Code,
      C0010_CIU_ID_Code = CIU_ID_Code,
      C0060_Total_Solvency_II_Amount = as.numeric(Total_Solvency_II_Amount),
      C0030_Underlying_Asset_Category = Underlying_Asset_Category,
      Level_Look_Through = ifelse(Level_Look_Through %in% c('1', '2', '3', '9'), Level_Look_Through, '9'),
      Asset_Liquidity = ifelse(Asset_Liquidity %in% c('1', '2', '3'), Asset_Liquidity, '3')
    )

  return(output_df)
}

# ============================================================================
# AAD237 - Loans and Mortgages (S.10.01.01)
# ============================================================================

transform_aad237 <- function(dataset) {
  output_df <- dataset %>%
    mutate(
      Loan_ID = Loan_ID,
      Loan_Type = ifelse(Loan_Type %in% c('1', '2', '3', '4'), Loan_Type, '4'),
      Portfolio = Portfolio,
      Outstanding_Amount = as.numeric(Outstanding_Amount),
      Total_Solvency_II_Amount = as.numeric(Total_Solvency_II_Amount),
      Collateral_Value = as.numeric(Collateral_Value),
      Interest_Rate = as.numeric(Interest_Rate),
      LTV_Ratio = round((Outstanding_Amount / Collateral_Value) * 100, 2)
    )

  return(output_df)
}

# ============================================================================
# AAD238 - Property (S.11.01.01)
# ============================================================================

transform_aad238 <- function(dataset) {
  output_df <- dataset %>%
    mutate(
      Property_ID = Property_ID,
      Portfolio = Portfolio,
      Property_Type = Property_Type,
      Current_Valuation = as.numeric(Current_Valuation),
      Rental_Income_Annual = as.numeric(Rental_Income_Annual),
      Occupancy_Rate = as.numeric(Occupancy_Rate),
      Total_Solvency_II_Amount = as.numeric(Total_Solvency_II_Amount),
      Rental_Yield = round((Rental_Income_Annual / Current_Valuation) * 100, 2),
      Capital_Appreciation = round(((Current_Valuation - Purchase_Price) / Purchase_Price) * 100, 2)
    )

  return(output_df)
}

# ============================================================================
# Main Execution Logic
# ============================================================================

# Determine which transformation to run based on table_type parameter
# Set table_type before running this script in Power BI
# Example: table_type <- "AAD230"

if (!exists("table_type")) {
  # Default to AAD230 if not specified
  table_type <- "AAD230"
  cat("Warning: table_type not specified, defaulting to AAD230\n")
}

cat(sprintf("Running transformer for: %s\n", table_type))

# Execute the appropriate transformation
result <- switch(table_type,
  "AAD230" = transform_aad230(dataset),
  "AAD233" = transform_aad233(dataset),
  "AAD235" = transform_aad235(dataset),
  "AAD236" = transform_aad236(dataset),
  "AAD237" = transform_aad237(dataset),
  "AAD238" = transform_aad238(dataset),
  {
    cat(sprintf("Error: Unknown table_type '%s'\n", table_type))
    cat("Valid options: AAD230, AAD233, AAD235, AAD236, AAD237, AAD238\n")
    dataset  # Return original dataset if unknown
  }
)

# Print summary
cat(sprintf("\nTransformation complete: %d rows, %d columns\n", nrow(result), ncol(result)))

# The 'result' variable is automatically returned to Power BI
