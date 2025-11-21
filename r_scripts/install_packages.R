# Install required R packages for Solvency II Claims Processing

# List of required packages
required_packages <- c(
  "readxl",      # Reading Excel files
  "dplyr",       # Data manipulation
  "tidyr",       # Data tidying
  "openxlsx"     # Writing Excel files
)

# Function to install packages if not already installed
install_if_missing <- function(packages) {
  for (package in packages) {
    if (!require(package, character.only = TRUE, quietly = TRUE)) {
      cat(paste("Installing", package, "...\n"))
      install.packages(package, dependencies = TRUE)
    } else {
      cat(paste(package, "is already installed.\n"))
    }
  }
}

# Install packages
cat("Checking and installing required packages...\n\n")
install_if_missing(required_packages)

cat("\n=== Package Installation Complete ===\n")
cat("All required packages are now installed.\n")
cat("You can now run the solvency_claims_processor.R script.\n")
