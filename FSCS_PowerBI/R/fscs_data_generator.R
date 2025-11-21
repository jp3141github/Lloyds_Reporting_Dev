# FSCS Data Generator for Lloyd's Syndicates
# ==========================================
#
# This module generates synthetic Lloyd's of London insurance data for
# Financial Services Compensation Scheme (FSCS) reporting purposes.
#
# The data generated includes:
# - Syndicate information
# - Gross written premiums (General and Life business)
# - Gross best estimate liabilities (General and Life business)
#
# Data is generated for 'protected contracts with eligible claimants' only.

library(dplyr)
library(tibble)
library(lubridate)


#' FSCS Data Generator Class
#'
#' @description
#' Generates synthetic Lloyd's syndicate data for FSCS reporting.
#'
#' @param num_syndicates Number of syndicates to generate data for
#' @param reporting_year Year for which the data is being reported
#' @param random_seed Seed for reproducibility
#'
#' @return A list containing generator functions
FSCSDataGenerator <- function(num_syndicates = 10,
                              reporting_year = 2024,
                              random_seed = 42) {

  # Set seed for reproducibility
  set.seed(random_seed)

  # Store parameters
  params <- list(
    num_syndicates = num_syndicates,
    reporting_year = reporting_year
  )


  #' Generate realistic Lloyd's syndicate numbers
  #'
  #' @return Vector of syndicate numbers
  generate_syndicate_numbers <- function() {
    # Lloyd's syndicate numbers typically range from 2000 to 6000
    sample(2000:6000, params$num_syndicates, replace = FALSE) %>% sort()
  }


  #' Generate gross written premium values
  #'
  #' @param business_type Character: 'general' or 'life' business
  #' @return Numeric vector of premium values
  generate_gross_written_premium <- function(business_type = 'general') {

    if (business_type == 'general') {
      # General business typically has higher premiums
      # Range: £10M to £500M
      min_value <- 10000000
      max_value <- 500000000
      mean_log <- log(150000000)
      sd_log <- 0.5
    } else {  # life business
      # Life business typically has lower volumes in Lloyd's
      # Range: £1M to £100M
      min_value <- 1000000
      max_value <- 100000000
      mean_log <- log(30000000)
      sd_log <- 0.5
    }

    # Generate log-normal distribution (typical for insurance premiums)
    values <- rlnorm(params$num_syndicates, meanlog = mean_log, sdlog = sd_log)

    # Clip to realistic ranges
    values <- pmin(pmax(values, min_value), max_value)

    # Add some zero values (some syndicates may not write certain business)
    zero_mask <- runif(params$num_syndicates) < 0.2
    values[zero_mask] <- 0

    round(values, 2)
  }


  #' Generate gross best estimate liabilities
  #'
  #' @param gwp_values Numeric vector of gross written premium values
  #' @param business_type Character: 'general' or 'life' business
  #' @return Numeric vector of liability values
  generate_best_estimate_liabilities <- function(gwp_values,
                                                 business_type = 'general') {

    if (business_type == 'general') {
      # General business BEL typically 1.5-3x of annual premium
      multiplier <- runif(params$num_syndicates, 1.5, 3.0)
    } else {  # life business
      # Life business BEL typically 3-8x of annual premium
      multiplier <- runif(params$num_syndicates, 3.0, 8.0)
    }

    # Calculate BEL as multiple of GWP with some randomness
    values <- gwp_values * multiplier

    # Add random variation (±20%)
    variation <- runif(params$num_syndicates, 0.8, 1.2)
    values <- values * variation

    # If GWP is zero, BEL should also be zero or very small
    zero_mask <- gwp_values == 0
    values[zero_mask] <- runif(sum(zero_mask), 0, 5000000)

    round(values, 2)
  }


  #' Generate complete FSCS dataset for all syndicates
  #'
  #' @return A tibble with all required fields
  generate_full_dataset <- function() {

    # Generate syndicate numbers
    syndicates <- generate_syndicate_numbers()

    # Generate gross written premiums
    gwp_general <- generate_gross_written_premium('general')
    gwp_life <- generate_gross_written_premium('life')

    # Generate best estimate liabilities
    bel_general <- generate_best_estimate_liabilities(gwp_general, 'general')
    bel_life <- generate_best_estimate_liabilities(gwp_life, 'life')

    # Create data frame
    df <- tibble(
      syndicate_number = syndicates,
      reporting_year = params$reporting_year,
      reporting_date = as.Date(paste0(params$reporting_year, "-12-31")),
      gwp_general_business = gwp_general,
      gwp_life_business = gwp_life,
      bel_general_business = bel_general,
      bel_life_business = bel_life,
      gwp_total = gwp_general + gwp_life,
      bel_total = bel_general + bel_life
    )

    # Add syndicate characteristics
    df <- df %>%
      mutate(
        managing_agent = paste0("Managing Agent ",
                               sprintf("%03d", sample(1:50, n(), replace = TRUE))),
        general_business_pct = if_else(
          gwp_total > 0,
          round((gwp_general_business / gwp_total * 100), 2),
          0
        )
      )

    df
  }


  #' Generate data in the exact format required by FSCS template
  #'
  #' @return A tibble formatted for FSCS submission
  generate_fscs_output_format <- function() {

    df <- generate_full_dataset()

    # Create output in FSCS format (one row per syndicate)
    output <- tibble(
      `Syndicate Number` = df$syndicate_number,
      `Reporting Year` = df$reporting_year,
      `Reporting Date` = df$reporting_date,
      `GWP General Business (£)` = df$gwp_general_business,
      `GWP Life Business (£)` = df$gwp_life_business,
      `BEL General Business (£)` = df$bel_general_business,
      `BEL Life Business (£)` = df$bel_life_business,
      Notes = 'Protected contracts with eligible claimants only'
    )

    output
  }


  #' Generate detailed transactional data
  #'
  #' @return A tibble with transaction-level data
  generate_detail_dataset <- function() {

    base_df <- generate_full_dataset()

    detail_records <- list()
    record_count <- 0

    for (i in 1:nrow(base_df)) {
      row <- base_df[i, ]
      syndicate <- row$syndicate_number

      # Generate 50-200 contracts per syndicate
      num_contracts <- sample(50:200, 1)

      for (j in 1:num_contracts) {
        record_count <- record_count + 1

        # Randomly assign business type
        is_general <- runif(1) > 0.3

        if (is_general) {
          business_type <- 'General'
          total_gwp <- row$gwp_general_business
          total_bel <- row$bel_general_business
          classes <- c('Property', 'Casualty', 'Marine', 'Aviation', 'Energy')
        } else {
          business_type <- 'Life'
          total_gwp <- row$gwp_life_business
          total_bel <- row$bel_life_business
          classes <- c('Term Life', 'Whole Life', 'Annuities', 'Critical Illness')
        }

        # Distribute total amounts across contracts
        if (total_gwp > 0) {
          contract_gwp <- (total_gwp / num_contracts) * runif(1, 0.5, 1.5)
          contract_bel <- (total_bel / num_contracts) * runif(1, 0.5, 1.5)
        } else {
          contract_gwp <- 0
          contract_bel <- 0
        }

        # Generate random dates
        inception_year <- params$reporting_year - sample(0:3, 1)
        inception_month <- sample(1:12, 1)
        inception_day <- sample(1:28, 1)

        expiry_year <- params$reporting_year + sample(1:5, 1)
        expiry_month <- sample(1:12, 1)
        expiry_day <- sample(1:28, 1)

        detail_records[[record_count]] <- list(
          syndicate_number = syndicate,
          contract_id = sprintf("CON-%d-%05d", syndicate, j),
          business_type = business_type,
          business_class = sample(classes, 1),
          inception_date = as.Date(paste(inception_year, inception_month,
                                        inception_day, sep = "-")),
          expiry_date = as.Date(paste(expiry_year, expiry_month,
                                     expiry_day, sep = "-")),
          gwp = round(contract_gwp, 2),
          bel = round(contract_bel, 2),
          currency = 'GBP',
          protected_contract = runif(1) > 0.1,  # 90% are protected
          eligible_claimant = runif(1) > 0.15,  # 85% are eligible
          territory = sample(c('UK', 'EEA', 'Worldwide'), 1)
        )
      }
    }

    # Convert list to tibble
    detail_df <- bind_rows(detail_records)

    # Filter to only protected contracts with eligible claimants
    detail_df <- detail_df %>%
      mutate(
        included_in_fscs = protected_contract & eligible_claimant
      )

    detail_df
  }


  # Return list of functions
  list(
    generate_syndicate_numbers = generate_syndicate_numbers,
    generate_gross_written_premium = generate_gross_written_premium,
    generate_best_estimate_liabilities = generate_best_estimate_liabilities,
    generate_full_dataset = generate_full_dataset,
    generate_fscs_output_format = generate_fscs_output_format,
    generate_detail_dataset = generate_detail_dataset
  )
}


#' Get FSCS summary data for Power BI
#'
#' Main function to be called from Power BI for summary data.
#'
#' @param num_syndicates Number of syndicates to generate
#' @param reporting_year Reporting year
#' @return A tibble with FSCS summary data
#' @export
get_fscs_summary_data <- function(num_syndicates = 10, reporting_year = 2024) {
  generator <- FSCSDataGenerator(num_syndicates, reporting_year)
  generator$generate_fscs_output_format()
}


#' Get FSCS detail data for Power BI
#'
#' Function to be called from Power BI for detailed transaction data.
#'
#' @param num_syndicates Number of syndicates to generate
#' @param reporting_year Reporting year
#' @return A tibble with detailed transaction data
#' @export
get_fscs_detail_data <- function(num_syndicates = 10, reporting_year = 2024) {
  generator <- FSCSDataGenerator(num_syndicates, reporting_year)
  generator$generate_detail_dataset()
}


# Testing code (only runs when script is executed directly)
if (!interactive()) {
  cat("="*80, "\n")
  cat("FSCS SUMMARY DATA\n")
  cat("="*80, "\n")

  generator <- FSCSDataGenerator(num_syndicates = 10, reporting_year = 2024)
  summary <- generator$generate_fscs_output_format()
  print(summary)

  cat("\n", "="*80, "\n")
  cat("DETAILED TRANSACTION DATA (First 20 records)\n")
  cat("="*80, "\n")

  detail <- generator$generate_detail_dataset()
  print(head(detail, 20))

  cat("\nTotal detail records generated:", nrow(detail), "\n")
  cat("Records included in FSCS:", sum(detail$included_in_fscs), "\n")
}
