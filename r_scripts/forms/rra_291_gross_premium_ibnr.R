# RRA 291 Gross Premium and IBNR Form - R Script
# This script processes RRA 291 Gross Premium and IBNR estimates
# R port of python_scripts/forms/rra_291_gross_premium_ibnr.py

library(dplyr)
library(tidyr)
library(readr)


#' Process RRA 291 Gross Premium and IBNR data
#'
#' @param data_source Path to the data CSV file
#' @return data.frame with processed data ready for analysis
#' @export
process_rra_291 <- function(data_source = '../../synthetic_data/rra_291_gross_premium_ibnr.csv') {

  # Load data
  df <- readr::read_csv(data_source, show_col_types = FALSE)

  # Calculate total incurred
  df <- df %>%
    mutate(
      Total_Incurred_Gross = Paid_Claims_Gross + Case_Reserves_Gross + IBNR_Best_Estimate
    )

  # Calculate reserve ratios
  df <- df %>%
    mutate(
      Case_Reserve_Ratio = ifelse(
        Total_Incurred_Gross > 0,
        Case_Reserves_Gross / Total_Incurred_Gross,
        0
      ),
      IBNR_Ratio = ifelse(
        Total_Incurred_Gross > 0,
        IBNR_Best_Estimate / Total_Incurred_Gross,
        0
      ),
      Paid_Ratio = ifelse(
        Total_Incurred_Gross > 0,
        Paid_Claims_Gross / Total_Incurred_Gross,
        0
      )
    )

  # Calculate IBNR range
  df <- df %>%
    mutate(
      IBNR_Range = IBNR_High - IBNR_Low,
      IBNR_Range_Pct = ifelse(
        IBNR_Best_Estimate > 0,
        IBNR_Range / IBNR_Best_Estimate,
        0
      )
    )

  # Calculate variance from best estimate
  df <- df %>%
    mutate(
      IBNR_High_Variance = IBNR_High - IBNR_Best_Estimate,
      IBNR_Low_Variance = IBNR_Best_Estimate - IBNR_Low
    )

  # Calculate ultimate loss and loss ratio
  df <- df %>%
    mutate(
      Ultimate_Loss = Total_Incurred_Gross,
      Earned_Premium_Ratio = ifelse(
        Gross_Written_Premium > 0,
        Gross_Earned_Premium / Gross_Written_Premium,
        0
      )
    )

  # Calculate loss ratio metrics
  df <- df %>%
    mutate(
      Loss_Ratio_Incurred = ifelse(
        Gross_Earned_Premium > 0,
        Total_Incurred_Gross / Gross_Earned_Premium,
        0
      ),
      Loss_Ratio_Paid = ifelse(
        Gross_Earned_Premium > 0,
        Paid_Claims_Gross / Gross_Earned_Premium,
        0
      )
    )

  # Add year age (assuming current year is 2024)
  df <- df %>%
    mutate(
      Year_Age = 2024 - Year_of_Account
    )

  # Maturity indicators
  df <- df %>%
    mutate(
      Is_Mature = Year_Age >= 3,
      Maturity_Level = cut(
        Year_Age,
        breaks = c(-Inf, 1, 3, 5, Inf),
        labels = c('Immature', 'Developing', 'Mature', 'Very Mature'),
        right = TRUE
      )
    )

  return(df)
}


#' Generate IBNR summary by Year of Account
#'
#' @param data_source Path to the data CSV file
#' @return data.frame with summary by Year of Account
#' @export
get_ibnr_summary_by_yoa <- function(data_source = '../../synthetic_data/rra_291_gross_premium_ibnr.csv') {

  df <- process_rra_291(data_source)

  summary <- df %>%
    group_by(Year_of_Account) %>%
    summarise(
      Gross_Written_Premium = sum(Gross_Written_Premium, na.rm = TRUE),
      Gross_Earned_Premium = sum(Gross_Earned_Premium, na.rm = TRUE),
      Paid_Claims_Gross = sum(Paid_Claims_Gross, na.rm = TRUE),
      Case_Reserves_Gross = sum(Case_Reserves_Gross, na.rm = TRUE),
      IBNR_Best_Estimate = sum(IBNR_Best_Estimate, na.rm = TRUE),
      IBNR_High = sum(IBNR_High, na.rm = TRUE),
      IBNR_Low = sum(IBNR_Low, na.rm = TRUE),
      Total_Incurred_Gross = sum(Total_Incurred_Gross, na.rm = TRUE),
      Ultimate_Loss_Ratio = mean(Ultimate_Loss_Ratio, na.rm = TRUE),
      .groups = 'drop'
    )

  # Calculate aggregated metrics
  summary <- summary %>%
    mutate(
      Loss_Ratio = ifelse(
        Gross_Earned_Premium > 0,
        Total_Incurred_Gross / Gross_Earned_Premium,
        0
      ),
      IBNR_to_Premium_Ratio = ifelse(
        Gross_Earned_Premium > 0,
        IBNR_Best_Estimate / Gross_Earned_Premium,
        0
      )
    )

  # Add year age
  summary <- summary %>%
    mutate(
      Year_Age = 2024 - Year_of_Account
    )

  # Convert to millions
  summary <- summary %>%
    mutate(
      Gross_Written_Premium_M = Gross_Written_Premium / 1000000,
      Gross_Earned_Premium_M = Gross_Earned_Premium / 1000000,
      Paid_Claims_Gross_M = Paid_Claims_Gross / 1000000,
      Case_Reserves_Gross_M = Case_Reserves_Gross / 1000000,
      IBNR_Best_Estimate_M = IBNR_Best_Estimate / 1000000,
      IBNR_High_M = IBNR_High / 1000000,
      IBNR_Low_M = IBNR_Low / 1000000,
      Total_Incurred_Gross_M = Total_Incurred_Gross / 1000000
    ) %>%
    select(-c(Gross_Written_Premium, Gross_Earned_Premium, Paid_Claims_Gross,
              Case_Reserves_Gross, IBNR_Best_Estimate, IBNR_High, IBNR_Low,
              Total_Incurred_Gross))

  # Round to 2 decimal places
  summary <- summary %>%
    mutate(across(where(is.numeric), ~round(.x, 2)))

  return(summary)
}


#' Generate IBNR summary by Line of Business
#'
#' @param data_source Path to the data CSV file
#' @return data.frame with summary by LOB
#' @export
get_ibnr_summary_by_lob <- function(data_source = '../../synthetic_data/rra_291_gross_premium_ibnr.csv') {

  df <- process_rra_291(data_source)

  summary <- df %>%
    group_by(LOB_Code) %>%
    summarise(
      Gross_Written_Premium = sum(Gross_Written_Premium, na.rm = TRUE),
      Gross_Earned_Premium = sum(Gross_Earned_Premium, na.rm = TRUE),
      Paid_Claims_Gross = sum(Paid_Claims_Gross, na.rm = TRUE),
      Case_Reserves_Gross = sum(Case_Reserves_Gross, na.rm = TRUE),
      IBNR_Best_Estimate = sum(IBNR_Best_Estimate, na.rm = TRUE),
      IBNR_High = sum(IBNR_High, na.rm = TRUE),
      IBNR_Low = sum(IBNR_Low, na.rm = TRUE),
      Total_Incurred_Gross = sum(Total_Incurred_Gross, na.rm = TRUE),
      Ultimate_Loss_Ratio = mean(Ultimate_Loss_Ratio, na.rm = TRUE),
      IBNR_Ratio = mean(IBNR_Ratio, na.rm = TRUE),
      .groups = 'drop'
    )

  # Calculate aggregated metrics
  summary <- summary %>%
    mutate(
      Loss_Ratio = ifelse(
        Gross_Earned_Premium > 0,
        Total_Incurred_Gross / Gross_Earned_Premium,
        0
      )
    )

  # Convert to millions
  summary <- summary %>%
    mutate(
      Gross_Written_Premium_M = Gross_Written_Premium / 1000000,
      Gross_Earned_Premium_M = Gross_Earned_Premium / 1000000,
      Paid_Claims_Gross_M = Paid_Claims_Gross / 1000000,
      Case_Reserves_Gross_M = Case_Reserves_Gross / 1000000,
      IBNR_Best_Estimate_M = IBNR_Best_Estimate / 1000000,
      IBNR_High_M = IBNR_High / 1000000,
      IBNR_Low_M = IBNR_Low / 1000000,
      Total_Incurred_Gross_M = Total_Incurred_Gross / 1000000
    ) %>%
    select(-c(Gross_Written_Premium, Gross_Earned_Premium, Paid_Claims_Gross,
              Case_Reserves_Gross, IBNR_Best_Estimate, IBNR_High, IBNR_Low,
              Total_Incurred_Gross))

  # Round to 2 decimal places
  summary <- summary %>%
    mutate(across(where(is.numeric), ~round(.x, 2)))

  return(summary)
}


#' Analyze IBNR estimate ranges
#'
#' @param data_source Path to the data CSV file
#' @return data.frame with IBNR range analysis
#' @export
get_ibnr_range_analysis <- function(data_source = '../../synthetic_data/rra_291_gross_premium_ibnr.csv') {

  df <- process_rra_291(data_source)

  analysis <- df %>%
    group_by(Year_of_Account, LOB_Code) %>%
    summarise(
      IBNR_Best_Estimate = sum(IBNR_Best_Estimate, na.rm = TRUE),
      IBNR_High = sum(IBNR_High, na.rm = TRUE),
      IBNR_Low = sum(IBNR_Low, na.rm = TRUE),
      IBNR_Range = sum(IBNR_Range, na.rm = TRUE),
      IBNR_Range_Pct = mean(IBNR_Range_Pct, na.rm = TRUE),
      .groups = 'drop'
    )

  # Calculate coefficient of variation
  analysis <- analysis %>%
    mutate(
      IBNR_CV = ifelse(
        IBNR_Best_Estimate > 0,
        IBNR_Range / (2 * IBNR_Best_Estimate),
        0
      )
    )

  # Categorize uncertainty
  analysis <- analysis %>%
    mutate(
      Uncertainty_Level = cut(
        IBNR_Range_Pct,
        breaks = c(0, 0.2, 0.4, 0.6, Inf),
        labels = c('Low', 'Moderate', 'High', 'Very High'),
        right = FALSE
      )
    )

  # Convert to millions
  analysis <- analysis %>%
    mutate(
      IBNR_Best_Estimate_M = IBNR_Best_Estimate / 1000000,
      IBNR_High_M = IBNR_High / 1000000,
      IBNR_Low_M = IBNR_Low / 1000000,
      IBNR_Range_M = IBNR_Range / 1000000
    ) %>%
    select(-c(IBNR_Best_Estimate, IBNR_High, IBNR_Low, IBNR_Range))

  # Round to 2 decimal places
  analysis <- analysis %>%
    mutate(across(where(is.numeric), ~round(.x, 2)))

  return(analysis)
}


#' Analyze ultimate loss ratio trends
#'
#' @param data_source Path to the data CSV file
#' @return data.frame with loss ratio trends by year and LOB
#' @export
get_ultimate_loss_ratio_trend <- function(data_source = '../../synthetic_data/rra_291_gross_premium_ibnr.csv') {

  df <- process_rra_291(data_source)

  trend <- df %>%
    group_by(Year_of_Account, LOB_Code) %>%
    summarise(
      Gross_Earned_Premium = sum(Gross_Earned_Premium, na.rm = TRUE),
      Total_Incurred_Gross = sum(Total_Incurred_Gross, na.rm = TRUE),
      Ultimate_Loss_Ratio = mean(Ultimate_Loss_Ratio, na.rm = TRUE),
      Loss_Ratio_Incurred = mean(Loss_Ratio_Incurred, na.rm = TRUE),
      Year_Age = first(Year_Age),
      .groups = 'drop'
    )

  # Calculate actual loss ratio from totals
  trend <- trend %>%
    mutate(
      Actual_Loss_Ratio = ifelse(
        Gross_Earned_Premium > 0,
        Total_Incurred_Gross / Gross_Earned_Premium,
        0
      )
    )

  # Identify outliers (loss ratio > 1.0)
  trend <- trend %>%
    mutate(
      Is_Outlier = Actual_Loss_Ratio > 1.0
    )

  # Round to 4 decimal places
  trend <- trend %>%
    mutate(across(where(is.numeric), ~round(.x, 4)))

  return(trend)
}


# Main execution for testing
if (sys.nframe() == 0) {
  cat("Processing RRA 291 Gross Premium and IBNR Data...\n")
  df <- process_rra_291()
  cat(sprintf("\nProcessed %d records\n", nrow(df)))

  cat("\n", rep("=", 80), "\n", sep = "")
  cat("IBNR Summary by Year of Account:\n")
  cat(rep("=", 80), "\n", sep = "")
  print(get_ibnr_summary_by_yoa())

  cat("\n", rep("=", 80), "\n", sep = "")
  cat("IBNR Summary by Line of Business:\n")
  cat(rep("=", 80), "\n", sep = "")
  print(get_ibnr_summary_by_lob())

  cat("\n", rep("=", 80), "\n", sep = "")
  cat("IBNR Range Analysis (Sample):\n")
  cat(rep("=", 80), "\n", sep = "")
  print(head(get_ibnr_range_analysis(), 10))
}
