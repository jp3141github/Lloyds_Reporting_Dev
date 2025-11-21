# Power BI R Query Script
# ========================
#
# This script is designed to be used directly in Power BI's R script data source.
#
# Instructions for Power BI:
# 1. Open Power BI Desktop
# 2. Get Data > More > Other > R script
# 3. Copy and paste this entire script
# 4. Click OK
#
# The script will generate synthetic Lloyd's FSCS data and return a dataset
# that can be used for reporting and visualization.

# Load required libraries
suppressPackageStartupMessages({
  library(dplyr)
  library(tibble)
  library(lubridate)
})


#' Generate FSCS data for Power BI consumption
#'
#' @param num_syndicates Number of syndicates to generate
#' @param reporting_year Reporting year
#' @return A tibble with FSCS data
generate_fscs_data <- function(num_syndicates = 15, reporting_year = 2024) {

  # Set seed for reproducibility
  set.seed(42)

  # Generate syndicate numbers
  syndicates <- sample(2000:6000, num_syndicates, replace = FALSE) %>% sort()

  # Initialize data list
  data_list <- list()

  for (i in 1:num_syndicates) {
    syndicate <- syndicates[i]

    # Generate GWP for general business (£10M to £500M)
    gwp_general <- rlnorm(1, meanlog = log(150000000), sdlog = 0.5)
    gwp_general <- pmin(pmax(gwp_general, 10000000), 500000000)
    if (runif(1) < 0.2) gwp_general <- 0

    # Generate GWP for life business (£1M to £100M)
    gwp_life <- rlnorm(1, meanlog = log(30000000), sdlog = 0.5)
    gwp_life <- pmin(pmax(gwp_life, 1000000), 100000000)
    if (runif(1) < 0.2) gwp_life <- 0

    # Generate BEL for general business (1.5-3x GWP)
    bel_general <- gwp_general * runif(1, 1.5, 3.0) * runif(1, 0.8, 1.2)
    if (gwp_general == 0) bel_general <- runif(1, 0, 5000000)

    # Generate BEL for life business (3-8x GWP)
    bel_life <- gwp_life * runif(1, 3.0, 8.0) * runif(1, 0.8, 1.2)
    if (gwp_life == 0) bel_life <- runif(1, 0, 5000000)

    # Calculate totals
    gwp_total <- gwp_general + gwp_life
    bel_total <- bel_general + bel_life

    data_list[[i]] <- list(
      Syndicate_Number = syndicate,
      Reporting_Year = reporting_year,
      Reporting_Date = as.Date(paste0(reporting_year, "-12-31")),
      Managing_Agent = paste0("MA_", sample(100:999, 1)),
      GWP_General_Business_GBP = round(gwp_general, 2),
      GWP_Life_Business_GBP = round(gwp_life, 2),
      GWP_Total_GBP = round(gwp_total, 2),
      BEL_General_Business_GBP = round(bel_general, 2),
      BEL_Life_Business_GBP = round(bel_life, 2),
      BEL_Total_GBP = round(bel_total, 2),
      General_Business_Percentage = if (gwp_total > 0) {
        round((gwp_general / gwp_total * 100), 2)
      } else {
        0
      },
      Data_Quality_Flag = 'Synthetic',
      Notes = 'Protected contracts with eligible claimants only'
    )
  }

  # Convert list to tibble
  bind_rows(data_list)
}


# ============================================================================
# MAIN EXECUTION BLOCK FOR POWER BI
# ============================================================================
# Power BI expects a data frame to be assigned to 'dataset' variable

# Generate the data
dataset <- generate_fscs_data(num_syndicates = 15, reporting_year = 2024)

# Print message (will appear in Power BI's script output window)
cat(sprintf("Generated %d syndicate records for FSCS reporting\n", nrow(dataset)))

# Power BI will automatically detect and use the 'dataset' data frame
# You can reference this in subsequent transformations
