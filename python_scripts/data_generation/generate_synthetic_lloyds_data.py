"""
Synthetic Lloyd's of London Data Generator
Generates realistic RRA (Reserving Return Annual) data for testing and development

This script creates synthetic Lloyd's data that can be used in Power BI
for testing RRA reporting templates.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

class LloydsDataGenerator:
    """Generates synthetic Lloyd's of London reserving data"""

    def __init__(self, output_dir='../../synthetic_data'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Lloyd's syndicate numbers (realistic ranges)
        self.syndicates = [2987, 33, 1183, 2791, 623, 4242, 5000, 1910, 2010, 2525]

        # Years of Account (YoA)
        self.current_year = 2024
        self.years_of_account = list(range(2018, 2026))  # 2018-2025

        # Classes of Business (Lloyd's typical classes)
        self.classes_of_business = {
            'A1': 'Direct Accident & Health',
            'A2': 'Accident & Health Reinsurance',
            'D1': 'Direct Motor (Private Car)',
            'D2': 'Direct Motor (Commercial)',
            'E1': 'Energy Offshore',
            'E2': 'Energy Onshore',
            'F1': 'Fire & Other Damage - Direct',
            'F2': 'Fire & Other Damage - Reinsurance',
            'M1': 'Marine Cargo',
            'M2': 'Marine Hull',
            'M3': 'Marine Liability',
            'N1': 'Non-Marine Property Treaty',
            'N2': 'Non-Marine Property Facultative',
            'P1': 'Professional Indemnity',
            'P2': 'Public & Products Liability',
            'T1': 'Third Party Liability - Direct',
            'T2': 'Third Party Liability - Reinsurance',
            'V1': 'Aviation',
            'W1': 'Political Risk & Contingency',
            'X1': 'Catastrophe Reinsurance'
        }

        # Risk codes
        self.risk_codes = {
            'RC01': 'Attritional',
            'RC02': 'Large Loss',
            'RC03': 'Catastrophe - Natural',
            'RC04': 'Catastrophe - Man-made',
            'RC05': 'Reserve Development'
        }

        # Catastrophe codes
        self.cat_codes = {
            'NAT01': 'Hurricane - USA',
            'NAT02': 'Earthquake - Japan',
            'NAT03': 'Flood - Europe',
            'NAT04': 'Windstorm - Europe',
            'NAT05': 'Wildfire - USA',
            'MAN01': 'Cyber Attack',
            'MAN02': 'Industrial Accident',
            'MAN03': 'Aviation Accident'
        }

        # Currency codes
        self.currencies = ['GBP', 'USD', 'EUR', 'CAD', 'AUD', 'JPY']

    def generate_control_data(self):
        """Generate RRA 010 Control Data"""
        control_data = []

        for syndicate in self.syndicates:
            control_data.append({
                'Syndicate_Number': syndicate,
                'Return_Type': 'RRA',
                'Status': random.choice(['Draft', 'Submitted', 'Approved']),
                'Edition': '1.1',
                'Managing_Agent_Name': f'Managing Agent {syndicate}',
                'First_Pure_YoA': min(self.years_of_account),
                'First_Reporting_YoA': min(self.years_of_account),
                'Final_Pure_YoA': max(self.years_of_account) - 1,
                'Prospective_Year': max(self.years_of_account),
                'Contact_Username': f'user{syndicate}',
                'Contact_Name': f'Contact Person {syndicate}',
                'Contact_Phone': f'+44 20 {random.randint(7000, 7999)} {random.randint(1000, 9999)}',
                'Contact_Email': f'contact{syndicate}@lloyds.com',
                'Submission_Date': datetime.now().strftime('%Y-%m-%d'),
                'Capacity_GBP': random.randint(50000000, 500000000)
            })

        df = pd.DataFrame(control_data)
        df.to_csv(f'{self.output_dir}/rra_010_control.csv', index=False)
        print(f"✓ Generated RRA 010 Control: {len(df)} records")
        return df

    def generate_exchange_rates(self):
        """Generate RRA 020 Exchange Rates"""
        exchange_rates = []

        # Base rates for main currencies (against GBP)
        base_rates = {
            'USD': 1.27,
            'EUR': 1.17,
            'CAD': 1.72,
            'AUD': 1.95,
            'JPY': 188.5,
            'GBP': 1.00
        }

        for year in self.years_of_account:
            for currency, base_rate in base_rates.items():
                # Add some random variation
                variation = random.uniform(0.95, 1.05)
                exchange_rates.append({
                    'Year_of_Account': year,
                    'Currency_Code': currency,
                    'Currency_Name': currency,
                    'Exchange_Rate_to_GBP': round(base_rate * variation, 4),
                    'Rate_Type': 'Average',
                    'Effective_Date': f'{year}-12-31'
                })

        df = pd.DataFrame(exchange_rates)
        df.to_csv(f'{self.output_dir}/rra_020_exchange_rates.csv', index=False)
        print(f"✓ Generated RRA 020 Exchange Rates: {len(df)} records")
        return df

    def generate_scob_mapping(self):
        """Generate RRA 071 SCOB (Syndicate Class of Business) Mapping"""
        scob_mapping = []

        for syndicate in self.syndicates:
            # Each syndicate writes 3-7 classes of business
            num_classes = random.randint(3, 7)
            selected_classes = random.sample(list(self.classes_of_business.keys()), num_classes)

            for class_code in selected_classes:
                scob_mapping.append({
                    'Syndicate_Number': syndicate,
                    'SCOB_Code': f'{class_code}_{syndicate}',
                    'LOB_Code': class_code,
                    'LOB_Description': self.classes_of_business[class_code],
                    'Reserving_Class': f'RC_{class_code}',
                    'Active_Flag': 'Y',
                    'Effective_From': f'{min(self.years_of_account)}-01-01',
                    'Effective_To': f'{max(self.years_of_account)}-12-31'
                })

        df = pd.DataFrame(scob_mapping)
        df.to_csv(f'{self.output_dir}/rra_071_scob_mapping.csv', index=False)
        print(f"✓ Generated RRA 071 SCOB Mapping: {len(df)} records")
        return df

    def generate_reserving_class_info(self):
        """Generate RRA 081 Reserving Class Information"""
        res_class_info = []

        for syndicate in self.syndicates:
            for lob_code, lob_desc in self.classes_of_business.items():
                res_class_info.append({
                    'Syndicate_Number': syndicate,
                    'Reserving_Class_Code': f'RC_{lob_code}',
                    'Reserving_Class_Description': f'{lob_desc} - Reserves',
                    'LOB_Code': lob_code,
                    'Development_Pattern': random.choice(['Short Tail', 'Medium Tail', 'Long Tail']),
                    'Average_Settlement_Years': random.randint(1, 15),
                    'Actuarial_Method': random.choice(['Chain Ladder', 'BF Method', 'Cape Cod', 'Expected Loss Ratio']),
                    'Last_Review_Date': f'{self.current_year}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'
                })

        df = pd.DataFrame(res_class_info)
        df.to_csv(f'{self.output_dir}/rra_081_reserving_class_info.csv', index=False)
        print(f"✓ Generated RRA 081 Reserving Class Info: {len(df)} records")
        return df

    def generate_lpt_data(self):
        """Generate RRA 091 LPT (Loss Portfolio Transfer) Data"""
        lpt_data = []

        # Only some syndicates have LPT
        for syndicate in random.sample(self.syndicates, k=3):
            for year in random.sample(self.years_of_account[:-2], k=2):
                lpt_data.append({
                    'Syndicate_Number': syndicate,
                    'Year_of_Account': year,
                    'LPT_Type': random.choice(['Quota Share', 'Excess of Loss', 'Stop Loss']),
                    'Counterparty_Name': f'Reinsurer_{random.randint(1, 5)}',
                    'LPT_Effective_Date': f'{year + 2}-01-01',
                    'Transfer_Amount_GBP': random.randint(5000000, 50000000),
                    'Outstanding_Claims_GBP': random.randint(3000000, 40000000),
                    'IBNR_GBP': random.randint(1000000, 15000000),
                    'Premium_Paid_GBP': random.randint(4000000, 45000000)
                })

        df = pd.DataFrame(lpt_data)
        df.to_csv(f'{self.output_dir}/rra_091_lpt.csv', index=False)
        print(f"✓ Generated RRA 091 LPT: {len(df)} records")
        return df

    def generate_net_claims(self):
        """Generate RRA 193 Net Claims Data"""
        net_claims = []

        for syndicate in self.syndicates:
            for year in self.years_of_account[:-1]:  # Exclude prospective year
                for lob_code in list(self.classes_of_business.keys())[:5]:
                    for development_year in range(0, min(8, self.current_year - year + 1)):

                        # Calculate cumulative paid and incurred
                        base_premium = random.randint(1000000, 20000000)
                        loss_ratio = random.uniform(0.45, 0.85)
                        development_factor = min(1.0, 0.2 + (development_year * 0.15))

                        cumulative_paid = int(base_premium * loss_ratio * development_factor)
                        case_reserves = int(base_premium * loss_ratio * (1 - development_factor) * 0.6)
                        ibnr = int(base_premium * loss_ratio * (1 - development_factor) * 0.4)

                        net_claims.append({
                            'Syndicate_Number': syndicate,
                            'Year_of_Account': year,
                            'Development_Year': development_year,
                            'LOB_Code': lob_code,
                            'Currency': 'GBP',
                            'Gross_Premium_Written': base_premium,
                            'Net_Premium_Written': int(base_premium * 0.85),
                            'Cumulative_Paid_Claims': cumulative_paid,
                            'Case_Reserves': case_reserves,
                            'IBNR_Reserve': ibnr,
                            'Total_Incurred': cumulative_paid + case_reserves + ibnr,
                            'Number_of_Claims': random.randint(10, 500),
                            'Number_of_Claims_Closed': int(random.randint(5, 400) * development_factor),
                            'As_At_Date': f'{year + development_year}-12-31'
                        })

        df = pd.DataFrame(net_claims)
        df.to_csv(f'{self.output_dir}/rra_193_net_claims.csv', index=False)
        print(f"✓ Generated RRA 193 Net Claims: {len(df)} records")
        return df

    def generate_gross_premium_ibnr(self):
        """Generate RRA 291 Gross Premium and IBNR"""
        gross_data = []

        for syndicate in self.syndicates:
            for year in self.years_of_account[:-1]:
                for lob_code in list(self.classes_of_business.keys())[:5]:

                    gwp = random.randint(5000000, 50000000)
                    ultimate_loss_ratio = random.uniform(0.55, 0.75)

                    gross_data.append({
                        'Syndicate_Number': syndicate,
                        'Year_of_Account': year,
                        'LOB_Code': lob_code,
                        'Currency': 'GBP',
                        'Gross_Written_Premium': gwp,
                        'Gross_Earned_Premium': int(gwp * random.uniform(0.85, 0.95)),
                        'Paid_Claims_Gross': int(gwp * ultimate_loss_ratio * random.uniform(0.4, 0.7)),
                        'Case_Reserves_Gross': int(gwp * ultimate_loss_ratio * random.uniform(0.1, 0.2)),
                        'IBNR_Best_Estimate': int(gwp * ultimate_loss_ratio * random.uniform(0.15, 0.35)),
                        'IBNR_High': int(gwp * ultimate_loss_ratio * random.uniform(0.20, 0.40)),
                        'IBNR_Low': int(gwp * ultimate_loss_ratio * random.uniform(0.10, 0.25)),
                        'Ultimate_Loss_Ratio': round(ultimate_loss_ratio, 4),
                        'As_At_Date': f'{self.current_year}-12-31'
                    })

        df = pd.DataFrame(gross_data)
        df.to_csv(f'{self.output_dir}/rra_291_gross_premium_ibnr.csv', index=False)
        print(f"✓ Generated RRA 291 Gross Premium & IBNR: {len(df)} records")
        return df

    def generate_net_premium_ibnr(self):
        """Generate RRA 292 Net Premium and IBNR Estimates"""
        net_data = []

        for syndicate in self.syndicates:
            for year in self.years_of_account[:-1]:
                for lob_code in list(self.classes_of_business.keys())[:5]:

                    nwp = random.randint(3000000, 40000000)
                    ultimate_loss_ratio = random.uniform(0.50, 0.70)
                    ri_recovery = random.uniform(0.10, 0.25)

                    net_data.append({
                        'Syndicate_Number': syndicate,
                        'Year_of_Account': year,
                        'LOB_Code': lob_code,
                        'Currency': 'GBP',
                        'Net_Written_Premium': nwp,
                        'Net_Earned_Premium': int(nwp * random.uniform(0.85, 0.95)),
                        'Paid_Claims_Net': int(nwp * ultimate_loss_ratio * random.uniform(0.45, 0.75)),
                        'Case_Reserves_Net': int(nwp * ultimate_loss_ratio * random.uniform(0.08, 0.18)),
                        'IBNR_Net_Best_Estimate': int(nwp * ultimate_loss_ratio * random.uniform(0.12, 0.30)),
                        'RI_Recoveries_Expected': int(nwp * ri_recovery),
                        'Net_Ultimate_Loss_Ratio': round(ultimate_loss_ratio, 4),
                        'Actuarial_Method': random.choice(['Chain Ladder', 'BF Method', 'Expected Loss Ratio']),
                        'As_At_Date': f'{self.current_year}-12-31'
                    })

        df = pd.DataFrame(net_data)
        df.to_csv(f'{self.output_dir}/rra_292_net_premium_ibnr.csv', index=False)
        print(f"✓ Generated RRA 292 Net Premium & IBNR: {len(df)} records")
        return df

    def generate_os_ibnr_pyoa(self):
        """Generate RRA 293 Outstanding & IBNR (< 20 Pure Years of Account)"""
        os_ibnr_data = []

        for syndicate in self.syndicates:
            for year in self.years_of_account[:-1]:
                for lob_code in list(self.classes_of_business.keys())[:5]:

                    outstanding = random.randint(500000, 15000000)
                    ibnr = random.randint(300000, 10000000)

                    os_ibnr_data.append({
                        'Syndicate_Number': syndicate,
                        'Pure_Year_of_Account': year,
                        'LOB_Code': lob_code,
                        'Currency': 'GBP',
                        'Outstanding_Claims': outstanding,
                        'IBNR_Reserve': ibnr,
                        'Total_Reserve': outstanding + ibnr,
                        'Number_Outstanding_Claims': random.randint(20, 300),
                        'Average_Outstanding_Claim': int(outstanding / random.randint(20, 300)) if outstanding > 0 else 0,
                        'Reserve_to_Premium_Ratio': round(random.uniform(0.3, 0.8), 4),
                        'As_At_Date': f'{self.current_year}-12-31'
                    })

        df = pd.DataFrame(os_ibnr_data)
        df.to_csv(f'{self.output_dir}/rra_293_os_ibnr_pyoa.csv', index=False)
        print(f"✓ Generated RRA 293 OS & IBNR: {len(df)} records")
        return df

    def generate_cat_ibnr(self):
        """Generate RRA 294 Gross IBNR Estimates (Catastrophe only)"""
        cat_ibnr_data = []

        # Only certain years have cat events
        cat_years = random.sample(self.years_of_account[:-1], k=4)

        for syndicate in self.syndicates:
            for year in cat_years:
                for cat_code, cat_desc in random.sample(list(self.cat_codes.items()), k=2):

                    cat_loss = random.randint(2000000, 80000000)

                    cat_ibnr_data.append({
                        'Syndicate_Number': syndicate,
                        'Year_of_Account': year,
                        'Catastrophe_Code': cat_code,
                        'Catastrophe_Description': cat_desc,
                        'Event_Date': f'{year}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}',
                        'Currency': 'GBP',
                        'Gross_Incurred_Loss': cat_loss,
                        'Paid_Loss': int(cat_loss * random.uniform(0.3, 0.7)),
                        'Case_Reserves': int(cat_loss * random.uniform(0.1, 0.25)),
                        'IBNR_Estimate': int(cat_loss * random.uniform(0.15, 0.40)),
                        'RI_Recoveries': int(cat_loss * random.uniform(0.30, 0.60)),
                        'Net_Cat_Loss': int(cat_loss * random.uniform(0.40, 0.70)),
                        'Market_Share_Estimate': round(random.uniform(0.01, 0.10), 4),
                        'As_At_Date': f'{self.current_year}-12-31'
                    })

        df = pd.DataFrame(cat_ibnr_data)
        df.to_csv(f'{self.output_dir}/rra_294_cat_ibnr.csv', index=False)
        print(f"✓ Generated RRA 294 Catastrophe IBNR: {len(df)} records")
        return df

    def generate_ulae(self):
        """Generate RRA 295 ULAE (Unallocated Loss Adjustment Expenses)"""
        ulae_data = []

        for syndicate in self.syndicates:
            for year in self.years_of_account[:-1]:

                total_reserves = random.randint(10000000, 100000000)
                ulae_ratio = random.uniform(0.03, 0.08)

                ulae_data.append({
                    'Syndicate_Number': syndicate,
                    'Year_of_Account': year,
                    'Currency': 'GBP',
                    'Total_Loss_Reserves': total_reserves,
                    'ULAE_Ratio': round(ulae_ratio, 4),
                    'ULAE_Reserve': int(total_reserves * ulae_ratio),
                    'ULAE_Method': random.choice(['Percentage of Reserves', 'Per Claim', 'Historical Average']),
                    'Internal_Costs': int(total_reserves * ulae_ratio * 0.6),
                    'External_Costs': int(total_reserves * ulae_ratio * 0.4),
                    'As_At_Date': f'{self.current_year}-12-31'
                })

        df = pd.DataFrame(ulae_data)
        df.to_csv(f'{self.output_dir}/rra_295_ulae.csv', index=False)
        print(f"✓ Generated RRA 295 ULAE: {len(df)} records")
        return df

    def generate_ielr(self):
        """Generate RRA 391 IELR (Incurred Emerging Loss Ratio)"""
        ielr_data = []

        for syndicate in self.syndicates:
            for year in self.years_of_account[:-1]:
                for lob_code in list(self.classes_of_business.keys())[:5]:

                    earned_premium = random.randint(5000000, 50000000)

                    # Generate development pattern
                    for dev_year in range(0, min(6, self.current_year - year + 1)):
                        incurred_loss = int(earned_premium * random.uniform(0.50, 0.75) * min(1.0, 0.3 + dev_year * 0.15))

                        ielr_data.append({
                            'Syndicate_Number': syndicate,
                            'Year_of_Account': year,
                            'Development_Year': dev_year,
                            'LOB_Code': lob_code,
                            'Currency': 'GBP',
                            'Earned_Premium': earned_premium,
                            'Incurred_Loss': incurred_loss,
                            'Incurred_Loss_Ratio': round(incurred_loss / earned_premium, 4),
                            'Paid_Loss': int(incurred_loss * random.uniform(0.5, 0.9)),
                            'Outstanding_Reserve': int(incurred_loss * random.uniform(0.1, 0.5)),
                            'Calendar_Year': year + dev_year,
                            'As_At_Date': f'{year + dev_year}-12-31'
                        })

        df = pd.DataFrame(ielr_data)
        df.to_csv(f'{self.output_dir}/rra_391_ielr.csv', index=False)
        print(f"✓ Generated RRA 391 IELR: {len(df)} records")
        return df

    def generate_rra_910(self):
        """Generate RRA 910 - Additional Information"""
        rra_910_data = []

        for syndicate in self.syndicates:
            rra_910_data.append({
                'Syndicate_Number': syndicate,
                'Reporting_Period': f'{self.current_year}-12-31',
                'Major_Events_Description': random.choice([
                    'No major events this period',
                    'Significant reserve release in Motor class',
                    'Hurricane losses impacting Property class',
                    'Strengthening of casualty reserves',
                    'Commutation of old year liabilities'
                ]),
                'Methodology_Changes': random.choice([
                    'No changes',
                    'Updated development patterns for long-tail classes',
                    'Revised IBNR methodology for cyber risks',
                    'Enhanced cat modeling approach'
                ]),
                'Material_Assumptions': 'Standard actuarial assumptions applied',
                'Data_Quality_Issues': random.choice(['None', 'Minor data reconciliation items', 'None identified']),
                'Actuary_Name': f'Chief Actuary {syndicate}',
                'Actuary_Qualification': random.choice(['FIA', 'ACII', 'FCAS']),
                'Sign_Off_Date': f'{self.current_year}-12-31'
            })

        df = pd.DataFrame(rra_910_data)
        df.to_csv(f'{self.output_dir}/rra_910_additional_info.csv', index=False)
        print(f"✓ Generated RRA 910 Additional Info: {len(df)} records")
        return df

    def generate_rra_990(self):
        """Generate RRA 990 - Validation Summary"""
        rra_990_data = []

        for syndicate in self.syndicates:
            rra_990_data.append({
                'Syndicate_Number': syndicate,
                'Reporting_Period': f'{self.current_year}-12-31',
                'Total_Forms_Submitted': 15,
                'Forms_With_Errors': random.randint(0, 2),
                'Forms_With_Warnings': random.randint(0, 5),
                'Validation_Status': random.choice(['Pass', 'Pass with Warnings', 'Review Required']),
                'Data_Completeness_Score': round(random.uniform(0.95, 1.00), 4),
                'Cross_Form_Reconciliation': random.choice(['Passed', 'Passed with Exceptions']),
                'YoY_Movement_Check': random.choice(['Within Tolerance', 'Requires Explanation']),
                'Submission_Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Submitted_By': f'user{syndicate}',
                'Validation_Version': '1.1'
            })

        df = pd.DataFrame(rra_990_data)
        df.to_csv(f'{self.output_dir}/rra_990_validation.csv', index=False)
        print(f"✓ Generated RRA 990 Validation: {len(df)} records")
        return df

    def generate_all_data(self):
        """Generate all RRA synthetic data files"""
        print("\n" + "="*60)
        print("Generating Synthetic Lloyd's RRA Data")
        print("="*60 + "\n")

        self.generate_control_data()
        self.generate_exchange_rates()
        self.generate_scob_mapping()
        self.generate_reserving_class_info()
        self.generate_lpt_data()
        self.generate_net_claims()
        self.generate_gross_premium_ibnr()
        self.generate_net_premium_ibnr()
        self.generate_os_ibnr_pyoa()
        self.generate_cat_ibnr()
        self.generate_ulae()
        self.generate_ielr()
        self.generate_rra_910()
        self.generate_rra_990()

        print("\n" + "="*60)
        print(f"All data generated successfully in: {self.output_dir}")
        print("="*60 + "\n")


if __name__ == "__main__":
    # Generate data
    generator = LloydsDataGenerator(output_dir='../../synthetic_data')
    generator.generate_all_data()

    print("\nSynthetic Lloyd's data generation complete!")
    print("Files can now be imported into Power BI for testing RRA reports.")
