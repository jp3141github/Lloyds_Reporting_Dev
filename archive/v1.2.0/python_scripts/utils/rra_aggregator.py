"""
RRA Aggregator - Combine and aggregate all RRA forms
This script provides functions to load and combine all RRA forms for comprehensive reporting
"""

import pandas as pd
import numpy as np
from pathlib import Path


class RRADataAggregator:
    """Aggregates all RRA form data for comprehensive reporting"""

    def __init__(self, data_dir='../../synthetic_data'):
        self.data_dir = Path(data_dir)
        self.forms = {}

    def load_all_forms(self):
        """Load all RRA form data into memory"""

        form_files = {
            'control': 'rra_010_control.csv',
            'exchange_rates': 'rra_020_exchange_rates.csv',
            'scob_mapping': 'rra_071_scob_mapping.csv',
            'reserving_class_info': 'rra_081_reserving_class_info.csv',
            'lpt': 'rra_091_lpt.csv',
            'net_claims': 'rra_193_net_claims.csv',
            'gross_premium_ibnr': 'rra_291_gross_premium_ibnr.csv',
            'net_premium_ibnr': 'rra_292_net_premium_ibnr.csv',
            'os_ibnr_pyoa': 'rra_293_os_ibnr_pyoa.csv',
            'cat_ibnr': 'rra_294_cat_ibnr.csv',
            'ulae': 'rra_295_ulae.csv',
            'ielr': 'rra_391_ielr.csv',
            'additional_info': 'rra_910_additional_info.csv',
            'validation': 'rra_990_validation.csv'
        }

        for form_name, file_name in form_files.items():
            file_path = self.data_dir / file_name
            if file_path.exists():
                self.forms[form_name] = pd.read_csv(file_path)
                print(f"✓ Loaded {form_name}: {len(self.forms[form_name])} records")
            else:
                print(f"✗ Warning: {file_name} not found")

        return self.forms

    def get_portfolio_summary(self):
        """Generate overall portfolio summary across all forms"""

        summary_data = []

        # Control data summary
        if 'control' in self.forms:
            control = self.forms['control']
            summary_data.append({
                'Category': 'Portfolio Overview',
                'Metric': 'Total Syndicates',
                'Value': len(control),
                'Unit': 'count'
            })
            summary_data.append({
                'Category': 'Portfolio Overview',
                'Metric': 'Total Capacity',
                'Value': control['Capacity_GBP'].sum() / 1000000,
                'Unit': 'GBP M'
            })

        # Gross Premium and IBNR summary
        if 'gross_premium_ibnr' in self.forms:
            gross = self.forms['gross_premium_ibnr']
            summary_data.extend([
                {
                    'Category': 'Gross Premium',
                    'Metric': 'Total Gross Written Premium',
                    'Value': gross['Gross_Written_Premium'].sum() / 1000000,
                    'Unit': 'GBP M'
                },
                {
                    'Category': 'Gross Premium',
                    'Metric': 'Total Gross Earned Premium',
                    'Value': gross['Gross_Earned_Premium'].sum() / 1000000,
                    'Unit': 'GBP M'
                },
                {
                    'Category': 'IBNR Reserves',
                    'Metric': 'Total IBNR (Best Estimate)',
                    'Value': gross['IBNR_Best_Estimate'].sum() / 1000000,
                    'Unit': 'GBP M'
                },
                {
                    'Category': 'Loss Ratios',
                    'Metric': 'Average Ultimate Loss Ratio',
                    'Value': gross['Ultimate_Loss_Ratio'].mean(),
                    'Unit': 'ratio'
                }
            ])

        # Net Premium and IBNR summary
        if 'net_premium_ibnr' in self.forms:
            net = self.forms['net_premium_ibnr']
            summary_data.extend([
                {
                    'Category': 'Net Premium',
                    'Metric': 'Total Net Written Premium',
                    'Value': net['Net_Written_Premium'].sum() / 1000000,
                    'Unit': 'GBP M'
                },
                {
                    'Category': 'Net Premium',
                    'Metric': 'Total Net Earned Premium',
                    'Value': net['Net_Earned_Premium'].sum() / 1000000,
                    'Unit': 'GBP M'
                }
            ])

        # Catastrophe summary
        if 'cat_ibnr' in self.forms:
            cat = self.forms['cat_ibnr']
            summary_data.extend([
                {
                    'Category': 'Catastrophe Losses',
                    'Metric': 'Total Cat Events',
                    'Value': len(cat),
                    'Unit': 'count'
                },
                {
                    'Category': 'Catastrophe Losses',
                    'Metric': 'Total Gross Cat Losses',
                    'Value': cat['Gross_Incurred_Loss'].sum() / 1000000,
                    'Unit': 'GBP M'
                },
                {
                    'Category': 'Catastrophe Losses',
                    'Metric': 'Total Net Cat Losses',
                    'Value': cat['Net_Cat_Loss'].sum() / 1000000,
                    'Unit': 'GBP M'
                }
            ])

        # ULAE summary
        if 'ulae' in self.forms:
            ulae = self.forms['ulae']
            summary_data.append({
                'Category': 'ULAE',
                'Metric': 'Total ULAE Reserves',
                'Value': ulae['ULAE_Reserve'].sum() / 1000000,
                'Unit': 'GBP M'
            })

        # LPT summary
        if 'lpt' in self.forms:
            lpt = self.forms['lpt']
            summary_data.append({
                'Category': 'LPT',
                'Metric': 'Total LPT Transfer Amount',
                'Value': lpt['Transfer_Amount_GBP'].sum() / 1000000,
                'Unit': 'GBP M'
            })

        df = pd.DataFrame(summary_data)
        df['Value'] = df['Value'].round(2)

        return df

    def get_syndicate_profile(self, syndicate_number):
        """Get comprehensive profile for a specific syndicate"""

        profile = {'Syndicate_Number': syndicate_number}

        # Control info
        if 'control' in self.forms:
            control = self.forms['control'][
                self.forms['control']['Syndicate_Number'] == syndicate_number
            ]
            if not control.empty:
                profile.update({
                    'Managing_Agent': control['Managing_Agent_Name'].iloc[0],
                    'Status': control['Status'].iloc[0],
                    'Capacity_GBP_M': control['Capacity_GBP'].iloc[0] / 1000000,
                    'First_YoA': control['First_Pure_YoA'].iloc[0],
                    'Final_YoA': control['Final_Pure_YoA'].iloc[0]
                })

        # Premium data
        if 'gross_premium_ibnr' in self.forms:
            gross = self.forms['gross_premium_ibnr'][
                self.forms['gross_premium_ibnr']['Syndicate_Number'] == syndicate_number
            ]
            if not gross.empty:
                profile.update({
                    'Total_GWP_M': gross['Gross_Written_Premium'].sum() / 1000000,
                    'Total_IBNR_M': gross['IBNR_Best_Estimate'].sum() / 1000000,
                    'Avg_Loss_Ratio': gross['Ultimate_Loss_Ratio'].mean()
                })

        # Classes of business
        if 'scob_mapping' in self.forms:
            scob = self.forms['scob_mapping'][
                self.forms['scob_mapping']['Syndicate_Number'] == syndicate_number
            ]
            profile['Number_of_Classes'] = len(scob)
            profile['Classes_of_Business'] = ', '.join(scob['LOB_Code'].unique())

        return pd.Series(profile)

    def get_lob_analysis(self):
        """Analyze performance across all lines of business"""

        if 'gross_premium_ibnr' not in self.forms:
            return pd.DataFrame()

        gross = self.forms['gross_premium_ibnr']

        lob_analysis = gross.groupby('LOB_Code').agg({
            'Gross_Written_Premium': 'sum',
            'Gross_Earned_Premium': 'sum',
            'IBNR_Best_Estimate': 'sum',
            'Ultimate_Loss_Ratio': 'mean',
            'Syndicate_Number': 'nunique'
        }).reset_index()

        lob_analysis = lob_analysis.rename(columns={
            'Syndicate_Number': 'Number_of_Syndicates'
        })

        # Calculate total incurred from other forms if available
        if 'net_claims' in self.forms:
            claims = self.forms['net_claims']
            claims_by_lob = claims.groupby('LOB_Code')['Total_Incurred'].sum()
            lob_analysis = lob_analysis.merge(
                claims_by_lob.rename('Total_Incurred'),
                on='LOB_Code',
                how='left'
            )

        # Convert to millions
        for col in ['Gross_Written_Premium', 'Gross_Earned_Premium', 'IBNR_Best_Estimate']:
            if col in lob_analysis.columns:
                lob_analysis[f'{col}_M'] = lob_analysis[col] / 1000000
                lob_analysis = lob_analysis.drop(columns=[col])

        lob_analysis = lob_analysis.round(2)

        return lob_analysis

    def get_yoa_development_summary(self):
        """Analyze development patterns across years of account"""

        if 'ielr' not in self.forms:
            return pd.DataFrame()

        ielr = self.forms['ielr']

        # Calculate development patterns
        dev_summary = ielr.groupby(['Year_of_Account', 'Development_Year']).agg({
            'Earned_Premium': 'sum',
            'Incurred_Loss': 'sum',
            'Incurred_Loss_Ratio': 'mean',
            'Paid_Loss': 'sum',
            'Outstanding_Reserve': 'sum'
        }).reset_index()

        dev_summary['Paid_Ratio'] = np.where(
            dev_summary['Incurred_Loss'] > 0,
            dev_summary['Paid_Loss'] / dev_summary['Incurred_Loss'],
            0
        )

        # Convert to millions
        for col in ['Earned_Premium', 'Incurred_Loss', 'Paid_Loss', 'Outstanding_Reserve']:
            dev_summary[f'{col}_M'] = dev_summary[col] / 1000000
            dev_summary = dev_summary.drop(columns=[col])

        dev_summary = dev_summary.round(4)

        return dev_summary

    def get_reserve_adequacy_indicators(self):
        """Calculate reserve adequacy indicators"""

        indicators = []

        # IBNR to Premium ratios
        if 'gross_premium_ibnr' in self.forms:
            gross = self.forms['gross_premium_ibnr']

            ibnr_to_premium = np.where(
                gross['Gross_Earned_Premium'] > 0,
                gross['IBNR_Best_Estimate'] / gross['Gross_Earned_Premium'],
                0
            )

            indicators.append({
                'Indicator': 'Average IBNR to Premium Ratio',
                'Value': np.mean(ibnr_to_premium),
                'Interpretation': 'Lower is better (less uncertainty)'
            })

            # IBNR range as % of estimate
            ibnr_range_pct = np.where(
                gross['IBNR_Best_Estimate'] > 0,
                (gross['IBNR_High'] - gross['IBNR_Low']) / gross['IBNR_Best_Estimate'],
                0
            )

            indicators.append({
                'Indicator': 'Average IBNR Range %',
                'Value': np.mean(ibnr_range_pct),
                'Interpretation': 'Measure of estimation uncertainty'
            })

        # Claims development patterns
        if 'net_claims' in self.forms:
            claims = self.forms['net_claims']

            # Latest development data
            latest = claims.sort_values('Development_Year').groupby(
                ['Syndicate_Number', 'Year_of_Account', 'LOB_Code']
            ).tail(1)

            paid_ratio = np.where(
                latest['Total_Incurred'] > 0,
                latest['Cumulative_Paid_Claims'] / latest['Total_Incurred'],
                0
            )

            indicators.append({
                'Indicator': 'Average Paid Claims Ratio',
                'Value': np.mean(paid_ratio),
                'Interpretation': 'Higher indicates more mature claims'
            })

        # ULAE adequacy
        if 'ulae' in self.forms:
            ulae = self.forms['ulae']

            indicators.append({
                'Indicator': 'Average ULAE Ratio',
                'Value': ulae['ULAE_Ratio'].mean(),
                'Interpretation': 'ULAE as % of loss reserves'
            })

        df = pd.DataFrame(indicators)
        if not df.empty:
            df['Value'] = df['Value'].round(4)

        return df


# For use in Power BI
def get_all_data_for_powerbi(data_dir='../../synthetic_data'):
    """
    Load and return all RRA data for Power BI
    This function can be called from Power BI to get all data

    Returns:
    --------
    dict
        Dictionary containing all loaded dataframes
    """
    aggregator = RRADataAggregator(data_dir)
    aggregator.load_all_forms()
    return aggregator.forms


if __name__ == "__main__":
    # Test the aggregator
    print("\n" + "="*80)
    print("RRA Data Aggregator - Testing")
    print("="*80 + "\n")

    aggregator = RRADataAggregator()
    aggregator.load_all_forms()

    print("\n" + "="*80)
    print("Portfolio Summary:")
    print("="*80)
    print(aggregator.get_portfolio_summary())

    print("\n" + "="*80)
    print("Line of Business Analysis:")
    print("="*80)
    print(aggregator.get_lob_analysis())

    print("\n" + "="*80)
    print("Reserve Adequacy Indicators:")
    print("="*80)
    print(aggregator.get_reserve_adequacy_indicators())

    # Test syndicate profile
    if 'control' in aggregator.forms and not aggregator.forms['control'].empty:
        test_syndicate = aggregator.forms['control']['Syndicate_Number'].iloc[0]
        print(f"\n" + "="*80)
        print(f"Sample Syndicate Profile: {test_syndicate}")
        print("="*80)
        print(aggregator.get_syndicate_profile(test_syndicate))
