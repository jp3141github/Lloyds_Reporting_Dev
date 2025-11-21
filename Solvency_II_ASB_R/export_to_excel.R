# Excel Export Utility for Solvency II ASB Returns (R Version)
# Exports synthetic data to Excel format matching Lloyd's specifications

# Required libraries
if (!require("tidyverse")) install.packages("tidyverse", quiet = TRUE)
if (!require("writexl")) install.packages("writexl", quiet = TRUE)

library(tidyverse)
library(writexl)

# Source the data generator
source("synthetic_data_generator.R")

# Export ASB returns to Excel
export_asb_returns_to_excel <- function(
    output_filename = "ASB_Returns_Output.xlsx",
    syndicate_number = "1234",
    syndicate_name = "Example Marine & Energy Syndicate",
    start_year = 2015,
    end_year = 2024
) {

  cat("Generating ASB returns data...\n")

  # Generate all data
  all_data <- generate_all_asb_data(
    syndicate_number = syndicate_number,
    syndicate_name = syndicate_name,
    start_year = start_year,
    end_year = end_year,
    claims_records = 500,
    inflation_records = 200
  )

  # Create cover sheet
  cover_sheet <- tibble(
    Field = c(
      "Return Type",
      "Syndicate Number",
      "Syndicate Name",
      "Reporting Period",
      "Currency",
      "Generation Date",
      "Status"
    ),
    Value = c(
      "Solvency II Pillar 3 - ASB Returns",
      syndicate_number,
      syndicate_name,
      paste("Annual", format(Sys.Date(), "%Y")),
      "Multi-currency",
      format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
      "Synthetic Data for Testing"
    )
  )

  # Summary by Line of Business
  lob_summary <- all_data$ASB_245_246_247 %>%
    group_by(LineOfBusiness) %>%
    summarise(
      TotalGrossClaimPaid = sum(GrossClaimPaid, na.rm = TRUE),
      TotalReinsuranceRecoveries = sum(ReinsuranceRecoveries, na.rm = TRUE),
      TotalGrossUndiscountedBEClaimsProvisions = sum(GrossUndiscountedBEClaimsProvisions, na.rm = TRUE),
      TotalGrossRBNS = sum(GrossRBNS, na.rm = TRUE),
      .groups = "drop"
    )

  # Summary by Underwriting Year
  year_summary <- all_data$ASB_245_246_247 %>%
    group_by(UnderwritingYear) %>%
    summarise(
      TotalGrossClaimPaid = sum(GrossClaimPaid, na.rm = TRUE),
      TotalReinsuranceRecoveries = sum(ReinsuranceRecoveries, na.rm = TRUE),
      TotalGrossUndiscountedBEClaimsProvisions = sum(GrossUndiscountedBEClaimsProvisions, na.rm = TRUE),
      TotalGrossRBNS = sum(GrossRBNS, na.rm = TRUE),
      .groups = "drop"
    )

  # Development year analysis
  dev_analysis <- all_data$ASB_245_246_247 %>%
    group_by(DevelopmentYear) %>%
    summarise(
      AvgGrossClaimPaid = mean(GrossClaimPaid, na.rm = TRUE),
      TotalGrossClaimPaid = sum(GrossClaimPaid, na.rm = TRUE),
      ClaimCount = n(),
      TotalReinsuranceRecoveries = sum(ReinsuranceRecoveries, na.rm = TRUE),
      .groups = "drop"
    )

  # Lines of Business reference table
  lob_reference <- tibble(
    Code = names(LloydsDataGenerator$LINES_OF_BUSINESS),
    Description = unname(LloydsDataGenerator$LINES_OF_BUSINESS)
  )

  # Create list of sheets
  sheets <- list(
    "Cover_Sheet" = cover_sheet,
    "ASB_245_246_247_Claims" = all_data$ASB_245_246_247,
    "ASB_248_InflationRates" = all_data$ASB_248,
    "Summary_by_LOB" = lob_summary,
    "Summary_by_Year" = year_summary,
    "Development_Analysis" = dev_analysis,
    "LOB_Reference" = lob_reference
  )

  # Write to Excel
  cat(sprintf("Writing data to %s...\n", output_filename))
  write_xlsx(sheets, output_filename)

  cat("\nExcel file exported successfully!\n")
  cat("Sheets created:\n")
  cat("  - Cover_Sheet\n")
  cat("  - ASB_245_246_247_Claims\n")
  cat("  - ASB_248_InflationRates\n")
  cat("  - Summary_by_LOB\n")
  cat("  - Summary_by_Year\n")
  cat("  - Development_Analysis\n")
  cat("  - LOB_Reference\n")

  return(invisible(sheets))
}

# Main execution
if (!interactive()) {

  cat("\n")
  cat(strrep("=", 80), "\n")
  cat("SOLVENCY II ASB RETURNS - EXCEL EXPORT\n")
  cat(strrep("=", 80), "\n\n")

  # Export to Excel
  export_asb_returns_to_excel(
    output_filename = "ASB_Returns_Synthetic_Data.xlsx",
    syndicate_number = "1234",
    syndicate_name = "Example Marine & Energy Syndicate",
    start_year = 2015,
    end_year = 2024
  )

  cat("\n")
  cat(strrep("=", 80), "\n")
  cat("Export complete!\n")
  cat(strrep("=", 80), "\n")
}
