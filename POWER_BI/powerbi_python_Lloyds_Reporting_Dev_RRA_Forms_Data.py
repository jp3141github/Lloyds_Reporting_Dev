import sys
import os
import pandas as pd

REPO_PATH = r'C:\Users\James\VS_Code_Python\Lloyds_Reporting\Lloyds_Reporting_Dev'

# Load RRA synthetic data directly
rra_010 = pd.read_csv(os.path.join(REPO_PATH, 'synthetic_data', 'rra_010_control.csv'))
rra_193 = pd.read_csv(os.path.join(REPO_PATH, 'synthetic_data', 'rra_193_net_claims.csv'))
rra_291 = pd.read_csv(os.path.join(REPO_PATH, 'synthetic_data', 'rra_291_gross_premium_ibnr.csv'))
rra_292 = pd.read_csv(os.path.join(REPO_PATH, 'synthetic_data', 'rra_292_net_premium_ibnr.csv'))
rra_990 = pd.read_csv(os.path.join(REPO_PATH, 'synthetic_data', 'rra_990_validation.csv'))