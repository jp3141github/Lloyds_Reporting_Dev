# Quarterly Monitoring Return Part B (QMB) - Power BI Data Generator
# Lloyd's Quarterly Business and Claims Analysis
#
# DISTINCT FROM QMA: QMB covers business/claims detail not in Part A:
# - Claims triangles (quarterly development)
# - Large loss register
# - Business segment analysis
# - Prior year development
# - Reinsurance performance
# - Key risk indicators
#
# QMA = Financial statements (Balance Sheet, P&L, Cash Flow)
# QMB = Business analysis (Claims detail, Large losses, Segments)
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
QUARTERS = ['Q1', 'Q2', 'Q3', 'Q4']
YEARS_OF_ACCOUNT = list(range(2018, 2025))

# Lloyd's Lines of Business
LINES_OF_BUSINESS = [
    ('PR', 'Property Direct'),
    ('CA', 'Casualty Direct'),
    ('MA', 'Marine Direct'),
    ('AV', 'Aviation Direct'),
    ('EN', 'Energy Direct'),
    ('PA', 'Accident & Health'),
    ('PR_RI', 'Property Reinsurance'),
    ('CA_RI', 'Casualty Reinsurance'),
    ('SP', 'Specialty')
]

# Geographic Segments
SEGMENTS = [
    ('US', 'United States'),
    ('UK', 'United Kingdom'),
    ('EU', 'European Union'),
    ('APAC', 'Asia Pacific'),
    ('ROW', 'Rest of World')
]

# =============================================================================
# QMB_001_Control - Submission metadata
# =============================================================================
def generate_qmb_001_control():
    records = []
    quarter_ends = {
        'Q1': datetime(2024, 3, 31),
        'Q2': datetime(2024, 6, 30),
        'Q3': datetime(2024, 9, 30),
        'Q4': datetime(2024, 12, 31)
    }

    for syn in SYNDICATES:
        for quarter in QUARTERS:
            quarter_end = quarter_ends[quarter]
            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Quarter': quarter,
                'QuarterEnd': quarter_end,
                'SubmissionDeadline': quarter_end + timedelta(days=35),
                'SubmissionDate': quarter_end + timedelta(days=np.random.randint(25, 34)),
                'ManagingAgent': f'MA{syn % 100:03d}',
                'ReportType': 'QMB',
                'Status': 'Final',
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# QMB_010_Claims_Triangle - Quarterly claims development triangle
# =============================================================================
def generate_qmb_010_claims_triangle():
    """Claims development triangle by underwriting year - key QMB content"""
    records = []

    for syn in SYNDICATES:
        for quarter in QUARTERS:
            for uw_year in YEARS_OF_ACCOUNT:
                # Only include years that are developed
                max_dev = REPORTING_YEAR - uw_year + 1
                if max_dev < 1:
                    continue

                # Base ultimate for this UW year
                base_ultimate = np.random.uniform(50, 200)

                for dev_year in range(1, min(max_dev + 1, 8)):  # Max 7 development years
                    # Development pattern (higher early, lower later)
                    if dev_year == 1:
                        cumulative_pct = np.random.uniform(0.30, 0.50)
                    elif dev_year == 2:
                        cumulative_pct = np.random.uniform(0.55, 0.75)
                    elif dev_year == 3:
                        cumulative_pct = np.random.uniform(0.75, 0.88)
                    elif dev_year == 4:
                        cumulative_pct = np.random.uniform(0.85, 0.94)
                    elif dev_year == 5:
                        cumulative_pct = np.random.uniform(0.92, 0.97)
                    else:
                        cumulative_pct = np.random.uniform(0.96, 0.99)

                    cumulative_paid = base_ultimate * cumulative_pct
                    outstanding = base_ultimate * (1 - cumulative_pct) * np.random.uniform(0.8, 1.2)
                    ibnr = base_ultimate - cumulative_paid - outstanding
                    ibnr = max(ibnr, 0)
                    incurred = cumulative_paid + outstanding + ibnr

                    records.append({
                        'Syndicate': syn,
                        'ReportingYear': REPORTING_YEAR,
                        'Quarter': quarter,
                        'UnderwritingYear': uw_year,
                        'DevelopmentYear': dev_year,
                        'CumulativePaid_GBP_M': round(cumulative_paid, 2),
                        'Outstanding_GBP_M': round(outstanding, 2),
                        'IBNR_GBP_M': round(ibnr, 2),
                        'Incurred_GBP_M': round(incurred, 2),
                        'Ultimate_GBP_M': round(base_ultimate, 2),
                        'DevelopmentFactor': round(cumulative_pct, 4),
                        'Currency': 'GBP'
                    })
    return pd.DataFrame(records)

# =============================================================================
# QMB_020_Large_Losses - Large loss register
# =============================================================================
def generate_qmb_020_large_losses():
    """Register of large/significant losses - key QMB content"""
    records = []
    large_loss_id = 1

    perils = ['Fire', 'Storm', 'Flood', 'Earthquake', 'Liability', 'Professional Indemnity',
              'Cyber', 'Aviation Incident', 'Marine Hull', 'Energy', 'Product Recall']

    for syn in SYNDICATES:
        num_large_losses = np.random.randint(5, 20)

        for _ in range(num_large_losses):
            quarter = np.random.choice(QUARTERS)
            lob_code, lob_name = LINES_OF_BUSINESS[np.random.randint(0, len(LINES_OF_BUSINESS))]
            uw_year = np.random.choice(YEARS_OF_ACCOUNT[-4:])  # Recent years

            gross_loss = np.random.uniform(2, 50)  # GBP millions - large loss threshold
            ri_recovery = gross_loss * np.random.uniform(0.30, 0.70)
            net_loss = gross_loss - ri_recovery

            paid_pct = np.random.uniform(0.20, 0.80)
            paid = net_loss * paid_pct
            outstanding = net_loss - paid

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Quarter': quarter,
                'LargeLossID': f'LL{syn}_{large_loss_id:04d}',
                'UnderwritingYear': uw_year,
                'LOB_Code': lob_code,
                'LOB_Name': lob_name,
                'Peril': np.random.choice(perils),
                'LossDate': datetime(uw_year, np.random.randint(1, 13), np.random.randint(1, 28)),
                'NotificationDate': datetime(uw_year, np.random.randint(1, 13), np.random.randint(1, 28)),
                'LossDescription': f'Large loss event - {np.random.choice(perils)}',
                'Territory': np.random.choice(['US', 'UK', 'EU', 'APAC', 'ROW']),
                'GrossLoss_GBP_M': round(gross_loss, 2),
                'RI_Recovery_GBP_M': round(ri_recovery, 2),
                'NetLoss_GBP_M': round(net_loss, 2),
                'Paid_GBP_M': round(paid, 2),
                'Outstanding_GBP_M': round(outstanding, 2),
                'Status': np.random.choice(['Open', 'Closed', 'Re-opened'], p=[0.6, 0.3, 0.1]),
                'CatEvent': np.random.choice(['Y', 'N'], p=[0.2, 0.8]),
                'Currency': 'GBP'
            })
            large_loss_id += 1

    return pd.DataFrame(records)

# =============================================================================
# QMB_030_Segment_Analysis - Business segment performance
# =============================================================================
def generate_qmb_030_segment_analysis():
    """Quarterly performance by business segment"""
    records = []

    for syn in SYNDICATES:
        total_gwp = np.random.uniform(150, 500)
        segment_weights = np.random.dirichlet(np.ones(len(SEGMENTS)))

        for quarter in QUARTERS:
            q_factor = np.random.uniform(0.22, 0.28)  # Quarterly portion

            for i, (seg_code, seg_name) in enumerate(SEGMENTS):
                seg_gwp = total_gwp * segment_weights[i] * q_factor
                seg_nep = seg_gwp * np.random.uniform(0.85, 0.95)

                # Segment-specific loss ratios
                loss_ratio = np.random.uniform(0.45, 0.80)
                expense_ratio = np.random.uniform(0.28, 0.40)
                combined_ratio = loss_ratio + expense_ratio

                claims = seg_nep * loss_ratio
                expenses = seg_nep * expense_ratio
                technical_result = seg_nep - claims - expenses

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'SegmentCode': seg_code,
                    'SegmentName': seg_name,
                    'GWP_GBP_M': round(seg_gwp, 2),
                    'NWP_GBP_M': round(seg_gwp * 0.90, 2),
                    'NEP_GBP_M': round(seg_nep, 2),
                    'ClaimsIncurred_GBP_M': round(claims, 2),
                    'Expenses_GBP_M': round(expenses, 2),
                    'TechnicalResult_GBP_M': round(technical_result, 2),
                    'LossRatio_Pct': round(loss_ratio * 100, 1),
                    'ExpenseRatio_Pct': round(expense_ratio * 100, 1),
                    'CombinedRatio_Pct': round(combined_ratio * 100, 1),
                    'PolicyCount': np.random.randint(100, 2000),
                    'AvgPremium_GBP': round(seg_gwp * 1000000 / np.random.randint(100, 2000), 0),
                    'Currency': 'GBP'
                })
    return pd.DataFrame(records)

# =============================================================================
# QMB_040_Prior_Year_Development - Prior year reserve development
# =============================================================================
def generate_qmb_040_prior_year_development():
    """Quarterly prior year reserve development - favorable/adverse"""
    records = []

    for syn in SYNDICATES:
        for quarter in QUARTERS:
            for uw_year in YEARS_OF_ACCOUNT[:-1]:  # Exclude current year
                for lob_code, lob_name in LINES_OF_BUSINESS:
                    # Skip some combinations for realism
                    if np.random.random() < 0.3:
                        continue

                    opening_reserve = np.random.uniform(5, 50)
                    claims_paid = opening_reserve * np.random.uniform(0.10, 0.30)

                    # Development can be favorable (negative) or adverse (positive)
                    development_pct = np.random.uniform(-0.15, 0.10)  # Slight favorable bias
                    development = opening_reserve * development_pct

                    closing_reserve = opening_reserve - claims_paid + development

                    records.append({
                        'Syndicate': syn,
                        'ReportingYear': REPORTING_YEAR,
                        'Quarter': quarter,
                        'UnderwritingYear': uw_year,
                        'LOB_Code': lob_code,
                        'LOB_Name': lob_name,
                        'OpeningReserve_GBP_M': round(opening_reserve, 2),
                        'ClaimsPaid_GBP_M': round(claims_paid, 2),
                        'Development_GBP_M': round(development, 2),
                        'DevelopmentType': 'Favorable' if development < 0 else 'Adverse',
                        'Development_Pct': round(development_pct * 100, 1),
                        'ClosingReserve_GBP_M': round(closing_reserve, 2),
                        'Currency': 'GBP'
                    })
    return pd.DataFrame(records)

# =============================================================================
# QMB_050_Reinsurance_Performance - RI program performance
# =============================================================================
def generate_qmb_050_reinsurance_performance():
    """Quarterly reinsurance program performance analysis"""
    records = []
    ri_programs = [
        ('QS', 'Quota Share'),
        ('XOL', 'Excess of Loss'),
        ('CAT', 'Catastrophe XOL'),
        ('FAC', 'Facultative'),
        ('AGG', 'Aggregate Stop Loss')
    ]

    for syn in SYNDICATES:
        for quarter in QUARTERS:
            for ri_code, ri_name in ri_programs:
                premium_ceded = np.random.uniform(2, 30)
                claims_recovered = premium_ceded * np.random.uniform(0.3, 1.5)
                commission_received = premium_ceded * np.random.uniform(0.15, 0.30) if ri_code in ['QS'] else 0

                net_cost = premium_ceded - claims_recovered - commission_received
                loss_ratio = claims_recovered / premium_ceded if premium_ceded > 0 else 0

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'RI_Program_Code': ri_code,
                    'RI_Program_Name': ri_name,
                    'PremiumCeded_GBP_M': round(premium_ceded, 2),
                    'ClaimsRecovered_GBP_M': round(claims_recovered, 2),
                    'CommissionReceived_GBP_M': round(commission_received, 2),
                    'NetCost_GBP_M': round(net_cost, 2),
                    'LossRatio_Pct': round(loss_ratio * 100, 1),
                    'Attachments': np.random.randint(0, 10),
                    'Exhaustions': np.random.randint(0, 3),
                    'TopReinsurer': np.random.choice(['Munich Re', 'Swiss Re', 'Hannover Re', 'SCOR', 'Lloyd\'s']),
                    'AvgCounterpartyRating': np.random.choice(['AAA', 'AA', 'A', 'BBB']),
                    'Currency': 'GBP'
                })
    return pd.DataFrame(records)

# =============================================================================
# QMB_060_Risk_Indicators - Key risk indicators
# =============================================================================
def generate_qmb_060_risk_indicators():
    """Quarterly key risk indicators (KRIs)"""
    records = []
    kris = [
        ('LOSS_RATIO', 'Loss Ratio', '%', 50, 75, 85),
        ('EXPENSE_RATIO', 'Expense Ratio', '%', 25, 35, 45),
        ('COMBINED_RATIO', 'Combined Ratio', '%', 85, 100, 110),
        ('LARGE_LOSS_COUNT', 'Large Loss Count', '#', 0, 5, 15),
        ('RESERVE_ADEQUACY', 'Reserve Adequacy Ratio', '%', 95, 100, 105),
        ('PREMIUM_GROWTH', 'Premium Growth Rate', '%', -5, 10, 30),
        ('RATE_CHANGE', 'Average Rate Change', '%', -5, 5, 15),
        ('RETENTION_RATE', 'Policy Retention Rate', '%', 70, 85, 95),
        ('CLAIMS_FREQUENCY', 'Claims Frequency', '%', 5, 15, 30),
        ('AVG_CLAIM_SIZE', 'Average Claim Size Growth', '%', -10, 5, 20)
    ]

    for syn in SYNDICATES:
        for quarter in QUARTERS:
            for kri_code, kri_name, unit, green_max, amber_max, red_threshold in kris:
                # Generate value with appropriate distribution
                if unit == '%':
                    value = np.random.uniform(green_max * 0.7, red_threshold * 1.1)
                else:
                    value = np.random.randint(0, int(red_threshold * 1.5))

                # Determine RAG status
                if value <= green_max:
                    rag_status = 'Green'
                elif value <= amber_max:
                    rag_status = 'Amber'
                else:
                    rag_status = 'Red'

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'KRI_Code': kri_code,
                    'KRI_Name': kri_name,
                    'Unit': unit,
                    'Value': round(value, 1),
                    'GreenThreshold': green_max,
                    'AmberThreshold': amber_max,
                    'RedThreshold': red_threshold,
                    'RAG_Status': rag_status,
                    'Trend': np.random.choice(['Improving', 'Stable', 'Deteriorating'], p=[0.3, 0.5, 0.2])
                })
    return pd.DataFrame(records)

# =============================================================================
# QMB_070_Cat_Exposure - Catastrophe exposure summary
# =============================================================================
def generate_qmb_070_cat_exposure():
    """Quarterly catastrophe exposure summary"""
    records = []
    cat_perils = [
        ('NA_HU', 'North Atlantic Hurricane'),
        ('EU_WS', 'European Windstorm'),
        ('US_EQ', 'US Earthquake'),
        ('JP_EQ', 'Japan Earthquake'),
        ('JP_TY', 'Japan Typhoon'),
        ('FL', 'Flood'),
        ('TR', 'Terrorism'),
        ('CY', 'Cyber')
    ]

    for syn in SYNDICATES:
        base_exposure = np.random.uniform(200, 800)

        for quarter in QUARTERS:
            for peril_code, peril_name in cat_perils:
                weight = np.random.uniform(0.05, 0.25)
                gross_pml = base_exposure * weight
                ri_limit = gross_pml * np.random.uniform(0.50, 0.80)
                net_pml = gross_pml - ri_limit

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'PerilCode': peril_code,
                    'PerilName': peril_name,
                    'GrossPML_100yr_GBP_M': round(gross_pml * 0.7, 2),
                    'GrossPML_250yr_GBP_M': round(gross_pml, 2),
                    'RI_Limit_GBP_M': round(ri_limit, 2),
                    'NetPML_100yr_GBP_M': round(net_pml * 0.7, 2),
                    'NetPML_250yr_GBP_M': round(net_pml, 2),
                    'AAL_GBP_M': round(gross_pml * np.random.uniform(0.02, 0.08), 2),
                    'Pct_of_Capacity': round((gross_pml / base_exposure) * 100, 1),
                    'Currency': 'GBP'
                })
    return pd.DataFrame(records)

# =============================================================================
# Generate all tables
# =============================================================================

# Control
QMB_001_Control = generate_qmb_001_control()

# Claims Analysis
QMB_010_Claims_Triangle = generate_qmb_010_claims_triangle()
QMB_020_Large_Losses = generate_qmb_020_large_losses()

# Business Analysis
QMB_030_Segment_Analysis = generate_qmb_030_segment_analysis()
QMB_040_Prior_Year_Development = generate_qmb_040_prior_year_development()

# Reinsurance
QMB_050_Reinsurance_Performance = generate_qmb_050_reinsurance_performance()

# Risk Management
QMB_060_Risk_Indicators = generate_qmb_060_risk_indicators()
QMB_070_Cat_Exposure = generate_qmb_070_cat_exposure()

# Summary statistics
print(f"QMB_001_Control: {len(QMB_001_Control)} rows")
print(f"QMB_010_Claims_Triangle: {len(QMB_010_Claims_Triangle)} rows")
print(f"QMB_020_Large_Losses: {len(QMB_020_Large_Losses)} rows")
print(f"QMB_030_Segment_Analysis: {len(QMB_030_Segment_Analysis)} rows")
print(f"QMB_040_Prior_Year_Development: {len(QMB_040_Prior_Year_Development)} rows")
print(f"QMB_050_Reinsurance_Performance: {len(QMB_050_Reinsurance_Performance)} rows")
print(f"QMB_060_Risk_Indicators: {len(QMB_060_Risk_Indicators)} rows")
print(f"QMB_070_Cat_Exposure: {len(QMB_070_Cat_Exposure)} rows")
