# Unified Form Processor for RRQ and RRA Data
# Automatically detects and processes both quarterly and annual Lloyd's returns
# R port of python_scripts/forms/unified_form_processor.py

library(R6)
library(dplyr)
library(tidyr)
library(readr)


#' UnifiedFormProcessor R6 Class
#'
#' Process Lloyd's forms with automatic RRQ/RRA detection
#'
#' @export
UnifiedFormProcessor <- R6::R6Class(
  "UnifiedFormProcessor",

  public = list(
    #' @field data_source Path to data file or directory
    data_source = NULL,

    #' @field return_type Detected return type ('RRQ' or 'RRA')
    return_type = NULL,

    #' @field reporting_quarter Reporting quarter (for RRQ)
    reporting_quarter = NULL,

    #' @field reporting_year Reporting year
    reporting_year = NULL,

    #' Initialize processor with data source
    #'
    #' @param data_source Path to CSV data file or directory containing multiple files
    initialize = function(data_source) {
      self$data_source <- data_source
      self$return_type <- NULL
      self$reporting_quarter <- NULL
      self$reporting_year <- NULL
    },

    #' Process Form 193 (Net Claims Development) for RRQ or RRA
    #'
    #' @param data_source Override default data source
    #' @return data.frame with processed claims development data
    process_form_193 = function(data_source = NULL) {
      # Load data
      if (!is.null(data_source)) {
        df <- readr::read_csv(data_source, show_col_types = FALSE)
      } else {
        df <- readr::read_csv(self$data_source, show_col_types = FALSE)
      }

      # Detect return type
      meta <- private$detect_return_type(df)
      self$return_type <- meta$return_type
      self$reporting_quarter <- meta$reporting_quarter
      self$reporting_year <- meta$reporting_year

      # Calculate key metrics (same for both RRQ and RRA)
      df <- df %>%
        mutate(
          Incurred_Claims = Cumulative_Paid_Claims + Case_Reserves + IBNR_Reserve
        )

      # Calculate loss ratio
      df <- df %>%
        mutate(
          Loss_Ratio_Net = ifelse(
            Net_Premium_Written > 0,
            Total_Incurred / Net_Premium_Written,
            0
          )
        )

      # Sort for development factor calculations
      df <- df %>%
        arrange(Syndicate_Number, Year_of_Account, LOB_Code, Development_Year)

      # Calculate development factors
      df <- df %>%
        group_by(Syndicate_Number, Year_of_Account, LOB_Code) %>%
        mutate(
          Prior_Cumulative_Paid = lag(Cumulative_Paid_Claims, 1),
          Paid_Development_Factor = ifelse(
            !is.na(Prior_Cumulative_Paid) & Prior_Cumulative_Paid > 0,
            Cumulative_Paid_Claims / Prior_Cumulative_Paid,
            NA_real_
          )
        ) %>%
        ungroup()

      # Calculate reserve ratios
      df <- df %>%
        mutate(
          Case_Reserve_Ratio = ifelse(
            Total_Incurred > 0,
            Case_Reserves / Total_Incurred,
            0
          ),
          IBNR_Ratio = ifelse(
            Total_Incurred > 0,
            IBNR_Reserve / Total_Incurred,
            0
          ),
          Paid_Ratio = ifelse(
            Total_Incurred > 0,
            Cumulative_Paid_Claims / Total_Incurred,
            0
          )
        )

      # Add maturity indicators
      df <- df %>%
        mutate(
          Maturity_Years = Development_Year,
          Is_Mature = Development_Year >= 3
        )

      # Average claim amounts
      df <- df %>%
        mutate(
          Average_Paid_Per_Claim = ifelse(
            Number_of_Claims_Closed > 0,
            Cumulative_Paid_Claims / Number_of_Claims_Closed,
            0
          )
        )

      # Add return type specific fields
      df <- df %>%
        mutate(
          Data_Scope = meta$return_type,
          Quarterly_Period = if (meta$is_quarterly) {
            paste(meta$reporting_quarter, meta$reporting_year)
          } else {
            'Annual'
          }
        )

      return(df)
    },

    #' Process Form 291 (Gross Premium and IBNR) for RRQ or RRA
    #'
    #' @param data_source Override default data source
    #' @return data.frame with processed IBNR data
    process_form_291 = function(data_source = NULL) {
      # Load data
      if (!is.null(data_source)) {
        df <- readr::read_csv(data_source, show_col_types = FALSE)
      } else {
        df <- readr::read_csv(self$data_source, show_col_types = FALSE)
      }

      # Detect return type
      meta <- private$detect_return_type(df)

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

      # Calculate loss ratios
      df <- df %>%
        mutate(
          Loss_Ratio_Incurred = ifelse(
            Gross_Earned_Premium > 0,
            Total_Incurred_Gross / Gross_Earned_Premium,
            0
          )
        )

      # Add return type context
      df <- df %>%
        mutate(
          Data_Scope = meta$return_type
        )

      if (meta$is_quarterly) {
        df <- df %>%
          mutate(
            Quarterly_Period = paste(meta$reporting_quarter, meta$reporting_year)
          )
      }

      return(df)
    },

    #' Compare current quarter vs prior quarter (RRQ only)
    #'
    #' @param current_data Path to current quarter data
    #' @param prior_data Path to prior quarter data
    #' @param form Form number to compare ('193', '291', etc.)
    #' @return data.frame with quarter-over-quarter movement analysis
    compare_quarters = function(current_data, prior_data, form = '193') {
      # Load data
      current <- readr::read_csv(current_data, show_col_types = FALSE)
      prior <- readr::read_csv(prior_data, show_col_types = FALSE)

      # Verify both are RRQ
      current_meta <- private$detect_return_type(current)
      prior_meta <- private$detect_return_type(prior)

      if (!(current_meta$is_quarterly && prior_meta$is_quarterly)) {
        stop("Both datasets must be RRQ for quarter comparison")
      }

      # Merge on key dimensions
      key_cols <- c('Syndicate_Number', 'Year_of_Account', 'LOB_Code', 'Development_Year')
      available_keys <- intersect(
        intersect(key_cols, names(current)),
        names(prior)
      )

      comparison <- current %>%
        full_join(
          prior,
          by = available_keys,
          suffix = c('_Current', '_Prior')
        )

      # Calculate movements for Form 193
      if (form == '193') {
        comparison <- comparison %>%
          mutate(
            Paid_Movement = coalesce(Cumulative_Paid_Claims_Current, 0) -
                           coalesce(Cumulative_Paid_Claims_Prior, 0),
            IBNR_Movement = coalesce(IBNR_Reserve_Current, 0) -
                           coalesce(IBNR_Reserve_Prior, 0),
            Total_Incurred_Movement = coalesce(Total_Incurred_Current, 0) -
                                     coalesce(Total_Incurred_Prior, 0)
          )

        # Flag significant movements (>10% change)
        comparison <- comparison %>%
          mutate(
            Significant_Movement = abs(
              Total_Incurred_Movement / coalesce(Total_Incurred_Prior, 1)
            ) > 0.10
          )

      } else if (form == '291') {
        comparison <- comparison %>%
          mutate(
            IBNR_Movement = coalesce(IBNR_Best_Estimate_Current, 0) -
                           coalesce(IBNR_Best_Estimate_Prior, 0),
            Premium_Movement = coalesce(Gross_Written_Premium_Current, 0) -
                             coalesce(Gross_Written_Premium_Prior, 0)
          )
      }

      # Add quarter labels
      comparison <- comparison %>%
        mutate(
          Current_Quarter = paste(current_meta$reporting_quarter, current_meta$reporting_year),
          Prior_Quarter = paste(prior_meta$reporting_quarter, prior_meta$reporting_year)
        )

      return(comparison)
    }
  ),

  private = list(
    #' Automatically detect if data is RRQ or RRA
    #'
    #' @param df data.frame to analyze
    #' @return list with detection results
    detect_return_type = function(df) {
      if ('Return_Type' %in% names(df)) {
        return_type <- df$Return_Type[1]
        reporting_quarter <- if ('Reporting_Quarter' %in% names(df)) df$Reporting_Quarter[1] else 'N/A'
        reporting_year <- if ('Reporting_Year' %in% names(df)) df$Reporting_Year[1] else 2024

        list(
          return_type = return_type,
          reporting_quarter = if (reporting_quarter != 'N/A') reporting_quarter else NULL,
          reporting_year = if (!is.na(reporting_year)) as.integer(reporting_year) else NULL,
          is_quarterly = return_type == 'RRQ',
          is_annual = return_type == 'RRA'
        )
      } else {
        # Legacy data without Return_Type field - assume RRA
        list(
          return_type = 'RRA',
          reporting_quarter = NULL,
          reporting_year = NULL,
          is_quarterly = FALSE,
          is_annual = TRUE
        )
      }
    }
  )
)


#' Convenience function to process any RRQ or RRA form
#'
#' @param data_path Path to data file
#' @param form_number Form number ('193', '291', etc.)
#' @return data.frame with processed data
#'
#' @examples
#' \dontrun{
#' df <- process_unified_rrq_rra('rrq_193_net_claims.csv', '193')
#' print(df$Data_Scope[1])  # 'RRQ' or 'RRA'
#' }
#' @export
process_unified_rrq_rra <- function(data_path, form_number) {
  processor <- UnifiedFormProcessor$new(data_path)

  if (form_number == '193') {
    return(processor$process_form_193())
  } else if (form_number == '291') {
    return(processor$process_form_291())
  } else {
    stop(sprintf("Form %s not yet supported in unified processor", form_number))
  }
}


# Power BI usage example
# In Power BI R script:
#
# source('C:/path/to/r_scripts/forms/unified_form_processor.R')
#
# # Automatically detects RRQ vs RRA
# df <- process_unified_rrq_rra(
#   'C:/path/to/data/rrq_193_net_claims.csv',
#   '193'
# )
#
# # df will have 'Data_Scope' column showing 'RRQ' or 'RRA'
# # df will have 'Quarterly_Period' showing quarter for RRQ data


# Main execution for testing
if (sys.nframe() == 0) {
  # Test with RRA data
  cat("Testing with RRA data...\n")
  cat(rep("=", 70), "\n", sep = "")

  tryCatch({
    processor_rra <- UnifiedFormProcessor$new('../../synthetic_data_rra_2024/rra_193_net_claims.csv')
    df_rra <- processor_rra$process_form_193()
    cat(sprintf("Processed RRA Form 193: %d records\n", nrow(df_rra)))
    cat(sprintf("Return Type: %s\n", df_rra$Data_Scope[1]))
    cat(sprintf("Years of Account: %s\n", paste(sort(unique(df_rra$Year_of_Account)), collapse = ", ")))
    cat(sprintf("Development Years: 0-%d\n", max(df_rra$Development_Year)))
  }, error = function(e) {
    cat(sprintf("RRA test failed: %s\n", e$message))
  })

  cat("\n", rep("=", 70), "\n", sep = "")
  cat("Testing with RRQ data...\n")
  cat(rep("=", 70), "\n", sep = "")

  tryCatch({
    processor_rrq <- UnifiedFormProcessor$new('../../synthetic_data_rrq_2024_q2/rrq_193_net_claims.csv')
    df_rrq <- processor_rrq$process_form_193()
    cat(sprintf("Processed RRQ Form 193: %d records\n", nrow(df_rrq)))
    cat(sprintf("Return Type: %s\n", df_rrq$Data_Scope[1]))
    cat(sprintf("Quarter: %s\n", df_rrq$Quarterly_Period[1]))
    cat(sprintf("Years of Account: %s\n", paste(sort(unique(df_rrq$Year_of_Account)), collapse = ", ")))
    cat(sprintf("Development Years: 0-%d\n", max(df_rrq$Development_Year)))

    # Show data reduction
    cat("\n", rep("=", 70), "\n", sep = "")
    cat("RRQ vs RRA Data Comparison:\n")
    cat(rep("=", 70), "\n", sep = "")
    cat(sprintf("RRA records: %d\n", nrow(df_rra)))
    cat(sprintf("RRQ records: %d\n", nrow(df_rrq)))
    cat(sprintf("Reduction: %.1f%%\n", (1 - nrow(df_rrq)/nrow(df_rra))*100))
  }, error = function(e) {
    cat(sprintf("RRQ test failed: %s\n", e$message))
  })

  # Test quarter comparison
  cat("\n", rep("=", 70), "\n", sep = "")
  cat("Testing Quarter Comparison (Q1 vs Q2)...\n")
  cat(rep("=", 70), "\n", sep = "")

  tryCatch({
    processor <- UnifiedFormProcessor$new('.')
    comparison <- processor$compare_quarters(
      current_data = '../../synthetic_data_rrq_2024_q2/rrq_193_net_claims.csv',
      prior_data = '../../synthetic_data_rrq_2024_q1/rrq_193_net_claims.csv',
      form = '193'
    )
    cat(sprintf("Comparison records: %d\n", nrow(comparison)))
    cat(sprintf("Significant movements: %d\n", sum(comparison$Significant_Movement, na.rm = TRUE)))
  }, error = function(e) {
    cat(sprintf("Comparison test failed: %s\n", e$message))
  })
}
