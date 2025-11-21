# Example Usage of FSCS Data Generator
# =====================================
#
# This script demonstrates how to use the fscs_data_generator.R module
# to create synthetic Lloyd's data for testing and development.

# Load required libraries
library(dplyr)
library(tibble)
library(lubridate)
library(writexl)

# Source the generator module
source("fscs_data_generator.R")


#' Main function demonstrating various usage patterns
main <- function() {

  cat("="*80, "\n")
  cat("FSCS DATA GENERATOR - EXAMPLE USAGE\n")
  cat("="*80, "\n\n")

  # Example 1: Generate summary data using convenience function
  cat("Example 1: Generate Summary Data\n")
  cat(paste(rep("-", 80), collapse = ""), "\n")

  summary_df <- get_fscs_summary_data(num_syndicates = 5, reporting_year = 2024)
  print(summary_df)
  cat("\n")

  # Example 2: Generate detailed transaction data
  cat("\nExample 2: Generate Detailed Transaction Data\n")
  cat(paste(rep("-", 80), collapse = ""), "\n")

  detail_df <- get_fscs_detail_data(num_syndicates = 5, reporting_year = 2024)
  cat(sprintf("Total transactions generated: %d\n", nrow(detail_df)))
  cat(sprintf("Transactions included in FSCS: %d\n",
              sum(detail_df$included_in_fscs)))
  cat("\nFirst 10 transactions:\n")
  print(head(detail_df, 10))
  cat("\n")

  # Example 3: Using the generator class directly
  cat("\nExample 3: Using Generator Class Directly\n")
  cat(paste(rep("-", 80), collapse = ""), "\n")

  generator <- FSCSDataGenerator(num_syndicates = 3, reporting_year = 2024)

  # Get full dataset with all fields
  full_data <- generator$generate_full_dataset()
  cat("Full dataset with calculated fields:\n")
  print(full_data)
  cat("\n")

  # Example 4: Generate data for multiple years
  cat("\nExample 4: Multi-Year Data Generation\n")
  cat(paste(rep("-", 80), collapse = ""), "\n")

  multi_year_data <- bind_rows(
    get_fscs_summary_data(num_syndicates = 3, reporting_year = 2022),
    get_fscs_summary_data(num_syndicates = 3, reporting_year = 2023),
    get_fscs_summary_data(num_syndicates = 3, reporting_year = 2024)
  )

  print(multi_year_data)
  cat("\n")

  # Example 5: Export to Excel (FSCS format)
  cat("\nExample 5: Export to Excel\n")
  cat(paste(rep("-", 80), collapse = ""), "\n")

  # Generate data
  generator <- FSCSDataGenerator(num_syndicates = 10, reporting_year = 2024)
  summary <- generator$generate_fscs_output_format()
  detail <- generator$generate_detail_dataset()
  full <- generator$generate_full_dataset()

  # Create list of data frames for export
  excel_data <- list(
    "FSCS_Summary" = summary,
    "Detail_Transactions" = detail,
    "Full_Dataset" = full
  )

  # Create summary statistics
  stats <- tibble(
    Metric = c(
      'Total Syndicates',
      'Total GWP (£M)',
      'Total BEL (£M)',
      'Avg GWP per Syndicate (£M)',
      'Avg BEL per Syndicate (£M)'
    ),
    Value = c(
      nrow(full),
      round(sum(full$gwp_total) / 1000000, 2),
      round(sum(full$bel_total) / 1000000, 2),
      round(mean(full$gwp_total) / 1000000, 2),
      round(mean(full$bel_total) / 1000000, 2)
    )
  )

  excel_data$"Summary_Statistics" <- stats

  # Export to Excel
  output_file <- 'FSCS_Synthetic_Data.xlsx'
  write_xlsx(excel_data, output_file)

  cat(sprintf("Data exported to: %s\n", output_file))
  cat("\n")

  # Example 6: Summary Statistics
  cat("\nExample 6: Summary Statistics\n")
  cat(paste(rep("-", 80), collapse = ""), "\n")

  cat(sprintf("Total GWP General Business: £%s\n",
              format(sum(full$gwp_general_business), big.mark = ",",
                    scientific = FALSE, nsmall = 2)))
  cat(sprintf("Total GWP Life Business: £%s\n",
              format(sum(full$gwp_life_business), big.mark = ",",
                    scientific = FALSE, nsmall = 2)))
  cat(sprintf("Total BEL General Business: £%s\n",
              format(sum(full$bel_general_business), big.mark = ",",
                    scientific = FALSE, nsmall = 2)))
  cat(sprintf("Total BEL Life Business: £%s\n",
              format(sum(full$bel_life_business), big.mark = ",",
                    scientific = FALSE, nsmall = 2)))
  cat(sprintf("\nAverage General Business %%: %.2f%%\n",
              mean(full$general_business_pct)))
  cat("\n")

  # Example 7: Filtering and Analysis
  cat("\nExample 7: Filtering and Analysis\n")
  cat(paste(rep("-", 80), collapse = ""), "\n")

  # Find syndicates with high GWP
  high_gwp <- full %>%
    filter(gwp_total > 200000000) %>%
    arrange(desc(gwp_total))

  cat(sprintf("Syndicates with GWP > £200M: %d\n", nrow(high_gwp)))
  if (nrow(high_gwp) > 0) {
    print(high_gwp %>% select(syndicate_number, gwp_total, managing_agent))
  }
  cat("\n")

  # Business mix analysis
  cat("Business Mix Analysis:\n")
  business_mix <- full %>%
    summarise(
      Avg_General_Pct = mean(general_business_pct),
      Syndicates_100pct_General = sum(general_business_pct == 100),
      Syndicates_Mixed = sum(general_business_pct > 0 & general_business_pct < 100),
      Syndicates_100pct_Life = sum(general_business_pct == 0)
    )
  print(business_mix)
  cat("\n")

  # Example 8: Transaction-level analysis
  cat("\nExample 8: Transaction-Level Analysis\n")
  cat(paste(rep("-", 80), collapse = ""), "\n")

  if (nrow(detail) > 0) {
    # Analyze by business type
    business_type_summary <- detail %>%
      group_by(business_type) %>%
      summarise(
        Num_Contracts = n(),
        Total_GWP = sum(gwp),
        Total_BEL = sum(bel),
        Avg_Contract_Size = mean(gwp),
        .groups = 'drop'
      )

    cat("Summary by Business Type:\n")
    print(business_type_summary)
    cat("\n")

    # Analyze by territory
    territory_summary <- detail %>%
      filter(included_in_fscs) %>%
      group_by(territory) %>%
      summarise(
        Num_Contracts = n(),
        Total_GWP = sum(gwp),
        .groups = 'drop'
      ) %>%
      arrange(desc(Total_GWP))

    cat("Summary by Territory (FSCS-included contracts only):\n")
    print(territory_summary)
    cat("\n")
  }

  cat("All examples completed successfully!\n")
}


# Run the main function
if (!interactive()) {
  main()
}
