# Quarterly Monitoring Return Part A (QMA) - Power BI Data Generator
# Primary Quarterly Financial Return - Backbone of Lloyd's Monitoring
#
# Generates 10 tables covering:
# - Balance sheet, P&L, cash flow
# - Technical account by line of business
# - Investment portfolio analysis
# - Reinsurance assets and creditors
# - Capital position and key ratios
# - Movement analysis vs. prior quarter
#
# Submitted within 30 business days of quarter-end
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
QUARTER_ENDS = {
    'Q1': datetime(2024, 3, 31),
    'Q2': datetime(2024, 6, 30),
    'Q3': datetime(2024, 9, 30),
    'Q4': datetime(2024, 12, 31)
}

# Lloyd's Lines of Business
LINES_OF_BUSINESS = [
    ('PR', 'Property Direct'),
    ('CA', 'Casualty Direct'),
    ('MA', 'Marine Direct'),
    ('AV', 'Aviation Direct'),
    ('EN', 'Energy Direct'),
    ('MO', 'Motor Direct'),
    ('PA', 'Accident & Health'),
    ('CR', 'Credit & Surety'),
    ('PR_RI', 'Property Reinsurance'),
    ('CA_RI', 'Casualty Reinsurance'),
    ('MA_RI', 'Marine Reinsurance'),
    ('SP', 'Specialty')
]

# =============================================================================
# QMA_001_Control - Submission metadata
# =============================================================================
def generate_qma_001_control():
    records = []
    for syn in SYNDICATES:
        for quarter in QUARTERS:
            quarter_end = QUARTER_ENDS[quarter]
            submission_deadline = quarter_end + timedelta(days=30)

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Quarter': quarter,
                'QuarterEnd': quarter_end,
                'SubmissionDeadline': submission_deadline,
                'SubmissionDate': submission_deadline - timedelta(days=np.random.randint(1, 10)),
                'ManagingAgent': f'MA{syn % 100:03d}',
                'ReportType': 'QMA',
                'ReportVersion': '1.0',
                'Status': 'Final',
                'Currency': 'GBP',
                'Audited': 'No' if quarter != 'Q4' else 'Yes'
            })
    return pd.DataFrame(records)

# =============================================================================
# QMA_010_Balance_Sheet - Quarterly balance sheet
# =============================================================================
def generate_qma_010_balance_sheet():
    records = []
    for syn in SYNDICATES:
        # Base values that grow through the year
        base_assets = np.random.uniform(300, 900)
        base_liabilities = base_assets * np.random.uniform(0.60, 0.80)

        for q_idx, quarter in enumerate(QUARTERS):
            # Assets grow through quarters
            growth_factor = 1 + (q_idx * 0.05) + np.random.uniform(-0.02, 0.05)
            total_assets = base_assets * growth_factor

            # Asset breakdown
            investments = total_assets * np.random.uniform(0.50, 0.65)
            ri_recoverables = total_assets * np.random.uniform(0.15, 0.25)
            premium_receivables = total_assets * np.random.uniform(0.10, 0.20)
            cash = total_assets * np.random.uniform(0.05, 0.15)
            other_assets = total_assets - investments - ri_recoverables - premium_receivables - cash

            # Liabilities
            total_liabilities = base_liabilities * growth_factor
            technical_provisions = total_liabilities * np.random.uniform(0.70, 0.85)
            creditors = total_liabilities * np.random.uniform(0.10, 0.20)
            other_liabilities = total_liabilities - technical_provisions - creditors

            # Equity
            equity = total_assets - total_liabilities

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Quarter': quarter,
                'QuarterEnd': QUARTER_ENDS[quarter],
                # Assets
                'TotalAssets_GBP_M': round(total_assets, 2),
                'Investments_GBP_M': round(investments, 2),
                'RI_Recoverables_GBP_M': round(ri_recoverables, 2),
                'PremiumReceivables_GBP_M': round(premium_receivables, 2),
                'Cash_GBP_M': round(cash, 2),
                'OtherAssets_GBP_M': round(other_assets, 2),
                # Liabilities
                'TotalLiabilities_GBP_M': round(total_liabilities, 2),
                'TechnicalProvisions_GBP_M': round(technical_provisions, 2),
                'Creditors_GBP_M': round(creditors, 2),
                'OtherLiabilities_GBP_M': round(other_liabilities, 2),
                # Equity
                'Equity_GBP_M': round(equity, 2),
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# QMA_020_PL_Statement - Profit & Loss account
# =============================================================================
def generate_qma_020_pl_statement():
    records = []
    for syn in SYNDICATES:
        base_gwp = np.random.uniform(50, 150)  # Quarterly GWP
        ytd_gwp = 0

        for q_idx, quarter in enumerate(QUARTERS):
            # Quarterly amounts
            q_gwp = base_gwp * np.random.uniform(0.8, 1.2)
            q_nwp = q_gwp * np.random.uniform(0.85, 0.95)
            q_nep = q_nwp * np.random.uniform(0.90, 1.05)

            # Claims and expenses
            loss_ratio = np.random.uniform(0.50, 0.75)
            expense_ratio = np.random.uniform(0.28, 0.38)

            q_claims = q_nep * loss_ratio
            q_expenses = q_nep * expense_ratio
            q_technical_result = q_nep - q_claims - q_expenses
            q_investment_income = base_gwp * np.random.uniform(0.01, 0.03)
            q_profit = q_technical_result + q_investment_income

            # YTD accumulation
            ytd_gwp += q_gwp
            ytd_nep = ytd_gwp * np.random.uniform(0.80, 0.90)
            ytd_claims = ytd_nep * loss_ratio
            ytd_expenses = ytd_nep * expense_ratio
            ytd_profit = ytd_nep - ytd_claims - ytd_expenses + (q_investment_income * (q_idx + 1))

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Quarter': quarter,
                'QuarterEnd': QUARTER_ENDS[quarter],
                # Quarterly figures
                'Q_GWP_GBP_M': round(q_gwp, 2),
                'Q_NWP_GBP_M': round(q_nwp, 2),
                'Q_NEP_GBP_M': round(q_nep, 2),
                'Q_ClaimsIncurred_GBP_M': round(q_claims, 2),
                'Q_Expenses_GBP_M': round(q_expenses, 2),
                'Q_TechnicalResult_GBP_M': round(q_technical_result, 2),
                'Q_InvestmentIncome_GBP_M': round(q_investment_income, 2),
                'Q_Profit_GBP_M': round(q_profit, 2),
                # YTD figures
                'YTD_GWP_GBP_M': round(ytd_gwp, 2),
                'YTD_NEP_GBP_M': round(ytd_nep, 2),
                'YTD_ClaimsIncurred_GBP_M': round(ytd_claims, 2),
                'YTD_Expenses_GBP_M': round(ytd_expenses, 2),
                'YTD_Profit_GBP_M': round(ytd_profit, 2),
                # Ratios
                'LossRatio_Pct': round(loss_ratio * 100, 1),
                'ExpenseRatio_Pct': round(expense_ratio * 100, 1),
                'CombinedRatio_Pct': round((loss_ratio + expense_ratio) * 100, 1),
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# QMA_030_Cash_Flow - Cash flow statement
# =============================================================================
def generate_qma_030_cash_flow():
    records = []
    for syn in SYNDICATES:
        base_premium = np.random.uniform(40, 120)
        opening_cash = np.random.uniform(20, 80)

        for q_idx, quarter in enumerate(QUARTERS):
            # Operating activities
            premium_received = base_premium * np.random.uniform(0.8, 1.2)
            claims_paid = premium_received * np.random.uniform(0.40, 0.65)
            expenses_paid = premium_received * np.random.uniform(0.20, 0.35)
            ri_paid = premium_received * np.random.uniform(0.05, 0.15)
            ri_received = ri_paid * np.random.uniform(0.3, 0.7)

            operating_cf = premium_received - claims_paid - expenses_paid - ri_paid + ri_received

            # Investing activities
            investment_purchases = np.random.uniform(10, 50)
            investment_sales = np.random.uniform(5, 40)
            investment_income = np.random.uniform(2, 10)
            investing_cf = investment_sales + investment_income - investment_purchases

            # Financing activities
            capital_calls = np.random.uniform(0, 20)
            distributions = np.random.uniform(0, 15)
            financing_cf = capital_calls - distributions

            # Net change and closing
            net_cf = operating_cf + investing_cf + financing_cf
            closing_cash = opening_cash + net_cf

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Quarter': quarter,
                'QuarterEnd': QUARTER_ENDS[quarter],
                # Operating
                'PremiumReceived_GBP_M': round(premium_received, 2),
                'ClaimsPaid_GBP_M': round(claims_paid, 2),
                'ExpensesPaid_GBP_M': round(expenses_paid, 2),
                'RI_PremiumPaid_GBP_M': round(ri_paid, 2),
                'RI_RecoveriesReceived_GBP_M': round(ri_received, 2),
                'OperatingCashFlow_GBP_M': round(operating_cf, 2),
                # Investing
                'InvestmentPurchases_GBP_M': round(investment_purchases, 2),
                'InvestmentSales_GBP_M': round(investment_sales, 2),
                'InvestmentIncome_GBP_M': round(investment_income, 2),
                'InvestingCashFlow_GBP_M': round(investing_cf, 2),
                # Financing
                'CapitalCalls_GBP_M': round(capital_calls, 2),
                'Distributions_GBP_M': round(distributions, 2),
                'FinancingCashFlow_GBP_M': round(financing_cf, 2),
                # Net
                'NetCashFlow_GBP_M': round(net_cf, 2),
                'OpeningCash_GBP_M': round(opening_cash, 2),
                'ClosingCash_GBP_M': round(closing_cash, 2),
                'Currency': 'GBP'
            })

            # Update opening cash for next quarter
            opening_cash = closing_cash

    return pd.DataFrame(records)

# =============================================================================
# QMA_040_Technical_Account - Technical account by LOB
# =============================================================================
def generate_qma_040_technical_account():
    records = []
    for syn in SYNDICATES:
        total_gwp = np.random.uniform(200, 600)
        lob_weights = np.random.dirichlet(np.ones(len(LINES_OF_BUSINESS)))

        for quarter in QUARTERS:
            q_factor = np.random.uniform(0.20, 0.30)  # Quarterly portion of annual

            for i, (lob_code, lob_name) in enumerate(LINES_OF_BUSINESS):
                lob_gwp = total_gwp * lob_weights[i] * q_factor
                lob_nep = lob_gwp * np.random.uniform(0.85, 0.98)

                # LOB-specific loss ratios
                if 'RI' in lob_code:
                    loss_ratio = np.random.uniform(0.55, 0.75)
                elif lob_code in ['CA', 'PA']:
                    loss_ratio = np.random.uniform(0.60, 0.80)
                else:
                    loss_ratio = np.random.uniform(0.45, 0.70)

                expense_ratio = np.random.uniform(0.28, 0.38)

                claims = lob_nep * loss_ratio
                expenses = lob_nep * expense_ratio
                technical_result = lob_nep - claims - expenses

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'LOB_Code': lob_code,
                    'LOB_Name': lob_name,
                    'GWP_GBP_M': round(lob_gwp, 2),
                    'NWP_GBP_M': round(lob_gwp * 0.9, 2),
                    'NEP_GBP_M': round(lob_nep, 2),
                    'ClaimsIncurred_GBP_M': round(claims, 2),
                    'Expenses_GBP_M': round(expenses, 2),
                    'TechnicalResult_GBP_M': round(technical_result, 2),
                    'LossRatio_Pct': round(loss_ratio * 100, 1),
                    'ExpenseRatio_Pct': round(expense_ratio * 100, 1),
                    'CombinedRatio_Pct': round((loss_ratio + expense_ratio) * 100, 1),
                    'Currency': 'GBP'
                })
    return pd.DataFrame(records)

# =============================================================================
# QMA_050_Investment_Portfolio - Investment holdings
# =============================================================================
def generate_qma_050_investment_portfolio():
    records = []
    asset_classes = [
        ('GOVT', 'Government Bonds', 0.40),
        ('CORP', 'Corporate Bonds', 0.30),
        ('CASH', 'Cash & Equivalents', 0.15),
        ('EQ', 'Equities', 0.05),
        ('PROP', 'Property', 0.05),
        ('ALT', 'Alternative', 0.05)
    ]

    for syn in SYNDICATES:
        base_portfolio = np.random.uniform(200, 600)

        for quarter in QUARTERS:
            # Portfolio grows through year
            q_factor = 1 + (QUARTERS.index(quarter) * 0.02)
            total_portfolio = base_portfolio * q_factor

            for asset_code, asset_name, base_alloc in asset_classes:
                alloc = base_alloc * np.random.uniform(0.8, 1.2)
                market_value = total_portfolio * alloc
                book_value = market_value * np.random.uniform(0.95, 1.05)
                unrealized_gain = market_value - book_value
                yield_rate = np.random.uniform(0.02, 0.06)
                duration = np.random.uniform(1, 7) if 'Bond' in asset_name else 0

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'AssetClass_Code': asset_code,
                    'AssetClass_Name': asset_name,
                    'MarketValue_GBP_M': round(market_value, 2),
                    'BookValue_GBP_M': round(book_value, 2),
                    'UnrealizedGainLoss_GBP_M': round(unrealized_gain, 2),
                    'Allocation_Pct': round(alloc * 100, 1),
                    'YieldRate_Pct': round(yield_rate * 100, 2),
                    'Duration_Years': round(duration, 1),
                    'CreditRating': np.random.choice(['AAA', 'AA', 'A', 'BBB']) if 'Bond' in asset_name else 'N/A',
                    'Currency': 'GBP'
                })
    return pd.DataFrame(records)

# =============================================================================
# QMA_060_Reinsurance_Assets - RI recoverable assets
# =============================================================================
def generate_qma_060_reinsurance_assets():
    records = []
    ri_types = [
        ('QS', 'Quota Share'),
        ('SS', 'Surplus Share'),
        ('XOL', 'Excess of Loss'),
        ('CAT', 'Catastrophe'),
        ('FAC', 'Facultative')
    ]

    for syn in SYNDICATES:
        base_ri = np.random.uniform(30, 150)

        for quarter in QUARTERS:
            for ri_code, ri_name in ri_types:
                weight = np.random.uniform(0.1, 0.4)
                gross_recoverable = base_ri * weight
                bad_debt_provision = gross_recoverable * np.random.uniform(0.01, 0.05)
                net_recoverable = gross_recoverable - bad_debt_provision

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'RI_Type_Code': ri_code,
                    'RI_Type_Name': ri_name,
                    'GrossRecoverable_GBP_M': round(gross_recoverable, 2),
                    'BadDebtProvision_GBP_M': round(bad_debt_provision, 2),
                    'NetRecoverable_GBP_M': round(net_recoverable, 2),
                    'AvgCounterpartyRating': np.random.choice(['AAA', 'AA', 'A', 'BBB']),
                    'CollateralHeld_GBP_M': round(gross_recoverable * np.random.uniform(0, 0.3), 2),
                    'Currency': 'GBP'
                })
    return pd.DataFrame(records)

# =============================================================================
# QMA_070_Creditors - Creditor analysis
# =============================================================================
def generate_qma_070_creditors():
    records = []
    creditor_types = [
        ('REINS', 'Reinsurers', 0.35),
        ('BROKER', 'Brokers', 0.25),
        ('TAX', 'Tax Authorities', 0.15),
        ('AGENTS', 'Managing Agent', 0.10),
        ('OTHER', 'Other Creditors', 0.15)
    ]

    for syn in SYNDICATES:
        base_creditors = np.random.uniform(40, 150)

        for quarter in QUARTERS:
            for cred_code, cred_name, base_weight in creditor_types:
                weight = base_weight * np.random.uniform(0.7, 1.3)
                amount = base_creditors * weight
                overdue = amount * np.random.uniform(0, 0.15)

                records.append({
                    'Syndicate': syn,
                    'ReportingYear': REPORTING_YEAR,
                    'Quarter': quarter,
                    'QuarterEnd': QUARTER_ENDS[quarter],
                    'Creditor_Code': cred_code,
                    'Creditor_Name': cred_name,
                    'Amount_GBP_M': round(amount, 2),
                    'OverdueAmount_GBP_M': round(overdue, 2),
                    'Current_GBP_M': round(amount - overdue, 2),
                    'Overdue30_GBP_M': round(overdue * 0.5, 2),
                    'Overdue60_GBP_M': round(overdue * 0.3, 2),
                    'Overdue90Plus_GBP_M': round(overdue * 0.2, 2),
                    'Currency': 'GBP'
                })
    return pd.DataFrame(records)

# =============================================================================
# QMA_080_Capital_Position - Capital position and movements
# =============================================================================
def generate_qma_080_capital_position():
    records = []
    for syn in SYNDICATES:
        base_scr = np.random.uniform(80, 200)
        base_own_funds = base_scr * np.random.uniform(1.3, 1.8)

        for q_idx, quarter in enumerate(QUARTERS):
            # Capital changes through quarters
            q_profit = np.random.uniform(-10, 30)
            q_capital_call = np.random.uniform(0, 10)
            q_distribution = np.random.uniform(0, 5) if q_idx == 3 else 0

            own_funds = base_own_funds + (q_profit * (q_idx + 1)) + q_capital_call - q_distribution
            scr = base_scr * (1 + np.random.uniform(-0.05, 0.05))
            mcr = scr * np.random.uniform(0.25, 0.35)

            coverage_ratio = own_funds / scr

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Quarter': quarter,
                'QuarterEnd': QUARTER_ENDS[quarter],
                'SCR_GBP_M': round(scr, 2),
                'MCR_GBP_M': round(mcr, 2),
                'OwnFunds_GBP_M': round(own_funds, 2),
                'Tier1_GBP_M': round(own_funds * 0.95, 2),
                'Tier2_GBP_M': round(own_funds * 0.05, 2),
                'CoverageRatio_Pct': round(coverage_ratio * 100, 1),
                'CoverageRatio': round(coverage_ratio, 3),
                'SurplusDeficit_GBP_M': round(own_funds - scr, 2),
                'Q_Profit_GBP_M': round(q_profit, 2),
                'Q_CapitalCall_GBP_M': round(q_capital_call, 2),
                'Q_Distribution_GBP_M': round(q_distribution, 2),
                'CapitalStatus': 'Adequate' if coverage_ratio >= 1.0 else 'Deficient',
                'Currency': 'GBP'
            })
    return pd.DataFrame(records)

# =============================================================================
# QMA_090_Key_Ratios - KPIs and performance metrics
# =============================================================================
def generate_qma_090_key_ratios():
    records = []
    for syn in SYNDICATES:
        for quarter in QUARTERS:
            loss_ratio = np.random.uniform(0.50, 0.75)
            expense_ratio = np.random.uniform(0.28, 0.38)
            combined_ratio = loss_ratio + expense_ratio

            records.append({
                'Syndicate': syn,
                'ReportingYear': REPORTING_YEAR,
                'Quarter': quarter,
                'QuarterEnd': QUARTER_ENDS[quarter],
                # Underwriting ratios
                'LossRatio_Pct': round(loss_ratio * 100, 1),
                'ExpenseRatio_Pct': round(expense_ratio * 100, 1),
                'CombinedRatio_Pct': round(combined_ratio * 100, 1),
                'AcquisitionRatio_Pct': round(expense_ratio * 0.7 * 100, 1),
                'AdminRatio_Pct': round(expense_ratio * 0.3 * 100, 1),
                # Capital ratios
                'SCR_Coverage_Pct': round(np.random.uniform(130, 180), 1),
                'MCR_Coverage_Pct': round(np.random.uniform(400, 600), 1),
                # Investment
                'InvestmentReturn_Pct': round(np.random.uniform(2, 5), 2),
                'ROE_Pct': round(np.random.uniform(5, 15), 1),
                # Operational
                'PremiumGrowth_Pct': round(np.random.uniform(-5, 15), 1),
                'ReserveDevelopment_Pct': round(np.random.uniform(-5, 5), 1),
                'CapacityUtilization_Pct': round(np.random.uniform(70, 95), 1)
            })
    return pd.DataFrame(records)

# =============================================================================
# Generate all tables
# =============================================================================

# Control
QMA_001_Control = generate_qma_001_control()

# Financial statements
QMA_010_Balance_Sheet = generate_qma_010_balance_sheet()
QMA_020_PL_Statement = generate_qma_020_pl_statement()
QMA_030_Cash_Flow = generate_qma_030_cash_flow()
QMA_040_Technical_Account = generate_qma_040_technical_account()

# Assets and liabilities detail
QMA_050_Investment_Portfolio = generate_qma_050_investment_portfolio()
QMA_060_Reinsurance_Assets = generate_qma_060_reinsurance_assets()
QMA_070_Creditors = generate_qma_070_creditors()

# Capital and performance
QMA_080_Capital_Position = generate_qma_080_capital_position()
QMA_090_Key_Ratios = generate_qma_090_key_ratios()

# Summary statistics
print(f"QMA_001_Control: {len(QMA_001_Control)} rows")
print(f"QMA_010_Balance_Sheet: {len(QMA_010_Balance_Sheet)} rows")
print(f"QMA_020_PL_Statement: {len(QMA_020_PL_Statement)} rows")
print(f"QMA_030_Cash_Flow: {len(QMA_030_Cash_Flow)} rows")
print(f"QMA_040_Technical_Account: {len(QMA_040_Technical_Account)} rows")
print(f"QMA_050_Investment_Portfolio: {len(QMA_050_Investment_Portfolio)} rows")
print(f"QMA_060_Reinsurance_Assets: {len(QMA_060_Reinsurance_Assets)} rows")
print(f"QMA_070_Creditors: {len(QMA_070_Creditors)} rows")
print(f"QMA_080_Capital_Position: {len(QMA_080_Capital_Position)} rows")
print(f"QMA_090_Key_Ratios: {len(QMA_090_Key_Ratios)} rows")
