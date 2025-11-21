# Power BI Script for Solvency II ASB Returns (R Version)
# This script can be used directly in Power BI as an R data source.
#
# Instructions for Power BI:
# 1. Open Power BI Desktop
# 2. Get Data > More > Other > R script
# 3. Copy and paste this script
# 4. Adjust parameters as needed
# 5. Select the tables you want to load

# Required libraries
if (!require("tidyverse")) install.packages("tidyverse", quiet = TRUE)
library(tidyverse)

# ============================================================================
# CONFIGURATION - Adjust these parameters as needed
# ============================================================================

SYNDICATE_NUMBER <- "1234"
SYNDICATE_NAME <- "Example Marine & Energy Syndicate"
START_YEAR <- 2015
END_YEAR <- 2024
RANDOM_SEED <- 42

# Number of records to generate
CLAIMS_RECORDS <- 500
INFLATION_RECORDS <- 200

# ============================================================================
# DATA GENERATOR FUNCTIONS (Embedded for Power BI)
# ============================================================================

# Lines of Business
LINES_OF_BUSINESS <- c(
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
)

CURRENCIES <- c("GBP", "USD", "EUR")

# Generate ASB 245/246/247 Claims Data
generate_claims_data <- function(num_records, start_year, end_year, random_seed) {

  set.seed(random_seed)
  data_list <- list()

  for (i in 1:num_records) {
    currency <- sample(CURRENCIES, 1)
    lob_code <- sample(names(LINES_OF_BUSINESS), 1)
    underwriting_year <- sample(start_year:end_year, 1)
    development_year <- sample(0:10, 1)

    base_claim <- exp(rnorm(1, mean = 10, sd = 2))
    development_factor <- max(1 - (development_year * 0.08), 0.3)

    gross_claim_paid <- base_claim * development_factor * runif(1, 0.8, 1.2)
    reinsurance_recoveries <- gross_claim_paid * runif(1, 0.1, 0.4)

    gross_be_provisions <- gross_claim_paid * runif(1, 1.1, 1.5)
    discounting_gross <- gross_be_provisions * runif(1, 0.02, 0.05)

    be_provisions_reins <- reinsurance_recoveries * runif(1, 1.1, 1.5)
    discounting_reins <- be_provisions_reins * runif(1, 0.02, 0.05)

    gross_rbns <- gross_claim_paid * runif(1, 0.6, 0.9)
    reinsurance_rbns <- reinsurance_recoveries * runif(1, 0.6, 0.9)

    discounting_rbns <- gross_rbns * runif(1, 0.015, 0.04)
    discounting_reins_rbns <- reinsurance_rbns * runif(1, 0.015, 0.04)

    record <- tibble(
      Currency = currency,
      LineOfBusiness = lob_code,
      LineOfBusinessName = LINES_OF_BUSINESS[lob_code],
      UnderwritingYear = underwriting_year,
      DevelopmentYear = development_year,
      GrossClaimPaid = round(gross_claim_paid, 2),
      ReinsuranceRecoveries = round(reinsurance_recoveries, 2),
      NetClaimPaid = round(gross_claim_paid - reinsurance_recoveries, 2),
      GrossUndiscountedBEClaimsProvisions = round(gross_be_provisions, 2),
      DiscountingGrossBEClaimsProvisions = round(discounting_gross, 2),
      UndiscountedBEClaimsProvisionsReinsRecoverable = round(be_provisions_reins, 2),
      DiscountingBEClaimsProvisionsReinsRecoverable = round(discounting_reins, 2),
      GrossRBNS = round(gross_rbns, 2),
      ReinsuranceRBNS = round(reinsurance_rbns, 2),
      NetRBNS = round(gross_rbns - reinsurance_rbns, 2),
      DiscountingRBNS = round(discounting_rbns, 2),
      DiscountingReinsuranceRBNS = round(discounting_reins_rbns, 2)
    )

    data_list[[i]] <- record
  }

  df <- bind_rows(data_list)
  df <- df %>% arrange(UnderwritingYear, LineOfBusiness, DevelopmentYear)
  return(df)
}

# Generate ASB 248 Inflation Data
generate_inflation_data <- function(num_records, start_year, end_year, random_seed) {

  set.seed(random_seed + 1)  # Different seed for variety
  data_list <- list()

  for (i in 1:num_records) {
    currency <- sample(CURRENCIES, 1)
    lob_code <- sample(names(LINES_OF_BUSINESS), 1)
    underwriting_year <- sample(start_year:end_year, 1)

    historic_total <- runif(1, 1.5, 4.5)
    historic_external <- historic_total * runif(1, 0.5, 0.7)
    historic_endogenous <- historic_total - historic_external

    expected_total <- historic_total * runif(1, 0.9, 1.1)
    expected_external <- expected_total * runif(1, 0.5, 0.7)
    expected_endogenous <- expected_total - expected_external

    record <- tibble(
      Currency = currency,
      LineOfBusiness = lob_code,
      LineOfBusinessName = LINES_OF_BUSINESS[lob_code],
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

  df <- bind_rows(data_list)
  df <- df %>% arrange(UnderwritingYear, LineOfBusiness)
  return(df)
}

# ============================================================================
# DATA GENERATION - This section runs when script is executed
# ============================================================================

# Generate the data tables for Power BI
# These will appear as available tables in Power BI

# ASB 245/246/247: Non-Life Insurance Claims Information
ASB_245_246_247_Claims <- generate_claims_data(
  CLAIMS_RECORDS,
  START_YEAR,
  END_YEAR,
  RANDOM_SEED
)

# ASB 248: Inflation Rates
ASB_248_InflationRates <- generate_inflation_data(
  INFLATION_RECORDS,
  START_YEAR,
  END_YEAR,
  RANDOM_SEED
)

# Metadata table for reference
Metadata <- tibble(
  SyndicateNumber = SYNDICATE_NUMBER,
  SyndicateName = SYNDICATE_NAME,
  StartYear = START_YEAR,
  EndYear = END_YEAR,
  GenerationDate = format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
  ClaimsRecords = nrow(ASB_245_246_247_Claims),
  InflationRecords = nrow(ASB_248_InflationRates)
)

# Lines of Business reference table
LinesOfBusiness <- tibble(
  LineOfBusiness = names(LINES_OF_BUSINESS),
  LineOfBusinessName = unname(LINES_OF_BUSINESS)
)

# Summary statistics for Power BI dashboards
Claims_Summary <- ASB_245_246_247_Claims %>%
  group_by(UnderwritingYear, LineOfBusiness, Currency) %>%
  summarise(
    TotalGrossClaimPaid = sum(GrossClaimPaid, na.rm = TRUE),
    TotalReinsuranceRecoveries = sum(ReinsuranceRecoveries, na.rm = TRUE),
    TotalNetClaimPaid = sum(NetClaimPaid, na.rm = TRUE),
    TotalGrossRBNS = sum(GrossRBNS, na.rm = TRUE),
    TotalNetRBNS = sum(NetRBNS, na.rm = TRUE),
    .groups = "drop"
  )

# Development year analysis
Development_Analysis <- ASB_245_246_247_Claims %>%
  group_by(DevelopmentYear, LineOfBusiness) %>%
  summarise(
    AvgGrossClaimPaid = mean(GrossClaimPaid, na.rm = TRUE),
    TotalGrossClaimPaid = sum(GrossClaimPaid, na.rm = TRUE),
    ClaimCount = n(),
    AvgReinsuranceRecoveries = mean(ReinsuranceRecoveries, na.rm = TRUE),
    TotalReinsuranceRecoveries = sum(ReinsuranceRecoveries, na.rm = TRUE),
    .groups = "drop"
  )

# ============================================================================
# OUTPUT - Available tables for Power BI
# ============================================================================
# The following dataframes will be available in Power BI:
# 1. ASB_245_246_247_Claims - Main claims data
# 2. ASB_248_InflationRates - Inflation rates data
# 3. Metadata - Generation metadata
# 4. LinesOfBusiness - Reference table
# 5. Claims_Summary - Aggregated summary
# 6. Development_Analysis - Development year analysis

cat("Data generation complete!\n")
cat(sprintf("ASB 245/246/247 Claims: %d records\n", nrow(ASB_245_246_247_Claims)))
cat(sprintf("ASB 248 Inflation Rates: %d records\n", nrow(ASB_248_InflationRates)))
