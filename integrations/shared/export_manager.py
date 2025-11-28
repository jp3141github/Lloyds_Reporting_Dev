"""
Export Manager
==============

Multi-format export utilities for Lloyd's regulatory data.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

import pandas as pd
import numpy as np


class ExportManager:
    """
    Multi-format export manager for regulatory data.

    Supports export to CSV, Excel, JSON, and specialized formats
    for Power BI and KNIME integration.
    """

    # Supported formats
    FORMATS = {
        'csv': 'Comma-separated values',
        'excel': 'Microsoft Excel (.xlsx)',
        'json': 'JSON format',
        'parquet': 'Apache Parquet',
        'arff': 'WEKA ARFF format (for KNIME)',
    }

    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize export manager.

        Args:
            output_dir: Default output directory
        """
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / 'exports'
        self._ensure_directory(self.output_dir)
        self.export_log: List[Dict[str, Any]] = []

    def _ensure_directory(self, path: Path):
        """Ensure directory exists."""
        path.mkdir(parents=True, exist_ok=True)

    def export_csv(self, df: pd.DataFrame, filename: str,
                   subdir: Optional[str] = None, **kwargs) -> Path:
        """
        Export DataFrame to CSV.

        Args:
            df: DataFrame to export
            filename: Output filename (without extension)
            subdir: Optional subdirectory
            **kwargs: Additional pandas to_csv arguments

        Returns:
            Path to exported file
        """
        output_path = self._get_output_path(filename, 'csv', subdir)
        df.to_csv(output_path, index=False, **kwargs)
        self._log_export('csv', output_path, len(df))
        return output_path

    def export_excel(self, df: pd.DataFrame, filename: str,
                     sheet_name: str = 'Data',
                     subdir: Optional[str] = None,
                     format_header: bool = True, **kwargs) -> Path:
        """
        Export DataFrame to Excel with optional formatting.

        Args:
            df: DataFrame to export
            filename: Output filename (without extension)
            sheet_name: Excel sheet name
            subdir: Optional subdirectory
            format_header: Apply header formatting
            **kwargs: Additional arguments

        Returns:
            Path to exported file
        """
        output_path = self._get_output_path(filename, 'xlsx', subdir)

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            if format_header:
                self._format_excel_header(writer, sheet_name)

        self._log_export('excel', output_path, len(df))
        return output_path

    def export_multi_sheet_excel(self, tables: Dict[str, pd.DataFrame],
                                  filename: str,
                                  subdir: Optional[str] = None) -> Path:
        """
        Export multiple DataFrames to Excel workbook with multiple sheets.

        Args:
            tables: Dictionary of sheet_name to DataFrame
            filename: Output filename (without extension)
            subdir: Optional subdirectory

        Returns:
            Path to exported file
        """
        output_path = self._get_output_path(filename, 'xlsx', subdir)

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for sheet_name, df in tables.items():
                # Truncate sheet name to Excel limit
                safe_name = sheet_name[:31]
                df.to_excel(writer, sheet_name=safe_name, index=False)
                self._format_excel_header(writer, safe_name)

        total_rows = sum(len(df) for df in tables.values())
        self._log_export('excel_multi', output_path, total_rows, {'sheets': len(tables)})
        return output_path

    def export_json(self, df: pd.DataFrame, filename: str,
                    subdir: Optional[str] = None,
                    orient: str = 'records') -> Path:
        """
        Export DataFrame to JSON.

        Args:
            df: DataFrame to export
            filename: Output filename (without extension)
            subdir: Optional subdirectory
            orient: JSON orientation ('records', 'columns', 'index', etc.)

        Returns:
            Path to exported file
        """
        output_path = self._get_output_path(filename, 'json', subdir)
        df.to_json(output_path, orient=orient, indent=2, date_format='iso')
        self._log_export('json', output_path, len(df))
        return output_path

    def export_parquet(self, df: pd.DataFrame, filename: str,
                       subdir: Optional[str] = None) -> Path:
        """
        Export DataFrame to Parquet format.

        Args:
            df: DataFrame to export
            filename: Output filename (without extension)
            subdir: Optional subdirectory

        Returns:
            Path to exported file
        """
        output_path = self._get_output_path(filename, 'parquet', subdir)
        df.to_parquet(output_path, index=False)
        self._log_export('parquet', output_path, len(df))
        return output_path

    def export_arff(self, df: pd.DataFrame, filename: str,
                    relation_name: Optional[str] = None,
                    subdir: Optional[str] = None) -> Path:
        """
        Export DataFrame to ARFF format for KNIME/WEKA.

        Args:
            df: DataFrame to export
            filename: Output filename (without extension)
            relation_name: ARFF relation name
            subdir: Optional subdirectory

        Returns:
            Path to exported file
        """
        output_path = self._get_output_path(filename, 'arff', subdir)
        relation = relation_name or filename

        with open(output_path, 'w') as f:
            # Write header
            f.write(f"@RELATION {relation}\n\n")

            # Write attributes
            for col in df.columns:
                dtype = df[col].dtype
                if np.issubdtype(dtype, np.number):
                    f.write(f"@ATTRIBUTE {col} NUMERIC\n")
                else:
                    unique_vals = df[col].dropna().unique()
                    if len(unique_vals) <= 50:
                        vals = ','.join(f"'{v}'" for v in unique_vals)
                        f.write(f"@ATTRIBUTE {col} {{{vals}}}\n")
                    else:
                        f.write(f"@ATTRIBUTE {col} STRING\n")

            # Write data
            f.write("\n@DATA\n")
            for _, row in df.iterrows():
                values = []
                for val in row:
                    if pd.isna(val):
                        values.append('?')
                    elif isinstance(val, str):
                        values.append(f"'{val}'")
                    else:
                        values.append(str(val))
                f.write(','.join(values) + '\n')

        self._log_export('arff', output_path, len(df))
        return output_path

    def export_all_formats(self, df: pd.DataFrame, base_filename: str,
                           formats: Optional[List[str]] = None,
                           subdir: Optional[str] = None) -> Dict[str, Path]:
        """
        Export DataFrame to multiple formats.

        Args:
            df: DataFrame to export
            base_filename: Base filename (without extension)
            formats: List of formats to export (default: csv, excel, json)
            subdir: Optional subdirectory

        Returns:
            Dictionary of format to output path
        """
        formats = formats or ['csv', 'excel', 'json']
        results = {}

        for fmt in formats:
            if fmt == 'csv':
                results['csv'] = self.export_csv(df, base_filename, subdir)
            elif fmt == 'excel':
                results['excel'] = self.export_excel(df, base_filename, subdir=subdir)
            elif fmt == 'json':
                results['json'] = self.export_json(df, base_filename, subdir)
            elif fmt == 'parquet':
                results['parquet'] = self.export_parquet(df, base_filename, subdir)
            elif fmt == 'arff':
                results['arff'] = self.export_arff(df, base_filename, subdir=subdir)

        return results

    def export_for_powerbi(self, tables: Dict[str, pd.DataFrame],
                           output_subdir: str = 'powerbi') -> Dict[str, Path]:
        """
        Export tables optimized for Power BI.

        Args:
            tables: Dictionary of table_name to DataFrame
            output_subdir: Output subdirectory

        Returns:
            Dictionary of table_name to output path
        """
        results = {}
        subdir = output_subdir

        for name, df in tables.items():
            # Export as CSV (Power BI preferred format)
            path = self.export_csv(df, name, subdir)
            results[name] = path

        # Create manifest file
        manifest = {
            'generated_at': datetime.now().isoformat(),
            'tables': [
                {
                    'name': name,
                    'file': str(path.name),
                    'rows': len(tables[name]),
                    'columns': tables[name].columns.tolist(),
                }
                for name, path in results.items()
            ]
        }

        manifest_path = self.output_dir / subdir / 'manifest.json'
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        return results

    def export_for_knime(self, tables: Dict[str, pd.DataFrame],
                         output_subdir: str = 'knime') -> Dict[str, Path]:
        """
        Export tables optimized for KNIME.

        Args:
            tables: Dictionary of table_name to DataFrame
            output_subdir: Output subdirectory

        Returns:
            Dictionary of table_name to output path
        """
        results = {}
        subdir = output_subdir

        for name, df in tables.items():
            # Export as ARFF (KNIME native format)
            path = self.export_arff(df, name, subdir=subdir)
            results[name] = path

            # Also export CSV as alternative
            self.export_csv(df, f"{name}_csv", subdir)

        return results

    def _get_output_path(self, filename: str, extension: str,
                         subdir: Optional[str] = None) -> Path:
        """Get full output path."""
        base_dir = self.output_dir / subdir if subdir else self.output_dir
        self._ensure_directory(base_dir)
        return base_dir / f"{filename}.{extension}"

    def _format_excel_header(self, writer, sheet_name: str):
        """Apply formatting to Excel header row."""
        try:
            from openpyxl.styles import Font, PatternFill, Alignment

            workbook = writer.book
            worksheet = writer.sheets[sheet_name]

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
        except ImportError:
            pass  # openpyxl styles not available

    def _log_export(self, format_type: str, path: Path, row_count: int,
                    extra: Optional[Dict[str, Any]] = None):
        """Log export operation."""
        log_entry = {
            'format': format_type,
            'path': str(path),
            'row_count': row_count,
            'timestamp': datetime.now().isoformat(),
        }
        if extra:
            log_entry.update(extra)
        self.export_log.append(log_entry)

    def get_export_summary(self) -> pd.DataFrame:
        """Get summary of all exports."""
        if not self.export_log:
            return pd.DataFrame()
        return pd.DataFrame(self.export_log)

    def clear_exports(self, subdir: Optional[str] = None):
        """Clear exported files."""
        import shutil
        target_dir = self.output_dir / subdir if subdir else self.output_dir
        if target_dir.exists():
            shutil.rmtree(target_dir)
            self._ensure_directory(target_dir)
