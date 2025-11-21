# Solvency II Pillar 3 - Risk and Claim Reporting
# Step B Claims Template Processor for Power BI
#
# This script processes Lloyd's of London claims data and transforms it
# into the format required for RRA (Reserve Return Annual) forms.
#
# Usage in Power BI:
# 1. Use 'Get Data' -> 'R script'
# 2. Copy this script or reference the file
# 3. Specify the input data source

library(readxl)
library(dplyr)
library(tidyr)
library(openxlsx)


#' Validate and clean the claims data
#'
#' @param df Input claims dataframe
#' @return Validated and cleaned dataframe
validate_claim_data <- function(df) {
  required_columns <- c(
    'Syndicate Number',
    'Claim Reference',
    'UMR',
    'Risk Code',
    'Year of Account',
    'Original Currency',
    'Claim status at beginning of period',
    'Claim status at end of period',
    'Outstanding Claims Amount as at beginning of period',
    'Paid to Date Amount',
    'Paid in Year amount',
    'Outstanding Claim amount as at end of period'
  )

  # Check for required columns
  missing_cols <- setdiff(required_columns, colnames(df))
  if (length(missing_cols) > 0) {
    warning(paste("Missing columns:", paste(missing_cols, collapse = ", ")))
  }

  # Convert numeric columns
  numeric_cols <- c(
    'Outstanding Claims Amount as at beginning of period',
    'Paid to Date Amount',
    'Paid in Year amount',
    'Outstanding Claim amount as at end of period'
  )

  for (col in numeric_cols) {
    if (col %in% colnames(df)) {
      df[[col]] <- as.numeric(df[[col]])
      df[[col]][is.na(df[[col]])] <- 0
    }
  }

  # Convert Year of Account to integer
  if ('Year of Account' %in% colnames(df)) {
    df[['Year of Account']] <- as.integer(df[['Year of Account']])
    df[['Year of Account']][is.na(df[['Year of Account']])] <- 0
  }

  return(df)
}


#' Calculate total incurred amounts for claims
#'
#' @param df Claims dataframe
#' @return Dataframe with calculated incurred amounts
calculate_incurred_amounts <- function(df) {
  df <- df %>%
    mutate(
      # Total Incurred = Paid to Date + Outstanding at end of period
      `Total Incurred as at end of period` =
        `Paid to Date Amount` +
        `Outstanding Claim amount as at end of period`,

      # Movement in year = Outstanding at end - Outstanding at beginning + Paid in year
      `Movement in Year` =
        `Outstanding Claim amount as at end of period` -
        `Outstanding Claims Amount as at beginning of period` +
        `Paid in Year amount`,

      # Reserve movement
      `Reserve Movement` =
        `Outstanding Claim amount as at end of period` -
        `Outstanding Claims Amount as at beginning of period`
    )

  return(df)
}


#' Aggregate claims data by syndicate and year of account
#'
#' @param df Claims dataframe with calculated amounts
#' @return Aggregated dataframe by syndicate
aggregate_by_syndicate <- function(df) {
  grouped <- df %>%
    group_by(`Syndicate Number`, `Year of Account`) %>%
    summarise(
      `Number of Claims` = n(),
      `Outstanding Claims Amount as at beginning of period` = sum(`Outstanding Claims Amount as at beginning of period`, na.rm = TRUE),
      `Paid to Date Amount` = sum(`Paid to Date Amount`, na.rm = TRUE),
      `Paid in Year amount` = sum(`Paid in Year amount`, na.rm = TRUE),
      `Outstanding Claim amount as at end of period` = sum(`Outstanding Claim amount as at end of period`, na.rm = TRUE),
      `Total Incurred as at end of period` = sum(`Total Incurred as at end of period`, na.rm = TRUE),
      `Movement in Year` = sum(`Movement in Year`, na.rm = TRUE),
      `Reserve Movement` = sum(`Reserve Movement`, na.rm = TRUE),
      .groups = 'drop'
    )

  return(grouped)
}


#' Aggregate claims data by risk code and year of account
#'
#' @param df Claims dataframe with calculated amounts
#' @return Aggregated dataframe by risk code
aggregate_by_risk_code <- function(df) {
  grouped <- df %>%
    group_by(`Syndicate Number`, `Year of Account`, `Risk Code`) %>%
    summarise(
      `Number of Claims` = n(),
      `Outstanding Claims Amount as at beginning of period` = sum(`Outstanding Claims Amount as at beginning of period`, na.rm = TRUE),
      `Paid to Date Amount` = sum(`Paid to Date Amount`, na.rm = TRUE),
      `Paid in Year amount` = sum(`Paid in Year amount`, na.rm = TRUE),
      `Outstanding Claim amount as at end of period` = sum(`Outstanding Claim amount as at end of period`, na.rm = TRUE),
      `Total Incurred as at end of period` = sum(`Total Incurred as at end of period`, na.rm = TRUE),
      `Movement in Year` = sum(`Movement in Year`, na.rm = TRUE),
      `Reserve Movement` = sum(`Reserve Movement`, na.rm = TRUE),
      .groups = 'drop'
    )

  return(grouped)
}


#' Aggregate claims data by claim status
#'
#' @param df Claims dataframe with calculated amounts
#' @return Aggregated dataframe by claim status
aggregate_by_claim_status <- function(df) {
  grouped <- df %>%
    group_by(`Syndicate Number`, `Year of Account`, `Claim status at end of period`) %>%
    summarise(
      `Number of Claims` = n(),
      `Outstanding Claims Amount as at beginning of period` = sum(`Outstanding Claims Amount as at beginning of period`, na.rm = TRUE),
      `Paid to Date Amount` = sum(`Paid to Date Amount`, na.rm = TRUE),
      `Paid in Year amount` = sum(`Paid in Year amount`, na.rm = TRUE),
      `Outstanding Claim amount as at end of period` = sum(`Outstanding Claim amount as at end of period`, na.rm = TRUE),
      `Total Incurred as at end of period` = sum(`Total Incurred as at end of period`, na.rm = TRUE),
      `Movement in Year` = sum(`Movement in Year`, na.rm = TRUE),
      `Reserve Movement` = sum(`Reserve Movement`, na.rm = TRUE),
      .groups = 'drop'
    )

  return(grouped)
}


#' Create overall summary report for all syndicates
#'
#' @param df Claims dataframe with calculated amounts
#' @return Summary report dataframe
create_summary_report <- function(df) {
  summary <- data.frame(
    `Total Number of Claims` = nrow(df),
    `Number of Syndicates` = n_distinct(df$`Syndicate Number`),
    `Outstanding Claims Amount as at beginning of period` = sum(df$`Outstanding Claims Amount as at beginning of period`, na.rm = TRUE),
    `Paid to Date Amount` = sum(df$`Paid to Date Amount`, na.rm = TRUE),
    `Paid in Year amount` = sum(df$`Paid in Year amount`, na.rm = TRUE),
    `Outstanding Claim amount as at end of period` = sum(df$`Outstanding Claim amount as at end of period`, na.rm = TRUE),
    `Total Incurred as at end of period` = sum(df$`Total Incurred as at end of period`, na.rm = TRUE),
    `Movement in Year` = sum(df$`Movement in Year`, na.rm = TRUE),
    `Reserve Movement` = sum(df$`Reserve Movement`, na.rm = TRUE),
    check.names = FALSE
  )

  return(summary)
}


#' Main processing function for claims data
#'
#' @param input_file Path to the Excel input file
#' @param sheet_name Name of the sheet containing claims data
#' @return List containing all output tables
process_claims_data <- function(input_file, sheet_name = 'input Sheet') {
  # Read the data
  df <- read_excel(input_file, sheet = sheet_name)

  # Validate and clean
  df <- validate_claim_data(df)

  # Calculate derived amounts
  df <- calculate_incurred_amounts(df)

  # Create different aggregations
  output_tables <- list(
    detailed_claims = df,
    by_syndicate = aggregate_by_syndicate(df),
    by_risk_code = aggregate_by_risk_code(df),
    by_claim_status = aggregate_by_claim_status(df),
    summary = create_summary_report(df)
  )

  return(output_tables)
}


#' Export all output tables to a single Excel file with multiple sheets
#'
#' @param output_tables List of dataframes to export
#' @param output_file Path to the output Excel file
export_to_excel <- function(output_tables, output_file) {
  wb <- createWorkbook()

  for (sheet_name in names(output_tables)) {
    addWorksheet(wb, sheet_name)
    writeData(wb, sheet_name, output_tables[[sheet_name]])
  }

  saveWorkbook(wb, output_file, overwrite = TRUE)
  cat(paste("Output exported to:", output_file, "\n"))
}


#' Transform function specifically designed for Power BI
#' This function expects the input dataframe to be loaded in Power BI
#'
#' @param input_df Input claims dataframe from Power BI
#' @return Transformed dataframe ready for visualization
powerbi_transform <- function(input_df) {
  # Validate and clean
  df <- validate_claim_data(input_df)

  # Calculate derived amounts
  df <- calculate_incurred_amounts(df)

  return(df)
}


# Main execution example
if (!interactive()) {
  # Example usage
  # Replace with your actual file path
  input_file <- "path/to/your/claims_data.xlsx"

  # Process the data
  output_tables <- process_claims_data(input_file)

  # Display summary statistics
  cat("\n=== Summary Report ===\n")
  print(output_tables$summary)

  cat("\n=== By Syndicate ===\n")
  print(output_tables$by_syndicate)

  cat("\n=== By Risk Code ===\n")
  print(output_tables$by_risk_code)

  cat("\n=== By Claim Status ===\n")
  print(output_tables$by_claim_status)

  # Export to Excel
  export_to_excel(output_tables, "claims_output.xlsx")
}


# For Power BI usage:
# 1. Load your data in Power BI
# 2. In R Script Visual or Transform, use:
#    dataset <- powerbi_transform(dataset)
# 3. The transformed data will be available for visualization
