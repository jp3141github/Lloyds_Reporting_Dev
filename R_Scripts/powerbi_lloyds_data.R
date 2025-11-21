# Power BI Integration Script for Lloyd's Synthetic Data
# =======================================================
# This script is designed to be used directly in Power BI's R script data source.
#
# HOW TO USE IN POWER BI:
# -----------------------
# 1. Open Power BI Desktop
# 2. Get Data -> More -> R script
# 3. Copy and paste this entire script
# 4. Click OK
# 5. Power BI will show available tables: syndicate_master, scr_impact_data, loss_ratio_data
# 6. Select the tables you want to import
#
# CUSTOMIZATION:
# --------------
# - Change NUM_SYNDICATES to generate more/fewer syndicates
# - Change RANDOM_SEED value for different random data
# - Adjust date ranges in the generation functions
#
# REQUIREMENTS:
# -------------
# Make sure dplyr is installed: install.packages("dplyr")

# Load required libraries
suppressPackageStartupMessages({
  if (!require(dplyr)) install.packages("dplyr")
  library(dplyr)
})


# ============================================================================
# CONFIGURATION
# ============================================================================

NUM_SYNDICATES <- 25
RANDOM_SEED <- 42


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

set_random_seed <- function(seed = 42) {
  set.seed(seed)
}


generate_syndicate_master <- function(num_syndicates = 20) {

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

  data.frame(
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
}


generate_scr_impact_data <- function(syndicates_df) {

  records <- list()
  idx <- 1

  for (i in 1:nrow(syndicates_df)) {
    syndicate_no <- syndicates_df$SyndicateNumber[i]
    capacity <- syndicates_df$StampCapacity_GBPm[i]

    base_uscr <- capacity * runif(1, 0.35, 0.50)
    base_1scr <- base_uscr * runif(1, 0.85, 0.95)

    # Latest LCR
    records[[idx]] <- data.frame(
      SyndicateNumber = syndicate_no,
      SubmissionType = "Latest LCR",
      SBFVersion = "LCR_2024_v1",
      SubmissionDate = as.Date("2024-10-15") + sample(0:30, 1),
      uSCR_GBPm = round(base_uscr, 2),
      X1SCR_GBPm = round(base_1scr, 2),
      SCR_Ratio = round(base_1scr / base_uscr, 4),
      stringsAsFactors = FALSE
    )
    idx <- idx + 1

    # Latest SBF
    sbf_uscr <- base_uscr * runif(1, 0.98, 1.08)
    sbf_1scr <- base_1scr * runif(1, 0.98, 1.08)

    records[[idx]] <- data.frame(
      SyndicateNumber = syndicate_no,
      SubmissionType = "Latest SBF",
      SBFVersion = "SBF_2025_v2",
      SubmissionDate = as.Date("2025-01-15") + sample(0:30, 1),
      uSCR_GBPm = round(sbf_uscr, 2),
      X1SCR_GBPm = round(sbf_1scr, 2),
      SCR_Ratio = round(sbf_1scr / sbf_uscr, 4),
      stringsAsFactors = FALSE
    )
    idx <- idx + 1

    # Movement
    movement_uscr <- sbf_uscr - base_uscr
    movement_1scr <- sbf_1scr - base_1scr

    records[[idx]] <- data.frame(
      SyndicateNumber = syndicate_no,
      SubmissionType = "Movement",
      SBFVersion = "Delta",
      SubmissionDate = as.Date("2025-01-15"),
      uSCR_GBPm = round(movement_uscr, 2),
      X1SCR_GBPm = round(movement_1scr, 2),
      SCR_Ratio = ifelse(movement_uscr != 0, round(movement_1scr / movement_uscr, 4), 0),
      stringsAsFactors = FALSE
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
      X1SCR_GBPm = round(movement_pct_1scr, 2),
      SCR_Ratio = NA,
      stringsAsFactors = FALSE
    )
    idx <- idx + 1
  }

  do.call(rbind, records)
}


generate_loss_ratio_data <- function(syndicates_df) {

  records <- list()
  idx <- 1

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

    if (business_class %in% names(base_loss_ratios)) {
      ratios <- base_loss_ratios[[business_class]]
    } else {
      ratios <- c(0.65, 0.72)
    }
    plan_base <- ratios[1]
    model_base <- ratios[2]

    # (A) 2024 LCR
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

    # (B) 2025 LCR
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

    # (C) 2025 Updated
    plan_increase <- runif(1, 0.01, 0.05)
    plan_2025_sbf <- plan_2025_lcr + plan_increase
    model_adjustment <- runif(1, 0.005, 0.04)
    model_2025_sbf <- model_2025_lcr + model_adjustment

    if (model_2025_sbf < plan_2025_sbf) {
      model_2025_sbf <- plan_2025_sbf + runif(1, 0.01, 0.03)
      comment <- "Modelled LR adjusted to align with plan"
    } else {
      comment <- "Plan increase driven by pricing"
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

    # (D) Movement
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

  do.call(rbind, records)
}


# ============================================================================
# MAIN EXECUTION - This runs when script is loaded in Power BI
# ============================================================================

# Initialize random seed
set_random_seed(RANDOM_SEED)

# Generate all data tables
syndicate_master <- generate_syndicate_master(NUM_SYNDICATES)
scr_impact_data <- generate_scr_impact_data(syndicate_master)
loss_ratio_data <- generate_loss_ratio_data(syndicate_master)

# Power BI will automatically detect these data frames and make them available
# as separate tables to import

cat(sprintf("Generated %d syndicates\n", nrow(syndicate_master)))
cat(sprintf("Generated %d SCR impact records\n", nrow(scr_impact_data)))
cat(sprintf("Generated %d loss ratio records\n", nrow(loss_ratio_data)))
