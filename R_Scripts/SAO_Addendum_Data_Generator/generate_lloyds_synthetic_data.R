# Lloyd's of London SAO Addendum Return - Synthetic Data Generator
# ===================================================================
#
# This script generates synthetic Lloyd's of London data for the SAO Addendum Return 2025.
# It creates three main datasets:
# 1. Specific IBNR data (Form 090)
# 2. Movements and Actual vs Expected Analysis (Form 100)
# 3. SAO Class Mappings
#
# The generated data can be used in Power BI for reporting purposes.
#
# Author: Claude AI
# Date: 2025-11-21

# Required packages
if (!require("dplyr")) install.packages("dplyr")
if (!require("tidyr")) install.packages("tidyr")
if (!require("openxlsx")) install.packages("openxlsx")

library(dplyr)
library(tidyr)
library(openxlsx)

# Set random seed for reproducibility
set.seed(42)

# =============================================================================
# Configuration
# =============================================================================

SYNDICATE_NUMBER <- "2060N"

# Lloyd's Lines of Business
LLOYDS_LOBS <- c(
  "Fire", "Property Direct", "Property Cat", "Property Cat XL",
  "Property Treaty", "Motor Direct", "Motor XL", "Marine Cargo",
  "Marine Hull", "Energy Offshore", "Energy Onshore", "Aviation Hull",
  "Aviation Liability", "D&O", "Professional Indemnity", "Casualty Treaty",
  "General Liability", "Medical Malpractice", "Product Liability",
  "Cyber", "Credit & Bond", "Political Risk", "Terrorism", "Accident & Health"
)

# Reserving class examples
RESERVING_CLASSES <- c(
  "Property Cat XL", "Marine Hull", "D&O US", "Aviation Liability",
  "Professional Indemnity", "Casualty Treaty", "Energy Offshore",
  "Property Direct", "Motor XL", "Cyber Liability", "Political Risk"
)

# CAT codes (examples of historical Lloyd's CAT codes)
CAT_CODES <- c("22E", "23A", "23B", "24C", "21D", "Non Nat-Cat")

# =============================================================================
# Function: Generate Specific IBNR Data (Form 090)
# =============================================================================

generate_specific_ibnr <- function(num_records = 50) {
  cat("Generating Specific IBNR data...\n")

  data <- data.frame(
    Reserving_Class = character(num_records),
    Lloyds_CAT_Code = character(num_records),
    Lloyds_Line_of_Business = character(num_records),
    Number_of_Losses = integer(num_records),
    Underwriting_Year = integer(num_records),
    Gross_IBNR_GBP000s = numeric(num_records),
    Net_IBNR_GBP000s = numeric(num_records),
    Comment = character(num_records),
    stringsAsFactors = FALSE
  )

  comments <- c(
    "Reserved using underlying cedant exposure and loss advice plus assumption on limits losses",
    "Based on market loss estimates and exposure analysis",
    "Actuarial analysis of reported losses and development patterns",
    "Industry loss estimates adjusted for portfolio exposure",
    "Initial reserve pending further loss development",
    ""
  )

  for (i in 1:num_records) {
    # Determine if CAT or Non-CAT
    is_cat <- runif(1) > 0.3
    cat_code <- if (is_cat) {
      sample(CAT_CODES[CAT_CODES != "Non Nat-Cat"], 1)
    } else {
      "Non Nat-Cat"
    }

    # Generate random values
    reserving_class <- sample(RESERVING_CLASSES, 1)
    lloyds_lob <- sample(LLOYDS_LOBS, 1)
    num_losses <- sample(1:20, 1)
    underwriting_year <- sample(c(2020:2025), 1)

    # Generate IBNR amounts (ensure > £1m gross as per requirements)
    gross_ibnr <- sample(1000:50000, 1)  # £000s
    reinsurance_recovery <- runif(1, 0.2, 0.5)  # 20-50% recovery
    net_ibnr <- as.integer(gross_ibnr * (1 - reinsurance_recovery))

    # Add to dataframe
    data[i, ] <- list(
      Reserving_Class = reserving_class,
      Lloyds_CAT_Code = cat_code,
      Lloyds_Line_of_Business = lloyds_lob,
      Number_of_Losses = num_losses,
      Underwriting_Year = underwriting_year,
      Gross_IBNR_GBP000s = gross_ibnr,
      Net_IBNR_GBP000s = net_ibnr,
      Comment = sample(comments, 1)
    )
  }

  # Sort by Reserving Class and Underwriting Year
  data <- data %>%
    arrange(Reserving_Class, Underwriting_Year)

  return(data)
}

# =============================================================================
# Function: Generate Movements and AvE Analysis Data (Form 100)
# =============================================================================

generate_movements_and_ave <- function(num_classes = 10) {
  cat("Generating Movements and AvE analysis data...\n")

  data <- data.frame()

  for (class_num in 1:num_classes) {
    class_name <- if (class_num <= length(RESERVING_CLASSES)) {
      RESERVING_CLASSES[class_num]
    } else {
      sprintf("Class %02d", class_num)
    }

    lloyds_lob <- sample(LLOYDS_LOBS, 1)

    # Generate data for each underwriting year
    uw_years <- list(
      list(year = 2023, label = "2023 & Prior"),
      list(year = 2024, label = "2024"),
      list(year = 2025, label = "2025")
    )

    for (uw in uw_years) {
      is_reporting_year <- if (uw$year >= 2024) "Yes" else "No"

      # Generate ultimate premium
      ultimate_premium <- sample(5000:100000, 1)  # £5m to £100m (in £000s)

      # Generate Actual vs Expected (can be positive or negative)
      ave_pct <- runif(1, -15, 10)  # -15% to +10%

      # Generate Initial Expected Loss Ratio
      ielr <- runif(1, 55, 75)  # 55% to 75%

      # Generate Ultimate Loss Ratio (should relate to IELR + AvE)
      ulr <- ielr + runif(1, -5, 10)

      # Generate prior year values (2024YE)
      prior_ielr_2024ye <- ielr + runif(1, -3, 3)
      prior_ulr_2024ye <- ulr + runif(1, -5, 5)
      prior_ave_2024ye <- ave_pct + runif(1, -5, 5)

      # Generate current year values (2025YE)
      current_ielr_2025ye <- ielr
      current_ulr_2025ye <- ulr
      current_ave_2025ye <- ave_pct

      # Syndicate estimate
      syndicate_ulr <- ulr + runif(1, -3, 3)

      row_data <- data.frame(
        Class_Number = class_num,
        Class_Name = class_name,
        Lloyds_Line_of_Business = lloyds_lob,
        Underwriting_Year = uw$year,
        Year_Label = uw$label,
        Reporting_Year = is_reporting_year,
        Ultimate_Premium_GBP000s = ultimate_premium,
        ActualVsExpected_Pct_Ultimate_Premium = round(ave_pct, 2),
        Initial_Expected_Loss_Ratio_Pct = round(ielr, 2),
        Ultimate_Loss_Ratio_Pct_2024YE = round(prior_ulr_2024ye, 2),
        Ultimate_Loss_Ratio_Pct_2025YE = round(current_ulr_2025ye, 2),
        Syndicate_Estimate_ULR_2025YE = round(syndicate_ulr, 2),
        IELR_2024YE = round(prior_ielr_2024ye, 2),
        IELR_2025YE = round(current_ielr_2025ye, 2),
        AvE_2024YE = round(prior_ave_2024ye, 2),
        AvE_2025YE = round(current_ave_2025ye, 2),
        stringsAsFactors = FALSE
      )

      data <- rbind(data, row_data)
    }
  }

  # Sort by Class Number and Underwriting Year
  data <- data %>%
    arrange(Class_Number, Underwriting_Year)

  return(data)
}

# =============================================================================
# Function: Generate SAO Class Mappings Data
# =============================================================================

generate_sao_class_mappings <- function(num_classes = 15) {
  cat("Generating SAO Class Mappings data...\n")

  data <- data.frame()

  for (i in 1:num_classes) {
    reserving_class <- if (i <= length(RESERVING_CLASSES)) {
      RESERVING_CLASSES[i]
    } else {
      paste0(RESERVING_CLASSES[i %% length(RESERVING_CLASSES) + 1], " Sub-", i)
    }

    # Select up to 4 Lloyd's LoB for this reserving class
    num_lobs <- sample(1:4, 1)
    selected_lobs <- sample(LLOYDS_LOBS, num_lobs)

    # Generate exposure percentages that sum to 100%
    exposures <- runif(num_lobs)
    exposures <- (exposures / sum(exposures)) * 100

    # Create row with up to 4 LoB
    row_data <- list(
      Reserving_Class_Name = reserving_class,
      Lloyds_LoB_1 = if (num_lobs >= 1) selected_lobs[1] else NA,
      LoB_1_Pct_Gross_Exposure = if (num_lobs >= 1) round(exposures[1], 2) else NA,
      Lloyds_LoB_2 = if (num_lobs >= 2) selected_lobs[2] else NA,
      LoB_2_Pct_Gross_Exposure = if (num_lobs >= 2) round(exposures[2], 2) else NA,
      Lloyds_LoB_3 = if (num_lobs >= 3) selected_lobs[3] else NA,
      LoB_3_Pct_Gross_Exposure = if (num_lobs >= 3) round(exposures[3], 2) else NA,
      Lloyds_LoB_4 = if (num_lobs >= 4) selected_lobs[4] else NA,
      LoB_4_Pct_Gross_Exposure = if (num_lobs >= 4) round(exposures[4], 2) else NA
    )

    data <- rbind(data, as.data.frame(row_data, stringsAsFactors = FALSE))
  }

  return(data)
}

# =============================================================================
# Function: Export Data to CSV Files
# =============================================================================

export_to_csv <- function(output_dir = "output") {
  cat("\n", rep("=", 70), "\n", sep = "")
  cat("Lloyd's of London SAO Addendum Return - Synthetic Data Generator\n")
  cat(rep("=", 70), "\n\n", sep = "")

  # Create output directory if it doesn't exist
  if (!dir.exists(output_dir)) {
    dir.create(output_dir, recursive = TRUE)
  }

  # Generate all data
  cat("Generating synthetic data...\n\n")
  df_ibnr <- generate_specific_ibnr(num_records = 50)
  df_movements <- generate_movements_and_ave(num_classes = 10)
  df_mappings <- generate_sao_class_mappings(num_classes = 15)

  # Create timestamp
  timestamp <- format(Sys.time(), "%Y%m%d_%H%M%S")

  # Export to CSV
  cat("\nExporting to CSV files...\n")

  file_ibnr <- file.path(output_dir,
                         sprintf("Specific_IBNR_%s_%s.csv", SYNDICATE_NUMBER, timestamp))
  write.csv(df_ibnr, file_ibnr, row.names = FALSE)
  cat(sprintf("Exported: %s (%d records)\n", file_ibnr, nrow(df_ibnr)))

  file_movements <- file.path(output_dir,
                               sprintf("Movements_and_AvE_%s_%s.csv", SYNDICATE_NUMBER, timestamp))
  write.csv(df_movements, file_movements, row.names = FALSE)
  cat(sprintf("Exported: %s (%d records)\n", file_movements, nrow(df_movements)))

  file_mappings <- file.path(output_dir,
                              sprintf("SAO_Class_Mappings_%s_%s.csv", SYNDICATE_NUMBER, timestamp))
  write.csv(df_mappings, file_mappings, row.names = FALSE)
  cat(sprintf("Exported: %s (%d records)\n", file_mappings, nrow(df_mappings)))

  cat("\nData generation complete!\n")

  return(list(
    Specific_IBNR = df_ibnr,
    Movements_and_AvE = df_movements,
    SAO_Class_Mappings = df_mappings
  ))
}

# =============================================================================
# Function: Export Data to Excel File
# =============================================================================

export_to_excel <- function(output_dir = "output") {
  cat("\n", rep("=", 70), "\n", sep = "")
  cat("Lloyd's of London SAO Addendum Return - Synthetic Data Generator\n")
  cat(rep("=", 70), "\n\n", sep = "")

  # Create output directory if it doesn't exist
  if (!dir.exists(output_dir)) {
    dir.create(output_dir, recursive = TRUE)
  }

  # Generate all data
  cat("Generating synthetic data...\n\n")
  df_ibnr <- generate_specific_ibnr(num_records = 50)
  df_movements <- generate_movements_and_ave(num_classes = 10)
  df_mappings <- generate_sao_class_mappings(num_classes = 15)

  # Create timestamp
  timestamp <- format(Sys.time(), "%Y%m%d_%H%M%S")

  # Create Excel workbook
  cat("\nExporting to Excel file...\n")
  wb <- createWorkbook()

  # Add sheets
  addWorksheet(wb, "Specific_IBNR")
  writeData(wb, "Specific_IBNR", df_ibnr)
  cat(sprintf("Added sheet: Specific_IBNR (%d records)\n", nrow(df_ibnr)))

  addWorksheet(wb, "Movements_and_AvE")
  writeData(wb, "Movements_and_AvE", df_movements)
  cat(sprintf("Added sheet: Movements_and_AvE (%d records)\n", nrow(df_movements)))

  addWorksheet(wb, "SAO_Class_Mappings")
  writeData(wb, "SAO_Class_Mappings", df_mappings)
  cat(sprintf("Added sheet: SAO_Class_Mappings (%d records)\n", nrow(df_mappings)))

  # Save workbook
  filename <- file.path(output_dir,
                        sprintf("SAO_Addendum_Synthetic_Data_%s_%s.xlsx",
                                SYNDICATE_NUMBER, timestamp))
  saveWorkbook(wb, filename, overwrite = TRUE)
  cat(sprintf("\nExported: %s\n", filename))
  cat("Data generation complete!\n")

  return(list(
    Specific_IBNR = df_ibnr,
    Movements_and_AvE = df_movements,
    SAO_Class_Mappings = df_mappings
  ))
}

# =============================================================================
# Function: Display Sample Data
# =============================================================================

display_sample_data <- function(data_list) {
  cat("\n", rep("=", 70), "\n", sep = "")
  cat("Sample Data Preview\n")
  cat(rep("=", 70), "\n", sep = "")

  for (table_name in names(data_list)) {
    cat("\n", table_name, " (first 5 rows):\n", sep = "")
    cat(rep("-", 70), "\n", sep = "")
    print(head(data_list[[table_name]], 5))
  }
}

# =============================================================================
# Main Execution
# =============================================================================

main <- function() {
  # Export to CSV files (for Power BI)
  data_list <- export_to_csv(output_dir = "output")

  cat("\n", rep("=", 70), "\n\n", sep = "")

  # Also export to Excel for easy viewing
  export_to_excel(output_dir = "output")

  # Display sample data
  display_sample_data(data_list)

  cat("\n", rep("=", 70), "\n", sep = "")
  cat("All files saved to 'output' directory\n")
  cat(rep("=", 70), "\n", sep = "")
}

# Run main function
if (!interactive()) {
  main()
}
