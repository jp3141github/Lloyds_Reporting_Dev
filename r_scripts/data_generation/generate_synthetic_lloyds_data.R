# Synthetic Lloyd's of London Data Generator (R Version)
# Generates realistic RRA (Reserving Return Annual) data for testing and development
#
# This script creates synthetic Lloyd's data that can be used in Power BI
# for testing RRA reporting templates.

library(dplyr)
library(lubridate)
library(readr)

# Set random seed for reproducibility
set.seed(42)

# Configuration
output_dir <- "../../synthetic_data"
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# Lloyd's syndicate numbers (realistic ranges)
syndicates <- c(2987, 33, 1183, 2791, 623, 4242, 5000, 1910, 2010, 2525)

# Years of Account (YoA)
current_year <- 2024
years_of_account <- 2018:2025

# Classes of Business (Lloyd's typical classes)
classes_of_business <- c(
  A1 = "Direct Accident & Health",
  A2 = "Accident & Health Reinsurance",
  D1 = "Direct Motor (Private Car)",
  D2 = "Direct Motor (Commercial)",
  E1 = "Energy Offshore",
  E2 = "Energy Onshore",
  F1 = "Fire & Other Damage - Direct",
  F2 = "Fire & Other Damage - Reinsurance",
  M1 = "Marine Cargo",
  M2 = "Marine Hull",
  M3 = "Marine Liability",
  N1 = "Non-Marine Property Treaty",
  N2 = "Non-Marine Property Facultative",
  P1 = "Professional Indemnity",
  P2 = "Public & Products Liability",
  T1 = "Third Party Liability - Direct",
  T2 = "Third Party Liability - Reinsurance",
  V1 = "Aviation",
  W1 = "Political Risk & Contingency",
  X1 = "Catastrophe Reinsurance"
)

# Catastrophe codes
cat_codes <- c(
  NAT01 = "Hurricane - USA",
  NAT02 = "Earthquake - Japan",
  NAT03 = "Flood - Europe",
  NAT04 = "Windstorm - Europe",
  NAT05 = "Wildfire - USA",
  MAN01 = "Cyber Attack",
  MAN02 = "Industrial Accident",
  MAN03 = "Aviation Accident"
)

# Currency codes
currencies <- c("GBP", "USD", "EUR", "CAD", "AUD", "JPY")

# Generate RRA 010 Control Data
generate_control_data <- function() {
  control_data <- data.frame()

  for (syndicate in syndicates) {
    control_data <- rbind(control_data, data.frame(
      Syndicate_Number = syndicate,
      Return_Type = "RRA",
      Status = sample(c("Draft", "Submitted", "Approved"), 1),
      Edition = "1.1",
      Managing_Agent_Name = paste0("Managing Agent ", syndicate),
      First_Pure_YoA = min(years_of_account),
      First_Reporting_YoA = min(years_of_account),
      Final_Pure_YoA = max(years_of_account) - 1,
      Prospective_Year = max(years_of_account),
      Contact_Username = paste0("user", syndicate),
      Contact_Name = paste0("Contact Person ", syndicate),
      Contact_Phone = sprintf("+44 20 %04d %04d",
                              sample(7000:7999, 1),
                              sample(1000:9999, 1)),
      Contact_Email = paste0("contact", syndicate, "@lloyds.com"),
      Submission_Date = format(Sys.Date(), "%Y-%m-%d"),
      Capacity_GBP = sample(50000000:500000000, 1),
      stringsAsFactors = FALSE
    ))
  }

  write_csv(control_data, file.path(output_dir, "rra_010_control.csv"))
  cat(sprintf("✓ Generated RRA 010 Control: %d records\n", nrow(control_data)))
  return(control_data)
}

# Generate RRA 020 Exchange Rates
generate_exchange_rates <- function() {
  base_rates <- c(USD = 1.27, EUR = 1.17, CAD = 1.72,
                  AUD = 1.95, JPY = 188.5, GBP = 1.00)

  exchange_rates <- data.frame()

  for (year in years_of_account) {
    for (i in 1:length(base_rates)) {
      currency <- names(base_rates)[i]
      base_rate <- base_rates[i]
      variation <- runif(1, 0.95, 1.05)

      exchange_rates <- rbind(exchange_rates, data.frame(
        Year_of_Account = year,
        Currency_Code = currency,
        Currency_Name = currency,
        Exchange_Rate_to_GBP = round(base_rate * variation, 4),
        Rate_Type = "Average",
        Effective_Date = paste0(year, "-12-31"),
        stringsAsFactors = FALSE
      ))
    }
  }

  write_csv(exchange_rates, file.path(output_dir, "rra_020_exchange_rates.csv"))
  cat(sprintf("✓ Generated RRA 020 Exchange Rates: %d records\n", nrow(exchange_rates)))
  return(exchange_rates)
}

# Generate RRA 071 SCOB Mapping
generate_scob_mapping <- function() {
  scob_mapping <- data.frame()

  for (syndicate in syndicates) {
    num_classes <- sample(3:7, 1)
    selected_classes <- sample(names(classes_of_business), num_classes)

    for (class_code in selected_classes) {
      scob_mapping <- rbind(scob_mapping, data.frame(
        Syndicate_Number = syndicate,
        SCOB_Code = paste0(class_code, "_", syndicate),
        LOB_Code = class_code,
        LOB_Description = classes_of_business[class_code],
        Reserving_Class = paste0("RC_", class_code),
        Active_Flag = "Y",
        Effective_From = paste0(min(years_of_account), "-01-01"),
        Effective_To = paste0(max(years_of_account), "-12-31"),
        stringsAsFactors = FALSE
      ))
    }
  }

  write_csv(scob_mapping, file.path(output_dir, "rra_071_scob_mapping.csv"))
  cat(sprintf("✓ Generated RRA 071 SCOB Mapping: %d records\n", nrow(scob_mapping)))
  return(scob_mapping)
}

# Generate RRA 081 Reserving Class Information
generate_reserving_class_info <- function() {
  res_class_info <- data.frame()

  for (syndicate in syndicates) {
    for (i in 1:length(classes_of_business)) {
      lob_code <- names(classes_of_business)[i]
      lob_desc <- classes_of_business[i]

      res_class_info <- rbind(res_class_info, data.frame(
        Syndicate_Number = syndicate,
        Reserving_Class_Code = paste0("RC_", lob_code),
        Reserving_Class_Description = paste0(lob_desc, " - Reserves"),
        LOB_Code = lob_code,
        Development_Pattern = sample(c("Short Tail", "Medium Tail", "Long Tail"), 1),
        Average_Settlement_Years = sample(1:15, 1),
        Actuarial_Method = sample(c("Chain Ladder", "BF Method", "Cape Cod", "Expected Loss Ratio"), 1),
        Last_Review_Date = format(as.Date(paste(current_year,
                                               sample(1:12, 1),
                                               sample(1:28, 1), sep = "-")), "%Y-%m-%d"),
        stringsAsFactors = FALSE
      ))
    }
  }

  write_csv(res_class_info, file.path(output_dir, "rra_081_reserving_class_info.csv"))
  cat(sprintf("✓ Generated RRA 081 Reserving Class Info: %d records\n", nrow(res_class_info)))
  return(res_class_info)
}

# Generate RRA 091 LPT Data
generate_lpt_data <- function() {
  lpt_data <- data.frame()

  selected_syndicates <- sample(syndicates, 3)

  for (syndicate in selected_syndicates) {
    selected_years <- sample(years_of_account[1:(length(years_of_account)-2)], 2)

    for (year in selected_years) {
      lpt_data <- rbind(lpt_data, data.frame(
        Syndicate_Number = syndicate,
        Year_of_Account = year,
        LPT_Type = sample(c("Quota Share", "Excess of Loss", "Stop Loss"), 1),
        Counterparty_Name = paste0("Reinsurer_", sample(1:5, 1)),
        LPT_Effective_Date = paste0(year + 2, "-01-01"),
        Transfer_Amount_GBP = sample(5000000:50000000, 1),
        Outstanding_Claims_GBP = sample(3000000:40000000, 1),
        IBNR_GBP = sample(1000000:15000000, 1),
        Premium_Paid_GBP = sample(4000000:45000000, 1),
        stringsAsFactors = FALSE
      ))
    }
  }

  write_csv(lpt_data, file.path(output_dir, "rra_091_lpt.csv"))
  cat(sprintf("✓ Generated RRA 091 LPT: %d records\n", nrow(lpt_data)))
  return(lpt_data)
}

# Generate RRA 193 Net Claims
generate_net_claims <- function() {
  net_claims <- data.frame()

  for (syndicate in syndicates) {
    for (year in years_of_account[1:(length(years_of_account)-1)]) {
      selected_lobs <- sample(names(classes_of_business), 5)

      for (lob_code in selected_lobs) {
        max_dev_years <- min(8, current_year - year + 1)

        for (dev_year in 0:(max_dev_years - 1)) {
          base_premium <- sample(1000000:20000000, 1)
          loss_ratio <- runif(1, 0.45, 0.85)
          development_factor <- min(1.0, 0.2 + (dev_year * 0.15))

          cumulative_paid <- as.integer(base_premium * loss_ratio * development_factor)
          case_reserves <- as.integer(base_premium * loss_ratio * (1 - development_factor) * 0.6)
          ibnr <- as.integer(base_premium * loss_ratio * (1 - development_factor) * 0.4)

          net_claims <- rbind(net_claims, data.frame(
            Syndicate_Number = syndicate,
            Year_of_Account = year,
            Development_Year = dev_year,
            LOB_Code = lob_code,
            Currency = "GBP",
            Gross_Premium_Written = base_premium,
            Net_Premium_Written = as.integer(base_premium * 0.85),
            Cumulative_Paid_Claims = cumulative_paid,
            Case_Reserves = case_reserves,
            IBNR_Reserve = ibnr,
            Total_Incurred = cumulative_paid + case_reserves + ibnr,
            Number_of_Claims = sample(10:500, 1),
            Number_of_Claims_Closed = as.integer(sample(5:400, 1) * development_factor),
            As_At_Date = paste0(year + dev_year, "-12-31"),
            stringsAsFactors = FALSE
          ))
        }
      }
    }
  }

  write_csv(net_claims, file.path(output_dir, "rra_193_net_claims.csv"))
  cat(sprintf("✓ Generated RRA 193 Net Claims: %d records\n", nrow(net_claims)))
  return(net_claims)
}

# Generate RRA 291 Gross Premium and IBNR
generate_gross_premium_ibnr <- function() {
  gross_data <- data.frame()

  for (syndicate in syndicates) {
    for (year in years_of_account[1:(length(years_of_account)-1)]) {
      selected_lobs <- sample(names(classes_of_business), 5)

      for (lob_code in selected_lobs) {
        gwp <- sample(5000000:50000000, 1)
        ultimate_loss_ratio <- runif(1, 0.55, 0.75)

        gross_data <- rbind(gross_data, data.frame(
          Syndicate_Number = syndicate,
          Year_of_Account = year,
          LOB_Code = lob_code,
          Currency = "GBP",
          Gross_Written_Premium = gwp,
          Gross_Earned_Premium = as.integer(gwp * runif(1, 0.85, 0.95)),
          Paid_Claims_Gross = as.integer(gwp * ultimate_loss_ratio * runif(1, 0.4, 0.7)),
          Case_Reserves_Gross = as.integer(gwp * ultimate_loss_ratio * runif(1, 0.1, 0.2)),
          IBNR_Best_Estimate = as.integer(gwp * ultimate_loss_ratio * runif(1, 0.15, 0.35)),
          IBNR_High = as.integer(gwp * ultimate_loss_ratio * runif(1, 0.20, 0.40)),
          IBNR_Low = as.integer(gwp * ultimate_loss_ratio * runif(1, 0.10, 0.25)),
          Ultimate_Loss_Ratio = round(ultimate_loss_ratio, 4),
          As_At_Date = paste0(current_year, "-12-31"),
          stringsAsFactors = FALSE
        ))
      }
    }
  }

  write_csv(gross_data, file.path(output_dir, "rra_291_gross_premium_ibnr.csv"))
  cat(sprintf("✓ Generated RRA 291 Gross Premium & IBNR: %d records\n", nrow(gross_data)))
  return(gross_data)
}

# Generate RRA 292 Net Premium and IBNR
generate_net_premium_ibnr <- function() {
  net_data <- data.frame()

  for (syndicate in syndicates) {
    for (year in years_of_account[1:(length(years_of_account)-1)]) {
      selected_lobs <- sample(names(classes_of_business), 5)

      for (lob_code in selected_lobs) {
        nwp <- sample(3000000:40000000, 1)
        ultimate_loss_ratio <- runif(1, 0.50, 0.70)
        ri_recovery <- runif(1, 0.10, 0.25)

        net_data <- rbind(net_data, data.frame(
          Syndicate_Number = syndicate,
          Year_of_Account = year,
          LOB_Code = lob_code,
          Currency = "GBP",
          Net_Written_Premium = nwp,
          Net_Earned_Premium = as.integer(nwp * runif(1, 0.85, 0.95)),
          Paid_Claims_Net = as.integer(nwp * ultimate_loss_ratio * runif(1, 0.45, 0.75)),
          Case_Reserves_Net = as.integer(nwp * ultimate_loss_ratio * runif(1, 0.08, 0.18)),
          IBNR_Net_Best_Estimate = as.integer(nwp * ultimate_loss_ratio * runif(1, 0.12, 0.30)),
          RI_Recoveries_Expected = as.integer(nwp * ri_recovery),
          Net_Ultimate_Loss_Ratio = round(ultimate_loss_ratio, 4),
          Actuarial_Method = sample(c("Chain Ladder", "BF Method", "Expected Loss Ratio"), 1),
          As_At_Date = paste0(current_year, "-12-31"),
          stringsAsFactors = FALSE
        ))
      }
    }
  }

  write_csv(net_data, file.path(output_dir, "rra_292_net_premium_ibnr.csv"))
  cat(sprintf("✓ Generated RRA 292 Net Premium & IBNR: %d records\n", nrow(net_data)))
  return(net_data)
}

# Generate RRA 293 Outstanding & IBNR
generate_os_ibnr_pyoa <- function() {
  os_ibnr_data <- data.frame()

  for (syndicate in syndicates) {
    for (year in years_of_account[1:(length(years_of_account)-1)]) {
      selected_lobs <- sample(names(classes_of_business), 5)

      for (lob_code in selected_lobs) {
        outstanding <- sample(500000:15000000, 1)
        ibnr <- sample(300000:10000000, 1)
        num_claims <- sample(20:300, 1)

        os_ibnr_data <- rbind(os_ibnr_data, data.frame(
          Syndicate_Number = syndicate,
          Pure_Year_of_Account = year,
          LOB_Code = lob_code,
          Currency = "GBP",
          Outstanding_Claims = outstanding,
          IBNR_Reserve = ibnr,
          Total_Reserve = outstanding + ibnr,
          Number_Outstanding_Claims = num_claims,
          Average_Outstanding_Claim = if(outstanding > 0) as.integer(outstanding / num_claims) else 0,
          Reserve_to_Premium_Ratio = round(runif(1, 0.3, 0.8), 4),
          As_At_Date = paste0(current_year, "-12-31"),
          stringsAsFactors = FALSE
        ))
      }
    }
  }

  write_csv(os_ibnr_data, file.path(output_dir, "rra_293_os_ibnr_pyoa.csv"))
  cat(sprintf("✓ Generated RRA 293 OS & IBNR: %d records\n", nrow(os_ibnr_data)))
  return(os_ibnr_data)
}

# Generate RRA 294 Catastrophe IBNR
generate_cat_ibnr <- function() {
  cat_ibnr_data <- data.frame()
  cat_years <- sample(years_of_account[1:(length(years_of_account)-1)], 4)

  for (syndicate in syndicates) {
    for (year in cat_years) {
      selected_cats <- sample(names(cat_codes), 2)

      for (cat_code in selected_cats) {
        cat_loss <- sample(2000000:80000000, 1)

        cat_ibnr_data <- rbind(cat_ibnr_data, data.frame(
          Syndicate_Number = syndicate,
          Year_of_Account = year,
          Catastrophe_Code = cat_code,
          Catastrophe_Description = cat_codes[cat_code],
          Event_Date = format(as.Date(paste(year, sample(1:12, 1), sample(1:28, 1), sep = "-")), "%Y-%m-%d"),
          Currency = "GBP",
          Gross_Incurred_Loss = cat_loss,
          Paid_Loss = as.integer(cat_loss * runif(1, 0.3, 0.7)),
          Case_Reserves = as.integer(cat_loss * runif(1, 0.1, 0.25)),
          IBNR_Estimate = as.integer(cat_loss * runif(1, 0.15, 0.40)),
          RI_Recoveries = as.integer(cat_loss * runif(1, 0.30, 0.60)),
          Net_Cat_Loss = as.integer(cat_loss * runif(1, 0.40, 0.70)),
          Market_Share_Estimate = round(runif(1, 0.01, 0.10), 4),
          As_At_Date = paste0(current_year, "-12-31"),
          stringsAsFactors = FALSE
        ))
      }
    }
  }

  write_csv(cat_ibnr_data, file.path(output_dir, "rra_294_cat_ibnr.csv"))
  cat(sprintf("✓ Generated RRA 294 Catastrophe IBNR: %d records\n", nrow(cat_ibnr_data)))
  return(cat_ibnr_data)
}

# Generate RRA 295 ULAE
generate_ulae <- function() {
  ulae_data <- data.frame()

  for (syndicate in syndicates) {
    for (year in years_of_account[1:(length(years_of_account)-1)]) {
      total_reserves <- sample(10000000:100000000, 1)
      ulae_ratio <- runif(1, 0.03, 0.08)

      ulae_data <- rbind(ulae_data, data.frame(
        Syndicate_Number = syndicate,
        Year_of_Account = year,
        Currency = "GBP",
        Total_Loss_Reserves = total_reserves,
        ULAE_Ratio = round(ulae_ratio, 4),
        ULAE_Reserve = as.integer(total_reserves * ulae_ratio),
        ULAE_Method = sample(c("Percentage of Reserves", "Per Claim", "Historical Average"), 1),
        Internal_Costs = as.integer(total_reserves * ulae_ratio * 0.6),
        External_Costs = as.integer(total_reserves * ulae_ratio * 0.4),
        As_At_Date = paste0(current_year, "-12-31"),
        stringsAsFactors = FALSE
      ))
    }
  }

  write_csv(ulae_data, file.path(output_dir, "rra_295_ulae.csv"))
  cat(sprintf("✓ Generated RRA 295 ULAE: %d records\n", nrow(ulae_data)))
  return(ulae_data)
}

# Generate RRA 391 IELR
generate_ielr <- function() {
  ielr_data <- data.frame()

  for (syndicate in syndicates) {
    for (year in years_of_account[1:(length(years_of_account)-1)]) {
      selected_lobs <- sample(names(classes_of_business), 5)

      for (lob_code in selected_lobs) {
        earned_premium <- sample(5000000:50000000, 1)
        max_dev_years <- min(6, current_year - year + 1)

        for (dev_year in 0:(max_dev_years - 1)) {
          incurred_loss <- as.integer(earned_premium * runif(1, 0.50, 0.75) *
                                     min(1.0, 0.3 + dev_year * 0.15))

          ielr_data <- rbind(ielr_data, data.frame(
            Syndicate_Number = syndicate,
            Year_of_Account = year,
            Development_Year = dev_year,
            LOB_Code = lob_code,
            Currency = "GBP",
            Earned_Premium = earned_premium,
            Incurred_Loss = incurred_loss,
            Incurred_Loss_Ratio = round(incurred_loss / earned_premium, 4),
            Paid_Loss = as.integer(incurred_loss * runif(1, 0.5, 0.9)),
            Outstanding_Reserve = as.integer(incurred_loss * runif(1, 0.1, 0.5)),
            Calendar_Year = year + dev_year,
            As_At_Date = paste0(year + dev_year, "-12-31"),
            stringsAsFactors = FALSE
          ))
        }
      }
    }
  }

  write_csv(ielr_data, file.path(output_dir, "rra_391_ielr.csv"))
  cat(sprintf("✓ Generated RRA 391 IELR: %d records\n", nrow(ielr_data)))
  return(ielr_data)
}

# Generate RRA 910
generate_rra_910 <- function() {
  rra_910_data <- data.frame()

  for (syndicate in syndicates) {
    rra_910_data <- rbind(rra_910_data, data.frame(
      Syndicate_Number = syndicate,
      Reporting_Period = paste0(current_year, "-12-31"),
      Major_Events_Description = sample(c(
        "No major events this period",
        "Significant reserve release in Motor class",
        "Hurricane losses impacting Property class",
        "Strengthening of casualty reserves",
        "Commutation of old year liabilities"
      ), 1),
      Methodology_Changes = sample(c(
        "No changes",
        "Updated development patterns for long-tail classes",
        "Revised IBNR methodology for cyber risks",
        "Enhanced cat modeling approach"
      ), 1),
      Material_Assumptions = "Standard actuarial assumptions applied",
      Data_Quality_Issues = sample(c("None", "Minor data reconciliation items", "None identified"), 1),
      Actuary_Name = paste0("Chief Actuary ", syndicate),
      Actuary_Qualification = sample(c("FIA", "ACII", "FCAS"), 1),
      Sign_Off_Date = paste0(current_year, "-12-31"),
      stringsAsFactors = FALSE
    ))
  }

  write_csv(rra_910_data, file.path(output_dir, "rra_910_additional_info.csv"))
  cat(sprintf("✓ Generated RRA 910 Additional Info: %d records\n", nrow(rra_910_data)))
  return(rra_910_data)
}

# Generate RRA 990
generate_rra_990 <- function() {
  rra_990_data <- data.frame()

  for (syndicate in syndicates) {
    rra_990_data <- rbind(rra_990_data, data.frame(
      Syndicate_Number = syndicate,
      Reporting_Period = paste0(current_year, "-12-31"),
      Total_Forms_Submitted = 15,
      Forms_With_Errors = sample(0:2, 1),
      Forms_With_Warnings = sample(0:5, 1),
      Validation_Status = sample(c("Pass", "Pass with Warnings", "Review Required"), 1),
      Data_Completeness_Score = round(runif(1, 0.95, 1.00), 4),
      Cross_Form_Reconciliation = sample(c("Passed", "Passed with Exceptions"), 1),
      YoY_Movement_Check = sample(c("Within Tolerance", "Requires Explanation"), 1),
      Submission_Timestamp = format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
      Submitted_By = paste0("user", syndicate),
      Validation_Version = "1.1",
      stringsAsFactors = FALSE
    ))
  }

  write_csv(rra_990_data, file.path(output_dir, "rra_990_validation.csv"))
  cat(sprintf("✓ Generated RRA 990 Validation: %d records\n", nrow(rra_990_data)))
  return(rra_990_data)
}

# Main execution
cat("\n", rep("=", 60), "\n", sep = "")
cat("Generating Synthetic Lloyd's RRA Data (R Version)\n")
cat(rep("=", 60), "\n\n", sep = "")

generate_control_data()
generate_exchange_rates()
generate_scob_mapping()
generate_reserving_class_info()
generate_lpt_data()
generate_net_claims()
generate_gross_premium_ibnr()
generate_net_premium_ibnr()
generate_os_ibnr_pyoa()
generate_cat_ibnr()
generate_ulae()
generate_ielr()
generate_rra_910()
generate_rra_990()

cat("\n", rep("=", 60), "\n", sep = "")
cat(sprintf("All data generated successfully in: %s\n", output_dir))
cat(rep("=", 60), "\n\n", sep = "")

cat("Synthetic Lloyd's data generation complete!\n")
cat("Files can now be imported into Power BI for testing RRA reports.\n")
