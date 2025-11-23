"""
RRA Forms Data Generator for Power BI
=====================================
Generates all 14 RRA (Reserving Return Annual) forms for Lloyd's syndicates.
Compatible with Power BI as a Python data source.

Tables Generated:
- rra_010: Control data and syndicate metadata
- rra_020: Exchange rates
- rra_071: SCOB Mapping (Solvency II Classes of Business)
- rra_081: Reserving class information
- rra_091: Lloyd's Pension Trust (LPT) transfers
- rra_193: Net Claims Development
- rra_291: Gross Premium and IBNR
- rra_292: Net Premium and IBNR
- rra_293: Outstanding IBNR by previous years of account
- rra_294: Catastrophe IBNR
- rra_295: ULAE (Unallocated Loss Adjustment Expenses)
- rra_391: IELR (Initial Expected Loss Ratio)
- rra_910: Additional information
- rra_990: Validation Summary

Usage in Power BI:
1. Get Data > More > Python script
2. Copy and paste this script
3. Select the tables you need from the list
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_SYNDICATES = 10
CURRENT_YEAR = 2024
YEARS_OF_ACCOUNT = list(range(2018, 2026))

# Lloyd's syndicate numbers (realistic ranges)
SYNDICATES = [2987, 33, 1183, 2791, 623, 4242, 5000, 1910, 2010, 2525]

# Classes of Business (Lloyd's typical classes)
CLASSES_OF_BUSINESS = {
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
CAT_CODES = {
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
CURRENCIES = ['GBP', 'USD', 'EUR', 'CAD', 'AUD', 'JPY']


# =============================================================================
# RRA 010 - Control Data
# =============================================================================
def generate_rra_010():
    """Generate RRA 010 Control Data"""
    control_data = []

    for syndicate in SYNDICATES:
        control_data.append({
            'Syndicate_Number': syndicate,
            'Return_Type': 'RRA',
            'Status': random.choice(['Draft', 'Submitted', 'Approved']),
            'Edition': '1.1',
            'Managing_Agent_Name': f'Managing Agent {syndicate}',
            'First_Pure_YoA': min(YEARS_OF_ACCOUNT),
            'First_Reporting_YoA': min(YEARS_OF_ACCOUNT),
            'Final_Pure_YoA': max(YEARS_OF_ACCOUNT) - 1,
            'Prospective_Year': max(YEARS_OF_ACCOUNT),
            'Contact_Username': f'user{syndicate}',
            'Contact_Name': f'Contact Person {syndicate}',
            'Contact_Phone': f'+44 20 {random.randint(7000, 7999)} {random.randint(1000, 9999)}',
            'Contact_Email': f'contact{syndicate}@lloyds.com',
            'Submission_Date': datetime.now().strftime('%Y-%m-%d'),
            'Capacity_GBP': random.randint(50000000, 500000000)
        })

    return pd.DataFrame(control_data)


# =============================================================================
# RRA 020 - Exchange Rates
# =============================================================================
def generate_rra_020():
    """Generate RRA 020 Exchange Rates"""
    exchange_rates = []

    base_rates = {
        'USD': 1.27,
        'EUR': 1.17,
        'CAD': 1.72,
        'AUD': 1.95,
        'JPY': 188.5,
        'GBP': 1.00
    }

    for year in YEARS_OF_ACCOUNT:
        for currency, base_rate in base_rates.items():
            variation = random.uniform(0.95, 1.05)
            exchange_rates.append({
                'Year_of_Account': year,
                'Currency_Code': currency,
                'Currency_Name': currency,
                'Exchange_Rate_to_GBP': round(base_rate * variation, 4),
                'Rate_Type': 'Average',
                'Effective_Date': f'{year}-12-31'
            })

    return pd.DataFrame(exchange_rates)


# =============================================================================
# RRA 071 - SCOB Mapping
# =============================================================================
def generate_rra_071():
    """Generate RRA 071 SCOB (Syndicate Class of Business) Mapping"""
    scob_mapping = []

    for syndicate in SYNDICATES:
        num_classes = random.randint(3, 7)
        selected_classes = random.sample(list(CLASSES_OF_BUSINESS.keys()), num_classes)

        for class_code in selected_classes:
            scob_mapping.append({
                'Syndicate_Number': syndicate,
                'SCOB_Code': f'{class_code}_{syndicate}',
                'LOB_Code': class_code,
                'LOB_Description': CLASSES_OF_BUSINESS[class_code],
                'Reserving_Class': f'RC_{class_code}',
                'Active_Flag': 'Y',
                'Effective_From': f'{min(YEARS_OF_ACCOUNT)}-01-01',
                'Effective_To': f'{max(YEARS_OF_ACCOUNT)}-12-31'
            })

    return pd.DataFrame(scob_mapping)


# =============================================================================
# RRA 081 - Reserving Class Info
# =============================================================================
def generate_rra_081():
    """Generate RRA 081 Reserving Class Information"""
    res_class_info = []

    for syndicate in SYNDICATES:
        for lob_code, lob_desc in CLASSES_OF_BUSINESS.items():
            res_class_info.append({
                'Syndicate_Number': syndicate,
                'Reserving_Class_Code': f'RC_{lob_code}',
                'Reserving_Class_Description': f'{lob_desc} - Reserves',
                'LOB_Code': lob_code,
                'Development_Pattern': random.choice(['Short Tail', 'Medium Tail', 'Long Tail']),
                'Average_Settlement_Years': random.randint(1, 15),
                'Actuarial_Method': random.choice(['Chain Ladder', 'BF Method', 'Cape Cod', 'Expected Loss Ratio']),
                'Last_Review_Date': f'{CURRENT_YEAR}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'
            })

    return pd.DataFrame(res_class_info)


# =============================================================================
# RRA 091 - LPT Data
# =============================================================================
def generate_rra_091():
    """Generate RRA 091 LPT (Loss Portfolio Transfer) Data"""
    lpt_data = []

    for syndicate in random.sample(SYNDICATES, k=3):
        for year in random.sample(YEARS_OF_ACCOUNT[:-2], k=2):
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

    return pd.DataFrame(lpt_data)


# =============================================================================
# RRA 193 - Net Claims
# =============================================================================
def generate_rra_193():
    """Generate RRA 193 Net Claims Data"""
    net_claims = []

    for syndicate in SYNDICATES:
        for year in YEARS_OF_ACCOUNT[:-1]:
            for lob_code in list(CLASSES_OF_BUSINESS.keys())[:5]:
                for development_year in range(0, min(8, CURRENT_YEAR - year + 1)):

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

    return pd.DataFrame(net_claims)


# =============================================================================
# RRA 291 - Gross Premium and IBNR
# =============================================================================
def generate_rra_291():
    """Generate RRA 291 Gross Premium and IBNR"""
    gross_data = []

    for syndicate in SYNDICATES:
        for year in YEARS_OF_ACCOUNT[:-1]:
            for lob_code in list(CLASSES_OF_BUSINESS.keys())[:5]:

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
                    'As_At_Date': f'{CURRENT_YEAR}-12-31'
                })

    return pd.DataFrame(gross_data)


# =============================================================================
# RRA 292 - Net Premium and IBNR
# =============================================================================
def generate_rra_292():
    """Generate RRA 292 Net Premium and IBNR Estimates"""
    net_data = []

    for syndicate in SYNDICATES:
        for year in YEARS_OF_ACCOUNT[:-1]:
            for lob_code in list(CLASSES_OF_BUSINESS.keys())[:5]:

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
                    'As_At_Date': f'{CURRENT_YEAR}-12-31'
                })

    return pd.DataFrame(net_data)


# =============================================================================
# RRA 293 - Outstanding & IBNR by PYOA
# =============================================================================
def generate_rra_293():
    """Generate RRA 293 Outstanding & IBNR (< 20 Pure Years of Account)"""
    os_ibnr_data = []

    for syndicate in SYNDICATES:
        for year in YEARS_OF_ACCOUNT[:-1]:
            for lob_code in list(CLASSES_OF_BUSINESS.keys())[:5]:

                outstanding = random.randint(500000, 15000000)
                ibnr = random.randint(300000, 10000000)
                num_claims = random.randint(20, 300)

                os_ibnr_data.append({
                    'Syndicate_Number': syndicate,
                    'Pure_Year_of_Account': year,
                    'LOB_Code': lob_code,
                    'Currency': 'GBP',
                    'Outstanding_Claims': outstanding,
                    'IBNR_Reserve': ibnr,
                    'Total_Reserve': outstanding + ibnr,
                    'Number_Outstanding_Claims': num_claims,
                    'Average_Outstanding_Claim': int(outstanding / num_claims) if num_claims > 0 else 0,
                    'Reserve_to_Premium_Ratio': round(random.uniform(0.3, 0.8), 4),
                    'As_At_Date': f'{CURRENT_YEAR}-12-31'
                })

    return pd.DataFrame(os_ibnr_data)


# =============================================================================
# RRA 294 - Catastrophe IBNR
# =============================================================================
def generate_rra_294():
    """Generate RRA 294 Gross IBNR Estimates (Catastrophe only)"""
    cat_ibnr_data = []

    cat_years = random.sample(YEARS_OF_ACCOUNT[:-1], k=4)

    for syndicate in SYNDICATES:
        for year in cat_years:
            for cat_code, cat_desc in random.sample(list(CAT_CODES.items()), k=2):

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
                    'As_At_Date': f'{CURRENT_YEAR}-12-31'
                })

    return pd.DataFrame(cat_ibnr_data)


# =============================================================================
# RRA 295 - ULAE
# =============================================================================
def generate_rra_295():
    """Generate RRA 295 ULAE (Unallocated Loss Adjustment Expenses)"""
    ulae_data = []

    for syndicate in SYNDICATES:
        for year in YEARS_OF_ACCOUNT[:-1]:

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
                'As_At_Date': f'{CURRENT_YEAR}-12-31'
            })

    return pd.DataFrame(ulae_data)


# =============================================================================
# RRA 391 - IELR
# =============================================================================
def generate_rra_391():
    """Generate RRA 391 IELR (Incurred Emerging Loss Ratio)"""
    ielr_data = []

    for syndicate in SYNDICATES:
        for year in YEARS_OF_ACCOUNT[:-1]:
            for lob_code in list(CLASSES_OF_BUSINESS.keys())[:5]:

                earned_premium = random.randint(5000000, 50000000)

                for dev_year in range(0, min(6, CURRENT_YEAR - year + 1)):
                    incurred_loss = int(earned_premium * random.uniform(0.50, 0.75) * min(1.0, 0.3 + dev_year * 0.15))

                    ielr_data.append({
                        'Syndicate_Number': syndicate,
                        'Year_of_Account': year,
                        'Development_Year': dev_year,
                        'LOB_Code': lob_code,
                        'Currency': 'GBP',
                        'Earned_Premium': earned_premium,
                        'Incurred_Loss': incurred_loss,
                        'Incurred_Loss_Ratio': round(incurred_loss / earned_premium, 4) if earned_premium > 0 else 0,
                        'Paid_Loss': int(incurred_loss * random.uniform(0.5, 0.9)),
                        'Outstanding_Reserve': int(incurred_loss * random.uniform(0.1, 0.5)),
                        'Calendar_Year': year + dev_year,
                        'As_At_Date': f'{year + dev_year}-12-31'
                    })

    return pd.DataFrame(ielr_data)


# =============================================================================
# RRA 910 - Additional Information
# =============================================================================
def generate_rra_910():
    """Generate RRA 910 - Additional Information"""
    rra_910_data = []

    for syndicate in SYNDICATES:
        rra_910_data.append({
            'Syndicate_Number': syndicate,
            'Reporting_Period': f'{CURRENT_YEAR}-12-31',
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
            'Sign_Off_Date': f'{CURRENT_YEAR}-12-31'
        })

    return pd.DataFrame(rra_910_data)


# =============================================================================
# RRA 990 - Validation Summary
# =============================================================================
def generate_rra_990():
    """Generate RRA 990 - Validation Summary"""
    rra_990_data = []

    for syndicate in SYNDICATES:
        rra_990_data.append({
            'Syndicate_Number': syndicate,
            'Reporting_Period': f'{CURRENT_YEAR}-12-31',
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

    return pd.DataFrame(rra_990_data)


# =============================================================================
# GENERATE ALL TABLES FOR POWER BI
# =============================================================================
print("Generating RRA Forms Data for Power BI...")
print("=" * 60)

# Generate all tables (these will be available in Power BI)
rra_010 = generate_rra_010()
rra_020 = generate_rra_020()
rra_071 = generate_rra_071()
rra_081 = generate_rra_081()
rra_091 = generate_rra_091()
rra_193 = generate_rra_193()
rra_291 = generate_rra_291()
rra_292 = generate_rra_292()
rra_293 = generate_rra_293()
rra_294 = generate_rra_294()
rra_295 = generate_rra_295()
rra_391 = generate_rra_391()
rra_910 = generate_rra_910()
rra_990 = generate_rra_990()

print(f"rra_010 (Control): {len(rra_010)} records")
print(f"rra_020 (Exchange Rates): {len(rra_020)} records")
print(f"rra_071 (SCOB Mapping): {len(rra_071)} records")
print(f"rra_081 (Reserving Class): {len(rra_081)} records")
print(f"rra_091 (LPT): {len(rra_091)} records")
print(f"rra_193 (Net Claims): {len(rra_193)} records")
print(f"rra_291 (Gross Premium IBNR): {len(rra_291)} records")
print(f"rra_292 (Net Premium IBNR): {len(rra_292)} records")
print(f"rra_293 (OS IBNR PYOA): {len(rra_293)} records")
print(f"rra_294 (Cat IBNR): {len(rra_294)} records")
print(f"rra_295 (ULAE): {len(rra_295)} records")
print(f"rra_391 (IELR): {len(rra_391)} records")
print(f"rra_910 (Additional Info): {len(rra_910)} records")
print(f"rra_990 (Validation): {len(rra_990)} records")
print("=" * 60)
print("All 14 RRA forms generated successfully!")
