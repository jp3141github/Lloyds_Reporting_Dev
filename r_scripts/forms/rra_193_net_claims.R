# RRA 193 Net Claims Form - Power BI R Script
# This script processes and analyzes RRA 193 Net Claims development triangles

library(dplyr)
library(tidyr)
library(readr)

#' Process RRA 193 Net Claims data for Power BI
#'
#' @param data_source Path to the net claims data CSV file
#' @return Processed claims data ready for Power BI visualization
process_rra_193 <- function(data_source = "../../synthetic_data/rra_193_net_claims.csv") {

  # Load data
  df <- read_csv(data_source, show_col_types = FALSE)

  # Calculate key metrics
  df <- df %>%
    mutate(
      Incurred_Claims = Cumulative_Paid_Claims + Case_Reserves + IBNR_Reserve,

      Loss_Ratio_Net = ifelse(Net_Premium_Written > 0,
                               Total_Incurred / Net_Premium_Written,
                               0),

      Loss_Ratio_Gross = ifelse(Gross_Premium_Written > 0,
                                 Total_Incurred / Gross_Premium_Written,
                                 0)
    )

  # Sort for development factor calculations
  df <- df %>%
    arrange(Syndicate_Number, Year_of_Account, LOB_Code, Development_Year)

  # Calculate development factors (year-over-year)
  df <- df %>%
    group_by(Syndicate_Number, Year_of_Account, LOB_Code) %>%
    mutate(
      Prior_Cumulative_Paid = lag(Cumulative_Paid_Claims),
      Paid_Development_Factor = ifelse(is.na(Prior_Cumulative_Paid) | Prior_Cumulative_Paid == 0,
                                        NA,
                                        Cumulative_Paid_Claims / Prior_Cumulative_Paid),

      Prior_Total_Incurred = lag(Total_Incurred),
      Incurred_Development_Factor = ifelse(is.na(Prior_Total_Incurred) | Prior_Total_Incurred == 0,
                                            NA,
                                            Total_Incurred / Prior_Total_Incurred),

      # Calculate reserve ratios
      Case_Reserve_Ratio = ifelse(Total_Incurred > 0,
                                   Case_Reserves / Total_Incurred,
                                   0),

      IBNR_Ratio = ifelse(Total_Incurred > 0,
                           IBNR_Reserve / Total_Incurred,
                           0),

      Paid_Ratio = ifelse(Total_Incurred > 0,
                           Cumulative_Paid_Claims / Total_Incurred,
                           0),

      # Calculate claims closure rate
      Claims_Closure_Rate = ifelse(Number_of_Claims > 0,
                                    Number_of_Claims_Closed / Number_of_Claims,
                                    0),

      # Add maturity indicators
      Maturity_Years = Development_Year,
      Is_Mature = Development_Year >= 3,

      # Calculate average claim amounts
      Average_Paid_Per_Claim = ifelse(Number_of_Claims_Closed > 0,
                                       Cumulative_Paid_Claims / Number_of_Claims_Closed,
                                       0),

      Average_Incurred_Per_Claim = ifelse(Number_of_Claims > 0,
                                           Total_Incurred / Number_of_Claims,
                                           0)
    ) %>%
    ungroup()

  return(df)
}


#' Create a development triangle for a specific metric
#'
#' @param data_source Path to the data file
#' @param metric Metric to display ('Total_Incurred', 'Cumulative_Paid_Claims', etc.)
#' @param syndicate Filter for specific syndicate (optional)
#' @param lob_code Filter for specific line of business (optional)
#' @return Development triangle
create_development_triangle <- function(data_source = "../../synthetic_data/rra_193_net_claims.csv",
                                        metric = "Total_Incurred",
                                        syndicate = NULL,
                                        lob_code = NULL) {

  df <- read_csv(data_source, show_col_types = FALSE)

  # Apply filters
  if (!is.null(syndicate)) {
    df <- df %>% filter(Syndicate_Number == syndicate)
  }
  if (!is.null(lob_code)) {
    df <- df %>% filter(LOB_Code == lob_code)
  }

  # Pivot to create triangle
  triangle <- df %>%
    group_by(Year_of_Account, Development_Year) %>%
    summarise(Value = sum(.data[[metric]], na.rm = TRUE), .groups = "drop") %>%
    pivot_wider(names_from = Development_Year,
                values_from = Value,
                values_fill = 0)

  return(triangle)
}


#' Calculate chain ladder development factors
#'
#' @param data_source Path to the data file
#' @param syndicate Filter for specific syndicate (optional)
#' @param lob_code Filter for specific line of business (optional)
#' @return Development factors by development year
calculate_chain_ladder <- function(data_source = "../../synthetic_data/rra_193_net_claims.csv",
                                   syndicate = NULL,
                                   lob_code = NULL) {

  df <- process_rra_193(data_source)

  # Apply filters
  if (!is.null(syndicate)) {
    df <- df %>% filter(Syndicate_Number == syndicate)
  }
  if (!is.null(lob_code)) {
    df <- df %>% filter(LOB_Code == lob_code)
  }

  # Calculate average development factors
  dev_factors <- df %>%
    group_by(Development_Year) %>%
    summarise(
      Paid_LDF_Mean = mean(Paid_Development_Factor, na.rm = TRUE),
      Paid_LDF_Median = median(Paid_Development_Factor, na.rm = TRUE),
      Paid_LDF_StdDev = sd(Paid_Development_Factor, na.rm = TRUE),
      Paid_Sample_Size = sum(!is.na(Paid_Development_Factor)),

      Incurred_LDF_Mean = mean(Incurred_Development_Factor, na.rm = TRUE),
      Incurred_LDF_Median = median(Incurred_Development_Factor, na.rm = TRUE),
      Incurred_LDF_StdDev = sd(Incurred_Development_Factor, na.rm = TRUE),
      Incurred_Sample_Size = sum(!is.na(Incurred_Development_Factor)),
      .groups = "drop"
    )

  return(dev_factors)
}


#' Generate claims summary by Year of Account
#'
#' @param data_source Path to the data file
#' @return Summary by Year of Account
get_claims_summary_by_yoa <- function(data_source = "../../synthetic_data/rra_193_net_claims.csv") {

  df <- process_rra_193(data_source)

  # Get latest development year for each YoA
  latest <- df %>%
    group_by(Syndicate_Number, Year_of_Account, LOB_Code) %>%
    slice_max(Development_Year, n = 1) %>%
    ungroup()

  summary <- latest %>%
    group_by(Year_of_Account) %>%
    summarise(
      Gross_Premium_Written_M = sum(Gross_Premium_Written) / 1000000,
      Net_Premium_Written_M = sum(Net_Premium_Written) / 1000000,
      Cumulative_Paid_Claims_M = sum(Cumulative_Paid_Claims) / 1000000,
      Case_Reserves_M = sum(Case_Reserves) / 1000000,
      IBNR_Reserve_M = sum(IBNR_Reserve) / 1000000,
      Total_Incurred_M = sum(Total_Incurred) / 1000000,
      Number_of_Claims = sum(Number_of_Claims),
      Number_of_Claims_Closed = sum(Number_of_Claims_Closed),

      Net_Loss_Ratio = ifelse(sum(Net_Premium_Written) > 0,
                               sum(Total_Incurred) / sum(Net_Premium_Written),
                               0),

      Claims_Closure_Rate = ifelse(sum(Number_of_Claims) > 0,
                                    sum(Number_of_Claims_Closed) / sum(Number_of_Claims),
                                    0),
      .groups = "drop"
    )

  summary <- summary %>%
    mutate(across(where(is.numeric), ~round(.x, 2)))

  return(summary)
}


#' Generate claims summary by Line of Business
#'
#' @param data_source Path to the data file
#' @return Summary by LOB
get_claims_summary_by_lob <- function(data_source = "../../synthetic_data/rra_193_net_claims.csv") {

  df <- process_rra_193(data_source)

  # Get latest development year for each combination
  latest <- df %>%
    group_by(Syndicate_Number, Year_of_Account, LOB_Code) %>%
    slice_max(Development_Year, n = 1) %>%
    ungroup()

  summary <- latest %>%
    group_by(LOB_Code) %>%
    summarise(
      Gross_Premium_Written_M = sum(Gross_Premium_Written) / 1000000,
      Net_Premium_Written_M = sum(Net_Premium_Written) / 1000000,
      Cumulative_Paid_Claims_M = sum(Cumulative_Paid_Claims) / 1000000,
      Case_Reserves_M = sum(Case_Reserves) / 1000000,
      IBNR_Reserve_M = sum(IBNR_Reserve) / 1000000,
      Total_Incurred_M = sum(Total_Incurred) / 1000000,
      Number_of_Claims = sum(Number_of_Claims),
      Loss_Ratio_Net = mean(Loss_Ratio_Net),

      Average_Claim_Size_M = ifelse(sum(Number_of_Claims) > 0,
                                     sum(Total_Incurred) / sum(Number_of_Claims) / 1000000,
                                     0),
      .groups = "drop"
    )

  summary <- summary %>%
    mutate(across(where(is.numeric), ~round(.x, 2)))

  return(summary)
}


# For use in Power BI
# df <- process_rra_193()


# Test the functions if run directly
if (interactive() || !exists("dataset")) {
  cat("Processing RRA 193 Net Claims Data...\n")
  df <- process_rra_193()
  cat(sprintf("\nProcessed %d records\n", nrow(df)))

  cat("\n", rep("=", 80), "\n", sep = "")
  cat("Claims Summary by Year of Account:\n")
  cat(rep("=", 80), "\n", sep = "")
  print(get_claims_summary_by_yoa())

  cat("\n", rep("=", 80), "\n", sep = "")
  cat("Claims Summary by Line of Business:\n")
  cat(rep("=", 80), "\n", sep = "")
  print(get_claims_summary_by_lob())

  cat("\n", rep("=", 80), "\n", sep = "")
  cat("Chain Ladder Development Factors:\n")
  cat(rep("=", 80), "\n", sep = "")
  print(calculate_chain_ladder())
}
