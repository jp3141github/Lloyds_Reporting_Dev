import sys
import os
import pandas as pd

REPO_PATH = r'C:\Users\James\VS_Code_Python\Lloyds_Reporting\Lloyds_Reporting_Dev'

sys.path.append(os.path.join(REPO_PATH, 'FSCS_PowerBI', 'Python'))

from fscs_data_generator import FSCSDataGenerator

gen = FSCSDataGenerator(random_seed=123)

summary_frames = []
detail_frames = []
for year in range(2018, 2026):
    gen.reporting_year = year
    summary_frames.append(gen.generate_fscs_output_format())
    detail_frames.append(gen.generate_detail_dataset())

summary_df = pd.concat(summary_frames, ignore_index=True)
detail_df = pd.concat(detail_frames, ignore_index=True)

fscs_summary = summary_df
fscs_detail = detail_df