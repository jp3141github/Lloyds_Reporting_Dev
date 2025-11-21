# R Package Installation Script for Lloyd's Reporting
# Run this script to install all required R packages
# Usage: Rscript install_packages.R

cat("Installing required R packages for Lloyd's Reporting...\n\n")

# List of required packages
required_packages <- c(
  # Core data manipulation (tidyverse components)
  "dplyr",      # Data manipulation
  "tidyr",      # Data tidying
  "readr",      # Reading CSV files
  "purrr",      # Functional programming
  "tibble",     # Modern data frames

  # Date/time handling
  "lubridate",  # Date/time manipulation

  # Optional: For enhanced visualizations (if using R visuals in Power BI)
  "ggplot2",    # Data visualization
  "scales",     # Scale functions for ggplot2

  # Optional: For working with Excel files
  "readxl",     # Reading Excel files
  "writexl",    # Writing Excel files
  "openxlsx",   # Writing Excel files (for Solvency II claims processor)

  # Optional: For statistical modeling
  "stats",      # Base R statistics (already installed)
  "MASS",       # Additional statistical functions

  # Optional: For working with databases
  # "DBI",      # Database interface
  # "odbc",     # ODBC database connectivity
  # "RMySQL",   # MySQL connectivity
  # "RPostgres" # PostgreSQL connectivity
)

# Function to install packages if not already installed
install_if_missing <- function(package) {
  if (!require(package, character.only = TRUE, quietly = TRUE)) {
    cat(sprintf("Installing %s...\n", package))
    install.packages(package, dependencies = TRUE, repos = "https://cloud.r-project.org/")
    if (require(package, character.only = TRUE, quietly = TRUE)) {
      cat(sprintf("✓ Successfully installed %s\n", package))
    } else {
      cat(sprintf("✗ Failed to install %s\n", package))
    }
  } else {
    cat(sprintf("✓ %s is already installed\n", package))
  }
}

# Install all required packages
cat("\nChecking and installing packages...\n")
cat(rep("=", 60), "\n", sep = "")

lapply(required_packages, install_if_missing)

cat("\n", rep("=", 60), "\n", sep = "")
cat("Package installation complete!\n\n")

# Display installed package versions
cat("Installed package versions:\n")
cat(rep("=", 60), "\n", sep = "")

for (pkg in required_packages) {
  if (require(pkg, character.only = TRUE, quietly = TRUE)) {
    version <- packageVersion(pkg)
    cat(sprintf("%-15s : %s\n", pkg, version))
  }
}

cat("\n", rep("=", 60), "\n", sep = "")
cat("Setup complete! You can now use the R scripts for Lloyd's reporting.\n")
