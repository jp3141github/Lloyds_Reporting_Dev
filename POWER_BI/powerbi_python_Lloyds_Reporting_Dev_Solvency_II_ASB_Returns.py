import sys
import os

REPO_PATH = r'C:\Users\James\VS_Code_Python\Lloyds_Reporting\Lloyds_Reporting_Dev'

sys.path.append(os.path.join(REPO_PATH, 'Solvency_II_ASB_Python'))

from synthetic_data_generator import LloydsDataGenerator
from powerbi_asb_returns import ASBReturnsProcessor

gen = LloydsDataGenerator()
data = gen.generate_all_data()

processor = ASBReturnsProcessor()
asb_245 = processor.process_asb_245(data)
asb_246 = processor.process_asb_246(data)
asb_247 = processor.process_asb_247(data)
asb_248 = processor.process_asb_248(data)