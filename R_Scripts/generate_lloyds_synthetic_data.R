# Lloyd's of London Synthetic Data Generator
# ===========================================
# This script generates synthetic SCR (Solvency Capital Requirement) data
# for Lloyd's syndicates, matching the structure of the SCR SBF template.
#
# Output Tables:
# 1. scr_impact_data: Impact on uSCR and 1SCR metrics
# 2. loss_ratio_data: Plan vs Modelled loss ratios
# 3. syndicate_master: Syndicate reference data
#
# Usage:
#   source("generate_lloyds_synthetic_data.R")
#   data <- generate_all_data(num_syndicates = 20, seed = 42)

library(dplyr)
library(lubridate)


#' Set random seed for reproducibility
#'
#' @param seed Random seed value
set_random_seed <- function(seed = 42) {
  set.seed(seed)
}


#' Generate master list of Lloyd's syndicates with reference data
#'
#' @param num_syndicates Number of syndicates to generate
#' @return Data frame with syndicate reference information
generate_syndicate_master <- function(num_syndicates = 20) {

  # Realistic Lloyd's syndicate numbers
  syndicate_numbers <- c(
    2001, 2003, 2010, 2014, 2020, 2025, 2030, 2035, 2040, 2050,
    2988, 3000, 3010, 3020, 3500, 4000, 4001, 5000, 5001, 5500,
    6000, 6100, 6200, 1176, 1200, 1234, 2791, 2987, 3624, 4242
  )[1:num_syndicates]

  syndicate_names <- c(
    "Global Property & Casualty", "Marine & Energy", "Professional Indemnity",
    "Reinsurance Division", "Aviation Underwriters", "Cyber & Technology",
    "Political Risk & Credit", "Specialty Lines", "Catastrophe Re",
    "Lloyd's Core Consortium", "Treaty Reinsurance", "Casualty Direct",
    "Motor & Transport", "Trade Credit", "Medical Malpractice",
    "D&O and Financial Lines", "Property Facultative", "Energy Offshore",
    "Aerospace", "Marine Hull", "Marine Cargo", "Construction & Engineering",
    "Terrorism Re", "Parametric Solutions", "Agriculture", "Life Re",
    "Warranty & Indemnity", "Environmental Liability", "Bloodstock & Livestock",
    "Fine Art & Specie"
  )[1:num_syndicates]

  business_classes <- c(
    "Property", "Marine", "Professional Indemnity", "Reinsurance", "Aviation",
    "Cyber", "Political Risk", "Specialty", "Catastrophe", "Multi-class"
  )

  df <- data.frame(
    SyndicateNumber = syndicate_numbers,
    SyndicateName = syndicate_names,
    ManagingAgent = paste0("Managing Agent ",
                           LETTERS[(1:num_syndicates - 1) %% 26 + 1],
                           LETTERS[((1:num_syndicates - 1) %/% 26) %% 26 + 1]),
    PrimaryBusinessClass = sample(business_classes, num_syndicates, replace = TRUE),
    YearOfAccount = rep(2025, num_syndicates),
    Active = rep(TRUE, num_syndicates),
    StampCapacity_GBPm = round(runif(num_syndicates, 50, 2000), 1),
    stringsAsFactors = FALSE
  )

  return(df)
}


#' Generate SCR impact data showing uSCR and 1SCR changes
#'
#' @param syndicates_df Data frame of syndicates from generate_syndicate_master
#' @return Data frame with SCR impact metrics
generate_scr_impact_data <- function(syndicates_df) {

  records <- list()
  idx <- 1

  for (i in 1:nrow(syndicates_df)) {
    syndicate_no <- syndicates_df$SyndicateNumber[i]
    capacity <- syndicates_df$StampCapacity_GBPm[i]

    # Base SCR values (typically 35-50% of stamp capacity)
    base_uscr <- capacity * runif(1, 0.35, 0.50)
    base_1scr <- base_uscr * runif(1, 0.85, 0.95)

    # Latest LCR submission
    records[[idx]] <- data.frame(
      SyndicateNumber = syndicate_no,
      SubmissionType = "Latest LCR",
      SBFVersion = "LCR_2024_v1",
      SubmissionDate = as.Date("2024-10-15") + sample(0:30, 1),
      uSCR_GBPm = round(base_uscr, 2),
      '1SCR_GBPm' = round(base_1scr, 2),
      SCR_Ratio = round(base_1scr / base_uscr, 4),
      stringsAsFactors = FALSE,
      check.names = FALSE
    )
    idx <- idx + 1

    # Latest SBF submission
    sbf_uscr <- base_uscr * runif(1, 0.98, 1.08)
    sbf_1scr <- base_1scr * runif(1, 0.98, 1.08)

    records[[idx]] <- data.frame(
      SyndicateNumber = syndicate_no,
      SubmissionType = "Latest SBF",
      SBFVersion = "SBF_2025_v2",
      SubmissionDate = as.Date("2025-01-15") + sample(0:30, 1),
      uSCR_GBPm = round(sbf_uscr, 2),
      '1SCR_GBPm' = round(sbf_1scr, 2),
      SCR_Ratio = round(sbf_1scr / sbf_uscr, 4),
      stringsAsFactors = FALSE,
      check.names = FALSE
    )
    idx <- idx + 1

    # Movement in £
    movement_uscr <- sbf_uscr - base_uscr
    movement_1scr <- sbf_1scr - base_1scr

    records[[idx]] <- data.frame(
      SyndicateNumber = syndicate_no,
      SubmissionType = "Movement",
      SBFVersion = "Delta",
      SubmissionDate = as.Date("2025-01-15"),
      uSCR_GBPm = round(movement_uscr, 2),
      '1SCR_GBPm' = round(movement_1scr, 2),
      SCR_Ratio = ifelse(movement_uscr != 0,
                         round(movement_1scr / movement_uscr, 4),
                         0),
      stringsAsFactors = FALSE,
      check.names = FALSE
    )
    idx <- idx + 1

    # Movement %
    movement_pct_uscr <- ifelse(base_uscr != 0, (movement_uscr / base_uscr * 100), 0)
    movement_pct_1scr <- ifelse(base_1scr != 0, (movement_1scr / base_1scr * 100), 0)

    records[[idx]] <- data.frame(
      SyndicateNumber = syndicate_no,
      SubmissionType = "Movement %",
      SBFVersion = "Delta %",
      SubmissionDate = as.Date("2025-01-15"),
      uSCR_GBPm = round(movement_pct_uscr, 2),
      '1SCR_GBPm' = round(movement_pct_1scr, 2),
      SCR_Ratio = NA,
      stringsAsFactors = FALSE,
      check.names = FALSE
    )
    idx <- idx + 1
  }

  df <- do.call(rbind, records)
  return(df)
}


#' Generate loss ratio data (Plan vs Modelled, Net Net basis)
#'
#' @param syndicates_df Data frame of syndicates from generate_syndicate_master
#' @return Data frame with loss ratio validation data
generate_loss_ratio_data <- function(syndicates_df) {

  records <- list()
  idx <- 1

  # Base loss ratios by business class
  base_loss_ratios <- list(
    "Property" = c(0.65, 0.72),
    "Marine" = c(0.68, 0.75),
    "Professional Indemnity" = c(0.70, 0.78),
    "Reinsurance" = c(0.72, 0.80),
    "Aviation" = c(0.66, 0.73),
    "Cyber" = c(0.62, 0.70),
    "Political Risk" = c(0.60, 0.68),
    "Specialty" = c(0.65, 0.73),
    "Catastrophe" = c(0.55, 0.65),
    "Multi-class" = c(0.67, 0.74)
  )

  for (i in 1:nrow(syndicates_df)) {
    syndicate_no <- syndicates_df$SyndicateNumber[i]
    business_class <- syndicates_df$PrimaryBusinessClass[i]

    # Get base loss ratios for this business class
    if (business_class %in% names(base_loss_ratios)) {
      ratios <- base_loss_ratios[[business_class]]
    } else {
      ratios <- c(0.65, 0.72)
    }
    plan_base <- ratios[1]
    model_base <- ratios[2]

    # (A) 2024 LCR submission
    plan_2024 <- plan_base + runif(1, -0.03, 0.03)
    model_2024 <- model_base + runif(1, -0.03, 0.03)
    self_uplift_2024 <- model_2024 - plan_2024

    records[[idx]] <- data.frame(
      SyndicateNumber = syndicate_no,
      RowLabel = "(A) 2024: LCR submission",
      ReportingPeriod = "2024 YOA",
      SubmissionDate = as.Date("2024-10-01"),
      PlanLossRatio_NetNet = round(plan_2024, 4),
      ModelledLossRatio_NetNet = round(model_2024, 4),
      SelfUplift_pct = round(self_uplift_2024 * 100, 2),
      SyndicateComments = "Initial 2024 YOA submission",
      stringsAsFactors = FALSE
    )
    idx <- idx + 1

    # (B) 2025 LCR submission
    plan_2025_lcr <- plan_2024 + runif(1, -0.02, 0.04)
    model_2025_lcr <- model_2024 + runif(1, -0.02, 0.04)
    self_uplift_2025_lcr <- model_2025_lcr - plan_2025_lcr

    records[[idx]] <- data.frame(
      SyndicateNumber = syndicate_no,
      RowLabel = "(B) 2025: LCR submission",
      ReportingPeriod = "2025 YOA",
      SubmissionDate = as.Date("2025-10-01"),
      PlanLossRatio_NetNet = round(plan_2025_lcr, 4),
      ModelledLossRatio_NetNet = round(model_2025_lcr, 4),
      SelfUplift_pct = round(self_uplift_2025_lcr * 100, 2),
      SyndicateComments = "Initial 2025 YOA submission",
      stringsAsFactors = FALSE
    )
    idx <- idx + 1

    # (C) 2025 Updated for resubmitted SBF
    plan_increase <- runif(1, 0.01, 0.05)
    plan_2025_sbf <- plan_2025_lcr + plan_increase
    model_adjustment <- runif(1, 0.005, 0.04)
    model_2025_sbf <- model_2025_lcr + model_adjustment

    # Ensure modelled >= plan (per Lloyd's guidance)
    if (model_2025_sbf < plan_2025_sbf) {
      model_2025_sbf <- plan_2025_sbf + runif(1, 0.01, 0.03)
      comment <- "Modelled LR adjusted to align with increased plan"
    } else {
      comment <- "Plan increase driven by pricing environment"
    }

    self_uplift_2025_sbf <- model_2025_sbf - plan_2025_sbf

    records[[idx]] <- data.frame(
      SyndicateNumber = syndicate_no,
      RowLabel = "(C) 2025: Updated for resubmitted SBF",
      ReportingPeriod = "2025 YOA",
      SubmissionDate = as.Date("2025-11-15"),
      PlanLossRatio_NetNet = round(plan_2025_sbf, 4),
      ModelledLossRatio_NetNet = round(model_2025_sbf, 4),
      SelfUplift_pct = round(self_uplift_2025_sbf * 100, 2),
      SyndicateComments = comment,
      stringsAsFactors = FALSE
    )
    idx <- idx + 1

    # (D) Movement: (C) - (A)
    plan_movement <- plan_2025_sbf - plan_2024
    model_movement <- model_2025_sbf - model_2024
    uplift_movement <- self_uplift_2025_sbf - self_uplift_2024

    if (uplift_movement < -0.01) {
      movement_comment <- "Self-uplift decrease reflects market hardening"
    } else {
      movement_comment <- "Movement within expected range"
    }

    records[[idx]] <- data.frame(
      SyndicateNumber = syndicate_no,
      RowLabel = "(D) Movement: (C) - (A)",
      ReportingPeriod = "Delta",
      SubmissionDate = as.Date("2025-11-15"),
      PlanLossRatio_NetNet = round(plan_movement, 4),
      ModelledLossRatio_NetNet = round(model_movement, 4),
      SelfUplift_pct = round(uplift_movement * 100, 2),
      SyndicateComments = movement_comment,
      stringsAsFactors = FALSE
    )
    idx <- idx + 1
  }

  df <- do.call(rbind, records)
  return(df)
}


#' Generate all synthetic Lloyd's data tables
#'
#' @param num_syndicates Number of syndicates to generate
#' @param seed Random seed for reproducibility
#' @param save_to_csv Whether to save data to CSV files
#' @param output_dir Directory to save CSV files
#' @return List containing all generated data frames
generate_all_data <- function(num_syndicates = 20,
                              seed = 42,
                              save_to_csv = FALSE,
                              output_dir = "./output") {

  set_random_seed(seed)

  cat(sprintf("Generating synthetic Lloyd's data for %d syndicates...\n", num_syndicates))

  # Generate data
  syndicate_master <- generate_syndicate_master(num_syndicates)
  scr_impact <- generate_scr_impact_data(syndicate_master)
  loss_ratio <- generate_loss_ratio_data(syndicate_master)

  data <- list(
    syndicate_master = syndicate_master,
    scr_impact_data = scr_impact,
    loss_ratio_data = loss_ratio
  )

  # Print summary
  cat("\n")
  cat(paste(rep("=", 60), collapse = ""), "\n")
  cat("DATA GENERATION COMPLETE\n")
  cat(paste(rep("=", 60), collapse = ""), "\n")
  cat(sprintf("\nSyndicate Master: %d syndicates\n", nrow(syndicate_master)))
  cat(sprintf("SCR Impact Data: %d records\n", nrow(scr_impact)))
  cat(sprintf("Loss Ratio Data: %d records\n", nrow(loss_ratio)))

  # Save to CSV if requested
  if (save_to_csv) {
    if (!dir.exists(output_dir)) {
      dir.create(output_dir, recursive = TRUE)
    }

    for (name in names(data)) {
      filepath <- file.path(output_dir, paste0(name, ".csv"))
      write.csv(data[[name]], filepath, row.names = FALSE)
      cat(sprintf("\nSaved: %s\n", filepath))
    }
  }

  return(data)
}


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if (!interactive()) {
  # Generate data and save to CSV when run as script
  data <- generate_all_data(
    num_syndicates = 25,
    seed = 42,
    save_to_csv = TRUE,
    output_dir = "./output"
  )

  # Display sample data
  cat("\n")
  cat(paste(rep("=", 60), collapse = ""), "\n")
  cat("SAMPLE DATA PREVIEW\n")
  cat(paste(rep("=", 60), collapse = ""), "\n")

  cat("\n1. SYNDICATE MASTER (first 5):\n")
  print(head(data$syndicate_master, 5))

  cat("\n2. SCR IMPACT DATA (first 10):\n")
  print(head(data$scr_impact_data, 10))

  cat("\n3. LOSS RATIO DATA (first 10):\n")
  print(head(data$loss_ratio_data, 10))
}
