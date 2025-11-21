# Synthetic Data Generator for Lloyd's of London Solvency II ASB Returns
# This script generates realistic synthetic insurance data for testing and demonstration purposes.

# Required libraries
if (!require("tidyverse")) install.packages("tidyverse", quiet = TRUE)
library(tidyverse)

# LloydsDataGenerator Class (using R6 or list-based approach)
LloydsDataGenerator <- list(

  # Lines of Business (EIOPA classifications)
  LINES_OF_BUSINESS = c(
    "LOB01" = "Medical expense insurance",
    "LOB02" = "Income protection insurance",
    "LOB03" = "Workers compensation insurance",
    "LOB04" = "Motor vehicle liability insurance",
    "LOB05" = "Other motor insurance",
    "LOB06" = "Marine, aviation and transport insurance",
    "LOB07" = "Fire and other damage to property insurance",
    "LOB08" = "General liability insurance",
    "LOB09" = "Credit and suretyship insurance",
    "LOB10" = "Legal expenses insurance",
    "LOB11" = "Assistance",
    "LOB12" = "Miscellaneous financial loss"
  ),

  CURRENCIES = c("GBP", "USD", "EUR")
)

# Generate ASB 245/246/247 Claims Data
generate_asb_245_246_247_data <- function(
    num_records = 500,
    syndicate_number = "1234",
    syndicate_name = "Example Syndicate",
    start_year = 2015,
    end_year = 2024,
    random_seed = 42
) {

  set.seed(random_seed)

  # Initialize data list
  data_list <- list()

  for (i in 1:num_records) {

    # Random selections
    currency <- sample(LloydsDataGenerator$CURRENCIES, 1)
    lob_code <- sample(names(LloydsDataGenerator$LINES_OF_BUSINESS), 1)
    underwriting_year <- sample(start_year:end_year, 1)
    development_year <- sample(0:10, 1)

    # Generate realistic claim amounts (in thousands)
    base_claim <- exp(rnorm(1, mean = 10, sd = 2))

    # Development pattern - claims develop over time
    development_factor <- max(1 - (development_year * 0.08), 0.3)

    gross_claim_paid <- base_claim * development_factor * runif(1, 0.8, 1.2)
    reinsurance_recoveries <- gross_claim_paid * runif(1, 0.1, 0.4)

    # Best estimate claims provisions
    gross_be_provisions <- gross_claim_paid * runif(1, 1.1, 1.5)
    discounting_gross <- gross_be_provisions * runif(1, 0.02, 0.05)

    be_provisions_reins <- reinsurance_recoveries * runif(1, 1.1, 1.5)
    discounting_reins <- be_provisions_reins * runif(1, 0.02, 0.05)

    # RBNS (Reported But Not Settled)
    gross_rbns <- gross_claim_paid * runif(1, 0.6, 0.9)
    reinsurance_rbns <- reinsurance_recoveries * runif(1, 0.6, 0.9)

    discounting_rbns <- gross_rbns * runif(1, 0.015, 0.04)
    discounting_reins_rbns <- reinsurance_rbns * runif(1, 0.015, 0.04)

    # Create record
    record <- tibble(
      Currency = currency,
      LineOfBusiness = lob_code,
      UnderwritingYear = underwriting_year,
      DevelopmentYear = development_year,
      GrossClaimPaid = round(gross_claim_paid, 2),
      ReinsuranceRecoveries = round(reinsurance_recoveries, 2),
      GrossUndiscountedBEClaimsProvisions = round(gross_be_provisions, 2),
      DiscountingGrossBEClaimsProvisions = round(discounting_gross, 2),
      UndiscountedBEClaimsProvisionsReinsRecoverable = round(be_provisions_reins, 2),
      DiscountingBEClaimsProvisionsReinsRecoverable = round(discounting_reins, 2),
      GrossRBNS = round(gross_rbns, 2),
      ReinsuranceRBNS = round(reinsurance_rbns, 2),
      DiscountingRBNS = round(discounting_rbns, 2),
      DiscountingReinsuranceRBNS = round(discounting_reins_rbns, 2)
    )

    data_list[[i]] <- record
  }

  # Combine all records
  df <- bind_rows(data_list)

  # Sort by underwriting year, development year, and line of business
  df <- df %>%
    arrange(UnderwritingYear, LineOfBusiness, DevelopmentYear)

  return(df)
}

# Generate ASB 248 Inflation Rates Data
generate_asb_248_data <- function(
    num_records = 200,
    syndicate_number = "1234",
    syndicate_name = "Example Syndicate",
    start_year = 2015,
    end_year = 2024,
    random_seed = 42
) {

  set.seed(random_seed)

  # Initialize data list
  data_list <- list()

  for (i in 1:num_records) {

    # Random selections
    currency <- sample(LloydsDataGenerator$CURRENCIES, 1)
    lob_code <- sample(names(LloydsDataGenerator$LINES_OF_BUSINESS), 1)
    underwriting_year <- sample(start_year:end_year, 1)

    # Generate realistic inflation rates (as percentages)
    historic_total <- runif(1, 1.5, 4.5)
    historic_external <- historic_total * runif(1, 0.5, 0.7)
    historic_endogenous <- historic_total - historic_external

    # Expected inflation rates
    expected_total <- historic_total * runif(1, 0.9, 1.1)
    expected_external <- expected_total * runif(1, 0.5, 0.7)
    expected_endogenous <- expected_total - expected_external

    # Create record
    record <- tibble(
      Currency = currency,
      LineOfBusiness = lob_code,
      UnderwritingYear = underwriting_year,
      HistoricInflationRateTotal = round(historic_total, 2),
      HistoricInflationRateExternal = round(historic_external, 2),
      HistoricInflationRateEndogenous = round(historic_endogenous, 2),
      ExpectedInflationRateTotal = round(expected_total, 2),
      ExpectedInflationRateExternal = round(expected_external, 2),
      ExpectedInflationRateEndogenous = round(expected_endogenous, 2)
    )

    data_list[[i]] <- record
  }

  # Combine all records
  df <- bind_rows(data_list)

  # Sort by underwriting year and line of business
  df <- df %>%
    arrange(UnderwritingYear, LineOfBusiness)

  return(df)
}

# Generate all ASB return data
generate_all_asb_data <- function(
    syndicate_number = "1234",
    syndicate_name = "Example Syndicate",
    start_year = 2015,
    end_year = 2024,
    claims_records = 500,
    inflation_records = 200,
    random_seed = 42
) {

  # Generate claims data
  asb_245_246_247 <- generate_asb_245_246_247_data(
    num_records = claims_records,
    syndicate_number = syndicate_number,
    syndicate_name = syndicate_name,
    start_year = start_year,
    end_year = end_year,
    random_seed = random_seed
  )

  # Generate inflation data
  asb_248 <- generate_asb_248_data(
    num_records = inflation_records,
    syndicate_number = syndicate_number,
    syndicate_name = syndicate_name,
    start_year = start_year,
    end_year = end_year,
    random_seed = random_seed
  )

  # Create metadata
  metadata <- tibble(
    SyndicateNumber = syndicate_number,
    SyndicateName = syndicate_name,
    StartYear = start_year,
    EndYear = end_year,
    GenerationDate = format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
    ClaimsRecords = nrow(asb_245_246_247),
    InflationRecords = nrow(asb_248)
  )

  # Return list of dataframes
  return(list(
    ASB_245_246_247 = asb_245_246_247,
    ASB_248 = asb_248,
    Metadata = metadata
  ))
}

# Main execution (when script is run directly)
if (!interactive()) {

  cat("=" %R% strrep("=", 79), "\n")
  cat("SYNTHETIC DATA GENERATION FOR SOLVENCY II ASB RETURNS\n")
  cat(strrep("=", 80), "\n\n")

  # Generate all data
  all_data <- generate_all_asb_data(
    syndicate_number = "1234",
    syndicate_name = "Example Marine & Energy Syndicate",
    start_year = 2015,
    end_year = 2024,
    claims_records = 500,
    inflation_records = 200
  )

  cat("Syndicate:", all_data$Metadata$SyndicateNumber, "-",
      all_data$Metadata$SyndicateName, "\n")
  cat("Generation Date:", all_data$Metadata$GenerationDate, "\n\n")

  cat("ASB 245/246/247 Claims Data:\n")
  print(head(all_data$ASB_245_246_247, 10))
  cat("Total records:", nrow(all_data$ASB_245_246_247), "\n\n")

  cat(strrep("=", 80), "\n")
  cat("ASB 248 Inflation Rates Data:\n")
  print(head(all_data$ASB_248, 10))
  cat("Total records:", nrow(all_data$ASB_248), "\n\n")

  # Save to CSV files
  write_csv(all_data$ASB_245_246_247, "ASB_245_246_247_synthetic_data.csv")
  write_csv(all_data$ASB_248, "ASB_248_synthetic_data.csv")

  cat(strrep("=", 80), "\n")
  cat("Data saved to CSV files:\n")
  cat("  - ASB_245_246_247_synthetic_data.csv\n")
  cat("  - ASB_248_synthetic_data.csv\n")
  cat(strrep("=", 80), "\n")
}
