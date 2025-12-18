"""
Unified Lloyd's of London Data Generator for RRQ and RRA
=========================================================

V2.0: Complete form coverage for all RRA/RRQ forms per Lloyd's Instructions V1.6 (March 2025)

Generates realistic RRQ (Quarterly) and RRA (Annual) data with configuration-based switching.
This script creates synthetic Lloyd's data for both quarterly and annual returns
that can be used in Power BI for testing RRA/RRQ reporting templates.

New in V2.0:
- Added Form 591 (Syndicate Reinsurance Structure)
- Added RRQ Forms 191, 192 (Gross Claims, Claims Triangles)
- Complete generation for all 15 RRA forms
- Quarterly-specific form handling
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
from typing import Literal, Optional, List

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


class UnifiedLloydsDataGenerator:
    """Generates synthetic Lloyd's data for both RRQ (Quarterly) and RRA (Annual) returns"""

    def __init__(self,
                 return_type: Literal['RRQ', 'RRA'] = 'RRA',
                 reporting_year: int = 2024,
                 reporting_quarter: Optional[Literal['Q1', 'Q2', 'Q3', 'Q4']] = None,
                 output_dir: str = '../../synthetic_data'):
        """
        Initialize the unified data generator

        Parameters:
        -----------
        return_type : str
            'RRQ' for quarterly or 'RRA' for annual
        reporting_year : int
            The year being reported
        reporting_quarter : str, optional
            'Q1', 'Q2', 'Q3', or 'Q4' (required for RRQ)
        output_dir : str
            Directory to save generated files
        """
        self.return_type = return_type
        self.reporting_year = reporting_year
        self.reporting_quarter = reporting_quarter

        # Validate inputs
        if return_type == 'RRQ' and reporting_quarter is None:
            raise ValueError("reporting_quarter is required for RRQ return type")

        # Create output directory with return type suffix
        if return_type == 'RRQ':
            self.output_dir = f"{output_dir}_{return_type.lower()}_{reporting_year}_{reporting_quarter.lower()}"
        else:
            self.output_dir = f"{output_dir}_{return_type.lower()}_{reporting_year}"

        os.makedirs(self.output_dir, exist_ok=True)

        # Lloyd's syndicate numbers (realistic ranges)
        self.syndicates = [2987, 33, 1183, 2791, 623, 4242, 5000, 1910, 2010, 2525]

        # Determine years of account scope based on return type
        self.current_year = reporting_year
        if return_type == 'RRA':
            # RRA: All historical years
            self.years_of_account = list(range(2018, reporting_year + 1))
        else:  # RRQ
            # RRQ: Current year + prior 2 years only
            self.years_of_account = list(range(reporting_year - 2, reporting_year + 1))

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

        # Determine "as at" date based on quarter
        self.as_at_date = self._get_as_at_date()

        # Define which forms are required for this return type and quarter
        self.required_forms = self._get_required_forms()

    def _get_as_at_date(self) -> str:
        """Get the 'as at' date based on return type and quarter"""
        if self.return_type == 'RRA':
            return f'{self.reporting_year}-12-31'
        else:  # RRQ
            quarter_end_dates = {
                'Q1': f'{self.reporting_year}-03-31',
                'Q2': f'{self.reporting_year}-06-30',
                'Q3': f'{self.reporting_year}-09-30',
                'Q4': f'{self.reporting_year}-12-31'
            }
            return quarter_end_dates[self.reporting_quarter]

    def _get_required_forms(self) -> List[str]:
        """Determine which forms are required based on return type and quarter"""
        # Forms required in all RRQ quarters (V2: added 191, 192)
        rrq_all_quarters = ['010', '020', '071', '091', '191', '192', '193', '291', '292', '293', '294', '295', '990']

        # Forms only required in Q4 for RRQ
        rrq_q4_only = ['081', '391', '910']

        # All RRA forms (V2: added 591)
        rra_all = ['010', '020', '071', '081', '091', '193', '291', '292', '293', '294', '295', '391', '591', '910', '990']

        if self.return_type == 'RRA':
            return rra_all
        else:  # RRQ
            if self.reporting_quarter == 'Q4':
                return rrq_all_quarters + rrq_q4_only
            else:
                return rrq_all_quarters

    def generate_control_data(self):
        """Generate Form 010 Control Data"""
        control_data = []

        for syndicate in self.syndicates:
            control_data.append({
                'Syndicate_Number': syndicate,
                'Return_Type': self.return_type,
                'Reporting_Quarter': self.reporting_quarter if self.return_type == 'RRQ' else 'N/A',
                'Reporting_Year': self.reporting_year,
                'Status': random.choice(['Draft', 'Submitted', 'Approved']),
                'Edition': '1.1',
                'Managing_Agent_Name': f'Managing Agent {syndicate}',
                'First_Pure_YoA': min(self.years_of_account),
                'First_Reporting_YoA': min(self.years_of_account),
                'Final_Pure_YoA': max(self.years_of_account) - 1 if self.return_type == 'RRA' else max(self.years_of_account),
                'Prospective_Year': max(self.years_of_account) if self.return_type == 'RRA' else 'N/A',
                'Contact_Username': f'user{syndicate}',
                'Contact_Name': f'Contact Person {syndicate}',
                'Contact_Phone': f'+44 20 {random.randint(7000, 7999)} {random.randint(1000, 9999)}',
                'Contact_Email': f'contact{syndicate}@lloyds.com',
                'Submission_Date': datetime.now().strftime('%Y-%m-%d'),
                'As_At_Date': self.as_at_date,
                'Capacity_GBP': random.randint(50000000, 500000000)
            })

        df = pd.DataFrame(control_data)
        filename = f'{self.return_type.lower()}_010_control.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 010 Control: {len(df)} records")
        return df

    def generate_exchange_rates(self):
        """Generate Form 020 Exchange Rates"""
        exchange_rates = []

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
                variation = random.uniform(0.95, 1.05)
                exchange_rates.append({
                    'Return_Type': self.return_type,
                    'Reporting_Period': self.as_at_date,
                    'Year_of_Account': year,
                    'Currency_Code': currency,
                    'Currency_Name': currency,
                    'Exchange_Rate_to_GBP': round(base_rate * variation, 4),
                    'Rate_Type': 'Average',
                    'Effective_Date': self.as_at_date
                })

        df = pd.DataFrame(exchange_rates)
        filename = f'{self.return_type.lower()}_020_exchange_rates.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 020 Exchange Rates: {len(df)} records")
        return df

    def generate_net_claims(self):
        """Generate Form 193 Net Claims Data with RRQ/RRA scoping"""
        net_claims = []

        for syndicate in self.syndicates:
            for year in self.years_of_account:
                for lob_code in list(self.classes_of_business.keys())[:5]:
                    # Determine development years based on return type
                    if self.return_type == 'RRA':
                        # RRA: Full development history
                        max_dev = min(8, self.reporting_year - year + 1)
                    else:  # RRQ
                        # RRQ: Limited development (typically 0-2 years)
                        max_dev = min(3, self.reporting_year - year + 1)

                    for development_year in range(0, max_dev):
                        base_premium = random.randint(1000000, 20000000)
                        loss_ratio = random.uniform(0.45, 0.85)
                        development_factor = min(1.0, 0.2 + (development_year * 0.15))

                        cumulative_paid = int(base_premium * loss_ratio * development_factor)
                        case_reserves = int(base_premium * loss_ratio * (1 - development_factor) * 0.6)
                        ibnr = int(base_premium * loss_ratio * (1 - development_factor) * 0.4)

                        net_claims.append({
                            'Return_Type': self.return_type,
                            'Reporting_Quarter': self.reporting_quarter if self.return_type == 'RRQ' else 'N/A',
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
                            'As_At_Date': self.as_at_date,
                            'Calendar_Period': f'{year + development_year}'
                        })

        df = pd.DataFrame(net_claims)
        filename = f'{self.return_type.lower()}_193_net_claims.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 193 Net Claims: {len(df)} records")
        return df

    def generate_gross_premium_ibnr(self):
        """Generate Form 291 Gross Premium and IBNR"""
        gross_data = []

        for syndicate in self.syndicates:
            for year in self.years_of_account:
                for lob_code in list(self.classes_of_business.keys())[:5]:
                    gwp = random.randint(5000000, 50000000)
                    ultimate_loss_ratio = random.uniform(0.55, 0.75)

                    gross_data.append({
                        'Return_Type': self.return_type,
                        'Reporting_Quarter': self.reporting_quarter if self.return_type == 'RRQ' else 'N/A',
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
                        'As_At_Date': self.as_at_date
                    })

        df = pd.DataFrame(gross_data)
        filename = f'{self.return_type.lower()}_291_gross_premium_ibnr.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 291 Gross Premium & IBNR: {len(df)} records")
        return df

    def generate_scob_mapping(self):
        """Generate Form 071 SCOB Mapping"""
        scob_data = []

        # Solvency II LOB mapping
        sii_lobs = {
            'A1': ('1', 'Medical expense insurance'),
            'A2': ('2', 'Income protection insurance'),
            'D1': ('4', 'Motor vehicle liability insurance'),
            'D2': ('5', 'Other motor insurance'),
            'E1': ('6', 'Marine, aviation and transport insurance'),
            'E2': ('6', 'Marine, aviation and transport insurance'),
            'F1': ('7', 'Fire and other damage to property insurance'),
            'F2': ('7', 'Fire and other damage to property insurance'),
            'M1': ('6', 'Marine, aviation and transport insurance'),
            'M2': ('6', 'Marine, aviation and transport insurance'),
            'M3': ('11', 'General liability insurance'),
            'N1': ('28', 'Non-proportional property reinsurance'),
            'N2': ('7', 'Fire and other damage to property insurance'),
            'P1': ('11', 'General liability insurance'),
            'P2': ('11', 'General liability insurance'),
            'T1': ('11', 'General liability insurance'),
            'T2': ('26', 'Non-proportional casualty reinsurance'),
            'V1': ('6', 'Marine, aviation and transport insurance'),
            'W1': ('12', 'Credit and suretyship insurance'),
            'X1': ('28', 'Non-proportional property reinsurance'),
        }

        for syndicate in self.syndicates:
            for scob_code, scob_desc in self.classes_of_business.items():
                sii_code, sii_desc = sii_lobs.get(scob_code, ('99', 'Other'))
                scob_data.append({
                    'Syndicate_Number': syndicate,
                    'SCOB_Code': scob_code,
                    'SCOB_Description': scob_desc,
                    'SII_LOB_Code': sii_code,
                    'SII_LOB_Description': sii_desc,
                    'Allocation_Percentage': 100,
                    'Year_of_Account': max(self.years_of_account),
                    'As_At_Date': self.as_at_date
                })

        df = pd.DataFrame(scob_data)
        filename = f'{self.return_type.lower()}_071_scob_mapping.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 071 SCOB Mapping: {len(df)} records")
        return df

    def generate_reserving_class(self):
        """Generate Form 081 Reserving Class Information"""
        reserving_data = []

        patterns = ['Short Tail', 'Medium Tail', 'Long Tail']
        methods = ['Chain Ladder', 'BF Method', 'Cape Cod', 'Expected Loss Ratio']

        reserving_classes = {
            'RC01': ('Motor', ['D1', 'D2'], 'Short Tail'),
            'RC02': ('Property', ['F1', 'F2', 'N1', 'N2'], 'Short Tail'),
            'RC03': ('Marine', ['M1', 'M2', 'M3'], 'Medium Tail'),
            'RC04': ('Casualty', ['T1', 'T2', 'P1', 'P2'], 'Long Tail'),
            'RC05': ('Energy', ['E1', 'E2'], 'Medium Tail'),
            'RC06': ('Aviation', ['V1'], 'Medium Tail'),
            'RC07': ('Accident & Health', ['A1', 'A2'], 'Short Tail'),
            'RC08': ('Specialty', ['W1', 'X1'], 'Long Tail'),
        }

        for syndicate in self.syndicates:
            for rc_code, (rc_name, scobs, pattern) in reserving_classes.items():
                reserving_data.append({
                    'Syndicate_Number': syndicate,
                    'Reserving_Class_Code': rc_code,
                    'Reserving_Class_Name': rc_name,
                    'SCOB_Codes': ','.join(scobs),
                    'Development_Pattern': pattern,
                    'Actuarial_Method': random.choice(methods),
                    'Year_of_Account': max(self.years_of_account),
                    'As_At_Date': self.as_at_date
                })

        df = pd.DataFrame(reserving_data)
        filename = f'{self.return_type.lower()}_081_reserving_class.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 081 Reserving Class: {len(df)} records")
        return df

    def generate_lpt_data(self):
        """Generate Form 091 LPT Data"""
        lpt_data = []

        transaction_types = ['LPT', 'ADC', 'RITC']
        counterparties = ['Swiss Re', 'Munich Re', 'Berkshire Hathaway', 'Lloyd\'s Central Fund']

        for syndicate in self.syndicates:
            # Not all syndicates have LPT transactions
            if random.random() > 0.3:
                num_transactions = random.randint(1, 3)
                for _ in range(num_transactions):
                    reserves = random.randint(10000000, 100000000)
                    premium_ratio = random.uniform(0.85, 1.05)
                    yoas = random.sample(self.years_of_account[:-1], min(3, len(self.years_of_account) - 1))

                    lpt_data.append({
                        'Syndicate_Number': syndicate,
                        'Transaction_Type': random.choice(transaction_types),
                        'Counterparty': random.choice(counterparties),
                        'Effective_Date': f'{self.reporting_year}-01-01',
                        'Years_of_Account': ','.join(map(str, sorted(yoas))),
                        'Gross_Reserves_Transferred_GBP': reserves,
                        'Net_Premium_GBP': int(reserves * premium_ratio),
                        'Cover_Limit_GBP': int(reserves * 1.5),
                        'Retention_GBP': int(reserves * 0.1),
                        'As_At_Date': self.as_at_date
                    })

        df = pd.DataFrame(lpt_data)
        filename = f'{self.return_type.lower()}_091_lpt_data.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 091 LPT Data: {len(df)} records")
        return df

    def generate_net_premium_ibnr(self):
        """Generate Form 292 Net Premium and IBNR"""
        net_data = []

        for syndicate in self.syndicates:
            for year in self.years_of_account:
                for lob_code in list(self.classes_of_business.keys())[:5]:
                    gwp = random.randint(5000000, 50000000)
                    retention = random.uniform(0.75, 0.90)
                    nwp = int(gwp * retention)
                    loss_ratio = random.uniform(0.55, 0.75)

                    net_data.append({
                        'Return_Type': self.return_type,
                        'Syndicate_Number': syndicate,
                        'Year_of_Account': year,
                        'LOB_Code': lob_code,
                        'Currency': 'GBP',
                        'Gross_Written_Premium': gwp,
                        'Net_Written_Premium': nwp,
                        'Ceded_Premium': gwp - nwp,
                        'Retention_Ratio': round(retention, 4),
                        'Paid_Claims_Net': int(nwp * loss_ratio * random.uniform(0.4, 0.7)),
                        'Case_Reserves_Net': int(nwp * loss_ratio * random.uniform(0.1, 0.2)),
                        'IBNR_Net': int(nwp * loss_ratio * random.uniform(0.15, 0.30)),
                        'RI_Recovery_Paid': int((gwp - nwp) * loss_ratio * random.uniform(0.3, 0.5)),
                        'RI_Recovery_OS': int((gwp - nwp) * loss_ratio * random.uniform(0.2, 0.4)),
                        'As_At_Date': self.as_at_date
                    })

        df = pd.DataFrame(net_data)
        filename = f'{self.return_type.lower()}_292_net_premium_ibnr.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 292 Net Premium & IBNR: {len(df)} records")
        return df

    def generate_outstanding_ibnr_pyoa(self):
        """Generate Form 293 Outstanding & IBNR by PYoA"""
        pyoa_data = []

        for syndicate in self.syndicates:
            current_yoa = max(self.years_of_account)
            for prior_yoa in self.years_of_account[:-1]:
                for lob_code in list(self.classes_of_business.keys())[:3]:
                    base_amount = random.randint(1000000, 20000000)
                    age = current_yoa - prior_yoa

                    # Older years have more paid, less outstanding
                    paid_factor = min(0.9, 0.3 + age * 0.15)
                    gross_os = int(base_amount * (1 - paid_factor) * 0.6)
                    gross_ibnr = int(base_amount * (1 - paid_factor) * 0.4)
                    retention = random.uniform(0.75, 0.90)

                    pyoa_data.append({
                        'Syndicate_Number': syndicate,
                        'Year_of_Account': current_yoa,
                        'Prior_YoA': prior_yoa,
                        'Class_of_Business': lob_code,
                        'Gross_Outstanding_GBP': gross_os,
                        'Gross_IBNR_GBP': gross_ibnr,
                        'Net_Outstanding_GBP': int(gross_os * retention),
                        'Net_IBNR_GBP': int(gross_ibnr * retention),
                        'Currency': 'GBP',
                        'As_At_Date': self.as_at_date
                    })

        df = pd.DataFrame(pyoa_data)
        filename = f'{self.return_type.lower()}_293_outstanding_ibnr_pyoa.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 293 Outstanding & IBNR by PYoA: {len(df)} records")
        return df

    def generate_catastrophe_ibnr(self):
        """Generate Form 294 Catastrophe IBNR"""
        cat_data = []

        for syndicate in self.syndicates:
            # Each syndicate affected by 2-4 cat events
            num_events = random.randint(2, 4)
            selected_cats = random.sample(list(self.cat_codes.keys()), num_events)

            for cat_code in selected_cats:
                for year in self.years_of_account[-3:]:  # Last 3 years
                    gross_ibnr = random.randint(5000000, 50000000)
                    ri_recovery = random.uniform(0.3, 0.6)

                    cat_data.append({
                        'Syndicate_Number': syndicate,
                        'Year_of_Account': year,
                        'Event_Code': cat_code,
                        'Event_Name': self.cat_codes[cat_code],
                        'Event_Date': f'{year}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}',
                        'Gross_IBNR_GBP': gross_ibnr,
                        'Net_IBNR_GBP': int(gross_ibnr * (1 - ri_recovery)),
                        'Expected_Recovery_GBP': int(gross_ibnr * ri_recovery),
                        'Confidence_Level': random.choice(['High', 'Medium', 'Low']),
                        'As_At_Date': self.as_at_date
                    })

        df = pd.DataFrame(cat_data)
        filename = f'{self.return_type.lower()}_294_catastrophe_ibnr.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 294 Catastrophe IBNR: {len(df)} records")
        return df

    def generate_ulae(self):
        """Generate Form 295 ULAE"""
        ulae_data = []

        expense_types = ['Claims Handling', 'Legal', 'Investigation', 'Administration']
        allocation_methods = ['Premium Based', 'Claims Based', 'Hybrid']

        for syndicate in self.syndicates:
            for year in self.years_of_account:
                basis_premium = random.randint(50000000, 200000000)

                for category in ['Internal', 'External']:
                    for exp_type in expense_types:
                        ulae_ratio = random.uniform(0.02, 0.06)
                        gross_ulae = int(basis_premium * ulae_ratio)
                        retention = random.uniform(0.85, 0.95)

                        ulae_data.append({
                            'Syndicate_Number': syndicate,
                            'Year_of_Account': year,
                            'ULAE_Category': category,
                            'Expense_Type': exp_type,
                            'Gross_ULAE_GBP': gross_ulae,
                            'Net_ULAE_GBP': int(gross_ulae * retention),
                            'Allocation_Method': random.choice(allocation_methods),
                            'Basis_Premium_GBP': basis_premium,
                            'As_At_Date': self.as_at_date
                        })

        df = pd.DataFrame(ulae_data)
        filename = f'{self.return_type.lower()}_295_ulae.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 295 ULAE: {len(df)} records")
        return df

    def generate_ielr(self):
        """Generate Form 391 IELR"""
        ielr_data = []

        methods = ['Chain Ladder', 'BF Method', 'Cape Cod', 'Expected Loss Ratio']

        for syndicate in self.syndicates:
            for year in self.years_of_account:
                for lob_code in list(self.classes_of_business.keys())[:5]:
                    initial_elr = random.uniform(55, 75)
                    current_elr = initial_elr + random.uniform(-5, 10)
                    premium = random.randint(10000000, 100000000)

                    ielr_data.append({
                        'Syndicate_Number': syndicate,
                        'Year_of_Account': year,
                        'Class_of_Business': lob_code,
                        'Reserving_Class': f'RC0{random.randint(1, 5)}',
                        'Initial_ELR': round(initial_elr, 2),
                        'Current_ELR': round(current_elr, 2),
                        'Gross_Premium_GBP': premium,
                        'Selected_Ultimate_GBP': int(premium * current_elr / 100),
                        'Method': random.choice(methods),
                        'As_At_Date': self.as_at_date
                    })

        df = pd.DataFrame(ielr_data)
        filename = f'{self.return_type.lower()}_391_ielr.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 391 IELR: {len(df)} records")
        return df

    def generate_reinsurance_structure(self):
        """Generate Form 591 Syndicate Reinsurance Structure (V2 NEW)"""
        ri_data = []

        program_types = ['Quota Share', 'Excess of Loss', 'Stop Loss', 'Facultative']
        reinsurers = [
            ('Swiss Re', 'AA-'),
            ('Munich Re', 'AA-'),
            ('Hannover Re', 'AA-'),
            ('SCOR', 'AA-'),
            ('Lloyd\'s Syndicates', 'A+'),
            ('Berkshire Hathaway', 'AA'),
            ('Everest Re', 'A+'),
            ('RenaissanceRe', 'A+'),
        ]

        for syndicate in self.syndicates:
            for year in self.years_of_account[-2:]:  # Current and prior year
                # Each syndicate has 3-6 reinsurance treaties
                num_treaties = random.randint(3, 6)

                for treaty_num in range(num_treaties):
                    reinsurer, rating = random.choice(reinsurers)
                    program_type = random.choice(program_types)

                    if program_type == 'Quota Share':
                        cession = random.uniform(0.10, 0.30)
                        attachment = 0
                        limit = random.randint(50000000, 200000000)
                    else:
                        cession = 0
                        attachment = random.randint(5000000, 50000000)
                        limit = random.randint(20000000, 100000000)

                    premium = int(limit * random.uniform(0.02, 0.15))

                    ri_data.append({
                        'Syndicate_Number': syndicate,
                        'Year_of_Account': year,
                        'Program_Type': program_type,
                        'Reinsurer_Name': reinsurer,
                        'Reinsurer_Rating': rating,
                        'Coverage_Layer': f'Layer {treaty_num + 1}',
                        'Attachment_Point_GBP': attachment,
                        'Limit_GBP': limit,
                        'Premium_GBP': premium,
                        'Cession_Rate': round(cession, 4),
                        'Effective_Date': f'{year}-01-01',
                        'Expiry_Date': f'{year}-12-31',
                        'Treaty_Reference': f'TRY-{syndicate}-{year}-{treaty_num + 1:03d}',
                        'As_At_Date': self.as_at_date
                    })

        df = pd.DataFrame(ri_data)
        filename = f'{self.return_type.lower()}_591_reinsurance_structure.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 591 Reinsurance Structure: {len(df)} records")
        return df

    def generate_additional_info(self):
        """Generate Form 910 Additional Information"""
        info_data = []

        sections = ['A', 'B', 'C', 'D']
        questions = {
            'A': ['Reserving methodology changes', 'Significant events impacting reserves'],
            'B': ['Reinsurance program changes', 'Counterparty credit concerns'],
            'C': ['Large loss developments', 'Cat event updates'],
            'D': ['Other material matters', 'Prospective year assumptions'],
        }

        for syndicate in self.syndicates:
            for section in sections:
                for q_num, question in enumerate(questions[section], 1):
                    info_data.append({
                        'Syndicate_Number': syndicate,
                        'Year_of_Account': max(self.years_of_account),
                        'Section': f'Section {section}',
                        'Question_Number': f'{section}{q_num}',
                        'Question_Text': question,
                        'Response': f'Response for {question} - Syndicate {syndicate}. No material issues to report.',
                        'Supporting_Reference': f'Table {random.randint(1, 10)}' if random.random() > 0.5 else None,
                        'Response_Date': self.as_at_date
                    })

        df = pd.DataFrame(info_data)
        filename = f'{self.return_type.lower()}_910_additional_info.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 910 Additional Information: {len(df)} records")
        return df

    def generate_validation_summary(self):
        """Generate Form 990 Validation Summary"""
        validation_data = []

        form_codes = self.required_forms
        statuses = ['Pass', 'Pass with Warnings', 'Pass']  # Weighted towards pass

        for syndicate in self.syndicates:
            for form_code in form_codes:
                if form_code == '990':
                    continue  # Don't validate the validation form

                status = random.choice(statuses)
                warnings = random.randint(0, 3) if 'Warnings' in status else 0

                validation_data.append({
                    'Syndicate_Number': syndicate,
                    'Return_Type': self.return_type,
                    'Form_Code': form_code,
                    'Validation_Status': status,
                    'Warnings_Count': warnings,
                    'Errors_Count': 0,
                    'Last_Validated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Validated_By': f'System',
                    'As_At_Date': self.as_at_date
                })

        df = pd.DataFrame(validation_data)
        filename = f'{self.return_type.lower()}_990_validation.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated {self.return_type} 990 Validation Summary: {len(df)} records")
        return df

    def generate_gross_claims_rrq(self):
        """Generate RRQ Form 191 Gross Claims Development (V2 NEW)"""
        claims_data = []

        for syndicate in self.syndicates:
            for year in self.years_of_account:
                for lob_code in list(self.classes_of_business.keys())[:5]:
                    max_dev = min(3, self.reporting_year - year + 1)

                    for dev_year in range(max_dev):
                        base_premium = random.randint(5000000, 50000000)
                        loss_ratio = random.uniform(0.50, 0.80)
                        development_factor = min(1.0, 0.25 + (dev_year * 0.20))

                        gross_paid = int(base_premium * loss_ratio * development_factor)
                        gross_case = int(base_premium * loss_ratio * (1 - development_factor) * 0.5)
                        gross_ibnr = int(base_premium * loss_ratio * (1 - development_factor) * 0.5)

                        claims_data.append({
                            'Syndicate_Number': syndicate,
                            'Year_of_Account': year,
                            'Development_Year': dev_year,
                            'Class_of_Business': lob_code,
                            'Currency': 'GBP',
                            'Gross_Paid_Claims': gross_paid,
                            'Gross_Case_Reserves': gross_case,
                            'Gross_IBNR': gross_ibnr,
                            'Gross_Incurred': gross_paid + gross_case + gross_ibnr,
                            'Reporting_Period': self.as_at_date
                        })

        df = pd.DataFrame(claims_data)
        filename = 'rrq_191_gross_claims.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated RRQ 191 Gross Claims Development: {len(df)} records")
        return df

    def generate_claims_triangles_rrq(self):
        """Generate RRQ Form 192 Claims Triangles Summary (V2 NEW)"""
        triangle_data = []

        triangle_types = ['Paid', 'Incurred', 'Case']
        bases = ['Gross', 'Net']
        methods = ['Chain Ladder', 'BF Method', 'Cape Cod']

        for syndicate in self.syndicates:
            for year in self.years_of_account:
                for tri_type in triangle_types:
                    for basis in bases:
                        base_premium = random.randint(10000000, 80000000)
                        loss_ratio = random.uniform(0.55, 0.75)
                        ultimate = int(base_premium * loss_ratio)

                        # Generate development columns
                        row = {
                            'Syndicate_Number': syndicate,
                            'Year_of_Account': year,
                            'Triangle_Type': tri_type,
                            'Basis': basis,
                            'Class_of_Business': random.choice(list(self.classes_of_business.keys())[:5]),
                            'Currency': 'GBP',
                        }

                        # Add development year columns
                        cumulative = 0
                        max_dev = min(10, self.reporting_year - year + 1)
                        for dev in range(11):
                            if dev < max_dev:
                                increment = ultimate * random.uniform(0.08, 0.15)
                                cumulative += increment
                                row[f'Dev_Year_{dev}'] = int(min(cumulative, ultimate))
                            else:
                                row[f'Dev_Year_{dev}'] = None

                        # Calculate IBNR
                        latest = row.get(f'Dev_Year_{max_dev - 1}', 0) or 0
                        ibnr = max(0, ultimate - latest)

                        row['Ultimate_Estimate'] = ultimate
                        row['Selected_IBNR'] = int(ibnr)
                        row['Method'] = random.choice(methods)
                        row['Reporting_Period'] = self.as_at_date

                        triangle_data.append(row)

        df = pd.DataFrame(triangle_data)
        filename = 'rrq_192_claims_triangles.csv'
        df.to_csv(f'{self.output_dir}/{filename}', index=False)
        print(f"✓ Generated RRQ 192 Claims Triangles Summary: {len(df)} records")
        return df

    def generate_all_data(self):
        """Generate all required forms based on return type and quarter (V2: Complete coverage)"""
        print("\n" + "="*70)
        print(f"Generating Synthetic Lloyd's {self.return_type} Data (V2.0)")
        if self.return_type == 'RRQ':
            print(f"Quarter: {self.reporting_quarter} {self.reporting_year}")
        else:
            print(f"Year: {self.reporting_year}")
        print(f"Years of Account in Scope: {min(self.years_of_account)}-{max(self.years_of_account)}")
        print(f"As At Date: {self.as_at_date}")
        print(f"Forms to Generate: {len(self.required_forms)}")
        print("="*70 + "\n")

        # Generate all forms based on requirements
        if '010' in self.required_forms:
            self.generate_control_data()

        if '020' in self.required_forms:
            self.generate_exchange_rates()

        if '071' in self.required_forms:
            self.generate_scob_mapping()

        if '081' in self.required_forms:
            self.generate_reserving_class()

        if '091' in self.required_forms:
            self.generate_lpt_data()

        if '191' in self.required_forms:
            self.generate_gross_claims_rrq()

        if '192' in self.required_forms:
            self.generate_claims_triangles_rrq()

        if '193' in self.required_forms:
            self.generate_net_claims()

        if '291' in self.required_forms:
            self.generate_gross_premium_ibnr()

        if '292' in self.required_forms:
            self.generate_net_premium_ibnr()

        if '293' in self.required_forms:
            self.generate_outstanding_ibnr_pyoa()

        if '294' in self.required_forms:
            self.generate_catastrophe_ibnr()

        if '295' in self.required_forms:
            self.generate_ulae()

        if '391' in self.required_forms:
            self.generate_ielr()

        if '591' in self.required_forms:
            self.generate_reinsurance_structure()

        if '910' in self.required_forms:
            self.generate_additional_info()

        if '990' in self.required_forms:
            self.generate_validation_summary()

        print("\n" + "="*70)
        print(f"All {self.return_type} data generated successfully in: {self.output_dir}")
        print(f"Forms generated: {', '.join(sorted(self.required_forms))}")
        print("="*70 + "\n")


def generate_full_year_rrq(year: int = 2024, output_base_dir: str = '../../synthetic_data'):
    """
    Generate RRQ data for all four quarters of a year

    Parameters:
    -----------
    year : int
        Reporting year
    output_base_dir : str
        Base output directory
    """
    print("\n" + "="*70)
    print(f"Generating Full Year RRQ Data for {year}")
    print("="*70 + "\n")

    quarters = ['Q1', 'Q2', 'Q3', 'Q4']

    for quarter in quarters:
        print(f"\nGenerating {quarter} {year}...")
        print("-" * 70)

        generator = UnifiedLloydsDataGenerator(
            return_type='RRQ',
            reporting_year=year,
            reporting_quarter=quarter,
            output_dir=output_base_dir
        )
        generator.generate_all_data()

    print("\n" + "="*70)
    print(f"Complete! Generated RRQ data for all quarters of {year}")
    print("="*70 + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate Unified Lloyd\'s RRQ/RRA Data')
    parser.add_argument('--type', choices=['RRQ', 'RRA'], default='RRA',
                        help='Return type: RRQ or RRA')
    parser.add_argument('--year', type=int, default=2024,
                        help='Reporting year')
    parser.add_argument('--quarter', choices=['Q1', 'Q2', 'Q3', 'Q4'],
                        help='Reporting quarter (required for RRQ)')
    parser.add_argument('--all-quarters', action='store_true',
                        help='Generate all four quarters of RRQ data')
    parser.add_argument('--output', default='../../synthetic_data',
                        help='Output directory')

    args = parser.parse_args()

    if args.all_quarters:
        # Generate all quarters
        generate_full_year_rrq(args.year, args.output)
    else:
        # Generate single return
        generator = UnifiedLloydsDataGenerator(
            return_type=args.type,
            reporting_year=args.year,
            reporting_quarter=args.quarter,
            output_dir=args.output
        )
        generator.generate_all_data()

    print("\nSynthetic Lloyd's data generation complete!")
    print("Files can now be imported into Power BI for testing RRA/RRQ reports.")
