# QSR Report Generator for Power BI (R)
# Generates Solvency II Quarterly Solvency Return (QSR) reports
#
# This script can be imported and used within Power BI to transform
# Lloyd's syndicate data into standardized QSR return formats.

library(dplyr)
library(tidyr)


# QSRReportGenerator class-like structure
QSRReportGenerator <- function(data_dir = '../Data/') {
  # Initialize data storage
  data_store <- list()

  # Load all synthetic data files
  load_data <- function() {
    datasets <- c(
      'balance_sheet',
      'own_funds',
      'technical_provisions',
      'premiums_claims',
      'investments',
      'scr_calculation',
      'mcr_calculation'
    )

    for (dataset in datasets) {
      filepath <- paste0(data_dir, 'synthetic_', dataset, '.csv')

      tryCatch({
        data_store[[dataset]] <<- read.csv(filepath, stringsAsFactors = FALSE)
        cat('Loaded', dataset, ':', nrow(data_store[[dataset]]), 'rows\n')
      }, error = function(e) {
        cat('Warning:', dataset, 'file not found\n')
        data_store[[dataset]] <<- data.frame()
      })
    }
  }


  # Generate QSR 002 - Overall Balance Sheet (S.02.01.02)
  generate_qsr002_balance_sheet <- function() {
    if (is.null(data_store$balance_sheet) || nrow(data_store$balance_sheet) == 0) {
      return(data.frame())
    }

    df <- data_store$balance_sheet

    # Format according to QSR 002 specification
    qsr002 <- data.frame(
      Syndicate = df$Syndicate,
      Reporting_Date = df$Reporting_Date,

      # Assets
      R0010_Goodwill = df$Goodwill,
      R0020_Deferred_Acquisition_Costs = df$Deferred_Acquisition_Costs,
      R0030_Intangible_Assets = df$Intangible_Assets,
      R0040_Deferred_Tax_Assets = df$Deferred_Tax_Assets,
      R0050_Pension_Benefit_Surplus = df$Pension_Benefit_Surplus,
      R0060_Property_Plant_Equipment = df$Property_Plant_Equipment,
      R0070_Investments = df$Investments,
      R0080_Holdings_Related_Undertakings = df$Holdings_Related_Undertakings,
      R0090_Equities = df$Equities,
      R0100_Bonds = df$Bonds,
      R0110_Government_Bonds = df$Government_Bonds,
      R0120_Corporate_Bonds = df$Corporate_Bonds,
      R0130_Collective_Investments = df$Collective_Investments,
      R0140_Derivatives = df$Derivatives,
      R0150_Deposits_Other_Than_Cash = df$Deposits_Other_Than_Cash,
      R0160_Reinsurance_Recoverables = df$Reinsurance_Recoverables,
      R0170_Insurance_Receivables = df$Insurance_Receivables,
      R0180_Reinsurance_Receivables = df$Reinsurance_Receivables,
      R0190_Receivables_Trade = df$Receivables_Trade,
      R0200_Cash_and_Cash_Equivalents = df$Cash_and_Cash_Equivalents,
      R0210_Other_Assets = df$Other_Assets,
      R0220_Total_Assets = df$Total_Assets,

      # Liabilities
      R0230_Technical_Provisions_NonLife = df$Technical_Provisions_NonLife,
      R0240_Technical_Provisions_Life = df$Technical_Provisions_Life,
      R0250_Best_Estimate = df$Best_Estimate,
      R0260_Risk_Margin = df$Risk_Margin,
      R0270_Deposits_From_Reinsurers = df$Deposits_From_Reinsurers,
      R0280_Deferred_Tax_Liabilities = df$Deferred_Tax_Liabilities,
      R0290_Derivatives_Liabilities = df$Derivatives_Liabilities,
      R0300_Debts_Credit_Institutions = df$Debts_Owed_Credit_Institutions,
      R0310_Insurance_Payables = df$Insurance_Payables,
      R0320_Reinsurance_Payables = df$Reinsurance_Payables,
      R0330_Payables_Trade = df$Payables_Trade,
      R0340_Other_Liabilities = df$Other_Liabilities,
      R0350_Total_Liabilities = df$Total_Liabilities,
      R0360_Excess_Assets_Over_Liabilities = df$Excess_Assets_Over_Liabilities,

      stringsAsFactors = FALSE
    )

    return(qsr002)
  }


  # Generate QSR 220 - Own Funds (S.23.01.01)
  generate_qsr220_own_funds <- function() {
    if (is.null(data_store$own_funds) || nrow(data_store$own_funds) == 0) {
      return(data.frame())
    }

    df <- data_store$own_funds

    qsr220 <- data.frame(
      Syndicate = df$Syndicate,
      Reporting_Date = df$Reporting_Date,

      # Basic own funds
      R0040_Members_Contributions_FIS_Tier1_Unrestricted = df$Members_Contributions_FIS,
      R0050_Subordinated_Liabilities_Tier2 = df$Subordinated_Liabilities,
      R0060_Reconciliation_Reserve = df$Reconciliation_Reserve,
      R0070_Deductions = df$Deductions_Own_Funds,

      # Tier classification
      R0080_Tier_1_Unrestricted = df$Tier_1_Unrestricted,
      R0090_Tier_1_Restricted = df$Tier_1_Restricted,
      R0100_Tier_2 = df$Tier_2,
      R0110_Tier_3 = df$Tier_3,

      # Total and eligible own funds
      R0120_Total_Own_Funds = df$Total_Own_Funds,
      R0130_Eligible_Own_Funds_SCR = df$Eligible_Own_Funds_SCR,
      R0140_Eligible_Own_Funds_MCR = df$Eligible_Own_Funds_MCR,

      stringsAsFactors = FALSE
    )

    return(qsr220)
  }


  # Generate QSR 240 - Non-Life Technical Provisions (S.17.01.02)
  generate_qsr240_technical_provisions <- function() {
    if (is.null(data_store$technical_provisions) || nrow(data_store$technical_provisions) == 0) {
      return(data.frame())
    }

    df <- data_store$technical_provisions

    qsr240 <- data.frame(
      Syndicate = df$Syndicate,
      Reporting_Date = df$Reporting_Date,
      Line_of_Business = df$Line_of_Business,

      # Technical provisions components
      Technical_Provisions_Calculated_Whole = df$Technical_Provisions_Calculated_Whole,

      # Best Estimate
      Best_Estimate_Gross = df$Best_Estimate_Gross,
      Best_Estimate_Recoverable = df$Best_Estimate_Recoverable,
      Best_Estimate_Net = df$Best_Estimate_Net,

      # Risk Margin
      Risk_Margin = df$Risk_Margin,

      # Total Technical Provisions
      Technical_Provisions_Gross = df$Technical_Provisions_Gross,
      Technical_Provisions_Recoverable = df$Technical_Provisions_Recoverable,
      Technical_Provisions_Net = df$Technical_Provisions_Net,

      stringsAsFactors = FALSE
    )

    return(qsr240)
  }


  # Generate QSR 440 - Non-Life Insurance Claims Information (S.05.01.02.01)
  generate_qsr440_premiums_claims <- function() {
    if (is.null(data_store$premiums_claims) || nrow(data_store$premiums_claims) == 0) {
      return(data.frame())
    }

    df <- data_store$premiums_claims

    qsr440 <- data.frame(
      Syndicate = df$Syndicate,
      Reporting_Date = df$Reporting_Date,
      Line_of_Business = df$Line_of_Business,

      # Premiums
      Premiums_Written_Gross = df$Premiums_Written_Gross,
      Premiums_Written_Reinsurers_Share = df$Premiums_Written_Reinsurers_Share,
      Premiums_Written_Net = df$Premiums_Written_Net,
      Premiums_Earned_Gross = df$Premiums_Earned_Gross,
      Premiums_Earned_Reinsurers_Share = df$Premiums_Earned_Reinsurers_Share,
      Premiums_Earned_Net = df$Premiums_Earned_Net,

      # Claims
      Claims_Incurred_Gross = df$Claims_Incurred_Gross,
      Claims_Incurred_Reinsurers_Share = df$Claims_Incurred_Reinsurers_Share,
      Claims_Incurred_Net = df$Claims_Incurred_Net,

      # Changes in other technical provisions
      Changes_Other_TP_Gross = df$Changes_Other_Technical_Provisions_Gross,
      Changes_Other_TP_Reinsurers = df$Changes_Other_Technical_Provisions_Reinsurers,
      Changes_Other_TP_Net = df$Changes_Other_Technical_Provisions_Net,

      # Expenses
      Expenses_Incurred = df$Expenses_Incurred,

      # Ratios
      Loss_Ratio = df$Loss_Ratio,
      Expense_Ratio = df$Expense_Ratio,
      Combined_Ratio = df$Combined_Ratio,

      stringsAsFactors = FALSE
    )

    return(qsr440)
  }


  # Generate QSR 291 - Operational Risk (S.41.01.11)
  generate_qsr291_operational_risk <- function() {
    if (is.null(data_store$scr_calculation) || nrow(data_store$scr_calculation) == 0) {
      return(data.frame())
    }

    df <- data_store$scr_calculation

    qsr291 <- data.frame(
      Syndicate = df$Syndicate,
      Reporting_Date = df$Reporting_Date,
      Operational_Risk = df$Operational_Risk,
      stringsAsFactors = FALSE
    )

    return(qsr291)
  }


  # Generate QSR 292 - Market Risk (S.14.01.10.01)
  generate_qsr292_market_risk <- function() {
    if (is.null(data_store$scr_calculation) || nrow(data_store$scr_calculation) == 0) {
      return(data.frame())
    }

    df <- data_store$scr_calculation

    qsr292 <- data.frame(
      Syndicate = df$Syndicate,
      Reporting_Date = df$Reporting_Date,
      Market_Risk_Total = df$Market_Risk,
      Interest_Rate_Risk = df$Interest_Rate_Risk,
      Equity_Risk = df$Equity_Risk,
      Property_Risk = df$Property_Risk,
      Spread_Risk = df$Spread_Risk,
      Currency_Risk = df$Currency_Risk,
      Concentration_Risk = df$Concentration_Risk,
      stringsAsFactors = FALSE
    )

    return(qsr292)
  }


  # Generate QSR 293 - Counterparty Default Risk (S.38.01.10.01)
  generate_qsr293_counterparty_risk <- function() {
    if (is.null(data_store$scr_calculation) || nrow(data_store$scr_calculation) == 0) {
      return(data.frame())
    }

    df <- data_store$scr_calculation

    qsr293 <- data.frame(
      Syndicate = df$Syndicate,
      Reporting_Date = df$Reporting_Date,
      Counterparty_Default_Risk = df$Counterparty_Default_Risk,
      stringsAsFactors = FALSE
    )

    return(qsr293)
  }


  # Generate QSR 510 - Minimum Capital Requirement (S.28.01.01)
  generate_qsr510_mcr <- function() {
    if (is.null(data_store$mcr_calculation) || nrow(data_store$mcr_calculation) == 0) {
      return(data.frame())
    }

    df <- data_store$mcr_calculation

    qsr510 <- data.frame(
      Syndicate = df$Syndicate,
      Reporting_Date = df$Reporting_Date,
      Linear_MCR = df$Linear_MCR,
      SCR = df$SCR,
      MCR_Cap = df$MCR_Cap,
      MCR_Floor = df$MCR_Floor,
      Combined_MCR = df$Combined_MCR,
      Absolute_Floor_MCR = df$Absolute_Floor_MCR,
      MCR = df$MCR,
      stringsAsFactors = FALSE
    )

    return(qsr510)
  }


  # Generate SCR Summary with all risk modules
  generate_scr_summary <- function() {
    if (is.null(data_store$scr_calculation) || nrow(data_store$scr_calculation) == 0) {
      return(data.frame())
    }

    df <- data_store$scr_calculation

    scr_summary <- data.frame(
      Syndicate = df$Syndicate,
      Reporting_Date = df$Reporting_Date,

      # Risk modules
      Market_Risk = df$Market_Risk,
      Counterparty_Default_Risk = df$Counterparty_Default_Risk,
      Life_Underwriting_Risk = df$Life_Underwriting_Risk,
      Health_Underwriting_Risk = df$Health_Underwriting_Risk,
      Non_Life_Underwriting_Risk = df$Non_Life_Underwriting_Risk,
      Diversification = df$Diversification,
      BSCR = df$BSCR,
      Operational_Risk = df$Operational_Risk,
      Loss_Absorbing_Capacity_DT = df$Loss_Absorbing_Capacity_DT,
      SCR = df$SCR,

      stringsAsFactors = FALSE
    )

    return(scr_summary)
  }


  # Generate Solvency Ratio Report combining Own Funds and SCR/MCR
  generate_solvency_ratio_report <- function() {
    if (is.null(data_store$own_funds) || nrow(data_store$own_funds) == 0 ||
        is.null(data_store$scr_calculation) || nrow(data_store$scr_calculation) == 0 ||
        is.null(data_store$mcr_calculation) || nrow(data_store$mcr_calculation) == 0) {
      return(data.frame())
    }

    # Merge own funds with SCR and MCR
    solvency <- data_store$own_funds %>%
      left_join(data_store$scr_calculation %>% select(Syndicate, SCR), by = 'Syndicate') %>%
      left_join(data_store$mcr_calculation %>% select(Syndicate, MCR), by = 'Syndicate')

    # Calculate ratios
    solvency <- solvency %>%
      mutate(
        SCR_Ratio = round((Eligible_Own_Funds_SCR / SCR * 100), 2),
        MCR_Ratio = round((Eligible_Own_Funds_MCR / MCR * 100), 2),
        Surplus_SCR = Eligible_Own_Funds_SCR - SCR,
        Surplus_MCR = Eligible_Own_Funds_MCR - MCR
      ) %>%
      select(Syndicate, Reporting_Date, Total_Own_Funds,
             Eligible_Own_Funds_SCR, Eligible_Own_Funds_MCR,
             SCR, MCR, SCR_Ratio, MCR_Ratio,
             Surplus_SCR, Surplus_MCR)

    return(solvency)
  }


  # Generate all QSR reports
  generate_all_reports <- function() {
    load_data()

    reports <- list(
      QSR002_Balance_Sheet = generate_qsr002_balance_sheet(),
      QSR220_Own_Funds = generate_qsr220_own_funds(),
      QSR240_Technical_Provisions = generate_qsr240_technical_provisions(),
      QSR440_Premiums_Claims = generate_qsr440_premiums_claims(),
      QSR291_Operational_Risk = generate_qsr291_operational_risk(),
      QSR292_Market_Risk = generate_qsr292_market_risk(),
      QSR293_Counterparty_Risk = generate_qsr293_counterparty_risk(),
      QSR510_MCR = generate_qsr510_mcr(),
      SCR_Summary = generate_scr_summary(),
      Solvency_Ratio_Report = generate_solvency_ratio_report()
    )

    return(reports)
  }


  # Return list of functions
  list(
    load_data = load_data,
    generate_qsr002_balance_sheet = generate_qsr002_balance_sheet,
    generate_qsr220_own_funds = generate_qsr220_own_funds,
    generate_qsr240_technical_provisions = generate_qsr240_technical_provisions,
    generate_qsr440_premiums_claims = generate_qsr440_premiums_claims,
    generate_qsr291_operational_risk = generate_qsr291_operational_risk,
    generate_qsr292_market_risk = generate_qsr292_market_risk,
    generate_qsr293_counterparty_risk = generate_qsr293_counterparty_risk,
    generate_qsr510_mcr = generate_qsr510_mcr,
    generate_scr_summary = generate_scr_summary,
    generate_solvency_ratio_report = generate_solvency_ratio_report,
    generate_all_reports = generate_all_reports
  )
}


# Main function to generate QSR reports
main <- function() {
  generator <- QSRReportGenerator(data_dir = '../Data/')
  reports <- generator$generate_all_reports()

  # Save reports to CSV
  output_dir <- '../Data/'

  for (report_name in names(reports)) {
    df <- reports[[report_name]]
    if (nrow(df) > 0) {
      output_file <- paste0(output_dir, report_name, '.csv')
      write.csv(df, output_file, row.names = FALSE)
      cat('Generated', report_name, ':', nrow(df), 'rows,', ncol(df), 'columns\n')
    } else {
      cat('Warning:', report_name, 'is empty\n')
    }
  }

  cat('\nAll QSR reports generated successfully!\n')
}


# Power BI compatible functions
# These functions can be called directly from Power BI R scripts

get_balance_sheet <- function(data_dir = '../Data/') {
  generator <- QSRReportGenerator(data_dir = data_dir)
  generator$load_data()
  return(generator$generate_qsr002_balance_sheet())
}


get_own_funds <- function(data_dir = '../Data/') {
  generator <- QSRReportGenerator(data_dir = data_dir)
  generator$load_data()
  return(generator$generate_qsr220_own_funds())
}


get_technical_provisions <- function(data_dir = '../Data/') {
  generator <- QSRReportGenerator(data_dir = data_dir)
  generator$load_data()
  return(generator$generate_qsr240_technical_provisions())
}


get_premiums_claims <- function(data_dir = '../Data/') {
  generator <- QSRReportGenerator(data_dir = data_dir)
  generator$load_data()
  return(generator$generate_qsr440_premiums_claims())
}


get_solvency_ratios <- function(data_dir = '../Data/') {
  generator <- QSRReportGenerator(data_dir = data_dir)
  generator$load_data()
  return(generator$generate_solvency_ratio_report())
}


# Run main function if script is executed directly
if (!interactive()) {
  main()
}
