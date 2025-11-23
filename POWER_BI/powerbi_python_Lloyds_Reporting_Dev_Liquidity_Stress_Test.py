import sys
import os

REPO_PATH = r'C:\Users\James\VS_Code_Python\Lloyds_Reporting\Lloyds_Reporting_Dev'

sys.path.append(os.path.join(REPO_PATH, 'python_implementation'))

from liquidity_stress_test import LiquidityStressTest

lst = LiquidityStressTest(os.path.join(REPO_PATH, 'data'))
lst.load_data()

capital_position = lst.calculate_capital_position_table()
liquidity_breakdown = lst.calculate_liquidity_breakdown_table()
cashflow_summary = lst.calculate_cashflow_summary_table()
stress_impact = lst.calculate_stress_impact_table()
dashboard_summary = lst.create_dashboard_summary()