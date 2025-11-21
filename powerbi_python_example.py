"""
Power BI Python Script Example
Copy this script into Power BI's Python script data source

Instructions:
1. In Power BI Desktop, click 'Get Data' -> 'More' -> 'Python script'
2. Copy and paste this entire script
3. Update the paths below to match your system
4. Click OK and select which tables to load
"""

import sys
import os

# UPDATE THIS PATH to where you cloned the repository
REPO_PATH = r'C:\path\to\Lloyds_Reporting_Dev'

# Add the python_scripts directory to the path
sys.path.append(os.path.join(REPO_PATH, 'python_scripts'))

# Import the processor
from solvency_claims_processor import process_claims_data

# UPDATE THIS PATH to your data file
# Use the synthetic data for testing, then replace with your actual data
input_file = os.path.join(REPO_PATH, 'synthetic_data', 'synthetic_lloyds_claims_data.xlsx')

# Process the claims data
print(f"Loading data from: {input_file}")
output_tables = process_claims_data(input_file, sheet_name='input Sheet')

# These variables will be available as separate tables in Power BI
# Select which ones you want to import
detailed_claims = output_tables['detailed_claims']
by_syndicate = output_tables['by_syndicate']
by_risk_code = output_tables['by_risk_code']
by_claim_status = output_tables['by_claim_status']
summary = output_tables['summary']

print(f"Successfully processed {len(detailed_claims)} claims")
print(f"Tables available: detailed_claims, by_syndicate, by_risk_code, by_claim_status, summary")
