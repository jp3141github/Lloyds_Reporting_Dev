# RRA 990 Validation Summary Form - R Script
# This script performs cross-form validation checks across all RRA forms
# R port of python_scripts/forms/rra_990_validation.py

library(dplyr)
library(tidyr)
library(readr)


#' Perform comprehensive validation across all RRA forms
#'
#' @param data_directory Directory containing all RRA form CSV files
#' @return data.frame with validation results
#' @export
validate_all_forms <- function(data_directory = '../../synthetic_data') {

  validation_results <- list()
  idx <- 1

  # Rule 1: Check all required files exist
  required_forms <- c('010', '020', '071', '081', '091', '193', '291', '292',
                     '293', '294', '295', '391', '910')

  for (form in required_forms) {
    files <- list.files(data_directory, pattern = sprintf('rra_%s.*\\.csv', form), full.names = TRUE)

    validation_results[[idx]] <- list(
      Rule_ID = sprintf('FILE_%s', form),
      Rule_Description = sprintf('Form %s file exists', form),
      Status = if (length(files) > 0) 'PASS' else 'FAIL',
      Severity = 'Critical',
      Records_Affected = if (length(files) > 0) 0 else 1,
      Details = if (length(files) > 0) sprintf('Found %d file(s)', length(files)) else 'File not found'
    )
    idx <- idx + 1
  }

  # Rule 2: Cross-form consistency - Syndicate numbers
  tryCatch({
    df_010 <- readr::read_csv(file.path(data_directory, 'rra_010_control.csv'), show_col_types = FALSE)
    df_193 <- readr::read_csv(file.path(data_directory, 'rra_193_net_claims.csv'), show_col_types = FALSE)
    df_291 <- readr::read_csv(file.path(data_directory, 'rra_291_gross_premium_ibnr.csv'), show_col_types = FALSE)

    syndicates_010 <- unique(df_010$Syndicate_Number)
    syndicates_193 <- unique(df_193$Syndicate_Number)
    syndicates_291 <- unique(df_291$Syndicate_Number)

    # Check if all syndicates in 193 and 291 are in 010
    orphan_193 <- setdiff(syndicates_193, syndicates_010)
    orphan_291 <- setdiff(syndicates_291, syndicates_010)

    validation_results[[idx]] <- list(
      Rule_ID = 'XREF_SYN_193',
      Rule_Description = 'All syndicates in Form 193 must exist in Form 010',
      Status = if (length(orphan_193) == 0) 'PASS' else 'FAIL',
      Severity = 'High',
      Records_Affected = length(orphan_193),
      Details = if (length(orphan_193) > 0) sprintf('Orphan syndicates: %s', paste(orphan_193, collapse = ', ')) else 'All syndicates valid'
    )
    idx <- idx + 1

    validation_results[[idx]] <- list(
      Rule_ID = 'XREF_SYN_291',
      Rule_Description = 'All syndicates in Form 291 must exist in Form 010',
      Status = if (length(orphan_291) == 0) 'PASS' else 'FAIL',
      Severity = 'High',
      Records_Affected = length(orphan_291),
      Details = if (length(orphan_291) > 0) sprintf('Orphan syndicates: %s', paste(orphan_291, collapse = ', ')) else 'All syndicates valid'
    )
    idx <- idx + 1

  }, error = function(e) {
    validation_results[[idx]] <<- list(
      Rule_ID = 'XREF_SYN',
      Rule_Description = 'Cross-form syndicate validation',
      Status = 'ERROR',
      Severity = 'Critical',
      Records_Affected = 0,
      Details = as.character(e$message)
    )
    idx <<- idx + 1
  })

  # Rule 3: Net vs Gross consistency (Form 292 vs 291)
  tryCatch({
    df_291 <- readr::read_csv(file.path(data_directory, 'rra_291_gross_premium_ibnr.csv'), show_col_types = FALSE)
    df_292 <- readr::read_csv(file.path(data_directory, 'rra_292_net_premium_ibnr.csv'), show_col_types = FALSE)

    # Merge on key dimensions
    merged <- df_291 %>%
      inner_join(
        df_292,
        by = c('Syndicate_Number', 'Year_of_Account', 'LOB_Code'),
        suffix = c('_Gross', '_Net')
      )

    # Check: Net amounts should be <= Gross amounts
    invalid_premium <- merged %>% filter(Net_Written_Premium > Gross_Written_Premium)
    invalid_claims <- merged %>% filter(Paid_Claims_Net > Paid_Claims_Gross)

    validation_results[[idx]] <- list(
      Rule_ID = 'NET_LE_GROSS_PREM',
      Rule_Description = 'Net Premium must be ≤ Gross Premium',
      Status = if (nrow(invalid_premium) == 0) 'PASS' else 'FAIL',
      Severity = 'Critical',
      Records_Affected = nrow(invalid_premium),
      Details = if (nrow(invalid_premium) > 0) sprintf('%d violations found', nrow(invalid_premium)) else 'All records valid'
    )
    idx <- idx + 1

    validation_results[[idx]] <- list(
      Rule_ID = 'NET_LE_GROSS_CLAIMS',
      Rule_Description = 'Net Claims must be ≤ Gross Claims',
      Status = if (nrow(invalid_claims) == 0) 'PASS' else 'FAIL',
      Severity = 'Critical',
      Records_Affected = nrow(invalid_claims),
      Details = if (nrow(invalid_claims) > 0) sprintf('%d violations found', nrow(invalid_claims)) else 'All records valid'
    )
    idx <- idx + 1

  }, error = function(e) {
    validation_results[[idx]] <<- list(
      Rule_ID = 'NET_GROSS_CHECK',
      Rule_Description = 'Net vs Gross validation',
      Status = 'SKIPPED',
      Severity = 'High',
      Records_Affected = 0,
      Details = 'Form 291 or 292 not found'
    )
    idx <<- idx + 1
  })

  # Rule 4: IBNR range validation
  tryCatch({
    df_291 <- readr::read_csv(file.path(data_directory, 'rra_291_gross_premium_ibnr.csv'), show_col_types = FALSE)

    invalid_range <- df_291 %>%
      filter(
        (IBNR_Low > IBNR_Best_Estimate) |
        (IBNR_Best_Estimate > IBNR_High)
      )

    validation_results[[idx]] <- list(
      Rule_ID = 'IBNR_RANGE',
      Rule_Description = 'IBNR Low ≤ Best ≤ High',
      Status = if (nrow(invalid_range) == 0) 'PASS' else 'FAIL',
      Severity = 'High',
      Records_Affected = nrow(invalid_range),
      Details = if (nrow(invalid_range) > 0) sprintf('%d violations found', nrow(invalid_range)) else 'All IBNR ranges valid'
    )
    idx <- idx + 1

  }, error = function(e) {
    # Skip if file not found
  })

  # Rule 5: Data completeness - no null key fields
  form_checks <- list(
    list(form = '010', fields = c('Syndicate_Number')),
    list(form = '193', fields = c('Syndicate_Number', 'Year_of_Account', 'LOB_Code')),
    list(form = '291', fields = c('Syndicate_Number', 'Year_of_Account', 'LOB_Code'))
  )

  for (check in form_checks) {
    tryCatch({
      files <- list.files(data_directory, pattern = sprintf('rra_%s.*\\.csv', check$form), full.names = TRUE)
      if (length(files) > 0) {
        df <- readr::read_csv(files[1], show_col_types = FALSE)
        null_records <- sum(rowSums(is.na(df[, check$fields])) > 0)

        validation_results[[idx]] <- list(
          Rule_ID = sprintf('COMP_%s', check$form),
          Rule_Description = sprintf('Form %s key fields completeness', check$form),
          Status = if (null_records == 0) 'PASS' else 'FAIL',
          Severity = 'Critical',
          Records_Affected = null_records,
          Details = if (null_records > 0) sprintf('%d records with null key fields', null_records) else 'All key fields populated'
        )
        idx <- idx + 1
      }
    }, error = function(e) {
      # Skip if file not found
    })
  }

  # Convert to data frame
  df_validation <- bind_rows(validation_results)

  # Add validation timestamp
  df_validation <- df_validation %>%
    mutate(Validation_Timestamp = Sys.time())

  # Sort by severity and status
  severity_order <- c('Critical' = 0, 'High' = 1, 'Medium' = 2, 'Low' = 3)
  status_order <- c('FAIL' = 0, 'ERROR' = 1, 'PASS' = 2, 'SKIPPED' = 3)

  df_validation <- df_validation %>%
    mutate(
      Severity_Order = severity_order[Severity],
      Status_Order = status_order[Status]
    ) %>%
    arrange(Severity_Order, Status_Order) %>%
    select(-Severity_Order, -Status_Order)

  return(df_validation)
}


#' Get high-level validation summary statistics
#'
#' @param data_directory Directory containing RRA forms
#' @return list with summary statistics
#' @export
get_validation_summary <- function(data_directory = '../../synthetic_data') {

  df <- validate_all_forms(data_directory)

  summary <- list(
    Total_Rules = nrow(df),
    Rules_Passed = nrow(df %>% filter(Status == 'PASS')),
    Rules_Failed = nrow(df %>% filter(Status == 'FAIL')),
    Rules_Error = nrow(df %>% filter(Status == 'ERROR')),
    Rules_Skipped = nrow(df %>% filter(Status == 'SKIPPED')),
    Critical_Failures = nrow(df %>% filter(Status == 'FAIL', Severity == 'Critical')),
    High_Failures = nrow(df %>% filter(Status == 'FAIL', Severity == 'High')),
    Total_Records_Affected = sum(df$Records_Affected, na.rm = TRUE),
    Validation_Status = if (nrow(df %>% filter(Status == 'FAIL')) == 0) 'PASS' else 'FAIL'
  )

  return(summary)
}


#' Export validation results to CSV
#'
#' @param data_directory Directory containing RRA forms
#' @param output_file Output CSV filename
#' @return data.frame with validation results
#' @export
export_validation_report <- function(data_directory = '../../synthetic_data',
                                    output_file = 'rra_990_validation.csv') {

  df_validation <- validate_all_forms(data_directory)
  readr::write_csv(df_validation, output_file)
  cat(sprintf("Validation report exported to: %s\n", output_file))

  return(df_validation)
}


# Main execution for testing
if (sys.nframe() == 0) {
  cat("Running RRA Form 990 Validation...\n")
  cat(rep("=", 80), "\n", sep = "")

  tryCatch({
    # Run validation
    df <- validate_all_forms()

    # Print summary
    summary <- get_validation_summary()
    cat("\nValidation Summary:\n")
    cat(rep("=", 80), "\n", sep = "")
    for (name in names(summary)) {
      cat(sprintf("%s: %s\n", name, summary[[name]]))
    }

    # Print detailed results
    cat("\n", rep("=", 80), "\n", sep = "")
    cat("Detailed Validation Results:\n")
    cat(rep("=", 80), "\n", sep = "")
    print(df)

    # Export to CSV
    cat("\n", rep("=", 80), "\n", sep = "")
    export_validation_report()

  }, error = function(e) {
    cat(sprintf("Validation failed with error: %s\n", e$message))
  })
}
