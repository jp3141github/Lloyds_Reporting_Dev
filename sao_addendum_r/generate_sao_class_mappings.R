###############################################################################
# SAO Addendum Return - SAO Class Mappings Data Generator
###############################################################################
# This script generates synthetic Lloyd's of London data for the SAO Class
# Mappings table. Maps Signing Actuary Reserving Classes to Lloyd's Lines
# of Business. Compatible with Power BI as an R data source.
#
# Usage in Power BI:
# 1. Get Data > More > R script
# 2. Copy and paste this script
# 3. Select the 'class_mappings' table
#
# Author: Claude
# Date: 2025-11-21
###############################################################################

# Set random seed for reproducibility
set.seed(456)

# Function to distribute exposure among multiple LoB
distribute_exposure <- function(total_exposure, num_parts) {
  #' Distribute exposure percentage among multiple LoB.
  #'
  #' @param total_exposure Total exposure to distribute
  #' @param num_parts Number of parts to divide into
  #' @return Vector of exposure percentages

  if (num_parts == 1) {
    return(round(total_exposure, 1))
  }

  # Generate random splits using Dirichlet distribution
  # Simulate with gamma distribution
  splits <- rgamma(num_parts, 1, 1)
  splits <- (splits / sum(splits)) * total_exposure

  return(round(splits, 1))
}

# Function to normalize exposures to 100%
normalize_exposures <- function(exposures) {
  #' Ensure exposures sum to exactly 100%.
  #'
  #' @param exposures Vector of exposure percentages
  #' @return Normalized exposure percentages

  total <- sum(exposures)
  if (total == 0) {
    return(exposures)
  }

  # Normalize to 100%
  normalized <- (exposures / total) * 100
  rounded <- round(normalized, 1)

  # Adjust to ensure sum is exactly 100%
  diff <- 100.0 - sum(rounded)
  if (diff != 0) {
    max_idx <- which.max(rounded)
    rounded[max_idx] <- round(rounded[max_idx] + diff, 1)
  }

  return(rounded)
}

# Function to generate SAO Class Mappings data
generate_class_mappings_data <- function(num_classes = 20) {
  #' Generate synthetic SAO Class Mappings data.
  #'
  #' Maps Signing Actuary Reserving Classes to Lloyd's Lines of Business.
  #' Each reserving class can map to up to 4 Lloyd's LoB with associated
  #' exposure percentages.
  #'
  #' @param num_classes Number of reserving classes to generate
  #' @return Data frame with synthetic class mappings data

  # Define comprehensive list of Signing Actuary Reserving Classes
  reserving_classes <- c(
    'Property Treaty', 'Property Direct', 'Property Cat XL', 'Property Facultative',
    'Casualty Treaty', 'Casualty Direct', 'Casualty XL', 'Casualty Facultative',
    'Marine Hull', 'Marine Cargo', 'Marine Liability', 'Marine Energy',
    'Aviation Hull', 'Aviation Liability', 'Aviation Reinsurance',
    'Energy Offshore', 'Energy Onshore', 'Energy Liability',
    'Professional Indemnity', 'D&O US', 'D&O UK', 'D&O Europe',
    'Cyber Direct', 'Cyber Treaty', 'Motor Direct', 'Motor Fleet',
    'Credit & Surety', 'Political Risk', 'Terrorism',
    'Accident & Health', 'Medical Malpractice', 'Product Liability'
  )

  # Define Lloyd's Lines of Business
  lloyds_lobs <- c(
    'Property Treaty', 'Property Direct', 'Property Cat XL', 'Property Facultative',
    'Casualty Treaty', 'Casualty Direct', 'D&O', 'Professional Indemnity',
    'Marine Hull', 'Marine Cargo', 'Marine Liability', 'Energy Offshore',
    'Aviation', 'Cyber', 'Motor', 'Credit & Surety',
    'Political Risk', 'Terrorism', 'Accident & Health',
    'Medical Malpractice', 'Product Liability', 'Environmental'
  )

  # Predefined primary mappings
  primary_mappings <- list(
    'Property Treaty' = 'Property Treaty',
    'Property Direct' = 'Property Direct',
    'Property Cat XL' = 'Property Cat XL',
    'Casualty Treaty' = 'Casualty Treaty',
    'Marine Hull' = 'Marine Hull',
    'Marine Cargo' = 'Marine Cargo',
    'Aviation Hull' = 'Aviation',
    'Aviation Liability' = 'Aviation',
    'Energy Offshore' = 'Energy Offshore',
    'Professional Indemnity' = 'Professional Indemnity',
    'D&O US' = 'D&O',
    'D&O UK' = 'D&O',
    'D&O Europe' = 'D&O',
    'Cyber Direct' = 'Cyber',
    'Cyber Treaty' = 'Cyber',
    'Motor Direct' = 'Motor',
    'Motor Fleet' = 'Motor',
    'Credit & Surety' = 'Credit & Surety',
    'Political Risk' = 'Political Risk',
    'Terrorism' = 'Terrorism',
    'Accident & Health' = 'Accident & Health',
    'Medical Malpractice' = 'Medical Malpractice',
    'Product Liability' = 'Product Liability'
  )

  # Ensure we don't exceed available classes
  num_classes <- min(num_classes, length(reserving_classes))

  # Initialize data frame
  data <- data.frame(
    `Signing Actuary Reserving Class Name` = character(num_classes),
    `Lloyd's LoB 1` = character(num_classes),
    `LoB 1: % of Gross Exposure` = numeric(num_classes),
    `Lloyd's LoB 2` = character(num_classes),
    `LoB 2: % of Gross Exposure` = numeric(num_classes),
    `Lloyd's LoB 3` = character(num_classes),
    `LoB 3: % of Gross Exposure` = numeric(num_classes),
    `Lloyd's LoB 4` = character(num_classes),
    `LoB 4: % of Gross Exposure` = numeric(num_classes),
    stringsAsFactors = FALSE,
    check.names = FALSE
  )

  # Generate records
  for (i in 1:num_classes) {
    res_class <- reserving_classes[i]

    # Get primary LoB mapping
    if (res_class %in% names(primary_mappings)) {
      primary_lob <- primary_mappings[[res_class]]
    } else {
      primary_lob <- sample(lloyds_lobs, 1)
    }

    # Determine number of LoB mappings (1-4)
    num_lobs <- sample(1:4, 1, prob = c(0.40, 0.35, 0.15, 0.10))

    # Generate exposure percentages
    if (num_lobs == 1) {
      exposures <- c(100.0, 0, 0, 0)
      lobs <- c(primary_lob, '', '', '')
    } else {
      # Primary LoB gets majority of exposure
      primary_exposure <- round(runif(1, 60, 85), 1)
      remaining_exposure <- 100.0 - primary_exposure

      # Distribute remaining exposure among secondary LoB
      secondary_exposures <- distribute_exposure(remaining_exposure, num_lobs - 1)

      # Combine exposures
      exposures <- c(primary_exposure, secondary_exposures)

      # Pad with zeros if needed
      while (length(exposures) < 4) {
        exposures <- c(exposures, 0)
      }

      # Normalize to ensure sum is 100%
      non_zero_count <- sum(exposures > 0)
      exposures[1:non_zero_count] <- normalize_exposures(exposures[1:non_zero_count])

      # Select secondary LoB (different from primary)
      available_lobs <- lloyds_lobs[lloyds_lobs != primary_lob]
      secondary_lobs <- sample(available_lobs, size = num_lobs - 1, replace = FALSE)

      # Combine LoB
      lobs <- c(primary_lob, secondary_lobs)

      # Pad with empty strings
      while (length(lobs) < 4) {
        lobs <- c(lobs, '')
      }
    }

    # Populate data frame
    data[i, 'Signing Actuary Reserving Class Name'] <- res_class
    data[i, "Lloyd's LoB 1"] <- lobs[1]
    data[i, 'LoB 1: % of Gross Exposure'] <- exposures[1]
    data[i, "Lloyd's LoB 2"] <- lobs[2]
    data[i, 'LoB 2: % of Gross Exposure'] <- exposures[2]
    data[i, "Lloyd's LoB 3"] <- lobs[3]
    data[i, 'LoB 3: % of Gross Exposure'] <- exposures[3]
    data[i, "Lloyd's LoB 4"] <- lobs[4]
    data[i, 'LoB 4: % of Gross Exposure'] <- exposures[4]
  }

  return(data)
}

# Generate the data
class_mappings <- generate_class_mappings_data(num_classes = 20)

# Display summary statistics
cat(paste(rep("=", 80), collapse = ""), "\n")
cat("SAO Addendum Return - SAO Class Mappings Summary\n")
cat(paste(rep("=", 80), collapse = ""), "\n")
cat(sprintf("Total Reserving Classes: %d\n", nrow(class_mappings)))
cat(sprintf("Classes mapping to 1 LoB: %d\n",
            sum(class_mappings$`Lloyd's LoB 2` == '')))
cat(sprintf("Classes mapping to 2 LoB: %d\n",
            sum(class_mappings$`Lloyd's LoB 2` != '' & class_mappings$`Lloyd's LoB 3` == '')))
cat(sprintf("Classes mapping to 3 LoB: %d\n",
            sum(class_mappings$`Lloyd's LoB 3` != '' & class_mappings$`Lloyd's LoB 4` == '')))
cat(sprintf("Classes mapping to 4 LoB: %d\n",
            sum(class_mappings$`Lloyd's LoB 4` != '')))
cat(paste(rep("=", 80), collapse = ""), "\n")
cat("\nSample Mappings:\n")
print(head(class_mappings, 10))
cat("\n")

# Verify all exposures sum to 100%
cat("Exposure Validation:\n")
all_valid <- TRUE
for (i in 1:nrow(class_mappings)) {
  total_exposure <- class_mappings[i, 'LoB 1: % of Gross Exposure'] +
                    class_mappings[i, 'LoB 2: % of Gross Exposure'] +
                    class_mappings[i, 'LoB 3: % of Gross Exposure'] +
                    class_mappings[i, 'LoB 4: % of Gross Exposure']

  if (abs(total_exposure - 100.0) > 0.1) {
    cat(sprintf("WARNING: %s total exposure = %.1f%%\n",
                class_mappings[i, 'Signing Actuary Reserving Class Name'],
                total_exposure))
    all_valid <- FALSE
  }
}

if (all_valid) {
  cat("All exposures validated successfully!\n")
}
cat("\n")

# This table will be available in Power BI
# Power BI will automatically detect the 'class_mappings' data frame
