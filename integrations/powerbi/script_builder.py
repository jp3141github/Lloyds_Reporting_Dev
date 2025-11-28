"""
Power BI Script Builder
=======================

Generates Python scripts for use in Power BI Desktop's Python script connector.
"""

from typing import List, Optional, Dict
from datetime import datetime


class ScriptBuilder:
    """
    Build Power BI-compatible Python scripts.

    Generates self-contained scripts that can be pasted directly into
    Power BI Desktop's Python script data source.
    """

    HEADER_TEMPLATE = '''"""
Lloyd's Regulatory Reporting Data for Power BI
Generated: {timestamp}
Categories: {categories}

Usage:
1. Open Power BI Desktop
2. Get Data > Python script
3. Paste this entire script
4. Click OK and select tables to import
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

'''

    def __init__(self):
        """Initialize the script builder."""
        pass

    def build_script(self, datasets: List[str], include_all: bool = False) -> str:
        """
        Build a Power BI Python script.

        Args:
            datasets: List of dataset names to include
            include_all: If True, include all available datasets

        Returns:
            Complete Python script as string
        """
        categories = self._categorize_datasets(datasets)

        script_parts = [
            self.HEADER_TEMPLATE.format(
                timestamp=datetime.now().isoformat(),
                categories=', '.join(categories)
            ),
            self._build_config_section(),
            self._build_helper_functions(),
        ]

        # Add dataset-specific generators
        for category in categories:
            script_parts.append(self._get_category_generator(category))

        # Add main execution block
        script_parts.append(self._build_main_block(categories))

        return '\n'.join(script_parts)

    def build_minimal_script(self, category: str) -> str:
        """
        Build a minimal script for a single category.

        Args:
            category: Category name (e.g., 'rra', 'qsr', 'lcr')

        Returns:
            Minimal Python script as string
        """
        return self.HEADER_TEMPLATE.format(
            timestamp=datetime.now().isoformat(),
            categories=category
        ) + self._build_config_section() + \
            self._build_helper_functions() + \
            self._get_category_generator(category) + \
            f"\n# Generate {category.upper()} data\n" + \
            f"datasets = generate_{category}_data()\n" + \
            "for name, df in datasets.items():\n" + \
            "    globals()[name] = df\n"

    def _categorize_datasets(self, datasets: List[str]) -> List[str]:
        """Categorize datasets by prefix."""
        categories = set()
        for ds in datasets:
            prefix = ds.split('_')[0].lower()
            if prefix in ['rra', 'rrq', 'qsr', 'asb', 'lcr', 'sbf', 'qma', 'fscs', 'liquidity', 'claims', 'qrt']:
                categories.add(prefix)
        return sorted(categories) if categories else ['rra']  # Default to RRA

    def _build_config_section(self) -> str:
        """Build configuration section."""
        return '''
# =============================================================================
# CONFIGURATION
# =============================================================================

SYNDICATES = [2987, 33, 1183, 2791, 623, 4242, 5000, 1910, 2010, 2525]
YEARS_OF_ACCOUNT = list(range(2018, 2026))
CURRENT_YEAR = 2024
LOB_CODES = ['A1', 'M1', 'P1', 'E1', 'F1']
LOB_NAMES = {
    'A1': 'Accident & Health',
    'M1': 'Marine',
    'P1': 'Property',
    'E1': 'Energy',
    'F1': 'Fire',
}
CURRENCIES = ['GBP', 'USD', 'EUR']

'''

    def _build_helper_functions(self) -> str:
        """Build common helper functions."""
        return '''
# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_syndicate_list():
    """Generate syndicate control data."""
    data = []
    for syn in SYNDICATES:
        data.append({
            'Syndicate_Number': syn,
            'Managing_Agent': f'Managing Agent {syn}',
            'Status': random.choice(['Active', 'Active']),
        })
    return pd.DataFrame(data)

def generate_development_factor(dev_year):
    """Calculate development factor."""
    return min(1.0, 0.2 + dev_year * 0.15)

'''

    def _get_category_generator(self, category: str) -> str:
        """Get the generator code for a specific category."""
        generators = {
            'rra': self._rra_generator(),
            'rrq': self._rrq_generator(),
            'qsr': self._qsr_generator(),
            'asb': self._asb_generator(),
            'lcr': self._lcr_generator(),
            'sbf': self._sbf_generator(),
            'qma': self._qma_generator(),
            'fscs': self._fscs_generator(),
            'liquidity': self._liquidity_generator(),
            'claims': self._claims_generator(),
        }
        return generators.get(category, '')

    def _rra_generator(self) -> str:
        return '''
# =============================================================================
# RRA FORM GENERATORS
# =============================================================================

def generate_rra_data():
    """Generate all RRA form datasets."""
    datasets = {}

    # RRA 010 - Control Data
    control_data = []
    for syn in SYNDICATES:
        control_data.append({
            'Syndicate_Number': syn,
            'Return_Type': 'RRA',
            'Status': random.choice(['Draft', 'Submitted', 'Approved']),
            'Managing_Agent': f'Managing Agent {syn}',
            'Reporting_Year': CURRENT_YEAR,
        })
    datasets['RRA_010_Control'] = pd.DataFrame(control_data)

    # RRA 193 - Net Claims
    claims_data = []
    for syn in SYNDICATES:
        for year in YEARS_OF_ACCOUNT[:-1]:
            for lob in LOB_CODES:
                for dev in range(min(8, CURRENT_YEAR - year + 1)):
                    base = random.randint(1_000_000, 20_000_000)
                    lr = random.uniform(0.45, 0.85)
                    df = generate_development_factor(dev)
                    claims_data.append({
                        'Syndicate_Number': syn,
                        'Year_of_Account': year,
                        'Development_Year': dev,
                        'LOB_Code': lob,
                        'Cumulative_Paid': int(base * lr * df),
                        'Case_Reserves': int(base * lr * (1-df) * 0.6),
                        'IBNR': int(base * lr * (1-df) * 0.4),
                    })
    datasets['RRA_193_NetClaims'] = pd.DataFrame(claims_data)

    # RRA 291 - Gross Premium & IBNR
    premium_data = []
    for syn in SYNDICATES:
        for year in YEARS_OF_ACCOUNT[:-1]:
            for lob in LOB_CODES:
                gwp = random.randint(5_000_000, 50_000_000)
                ulr = random.uniform(0.55, 0.75)
                premium_data.append({
                    'Syndicate_Number': syn,
                    'Year_of_Account': year,
                    'LOB_Code': lob,
                    'Gross_Written_Premium': gwp,
                    'IBNR_Best_Estimate': int(gwp * ulr * random.uniform(0.15, 0.35)),
                    'Ultimate_Loss_Ratio': round(ulr, 4),
                })
    datasets['RRA_291_GrossPremiumIBNR'] = pd.DataFrame(premium_data)

    # RRA Summary
    summary_data = []
    for syn in SYNDICATES:
        gwp = random.randint(100_000_000, 500_000_000)
        summary_data.append({
            'Syndicate_Number': syn,
            'Gross_Written_Premium': gwp,
            'Net_Written_Premium': int(gwp * 0.8),
            'Ultimate_Loss_Ratio': round(random.uniform(0.55, 0.75), 4),
            'Combined_Ratio': round(random.uniform(0.90, 1.05), 4),
        })
    datasets['RRA_Summary'] = pd.DataFrame(summary_data)

    return datasets

'''

    def _rrq_generator(self) -> str:
        return '''
# =============================================================================
# RRQ FORM GENERATORS
# =============================================================================

def generate_rrq_data():
    """Generate RRQ (Quarterly) form datasets."""
    datasets = {}

    quarters = ['Q1', 'Q2', 'Q3', 'Q4']

    # RRQ Control
    control_data = []
    for syn in SYNDICATES:
        for q in quarters:
            control_data.append({
                'Syndicate_Number': syn,
                'Return_Type': 'RRQ',
                'Quarter': f'{CURRENT_YEAR}-{q}',
                'Status': random.choice(['Draft', 'Submitted']),
            })
    datasets['RRQ_010_Control'] = pd.DataFrame(control_data)

    # RRQ Claims
    claims_data = []
    for syn in SYNDICATES:
        for q in quarters:
            for lob in LOB_CODES:
                claims_data.append({
                    'Syndicate_Number': syn,
                    'Quarter': f'{CURRENT_YEAR}-{q}',
                    'LOB_Code': lob,
                    'Cumulative_Paid': random.randint(1_000_000, 20_000_000),
                    'Case_Reserves': random.randint(500_000, 10_000_000),
                    'IBNR': random.randint(200_000, 5_000_000),
                })
    datasets['RRQ_193_NetClaims'] = pd.DataFrame(claims_data)

    return datasets

'''

    def _qsr_generator(self) -> str:
        return '''
# =============================================================================
# QSR (QUARTERLY SOLVENCY RETURN) GENERATORS
# =============================================================================

def generate_qsr_data():
    """Generate QSR datasets."""
    datasets = {}

    # Balance Sheet
    bs_data = []
    for syn in SYNDICATES:
        total = random.randint(500_000_000, 2_000_000_000)
        bs_data.append({
            'Syndicate_Number': syn,
            'Total_Assets': total,
            'Investments': int(total * 0.6),
            'Technical_Provisions': int(total * 0.6),
            'Own_Funds': int(total * 0.25),
        })
    datasets['QSR_BalanceSheet'] = pd.DataFrame(bs_data)

    # SCR Summary
    scr_data = []
    for syn in SYNDICATES:
        scr = random.randint(80_000_000, 300_000_000)
        of = int(scr * random.uniform(1.2, 2.5))
        scr_data.append({
            'Syndicate_Number': syn,
            'Own_Funds': of,
            'SCR': scr,
            'Coverage_Ratio': round(of / scr, 4),
            'Market_Risk': int(scr * 0.25),
            'Underwriting_Risk': int(scr * 0.45),
            'Operational_Risk': int(scr * 0.08),
        })
    datasets['QSR_SCR_Summary'] = pd.DataFrame(scr_data)

    return datasets

'''

    def _asb_generator(self) -> str:
        return '''
# =============================================================================
# ASB (ANNUAL SOLVENCY BALANCE SHEET) GENERATORS
# =============================================================================

def generate_asb_data():
    """Generate ASB datasets."""
    datasets = {}

    # Claims Triangle
    triangle_data = []
    for syn in SYNDICATES[:5]:
        for origin in range(2015, 2024):
            for dev in range(2024 - origin + 1):
                base = random.randint(5_000_000, 50_000_000)
                triangle_data.append({
                    'Syndicate_Number': syn,
                    'Origin_Year': origin,
                    'Development_Year': dev,
                    'Cumulative_Paid': int(base * min(1, 0.1 + dev * 0.12)),
                    'Cumulative_Incurred': int(base * min(1, 0.15 + dev * 0.12)),
                })
    datasets['ASB_ClaimsTriangle'] = pd.DataFrame(triangle_data)

    # Development Factors
    factors_data = []
    for lob in LOB_CODES:
        for dev in range(10):
            factors_data.append({
                'LOB_Code': lob,
                'Development_Year': dev,
                'Paid_Factor': round(random.uniform(1.0, 2.5) if dev < 5 else 1.05, 4),
                'Incurred_Factor': round(random.uniform(1.0, 2.0) if dev < 5 else 1.02, 4),
            })
    datasets['ASB_DevelopmentFactors'] = pd.DataFrame(factors_data)

    return datasets

'''

    def _lcr_generator(self) -> str:
        return '''
# =============================================================================
# LCR (LLOYD'S CAPITAL RETURN) GENERATORS
# =============================================================================

def generate_lcr_data():
    """Generate LCR datasets."""
    datasets = {}

    # SCR Summary
    scr_data = []
    for syn in SYNDICATES:
        scr = random.randint(80_000_000, 300_000_000)
        scr_data.append({
            'Syndicate_Number': syn,
            'Premium_Risk': int(scr * 0.20),
            'Reserve_Risk': int(scr * 0.25),
            'Cat_Risk': int(scr * 0.15),
            'Market_Risk': int(scr * 0.20),
            'Credit_Risk': int(scr * 0.08),
            'Operational_Risk': int(scr * 0.07),
            'Total_SCR': scr,
        })
    datasets['LCR_SCR_Summary'] = pd.DataFrame(scr_data)

    # Cat Risk by Peril
    perils = ['US_Hurricane', 'EU_Windstorm', 'JP_Earthquake', 'Cyber', 'Pandemic']
    cat_data = []
    for syn in SYNDICATES:
        for peril in perils:
            gross = random.randint(50_000_000, 500_000_000)
            cat_data.append({
                'Syndicate_Number': syn,
                'Peril': peril,
                'Gross_Loss': gross,
                'RI_Recovery': int(gross * random.uniform(0.40, 0.60)),
                'Net_Loss': int(gross * random.uniform(0.40, 0.60)),
            })
    datasets['LCR_CatRisk'] = pd.DataFrame(cat_data)

    # Coverage Ratios
    coverage_data = []
    for syn in SYNDICATES:
        scr = random.randint(80_000_000, 300_000_000)
        of = int(scr * random.uniform(1.2, 2.5))
        coverage_data.append({
            'Syndicate_Number': syn,
            'Own_Funds': of,
            'SCR': scr,
            'Coverage_Ratio': round(of / scr, 4),
            'Excess_Capital': of - scr,
        })
    datasets['LCR_Coverage'] = pd.DataFrame(coverage_data)

    return datasets

'''

    def _sbf_generator(self) -> str:
        return '''
# =============================================================================
# SBF (SYNDICATE BUSINESS FORECAST) GENERATORS
# =============================================================================

def generate_sbf_data():
    """Generate SBF datasets."""
    datasets = {}

    # Income Statement Forecast
    income_data = []
    for syn in SYNDICATES:
        for year in [2024, 2025, 2026]:
            gwp = random.randint(100_000_000, 500_000_000)
            income_data.append({
                'Syndicate_Number': syn,
                'Forecast_Year': year,
                'Gross_Written_Premium': gwp,
                'Net_Earned_Premium': int(gwp * 0.8),
                'Claims_Incurred': int(gwp * random.uniform(0.50, 0.70)),
                'Underwriting_Result': int(gwp * random.uniform(-0.05, 0.15)),
            })
    datasets['SBF_IncomeStatement'] = pd.DataFrame(income_data)

    # Combined Ratios
    ratio_data = []
    for syn in SYNDICATES:
        for year in [2024, 2025, 2026]:
            lr = random.uniform(0.55, 0.72)
            er = random.uniform(0.28, 0.38)
            ratio_data.append({
                'Syndicate_Number': syn,
                'Forecast_Year': year,
                'Loss_Ratio': round(lr, 4),
                'Expense_Ratio': round(er, 4),
                'Combined_Ratio': round(lr + er, 4),
            })
    datasets['SBF_Ratios'] = pd.DataFrame(ratio_data)

    return datasets

'''

    def _qma_generator(self) -> str:
        return '''
# =============================================================================
# QMA (QUARTERLY MONITORING) GENERATORS
# =============================================================================

def generate_qma_data():
    """Generate QMA datasets."""
    datasets = {}
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']

    # P&L Statement
    pl_data = []
    for syn in SYNDICATES:
        for q in quarters:
            premium = random.randint(20_000_000, 100_000_000)
            pl_data.append({
                'Syndicate_Number': syn,
                'Quarter': f'{CURRENT_YEAR}-{q}',
                'Net_Earned_Premium': premium,
                'Claims_Incurred': int(premium * random.uniform(0.50, 0.70)),
                'Operating_Expenses': int(premium * random.uniform(0.25, 0.35)),
                'Profit_Before_Tax': int(premium * random.uniform(-0.05, 0.20)),
            })
    datasets['QMA_ProfitLoss'] = pd.DataFrame(pl_data)

    # Key Ratios
    ratio_data = []
    for syn in SYNDICATES:
        ratio_data.append({
            'Syndicate_Number': syn,
            'Loss_Ratio': round(random.uniform(0.55, 0.72), 4),
            'Expense_Ratio': round(random.uniform(0.28, 0.38), 4),
            'Combined_Ratio': round(random.uniform(0.88, 1.05), 4),
            'Return_on_Capital': round(random.uniform(0.05, 0.20), 4),
        })
    datasets['QMA_KeyRatios'] = pd.DataFrame(ratio_data)

    return datasets

'''

    def _fscs_generator(self) -> str:
        return '''
# =============================================================================
# FSCS GENERATORS
# =============================================================================

def generate_fscs_data():
    """Generate FSCS datasets."""
    datasets = {}

    fscs_data = []
    for syn in SYNDICATES:
        for year in range(2020, 2025):
            fscs_data.append({
                'Syndicate_Number': syn,
                'Year': year,
                'Protected_Liabilities': random.randint(10_000_000, 100_000_000),
                'FSCS_Levy': random.randint(100_000, 2_000_000),
            })
    datasets['FSCS_Summary'] = pd.DataFrame(fscs_data)

    return datasets

'''

    def _liquidity_generator(self) -> str:
        return '''
# =============================================================================
# LIQUIDITY STRESS TEST GENERATORS
# =============================================================================

def generate_liquidity_data():
    """Generate Liquidity datasets."""
    datasets = {}

    # Capital Position
    capital_data = []
    for syn in SYNDICATES:
        fal = random.randint(100_000_000, 500_000_000)
        capital_data.append({
            'Syndicate_Number': syn,
            'FAL': fal,
            'FIS': int(fal * random.uniform(0.80, 0.95)),
            'uSCR': int(fal * random.uniform(0.60, 0.85)),
            'Excess_Capital': int(fal * random.uniform(0.15, 0.40)),
        })
    datasets['Liquidity_Capital'] = pd.DataFrame(capital_data)

    # Stress Scenarios
    scenarios = ['Base', 'Adverse', '1-in-200']
    stress_data = []
    for syn in SYNDICATES:
        for scenario in scenarios:
            mult = {'Base': 1.0, 'Adverse': 1.5, '1-in-200': 2.5}[scenario]
            base = random.randint(50_000_000, 200_000_000)
            stress_data.append({
                'Syndicate_Number': syn,
                'Scenario': scenario,
                'Gross_Loss': int(base * mult),
                'Net_Loss': int(base * mult * random.uniform(0.40, 0.60)),
            })
    datasets['Liquidity_Stress'] = pd.DataFrame(stress_data)

    return datasets

'''

    def _claims_generator(self) -> str:
        return '''
# =============================================================================
# CLAIMS ANALYSIS GENERATORS
# =============================================================================

def generate_claims_data():
    """Generate Claims datasets."""
    datasets = {}

    # Detailed Claims
    claims_data = []
    statuses = ['Open', 'Closed', 'Reopened']
    for _ in range(500):
        claims_data.append({
            'Claim_Reference': f'CLM{random.randint(100000, 999999)}',
            'Syndicate_Number': random.choice(SYNDICATES),
            'Year_of_Account': random.choice(YEARS_OF_ACCOUNT),
            'Status': random.choice(statuses),
            'Outstanding': random.randint(10000, 500000),
            'Paid': random.randint(5000, 300000),
        })
    datasets['Claims_Detail'] = pd.DataFrame(claims_data)

    # Claims by Syndicate
    syn_claims = []
    for syn in SYNDICATES:
        syn_claims.append({
            'Syndicate_Number': syn,
            'Total_Claims': random.randint(100, 1000),
            'Total_Outstanding': random.randint(10_000_000, 100_000_000),
            'Total_Paid': random.randint(5_000_000, 80_000_000),
        })
    datasets['Claims_BySyndicate'] = pd.DataFrame(syn_claims)

    return datasets

'''

    def _build_main_block(self, categories: List[str]) -> str:
        """Build the main execution block."""
        generators = [f"generate_{cat}_data()" for cat in categories]

        return f'''
# =============================================================================
# MAIN EXECUTION
# =============================================================================

# Generate all datasets
all_datasets = {{}}
{''.join(f"all_datasets.update({gen})" + chr(10) for gen in generators)}

# Make each dataset available as a separate DataFrame for Power BI
for name, df in all_datasets.items():
    globals()[name] = df

# Print summary
print(f"Generated {{len(all_datasets)}} datasets:")
for name, df in all_datasets.items():
    print(f"  {{name}}: {{len(df)}} rows")
'''

    def generate_full_script(self, categories: List[str]) -> str:
        """
        Generate a full Power BI Python script.

        Alias for build_script() for API compatibility.

        Args:
            categories: List of data categories to include

        Returns:
            Complete Python script as string
        """
        return self.build_script(categories)
