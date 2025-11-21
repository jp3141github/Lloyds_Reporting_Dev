# Install Required R Packages for FSCS Data Generator
# ====================================================

# List of required packages
required_packages <- c(
  "dplyr",      # Data manipulation
  "tibble",     # Modern data frames
  "lubridate",  # Date handling
  "writexl"     # Excel export (no Java dependency)
)

# Function to install packages if not already installed
install_if_missing <- function(packages) {
  for (pkg in packages) {
    if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
      cat(sprintf("Installing %s...\n", pkg))
      install.packages(pkg, repos = "https://cran.r-project.org")
    } else {
      cat(sprintf("%s is already installed.\n", pkg))
    }
  }
}

# Install packages
cat("Checking and installing required packages...\n")
cat("=" %R% 50, "\n")

install_if_missing(required_packages)

cat("\n")
cat("All required packages are installed!\n")
cat("\nYou can now use the FSCS data generator.\n")

# Load packages to verify installation
cat("\nVerifying installation by loading packages...\n")
suppressPackageStartupMessages({
  library(dplyr)
  library(tibble)
  library(lubridate)
  library(writexl)
})

cat("All packages loaded successfully!\n")
