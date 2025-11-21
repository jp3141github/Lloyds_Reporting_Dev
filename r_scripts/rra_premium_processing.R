# RRA Premium Processing Script for Power BI
# Solvency II Pillar 3 - Risk and Claim Reporting
# Reserve Return Annual (RRA) Forms Generator
#
# This script processes Lloyd's premium data and generates output tables
# required by the RRA - Reserve Return Annual forms.
#
# Compatible with Power BI R visual and data transformations.

# Required libraries
required_packages <- c("dplyr", "tidyr", "readr", "writexl", "lubridate")

# Function to check and install packages
install_if_missing <- function(packages) {
  for (pkg in packages) {
    if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
      message(paste("Installing package:", pkg))
      install.packages(pkg, repos = "http://cran.r-project.org", quiet = TRUE)
      library(pkg, character.only = TRUE)
    }
  }
}

# Install and load required packages
install_if_missing(required_packages)

# RRAPremiumProcessor Class (using R6 for OOP approach)
# For simplicity, we'll use functional programming approach in R

#' Validate Premium Data
#'
#' @param premium_data Data frame containing premium data
#' @return Validated data frame or error
validate_premium_data <- function(premium_data) {
  required_columns <- c(
    "Syndicate Number", "UMR", "Insured Country", "Risk Location",
    "Insured Name", "Insured - Policyholder Type", "Risk Code",
    "Risk / Certificate Reference", "Original Currency", "Sum Insured",
    "Gross Annual Premium in Period", "YOA", "Part VII Indicator"
  )

  missing_cols <- setdiff(required_columns, names(premium_data))

  if (length(missing_cols) > 0) {
    stop(paste("Missing required columns:", paste(missing_cols, collapse = ", ")))
  }

  return(premium_data)
}

#' Create Premium Summary By Syndicate
#'
#' @param premium_data Data frame containing premium data
#' @return Data frame with premium summary by syndicate
create_premium_summary_by_syndicate <- function(premium_data) {
  summary_df <- premium_data %>%
    group_by(`Syndicate Number`, YOA) %>%
    summarise(
      `Total Premium` = sum(`Gross Annual Premium in Period`, na.rm = TRUE),
      `Average Premium` = mean(`Gross Annual Premium in Period`, na.rm = TRUE),
      `Number of Risks` = n(),
      `Total Sum Insured` = sum(`Sum Insured`, na.rm = TRUE),
      `Unique UMRs` = n_distinct(UMR),
      .groups = 'drop'
    ) %>%
    mutate(across(where(is.numeric), ~round(., 2)))

  return(summary_df)
}

#' Create Premium Analysis By Risk Code
#'
#' @param premium_data Data frame containing premium data
#' @return Data frame with premium breakdown by risk code
create_premium_by_risk_code <- function(premium_data) {
  risk_summary <- premium_data %>%
    group_by(`Risk Code`, YOA, `Syndicate Number`) %>%
    summarise(
      `Total Premium` = sum(`Gross Annual Premium in Period`, na.rm = TRUE),
      `Total Sum Insured` = sum(`Sum Insured`, na.rm = TRUE),
      `Number of Policies` = n(),
      .groups = 'drop'
    ) %>%
    mutate(across(where(is.numeric), ~round(., 2)))

  return(risk_summary)
}

#' Create Geographic Analysis
#'
#' @param premium_data Data frame containing premium data
#' @return Data frame with premium analysis by country
create_geographic_analysis <- function(premium_data) {
  geo_summary <- premium_data %>%
    group_by(Country = `Insured Country`, YOA) %>%
    summarise(
      `Total Premium` = sum(`Gross Annual Premium in Period`, na.rm = TRUE),
      `Total Sum Insured` = sum(`Sum Insured`, na.rm = TRUE),
      `Number of Syndicates` = n_distinct(`Syndicate Number`),
      `Number of Policies` = n(),
      .groups = 'drop'
    ) %>%
    group_by(YOA) %>%
    mutate(
      `Premium Share %` = round((`Total Premium` / sum(`Total Premium`)) * 100, 2)
    ) %>%
    ungroup() %>%
    mutate(across(c(`Total Premium`, `Total Sum Insured`), ~round(., 2)))

  return(geo_summary)
}

#' Create Policyholder Type Analysis
#'
#' @param premium_data Data frame containing premium data
#' @return Data frame with premium analysis by policyholder type
create_policyholder_type_analysis <- function(premium_data) {
  type_summary <- premium_data %>%
    group_by(
      `Policyholder Type` = `Insured - Policyholder Type`,
      YOA,
      `Syndicate Number`
    ) %>%
    summarise(
      `Total Premium` = sum(`Gross Annual Premium in Period`, na.rm = TRUE),
      `Average Premium` = mean(`Gross Annual Premium in Period`, na.rm = TRUE),
      `Total Sum Insured` = sum(`Sum Insured`, na.rm = TRUE),
      `Number of Policies` = n(),
      .groups = 'drop'
    ) %>%
    mutate(across(where(is.numeric), ~round(., 2)))

  return(type_summary)
}

#' Create Currency Analysis
#'
#' @param premium_data Data frame containing premium data
#' @return Data frame with premium analysis by currency
create_currency_analysis <- function(premium_data) {
  currency_summary <- premium_data %>%
    group_by(Currency = `Original Currency`, YOA) %>%
    summarise(
      `Total Premium` = sum(`Gross Annual Premium in Period`, na.rm = TRUE),
      `Total Sum Insured` = sum(`Sum Insured`, na.rm = TRUE),
      `Number of Policies` = n(),
      .groups = 'drop'
    ) %>%
    group_by(YOA) %>%
    mutate(
      `Policy Share %` = round((`Number of Policies` / sum(`Number of Policies`)) * 100, 2)
    ) %>%
    ungroup() %>%
    mutate(across(c(`Total Premium`, `Total Sum Insured`), ~round(., 2)))

  return(currency_summary)
}

#' Create Part VII Analysis
#'
#' @param premium_data Data frame containing premium data
#' @return Data frame with analysis of Part VII transfers
create_part_vii_analysis <- function(premium_data) {
  part_vii_summary <- premium_data %>%
    group_by(`Part VII Indicator`, YOA, `Syndicate Number`) %>%
    summarise(
      `Total Premium` = sum(`Gross Annual Premium in Period`, na.rm = TRUE),
      `Total Sum Insured` = sum(`Sum Insured`, na.rm = TRUE),
      `Number of Policies` = n(),
      .groups = 'drop'
    ) %>%
    mutate(across(where(is.numeric), ~round(., 2)))

  return(part_vii_summary)
}

#' Create Detailed Risk Register
#'
#' @param premium_data Data frame containing premium data
#' @return Data frame with detailed risk-level data
create_detailed_risk_register <- function(premium_data) {
  risk_register <- premium_data %>%
    mutate(
      `Premium to Sum Insured Ratio` = round(
        (`Gross Annual Premium in Period` / `Sum Insured`) * 100, 2
      ),
      `Risk Size Classification` = case_when(
        `Gross Annual Premium in Period` < 50000 ~ "Small",
        `Gross Annual Premium in Period` < 500000 ~ "Medium",
        `Gross Annual Premium in Period` < 2000000 ~ "Large",
        TRUE ~ "Very Large"
      )
    )

  return(risk_register)
}

#' Generate All RRA Outputs
#'
#' @param premium_data Data frame containing premium data
#' @return List of data frames containing all outputs
generate_all_rra_outputs <- function(premium_data) {
  # Validate data first
  premium_data <- validate_premium_data(premium_data)

  outputs <- list(
    Premium_Summary_By_Syndicate = create_premium_summary_by_syndicate(premium_data),
    Premium_By_Risk_Code = create_premium_by_risk_code(premium_data),
    Geographic_Analysis = create_geographic_analysis(premium_data),
    Policyholder_Type_Analysis = create_policyholder_type_analysis(premium_data),
    Currency_Analysis = create_currency_analysis(premium_data),
    Part_VII_Analysis = create_part_vii_analysis(premium_data),
    Detailed_Risk_Register = create_detailed_risk_register(premium_data)
  )

  return(outputs)
}

#' Export RRA Outputs to Excel
#'
#' @param premium_data Data frame containing premium data
#' @param output_path Path to output Excel file
export_rra_outputs <- function(premium_data, output_path = "rra_premium_output.xlsx") {
  outputs <- generate_all_rra_outputs(premium_data)

  # Export to Excel using writexl
  write_xlsx(outputs, output_path)

  message(paste("RRA outputs exported to", output_path))
  return(invisible(NULL))
}

#' Process Premium Data for Power BI
#'
#' Main function for Power BI integration.
#' This function is designed to be called from Power BI R visual or script.
#'
#' @param dataset Data frame from Power BI
#' @return Data frame with processed output for visualization
process_premium_data_for_powerbi <- function(dataset) {
  # Validate data
  dataset <- validate_premium_data(dataset)

  # For Power BI, typically return a single DataFrame for visualization
  # You can modify this to return different outputs based on requirements
  result <- create_premium_summary_by_syndicate(dataset)

  return(result)
}

# Main execution block (for standalone testing)
if (interactive() || !exists("dataset")) {

  main <- function() {
    # Load synthetic data
    message("Loading premium data...")

    # Try to read the CSV file
    data_path <- "../synthetic_data/synthetic_lloyds_premium_data.csv"

    if (!file.exists(data_path)) {
      stop(paste("Data file not found:", data_path))
    }

    premium_data <- read_csv(data_path, show_col_types = FALSE)

    message(paste("Loaded", nrow(premium_data), "premium records"))

    # Process data
    message("\nProcessing RRA outputs...")
    outputs <- generate_all_rra_outputs(premium_data)

    # Display summary of each output
    message("\n", paste(rep("=", 80), collapse = ""))
    message("RRA OUTPUT TABLES GENERATED")
    message(paste(rep("=", 80), collapse = ""))

    for (name in names(outputs)) {
      df <- outputs[[name]]
      message("\n", name, ":")
      message("  Rows: ", nrow(df))
      message("  Columns: ", paste(names(df), collapse = ", "))
      message("\n  Preview:")
      print(head(df, 5))
      message(paste(rep("-", 80), collapse = ""))
    }

    # Export to Excel
    output_file <- "../synthetic_data/rra_premium_outputs_r.xlsx"
    export_rra_outputs(premium_data, output_file)
    message("\n✓ All outputs exported to ", output_file)

    # Power BI integration example
    message("\n", paste(rep("=", 80), collapse = ""))
    message("POWER BI INTEGRATION EXAMPLE")
    message(paste(rep("=", 80), collapse = ""))
    message("\nTo use in Power BI, source this script and call:")
    message("  result <- process_premium_data_for_powerbi(dataset)")
    message("\nOr create custom visualizations using individual functions:")
    message("  geographic_data <- create_geographic_analysis(dataset)")

    return(invisible(outputs))
  }

  # Run main function
  tryCatch({
    main()
  }, error = function(e) {
    message("Error: ", e$message)
  })
}

# For Power BI: When using this script in Power BI, the 'dataset' variable
# will be automatically provided by Power BI. The script will execute and
# return the result for visualization.
if (exists("dataset")) {
  # Power BI execution path
  output <- process_premium_data_for_powerbi(dataset)
  print(output)
}
