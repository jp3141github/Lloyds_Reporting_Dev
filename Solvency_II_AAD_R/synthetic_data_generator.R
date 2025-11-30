# Synthetic Lloyd's of London Data Generator for Solvency II AAD Returns
# This script generates synthetic data that mimics Lloyd's of London insurance data
# for use with Power BI and AAD return generation.

library(dplyr)
library(tidyr)
library(lubridate)

# Set random seed for reproducibility
set.seed(42)

# Lloyd's specific reference data
portfolios <- c('L', 'NL', 'RF')
currencies <- c('GBP', 'USD', 'EUR', 'JPY', 'CHF', 'AUD', 'CAD')
countries <- c('GB', 'US', 'DE', 'FR', 'IT', 'ES', 'NL', 'BE', 'IE', 'LU')
asset_types <- c('Government Bond', 'Corporate Bond', 'Equity', 'Property',
                 'Cash', 'Collective Investment', 'Derivatives')
cic_codes <- c('1', '2', '31', '32', '4', '5', '6', '71', '72', '8', '9')
issuer_sectors <- c('1', '2', '3', '4', '5', '6')
rating_agencies <- c('1', '2', '3', '4')
external_ratings <- c('AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC')

current_date <- as.Date('2024-12-31')

#' Generate synthetic asset identification codes
generate_asset_id <- function(id_type = 'ISIN') {
  if (id_type == 'ISIN') {
    # ISIN format: 2 letter country code + 9 alphanumeric + 1 check digit
    country <- sample(countries, 1)
    code <- paste0(sample(c(LETTERS, 0:9), 9, replace = TRUE), collapse = '')
    return(paste0(country, code, sample(0:9, 1)))
  } else if (id_type == 'SEDOL') {
    # SEDOL format: 7 alphanumeric characters
    return(paste0(sample(c(LETTERS, 0:9), 7, replace = TRUE), collapse = ''))
  } else if (id_type == 'CUSIP') {
    # CUSIP format: 9 alphanumeric characters
    return(paste0(sample(c(LETTERS, 0:9), 9, replace = TRUE), collapse = ''))
  } else {
    return(paste0(sample(c(LETTERS, 0:9), 10, replace = TRUE), collapse = ''))
  }
}

#' Generate synthetic Legal Entity Identifier
generate_lei_code <- function() {
  paste0(sample(c(LETTERS, 0:9), 20, replace = TRUE), collapse = '')
}

#' Generate AAD230 - List of assets (S.06.02.01)
generate_aad230_assets <- function(num_records = 1000) {
  cat("Generating AAD230 assets data...\n")

  aad230_data <- data.frame(
    Portfolio = sample(portfolios, num_records, replace = TRUE),
    Fund_Number = sample(c(1:50, NA), num_records, replace = TRUE),
    Asset_Held_Unit_Linked = sample(c('Y', 'N'), num_records, replace = TRUE),
    Asset_ID_Code = sapply(1:num_records, function(x) generate_asset_id('ISIN')),
    Asset_ID_Code_Type = sample(c('ISIN', 'SEDOL', 'CUSIP', 'BT'), num_records, replace = TRUE),
    Asset_Pledged_Collateral = sample(c('Y', 'N'), num_records, replace = TRUE),
    Item_Title = paste('Asset', 1:num_records, '-', sample(asset_types, num_records, replace = TRUE)),
    Issuer_Name = paste('Issuer', sample(1:200, num_records, replace = TRUE)),
    Issuer_Code = sapply(1:num_records, function(x) generate_lei_code()),
    Type_Issuer_Code = 'LEI',
    Issuer_Sector = sample(issuer_sectors, num_records, replace = TRUE),
    Issuer_Group = paste('Group', sample(1:50, num_records, replace = TRUE)),
    Issuer_Group_Code = sapply(1:num_records, function(x) generate_lei_code()),
    Type_Issuer_Group_Code = 'LEI',
    Issuer_Country = sample(countries, num_records, replace = TRUE),
    Country_Custody = sample(countries, num_records, replace = TRUE),
    Currency = sample(currencies, num_records, replace = TRUE),
    CIC = sample(cic_codes, num_records, replace = TRUE),
    Holdings_Related_Undertakings = sample(c('Y', 'N'), num_records, replace = TRUE),
    External_Rating = sample(external_ratings, num_records, replace = TRUE),
    Nominated_ECAI = sample(rating_agencies, num_records, replace = TRUE),
    Duration = round(runif(num_records, 0.5, 20), 2),
    Quantity = sample(1000:1000000, num_records, replace = TRUE),
    Par_Amount = 0,  # Will be calculated
    Unit_Solvency_II_Price = round(runif(num_records, 50, 150), 4),
    Unit_Pct_Par_Amount_Price = round(runif(num_records, 95, 105), 4),
    Valuation_Method = sample(c('1', '2'), num_records, replace = TRUE),
    Acquisition_Value = 0,  # Will be calculated
    Total_Solvency_II_Amount = 0,  # Will be calculated
    Maturity_Date = current_date + days(sample(365:10950, num_records, replace = TRUE)),
    Accrued_Interest = 0,  # Will be calculated
    Market_Value_Non_FIS = 0,  # Will be calculated
    Market_Value_FIS = 0,  # Will be calculated
    Issue_Type = sample(c('1', '2', '3'), num_records, replace = TRUE),
    Matching_Portfolio_Numbers = sample(1:10, num_records, replace = TRUE),
    Custodian = paste('Custodian', sample(1:20, num_records, replace = TRUE)),
    Infrastructure_Investment = sample(c('Y', 'N'), num_records, replace = TRUE),
    Credit_Quality_Step = sample(0:6, num_records, replace = TRUE),
    Internal_Rating = sample(c('A', 'B', 'C', 'D'), num_records, replace = TRUE),
    SCR_Calc_Approach_CIU = sample(c('1', '2', '9', NA), num_records, replace = TRUE),
    Asset_Liquidity = sample(c('1', '2', '3'), num_records, replace = TRUE),
    Fund_Redemption_Frequency = sample(c('D', 'W', 'M', 'Q', 'A', NA), num_records, replace = TRUE),
    Trust_Fund_Name = NA
  ) %>%
    mutate(
      Par_Amount = round(Quantity * runif(n(), 0.8, 1.2), 2),
      Total_Solvency_II_Amount = round(Quantity * Unit_Solvency_II_Price, 2),
      Acquisition_Value = round(Total_Solvency_II_Amount * runif(n(), 0.95, 1.05), 2),
      Accrued_Interest = round(Total_Solvency_II_Amount * runif(n(), 0, 0.05), 2),
      Market_Value_Non_FIS = round(Total_Solvency_II_Amount * runif(n(), 0.98, 1.02), 2),
      Market_Value_FIS = round(Total_Solvency_II_Amount * runif(n(), 0.98, 1.02), 2)
    )

  return(aad230_data)
}

#' Generate AAD233 - Open derivatives (S.08.01.01)
generate_aad233_derivatives <- function(num_derivatives = 100) {
  cat("Generating AAD233 derivatives data...\n")

  derivative_types <- c('FX Forward', 'Interest Rate Swap', 'Credit Default Swap',
                       'Equity Option', 'Commodity Future')

  aad233_data <- data.frame(
    Portfolio = sample(portfolios, num_derivatives, replace = TRUE),
    Fund_Number = sample(c(1:50, NA), num_derivatives, replace = TRUE),
    Derivatives_Unit_Linked = sample(c('Y', 'N'), num_derivatives, replace = TRUE),
    Derivative_ID_Code = sapply(1:num_derivatives, function(x) generate_asset_id('ISIN')),
    Derivative_ID_Code_Type = 'ISIN',
    Counterparty_Name = paste('Counterparty', sample(1:50, num_derivatives, replace = TRUE)),
    Counterparty_Code = sapply(1:num_derivatives, function(x) generate_lei_code()),
    Type_Counterparty_Code = 'LEI',
    External_Rating = sample(external_ratings, num_derivatives, replace = TRUE),
    Nominated_ECAI = sample(rating_agencies, num_derivatives, replace = TRUE),
    Counterparty_Group = paste('CP Group', sample(1:30, num_derivatives, replace = TRUE)),
    Counterparty_Group_Code = sapply(1:num_derivatives, function(x) generate_lei_code()),
    Type_Counterparty_Group_Code = 'LEI',
    Contract_Name = paste(sample(derivative_types, num_derivatives, replace = TRUE), 'Contract', 1:num_derivatives),
    Instrument_Underlying = sample(c('Equity', 'Bond', 'Currency', 'Commodity', 'Index'), num_derivatives, replace = TRUE),
    Currency = sample(currencies, num_derivatives, replace = TRUE),
    CIC = sample(c('A', 'B', 'C', 'D'), num_derivatives, replace = TRUE),
    Use_Derivative = sample(c('MI', 'MA', 'EPM'), num_derivatives, replace = TRUE),
    Delta = round(runif(num_derivatives, -1, 1), 4),
    Notional_Amount = round(runif(num_derivatives, 1000000, 50000000), 2),
    Buyer_Seller = sample(c('B', 'S'), num_derivatives, replace = TRUE),
    Premium_Paid = 0,  # Will be calculated
    Premium_Received = 0,  # Will be calculated
    Number_Contracts = sample(1:1000, num_derivatives, replace = TRUE),
    Contract_Size = round(runif(num_derivatives, 100, 10000), 2),
    Trigger_Value = 0,  # Will be calculated
    Unwind_Trigger = sample(c('B', 'F', 'R', 'N', 'M', 'O', 'NT'), num_derivatives, replace = TRUE),
    Max_Loss_Unwinding = 0,  # Will be calculated
    Swap_Outflow_Amount = 0,  # Will be calculated
    Swap_Inflow_Amount = 0,  # Will be calculated
    Swap_Delivered_Currency = sample(currencies, num_derivatives, replace = TRUE),
    Swap_Received_Currency = sample(currencies, num_derivatives, replace = TRUE),
    Initial_Date = current_date - days(sample(30:3650, num_derivatives, replace = TRUE)),
    Maturity_Date = current_date + days(sample(365:10950, num_derivatives, replace = TRUE)),
    Duration = round(runif(num_derivatives, 0.1, 10), 2),
    Valuation_Method = sample(c('1', '2'), num_derivatives, replace = TRUE),
    Total_SII_Amount_Non_FIS = 0,  # Will be calculated
    Total_SII_Amount_FIS = 0,  # Will be calculated
    Solvency_II_Value = 0,  # Will be calculated
    Credit_Quality_Step = sample(0:6, num_derivatives, replace = TRUE),
    Internal_Rating = sample(c('A', 'B', 'C', 'D'), num_derivatives, replace = TRUE),
    Type_Code_Underlying = sample(c('1', '2', '3'), num_derivatives, replace = TRUE),
    Trust_Fund_Name = NA
  ) %>%
    mutate(
      Premium_Paid = round(Notional_Amount * runif(n(), 0, 0.05), 2),
      Premium_Received = round(Notional_Amount * runif(n(), 0, 0.05), 2),
      Trigger_Value = round(Notional_Amount * runif(n(), 0.7, 1.3), 2),
      Max_Loss_Unwinding = round(Notional_Amount * runif(n(), 0.1, 0.3), 2),
      Swap_Outflow_Amount = round(Notional_Amount * runif(n(), 0, 0.5), 2),
      Swap_Inflow_Amount = round(Notional_Amount * runif(n(), 0, 0.5), 2),
      Total_SII_Amount_Non_FIS = round(Notional_Amount * runif(n(), -0.1, 0.1), 2),
      Total_SII_Amount_FIS = round(Notional_Amount * runif(n(), -0.1, 0.1), 2),
      Solvency_II_Value = round(Notional_Amount * runif(n(), -0.1, 0.1), 2)
    )

  return(aad233_data)
}

#' Generate AAD235 - Income/gains and losses (S.09.01.01)
generate_aad235_income <- function() {
  cat("Generating AAD235 income data...\n")

  asset_categories <- c('10', '20', '31', '32', '40', '50', '60', '71', '72', '80', '90', '95')

  aad235_data <- data.frame(
    Asset_Category = asset_categories,
    Dividends = round(runif(length(asset_categories), 0, 5000000), 2),
    Interest = round(runif(length(asset_categories), 0, 10000000), 2),
    Rent = round(runif(length(asset_categories), 0, 2000000), 2),
    Net_Gains_Losses = round(runif(length(asset_categories), -5000000, 10000000), 2),
    Unrealised_Gains_Losses = round(runif(length(asset_categories), -3000000, 8000000), 2),
    Portfolio = sample(portfolios, length(asset_categories), replace = TRUE),
    Asset_Held_Unit_Linked = sample(c('Y', 'N'), length(asset_categories), replace = TRUE),
    Fund_Number = sample(c(1:50, NA), length(asset_categories), replace = TRUE)
  )

  return(aad235_data)
}

#' Generate AAD236 - CIU Look-through (S.06.03.01)
generate_aad236_ciu_lookthrough <- function(num_funds = 50) {
  cat("Generating AAD236 CIU look-through data...\n")

  fund_types <- c('Equity Fund', 'Bond Fund', 'Mixed Fund', 'Property Fund')

  aad236_data <- data.frame(
    Investment_Fund_Code = sapply(1:num_funds, function(x) generate_asset_id('ISIN')),
    Investment_Fund_Code_Type = 'ISIN',
    CIU_ID_Code = sapply(1:num_funds, function(x) generate_asset_id('ISIN')),
    CIU_ID_Code_Type = 'ISIN',
    Item_Title = paste('Fund', 1:num_funds, '-', sample(fund_types, num_funds, replace = TRUE)),
    Issuer_Group = paste('Fund Manager', sample(1:30, num_funds, replace = TRUE)),
    Issuer_Group_Code = sapply(1:num_funds, function(x) generate_lei_code()),
    Issuer_Group_Code_Type = 'LEI',
    External_Rating = sample(external_ratings, num_funds, replace = TRUE),
    Rating_Agency = sample(rating_agencies, num_funds, replace = TRUE),
    Duration = round(runif(num_funds, 1, 15), 2),
    CIC = sample(c('91', '92', '93', '94', '95', '96'), num_funds, replace = TRUE),
    Underlying_Asset_Category = sample(c('1', '2', '3', '4', '5', '9'), num_funds, replace = TRUE),
    Country_Issue = sample(countries, num_funds, replace = TRUE),
    Currency = sample(currencies, num_funds, replace = TRUE),
    Total_SII_Amount_Non_FIS = 0,  # Will be calculated
    Total_SII_Amount_FIS = 0,  # Will be calculated
    Total_Solvency_II_Amount = round(runif(num_funds, 5000000, 100000000), 2),
    Issue_Type = sample(c('1', '2', '3'), num_funds, replace = TRUE),
    Level_Look_Through = sample(c('1', '2', '3', '9'), num_funds, replace = TRUE),
    Maturity_Date = current_date + days(sample(365:3650, num_funds, replace = TRUE)),
    Fund_Number = sample(c(1:50, NA), num_funds, replace = TRUE),
    Notional_Amount = 0,  # Will be calculated
    Asset_Liquidity = sample(c('1', '2', '3'), num_funds, replace = TRUE),
    Trust_Fund_Name = NA
  ) %>%
    mutate(
      Total_SII_Amount_Non_FIS = round(Total_Solvency_II_Amount * runif(n(), 0.98, 1.02), 2),
      Total_SII_Amount_FIS = round(Total_Solvency_II_Amount * runif(n(), 0.98, 1.02), 2),
      Notional_Amount = round(Total_Solvency_II_Amount * runif(n(), 0.95, 1.05), 2)
    )

  return(aad236_data)
}

#' Generate AAD237 - Loans and mortgages (S.10.01.01)
generate_aad237_loans_mortgages <- function(num_loans = 200) {
  cat("Generating AAD237 loans and mortgages data...\n")

  aad237_data <- data.frame(
    Loan_ID = paste0('LOAN', sample(100000:999999, num_loans, replace = FALSE)),
    Loan_Type = sample(c('1', '2', '3', '4'), num_loans, replace = TRUE),
    Portfolio = sample(portfolios, num_loans, replace = TRUE),
    Fund_Number = sample(c(1:50, NA), num_loans, replace = TRUE),
    Counterparty_Name = paste('Borrower', sample(1:500, num_loans, replace = TRUE)),
    Counterparty_Code = sapply(1:num_loans, function(x) generate_lei_code()),
    Type_Counterparty_Code = 'LEI',
    Country = sample(countries, num_loans, replace = TRUE),
    Currency = sample(currencies, num_loans, replace = TRUE),
    Original_Amount = 0,  # Will be calculated
    Outstanding_Amount = round(runif(num_loans, 100000, 10000000), 2),
    Interest_Rate = round(runif(num_loans, 1, 8), 3),
    Acquisition_Date = current_date - days(sample(365:7300, num_loans, replace = TRUE)),
    Maturity_Date = current_date + days(sample(365:9125, num_loans, replace = TRUE)),
    Duration = round(runif(num_loans, 1, 25), 2),
    Collateral_Value = 0,  # Will be calculated
    Valuation_Method = sample(c('1', '2'), num_loans, replace = TRUE),
    Total_Solvency_II_Amount = 0,  # Will be calculated
    Credit_Quality_Step = sample(0:6, num_loans, replace = TRUE),
    Internal_Rating = sample(c('A', 'B', 'C', 'D'), num_loans, replace = TRUE),
    Asset_Liquidity = sample(c('1', '2', '3'), num_loans, replace = TRUE)
  ) %>%
    mutate(
      Original_Amount = round(Outstanding_Amount * runif(n(), 1.1, 1.5), 2),
      Collateral_Value = round(Outstanding_Amount * runif(n(), 1.2, 2.0), 2),
      Total_Solvency_II_Amount = round(Outstanding_Amount * runif(n(), 0.95, 1.05), 2)
    )

  return(aad237_data)
}

#' Generate AAD238 - Property (S.11.01.01)
generate_aad238_property <- function(num_properties = 100) {
  cat("Generating AAD238 property data...\n")

  property_types <- c('Office', 'Retail', 'Industrial', 'Residential', 'Mixed Use', 'Land')

  aad238_data <- data.frame(
    Property_ID = paste0('PROP', sample(10000:99999, num_properties, replace = FALSE)),
    Portfolio = sample(portfolios, num_properties, replace = TRUE),
    Fund_Number = sample(c(1:50, NA), num_properties, replace = TRUE),
    Property_Type = sample(property_types, num_properties, replace = TRUE),
    Country = sample(countries, num_properties, replace = TRUE),
    Currency = sample(currencies, num_properties, replace = TRUE),
    Purchase_Date = current_date - days(sample(365:7300, num_properties, replace = TRUE)),
    Purchase_Price = 0,  # Will be calculated
    Valuation_Date = current_date,
    Current_Valuation = round(runif(num_properties, 1000000, 50000000), 2),
    Rental_Income_Annual = 0,  # Will be calculated
    Occupancy_Rate = round(runif(num_properties, 70, 100), 1),
    Valuation_Method = sample(c('1', '2'), num_properties, replace = TRUE),
    Total_Solvency_II_Amount = 0,  # Will be calculated
    Asset_Liquidity = sample(c('2', '3'), num_properties, replace = TRUE),
    Trust_Fund_Name = NA
  ) %>%
    mutate(
      Purchase_Price = round(Current_Valuation * runif(n(), 0.7, 1.2), 2),
      Rental_Income_Annual = round(Current_Valuation * runif(n(), 0.03, 0.08), 2),
      Total_Solvency_II_Amount = Current_Valuation
    )

  return(aad238_data)
}

#' Generate all AAD datasets
generate_all_datasets <- function(num_assets = 1000) {
  cat("=======================================================\n")
  cat("Generating synthetic Lloyd's data for AAD Returns...\n")
  cat("=======================================================\n\n")

  datasets <- list(
    AAD230_Assets = generate_aad230_assets(num_assets),
    AAD233_Derivatives = generate_aad233_derivatives(),
    AAD235_Income = generate_aad235_income(),
    AAD236_CIU_Lookthrough = generate_aad236_ciu_lookthrough(),
    AAD237_Loans_Mortgages = generate_aad237_loans_mortgages(),
    AAD238_Property = generate_aad238_property()
  )

  cat("\n=======================================================\n")
  cat("Generation complete!\n")
  cat("=======================================================\n\n")

  for (name in names(datasets)) {
    cat(sprintf("  - %s: %d records, %d columns\n",
                name, nrow(datasets[[name]]), ncol(datasets[[name]])))
  }

  return(datasets)
}

#' Save all datasets to CSV files
save_datasets <- function(datasets, output_dir = 'synthetic_data') {
  # Create output directory if it doesn't exist
  if (!dir.exists(output_dir)) {
    dir.create(output_dir, recursive = TRUE)
  }

  cat("\nSaving datasets to CSV files...\n")

  for (name in names(datasets)) {
    filepath <- file.path(output_dir, paste0(name, '.csv'))
    write.csv(datasets[[name]], filepath, row.names = FALSE)
    cat(sprintf("Saved: %s\n", filepath))
  }

  cat(sprintf("\nAll datasets saved to '%s' directory\n", output_dir))
}

# Main execution
main <- function() {
  datasets <- generate_all_datasets(num_assets = 1000)

  save_datasets(datasets, output_dir = 'synthetic_data')

  cat("\nSample data from AAD230 (first 5 rows):\n")
  print(head(datasets$AAD230_Assets, 5))

  return(datasets)
}

# Run if executed as a script
if (!interactive()) {
  main()
}
