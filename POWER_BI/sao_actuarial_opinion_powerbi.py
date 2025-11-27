# Statement of Actuarial Opinion (SAO) - Power BI Data Generator
# Annual Actuarial Opinion on Technical Provisions Adequacy
#
# SAO is the annual formal opinion on adequacy of technical provisions:
# - Opinion on gross and net reserves by syndicate
# - Supported by detailed internal analysis
# - Based on QMA (GAAP reserves) and RRA (actuarial best estimates)
# - Required annually for each syndicate
#
# Components:
# - Opinion summary and conclusions
# - Class-by-class reserve analysis
# - Actual vs Expected analysis
# - Key assumptions and methodology
# - Specific IBNR for large losses/cats
# - Margin analysis (booked vs best estimate)
#
# Relationship to other returns:
# - QMA: Booked GAAP/IFRS reserves (starting point)
# - RRA: Actuarial best estimate by class
# - ASR/ASB: Solvency II BEL + Risk Margin
# - AFR: Actuarial Function Report (governance narrative)
#
# Submitted annually, typically March following year-end
#
# Usage in Power BI:
# 1. Get Data > More > Other > Python script
# 2. Paste this entire file
# 3. Select tables from navigator
# 4. Load

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# Configuration
SYNDICATES = [33, 623, 1183, 1910, 2010, 2525, 2791, 2987, 4242, 5000]
REPORTING_YEAR = 2024
CURRENCY = 'GBP'

# Underwriting years for analysis
UW_YEARS = list(range(2015, 2025))

# Reserving classes
RESERVING_CLASSES = [
    ('RC01', 'Property Direct & Facultative'),
    ('RC02', 'Property Treaty'),
    ('RC03', 'Casualty - Short Tail'),
    ('RC04', 'Casualty - Long Tail'),
    ('RC05', 'Marine Hull'),
    ('RC06', 'Marine Cargo'),
    ('RC07', 'Marine Liability'),
    ('RC08', 'Energy'),
    ('RC09', 'Aviation'),
    ('RC10', 'Motor'),
    ('RC11', 'Accident & Health'),
    ('RC12', 'Credit & Surety'),
    ('RC13', 'Financial Lines'),
    ('RC14', 'Cyber'),
    ('RC15', 'Political Risk & Terror')
]

# Lloyd's Lines of Business for mapping
LLOYDS_LOBS = [
    'Property D&F', 'Property Treaty', 'Casualty', 'Marine',
    'Energy', 'Aviation', 'Motor', 'Accident & Health',
    'Credit & Surety', 'Financial Lines', 'Specialty'
]

# Cat codes for specific IBNR
CAT_CODES = [
    ('22E', 'Hurricane Ian 2022'),
    ('23E', 'Turkey/Syria Earthquake 2023'),
    ('24E', 'Various 2024 Events'),
    ('21E', 'European Floods 2021'),
    ('20E', 'COVID-19 2020'),
    ('Non-Cat', 'Non-Catastrophe Events')
]

# Opinion outcomes
OPINION_TYPES = [
    'Adequate',
    'Adequate with qualification',
    'Inadequate - strengthening required',
    'Unable to opine'
]

# =============================================================================
# SAO_001_Control - Submission metadata
# =============================================================================
def generate_sao_001_control():
    records = []
    for syn in SYNDICATES:
        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'Year_End_Date': datetime(REPORTING_YEAR, 12, 31),
            'Opinion_Date': datetime(REPORTING_YEAR + 1, 3, 15) + timedelta(days=np.random.randint(0, 10)),
            'Submission_Deadline': datetime(REPORTING_YEAR + 1, 3, 31),
            'ManagingAgent': f'MA{syn % 100:03d}',
            'ReportType': 'SAO',
            'ReturnVersion': '2024.1',
            'Status': 'Final',
            'Signing_Actuary': f'Actuary_{np.random.randint(100, 999)}',
            'Actuarial_Firm': np.random.choice(['Internal', 'PWC', 'EY', 'KPMG', 'Deloitte', 'WTW', 'Milliman']),
            'Peer_Reviewer': f'Reviewer_{np.random.randint(100, 999)}',
            'Currency': CURRENCY
        })
    return pd.DataFrame(records)

# =============================================================================
# SAO_010_Opinion_Summary - High-level opinion conclusions
# =============================================================================
def generate_sao_010_opinion_summary():
    records = []
    for syn in SYNDICATES:
        # Generate reserve figures
        gross_booked = np.random.uniform(200, 800)
        gross_be = gross_booked * np.random.uniform(0.92, 1.02)
        gross_margin = gross_booked - gross_be
        gross_margin_pct = (gross_margin / gross_be) * 100

        net_booked = gross_booked * np.random.uniform(0.55, 0.75)
        net_be = net_booked * np.random.uniform(0.93, 1.02)
        net_margin = net_booked - net_be
        net_margin_pct = (net_margin / net_be) * 100

        # Determine opinion based on margin
        if gross_margin_pct > 1 and net_margin_pct > 1:
            opinion_gross = 'Adequate'
            opinion_net = 'Adequate'
        elif gross_margin_pct > -2 and net_margin_pct > -2:
            opinion_gross = 'Adequate' if gross_margin_pct > 0 else 'Adequate with qualification'
            opinion_net = 'Adequate' if net_margin_pct > 0 else 'Adequate with qualification'
        else:
            opinion_gross = 'Inadequate - strengthening required' if gross_margin_pct < -2 else 'Adequate with qualification'
            opinion_net = 'Inadequate - strengthening required' if net_margin_pct < -2 else 'Adequate with qualification'

        # Confidence level
        confidence_50th = gross_be
        confidence_75th = gross_be * np.random.uniform(1.05, 1.12)
        confidence_90th = gross_be * np.random.uniform(1.12, 1.22)

        records.append({
            'Syndicate': syn,
            'ReportingYear': REPORTING_YEAR,
            'Year_End_Date': datetime(REPORTING_YEAR, 12, 31),
            # Gross reserves
            'Gross_Booked_Reserves_GBP_M': round(gross_booked, 2),
            'Gross_Best_Estimate_GBP_M': round(gross_be, 2),
            'Gross_Margin_GBP_M': round(gross_margin, 2),
            'Gross_Margin_Pct': round(gross_margin_pct, 1),
            'Gross_Opinion': opinion_gross,
            # Net reserves
            'Net_Booked_Reserves_GBP_M': round(net_booked, 2),
            'Net_Best_Estimate_GBP_M': round(net_be, 2),
            'Net_Margin_GBP_M': round(net_margin, 2),
            'Net_Margin_Pct': round(net_margin_pct, 1),
            'Net_Opinion': opinion_net,
            # Confidence levels
            'BE_50th_Percentile_GBP_M': round(confidence_50th, 2),
            'BE_75th_Percentile_GBP_M': round(confidence_75th, 2),
            'BE_90th_Percentile_GBP_M': round(confidence_90th, 2),
            'Booked_Percentile': np.random.randint(55, 75),
            # Summary
            'Overall_Assessment': 'Satisfactory' if opinion_gross == 'Adequate' and opinion_net == 'Adequate' else 'Attention Required',
            'Currency': CURRENCY
        })
    return pd.DataFrame(records)

# =============================================================================
# SAO_020_Class_Analysis - Class-by-class reserve analysis
# =============================================================================
def generate_sao_020_class_analysis():
    records = []
    for syn in SYNDICATES:
        total_gross_booked = np.random.uniform(200, 800)
        class_weights = np.random.dirichlet(np.ones(len(RESERVING_CLASSES)) * 0.5)

        for i, (rc_code, rc_name) in enumerate(RESERVING_CLASSES):
            weight = class_weights[i]
            if weight < 0.02:  # Skip very small classes
                continue

            # Class-level reserves
            gross_booked = total_gross_booked * weight
            gross_be = gross_booked * np.random.uniform(0.90, 1.05)
            gross_margin = gross_booked - gross_be

            net_booked = gross_booked * np.random.uniform(0.50, 0.80)
            net_be = net_booked * np.random.uniform(0.92, 1.05)
            net_margin = net_booked - net_be

            # Ultimate premium
            ultimate_premium = gross_booked * np.random.uniform(0.8, 1.5)

            # Loss ratios
            ielr = np.random.uniform(55, 80)  # Initial Expected Loss Ratio
            ulr = ielr + np.random.uniform(-5, 10)  # Ultimate Loss Ratio
            booked_lr = ulr * np.random.uniform(0.98, 1.05)

            # Development stage
            if 'Short' in rc_name or 'Property' in rc_name:
                paid_pct = np.random.uniform(60, 85)
            elif 'Long' in rc_name or 'Liability' in rc_name or 'Financial' in rc_name:
                paid_pct = np.random.uniform(25, 50)
            else:
                paid_pct = np.random.uniform(40, 70)

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Class_Code': rc_code,
                'Class_Name': rc_name,
                'Lloyds_LOB': LLOYDS_LOBS[i % len(LLOYDS_LOBS)],
                # Premium
                'Ultimate_Premium_GBP_M': round(ultimate_premium, 2),
                # Gross reserves
                'Gross_Booked_GBP_M': round(gross_booked, 2),
                'Gross_Best_Estimate_GBP_M': round(gross_be, 2),
                'Gross_Margin_GBP_M': round(gross_margin, 2),
                'Gross_Margin_Pct': round((gross_margin / gross_be) * 100, 1) if gross_be > 0 else 0,
                # Net reserves
                'Net_Booked_GBP_M': round(net_booked, 2),
                'Net_Best_Estimate_GBP_M': round(net_be, 2),
                'Net_Margin_GBP_M': round(net_margin, 2),
                'Net_Margin_Pct': round((net_margin / net_be) * 100, 1) if net_be > 0 else 0,
                # Loss ratios
                'IELR_Pct': round(ielr, 1),
                'ULR_Pct': round(ulr, 1),
                'Booked_LR_Pct': round(booked_lr, 1),
                # Development
                'Paid_Pct': round(paid_pct, 1),
                'Outstanding_Pct': round(100 - paid_pct - np.random.uniform(10, 30), 1),
                'IBNR_Pct': round(np.random.uniform(10, 30), 1),
                # Assessment
                'Reserve_Assessment': np.random.choice(['Adequate', 'Slightly High', 'Slightly Low', 'Uncertain'],
                                                       p=[0.6, 0.15, 0.15, 0.1]),
                'Currency': CURRENCY
            })

    return pd.DataFrame(records)

# =============================================================================
# SAO_030_UW_Year_Analysis - Analysis by underwriting year
# =============================================================================
def generate_sao_030_uw_year_analysis():
    records = []
    for syn in SYNDICATES:
        for rc_code, rc_name in RESERVING_CLASSES[:8]:  # Top 8 classes
            for uw_year in UW_YEARS:
                years_developed = REPORTING_YEAR - uw_year

                # Older years have less reserves
                if years_developed > 7:
                    decay = np.exp(-0.4 * (years_developed - 7))
                else:
                    decay = 1.0

                gross_be = np.random.uniform(5, 40) * decay
                if gross_be < 0.5:
                    continue

                net_be = gross_be * np.random.uniform(0.50, 0.80)
                gross_booked = gross_be * np.random.uniform(0.98, 1.08)
                net_booked = net_be * np.random.uniform(0.98, 1.08)

                # Paid progression
                if 'Property' in rc_name or 'Short' in rc_name:
                    expected_paid_pct = min(95, 40 + years_developed * 12)
                else:
                    expected_paid_pct = min(95, 15 + years_developed * 8)

                actual_paid_pct = expected_paid_pct * np.random.uniform(0.90, 1.10)

                # A vs E variance
                ave_variance = np.random.normal(0, 5)

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Class_Code': rc_code,
                    'Class_Name': rc_name,
                    'UW_Year': uw_year,
                    'Development_Year': years_developed,
                    'Gross_Best_Estimate_GBP_M': round(gross_be, 2),
                    'Gross_Booked_GBP_M': round(gross_booked, 2),
                    'Net_Best_Estimate_GBP_M': round(net_be, 2),
                    'Net_Booked_GBP_M': round(net_booked, 2),
                    'Expected_Paid_Pct': round(expected_paid_pct, 1),
                    'Actual_Paid_Pct': round(actual_paid_pct, 1),
                    'AvE_Variance_Pct': round(ave_variance, 1),
                    'Development_Status': 'Mature' if years_developed >= 5 else 'Developing',
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# SAO_040_Actual_vs_Expected - Actual vs Expected analysis (Form 100)
# =============================================================================
def generate_sao_040_actual_vs_expected():
    records = []
    for syn in SYNDICATES:
        for rc_code, rc_name in RESERVING_CLASSES:
            for uw_year_group in ['2023 & Prior', '2024', 'All Years']:
                is_reporting_year = 1 if uw_year_group == '2024' else 0

                # Premium and reserves
                if uw_year_group == '2023 & Prior':
                    ultimate_premium = np.random.uniform(50, 200)
                elif uw_year_group == '2024':
                    ultimate_premium = np.random.uniform(20, 100)
                else:
                    ultimate_premium = np.random.uniform(70, 300)

                # Loss ratios
                ielr = np.random.uniform(55, 75)
                ulr = ielr + np.random.uniform(-5, 10)

                # Reserves
                reserves_py = ultimate_premium * ulr / 100 * np.random.uniform(0.3, 0.7)
                reserves_cy = reserves_py * np.random.uniform(0.85, 1.15)

                # A vs E
                expected_emergence = reserves_py * np.random.uniform(0.20, 0.40)
                actual_emergence = expected_emergence * np.random.uniform(0.85, 1.20)
                ave_variance = actual_emergence - expected_emergence
                ave_pct = (ave_variance / expected_emergence) * 100 if expected_emergence > 0 else 0

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Class_Code': rc_code,
                    'Class_Name': rc_name,
                    'UW_Year_Group': uw_year_group,
                    'Reporting_Year_Flag': is_reporting_year,
                    'Ultimate_Premium_GBP_M': round(ultimate_premium, 2),
                    'IELR_Pct': round(ielr, 1),
                    'ULR_Pct': round(ulr, 1),
                    'Reserves_Prior_YE_GBP_M': round(reserves_py, 2),
                    'Reserves_Current_YE_GBP_M': round(reserves_cy, 2),
                    'Expected_Emergence_GBP_M': round(expected_emergence, 2),
                    'Actual_Emergence_GBP_M': round(actual_emergence, 2),
                    'AvE_Variance_GBP_M': round(ave_variance, 2),
                    'AvE_Variance_Pct': round(ave_pct, 1),
                    'Assessment': 'Within Expectations' if abs(ave_pct) < 10 else 'Outside Expectations',
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# SAO_050_Specific_IBNR - Specific IBNR for cats and large losses (Form 090)
# =============================================================================
def generate_sao_050_specific_ibnr():
    records = []
    for syn in SYNDICATES:
        for rc_code, rc_name in RESERVING_CLASSES[:10]:  # Top 10 classes
            for cat_code, cat_desc in CAT_CODES:
                # Not all classes affected by all cats
                if np.random.random() < 0.6:
                    continue

                # Number of losses
                num_losses = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.15, 0.07, 0.03])

                # IBNR amounts (log-normal distribution)
                gross_ibnr = np.random.lognormal(mean=np.log(10), sigma=0.8)
                gross_ibnr = max(1, round(gross_ibnr, 0))

                # Net as percentage of gross
                net_pct = np.random.uniform(0.55, 0.90)
                net_ibnr = round(gross_ibnr * net_pct, 0)

                # UW year affected
                if cat_code == '24E':
                    uw_year = 2024
                elif cat_code == '23E':
                    uw_year = 2023
                elif cat_code == '22E':
                    uw_year = 2022
                elif cat_code == '21E':
                    uw_year = 2021
                elif cat_code == '20E':
                    uw_year = 2020
                else:
                    uw_year = np.random.choice([2022, 2023, 2024])

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Class_Code': rc_code,
                    'Class_Name': rc_name,
                    'Cat_Code': cat_code,
                    'Cat_Description': cat_desc,
                    'UW_Year': uw_year,
                    'Number_of_Losses': int(num_losses),
                    'Gross_IBNR_GBP_K': int(gross_ibnr),
                    'Net_IBNR_GBP_K': int(net_ibnr),
                    'Net_Pct_of_Gross': round(net_pct * 100, 1),
                    'Uncertainty': np.random.choice(['Low', 'Medium', 'High'], p=[0.3, 0.5, 0.2]),
                    'Comment': f'IBNR for {cat_desc} based on exposure analysis and loss development',
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# SAO_060_Assumptions - Key actuarial assumptions
# =============================================================================
def generate_sao_060_assumptions():
    records = []

    assumption_types = [
        ('LOSS_DEV', 'Loss Development Factors', 'Chain ladder development factors by class'),
        ('TAIL', 'Tail Factors', 'Development beyond observed triangle'),
        ('IELR', 'Initial Expected Loss Ratio', 'A priori loss ratio for recent years'),
        ('TREND', 'Claims Inflation', 'Annual inflation assumption'),
        ('FREQ', 'Claims Frequency', 'Expected claim count trends'),
        ('SEV', 'Claims Severity', 'Average claim size trends'),
        ('RI_COLL', 'RI Collectability', 'Bad debt provision on RI recoverables'),
        ('ULAE', 'ULAE Loading', 'Unallocated loss adjustment expense'),
        ('DISCOUNT', 'Discount Rate', 'Rate used for discounting (SII only)'),
        ('ENID', 'ENID Allowance', 'Events Not In Data provision')
    ]

    for syn in SYNDICATES:
        for rc_code, rc_name in RESERVING_CLASSES[:8]:
            for assum_code, assum_name, assum_desc in assumption_types:
                # Generate assumption values based on type
                if assum_code == 'LOSS_DEV':
                    value = np.random.uniform(1.05, 1.25)
                    unit = 'Factor'
                elif assum_code == 'TAIL':
                    value = np.random.uniform(1.01, 1.10)
                    unit = 'Factor'
                elif assum_code == 'IELR':
                    value = np.random.uniform(55, 80)
                    unit = 'Pct'
                elif assum_code == 'TREND':
                    value = np.random.uniform(2, 6)
                    unit = 'Pct'
                elif assum_code == 'RI_COLL':
                    value = np.random.uniform(1, 5)
                    unit = 'Pct'
                elif assum_code == 'ULAE':
                    value = np.random.uniform(2, 8)
                    unit = 'Pct'
                elif assum_code == 'DISCOUNT':
                    value = np.random.uniform(2, 4)
                    unit = 'Pct'
                elif assum_code == 'ENID':
                    value = np.random.uniform(0.5, 3)
                    unit = 'Pct'
                else:
                    value = np.random.uniform(0, 5)
                    unit = 'Pct'

                # Prior year value for comparison
                py_value = value * np.random.uniform(0.92, 1.08)
                change = value - py_value

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Class_Code': rc_code,
                    'Class_Name': rc_name,
                    'Assumption_Code': assum_code,
                    'Assumption_Name': assum_name,
                    'Assumption_Description': assum_desc,
                    'Current_Value': round(value, 3),
                    'Prior_Year_Value': round(py_value, 3),
                    'Change': round(change, 3),
                    'Unit': unit,
                    'Source': np.random.choice(['Historical Experience', 'Market Data', 'Management View', 'Model Output']),
                    'Sensitivity_Impact_Pct': round(np.random.uniform(0.5, 5), 1),
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# SAO_070_Movement_Analysis - Year-on-year reserve movements
# =============================================================================
def generate_sao_070_movement_analysis():
    records = []

    movement_types = [
        ('OPEN_BE', 'Opening Best Estimate'),
        ('PAID', 'Claims Paid'),
        ('REVISIONS', 'Reserve Revisions - Prior Years'),
        ('NEW_BE', 'New Business Best Estimate'),
        ('FX', 'Foreign Exchange Movement'),
        ('OTHER', 'Other Movements'),
        ('CLOSE_BE', 'Closing Best Estimate')
    ]

    for syn in SYNDICATES:
        # Overall movement
        opening_be = np.random.uniform(200, 700)

        for basis in ['Gross', 'Net']:
            scale = 1.0 if basis == 'Gross' else np.random.uniform(0.55, 0.75)

            paid = opening_be * scale * np.random.uniform(0.25, 0.40)
            revisions = opening_be * scale * np.random.uniform(-0.08, 0.08)
            new_be = opening_be * scale * np.random.uniform(0.20, 0.35)
            fx = opening_be * scale * np.random.uniform(-0.03, 0.03)
            other = opening_be * scale * np.random.uniform(-0.02, 0.02)
            closing_be = opening_be * scale - paid + revisions + new_be + fx + other

            values = [opening_be * scale, -paid, revisions, new_be, fx, other, closing_be]

            for (mvt_code, mvt_name), value in zip(movement_types, values):
                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Basis': basis,
                    'Movement_Code': mvt_code,
                    'Movement_Name': mvt_name,
                    'Amount_GBP_M': round(value, 2),
                    'Pct_of_Opening': round((value / (opening_be * scale)) * 100, 1) if opening_be * scale > 0 else 0,
                    'Currency': CURRENCY
                })

    return pd.DataFrame(records)

# =============================================================================
# SAO_080_Sensitivity - Sensitivity analysis
# =============================================================================
def generate_sao_080_sensitivity():
    records = []

    sensitivities = [
        ('LDF_UP_5', 'Loss Development +5%', 5),
        ('LDF_DN_5', 'Loss Development -5%', -5),
        ('TAIL_UP_2', 'Tail Factor +2%', 2),
        ('TAIL_DN_2', 'Tail Factor -2%', -2),
        ('IELR_UP_5', 'IELR +5 pts', 5),
        ('IELR_DN_5', 'IELR -5 pts', -5),
        ('TREND_UP_1', 'Inflation +1%', 1),
        ('TREND_DN_1', 'Inflation -1%', -1),
        ('RI_COLL_UP_2', 'RI Bad Debt +2%', 2)
    ]

    for syn in SYNDICATES:
        base_be = np.random.uniform(200, 600)

        for sens_code, sens_name, factor in sensitivities:
            # Impact varies by sensitivity type
            if 'LDF' in sens_code:
                impact_pct = factor * np.random.uniform(0.8, 1.2)
            elif 'TAIL' in sens_code:
                impact_pct = factor * np.random.uniform(0.3, 0.6)
            elif 'IELR' in sens_code:
                impact_pct = factor * np.random.uniform(0.6, 1.0)
            elif 'TREND' in sens_code:
                impact_pct = factor * np.random.uniform(0.4, 0.8)
            else:
                impact_pct = factor * np.random.uniform(0.2, 0.5)

            impact_amount = base_be * (impact_pct / 100)

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Sensitivity_Code': sens_code,
                'Sensitivity_Name': sens_name,
                'Factor_Change': factor,
                'Base_BE_GBP_M': round(base_be, 2),
                'Impact_GBP_M': round(impact_amount, 2),
                'Impact_Pct': round(impact_pct, 2),
                'Stressed_BE_GBP_M': round(base_be + impact_amount, 2),
                'Currency': CURRENCY
            })

    return pd.DataFrame(records)

# =============================================================================
# Generate all tables
# =============================================================================

# Control
SAO_001_Control = generate_sao_001_control()

# Opinion and analysis
SAO_010_Opinion_Summary = generate_sao_010_opinion_summary()
SAO_020_Class_Analysis = generate_sao_020_class_analysis()
SAO_030_UW_Year_Analysis = generate_sao_030_uw_year_analysis()
SAO_040_Actual_vs_Expected = generate_sao_040_actual_vs_expected()
SAO_050_Specific_IBNR = generate_sao_050_specific_ibnr()
SAO_060_Assumptions = generate_sao_060_assumptions()
SAO_070_Movement_Analysis = generate_sao_070_movement_analysis()
SAO_080_Sensitivity = generate_sao_080_sensitivity()

# Summary statistics
print("=" * 70)
print("SAO - Statement of Actuarial Opinion Data Generator")
print("=" * 70)
print(f"SAO_001_Control: {len(SAO_001_Control)} rows")
print(f"SAO_010_Opinion_Summary: {len(SAO_010_Opinion_Summary)} rows")
print(f"SAO_020_Class_Analysis: {len(SAO_020_Class_Analysis)} rows")
print(f"SAO_030_UW_Year_Analysis: {len(SAO_030_UW_Year_Analysis)} rows")
print(f"SAO_040_Actual_vs_Expected: {len(SAO_040_Actual_vs_Expected)} rows")
print(f"SAO_050_Specific_IBNR: {len(SAO_050_Specific_IBNR)} rows")
print(f"SAO_060_Assumptions: {len(SAO_060_Assumptions)} rows")
print(f"SAO_070_Movement_Analysis: {len(SAO_070_Movement_Analysis)} rows")
print(f"SAO_080_Sensitivity: {len(SAO_080_Sensitivity)} rows")
print("=" * 70)
print("SAO data generated successfully!")
