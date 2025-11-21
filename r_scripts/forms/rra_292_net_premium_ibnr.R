# RRA 292 Net Premium and IBNR Form - R Script
# This script processes RRA 292 Net Premium and IBNR estimates (after reinsurance)
# R port of python_scripts/forms/rra_292_net_premium_ibnr.py

library(dplyr)
library(tidyr)
library(readr)


#' Process RRA 292 Net Premium and IBNR data
#'
#' @param data_source Path to the data CSV file
#' @return data.frame with processed data ready for analysis
#' @export
process_rra_292 <- function(data_source = '../../synthetic_data/rra_292_net_premium_ibnr.csv') {

  # Load data
  df <- readr::read_csv(data_source, show_col_types = FALSE)

  # Calculate total incurred (net)
  df <- df %>%
    mutate(
      Total_Incurred_Net = Paid_Claims_Net + Case_Reserves_Net + IBNR_Best_Estimate_Net
    )

  # Calculate reserve ratios
  df <- df %>%
    mutate(
      Case_Reserve_Ratio = ifelse(
        Total_Incurred_Net > 0,
        Case_Reserves_Net / Total_Incurred_Net,
        0
      ),
      IBNR_Ratio = ifelse(
        Total_Incurred_Net > 0,
        IBNR_Best_Estimate_Net / Total_Incurred_Net,
        0
      ),
      Paid_Ratio = ifelse(
        Total_Incurred_Net > 0,
        Paid_Claims_Net / Total_Incurred_Net,
        0
      )
    )

  # Calculate IBNR range (net)
  df <- df %>%
    mutate(
      IBNR_Range_Net = IBNR_High_Net - IBNR_Low_Net,
      IBNR_Range_Pct = ifelse(
        IBNR_Best_Estimate_Net > 0,
        IBNR_Range_Net / IBNR_Best_Estimate_Net,
        0
      )
    )

  # Calculate variance from best estimate
  df <- df %>%
    mutate(
      IBNR_High_Variance = IBNR_High_Net - IBNR_Best_Estimate_Net,
      IBNR_Low_Variance = IBNR_Best_Estimate_Net - IBNR_Low_Net
    )

  # Calculate ultimate loss and loss ratio (net)
  df <- df %>%
    mutate(
      Ultimate_Loss_Net = Total_Incurred_Net,
      Earned_Premium_Ratio = ifelse(
        Net_Written_Premium > 0,
        Net_Earned_Premium / Net_Written_Premium,
        0
      )
    )

  # Calculate loss ratio metrics (net)
  df <- df %>%
    mutate(
      Loss_Ratio_Incurred_Net = ifelse(
        Net_Earned_Premium > 0,
        Total_Incurred_Net / Net_Earned_Premium,
        0
      ),
      Loss_Ratio_Paid_Net = ifelse(
        Net_Earned_Premium > 0,
        Paid_Claims_Net / Net_Earned_Premium,
        0
      )
    )

  # Add year age
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


#' Analyze reinsurance recoveries by comparing net to gross
#'
#' @param data_source Path to net data CSV file
#' @param gross_data_source Path to gross data CSV file
#' @return data.frame with RI recovery analysis
#' @export
get_ri_recovery_analysis <- function(data_source = '../../synthetic_data/rra_292_net_premium_ibnr.csv',
                                    gross_data_source = '../../synthetic_data/rra_291_gross_premium_ibnr.csv') {

  df_net <- process_rra_292(data_source)
  df_gross <- readr::read_csv(gross_data_source, show_col_types = FALSE)

  # Merge on key dimensions
  df_merged <- df_net %>%
    left_join(
      df_gross %>%
        select(Syndicate_Number, Year_of_Account, LOB_Code,
               Gross_Written_Premium, Gross_Earned_Premium,
               Paid_Claims_Gross, Case_Reserves_Gross, IBNR_Best_Estimate),
      by = c('Syndicate_Number', 'Year_of_Account', 'LOB_Code')
    )

  # Calculate RI recoveries
  df_merged <- df_merged %>%
    mutate(
      RI_Written_Premium = Gross_Written_Premium - Net_Written_Premium,
      RI_Earned_Premium = Gross_Earned_Premium - Net_Earned_Premium,
      RI_Paid_Recovery = Paid_Claims_Gross - Paid_Claims_Net,
      RI_Case_Reserve_Recovery = Case_Reserves_Gross - Case_Reserves_Net,
      RI_IBNR_Recovery = IBNR_Best_Estimate - IBNR_Best_Estimate_Net
    )

  # Calculate RI ratios
  df_merged <- df_merged %>%
    mutate(
      RI_Cession_Ratio = ifelse(
        Gross_Written_Premium > 0,
        RI_Written_Premium / Gross_Written_Premium,
        0
      ),
      RI_Recovery_Ratio = ifelse(
        Paid_Claims_Gross > 0,
        RI_Paid_Recovery / Paid_Claims_Gross,
        0
      )
    )

  return(df_merged)
}


#' Generate Net Premium and IBNR summary by Year of Account
#'
#' @param data_source Path to the data CSV file
#' @return data.frame with summary by Year of Account
#' @export
get_net_summary_by_yoa <- function(data_source = '../../synthetic_data/rra_292_net_premium_ibnr.csv') {

  df <- process_rra_292(data_source)

  summary <- df %>%
    group_by(Year_of_Account) %>%
    summarise(
      Net_Written_Premium = sum(Net_Written_Premium, na.rm = TRUE),
      Net_Earned_Premium = sum(Net_Earned_Premium, na.rm = TRUE),
      Paid_Claims_Net = sum(Paid_Claims_Net, na.rm = TRUE),
      Case_Reserves_Net = sum(Case_Reserves_Net, na.rm = TRUE),
      IBNR_Best_Estimate_Net = sum(IBNR_Best_Estimate_Net, na.rm = TRUE),
      IBNR_High_Net = sum(IBNR_High_Net, na.rm = TRUE),
      IBNR_Low_Net = sum(IBNR_Low_Net, na.rm = TRUE),
      Total_Incurred_Net = sum(Total_Incurred_Net, na.rm = TRUE),
      Ultimate_Loss_Ratio = mean(Ultimate_Loss_Ratio, na.rm = TRUE),
      .groups = 'drop'
    )

  # Calculate aggregated metrics
  summary <- summary %>%
    mutate(
      Loss_Ratio_Net = ifelse(
        Net_Earned_Premium > 0,
        Total_Incurred_Net / Net_Earned_Premium,
        0
      ),
      IBNR_to_Premium_Ratio = ifelse(
        Net_Earned_Premium > 0,
        IBNR_Best_Estimate_Net / Net_Earned_Premium,
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
      Net_Written_Premium_M = Net_Written_Premium / 1000000,
      Net_Earned_Premium_M = Net_Earned_Premium / 1000000,
      Paid_Claims_Net_M = Paid_Claims_Net / 1000000,
      Case_Reserves_Net_M = Case_Reserves_Net / 1000000,
      IBNR_Best_Estimate_Net_M = IBNR_Best_Estimate_Net / 1000000,
      IBNR_High_Net_M = IBNR_High_Net / 1000000,
      IBNR_Low_Net_M = IBNR_Low_Net / 1000000,
      Total_Incurred_Net_M = Total_Incurred_Net / 1000000
    ) %>%
    select(-c(Net_Written_Premium, Net_Earned_Premium, Paid_Claims_Net,
              Case_Reserves_Net, IBNR_Best_Estimate_Net, IBNR_High_Net,
              IBNR_Low_Net, Total_Incurred_Net))

  # Round to 2 decimal places
  summary <- summary %>%
    mutate(across(where(is.numeric), ~round(.x, 2)))

  return(summary)
}


#' Generate Net Premium and IBNR summary by Line of Business
#'
#' @param data_source Path to the data CSV file
#' @return data.frame with summary by LOB
#' @export
get_net_summary_by_lob <- function(data_source = '../../synthetic_data/rra_292_net_premium_ibnr.csv') {

  df <- process_rra_292(data_source)

  summary <- df %>%
    group_by(LOB_Code) %>%
    summarise(
      Net_Written_Premium = sum(Net_Written_Premium, na.rm = TRUE),
      Net_Earned_Premium = sum(Net_Earned_Premium, na.rm = TRUE),
      Paid_Claims_Net = sum(Paid_Claims_Net, na.rm = TRUE),
      Case_Reserves_Net = sum(Case_Reserves_Net, na.rm = TRUE),
      IBNR_Best_Estimate_Net = sum(IBNR_Best_Estimate_Net, na.rm = TRUE),
      IBNR_High_Net = sum(IBNR_High_Net, na.rm = TRUE),
      IBNR_Low_Net = sum(IBNR_Low_Net, na.rm = TRUE),
      Total_Incurred_Net = sum(Total_Incurred_Net, na.rm = TRUE),
      Ultimate_Loss_Ratio = mean(Ultimate_Loss_Ratio, na.rm = TRUE),
      IBNR_Ratio = mean(IBNR_Ratio, na.rm = TRUE),
      .groups = 'drop'
    )

  # Calculate aggregated metrics
  summary <- summary %>%
    mutate(
      Loss_Ratio_Net = ifelse(
        Net_Earned_Premium > 0,
        Total_Incurred_Net / Net_Earned_Premium,
        0
      )
    )

  # Convert to millions
  summary <- summary %>%
    mutate(
      Net_Written_Premium_M = Net_Written_Premium / 1000000,
      Net_Earned_Premium_M = Net_Earned_Premium / 1000000,
      Paid_Claims_Net_M = Paid_Claims_Net / 1000000,
      Case_Reserves_Net_M = Case_Reserves_Net / 1000000,
      IBNR_Best_Estimate_Net_M = IBNR_Best_Estimate_Net / 1000000,
      IBNR_High_Net_M = IBNR_High_Net / 1000000,
      IBNR_Low_Net_M = IBNR_Low_Net / 1000000,
      Total_Incurred_Net_M = Total_Incurred_Net / 1000000
    ) %>%
    select(-c(Net_Written_Premium, Net_Earned_Premium, Paid_Claims_Net,
              Case_Reserves_Net, IBNR_Best_Estimate_Net, IBNR_High_Net,
              IBNR_Low_Net, Total_Incurred_Net))

  # Round to 2 decimal places
  summary <- summary %>%
    mutate(across(where(is.numeric), ~round(.x, 2)))

  return(summary)
}


#' Compare net (Form 292) vs gross (Form 291) metrics
#'
#' @param net_data_source Path to net data CSV file
#' @param gross_data_source Path to gross data CSV file
#' @return data.frame with comparison analysis
#' @export
compare_net_vs_gross <- function(net_data_source = '../../synthetic_data/rra_292_net_premium_ibnr.csv',
                                gross_data_source = '../../synthetic_data/rra_291_gross_premium_ibnr.csv') {

  df_net <- process_rra_292(net_data_source)
  df_gross <- readr::read_csv(gross_data_source, show_col_types = FALSE)

  # Aggregate both
  net_agg <- df_net %>%
    group_by(Year_of_Account, LOB_Code) %>%
    summarise(
      Net_Earned_Premium = sum(Net_Earned_Premium, na.rm = TRUE),
      Total_Incurred_Net = sum(Total_Incurred_Net, na.rm = TRUE),
      .groups = 'drop'
    )

  gross_agg <- df_gross %>%
    group_by(Year_of_Account, LOB_Code) %>%
    summarise(
      Gross_Earned_Premium = sum(Gross_Earned_Premium, na.rm = TRUE),
      Paid_Claims_Gross = sum(Paid_Claims_Gross, na.rm = TRUE),
      Case_Reserves_Gross = sum(Case_Reserves_Gross, na.rm = TRUE),
      IBNR_Best_Estimate = sum(IBNR_Best_Estimate, na.rm = TRUE),
      .groups = 'drop'
    ) %>%
    mutate(
      Total_Incurred_Gross = Paid_Claims_Gross + Case_Reserves_Gross + IBNR_Best_Estimate
    )

  # Merge
  comparison <- net_agg %>%
    full_join(gross_agg, by = c('Year_of_Account', 'LOB_Code'))

  # Calculate RI impact
  comparison <- comparison %>%
    mutate(
      RI_Premium_Ceded = Gross_Earned_Premium - Net_Earned_Premium,
      RI_Claims_Recovered = Total_Incurred_Gross - Total_Incurred_Net,
      Net_Retention_Ratio = ifelse(
        Gross_Earned_Premium > 0,
        Net_Earned_Premium / Gross_Earned_Premium,
        0
      ),
      RI_Loss_Ratio_Benefit = ifelse(
        Gross_Earned_Premium > 0,
        (Total_Incurred_Gross / Gross_Earned_Premium) -
        (Total_Incurred_Net / Net_Earned_Premium),
        0
      )
    )

  return(comparison)
}


# Main execution for testing
if (sys.nframe() == 0) {
  cat("Processing RRA 292 Net Premium and IBNR Data...\n")

  tryCatch({
    df <- process_rra_292()
    cat(sprintf("\nProcessed %d records\n", nrow(df)))

    cat("\n", rep("=", 80), "\n", sep = "")
    cat("Net Premium and IBNR Summary by Year of Account:\n")
    cat(rep("=", 80), "\n", sep = "")
    print(get_net_summary_by_yoa())

    cat("\n", rep("=", 80), "\n", sep = "")
    cat("Net Premium and IBNR Summary by Line of Business:\n")
    cat(rep("=", 80), "\n", sep = "")
    print(get_net_summary_by_lob())

    cat("\n", rep("=", 80), "\n", sep = "")
    cat("RI Recovery Analysis (Sample):\n")
    cat(rep("=", 80), "\n", sep = "")
    ri_analysis <- get_ri_recovery_analysis()
    print(head(ri_analysis[, c('Year_of_Account', 'LOB_Code', 'RI_Cession_Ratio', 'RI_Recovery_Ratio')], 10))
  }, error = function(e) {
    cat("Note: Synthetic data file not found. Generate with generate_synthetic_lloyds_data.R\n")
  })
}
