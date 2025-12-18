# Lloyd's Liquidity Stress Test - R Implementation for Power BI
# Processes Lloyd's syndicate data to generate RRA (Reserve Return Annual) form outputs

library(dplyr)
library(tidyr)
library(jsonlite)
library(readr)
library(openxlsx)

#' LiquidityStressTest R6 Class
#'
#' Main class for processing Lloyd's Liquidity Stress Test data
#' Compatible with Power BI R visual
#'
#' @export
LiquidityStressTest <- R6::R6Class(
  "LiquidityStressTest",

  public = list(
    data_path = NULL,
    metadata = NULL,
    assets_data = NULL,
    cashflow_data = NULL,
    stress_data = NULL,

    #' Initialize the LiquidityStressTest object
    #'
    #' @param data_path Path to directory containing syndicate data
    initialize = function(data_path = "../data") {
      self$data_path <- data_path
    },

    #' Load data for analysis
    #'
    #' @param syndicate_number Specific syndicate to load (optional)
    #' @return List of loaded data
    load_data = function(syndicate_number = NULL) {
      if (!is.null(syndicate_number)) {
        # Load individual syndicate
        syndicate_path <- file.path(self$data_path, paste0("syndicate_", syndicate_number))

        metadata <- fromJSON(file.path(syndicate_path, "metadata.json"))
        assets <- read_csv(file.path(syndicate_path, "assets_liquidity.csv"), show_col_types = FALSE)
        cashflow <- read_csv(file.path(syndicate_path, "cashflow.csv"), show_col_types = FALSE)
        stress <- read_csv(file.path(syndicate_path, "stress_scenario.csv"), show_col_types = FALSE)

        return(list(
          metadata = metadata,
          assets = assets,
          cashflow = cashflow,
          stress = stress
        ))
      } else {
        # Load all syndicates combined
        self$metadata <- read_csv(file.path(self$data_path, "all_syndicates_metadata.csv"), show_col_types = FALSE)
        self$assets_data <- read_csv(file.path(self$data_path, "all_syndicates_assets.csv"), show_col_types = FALSE)
        self$cashflow_data <- read_csv(file.path(self$data_path, "all_syndicates_cashflow.csv"), show_col_types = FALSE)
        self$stress_data <- read_csv(file.path(self$data_path, "all_syndicates_stress.csv"), show_col_types = FALSE)

        return(list(
          metadata = self$metadata,
          assets = self$assets_data,
          cashflow = self$cashflow_data,
          stress = self$stress_data
        ))
      }
    },

    #' Calculate Capital Position Table
    #'
    #' Generate Capital Position summary table for RRA forms
    #'
    #' @param syndicate_number Filter for specific syndicate (optional)
    #' @return Data frame with capital position
    calculate_capital_position_table = function(syndicate_number = NULL) {
      if (is.null(self$metadata)) {
        self$load_data()
      }

      df <- self$metadata

      if (!is.null(syndicate_number)) {
        df <- df %>% filter(syndicate_number == !!syndicate_number)
      }

      # Select relevant columns and calculate ratios
      capital_position <- df %>%
        select(
          syndicate_number,
          syndicate_name,
          managing_agent,
          qma_date,
          syndicate_fal,
          syndicate_fis,
          syndicate_uscr,
          syndicate_ueca
        ) %>%
        mutate(
          solvency_ratio = round(syndicate_fal / syndicate_uscr, 2),
          eca_coverage = round(syndicate_fal / syndicate_ueca, 2),
          syndicate_fal_formatted = paste0("£", format(syndicate_fal, big.mark = ",", scientific = FALSE)),
          syndicate_fis_formatted = paste0("£", format(syndicate_fis, big.mark = ",", scientific = FALSE)),
          syndicate_uscr_formatted = paste0("£", format(syndicate_uscr, big.mark = ",", scientific = FALSE)),
          syndicate_ueca_formatted = paste0("£", format(syndicate_ueca, big.mark = ",", scientific = FALSE))
        )

      return(capital_position)
    },

    #' Calculate Liquidity Breakdown Table
    #'
    #' Generate Asset & Liquidity Breakdown table for RRA forms
    #'
    #' @param syndicate_number Filter for specific syndicate (optional)
    #' @param date Filter for specific date (optional)
    #' @return Data frame with liquidity breakdown
    calculate_liquidity_breakdown_table = function(syndicate_number = NULL, date = NULL) {
      if (is.null(self$assets_data)) {
        self$load_data()
      }

      df <- self$assets_data

      if (!is.null(syndicate_number)) {
        df <- df %>% filter(syndicate_number == !!syndicate_number)
      }

      if (!is.null(date)) {
        df <- df %>% filter(date == !!date)
      }

      # Calculate totals and percentages
      df <- df %>%
        mutate(
          total_assets = restricted_assets_total + illiquid_assets_total + liquid_assets_total,
          restricted_pct = round(restricted_assets_total / total_assets * 100, 2),
          illiquid_pct = round(illiquid_assets_total / total_assets * 100, 2),
          liquid_pct = round(liquid_assets_total / total_assets * 100, 2)
        )

      return(df)
    },

    #' Calculate Cashflow Summary Table
    #'
    #' Generate Cashflow Summary table for RRA forms
    #'
    #' @param syndicate_number Filter for specific syndicate (optional)
    #' @return Data frame with cashflow summary
    calculate_cashflow_summary_table = function(syndicate_number = NULL) {
      if (is.null(self$cashflow_data)) {
        self$load_data()
      }

      df <- self$cashflow_data

      if (!is.null(syndicate_number)) {
        df <- df %>% filter(syndicate_number == !!syndicate_number)
      }

      # Add cumulative columns
      df <- df %>%
        group_by(syndicate_number) %>%
        mutate(
          cumulative_premium_income = cumsum(premium_income),
          cumulative_claims_paid = cumsum(claims_paid),
          cumulative_total_movements = cumsum(total_movements)
        ) %>%
        ungroup()

      return(df)
    },

    #' Calculate Stress Impact Table
    #'
    #' Generate Stress Test Impact table for RRA forms
    #'
    #' @param syndicate_number Filter for specific syndicate (optional)
    #' @return Data frame with stress impact analysis
    calculate_stress_impact_table = function(syndicate_number = NULL) {
      if (is.null(self$cashflow_data) || is.null(self$stress_data)) {
        self$load_data()
      }

      # Merge baseline cashflow with stress scenario
      merged <- self$cashflow_data %>%
        left_join(
          self$stress_data,
          by = c("syndicate_number", "date")
        )

      if (!is.null(syndicate_number)) {
        merged <- merged %>% filter(syndicate_number == !!syndicate_number)
      }

      # Calculate stressed cashflow positions
      merged <- merged %>%
        mutate(
          stressed_closing_funds = closing_free_funds + stress_scenario_impact,
          liquidity_gap = closing_free_funds - stressed_closing_funds
        ) %>%
        group_by(syndicate_number) %>%
        mutate(
          min_liquidity_baseline = min(closing_free_funds),
          min_liquidity_stressed = min(stressed_closing_funds)
        ) %>%
        ungroup()

      return(merged)
    },

    #' Calculate all RRA Output Tables
    #'
    #' Generate all RRA output tables
    #'
    #' @param syndicate_number Filter for specific syndicate (optional)
    #' @return List of all output tables
    calculate_rra_output_tables = function(syndicate_number = NULL) {
      list(
        capital_position = self$calculate_capital_position_table(syndicate_number),
        liquidity_breakdown = self$calculate_liquidity_breakdown_table(syndicate_number),
        cashflow_summary = self$calculate_cashflow_summary_table(syndicate_number),
        stress_impact = self$calculate_stress_impact_table(syndicate_number)
      )
    },

    #' Create Dashboard Summary
    #'
    #' Create executive dashboard summary with key metrics
    #'
    #' @param syndicate_number Filter for specific syndicate (optional)
    #' @return Data frame with dashboard summary
    create_dashboard_summary = function(syndicate_number = NULL) {
      if (is.null(self$metadata)) {
        self$load_data()
      }

      capital <- self$calculate_capital_position_table(syndicate_number)
      stress <- self$calculate_stress_impact_table(syndicate_number)

      summary_data <- capital %>%
        rowwise() %>%
        mutate(
          synd_stress = list(stress %>% filter(syndicate_number == .data$syndicate_number)),
          synd_meta = list(self$metadata %>% filter(syndicate_number == .data$syndicate_number) %>% slice(1))
        ) %>%
        mutate(
          baseline_min_liquidity = min(synd_stress[[1]]$closing_free_funds),
          stressed_min_liquidity = min(synd_stress[[1]]$stressed_closing_funds),
          max_liquidity_gap = max(synd_stress[[1]]$liquidity_gap),
          stress_scenario = synd_meta[[1]]$scenario_type,
          gross_loss_estimate = synd_meta[[1]]$gross_loss_estimate,
          net_loss_estimate = synd_meta[[1]]$net_loss_estimate,
          us_funding_requirement = synd_meta[[1]]$us_funding_requirement,
          stress_test_pass = stressed_min_liquidity > 0
        ) %>%
        select(
          syndicate_number,
          syndicate_name,
          managing_agent,
          total_fal = syndicate_fal,
          solvency_ratio,
          baseline_min_liquidity,
          stressed_min_liquidity,
          max_liquidity_gap,
          stress_scenario,
          gross_loss_estimate,
          net_loss_estimate,
          us_funding_requirement,
          stress_test_pass
        ) %>%
        ungroup()

      return(summary_data)
    },

    #' Export to Excel
    #'
    #' Export all tables to Excel workbook for easy viewing
    #'
    #' @param output_path Path for output Excel file
    #' @param syndicate_number Filter for specific syndicate (optional)
    export_to_excel = function(output_path, syndicate_number = NULL) {
      tables <- self$calculate_rra_output_tables(syndicate_number)
      summary <- self$create_dashboard_summary(syndicate_number)

      wb <- createWorkbook()

      addWorksheet(wb, "Dashboard Summary")
      writeData(wb, "Dashboard Summary", summary)

      addWorksheet(wb, "Capital Position")
      writeData(wb, "Capital Position", tables$capital_position)

      addWorksheet(wb, "Liquidity Breakdown")
      writeData(wb, "Liquidity Breakdown", tables$liquidity_breakdown)

      addWorksheet(wb, "Cashflow Summary")
      writeData(wb, "Cashflow Summary", tables$cashflow_summary)

      addWorksheet(wb, "Stress Impact Analysis")
      writeData(wb, "Stress Impact Analysis", tables$stress_impact)

      saveWorkbook(wb, output_path, overwrite = TRUE)
      cat(paste0("✓ Exported to ", output_path, "\n"))
    }
  )
)

# Power BI Integration Functions
# These functions can be called directly from Power BI R visuals

#' Get Capital Position Table
#'
#' Power BI wrapper for capital position table
#'
#' @param dataset Input dataset from Power BI
#' @return Processed capital position table
#' @export
get_capital_position <- function(dataset) {
  lst <- LiquidityStressTest$new()
  lst$metadata <- dataset
  return(lst$calculate_capital_position_table())
}

#' Get Liquidity Breakdown Table
#'
#' Power BI wrapper for liquidity breakdown table
#'
#' @param dataset Input dataset from Power BI
#' @return Processed liquidity breakdown table
#' @export
get_liquidity_breakdown <- function(dataset) {
  lst <- LiquidityStressTest$new()
  lst$assets_data <- dataset
  return(lst$calculate_liquidity_breakdown_table())
}

#' Get Stress Impact Analysis
#'
#' Power BI wrapper for stress impact analysis
#'
#' @param cashflow_dataset Cashflow data from Power BI
#' @param stress_dataset Stress scenario data from Power BI
#' @return Processed stress impact table
#' @export
get_stress_impact <- function(cashflow_dataset, stress_dataset) {
  lst <- LiquidityStressTest$new()
  lst$cashflow_data <- cashflow_dataset
  lst$stress_data <- stress_dataset
  return(lst$calculate_stress_impact_table())
}

# Example usage and testing
if (interactive() || !exists("test_mode")) {
  cat("Lloyd's Liquidity Stress Test - R Implementation\n")
  cat(strrep("=", 80), "\n")

  # Initialize
  lst <- LiquidityStressTest$new("data")

  # Load all data
  cat("\nLoading data...\n")
  lst$load_data()
  cat(paste0("✓ Loaded data for ", nrow(lst$metadata), " syndicates\n"))

  # Generate dashboard summary
  cat("\nGenerating dashboard summary...\n")
  summary <- lst$create_dashboard_summary()
  print(summary)

  # Export all tables for syndicate 2001
  cat("\n", strrep("=", 80), "\n", sep = "")
  cat("Exporting detailed analysis for Syndicate 2001...\n")
  lst$export_to_excel("r_implementation/syndicate_2001_analysis.xlsx", syndicate_number = 2001)

  # Export combined analysis for all syndicates
  cat("\nExporting combined analysis for all syndicates...\n")
  lst$export_to_excel("r_implementation/all_syndicates_analysis.xlsx")

  cat("\n", strrep("=", 80), "\n", sep = "")
  cat("Processing complete!\n")
}
