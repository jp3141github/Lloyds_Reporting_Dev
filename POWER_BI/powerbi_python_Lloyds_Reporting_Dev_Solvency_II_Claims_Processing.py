import sys
import os

REPO_PATH = r'C:\Users\James\VS_Code_Python\Lloyds_Reporting\Lloyds_Reporting_Dev'

sys.path.append(os.path.join(REPO_PATH, 'python_scripts'))

from solvency_claims_processor import process_claims_data

input_file = os.path.join(REPO_PATH, 'synthetic_data', 'synthetic_lloyds_claims_data.xlsx')

output_tables = process_claims_data(input_file, sheet_name='input Sheet')

detailed_claims = output_tables['detailed_claims']
by_syndicate = output_tables['by_syndicate']
by_risk_code = output_tables['by_risk_code']
by_claim_status = output_tables['by_claim_status']
summary = output_tables['summary']