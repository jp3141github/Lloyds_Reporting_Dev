# RRA Aggregator - Combine and aggregate all RRA forms (R Version)
# This script provides functions to load and combine all RRA forms for comprehensive reporting

library(dplyr)
library(tidyr)
library(readr)
library(purrr)

#' RRA Data Aggregator Class
#'
#' Aggregates all RRA form data for comprehensive reporting
rra_load_all_forms <- function(data_dir = "../../synthetic_data") {

  form_files <- list(
    control = "rra_010_control.csv",
    exchange_rates = "rra_020_exchange_rates.csv",
    scob_mapping = "rra_071_scob_mapping.csv",
    reserving_class_info = "rra_081_reserving_class_info.csv",
    lpt = "rra_091_lpt.csv",
    net_claims = "rra_193_net_claims.csv",
    gross_premium_ibnr = "rra_291_gross_premium_ibnr.csv",
    net_premium_ibnr = "rra_292_net_premium_ibnr.csv",
    os_ibnr_pyoa = "rra_293_os_ibnr_pyoa.csv",
    cat_ibnr = "rra_294_cat_ibnr.csv",
    ulae = "rra_295_ulae.csv",
    ielr = "rra_391_ielr.csv",
    additional_info = "rra_910_additional_info.csv",
    validation = "rra_990_validation.csv"
  )

  forms <- list()

  for (form_name in names(form_files)) {
    file_path <- file.path(data_dir, form_files[[form_name]])

    if (file.exists(file_path)) {
      forms[[form_name]] <- read_csv(file_path, show_col_types = FALSE)
      cat(sprintf("✓ Loaded %s: %d records\n", form_name, nrow(forms[[form_name]])))
    } else {
      cat(sprintf("✗ Warning: %s not found\n", form_files[[form_name]]))
    }
  }

  return(forms)
}


#' Generate overall portfolio summary across all forms
#'
#' @param forms List of loaded RRA forms
#' @return Portfolio summary dataframe
get_portfolio_summary <- function(forms) {

  summary_data <- list()

  # Control data summary
  if ("control" %in% names(forms)) {
    control <- forms$control

    summary_data <- append(summary_data, list(
      data.frame(
        Category = "Portfolio Overview",
        Metric = "Total Syndicates",
        Value = nrow(control),
        Unit = "count",
        stringsAsFactors = FALSE
      ),
      data.frame(
        Category = "Portfolio Overview",
        Metric = "Total Capacity",
        Value = sum(control$Capacity_GBP) / 1000000,
        Unit = "GBP M",
        stringsAsFactors = FALSE
      )
    ))
  }

  # Gross Premium and IBNR summary
  if ("gross_premium_ibnr" %in% names(forms)) {
    gross <- forms$gross_premium_ibnr

    summary_data <- append(summary_data, list(
      data.frame(
        Category = "Gross Premium",
        Metric = "Total Gross Written Premium",
        Value = sum(gross$Gross_Written_Premium) / 1000000,
        Unit = "GBP M",
        stringsAsFactors = FALSE
      ),
      data.frame(
        Category = "Gross Premium",
        Metric = "Total Gross Earned Premium",
        Value = sum(gross$Gross_Earned_Premium) / 1000000,
        Unit = "GBP M",
        stringsAsFactors = FALSE
      ),
      data.frame(
        Category = "IBNR Reserves",
        Metric = "Total IBNR (Best Estimate)",
        Value = sum(gross$IBNR_Best_Estimate) / 1000000,
        Unit = "GBP M",
        stringsAsFactors = FALSE
      ),
      data.frame(
        Category = "Loss Ratios",
        Metric = "Average Ultimate Loss Ratio",
        Value = mean(gross$Ultimate_Loss_Ratio),
        Unit = "ratio",
        stringsAsFactors = FALSE
      )
    ))
  }

  # Net Premium and IBNR summary
  if ("net_premium_ibnr" %in% names(forms)) {
    net <- forms$net_premium_ibnr

    summary_data <- append(summary_data, list(
      data.frame(
        Category = "Net Premium",
        Metric = "Total Net Written Premium",
        Value = sum(net$Net_Written_Premium) / 1000000,
        Unit = "GBP M",
        stringsAsFactors = FALSE
      ),
      data.frame(
        Category = "Net Premium",
        Metric = "Total Net Earned Premium",
        Value = sum(net$Net_Earned_Premium) / 1000000,
        Unit = "GBP M",
        stringsAsFactors = FALSE
      )
    ))
  }

  # Catastrophe summary
  if ("cat_ibnr" %in% names(forms)) {
    cat_data <- forms$cat_ibnr

    summary_data <- append(summary_data, list(
      data.frame(
        Category = "Catastrophe Losses",
        Metric = "Total Cat Events",
        Value = nrow(cat_data),
        Unit = "count",
        stringsAsFactors = FALSE
      ),
      data.frame(
        Category = "Catastrophe Losses",
        Metric = "Total Gross Cat Losses",
        Value = sum(cat_data$Gross_Incurred_Loss) / 1000000,
        Unit = "GBP M",
        stringsAsFactors = FALSE
      ),
      data.frame(
        Category = "Catastrophe Losses",
        Metric = "Total Net Cat Losses",
        Value = sum(cat_data$Net_Cat_Loss) / 1000000,
        Unit = "GBP M",
        stringsAsFactors = FALSE
      )
    ))
  }

  # ULAE summary
  if ("ulae" %in% names(forms)) {
    ulae <- forms$ulae

    summary_data <- append(summary_data, list(
      data.frame(
        Category = "ULAE",
        Metric = "Total ULAE Reserves",
        Value = sum(ulae$ULAE_Reserve) / 1000000,
        Unit = "GBP M",
        stringsAsFactors = FALSE
      )
    ))
  }

  # LPT summary
  if ("lpt" %in% names(forms)) {
    lpt <- forms$lpt

    summary_data <- append(summary_data, list(
      data.frame(
        Category = "LPT",
        Metric = "Total LPT Transfer Amount",
        Value = sum(lpt$Transfer_Amount_GBP) / 1000000,
        Unit = "GBP M",
        stringsAsFactors = FALSE
      )
    ))
  }

  df <- do.call(rbind, summary_data)
  df$Value <- round(df$Value, 2)

  return(df)
}


#' Get comprehensive profile for a specific syndicate
#'
#' @param forms List of loaded RRA forms
#' @param syndicate_number Syndicate number to profile
#' @return Syndicate profile dataframe
get_syndicate_profile <- function(forms, syndicate_number) {

  profile <- list(Syndicate_Number = syndicate_number)

  # Control info
  if ("control" %in% names(forms)) {
    control <- forms$control %>%
      filter(Syndicate_Number == syndicate_number)

    if (nrow(control) > 0) {
      profile$Managing_Agent <- control$Managing_Agent_Name[1]
      profile$Status <- control$Status[1]
      profile$Capacity_GBP_M <- control$Capacity_GBP[1] / 1000000
      profile$First_YoA <- control$First_Pure_YoA[1]
      profile$Final_YoA <- control$Final_Pure_YoA[1]
    }
  }

  # Premium data
  if ("gross_premium_ibnr" %in% names(forms)) {
    gross <- forms$gross_premium_ibnr %>%
      filter(Syndicate_Number == syndicate_number)

    if (nrow(gross) > 0) {
      profile$Total_GWP_M <- sum(gross$Gross_Written_Premium) / 1000000
      profile$Total_IBNR_M <- sum(gross$IBNR_Best_Estimate) / 1000000
      profile$Avg_Loss_Ratio <- mean(gross$Ultimate_Loss_Ratio)
    }
  }

  # Classes of business
  if ("scob_mapping" %in% names(forms)) {
    scob <- forms$scob_mapping %>%
      filter(Syndicate_Number == syndicate_number)

    profile$Number_of_Classes <- nrow(scob)
    profile$Classes_of_Business <- paste(unique(scob$LOB_Code), collapse = ", ")
  }

  return(as.data.frame(profile))
}


#' Analyze performance across all lines of business
#'
#' @param forms List of loaded RRA forms
#' @return LOB analysis dataframe
get_lob_analysis <- function(forms) {

  if (!"gross_premium_ibnr" %in% names(forms)) {
    return(data.frame())
  }

  gross <- forms$gross_premium_ibnr

  lob_analysis <- gross %>%
    group_by(LOB_Code) %>%
    summarise(
      Gross_Written_Premium_M = sum(Gross_Written_Premium) / 1000000,
      Gross_Earned_Premium_M = sum(Gross_Earned_Premium) / 1000000,
      IBNR_Best_Estimate_M = sum(IBNR_Best_Estimate) / 1000000,
      Ultimate_Loss_Ratio = mean(Ultimate_Loss_Ratio),
      Number_of_Syndicates = n_distinct(Syndicate_Number),
      .groups = "drop"
    )

  # Calculate total incurred from other forms if available
  if ("net_claims" %in% names(forms)) {
    claims <- forms$net_claims

    claims_by_lob <- claims %>%
      group_by(LOB_Code) %>%
      summarise(Total_Incurred_M = sum(Total_Incurred) / 1000000, .groups = "drop")

    lob_analysis <- lob_analysis %>%
      left_join(claims_by_lob, by = "LOB_Code")
  }

  lob_analysis <- lob_analysis %>%
    mutate(across(where(is.numeric), ~round(.x, 2)))

  return(lob_analysis)
}


#' Analyze development patterns across years of account
#'
#' @param forms List of loaded RRA forms
#' @return Development summary dataframe
get_yoa_development_summary <- function(forms) {

  if (!"ielr" %in% names(forms)) {
    return(data.frame())
  }

  ielr <- forms$ielr

  # Calculate development patterns
  dev_summary <- ielr %>%
    group_by(Year_of_Account, Development_Year) %>%
    summarise(
      Earned_Premium_M = sum(Earned_Premium) / 1000000,
      Incurred_Loss_M = sum(Incurred_Loss) / 1000000,
      Incurred_Loss_Ratio = mean(Incurred_Loss_Ratio),
      Paid_Loss_M = sum(Paid_Loss) / 1000000,
      Outstanding_Reserve_M = sum(Outstanding_Reserve) / 1000000,
      .groups = "drop"
    )

  dev_summary <- dev_summary %>%
    mutate(
      Paid_Ratio = ifelse(Incurred_Loss_M > 0,
                           Paid_Loss_M / Incurred_Loss_M,
                           0)
    )

  dev_summary <- dev_summary %>%
    mutate(across(where(is.numeric), ~round(.x, 4)))

  return(dev_summary)
}


#' Calculate reserve adequacy indicators
#'
#' @param forms List of loaded RRA forms
#' @return Reserve adequacy indicators dataframe
get_reserve_adequacy_indicators <- function(forms) {

  indicators <- list()

  # IBNR to Premium ratios
  if ("gross_premium_ibnr" %in% names(forms)) {
    gross <- forms$gross_premium_ibnr

    ibnr_to_premium <- ifelse(gross$Gross_Earned_Premium > 0,
                               gross$IBNR_Best_Estimate / gross$Gross_Earned_Premium,
                               0)

    indicators <- append(indicators, list(
      data.frame(
        Indicator = "Average IBNR to Premium Ratio",
        Value = mean(ibnr_to_premium),
        Interpretation = "Lower is better (less uncertainty)",
        stringsAsFactors = FALSE
      )
    ))

    # IBNR range as % of estimate
    ibnr_range_pct <- ifelse(gross$IBNR_Best_Estimate > 0,
                              (gross$IBNR_High - gross$IBNR_Low) / gross$IBNR_Best_Estimate,
                              0)

    indicators <- append(indicators, list(
      data.frame(
        Indicator = "Average IBNR Range %",
        Value = mean(ibnr_range_pct),
        Interpretation = "Measure of estimation uncertainty",
        stringsAsFactors = FALSE
      )
    ))
  }

  # Claims development patterns
  if ("net_claims" %in% names(forms)) {
    claims <- forms$net_claims

    # Latest development data
    latest <- claims %>%
      group_by(Syndicate_Number, Year_of_Account, LOB_Code) %>%
      slice_max(Development_Year, n = 1) %>%
      ungroup()

    paid_ratio <- ifelse(latest$Total_Incurred > 0,
                          latest$Cumulative_Paid_Claims / latest$Total_Incurred,
                          0)

    indicators <- append(indicators, list(
      data.frame(
        Indicator = "Average Paid Claims Ratio",
        Value = mean(paid_ratio),
        Interpretation = "Higher indicates more mature claims",
        stringsAsFactors = FALSE
      )
    ))
  }

  # ULAE adequacy
  if ("ulae" %in% names(forms)) {
    ulae <- forms$ulae

    indicators <- append(indicators, list(
      data.frame(
        Indicator = "Average ULAE Ratio",
        Value = mean(ulae$ULAE_Ratio),
        Interpretation = "ULAE as % of loss reserves",
        stringsAsFactors = FALSE
      )
    ))
  }

  if (length(indicators) > 0) {
    df <- do.call(rbind, indicators)
    df$Value <- round(df$Value, 4)
    return(df)
  } else {
    return(data.frame())
  }
}


# Main execution and testing
if (interactive() || !exists("dataset")) {
  cat("\n", rep("=", 80), "\n", sep = "")
  cat("RRA Data Aggregator - Testing (R Version)\n")
  cat(rep("=", 80), "\n\n", sep = "")

  forms <- rra_load_all_forms()

  cat("\n", rep("=", 80), "\n", sep = "")
  cat("Portfolio Summary:\n")
  cat(rep("=", 80), "\n", sep = "")
  print(get_portfolio_summary(forms))

  cat("\n", rep("=", 80), "\n", sep = "")
  cat("Line of Business Analysis:\n")
  cat(rep("=", 80), "\n", sep = "")
  print(get_lob_analysis(forms))

  cat("\n", rep("=", 80), "\n", sep = "")
  cat("Reserve Adequacy Indicators:\n")
  cat(rep("=", 80), "\n", sep = "")
  print(get_reserve_adequacy_indicators(forms))

  # Test syndicate profile
  if ("control" %in% names(forms) && nrow(forms$control) > 0) {
    test_syndicate <- forms$control$Syndicate_Number[1]
    cat(sprintf("\n%s\n", paste(rep("=", 80), collapse = "")))
    cat(sprintf("Sample Syndicate Profile: %d\n", test_syndicate))
    cat(sprintf("%s\n", paste(rep("=", 80), collapse = "")))
    print(get_syndicate_profile(forms, test_syndicate))
  }
}
