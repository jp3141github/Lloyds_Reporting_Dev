import sys
import os

REPO_PATH = r'C:\Users\James\VS_Code_Python\Lloyds_Reporting\Lloyds_Reporting_Dev'
DATA_DIR = os.path.join(REPO_PATH, 'Solvency_II_QSR_Reporting', 'Data') + os.sep

sys.path.append(os.path.join(REPO_PATH, 'Solvency_II_QSR_Reporting', 'Python'))

from qsr_report_generator import QSRReportGenerator

generator = QSRReportGenerator(data_dir=DATA_DIR)
generator.load_data()
reports = generator.generate_all_reports()

qsr_summary = reports['SCR_Summary']
qsr_claims = reports['QSR440_Premiums_Claims']
qsr_premiums = reports['QSR002_Balance_Sheet']