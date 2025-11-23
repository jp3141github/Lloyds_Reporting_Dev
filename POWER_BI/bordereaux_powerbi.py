# Premium & Claims Bordereaux - Power BI Data Generator
# Delegated Authority Transaction-Level Reporting
# Following Lloyd's Coverholder Reporting Standards (CRS) v5.2
#
# Generates 5 tables covering:
# - Premium bordereaux with 500+ transaction records
# - Claims bordereaux with 300+ claim records
# - Risk bordereaux for exposure analysis
# - Coverholder summary statistics
# - Contract performance metrics
#
# Key Lloyd's Identifiers:
# - UMR (Unique Market Reference): B2024A1234567
# - OSN (Original Signing Number): OSN12345678
# - UCR (Unique Claim Reference): B2024A1234567/2024/001
#
# Usage in Power BI:
# 1. Get Data > More > Other > Python script
# 2. Paste this entire file
# 3. Select tables from navigator
# 4. Load

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
SYNDICATES = [33, 623, 1183, 1910, 2010, 2525, 2791, 2987, 4242, 5000]
REPORTING_YEAR = 2024
NUM_PREMIUM_RECORDS = 500
NUM_CLAIMS_RECORDS = 300

# Coverholders (sample TPAs and Coverholders)
COVERHOLDERS = [
    ('CH001', 'ABC Underwriting Services Ltd', 'UK'),
    ('CH002', 'Global Risk Partners Inc', 'US'),
    ('CH003', 'Pacific Cover Solutions', 'AU'),
    ('CH004', 'European Risk Services', 'DE'),
    ('CH005', 'Atlantic Specialty MGA', 'US'),
    ('CH006', 'Northern Marine Cover', 'NO'),
    ('CH007', 'Asia Pacific Binding Authority', 'SG'),
    ('CH008', 'Canadian Risk Management', 'CA'),
    ('CH009', 'Mediterranean Underwriters', 'ES'),
    ('CH010', 'South American Cover Services', 'BR')
]

# Brokers
BROKERS = ['AON', 'MARSH', 'WTW', 'GALLAGHER', 'LOCKTON', 'JLT', 'HOWDEN', 'MILLER', 'UIB', 'TYSERS']

# Lines of Business
LINES_OF_BUSINESS = [
    ('PR', 'Property', 0.25),
    ('CA', 'Casualty', 0.20),
    ('MA', 'Marine', 0.10),
    ('AV', 'Aviation', 0.05),
    ('EN', 'Energy', 0.08),
    ('PA', 'Accident & Health', 0.12),
    ('CR', 'Credit', 0.05),
    ('MO', 'Motor', 0.08),
    ('SP', 'Specialty', 0.07)
]

# Countries
COUNTRIES = [
    ('US', 'United States'), ('GB', 'United Kingdom'), ('DE', 'Germany'),
    ('FR', 'France'), ('AU', 'Australia'), ('CA', 'Canada'),
    ('JP', 'Japan'), ('SG', 'Singapore'), ('NL', 'Netherlands'),
    ('CH', 'Switzerland'), ('ES', 'Spain'), ('IT', 'Italy')
]

# Currencies
CURRENCIES = ['GBP', 'USD', 'EUR', 'AUD', 'CAD', 'CHF', 'JPY']
FX_RATES = {'GBP': 1.0, 'USD': 0.79, 'EUR': 0.86, 'AUD': 0.52, 'CAD': 0.59, 'CHF': 0.90, 'JPY': 0.0053}

# Perils
PERILS = [
    'Fire', 'Flood', 'Storm', 'Earthquake', 'Theft', 'Business Interruption',
    'Liability', 'Professional Indemnity', 'Product Liability', 'Employers Liability',
    'Marine Cargo', 'Marine Hull', 'Aviation Hull', 'Aviation Liability',
    'Motor Third Party', 'Motor Comprehensive', 'Accident', 'Health'
]

# Claim Status
CLAIM_STATUS = ['Open', 'Closed', 'Re-opened', 'IBNR', 'Pending']

# =============================================================================
# Helper Functions
# =============================================================================
def generate_umr(year):
    """Generate Lloyd's Unique Market Reference"""
    broker_prefix = random.choice(['B', 'W', 'A', 'M', 'G', 'L'])
    alpha = random.choice(string.ascii_uppercase)
    number = f"{random.randint(1000000, 9999999)}"
    return f"{broker_prefix}{year}{alpha}{number}"

def generate_osn():
    """Generate Original Signing Number"""
    return f"OSN{random.randint(10000000, 99999999)}"

def generate_ucr(umr, year, seq):
    """Generate Unique Claim Reference"""
    return f"{umr}/{year}/{seq:03d}"

def generate_policy_ref():
    """Generate Policy Reference"""
    return f"POL{random.randint(100000, 999999)}"

def generate_certificate_ref():
    """Generate Certificate Reference"""
    return f"CERT{random.randint(10000, 99999)}"

# =============================================================================
# Premium_Bordereaux - Policy-level premium transactions
# =============================================================================
def generate_premium_bordereaux():
    records = []

    for i in range(NUM_PREMIUM_RECORDS):
        syn = random.choice(SYNDICATES)
        ch_code, ch_name, ch_country = random.choice(COVERHOLDERS)
        lob_code, lob_name, _ = random.choices(LINES_OF_BUSINESS, weights=[x[2] for x in LINES_OF_BUSINESS])[0]
        country_code, country_name = random.choice(COUNTRIES)
        currency = random.choice(CURRENCIES)

        # Dates
        inception_date = datetime(REPORTING_YEAR, 1, 1) + timedelta(days=random.randint(0, 364))
        expiry_date = inception_date + timedelta(days=random.choice([30, 90, 180, 365]))
        bordereaux_date = inception_date + timedelta(days=random.randint(15, 45))

        # Lloyd's identifiers
        umr = generate_umr(REPORTING_YEAR)
        osn = generate_osn()
        policy_ref = generate_policy_ref()
        cert_ref = generate_certificate_ref()

        # Premium amounts
        gross_premium = round(np.random.lognormal(mean=8, sigma=1.5), 2)  # Range approx 500 to 500,000
        gross_premium = min(max(gross_premium, 500), 2000000)  # Cap at reasonable range

        # Lloyd's participation
        lloyds_pct = random.choice([0.10, 0.15, 0.20, 0.25, 0.30, 0.50, 1.00])
        lloyds_premium = round(gross_premium * lloyds_pct, 2)

        # Deductions
        brokerage_pct = random.uniform(0.10, 0.20)
        commission_pct = random.uniform(0.05, 0.15)
        tax_pct = random.uniform(0, 0.12)

        brokerage = round(gross_premium * brokerage_pct, 2)
        commission = round(gross_premium * commission_pct, 2)
        tax = round(gross_premium * tax_pct, 2)

        net_premium = round(gross_premium - brokerage - commission, 2)
        lloyds_net_premium = round(net_premium * lloyds_pct, 2)

        # Convert to GBP
        fx_rate = FX_RATES.get(currency, 1.0)
        gross_premium_gbp = round(gross_premium * fx_rate, 2)
        lloyds_premium_gbp = round(lloyds_premium * fx_rate, 2)

        records.append({
            'RecordID': i + 1,
            'Syndicate': syn,
            'CoverholderCode': ch_code,
            'CoverholderName': ch_name,
            'BrokerName': random.choice(BROKERS),
            'UMR': umr,
            'OSN': osn,
            'PolicyReference': policy_ref,
            'CertificateReference': cert_ref,
            'InceptionDate': inception_date,
            'ExpiryDate': expiry_date,
            'BordereauxDate': bordereaux_date,
            'LOB_Code': lob_code,
            'LOB_Name': lob_name,
            'Peril': random.choice(PERILS),
            'RiskCountryCode': country_code,
            'RiskCountryName': country_name,
            'InsuredName': f'Insured_{i+1:05d}',
            'SumInsured': round(gross_premium * random.uniform(50, 200), 0),
            'Deductible': round(gross_premium * random.uniform(0.01, 0.05), 0),
            'Currency': currency,
            'FX_Rate_to_GBP': fx_rate,
            'GrossPremium': gross_premium,
            'Brokerage': brokerage,
            'BrokeragePct': round(brokerage_pct * 100, 2),
            'Commission': commission,
            'CommissionPct': round(commission_pct * 100, 2),
            'Tax': tax,
            'TaxPct': round(tax_pct * 100, 2),
            'NetPremium': net_premium,
            'LloydsPct': round(lloyds_pct * 100, 1),
            'LloydsGrossPremium': lloyds_premium,
            'LloydsNetPremium': lloyds_net_premium,
            'GrossPremium_GBP': gross_premium_gbp,
            'LloydsPremium_GBP': lloyds_premium_gbp,
            'TransactionType': random.choice(['New Business', 'Renewal', 'Endorsement', 'Cancellation']),
            'PolicyStatus': random.choice(['Active', 'Expired', 'Cancelled', 'Pending'])
        })

    return pd.DataFrame(records)

# =============================================================================
# Claims_Bordereaux - Claim-level details
# =============================================================================
def generate_claims_bordereaux():
    records = []
    premium_df = generate_premium_bordereaux()  # Link to premium records

    for i in range(NUM_CLAIMS_RECORDS):
        # Link to a random premium record
        premium_record = premium_df.iloc[random.randint(0, len(premium_df)-1)]

        syn = premium_record['Syndicate']
        umr = premium_record['UMR']
        lloyds_pct = premium_record['LloydsPct'] / 100
        currency = premium_record['Currency']
        fx_rate = premium_record['FX_Rate_to_GBP']

        # Generate UCR
        ucr = generate_ucr(umr, REPORTING_YEAR, i + 1)

        # Dates
        loss_date = premium_record['InceptionDate'] + timedelta(days=random.randint(0, 180))
        notification_date = loss_date + timedelta(days=random.randint(1, 30))
        bordereaux_date = notification_date + timedelta(days=random.randint(15, 45))

        # Claim amounts
        gross_paid = round(np.random.lognormal(mean=7, sigma=1.5), 2)
        gross_paid = min(max(gross_paid, 0), 500000)

        gross_outstanding = round(np.random.lognormal(mean=7, sigma=1.5), 2) if random.random() > 0.3 else 0
        gross_outstanding = min(max(gross_outstanding, 0), 1000000)

        gross_incurred = gross_paid + gross_outstanding

        # ALAE (Allocated Loss Adjustment Expenses)
        alae_paid = round(gross_paid * random.uniform(0.02, 0.10), 2)
        alae_outstanding = round(gross_outstanding * random.uniform(0.02, 0.10), 2)

        # Defence costs
        defence_paid = round(gross_paid * random.uniform(0, 0.05), 2)
        defence_outstanding = round(gross_outstanding * random.uniform(0, 0.05), 2)

        # RI recoveries
        ri_paid = round(gross_paid * random.uniform(0, 0.30), 2)
        ri_outstanding = round(gross_outstanding * random.uniform(0, 0.30), 2)

        # Net amounts
        net_paid = gross_paid - ri_paid
        net_outstanding = gross_outstanding - ri_outstanding
        net_incurred = net_paid + net_outstanding

        # Lloyd's share
        lloyds_paid = round(net_paid * lloyds_pct, 2)
        lloyds_outstanding = round(net_outstanding * lloyds_pct, 2)
        lloyds_incurred = lloyds_paid + lloyds_outstanding

        # Convert to GBP
        gross_incurred_gbp = round(gross_incurred * fx_rate, 2)
        lloyds_incurred_gbp = round(lloyds_incurred * fx_rate, 2)

        # Claim status
        if gross_outstanding == 0:
            status = 'Closed'
        else:
            status = random.choice(['Open', 'Re-opened', 'Pending'])

        records.append({
            'RecordID': i + 1,
            'Syndicate': syn,
            'UCR': ucr,
            'UMR': umr,
            'CoverholderCode': premium_record['CoverholderCode'],
            'CoverholderName': premium_record['CoverholderName'],
            'LOB_Code': premium_record['LOB_Code'],
            'LOB_Name': premium_record['LOB_Name'],
            'LossDate': loss_date,
            'NotificationDate': notification_date,
            'BordereauxDate': bordereaux_date,
            'ClaimReference': f'CLM{i+1:06d}',
            'ClaimStatus': status,
            'Peril': premium_record['Peril'],
            'LossDescription': f'Loss event {i+1} - {premium_record["Peril"]}',
            'ClaimantName': f'Claimant_{i+1:05d}',
            'RiskCountryCode': premium_record['RiskCountryCode'],
            'Currency': currency,
            'FX_Rate_to_GBP': fx_rate,
            # Gross amounts
            'GrossPaid': round(gross_paid, 2),
            'GrossOutstanding': round(gross_outstanding, 2),
            'GrossIncurred': round(gross_incurred, 2),
            # ALAE and Defence
            'ALAE_Paid': alae_paid,
            'ALAE_Outstanding': alae_outstanding,
            'DefenceCosts_Paid': defence_paid,
            'DefenceCosts_Outstanding': defence_outstanding,
            # RI Recoveries
            'RI_Paid': ri_paid,
            'RI_Outstanding': ri_outstanding,
            # Net amounts
            'NetPaid': round(net_paid, 2),
            'NetOutstanding': round(net_outstanding, 2),
            'NetIncurred': round(net_incurred, 2),
            # Lloyd's share
            'LloydsPct': round(lloyds_pct * 100, 1),
            'LloydsPaid': lloyds_paid,
            'LloydsOutstanding': lloyds_outstanding,
            'LloydsIncurred': lloyds_incurred,
            # GBP equivalents
            'GrossIncurred_GBP': gross_incurred_gbp,
            'LloydsIncurred_GBP': lloyds_incurred_gbp,
            # Reserve movement
            'ReserveMovement': round((gross_outstanding - gross_paid) * random.uniform(-0.2, 0.2), 2),
            'LargeClaimFlag': 'Y' if gross_incurred > 100000 else 'N'
        })

    return pd.DataFrame(records)

# =============================================================================
# Risk_Bordereaux - Risk exposure summary
# =============================================================================
def generate_risk_bordereaux():
    records = []
    record_id = 1

    for syn in SYNDICATES:
        for ch_code, ch_name, _ in COVERHOLDERS[:5]:  # Top 5 coverholders per syndicate
            for lob_code, lob_name, _ in LINES_OF_BUSINESS:
                # Skip some combinations for realism
                if random.random() < 0.3:
                    continue

                num_policies = random.randint(10, 200)
                total_sum_insured = num_policies * random.uniform(500000, 5000000)
                total_premium = total_sum_insured * random.uniform(0.001, 0.01)
                avg_rate = (total_premium / total_sum_insured) * 100

                records.append({
                    'RecordID': record_id,
                    'Syndicate': syn,
                    'CoverholderCode': ch_code,
                    'CoverholderName': ch_name,
                    'LOB_Code': lob_code,
                    'LOB_Name': lob_name,
                    'ReportingPeriod': f'{REPORTING_YEAR}-12',
                    'NumPolicies': num_policies,
                    'NumActiveRisks': int(num_policies * 0.85),
                    'TotalSumInsured_GBP_M': round(total_sum_insured / 1000000, 2),
                    'MaxSingleRisk_GBP_M': round(total_sum_insured / num_policies * 3 / 1000000, 2),
                    'AvgSumInsured_GBP_M': round(total_sum_insured / num_policies / 1000000, 4),
                    'TotalPremium_GBP_M': round(total_premium / 1000000, 2),
                    'AvgRate_Pct': round(avg_rate, 3),
                    'PrimaryTerritory': random.choice(['US', 'UK', 'EU', 'APAC']),
                    'PML_GBP_M': round(total_sum_insured * random.uniform(0.1, 0.3) / 1000000, 2),
                    'EML_GBP_M': round(total_sum_insured * random.uniform(0.05, 0.15) / 1000000, 2),
                    'Currency': 'GBP'
                })
                record_id += 1

    return pd.DataFrame(records)

# =============================================================================
# Coverholder_Summary - Performance by coverholder
# =============================================================================
def generate_coverholder_summary():
    records = []

    for syn in SYNDICATES:
        for ch_code, ch_name, ch_country in COVERHOLDERS:
            gwp = np.random.uniform(5, 50)  # GBP millions
            nep = gwp * np.random.uniform(0.85, 0.95)
            claims_incurred = nep * np.random.uniform(0.40, 0.80)
            loss_ratio = claims_incurred / nep

            records.append({
                'Syndicate': syn,
                'CoverholderCode': ch_code,
                'CoverholderName': ch_name,
                'CoverholderCountry': ch_country,
                'ContractReference': f'COV{syn}{ch_code}',
                'ContractInception': datetime(REPORTING_YEAR - 1, 1, 1),
                'ContractExpiry': datetime(REPORTING_YEAR, 12, 31),
                'BindingAuthority_GBP_M': round(gwp * 1.2, 2),
                'GWP_GBP_M': round(gwp, 2),
                'NWP_GBP_M': round(gwp * 0.9, 2),
                'NEP_GBP_M': round(nep, 2),
                'ClaimsIncurred_GBP_M': round(claims_incurred, 2),
                'LossRatio_Pct': round(loss_ratio * 100, 1),
                'NumPolicies': random.randint(100, 2000),
                'NumClaims': random.randint(10, 200),
                'ClaimsFrequency_Pct': round(random.uniform(5, 20), 1),
                'AvgClaimSize_GBP': round(claims_incurred * 1000000 / max(random.randint(10, 200), 1), 0),
                'CommissionRate_Pct': round(random.uniform(15, 30), 1),
                'ProfitCommission_Pct': round(random.uniform(0, 20), 1),
                'LloydsParticipation_Pct': round(random.uniform(10, 50), 1),
                'AuditStatus': random.choice(['Completed', 'Scheduled', 'Overdue']),
                'LastAuditDate': datetime(REPORTING_YEAR, random.randint(1, 12), random.randint(1, 28)),
                'RiskRating': random.choice(['Low', 'Medium', 'High']),
                'Currency': 'GBP'
            })

    return pd.DataFrame(records)

# =============================================================================
# Contract_Performance - TPA/Coverholder contract metrics
# =============================================================================
def generate_contract_performance():
    records = []

    for syn in SYNDICATES:
        for ch_code, ch_name, _ in COVERHOLDERS:
            for year in [REPORTING_YEAR - 2, REPORTING_YEAR - 1, REPORTING_YEAR]:
                gwp = np.random.uniform(5, 50)
                loss_ratio = np.random.uniform(0.40, 0.85)
                expense_ratio = np.random.uniform(0.25, 0.40)
                combined_ratio = loss_ratio + expense_ratio

                records.append({
                    'Syndicate': syn,
                    'CoverholderCode': ch_code,
                    'CoverholderName': ch_name,
                    'UnderwritingYear': year,
                    'GWP_GBP_M': round(gwp, 2),
                    'NEP_GBP_M': round(gwp * 0.90, 2),
                    'ClaimsPaid_GBP_M': round(gwp * loss_ratio * 0.6, 2),
                    'ClaimsOutstanding_GBP_M': round(gwp * loss_ratio * 0.4, 2),
                    'ClaimsIncurred_GBP_M': round(gwp * loss_ratio, 2),
                    'Expenses_GBP_M': round(gwp * expense_ratio, 2),
                    'TechnicalResult_GBP_M': round(gwp * (1 - combined_ratio), 2),
                    'LossRatio_Pct': round(loss_ratio * 100, 1),
                    'ExpenseRatio_Pct': round(expense_ratio * 100, 1),
                    'CombinedRatio_Pct': round(combined_ratio * 100, 1),
                    'UltimateLossRatio_Pct': round(loss_ratio * 100 * random.uniform(0.95, 1.10), 1),
                    'IBNR_GBP_M': round(gwp * loss_ratio * random.uniform(0.1, 0.3), 2),
                    'DevelopmentYear': REPORTING_YEAR - year,
                    'Currency': 'GBP'
                })

    return pd.DataFrame(records)

# =============================================================================
# Generate all tables
# =============================================================================

# Main bordereaux
Premium_Bordereaux = generate_premium_bordereaux()
Claims_Bordereaux = generate_claims_bordereaux()
Risk_Bordereaux = generate_risk_bordereaux()

# Summary tables
Coverholder_Summary = generate_coverholder_summary()
Contract_Performance = generate_contract_performance()

# Summary statistics
print(f"Premium_Bordereaux: {len(Premium_Bordereaux)} rows")
print(f"Claims_Bordereaux: {len(Claims_Bordereaux)} rows")
print(f"Risk_Bordereaux: {len(Risk_Bordereaux)} rows")
print(f"Coverholder_Summary: {len(Coverholder_Summary)} rows")
print(f"Contract_Performance: {len(Contract_Performance)} rows")
