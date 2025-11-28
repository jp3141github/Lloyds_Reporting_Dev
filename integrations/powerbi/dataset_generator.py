"""
Power BI Dataset Generator
==========================

Generates synthetic datasets optimized for Power BI visualization.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import random
import sys
from pathlib import Path

# Add parent paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from lloyds_reporting.config import (
        SYNDICATES_PRIMARY,
        CLASSES_OF_BUSINESS,
        CURRENCIES,
        YEARS_OF_ACCOUNT,
        CURRENT_YEAR,
        DevelopmentFactors,
        CapitalRatios,
    )
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    SYNDICATES_PRIMARY = [2987, 33, 1183, 2791, 623, 4242, 5000, 1910, 2010, 2525]
    CLASSES_OF_BUSINESS = {'A1': 'Accident & Health', 'M1': 'Marine', 'P1': 'Property'}
    CURRENCIES = ['GBP', 'USD', 'EUR']
    YEARS_OF_ACCOUNT = list(range(2018, 2026))
    CURRENT_YEAR = 2024


class DatasetGenerator:
    """
    Generate synthetic datasets for Power BI consumption.

    All methods return dictionaries of DataFrames ready for Power BI.
    """

    def __init__(self, seed: int = 42):
        """Initialize with random seed for reproducibility."""
        self.seed = seed
        np.random.seed(seed)
        random.seed(seed)

        self.syndicates = SYNDICATES_PRIMARY
        self.lob_codes = list(CLASSES_OF_BUSINESS.keys())
        self.lob_names = CLASSES_OF_BUSINESS
        self.currencies = CURRENCIES
        self.years = YEARS_OF_ACCOUNT
        self.current_year = CURRENT_YEAR

    # =========================================================================
    # RRA FORMS
    # =========================================================================

    def generate_rra_forms(self) -> Dict[str, pd.DataFrame]:
        """Generate all RRA form datasets."""
        return {
            '010_Control': self._generate_control_data('RRA'),
            '020_ExchangeRates': self._generate_exchange_rates(),
            '193_NetClaims': self._generate_net_claims(),
            '291_GrossPremiumIBNR': self._generate_gross_premium_ibnr(),
            '292_NetPremiumIBNR': self._generate_net_premium_ibnr(),
            '990_Validation': self._generate_validation_summary(),
            'DevelopmentTriangle': self._generate_development_triangle(),
            'SyndicateSummary': self._generate_syndicate_summary(),
        }

    def generate_rrq_forms(self) -> Dict[str, pd.DataFrame]:
        """Generate RRQ form datasets."""
        return {
            '010_Control': self._generate_control_data('RRQ'),
            '020_ExchangeRates': self._generate_exchange_rates(),
            '193_NetClaims': self._generate_net_claims(quarterly=True),
            '291_GrossPremiumIBNR': self._generate_gross_premium_ibnr(quarterly=True),
        }

    # =========================================================================
    # SOLVENCY II RETURNS
    # =========================================================================

    def generate_qsr_data(self) -> Dict[str, pd.DataFrame]:
        """Generate Quarterly Solvency Return datasets."""
        return {
            'BalanceSheet': self._generate_balance_sheet(),
            'OwnFunds': self._generate_own_funds(),
            'TechnicalProvisions': self._generate_technical_provisions(),
            'SCR_Summary': self._generate_scr_summary(),
            'MCR_Calculation': self._generate_mcr_calculation(),
            'SolvencyRatio': self._generate_solvency_ratio(),
        }

    def generate_asb_data(self) -> Dict[str, pd.DataFrame]:
        """Generate Annual Solvency Balance Sheet datasets."""
        return {
            'ClaimsGross': self._generate_asb_claims('Gross'),
            'ClaimsNet': self._generate_asb_claims('Net'),
            'ClaimsReinsurance': self._generate_asb_claims('Reinsurance'),
            'DevelopmentFactors': self._generate_development_factors(),
            'InflationRates': self._generate_inflation_rates(),
        }

    # =========================================================================
    # LLOYD'S SPECIFIC RETURNS
    # =========================================================================

    def generate_lcr_data(self) -> Dict[str, pd.DataFrame]:
        """Generate Lloyd's Capital Return datasets."""
        return {
            'SCR_Summary': self._generate_lcr_scr(),
            'PremiumRisk': self._generate_lcr_premium_risk(),
            'ReserveRisk': self._generate_lcr_reserve_risk(),
            'CatRisk': self._generate_lcr_cat_risk(),
            'MarketRisk': self._generate_lcr_market_risk(),
            'CoverageRatios': self._generate_lcr_coverage(),
        }

    def generate_sbf_data(self) -> Dict[str, pd.DataFrame]:
        """Generate Syndicate Business Forecast datasets."""
        return {
            'IncomeStatement': self._generate_sbf_income(),
            'PremiumForecast': self._generate_sbf_premium(),
            'ClaimsForecast': self._generate_sbf_claims(),
            'CombinedRatios': self._generate_sbf_ratios(),
        }

    def generate_qma_data(self) -> Dict[str, pd.DataFrame]:
        """Generate Quarterly Monitoring datasets."""
        return {
            'BalanceSheet': self._generate_qma_balance_sheet(),
            'ProfitLoss': self._generate_qma_pl(),
            'TechnicalAccount': self._generate_qma_technical(),
            'KeyRatios': self._generate_qma_ratios(),
        }

    # =========================================================================
    # OTHER DATASETS
    # =========================================================================

    def generate_fscs_data(self) -> Dict[str, pd.DataFrame]:
        """Generate FSCS datasets."""
        return {
            'Summary': self._generate_fscs_summary(),
            'Detail': self._generate_fscs_detail(),
        }

    def generate_liquidity_data(self) -> Dict[str, pd.DataFrame]:
        """Generate Liquidity Stress Testing datasets."""
        return {
            'CapitalPosition': self._generate_liquidity_capital(),
            'AssetBreakdown': self._generate_liquidity_assets(),
            'CashflowSummary': self._generate_liquidity_cashflow(),
            'StressImpact': self._generate_liquidity_stress(),
        }

    def generate_claims_data(self) -> Dict[str, pd.DataFrame]:
        """Generate Claims Analysis datasets."""
        return {
            'DetailedClaims': self._generate_detailed_claims(),
            'BySyndicate': self._generate_claims_by_syndicate(),
            'ByRiskCode': self._generate_claims_by_risk(),
            'ByStatus': self._generate_claims_by_status(),
        }

    # =========================================================================
    # HELPER METHODS - COMMON DATA
    # =========================================================================

    def _generate_control_data(self, return_type: str) -> pd.DataFrame:
        """Generate control data for RRA/RRQ."""
        data = []
        for syn in self.syndicates:
            data.append({
                'Syndicate_Number': syn,
                'Return_Type': return_type,
                'Status': random.choice(['Draft', 'Submitted', 'Approved']),
                'Managing_Agent': f'Managing Agent {syn}',
                'Reporting_Year': self.current_year,
                'Submission_Date': datetime.now().strftime('%Y-%m-%d'),
            })
        return pd.DataFrame(data)

    def _generate_exchange_rates(self) -> pd.DataFrame:
        """Generate exchange rate data."""
        base_rates = {'GBP': 1.00, 'USD': 1.27, 'EUR': 1.17, 'CAD': 1.72, 'AUD': 1.95, 'JPY': 188.5}
        data = []
        for year in self.years:
            for curr, rate in base_rates.items():
                data.append({
                    'Year_of_Account': year,
                    'Currency': curr,
                    'Exchange_Rate_GBP': round(rate * random.uniform(0.95, 1.05), 4),
                    'Rate_Type': 'Average',
                })
        return pd.DataFrame(data)

    def _generate_net_claims(self, quarterly: bool = False) -> pd.DataFrame:
        """Generate net claims development data."""
        data = []
        for syn in self.syndicates:
            for year in self.years[:-1]:
                for lob in self.lob_codes[:5]:
                    for dev_year in range(min(8, self.current_year - year + 1)):
                        base = random.randint(1_000_000, 20_000_000)
                        loss_ratio = random.uniform(0.45, 0.85)
                        dev_factor = min(1.0, 0.2 + dev_year * 0.15)

                        data.append({
                            'Syndicate_Number': syn,
                            'Year_of_Account': year,
                            'Development_Year': dev_year,
                            'LOB_Code': lob,
                            'LOB_Name': self.lob_names.get(lob, lob),
                            'Currency': 'GBP',
                            'Cumulative_Paid': int(base * loss_ratio * dev_factor),
                            'Case_Reserves': int(base * loss_ratio * (1 - dev_factor) * 0.6),
                            'IBNR': int(base * loss_ratio * (1 - dev_factor) * 0.4),
                            'Total_Incurred': int(base * loss_ratio),
                            'As_At_Date': f'{year + dev_year}-12-31',
                        })
        return pd.DataFrame(data)

    def _generate_gross_premium_ibnr(self, quarterly: bool = False) -> pd.DataFrame:
        """Generate gross premium and IBNR data."""
        data = []
        for syn in self.syndicates:
            for year in self.years[:-1]:
                for lob in self.lob_codes[:5]:
                    gwp = random.randint(5_000_000, 50_000_000)
                    ulr = random.uniform(0.55, 0.75)
                    data.append({
                        'Syndicate_Number': syn,
                        'Year_of_Account': year,
                        'LOB_Code': lob,
                        'LOB_Name': self.lob_names.get(lob, lob),
                        'Gross_Written_Premium': gwp,
                        'Gross_Earned_Premium': int(gwp * random.uniform(0.85, 0.95)),
                        'Paid_Claims': int(gwp * ulr * random.uniform(0.4, 0.7)),
                        'Case_Reserves': int(gwp * ulr * random.uniform(0.1, 0.2)),
                        'IBNR_Best_Estimate': int(gwp * ulr * random.uniform(0.15, 0.35)),
                        'IBNR_High': int(gwp * ulr * random.uniform(0.20, 0.40)),
                        'IBNR_Low': int(gwp * ulr * random.uniform(0.10, 0.25)),
                        'Ultimate_Loss_Ratio': round(ulr, 4),
                    })
        return pd.DataFrame(data)

    def _generate_net_premium_ibnr(self) -> pd.DataFrame:
        """Generate net premium and IBNR data."""
        data = []
        for syn in self.syndicates:
            for year in self.years[:-1]:
                for lob in self.lob_codes[:5]:
                    nwp = random.randint(3_000_000, 40_000_000)
                    ulr = random.uniform(0.50, 0.70)
                    data.append({
                        'Syndicate_Number': syn,
                        'Year_of_Account': year,
                        'LOB_Code': lob,
                        'Net_Written_Premium': nwp,
                        'Net_Earned_Premium': int(nwp * random.uniform(0.85, 0.95)),
                        'Net_Paid_Claims': int(nwp * ulr * random.uniform(0.45, 0.75)),
                        'Net_Case_Reserves': int(nwp * ulr * random.uniform(0.08, 0.18)),
                        'Net_IBNR': int(nwp * ulr * random.uniform(0.12, 0.30)),
                        'RI_Recoveries': int(nwp * random.uniform(0.10, 0.25)),
                        'Net_Ultimate_Loss_Ratio': round(ulr, 4),
                    })
        return pd.DataFrame(data)

    def _generate_validation_summary(self) -> pd.DataFrame:
        """Generate validation summary data."""
        data = []
        for syn in self.syndicates:
            data.append({
                'Syndicate_Number': syn,
                'Total_Forms': 15,
                'Forms_With_Errors': random.randint(0, 2),
                'Forms_With_Warnings': random.randint(0, 5),
                'Validation_Status': random.choice(['Pass', 'Pass with Warnings', 'Review Required']),
                'Completeness_Score': round(random.uniform(0.95, 1.00), 4),
            })
        return pd.DataFrame(data)

    def _generate_development_triangle(self) -> pd.DataFrame:
        """Generate claims development triangle."""
        data = []
        for syn in self.syndicates[:3]:  # Limit for performance
            for origin_year in range(2018, 2024):
                for dev_year in range(2024 - origin_year + 1):
                    base = random.randint(10_000_000, 100_000_000)
                    factor = min(1.0, 0.15 + dev_year * 0.12)
                    data.append({
                        'Syndicate_Number': syn,
                        'Origin_Year': origin_year,
                        'Development_Year': dev_year,
                        'Calendar_Year': origin_year + dev_year,
                        'Cumulative_Paid': int(base * factor),
                        'Cumulative_Incurred': int(base * factor * 1.3),
                    })
        return pd.DataFrame(data)

    def _generate_syndicate_summary(self) -> pd.DataFrame:
        """Generate syndicate-level summary."""
        data = []
        for syn in self.syndicates:
            gwp = random.randint(100_000_000, 500_000_000)
            data.append({
                'Syndicate_Number': syn,
                'Managing_Agent': f'Managing Agent {syn}',
                'Capacity_GBP': gwp,
                'Gross_Written_Premium': int(gwp * random.uniform(0.7, 0.95)),
                'Net_Written_Premium': int(gwp * random.uniform(0.5, 0.8)),
                'Ultimate_Loss_Ratio': round(random.uniform(0.55, 0.75), 4),
                'Combined_Ratio': round(random.uniform(0.90, 1.05), 4),
                'Solvency_Ratio': round(random.uniform(1.2, 2.0), 4),
            })
        return pd.DataFrame(data)

    # =========================================================================
    # HELPER METHODS - SOLVENCY II
    # =========================================================================

    def _generate_balance_sheet(self) -> pd.DataFrame:
        """Generate balance sheet data."""
        data = []
        for syn in self.syndicates:
            total_assets = random.randint(500_000_000, 2_000_000_000)
            data.append({
                'Syndicate_Number': syn,
                'Total_Assets': total_assets,
                'Investments': int(total_assets * 0.6),
                'Reinsurance_Recoverables': int(total_assets * 0.15),
                'Cash_And_Equivalents': int(total_assets * 0.1),
                'Other_Assets': int(total_assets * 0.15),
                'Total_Liabilities': int(total_assets * 0.75),
                'Technical_Provisions': int(total_assets * 0.6),
                'Other_Liabilities': int(total_assets * 0.15),
                'Own_Funds': int(total_assets * 0.25),
            })
        return pd.DataFrame(data)

    def _generate_own_funds(self) -> pd.DataFrame:
        """Generate own funds data."""
        data = []
        for syn in self.syndicates:
            total = random.randint(100_000_000, 500_000_000)
            data.append({
                'Syndicate_Number': syn,
                'Tier_1_Unrestricted': int(total * 0.7),
                'Tier_1_Restricted': int(total * 0.15),
                'Tier_2': int(total * 0.1),
                'Tier_3': int(total * 0.05),
                'Total_Own_Funds': total,
                'Eligible_Own_Funds_SCR': int(total * 0.95),
                'Eligible_Own_Funds_MCR': int(total * 0.85),
            })
        return pd.DataFrame(data)

    def _generate_technical_provisions(self) -> pd.DataFrame:
        """Generate technical provisions data."""
        data = []
        for syn in self.syndicates:
            for lob in self.lob_codes[:5]:
                bel = random.randint(20_000_000, 200_000_000)
                data.append({
                    'Syndicate_Number': syn,
                    'LOB_Code': lob,
                    'Best_Estimate_Liabilities': bel,
                    'Risk_Margin': int(bel * random.uniform(0.04, 0.08)),
                    'Total_Technical_Provisions': int(bel * random.uniform(1.04, 1.08)),
                    'Reinsurance_Recoverables': int(bel * random.uniform(0.15, 0.35)),
                    'Net_Technical_Provisions': int(bel * random.uniform(0.70, 0.90)),
                })
        return pd.DataFrame(data)

    def _generate_scr_summary(self) -> pd.DataFrame:
        """Generate SCR summary data."""
        data = []
        for syn in self.syndicates:
            scr = random.randint(80_000_000, 300_000_000)
            data.append({
                'Syndicate_Number': syn,
                'Market_Risk': int(scr * 0.25),
                'Counterparty_Risk': int(scr * 0.10),
                'Underwriting_Risk': int(scr * 0.45),
                'Operational_Risk': int(scr * 0.08),
                'Diversification_Benefit': -int(scr * 0.15),
                'LAC_DT': -int(scr * 0.05),
                'Total_SCR': scr,
            })
        return pd.DataFrame(data)

    def _generate_mcr_calculation(self) -> pd.DataFrame:
        """Generate MCR calculation data."""
        data = []
        for syn in self.syndicates:
            scr = random.randint(80_000_000, 300_000_000)
            mcr = int(scr * random.uniform(0.25, 0.45))
            data.append({
                'Syndicate_Number': syn,
                'Linear_MCR': mcr,
                'SCR_Based_MCR': int(scr * 0.45),
                'Absolute_Floor_MCR': 3_700_000,
                'Combined_MCR': max(mcr, 3_700_000),
                'Final_MCR': min(max(mcr, 3_700_000), int(scr * 0.45)),
            })
        return pd.DataFrame(data)

    def _generate_solvency_ratio(self) -> pd.DataFrame:
        """Generate solvency ratio data."""
        data = []
        for syn in self.syndicates:
            scr = random.randint(80_000_000, 300_000_000)
            own_funds = int(scr * random.uniform(1.2, 2.5))
            data.append({
                'Syndicate_Number': syn,
                'Own_Funds': own_funds,
                'SCR': scr,
                'MCR': int(scr * 0.35),
                'SCR_Coverage_Ratio': round(own_funds / scr, 4),
                'MCR_Coverage_Ratio': round(own_funds / (scr * 0.35), 4),
                'Excess_Own_Funds': own_funds - scr,
            })
        return pd.DataFrame(data)

    def _generate_asb_claims(self, claim_type: str) -> pd.DataFrame:
        """Generate ASB claims triangle data."""
        multiplier = {'Gross': 1.0, 'Net': 0.7, 'Reinsurance': 0.3}.get(claim_type, 1.0)
        data = []
        for syn in self.syndicates[:5]:
            for origin in range(2015, 2024):
                for dev in range(2024 - origin + 1):
                    base = random.randint(5_000_000, 50_000_000)
                    data.append({
                        'Syndicate_Number': syn,
                        'Claim_Type': claim_type,
                        'Origin_Year': origin,
                        'Development_Year': dev,
                        'Cumulative_Paid': int(base * multiplier * min(1, 0.1 + dev * 0.12)),
                        'Cumulative_Incurred': int(base * multiplier * min(1, 0.15 + dev * 0.12)),
                    })
        return pd.DataFrame(data)

    def _generate_development_factors(self) -> pd.DataFrame:
        """Generate claims development factors."""
        data = []
        for lob in self.lob_codes[:5]:
            for dev_year in range(10):
                data.append({
                    'LOB_Code': lob,
                    'Development_Year': dev_year,
                    'Paid_Development_Factor': round(random.uniform(1.0, 2.5) if dev_year < 5 else random.uniform(1.0, 1.2), 4),
                    'Incurred_Development_Factor': round(random.uniform(1.0, 2.0) if dev_year < 5 else random.uniform(1.0, 1.1), 4),
                })
        return pd.DataFrame(data)

    def _generate_inflation_rates(self) -> pd.DataFrame:
        """Generate inflation rate assumptions."""
        data = []
        for lob in self.lob_codes[:5]:
            data.append({
                'LOB_Code': lob,
                'Claims_Inflation_Rate': round(random.uniform(0.02, 0.06), 4),
                'Expense_Inflation_Rate': round(random.uniform(0.02, 0.04), 4),
                'Wage_Inflation_Rate': round(random.uniform(0.025, 0.045), 4),
            })
        return pd.DataFrame(data)

    # =========================================================================
    # HELPER METHODS - LCR
    # =========================================================================

    def _generate_lcr_scr(self) -> pd.DataFrame:
        """Generate LCR SCR summary."""
        data = []
        for syn in self.syndicates:
            scr = random.randint(80_000_000, 300_000_000)
            data.append({
                'Syndicate_Number': syn,
                'Premium_Risk_SCR': int(scr * 0.20),
                'Reserve_Risk_SCR': int(scr * 0.25),
                'Cat_Risk_SCR': int(scr * 0.15),
                'Market_Risk_SCR': int(scr * 0.20),
                'Credit_Risk_SCR': int(scr * 0.08),
                'Operational_Risk_SCR': int(scr * 0.07),
                'Diversification': -int(scr * 0.12),
                'Total_SCR': scr,
            })
        return pd.DataFrame(data)

    def _generate_lcr_premium_risk(self) -> pd.DataFrame:
        """Generate LCR premium risk by LOB."""
        data = []
        for syn in self.syndicates:
            for lob in self.lob_codes[:5]:
                nep = random.randint(10_000_000, 100_000_000)
                data.append({
                    'Syndicate_Number': syn,
                    'LOB_Code': lob,
                    'Net_Earned_Premium': nep,
                    'Volume_Measure': int(nep * 1.1),
                    'Premium_Risk_Factor': round(random.uniform(0.05, 0.15), 4),
                    'Premium_Risk_SCR': int(nep * random.uniform(0.05, 0.15)),
                })
        return pd.DataFrame(data)

    def _generate_lcr_reserve_risk(self) -> pd.DataFrame:
        """Generate LCR reserve risk."""
        data = []
        for syn in self.syndicates:
            for lob in self.lob_codes[:5]:
                reserves = random.randint(20_000_000, 200_000_000)
                data.append({
                    'Syndicate_Number': syn,
                    'LOB_Code': lob,
                    'Net_Best_Estimate': reserves,
                    'Reserve_Risk_Factor': round(random.uniform(0.08, 0.20), 4),
                    'Reserve_Risk_SCR': int(reserves * random.uniform(0.08, 0.20)),
                })
        return pd.DataFrame(data)

    def _generate_lcr_cat_risk(self) -> pd.DataFrame:
        """Generate LCR catastrophe risk."""
        perils = ['US_Hurricane', 'EU_Windstorm', 'JP_Earthquake', 'Cyber', 'Pandemic']
        data = []
        for syn in self.syndicates:
            for peril in perils:
                data.append({
                    'Syndicate_Number': syn,
                    'Peril': peril,
                    'Gross_Loss': random.randint(50_000_000, 500_000_000),
                    'RI_Recovery': random.randint(20_000_000, 300_000_000),
                    'Net_Loss': random.randint(20_000_000, 200_000_000),
                    'Cat_Risk_SCR': random.randint(10_000_000, 100_000_000),
                })
        return pd.DataFrame(data)

    def _generate_lcr_market_risk(self) -> pd.DataFrame:
        """Generate LCR market risk."""
        risk_types = ['Interest_Rate', 'Equity', 'Property', 'Spread', 'Currency']
        data = []
        for syn in self.syndicates:
            for risk in risk_types:
                data.append({
                    'Syndicate_Number': syn,
                    'Risk_Type': risk,
                    'Exposure': random.randint(50_000_000, 500_000_000),
                    'Shock_Factor': round(random.uniform(0.05, 0.25), 4),
                    'SCR_Contribution': random.randint(5_000_000, 50_000_000),
                })
        return pd.DataFrame(data)

    def _generate_lcr_coverage(self) -> pd.DataFrame:
        """Generate LCR coverage ratios."""
        data = []
        for syn in self.syndicates:
            scr = random.randint(80_000_000, 300_000_000)
            own_funds = int(scr * random.uniform(1.2, 2.5))
            data.append({
                'Syndicate_Number': syn,
                'Own_Funds': own_funds,
                'SCR': scr,
                'Coverage_Ratio': round(own_funds / scr, 4),
                'Excess_Capital': own_funds - scr,
                'Rating_Implied': 'A' if own_funds / scr > 1.5 else 'BBB',
            })
        return pd.DataFrame(data)

    # =========================================================================
    # HELPER METHODS - SBF
    # =========================================================================

    def _generate_sbf_income(self) -> pd.DataFrame:
        """Generate SBF income statement forecast."""
        data = []
        for syn in self.syndicates:
            for year in [2024, 2025, 2026]:
                gwp = random.randint(100_000_000, 500_000_000)
                data.append({
                    'Syndicate_Number': syn,
                    'Forecast_Year': year,
                    'Gross_Written_Premium': gwp,
                    'Net_Earned_Premium': int(gwp * 0.8),
                    'Claims_Incurred': int(gwp * random.uniform(0.50, 0.70)),
                    'Acquisition_Costs': int(gwp * random.uniform(0.20, 0.30)),
                    'Operating_Expenses': int(gwp * random.uniform(0.08, 0.12)),
                    'Investment_Income': int(gwp * random.uniform(0.03, 0.06)),
                    'Underwriting_Result': int(gwp * random.uniform(-0.05, 0.15)),
                })
        return pd.DataFrame(data)

    def _generate_sbf_premium(self) -> pd.DataFrame:
        """Generate SBF premium forecast by LOB."""
        data = []
        for syn in self.syndicates:
            for year in [2024, 2025, 2026]:
                for lob in self.lob_codes[:5]:
                    gwp = random.randint(10_000_000, 100_000_000)
                    data.append({
                        'Syndicate_Number': syn,
                        'Forecast_Year': year,
                        'LOB_Code': lob,
                        'Gross_Written_Premium': gwp,
                        'Growth_Rate': round(random.uniform(-0.05, 0.20), 4),
                        'Rate_Change': round(random.uniform(-0.02, 0.10), 4),
                    })
        return pd.DataFrame(data)

    def _generate_sbf_claims(self) -> pd.DataFrame:
        """Generate SBF claims forecast."""
        data = []
        for syn in self.syndicates:
            for year in [2024, 2025, 2026]:
                for lob in self.lob_codes[:5]:
                    data.append({
                        'Syndicate_Number': syn,
                        'Forecast_Year': year,
                        'LOB_Code': lob,
                        'Expected_Loss_Ratio': round(random.uniform(0.50, 0.75), 4),
                        'Claims_Estimate': random.randint(5_000_000, 75_000_000),
                        'IBNR_Assumption': round(random.uniform(0.10, 0.25), 4),
                    })
        return pd.DataFrame(data)

    def _generate_sbf_ratios(self) -> pd.DataFrame:
        """Generate SBF combined ratios."""
        data = []
        for syn in self.syndicates:
            for year in [2024, 2025, 2026]:
                loss_ratio = random.uniform(0.55, 0.72)
                expense_ratio = random.uniform(0.28, 0.38)
                data.append({
                    'Syndicate_Number': syn,
                    'Forecast_Year': year,
                    'Loss_Ratio': round(loss_ratio, 4),
                    'Expense_Ratio': round(expense_ratio, 4),
                    'Combined_Ratio': round(loss_ratio + expense_ratio, 4),
                    'Target_Combined_Ratio': round(random.uniform(0.92, 0.98), 4),
                })
        return pd.DataFrame(data)

    # =========================================================================
    # HELPER METHODS - QMA
    # =========================================================================

    def _generate_qma_balance_sheet(self) -> pd.DataFrame:
        """Generate QMA quarterly balance sheet."""
        data = []
        for syn in self.syndicates:
            for q in ['Q1', 'Q2', 'Q3', 'Q4']:
                total = random.randint(500_000_000, 2_000_000_000)
                data.append({
                    'Syndicate_Number': syn,
                    'Quarter': f'2024-{q}',
                    'Total_Assets': total,
                    'Total_Liabilities': int(total * 0.75),
                    'Net_Assets': int(total * 0.25),
                })
        return pd.DataFrame(data)

    def _generate_qma_pl(self) -> pd.DataFrame:
        """Generate QMA P&L statement."""
        data = []
        for syn in self.syndicates:
            for q in ['Q1', 'Q2', 'Q3', 'Q4']:
                premium = random.randint(20_000_000, 100_000_000)
                data.append({
                    'Syndicate_Number': syn,
                    'Quarter': f'2024-{q}',
                    'Net_Earned_Premium': premium,
                    'Claims_Incurred': int(premium * random.uniform(0.50, 0.70)),
                    'Operating_Expenses': int(premium * random.uniform(0.25, 0.35)),
                    'Investment_Return': int(premium * random.uniform(0.02, 0.05)),
                    'Profit_Before_Tax': int(premium * random.uniform(-0.05, 0.20)),
                })
        return pd.DataFrame(data)

    def _generate_qma_technical(self) -> pd.DataFrame:
        """Generate QMA technical account."""
        data = []
        for syn in self.syndicates:
            for lob in self.lob_codes[:5]:
                nep = random.randint(10_000_000, 80_000_000)
                data.append({
                    'Syndicate_Number': syn,
                    'LOB_Code': lob,
                    'Net_Earned_Premium': nep,
                    'Claims_Incurred': int(nep * random.uniform(0.50, 0.70)),
                    'Technical_Result': int(nep * random.uniform(-0.05, 0.25)),
                })
        return pd.DataFrame(data)

    def _generate_qma_ratios(self) -> pd.DataFrame:
        """Generate QMA key ratios."""
        data = []
        for syn in self.syndicates:
            data.append({
                'Syndicate_Number': syn,
                'Loss_Ratio': round(random.uniform(0.55, 0.72), 4),
                'Expense_Ratio': round(random.uniform(0.28, 0.38), 4),
                'Combined_Ratio': round(random.uniform(0.88, 1.05), 4),
                'Investment_Yield': round(random.uniform(0.02, 0.05), 4),
                'Return_on_Capital': round(random.uniform(0.05, 0.20), 4),
            })
        return pd.DataFrame(data)

    # =========================================================================
    # HELPER METHODS - FSCS & LIQUIDITY
    # =========================================================================

    def _generate_fscs_summary(self) -> pd.DataFrame:
        """Generate FSCS summary data."""
        data = []
        for syn in self.syndicates:
            for year in range(2020, 2025):
                data.append({
                    'Syndicate_Number': syn,
                    'Year': year,
                    'Protected_Liabilities': random.randint(10_000_000, 100_000_000),
                    'FSCS_Levy': random.randint(100_000, 2_000_000),
                    'Management_Expenses_Levy': random.randint(50_000, 500_000),
                })
        return pd.DataFrame(data)

    def _generate_fscs_detail(self) -> pd.DataFrame:
        """Generate FSCS detailed data."""
        data = []
        for syn in self.syndicates:
            for lob in self.lob_codes[:5]:
                data.append({
                    'Syndicate_Number': syn,
                    'LOB_Code': lob,
                    'Protected_Liabilities': random.randint(2_000_000, 20_000_000),
                    'Eligible_Premium': random.randint(5_000_000, 50_000_000),
                    'Levy_Rate': round(random.uniform(0.001, 0.005), 6),
                })
        return pd.DataFrame(data)

    def _generate_liquidity_capital(self) -> pd.DataFrame:
        """Generate liquidity capital position."""
        data = []
        for syn in self.syndicates:
            fal = random.randint(100_000_000, 500_000_000)
            data.append({
                'Syndicate_Number': syn,
                'FAL': fal,
                'FIS': int(fal * random.uniform(0.80, 0.95)),
                'uSCR': int(fal * random.uniform(0.60, 0.85)),
                'uECA': int(fal * random.uniform(0.10, 0.20)),
                'Excess_Capital': int(fal * random.uniform(0.15, 0.40)),
            })
        return pd.DataFrame(data)

    def _generate_liquidity_assets(self) -> pd.DataFrame:
        """Generate liquidity asset breakdown."""
        data = []
        quarters = ['2024-Q4', '2025-Q1', '2025-Q2', '2025-Q3', '2025-Q4']
        for syn in self.syndicates:
            for q in quarters:
                total = random.randint(300_000_000, 1_000_000_000)
                data.append({
                    'Syndicate_Number': syn,
                    'Quarter': q,
                    'Liquid_Assets': int(total * random.uniform(0.25, 0.40)),
                    'Illiquid_Assets': int(total * random.uniform(0.25, 0.35)),
                    'Restricted_Assets': int(total * random.uniform(0.30, 0.45)),
                    'Total_Assets': total,
                })
        return pd.DataFrame(data)

    def _generate_liquidity_cashflow(self) -> pd.DataFrame:
        """Generate liquidity cashflow summary."""
        data = []
        quarters = ['2024-Q4', '2025-Q1', '2025-Q2', '2025-Q3', '2025-Q4']
        for syn in self.syndicates:
            opening = random.randint(50_000_000, 200_000_000)
            for q in quarters:
                inflows = random.randint(30_000_000, 100_000_000)
                outflows = random.randint(25_000_000, 90_000_000)
                closing = opening + inflows - outflows
                data.append({
                    'Syndicate_Number': syn,
                    'Quarter': q,
                    'Opening_Balance': opening,
                    'Cash_Inflows': inflows,
                    'Cash_Outflows': outflows,
                    'Net_Movement': inflows - outflows,
                    'Closing_Balance': closing,
                })
                opening = closing
        return pd.DataFrame(data)

    def _generate_liquidity_stress(self) -> pd.DataFrame:
        """Generate liquidity stress impact."""
        scenarios = ['Base', 'Adverse', '1-in-200']
        data = []
        for syn in self.syndicates:
            for scenario in scenarios:
                multiplier = {'Base': 1.0, 'Adverse': 1.5, '1-in-200': 2.5}.get(scenario, 1.0)
                base_loss = random.randint(50_000_000, 200_000_000)
                data.append({
                    'Syndicate_Number': syn,
                    'Scenario': scenario,
                    'Gross_Loss': int(base_loss * multiplier),
                    'RI_Recovery': int(base_loss * multiplier * random.uniform(0.40, 0.60)),
                    'Net_Loss': int(base_loss * multiplier * random.uniform(0.40, 0.60)),
                    'Liquidity_Impact': int(base_loss * multiplier * random.uniform(0.20, 0.40)),
                })
        return pd.DataFrame(data)

    # =========================================================================
    # HELPER METHODS - CLAIMS
    # =========================================================================

    def _generate_detailed_claims(self) -> pd.DataFrame:
        """Generate detailed claims data."""
        data = []
        statuses = ['Open', 'Closed', 'Reopened']
        for _ in range(500):
            syn = random.choice(self.syndicates)
            data.append({
                'Claim_Reference': f'CLM{random.randint(100000, 999999)}',
                'Syndicate_Number': syn,
                'Year_of_Account': random.choice(self.years),
                'Risk_Code': random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9']),
                'Currency': random.choice(self.currencies),
                'Status': random.choice(statuses),
                'Outstanding_Amount': random.randint(10000, 500000),
                'Paid_Amount': random.randint(5000, 300000),
                'Incurred_Amount': random.randint(15000, 800000),
            })
        return pd.DataFrame(data)

    def _generate_claims_by_syndicate(self) -> pd.DataFrame:
        """Generate claims summary by syndicate."""
        data = []
        for syn in self.syndicates:
            data.append({
                'Syndicate_Number': syn,
                'Total_Claims': random.randint(100, 1000),
                'Open_Claims': random.randint(20, 200),
                'Closed_Claims': random.randint(80, 800),
                'Total_Outstanding': random.randint(10_000_000, 100_000_000),
                'Total_Paid': random.randint(5_000_000, 80_000_000),
                'Total_Incurred': random.randint(15_000_000, 180_000_000),
            })
        return pd.DataFrame(data)

    def _generate_claims_by_risk(self) -> pd.DataFrame:
        """Generate claims summary by risk code."""
        risk_codes = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        data = []
        for risk in risk_codes:
            data.append({
                'Risk_Code': risk,
                'Risk_Description': f'Risk Type {risk}',
                'Total_Claims': random.randint(50, 500),
                'Average_Claim_Size': random.randint(50000, 500000),
                'Total_Incurred': random.randint(5_000_000, 50_000_000),
            })
        return pd.DataFrame(data)

    def _generate_claims_by_status(self) -> pd.DataFrame:
        """Generate claims summary by status."""
        statuses = ['Open', 'Closed', 'Reopened', 'Pending']
        data = []
        for status in statuses:
            multiplier = {'Open': 0.3, 'Closed': 0.6, 'Reopened': 0.05, 'Pending': 0.05}.get(status, 0.25)
            data.append({
                'Status': status,
                'Claim_Count': int(1000 * multiplier),
                'Total_Outstanding': int(100_000_000 * multiplier),
                'Total_Paid': int(80_000_000 * multiplier),
                'Average_Age_Days': random.randint(30, 500),
            })
        return pd.DataFrame(data)
