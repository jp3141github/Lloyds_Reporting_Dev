# Synthetic Lloyd's of London Data Generator (R)
# Generates realistic synthetic data for Solvency II QSR reporting
#
# This script creates synthetic data mimicking Lloyd's of London syndicate data
# for use in Power BI reporting and analysis.

library(dplyr)
library(tidyr)

# Set seed for reproducibility
set.seed(42)

# LloydsDataGenerator Class-like structure
LloydsDataGenerator <- list(

  # Define syndicate numbers (typical Lloyd's syndicate numbers)
  syndicates = c('0001', '0033', '0099', '0218', '0308', '0510', '0609', '0727',
                 '0886', '1003', '1183', '1221', '1458', '1729', '1955', '2001',
                 '2003', '2121', '2488', '2623', '2791', '3000', '3210', '3456',
                 '4242', '5000', '5820', '6104', '6117', '6129'),

  # Lines of business (Solvency II classification)
  lines_of_business = c(
    'Medical expense insurance',
    'Income protection insurance',
    'Workers compensation insurance',
    'Motor vehicle liability insurance',
    'Other motor insurance',
    'Marine, aviation and transport insurance',
    'Fire and other damage to property insurance',
    'General liability insurance',
    'Credit and suretyship insurance',
    'Legal expenses insurance',
    'Assistance',
    'Miscellaneous financial loss',
    'Non-proportional health reinsurance',
    'Non-proportional casualty reinsurance',
    'Non-proportional marine, aviation and transport reinsurance',
    'Non-proportional property reinsurance'
  ),

  # Asset classes for investments
  asset_classes = c(
    'Government bonds',
    'Corporate bonds',
    'Equities',
    'Investment funds',
    'Property',
    'Loans and mortgages',
    'Cash and deposits'
  ),

  # Countries for geographical diversification
  countries = c('GB', 'US', 'DE', 'FR', 'JP', 'AU', 'CA', 'CH', 'NL', 'IT'),

  # Reporting date
  reporting_date = as.Date('2025-09-30')  # Q3 2025
)


# Generate QSR 002 - Balance Sheet data
generate_balance_sheet_data <- function(num_syndicates = 10) {
  syndicates <- sample(LloydsDataGenerator$syndicates,
                       min(num_syndicates, length(LloydsDataGenerator$syndicates)))

  balance_sheet_list <- lapply(syndicates, function(syndicate) {
    # Assets
    assets <- data.frame(
      Syndicate = syndicate,
      Reporting_Date = LloydsDataGenerator$reporting_date,
      Goodwill = 0,  # Always 0 per validation
      Deferred_Acquisition_Costs = 0,  # Always 0 per validation
      Intangible_Assets = 0,
      Deferred_Tax_Assets = runif(1, 0, 5000000),
      Pension_Benefit_Surplus = runif(1, 0, 2000000),
      Property_Plant_Equipment = runif(1, 1000000, 10000000),
      Investments = runif(1, 100000000, 500000000),
      Holdings_Related_Undertakings = runif(1, 0, 50000000),
      Equities = runif(1, 10000000, 100000000),
      Bonds = runif(1, 50000000, 300000000),
      Government_Bonds = runif(1, 30000000, 200000000),
      Corporate_Bonds = runif(1, 20000000, 100000000),
      Collective_Investments = runif(1, 5000000, 50000000),
      Derivatives = runif(1, 0, 10000000),
      Deposits_Other_Than_Cash = runif(1, 5000000, 30000000),
      Reinsurance_Recoverables = runif(1, 20000000, 150000000),
      Insurance_Receivables = runif(1, 10000000, 80000000),
      Reinsurance_Receivables = runif(1, 5000000, 40000000),
      Receivables_Trade = runif(1, 3000000, 20000000),
      Cash_and_Cash_Equivalents = runif(1, 10000000, 60000000),
      Other_Assets = runif(1, 2000000, 15000000),
      stringsAsFactors = FALSE
    )

    # Calculate total assets
    assets$Total_Assets <- rowSums(assets[, -c(1, 2)])

    # Liabilities
    tech_provisions <- runif(1, 150000000, 400000000)
    assets$Technical_Provisions_NonLife <- tech_provisions
    assets$Technical_Provisions_Life <- 0  # Assuming non-life only
    assets$Best_Estimate <- tech_provisions * 0.85
    assets$Risk_Margin <- tech_provisions * 0.15
    assets$Deposits_From_Reinsurers <- runif(1, 5000000, 30000000)
    assets$Deferred_Tax_Liabilities <- runif(1, 0, 3000000)
    assets$Derivatives_Liabilities <- runif(1, 0, 5000000)
    assets$Debts_Owed_Credit_Institutions <- runif(1, 0, 20000000)
    assets$Insurance_Payables <- runif(1, 8000000, 50000000)
    assets$Reinsurance_Payables <- runif(1, 4000000, 25000000)
    assets$Payables_Trade <- runif(1, 2000000, 15000000)
    assets$Other_Liabilities <- runif(1, 3000000, 20000000)

    # Calculate total liabilities
    assets$Total_Liabilities <- (assets$Technical_Provisions_NonLife +
                                   assets$Technical_Provisions_Life +
                                   assets$Deposits_From_Reinsurers +
                                   assets$Deferred_Tax_Liabilities +
                                   assets$Derivatives_Liabilities +
                                   assets$Debts_Owed_Credit_Institutions +
                                   assets$Insurance_Payables +
                                   assets$Reinsurance_Payables +
                                   assets$Payables_Trade +
                                   assets$Other_Liabilities)

    # Excess of assets over liabilities (Own Funds)
    assets$Excess_Assets_Over_Liabilities <- assets$Total_Assets - assets$Total_Liabilities

    return(assets)
  })

  return(bind_rows(balance_sheet_list))
}


# Generate QSR 220 - Own Funds data
generate_own_funds_data <- function(num_syndicates = 10) {
  syndicates <- sample(LloydsDataGenerator$syndicates,
                       min(num_syndicates, length(LloydsDataGenerator$syndicates)))

  own_funds_list <- lapply(syndicates, function(syndicate) {
    own_funds <- data.frame(
      Syndicate = syndicate,
      Reporting_Date = LloydsDataGenerator$reporting_date,
      Members_Contributions_FIS = runif(1, 50000000, 200000000),
      Subordinated_Liabilities = runif(1, 0, 30000000),
      Reconciliation_Reserve = runif(1, 20000000, 100000000),
      Deductions_Own_Funds = runif(1, 0, 5000000),
      stringsAsFactors = FALSE
    )

    # Tier classification
    own_funds$Tier_1_Unrestricted <- own_funds$Members_Contributions_FIS + own_funds$Reconciliation_Reserve
    own_funds$Tier_1_Restricted <- 0
    own_funds$Tier_2 <- own_funds$Subordinated_Liabilities
    own_funds$Tier_3 <- 0

    own_funds$Total_Own_Funds <- (own_funds$Tier_1_Unrestricted +
                                     own_funds$Tier_1_Restricted +
                                     own_funds$Tier_2 +
                                     own_funds$Tier_3 -
                                     own_funds$Deductions_Own_Funds)

    # Eligible own funds to meet SCR and MCR
    own_funds$Eligible_Own_Funds_SCR <- own_funds$Total_Own_Funds
    own_funds$Eligible_Own_Funds_MCR <- own_funds$Tier_1_Unrestricted + pmin(own_funds$Tier_2, own_funds$Tier_1_Unrestricted * 0.2)

    return(own_funds)
  })

  return(bind_rows(own_funds_list))
}


# Generate QSR 240 - Technical Provisions data
generate_technical_provisions_data <- function(num_syndicates = 10) {
  syndicates <- sample(LloydsDataGenerator$syndicates,
                       min(num_syndicates, length(LloydsDataGenerator$syndicates)))

  tp_list <- lapply(syndicates, function(syndicate) {
    # Select 8 non-life LOBs
    selected_lobs <- sample(LloydsDataGenerator$lines_of_business[1:12], 8)

    lob_data <- lapply(selected_lobs, function(lob) {
      tp <- data.frame(
        Syndicate = syndicate,
        Reporting_Date = LloydsDataGenerator$reporting_date,
        Line_of_Business = lob,
        Technical_Provisions_Calculated_Whole = 0,
        Best_Estimate_Gross = runif(1, 10000000, 50000000),
        Best_Estimate_Recoverable = runif(1, 2000000, 15000000),
        Risk_Margin = runif(1, 1000000, 8000000),
        stringsAsFactors = FALSE
      )

      tp$Best_Estimate_Net <- tp$Best_Estimate_Gross - tp$Best_Estimate_Recoverable
      tp$Technical_Provisions_Gross <- tp$Best_Estimate_Gross + tp$Risk_Margin
      tp$Technical_Provisions_Recoverable <- tp$Best_Estimate_Recoverable
      tp$Technical_Provisions_Net <- tp$Technical_Provisions_Gross - tp$Technical_Provisions_Recoverable

      return(tp)
    })

    return(bind_rows(lob_data))
  })

  return(bind_rows(tp_list))
}


# Generate QSR 440/450 - Premiums, Claims and Expenses data
generate_premiums_claims_data <- function(num_syndicates = 10) {
  syndicates <- sample(LloydsDataGenerator$syndicates,
                       min(num_syndicates, length(LloydsDataGenerator$syndicates)))

  pc_list <- lapply(syndicates, function(syndicate) {
    selected_lobs <- sample(LloydsDataGenerator$lines_of_business[1:12], 8)

    lob_data <- lapply(selected_lobs, function(lob) {
      pc <- data.frame(
        Syndicate = syndicate,
        Reporting_Date = LloydsDataGenerator$reporting_date,
        Line_of_Business = lob,
        Premiums_Written_Gross = runif(1, 20000000, 100000000),
        Premiums_Written_Reinsurers_Share = runif(1, 5000000, 30000000),
        Premiums_Earned_Gross = runif(1, 18000000, 95000000),
        Premiums_Earned_Reinsurers_Share = runif(1, 4500000, 28500000),
        Claims_Incurred_Gross = runif(1, 12000000, 70000000),
        Claims_Incurred_Reinsurers_Share = runif(1, 3000000, 21000000),
        Changes_Other_Technical_Provisions_Gross = runif(1, -5000000, 5000000),
        Changes_Other_Technical_Provisions_Reinsurers = runif(1, -1500000, 1500000),
        Expenses_Incurred = runif(1, 5000000, 25000000),
        stringsAsFactors = FALSE
      )

      pc$Premiums_Written_Net <- pc$Premiums_Written_Gross - pc$Premiums_Written_Reinsurers_Share
      pc$Premiums_Earned_Net <- pc$Premiums_Earned_Gross - pc$Premiums_Earned_Reinsurers_Share
      pc$Claims_Incurred_Net <- pc$Claims_Incurred_Gross - pc$Claims_Incurred_Reinsurers_Share
      pc$Changes_Other_Technical_Provisions_Net <- (pc$Changes_Other_Technical_Provisions_Gross -
                                                     pc$Changes_Other_Technical_Provisions_Reinsurers)

      # Calculate ratios
      pc$Loss_Ratio <- ifelse(pc$Premiums_Earned_Net != 0,
                              (pc$Claims_Incurred_Net / pc$Premiums_Earned_Net * 100), 0)
      pc$Expense_Ratio <- ifelse(pc$Premiums_Earned_Net != 0,
                                 (pc$Expenses_Incurred / pc$Premiums_Earned_Net * 100), 0)
      pc$Combined_Ratio <- pc$Loss_Ratio + pc$Expense_Ratio

      return(pc)
    })

    return(bind_rows(lob_data))
  })

  return(bind_rows(pc_list))
}


# Generate investment portfolio data
generate_investments_data <- function(num_syndicates = 10) {
  syndicates <- sample(LloydsDataGenerator$syndicates,
                       min(num_syndicates, length(LloydsDataGenerator$syndicates)))

  inv_list <- lapply(syndicates, function(syndicate) {
    asset_data <- lapply(LloydsDataGenerator$asset_classes, function(asset_class) {
      data.frame(
        Syndicate = syndicate,
        Reporting_Date = LloydsDataGenerator$reporting_date,
        Asset_Class = asset_class,
        Solvency_II_Value = runif(1, 5000000, 80000000),
        Accrued_Interest = runif(1, 0, 500000),
        Country = sample(LloydsDataGenerator$countries, 1),
        stringsAsFactors = FALSE
      )
    })

    return(bind_rows(asset_data))
  })

  return(bind_rows(inv_list))
}


# Generate SCR (Solvency Capital Requirement) calculation data
generate_scr_calculation_data <- function(num_syndicates = 10) {
  syndicates <- sample(LloydsDataGenerator$syndicates,
                       min(num_syndicates, length(LloydsDataGenerator$syndicates)))

  scr_list <- lapply(syndicates, function(syndicate) {
    scr <- data.frame(
      Syndicate = syndicate,
      Reporting_Date = LloydsDataGenerator$reporting_date,
      Market_Risk = runif(1, 15000000, 60000000),
      Interest_Rate_Risk = runif(1, 3000000, 15000000),
      Equity_Risk = runif(1, 5000000, 25000000),
      Property_Risk = runif(1, 2000000, 10000000),
      Spread_Risk = runif(1, 4000000, 20000000),
      Currency_Risk = runif(1, 2000000, 12000000),
      Concentration_Risk = runif(1, 1000000, 5000000),
      Counterparty_Default_Risk = runif(1, 8000000, 35000000),
      Life_Underwriting_Risk = 0,  # Assuming non-life only
      Health_Underwriting_Risk = runif(1, 2000000, 10000000),
      Non_Life_Underwriting_Risk = runif(1, 25000000, 100000000),
      Premium_Reserve_Risk = runif(1, 15000000, 70000000),
      Lapse_Risk = runif(1, 0, 5000000),
      CAT_Risk = runif(1, 10000000, 40000000),
      Operational_Risk = runif(1, 5000000, 20000000),
      Loss_Absorbing_Capacity_DT = runif(1, -10000000, -2000000),
      stringsAsFactors = FALSE
    )

    # Calculate BSCR
    bscr_before_diversification <- (scr$Market_Risk +
                                      scr$Counterparty_Default_Risk +
                                      scr$Life_Underwriting_Risk +
                                      scr$Health_Underwriting_Risk +
                                      scr$Non_Life_Underwriting_Risk)

    # Apply diversification benefit (typically 10-30%)
    diversification_benefit <- bscr_before_diversification * runif(1, -0.30, -0.10)
    scr$Diversification <- diversification_benefit
    scr$BSCR <- bscr_before_diversification + diversification_benefit

    # Calculate final SCR
    scr$SCR <- scr$BSCR + scr$Operational_Risk + scr$Loss_Absorbing_Capacity_DT

    # Ensure SCR is positive
    scr$SCR <- pmax(scr$SCR, 0)

    return(scr)
  })

  return(bind_rows(scr_list))
}


# Generate QSR 510/511 - MCR (Minimum Capital Requirement) data
generate_mcr_calculation_data <- function(num_syndicates = 10) {
  syndicates <- sample(LloydsDataGenerator$syndicates,
                       min(num_syndicates, length(LloydsDataGenerator$syndicates)))

  mcr_list <- lapply(syndicates, function(syndicate) {
    # Get corresponding SCR
    scr_value <- runif(1, 60000000, 150000000)

    mcr <- data.frame(
      Syndicate = syndicate,
      Reporting_Date = LloydsDataGenerator$reporting_date,
      Linear_MCR = runif(1, 15000000, 50000000),
      SCR = scr_value,
      MCR_Cap = scr_value * 0.45,
      MCR_Floor = scr_value * 0.25,
      Absolute_Floor_MCR = 2200000,  # EUR 2.2m converted to GBP equivalent
      stringsAsFactors = FALSE
    )

    # MCR is the maximum of Linear MCR and Absolute Floor,
    # but capped between MCR Floor and MCR Cap
    mcr$Combined_MCR <- pmax(
      pmin(mcr$Linear_MCR, mcr$MCR_Cap),
      pmax(mcr$MCR_Floor, mcr$Absolute_Floor_MCR)
    )

    mcr$MCR <- mcr$Combined_MCR

    return(mcr)
  })

  return(bind_rows(mcr_list))
}


# Main function to generate all synthetic data
generate_all_data <- function(num_syndicates = 15) {
  cat("Generating synthetic Lloyd's data for", num_syndicates, "syndicates...\n\n")

  balance_sheet <- generate_balance_sheet_data(num_syndicates)
  cat("Generated balance_sheet:", nrow(balance_sheet), "rows\n")

  own_funds <- generate_own_funds_data(num_syndicates)
  cat("Generated own_funds:", nrow(own_funds), "rows\n")

  technical_provisions <- generate_technical_provisions_data(num_syndicates)
  cat("Generated technical_provisions:", nrow(technical_provisions), "rows\n")

  premiums_claims <- generate_premiums_claims_data(num_syndicates)
  cat("Generated premiums_claims:", nrow(premiums_claims), "rows\n")

  investments <- generate_investments_data(num_syndicates)
  cat("Generated investments:", nrow(investments), "rows\n")

  scr_calculation <- generate_scr_calculation_data(num_syndicates)
  cat("Generated scr_calculation:", nrow(scr_calculation), "rows\n")

  mcr_calculation <- generate_mcr_calculation_data(num_syndicates)
  cat("Generated mcr_calculation:", nrow(mcr_calculation), "rows\n")

  # Save to CSV files
  output_dir <- '../Data/'

  write.csv(balance_sheet, paste0(output_dir, 'synthetic_balance_sheet.csv'), row.names = FALSE)
  write.csv(own_funds, paste0(output_dir, 'synthetic_own_funds.csv'), row.names = FALSE)
  write.csv(technical_provisions, paste0(output_dir, 'synthetic_technical_provisions.csv'), row.names = FALSE)
  write.csv(premiums_claims, paste0(output_dir, 'synthetic_premiums_claims.csv'), row.names = FALSE)
  write.csv(investments, paste0(output_dir, 'synthetic_investments.csv'), row.names = FALSE)
  write.csv(scr_calculation, paste0(output_dir, 'synthetic_scr_calculation.csv'), row.names = FALSE)
  write.csv(mcr_calculation, paste0(output_dir, 'synthetic_mcr_calculation.csv'), row.names = FALSE)

  cat("\nSynthetic data generation complete!\n")
  cat("Files saved to:", output_dir, "\n")
}


# Run the main function
if (!interactive()) {
  generate_all_data(num_syndicates = 15)
}
