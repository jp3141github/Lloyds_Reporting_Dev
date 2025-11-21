###############################################################################
# SAO Addendum Return - 100 Movements and Actual vs Expected Analysis
###############################################################################
# This script generates synthetic Lloyd's of London data for the 100 Movements
# and AvE analysis table. Compatible with Power BI as an R data source.
#
# Usage in Power BI:
# 1. Get Data > More > R script
# 2. Copy and paste this script
# 3. Select the 'movements_ave' or 'movements_ave_summary' table
#
# Author: Claude
# Date: 2025-11-21
###############################################################################

# Set random seed for reproducibility
set.seed(123)

# Function to generate Movements and AvE Analysis data
generate_movements_ave_data <- function(num_classes = 10) {
  #' Generate synthetic Movements and Actual vs Expected Analysis data.
  #'
  #' Creates data for the top 10 largest classes by total net reserves,
  #' with analysis by underwriting year.
  #'
  #' @param num_classes Number of reserving classes (default 10)
  #' @return Data frame with synthetic Movements and AvE analysis data

  # Define reserving classes (top 10 by reserves)
  reserving_classes <- c(
    'Property Treaty', 'Casualty XL', 'Marine Hull', 'Aviation',
    'Energy Offshore', 'Professional Indemnity', 'D&O US',
    'Cyber', 'Motor', 'Property Direct'
  )[1:num_classes]

  # Define Lloyd's Lines of Business
  lloyds_lobs <- c(
    'Property Treaty', 'Casualty Treaty', 'Marine Hull', 'Aviation',
    'Energy Offshore', 'Professional Indemnity', 'D&O',
    'Cyber', 'Motor', 'Property Direct'
  )[1:num_classes]

  # Underwriting years to analyze
  underwriting_years <- c(2023, 2024, 2025)
  year_labels <- c('2023 & Prior', '2024', '2025')

  # Initialize data frame
  num_records <- num_classes * length(underwriting_years)
  data <- data.frame(
    `Class ID` = character(num_records),
    `Reserving Class` = character(num_records),
    `Lloyd's Line of Business` = character(num_records),
    `Underwriting Year` = character(num_records),
    `Reporting Year?` = integer(num_records),
    `Ultimate Premium (£000s)` = integer(num_records),
    `Actual vs Expected as % of ultimate premium` = numeric(num_records),
    `Initial Expected Loss Ratio (IELR) (%)` = numeric(num_records),
    `Ultimate Loss Ratio (ULR) (%)` = numeric(num_records),
    `Reserves 2024YE (£000s)` = integer(num_records),
    `Reserves 2025YE (£000s)` = integer(num_records),
    `Syndicate Estimate - 2025YE (£000s)` = integer(num_records),
    stringsAsFactors = FALSE,
    check.names = FALSE
  )

  # Generate records
  row_idx <- 1
  for (class_idx in 1:num_classes) {
    res_class <- reserving_classes[class_idx]
    lob <- lloyds_lobs[class_idx]

    for (year_idx in 1:length(underwriting_years)) {
      uw_year <- underwriting_years[year_idx]
      uw_label <- year_labels[year_idx]

      # Reporting year indicator
      is_reporting_year <- ifelse(uw_year == 2025, 1, 0)

      # Ultimate Premium (£000s) - varies by year
      if (uw_year == 2023) {
        base_premium <- runif(1, 5000, 15000)
      } else if (uw_year == 2024) {
        base_premium <- runif(1, 15000, 30000)
      } else {  # 2025
        base_premium <- runif(1, 20000, 50000)
      }
      ultimate_premium <- round(base_premium * (1 + rnorm(1, 0, 0.1)), 0)

      # Initial Expected Loss Ratio (IELR)
      ielr <- round(runif(1, 50, 75), 1)

      # Ultimate Loss Ratio (ULR)
      ulr <- round(ielr + rnorm(1, 0, 5), 1)

      # Actual vs Expected as % of ultimate premium
      if (uw_year == 2023) {
        ave_pct <- round(rnorm(1, 2, 5), 1)
      } else if (uw_year == 2024) {
        ave_pct <- round(rnorm(1, 0, 3), 1)
      } else {  # 2025
        ave_pct <- round(rnorm(1, -1, 2), 1)
      }

      # Reserves at 2024 YE
      reserves_2024ye <- round(ultimate_premium * ulr / 100 * runif(1, 0.3, 0.8), 0)

      # Reserves at 2025 YE
      reserves_2025ye <- round(ultimate_premium * ulr / 100 * runif(1, 0.2, 0.7), 0)

      # Syndicate estimate at 2025 YE
      syndicate_estimate_2025ye <- round(reserves_2025ye * (1 + rnorm(1, 0, 0.05)), 0)

      # Populate data frame
      data[row_idx, 'Class ID'] <- sprintf('%02d', class_idx)
      data[row_idx, 'Reserving Class'] <- res_class
      data[row_idx, "Lloyd's Line of Business"] <- lob
      data[row_idx, 'Underwriting Year'] <- uw_label
      data[row_idx, 'Reporting Year?'] <- is_reporting_year
      data[row_idx, 'Ultimate Premium (£000s)'] <- ultimate_premium
      data[row_idx, 'Actual vs Expected as % of ultimate premium'] <- ave_pct
      data[row_idx, 'Initial Expected Loss Ratio (IELR) (%)'] <- ielr
      data[row_idx, 'Ultimate Loss Ratio (ULR) (%)'] <- ulr
      data[row_idx, 'Reserves 2024YE (£000s)'] <- reserves_2024ye
      data[row_idx, 'Reserves 2025YE (£000s)'] <- reserves_2025ye
      data[row_idx, 'Syndicate Estimate - 2025YE (£000s)'] <- syndicate_estimate_2025ye

      row_idx <- row_idx + 1
    }
  }

  # Sort by Class ID and Underwriting Year
  data <- data[order(data$`Class ID`, match(data$`Underwriting Year`, year_labels)), ]
  rownames(data) <- NULL

  return(data)
}

# Function to generate summary data
generate_summary_data <- function(movements_ave_df) {
  #' Generate summary data for all classes combined.
  #'
  #' @param movements_ave_df Main movements and AvE analysis data frame
  #' @return Data frame with summary statistics

  year_labels <- c('2023 & Prior', '2024', '2025')
  summary_data <- data.frame(
    Metric = character(),
    `Ultimate Premium (£000s)` = integer(),
    `Reserves 2024YE (£000s)` = integer(),
    `Reserves 2025YE (£000s)` = integer(),
    `Syndicate Estimate - 2025YE (£000s)` = integer(),
    `Avg ULR (%)` = numeric(),
    `Avg AvE (%)` = numeric(),
    stringsAsFactors = FALSE,
    check.names = FALSE
  )

  for (uw_year in year_labels) {
    year_data <- movements_ave_df[movements_ave_df$`Underwriting Year` == uw_year, ]

    summary_row <- data.frame(
      Metric = paste('Total -', uw_year),
      `Ultimate Premium (£000s)` = sum(year_data$`Ultimate Premium (£000s)`),
      `Reserves 2024YE (£000s)` = sum(year_data$`Reserves 2024YE (£000s)`),
      `Reserves 2025YE (£000s)` = sum(year_data$`Reserves 2025YE (£000s)`),
      `Syndicate Estimate - 2025YE (£000s)` = sum(year_data$`Syndicate Estimate - 2025YE (£000s)`),
      `Avg ULR (%)` = round(mean(year_data$`Ultimate Loss Ratio (ULR) (%)`), 1),
      `Avg AvE (%)` = round(mean(year_data$`Actual vs Expected as % of ultimate premium`), 1),
      stringsAsFactors = FALSE,
      check.names = FALSE
    )

    summary_data <- rbind(summary_data, summary_row)
  }

  # Grand total
  grand_total <- data.frame(
    Metric = 'Grand Total',
    `Ultimate Premium (£000s)` = sum(movements_ave_df$`Ultimate Premium (£000s)`),
    `Reserves 2024YE (£000s)` = sum(movements_ave_df$`Reserves 2024YE (£000s)`),
    `Reserves 2025YE (£000s)` = sum(movements_ave_df$`Reserves 2025YE (£000s)`),
    `Syndicate Estimate - 2025YE (£000s)` = sum(movements_ave_df$`Syndicate Estimate - 2025YE (£000s)`),
    `Avg ULR (%)` = round(mean(movements_ave_df$`Ultimate Loss Ratio (ULR) (%)`), 1),
    `Avg AvE (%)` = round(mean(movements_ave_df$`Actual vs Expected as % of ultimate premium`), 1),
    stringsAsFactors = FALSE,
    check.names = FALSE
  )

  summary_data <- rbind(summary_data, grand_total)

  return(summary_data)
}

# Generate the data
movements_ave <- generate_movements_ave_data(num_classes = 10)
movements_ave_summary <- generate_summary_data(movements_ave)

# Display summary statistics
cat(paste(rep("=", 80), collapse = ""), "\n")
cat("SAO Addendum Return - 100 Movements and AvE Analysis Summary\n")
cat(paste(rep("=", 80), collapse = ""), "\n")
cat(sprintf("Total Classes: %d\n", length(unique(movements_ave$`Reserving Class`))))
cat(sprintf("Total Records: %d\n", nrow(movements_ave)))
cat(sprintf("Total Ultimate Premium: £%s k\n",
            format(sum(movements_ave$`Ultimate Premium (£000s)`), big.mark = ",")))
cat(sprintf("Total Reserves (2025YE): £%s k\n",
            format(sum(movements_ave$`Reserves 2025YE (£000s)`), big.mark = ",")))
cat(paste(rep("=", 80), collapse = ""), "\n")
cat("\nSummary by Underwriting Year:\n")
print(movements_ave_summary)
cat("\n")
cat(paste(rep("=", 80), collapse = ""), "\n")
cat("\nFirst 15 records:\n")
print(head(movements_ave, 15))
cat("\n")

# These tables will be available in Power BI
# Power BI will automatically detect the 'movements_ave' and
# 'movements_ave_summary' data frames
