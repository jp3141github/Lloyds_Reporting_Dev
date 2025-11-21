###############################################################################
# SAO Addendum Return - 090 Specific IBNR Data Generator
###############################################################################
# This script generates synthetic Lloyd's of London data for the 090 Specific
# IBNR table. Compatible with Power BI as an R data source.
#
# Usage in Power BI:
# 1. Get Data > More > R script
# 2. Copy and paste this script
# 3. Select the 'specific_ibnr' table
#
# Author: Claude
# Date: 2025-11-21
###############################################################################

# Set random seed for reproducibility
set.seed(42)

# Function to generate Specific IBNR data
generate_specific_ibnr_data <- function(num_records = 50) {
  #' Generate synthetic Specific IBNR data for Lloyd's SAO Addendum Return.
  #'
  #' @param num_records Number of records to generate
  #' @return Data frame with synthetic Specific IBNR data

  # Define Lloyd's CAT codes (Natural catastrophes)
  cat_codes <- c(
    '22E', '21E', '23E', '24E', '25E',  # Historic CAT events
    '26E', '27E', '28E', '29E', '30E',
    'Non Nat-Cat'  # Non-natural catastrophe events
  )

  # Define reserving classes
  reserving_classes <- c(
    'Prop Cat XL', 'Marine Hull', 'Aviation', 'Energy', 'Casualty',
    'D&O US', 'D&O UK', 'Professional Indemnity', 'Cyber',
    'Motor', 'Property Treaty', 'Property Direct', 'Marine Cargo',
    'Terrorism', 'Political Risk', 'Credit & Bond', 'Accident & Health'
  )

  # Define Lloyd's Lines of Business
  lloyds_lobs <- c(
    'Property Cat XL', 'Marine Hull', 'Aviation', 'Energy Offshore',
    'Casualty Treaty', 'D&O', 'Professional Indemnity', 'Cyber',
    'Motor', 'Property Treaty', 'Property Direct', 'Marine Cargo',
    'Terrorism', 'Political Risk', 'Credit & Surety', 'Accident & Health'
  )

  # Underwriting years
  underwriting_years <- 2010:2025

  # Generate year weights (favoring more recent years)
  year_weights <- exp(seq(-2, 0, length.out = length(underwriting_years)))
  year_weights <- year_weights / sum(year_weights)

  # Initialize data frame
  data <- data.frame(
    `Reserving Class` = character(num_records),
    `Lloyd's Cat Code` = character(num_records),
    `Lloyd's Line of Business` = character(num_records),
    `Number of losses` = integer(num_records),
    `Underwriting Year` = integer(num_records),
    `Gross IBNR (£000s)` = integer(num_records),
    `Net IBNR (£000s)` = integer(num_records),
    `Comment (optional)` = character(num_records),
    stringsAsFactors = FALSE,
    check.names = FALSE
  )

  # Generate records
  for (i in 1:num_records) {
    # Select random values
    cat_code <- sample(cat_codes, 1)
    reserving_class <- sample(reserving_classes, 1)

    # Map reserving class to appropriate Lloyd's LoB
    lob_index <- (match(reserving_class, reserving_classes) - 1) %% length(lloyds_lobs) + 1
    lloyds_lob <- lloyds_lobs[lob_index]

    # Generate random underwriting year (more recent years more likely)
    uw_year <- sample(underwriting_years, 1, prob = year_weights)

    # Number of losses
    num_losses <- sample(1:5, 1, prob = c(0.5, 0.25, 0.15, 0.07, 0.03))

    # Gross IBNR (£000s) - range from £1,000k to £50,000k (i.e., £1m to £50m gross)
    # Using lognormal distribution: meanlog=log(10000), sdlog=0.8 gives good range
    gross_ibnr <- max(1000, round(rlnorm(1, meanlog = log(10000), sdlog = 0.8), 0))

    # Net IBNR (70-95% of gross)
    net_percentage <- runif(1, 0.70, 0.95)
    net_ibnr <- round(gross_ibnr * net_percentage, 0)

    # Generate comment
    comments <- c(
      'Reserved using underlying cedant exposure and loss advice plus assumption on limits losses',
      'Based on industry loss estimates and exposure analysis',
      'Derived from actuarial model with management adjustments',
      'Estimated based on similar historical events',
      'Reserve includes uncertainty loading for emerging claims',
      'Subject to significant uncertainty due to limited data',
      ''
    )
    comment <- sample(comments, 1, prob = c(0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.10))

    # Populate data frame
    data[i, 'Reserving Class'] <- reserving_class
    data[i, "Lloyd's Cat Code"] <- cat_code
    data[i, "Lloyd's Line of Business"] <- lloyds_lob
    data[i, 'Number of losses'] <- num_losses
    data[i, 'Underwriting Year'] <- uw_year
    data[i, 'Gross IBNR (£000s)'] <- gross_ibnr
    data[i, 'Net IBNR (£000s)'] <- net_ibnr
    data[i, 'Comment (optional)'] <- ifelse(comment == '', NA, comment)
  }

  # Sort by Underwriting Year (descending) and Reserving Class
  data <- data[order(-data$`Underwriting Year`, data$`Reserving Class`), ]
  rownames(data) <- NULL

  return(data)
}

# Generate the data
specific_ibnr <- generate_specific_ibnr_data(num_records = 50)

# Display summary statistics
cat(paste(rep("=", 80), collapse = ""), "\n")
cat("SAO Addendum Return - 090 Specific IBNR Summary\n")
cat(paste(rep("=", 80), collapse = ""), "\n")
cat(sprintf("Total Records: %d\n", nrow(specific_ibnr)))
cat(sprintf("Total Gross IBNR: £%s k\n",
            format(sum(specific_ibnr$`Gross IBNR (£000s)`), big.mark = ",")))
cat(sprintf("Total Net IBNR: £%s k\n",
            format(sum(specific_ibnr$`Net IBNR (£000s)`), big.mark = ",")))
cat(sprintf("Underwriting Years: %d - %d\n",
            min(specific_ibnr$`Underwriting Year`),
            max(specific_ibnr$`Underwriting Year`)))
cat(sprintf("Number of CAT Events: %d\n",
            sum(specific_ibnr$`Lloyd's Cat Code` != 'Non Nat-Cat')))
cat(sprintf("Number of Non Nat-Cat Events: %d\n",
            sum(specific_ibnr$`Lloyd's Cat Code` == 'Non Nat-Cat')))
cat(paste(rep("=", 80), collapse = ""), "\n")
cat("\nFirst 10 records:\n")
print(head(specific_ibnr, 10))
cat("\n")

# This table will be available in Power BI
# Power BI will automatically detect the 'specific_ibnr' data frame
