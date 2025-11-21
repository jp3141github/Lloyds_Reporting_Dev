# RRA 010 Control Form - Power BI R Script
# This script processes and validates RRA 010 Control data for Power BI reporting

library(dplyr)
library(lubridate)
library(readr)

#' Process RRA 010 Control data for Power BI
#'
#' @param data_source Path to the control data CSV file
#' @return Processed control data ready for Power BI visualization
process_rra_010 <- function(data_source = "../../synthetic_data/rra_010_control.csv") {

  # Load data
  df <- read_csv(data_source, show_col_types = FALSE)

  # Add calculated fields
  df <- df %>%
    mutate(
      Capacity_Millions = Capacity_GBP / 1000000,
      YoA_Range = Final_Pure_YoA - First_Pure_YoA + 1,
      Is_Active = Status %in% c("Submitted", "Approved"),

      # Add submission year
      Submission_Year = year(as.Date(Submission_Date)),

      # Calculate days since submission
      Days_Since_Submission = as.numeric(difftime(Sys.Date(),
                                                   as.Date(Submission_Date),
                                                   units = "days")),

      # Add status priority for sorting
      Status_Priority = case_when(
        Status == "Draft" ~ 1,
        Status == "Submitted" ~ 2,
        Status == "Approved" ~ 3,
        TRUE ~ 0
      )
    )

  return(df)
}


#' Generate summary statistics for RRA 010 Control
#'
#' @param data_source Path to the control data CSV file
#' @return Summary statistics dataframe
get_control_summary <- function(data_source = "../../synthetic_data/rra_010_control.csv") {

  df <- process_rra_010(data_source)

  summary <- data.frame(
    Metric = c(
      "Total Syndicates",
      "Total Capacity (GBP M)",
      "Average Capacity (GBP M)",
      "Syndicates Submitted",
      "Syndicates Approved",
      "Average YoA Range"
    ),
    Value = c(
      nrow(df),
      sum(df$Capacity_GBP) / 1000000,
      mean(df$Capacity_GBP) / 1000000,
      sum(df$Status == "Submitted"),
      sum(df$Status == "Approved"),
      mean(df$YoA_Range)
    ),
    stringsAsFactors = FALSE
  )

  summary$Value <- round(summary$Value, 2)

  return(summary)
}


#' Validate RRA 010 Control data
#'
#' @param data_source Path to the control data CSV file
#' @return Validation results dataframe
validate_rra_010 <- function(data_source = "../../synthetic_data/rra_010_control.csv") {

  df <- read_csv(data_source, show_col_types = FALSE)

  validations <- list()

  # Check for missing syndicate numbers
  missing_synd <- sum(is.na(df$Syndicate_Number))
  validations[[1]] <- data.frame(
    Rule = "Syndicate Number Required",
    Status = ifelse(missing_synd == 0, "PASS", "FAIL"),
    Records_Affected = missing_synd,
    stringsAsFactors = FALSE
  )

  # Check for valid email addresses
  invalid_emails <- sum(!grepl("@", df$Contact_Email, fixed = TRUE))
  validations[[2]] <- data.frame(
    Rule = "Valid Email Address",
    Status = ifelse(invalid_emails == 0, "PASS", "FAIL"),
    Records_Affected = invalid_emails,
    stringsAsFactors = FALSE
  )

  # Check that First YoA <= Final YoA
  invalid_yoa <- sum(df$First_Pure_YoA > df$Final_Pure_YoA, na.rm = TRUE)
  validations[[3]] <- data.frame(
    Rule = "First YoA <= Final YoA",
    Status = ifelse(invalid_yoa == 0, "PASS", "FAIL"),
    Records_Affected = invalid_yoa,
    stringsAsFactors = FALSE
  )

  # Check capacity is positive
  invalid_capacity <- sum(df$Capacity_GBP <= 0, na.rm = TRUE)
  validations[[4]] <- data.frame(
    Rule = "Capacity > 0",
    Status = ifelse(invalid_capacity == 0, "PASS", "FAIL"),
    Records_Affected = invalid_capacity,
    stringsAsFactors = FALSE
  )

  validation_df <- do.call(rbind, validations)

  return(validation_df)
}


# For use in Power BI - the 'dataset' variable will be provided by Power BI
# Uncomment the following line when using in Power BI:
# df <- process_rra_010()
# The processed dataframe 'df' will be available for visualization in Power BI


# Test the functions if run directly
if (interactive() || !exists("dataset")) {
  cat("Processing RRA 010 Control Data...\n")
  df <- process_rra_010()
  cat(sprintf("\nProcessed %d records\n", nrow(df)))
  cat("\nSample data:\n")
  print(head(df))

  cat("\n", rep("=", 60), "\n", sep = "")
  cat("Control Summary:\n")
  cat(rep("=", 60), "\n", sep = "")
  print(get_control_summary())

  cat("\n", rep("=", 60), "\n", sep = "")
  cat("Validation Results:\n")
  cat(rep("=", 60), "\n", sep = "")
  print(validate_rra_010())
}
