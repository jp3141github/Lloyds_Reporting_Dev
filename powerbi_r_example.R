# Power BI R Script Example
# Copy this script into Power BI's R script data source
#
# Instructions:
# 1. In Power BI Desktop, click 'Get Data' -> 'More' -> 'R script'
# 2. Copy and paste this entire script
# 3. Update the paths below to match your system
# 4. Click OK and select which tables to load

# UPDATE THIS PATH to where you cloned the repository
REPO_PATH <- 'C:/path/to/Lloyds_Reporting_Dev'

# Source the processor script
source(file.path(REPO_PATH, 'r_scripts', 'solvency_claims_processor.R'))

# UPDATE THIS PATH to your data file
# Use the synthetic data for testing, then replace with your actual data
input_file <- file.path(REPO_PATH, 'synthetic_data', 'synthetic_lloyds_claims_data.xlsx')

# Process the claims data
cat(paste("Loading data from:", input_file, "\n"))
output_tables <- process_claims_data(input_file)

# These variables will be available as separate tables in Power BI
# Select which ones you want to import
detailed_claims <- output_tables$detailed_claims
by_syndicate <- output_tables$by_syndicate
by_risk_code <- output_tables$by_risk_code
by_claim_status <- output_tables$by_claim_status
summary <- output_tables$summary

cat(paste("Successfully processed", nrow(detailed_claims), "claims\n"))
cat("Tables available: detailed_claims, by_syndicate, by_risk_code, by_claim_status, summary\n")
