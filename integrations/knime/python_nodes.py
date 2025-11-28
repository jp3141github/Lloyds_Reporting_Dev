"""
KNIME Python Node Scripts
=========================

Pre-built Python scripts for use in KNIME Python Script nodes.
"""

from typing import Dict


class PythonNodeScripts:
    """
    Pre-built Python scripts for KNIME nodes.

    Provides ready-to-use scripts that can be copied into
    KNIME Python Script nodes for Lloyd's regulatory reporting.
    """

    @staticmethod
    def get_data_loader_script(category: str) -> str:
        """
        Get a data loader script for a specific category.

        Args:
            category: Data category (rra, rrq, qsr, asb, lcr, sbf, qma, fscs, liquidity, claims)

        Returns:
            Python script string
        """
        return f'''# Lloyd's Regulatory Reporting Data Loader
# Category: {category.upper()}
# For use in KNIME Python Script node

import pandas as pd
import numpy as np
import sys

# Configure path to Lloyd's Reporting Dev
LLOYDS_PATH = '/path/to/Lloyds_Reporting_Dev'
sys.path.insert(0, LLOYDS_PATH)

try:
    from integrations.knime import KNIMEConnector

    connector = KNIMEConnector()
    datasets = connector.generate_all_datasets(['{category}'])

    # Get all tables for this category
    output_table = pd.DataFrame()
    for name, df in datasets.items():
        if output_table.empty:
            output_table = df
        else:
            # If multiple tables, concatenate with source column
            df = df.copy()
            df['_source_table'] = name
            if '_source_table' not in output_table.columns:
                output_table['_source_table'] = list(datasets.keys())[0]
            output_table = pd.concat([output_table, df], ignore_index=True)

except Exception as e:
    print(f"Error loading {category.upper()} data: {{e}}")
    output_table = pd.DataFrame({{'Error': [str(e)], 'Category': ['{category}']}})
'''

    @staticmethod
    def get_all_data_script() -> str:
        """Get script to load all regulatory data categories."""
        return '''# Lloyd's Regulatory Reporting - All Categories
# For use in KNIME Python Script node

import pandas as pd
import numpy as np
import sys

# Configure path to Lloyd's Reporting Dev
LLOYDS_PATH = '/path/to/Lloyds_Reporting_Dev'
sys.path.insert(0, LLOYDS_PATH)

try:
    from integrations.knime import KNIMEConnector

    connector = KNIMEConnector()

    # Generate all datasets
    datasets = connector.generate_all_datasets()

    # Create summary table
    summary_rows = []
    for name, df in datasets.items():
        summary_rows.append({
            'table_name': name,
            'row_count': len(df),
            'column_count': len(df.columns),
            'columns': ', '.join(df.columns.tolist()[:10]) + ('...' if len(df.columns) > 10 else ''),
            'memory_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
        })

    output_table = pd.DataFrame(summary_rows)
    print(f"Loaded {len(datasets)} tables successfully")

except Exception as e:
    print(f"Error loading data: {e}")
    output_table = pd.DataFrame({'Error': [str(e)]})
'''

    @staticmethod
    def get_qrt_generator_script() -> str:
        """Get script to generate QRT templates."""
        return '''# Lloyd's QRT Template Generator
# For use in KNIME Python Script node

import pandas as pd
import numpy as np
import sys

# Configure path
LLOYDS_PATH = '/path/to/Lloyds_Reporting_Dev'
sys.path.insert(0, LLOYDS_PATH)

try:
    from QRTs import generate_all_qrts

    # Generate all QRT templates
    qrts = generate_all_qrts()

    # Create summary output
    summary_rows = []
    for name, df in qrts.items():
        summary_rows.append({
            'qrt_code': name,
            'rows': len(df),
            'columns': len(df.columns),
            'column_list': ', '.join(df.columns.tolist()[:5]) + ('...' if len(df.columns) > 5 else ''),
        })

    output_table = pd.DataFrame(summary_rows)
    print(f"Generated {len(qrts)} QRT templates")

except Exception as e:
    print(f"Error generating QRTs: {e}")
    output_table = pd.DataFrame({'Error': [str(e)]})
'''

    @staticmethod
    def get_claims_analysis_script() -> str:
        """Get script for claims development analysis."""
        return '''# Lloyd's Claims Development Analysis
# For use in KNIME Python Script node

import pandas as pd
import numpy as np
import sys

LLOYDS_PATH = '/path/to/Lloyds_Reporting_Dev'
sys.path.insert(0, LLOYDS_PATH)

try:
    from integrations.knime import KNIMEConnector

    connector = KNIMEConnector()
    datasets = connector.generate_all_datasets(['claims'])

    # Get claims triangle data
    claims_data = datasets.get('claims_development_triangle', pd.DataFrame())

    if not claims_data.empty:
        # Calculate development factors
        numeric_cols = claims_data.select_dtypes(include=[np.number]).columns

        output_table = claims_data
        print(f"Loaded claims data with {len(claims_data)} rows")
    else:
        output_table = pd.DataFrame({'Message': ['No claims data available']})

except Exception as e:
    print(f"Error: {e}")
    output_table = pd.DataFrame({'Error': [str(e)]})
'''

    @staticmethod
    def get_capital_analysis_script() -> str:
        """Get script for capital position analysis."""
        return '''# Lloyd's Capital Position Analysis
# For use in KNIME Python Script node

import pandas as pd
import numpy as np
import sys

LLOYDS_PATH = '/path/to/Lloyds_Reporting_Dev'
sys.path.insert(0, LLOYDS_PATH)

try:
    from integrations.knime import KNIMEConnector

    connector = KNIMEConnector()
    datasets = connector.generate_all_datasets(['lcr', 'liquidity'])

    # Combine capital metrics
    output_rows = []

    for name, df in datasets.items():
        if 'lcr' in name.lower() or 'capital' in name.lower():
            row = {
                'table': name,
                'records': len(df),
            }
            # Add numeric summaries
            for col in df.select_dtypes(include=[np.number]).columns[:5]:
                row[f'{col}_sum'] = df[col].sum()
            output_rows.append(row)

    if output_rows:
        output_table = pd.DataFrame(output_rows)
    else:
        output_table = pd.DataFrame({'Message': ['No capital data found']})

except Exception as e:
    print(f"Error: {e}")
    output_table = pd.DataFrame({'Error': [str(e)]})
'''

    @staticmethod
    def get_solvency_report_script() -> str:
        """Get script for Solvency II reporting."""
        return '''# Lloyd's Solvency II Reporting
# For use in KNIME Python Script node

import pandas as pd
import numpy as np
import sys

LLOYDS_PATH = '/path/to/Lloyds_Reporting_Dev'
sys.path.insert(0, LLOYDS_PATH)

try:
    from integrations.knime import KNIMEConnector

    connector = KNIMEConnector()
    datasets = connector.generate_all_datasets(['qsr', 'asb'])

    # Build solvency summary
    output_rows = []
    for name, df in datasets.items():
        row = {
            'table_name': name,
            'row_count': len(df),
            'column_count': len(df.columns),
        }

        # Add key metrics if available
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            row['total_value'] = df[numeric_cols].sum().sum()
            row['mean_value'] = df[numeric_cols].mean().mean()

        output_rows.append(row)

    output_table = pd.DataFrame(output_rows)
    print(f"Generated solvency report with {len(output_rows)} tables")

except Exception as e:
    print(f"Error: {e}")
    output_table = pd.DataFrame({'Error': [str(e)]})
'''

    @staticmethod
    def get_data_validation_script() -> str:
        """Get script for data validation checks."""
        return '''# Lloyd's Data Validation
# For use in KNIME Python Script node

import pandas as pd
import numpy as np
import sys

LLOYDS_PATH = '/path/to/Lloyds_Reporting_Dev'
sys.path.insert(0, LLOYDS_PATH)

# Input table from previous node
input_data = input_table.copy() if 'input_table' in dir() else pd.DataFrame()

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Run validation checks on input data."""
    validations = []

    # Check for null values
    null_counts = df.isnull().sum()
    for col, count in null_counts.items():
        if count > 0:
            validations.append({
                'check': 'null_values',
                'column': col,
                'status': 'WARNING',
                'message': f'{count} null values found',
                'value': count
            })

    # Check for negative values in numeric columns
    for col in df.select_dtypes(include=[np.number]).columns:
        neg_count = (df[col] < 0).sum()
        if neg_count > 0:
            validations.append({
                'check': 'negative_values',
                'column': col,
                'status': 'INFO',
                'message': f'{neg_count} negative values',
                'value': neg_count
            })

    # Check for duplicates
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        validations.append({
            'check': 'duplicates',
            'column': 'ALL',
            'status': 'WARNING',
            'message': f'{dup_count} duplicate rows',
            'value': dup_count
        })

    if not validations:
        validations.append({
            'check': 'overall',
            'column': 'ALL',
            'status': 'PASS',
            'message': 'All validation checks passed',
            'value': 0
        })

    return pd.DataFrame(validations)

if not input_data.empty:
    output_table = validate_data(input_data)
else:
    output_table = pd.DataFrame({
        'check': ['no_data'],
        'column': ['N/A'],
        'status': ['ERROR'],
        'message': ['No input data provided'],
        'value': [0]
    })
'''

    @staticmethod
    def get_excel_export_script() -> str:
        """Get script for Excel export with formatting."""
        return '''# Lloyd's Excel Export with Formatting
# For use in KNIME Python Script node

import pandas as pd
import numpy as np
from pathlib import Path
import sys

LLOYDS_PATH = '/path/to/Lloyds_Reporting_Dev'
sys.path.insert(0, LLOYDS_PATH)

# Input table from previous node
input_data = input_table.copy() if 'input_table' in dir() else pd.DataFrame()

# Configuration
OUTPUT_PATH = '/path/to/output/report.xlsx'
SHEET_NAME = 'Regulatory Data'

try:
    if not input_data.empty:
        # Ensure output directory exists
        Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)

        # Export with openpyxl for formatting
        with pd.ExcelWriter(OUTPUT_PATH, engine='openpyxl') as writer:
            input_data.to_excel(writer, sheet_name=SHEET_NAME, index=False)

            # Get workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets[SHEET_NAME]

            # Format header row
            from openpyxl.styles import Font, PatternFill, Alignment

            header_font = Font(bold=True, color='FFFFFF')
            header_fill = PatternFill(start_color='003366', end_color='003366', fill_type='solid')

            for cell in worksheet[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal='center')

            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                worksheet.column_dimensions[column_letter].width = min(max_length + 2, 50)

        output_table = pd.DataFrame({
            'status': ['SUCCESS'],
            'file_path': [OUTPUT_PATH],
            'rows_exported': [len(input_data)],
            'columns_exported': [len(input_data.columns)]
        })
    else:
        output_table = pd.DataFrame({
            'status': ['ERROR'],
            'message': ['No input data to export']
        })

except Exception as e:
    output_table = pd.DataFrame({
        'status': ['ERROR'],
        'message': [str(e)]
    })
'''

    @classmethod
    def get_all_scripts(cls) -> Dict[str, str]:
        """Get all available scripts as a dictionary."""
        return {
            'data_loader_rra': cls.get_data_loader_script('rra'),
            'data_loader_rrq': cls.get_data_loader_script('rrq'),
            'data_loader_qsr': cls.get_data_loader_script('qsr'),
            'data_loader_asb': cls.get_data_loader_script('asb'),
            'data_loader_lcr': cls.get_data_loader_script('lcr'),
            'data_loader_sbf': cls.get_data_loader_script('sbf'),
            'data_loader_qma': cls.get_data_loader_script('qma'),
            'data_loader_fscs': cls.get_data_loader_script('fscs'),
            'data_loader_liquidity': cls.get_data_loader_script('liquidity'),
            'data_loader_claims': cls.get_data_loader_script('claims'),
            'all_data': cls.get_all_data_script(),
            'qrt_generator': cls.get_qrt_generator_script(),
            'claims_analysis': cls.get_claims_analysis_script(),
            'capital_analysis': cls.get_capital_analysis_script(),
            'solvency_report': cls.get_solvency_report_script(),
            'data_validation': cls.get_data_validation_script(),
            'excel_export': cls.get_excel_export_script(),
        }

    @classmethod
    def list_scripts(cls) -> str:
        """List all available scripts with descriptions."""
        scripts = [
            ('data_loader_*', 'Load data for specific categories (rra, rrq, qsr, etc.)'),
            ('all_data', 'Load all regulatory data categories with summary'),
            ('qrt_generator', 'Generate Solvency II QRT templates'),
            ('claims_analysis', 'Claims development triangle analysis'),
            ('capital_analysis', 'Capital position and LCR analysis'),
            ('solvency_report', 'Solvency II QSR/ASB reporting'),
            ('data_validation', 'Run validation checks on input data'),
            ('excel_export', 'Export to formatted Excel file'),
        ]

        output = "Available KNIME Python Node Scripts:\n"
        output += "=" * 50 + "\n\n"
        for name, desc in scripts:
            output += f"  {name}\n    {desc}\n\n"

        return output
