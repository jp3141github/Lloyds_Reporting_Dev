"""
KNIME Workflow Builder
======================

Generates KNIME workflow configurations and templates.
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class WorkflowBuilder:
    """
    Build KNIME workflow configurations and templates.

    Generates workflow.knime files, node configurations, and
    connection specifications for Lloyd's reporting workflows.
    """

    # Standard node types used in Lloyd's workflows
    NODE_TYPES = {
        'csv_reader': 'org.knime.base.node.io.csvreader.CSVReaderNodeFactory',
        'python_script': 'org.knime.python3.scripting.nodes.script.Python3ScriptNodeFactory',
        'table_view': 'org.knime.base.node.viz.table.TableNodeFactory',
        'excel_writer': 'org.knime.ext.poi3.node.io.filehandling.excel.writer.ExcelTableWriterNodeFactory',
        'column_filter': 'org.knime.base.node.preproc.filter.column.ColumnFilterNodeFactory',
        'row_filter': 'org.knime.base.node.preproc.filter.row3.RowFilterNodeFactory',
        'group_by': 'org.knime.base.node.preproc.groupby.GroupByNodeFactory',
        'joiner': 'org.knime.base.node.preproc.joiner3.Joiner3NodeFactory',
        'pivot': 'org.knime.base.node.preproc.pivot.Pivot2NodeFactory',
        'statistics': 'org.knime.base.node.stats.viz.extended.ExtendedStatisticsNodeFactory',
    }

    def __init__(self):
        """Initialize workflow builder."""
        self.nodes = []
        self.connections = []
        self.workflow_name = "Lloyd's Regulatory Reporting"
        self.node_counter = 0

    def create_workflow_template(self, name: str = "Lloyd's Reporting Workflow") -> Dict[str, Any]:
        """
        Create a complete workflow template configuration.

        Args:
            name: Workflow name

        Returns:
            Workflow configuration dictionary
        """
        self.workflow_name = name
        self.nodes = []
        self.connections = []
        self.node_counter = 0

        return {
            'workflow': {
                'name': name,
                'version': '1.0.0',
                'created': datetime.now().isoformat(),
                'description': 'Lloyd\'s of London regulatory reporting workflow',
                'author': 'Lloyd\'s Development Team',
            },
            'metadata': {
                'knime_version': '5.2+',
                'python_version': '3.9+',
                'required_extensions': [
                    'KNIME Python Integration',
                    'KNIME Excel Support',
                    'KNIME Statistics',
                ],
            },
            'nodes': [],
            'connections': [],
        }

    def add_data_loader_node(self, dataset_category: str, x: int = 100, y: int = 100) -> int:
        """
        Add a Python data loader node.

        Args:
            dataset_category: Category to load (rra, qsr, lcr, etc.)
            x: X position in workflow
            y: Y position in workflow

        Returns:
            Node ID
        """
        node_id = self._next_node_id()
        self.nodes.append({
            'id': node_id,
            'type': 'python_script',
            'factory': self.NODE_TYPES['python_script'],
            'name': f'Load {dataset_category.upper()} Data',
            'position': {'x': x, 'y': y},
            'settings': {
                'script': self._get_loader_script(dataset_category),
                'python_version': '3',
                'output_mode': 'table',
            },
        })
        return node_id

    def add_csv_reader_node(self, file_path: str, x: int = 100, y: int = 100) -> int:
        """
        Add a CSV reader node.

        Args:
            file_path: Path to CSV file
            x: X position
            y: Y position

        Returns:
            Node ID
        """
        node_id = self._next_node_id()
        self.nodes.append({
            'id': node_id,
            'type': 'csv_reader',
            'factory': self.NODE_TYPES['csv_reader'],
            'name': f'Read {Path(file_path).stem}',
            'position': {'x': x, 'y': y},
            'settings': {
                'file_path': file_path,
                'has_header': True,
                'delimiter': ',',
                'quote_char': '"',
            },
        })
        return node_id

    def add_table_view_node(self, name: str, x: int = 100, y: int = 100) -> int:
        """Add a table view node for data preview."""
        node_id = self._next_node_id()
        self.nodes.append({
            'id': node_id,
            'type': 'table_view',
            'factory': self.NODE_TYPES['table_view'],
            'name': name,
            'position': {'x': x, 'y': y},
        })
        return node_id

    def add_excel_writer_node(self, output_path: str, x: int = 100, y: int = 100) -> int:
        """Add an Excel writer node."""
        node_id = self._next_node_id()
        self.nodes.append({
            'id': node_id,
            'type': 'excel_writer',
            'factory': self.NODE_TYPES['excel_writer'],
            'name': f'Export to Excel',
            'position': {'x': x, 'y': y},
            'settings': {
                'output_path': output_path,
                'sheet_name': 'Data',
                'overwrite': True,
            },
        })
        return node_id

    def add_group_by_node(self, group_columns: List[str], agg_columns: Dict[str, str],
                          x: int = 100, y: int = 100) -> int:
        """
        Add a GroupBy node.

        Args:
            group_columns: Columns to group by
            agg_columns: Dict of column -> aggregation method
            x: X position
            y: Y position
        """
        node_id = self._next_node_id()
        self.nodes.append({
            'id': node_id,
            'type': 'group_by',
            'factory': self.NODE_TYPES['group_by'],
            'name': 'Group By',
            'position': {'x': x, 'y': y},
            'settings': {
                'group_columns': group_columns,
                'aggregations': agg_columns,
            },
        })
        return node_id

    def add_statistics_node(self, x: int = 100, y: int = 100) -> int:
        """Add a statistics node."""
        node_id = self._next_node_id()
        self.nodes.append({
            'id': node_id,
            'type': 'statistics',
            'factory': self.NODE_TYPES['statistics'],
            'name': 'Calculate Statistics',
            'position': {'x': x, 'y': y},
        })
        return node_id

    def add_connection(self, source_node: int, source_port: int,
                       dest_node: int, dest_port: int):
        """
        Add a connection between nodes.

        Args:
            source_node: Source node ID
            source_port: Source port index
            dest_node: Destination node ID
            dest_port: Destination port index
        """
        self.connections.append({
            'source': {'node_id': source_node, 'port': source_port},
            'destination': {'node_id': dest_node, 'port': dest_port},
        })

    def build_rra_workflow(self) -> Dict[str, Any]:
        """Build a complete RRA analysis workflow."""
        workflow = self.create_workflow_template("RRA Analysis Workflow")

        # Add nodes
        loader = self.add_data_loader_node('rra', 100, 100)
        stats = self.add_statistics_node(300, 100)
        view = self.add_table_view_node('RRA Data View', 300, 200)
        excel = self.add_excel_writer_node('rra_output.xlsx', 500, 100)

        # Add connections
        self.add_connection(loader, 0, stats, 0)
        self.add_connection(loader, 0, view, 0)
        self.add_connection(stats, 0, excel, 0)

        workflow['nodes'] = self.nodes
        workflow['connections'] = self.connections
        return workflow

    def build_solvency_workflow(self) -> Dict[str, Any]:
        """Build a Solvency II analysis workflow."""
        workflow = self.create_workflow_template("Solvency II Reporting Workflow")

        # QSR Data
        qsr_loader = self.add_data_loader_node('qsr', 100, 100)
        # ASB Data
        asb_loader = self.add_data_loader_node('asb', 100, 250)
        # Views
        qsr_view = self.add_table_view_node('QSR Data', 300, 100)
        asb_view = self.add_table_view_node('ASB Data', 300, 250)
        # Statistics
        qsr_stats = self.add_statistics_node(500, 100)
        asb_stats = self.add_statistics_node(500, 250)

        # Connections
        self.add_connection(qsr_loader, 0, qsr_view, 0)
        self.add_connection(asb_loader, 0, asb_view, 0)
        self.add_connection(qsr_loader, 0, qsr_stats, 0)
        self.add_connection(asb_loader, 0, asb_stats, 0)

        workflow['nodes'] = self.nodes
        workflow['connections'] = self.connections
        return workflow

    def build_capital_workflow(self) -> Dict[str, Any]:
        """Build a Lloyd's Capital analysis workflow."""
        workflow = self.create_workflow_template("Lloyd's Capital Analysis Workflow")

        # LCR Data
        lcr_loader = self.add_data_loader_node('lcr', 100, 100)
        # Liquidity Data
        liq_loader = self.add_data_loader_node('liquidity', 100, 250)
        # Views and exports
        lcr_view = self.add_table_view_node('LCR Data', 300, 100)
        liq_view = self.add_table_view_node('Liquidity Data', 300, 250)
        excel_export = self.add_excel_writer_node('capital_analysis.xlsx', 500, 175)

        # Connections
        self.add_connection(lcr_loader, 0, lcr_view, 0)
        self.add_connection(liq_loader, 0, liq_view, 0)
        self.add_connection(lcr_loader, 0, excel_export, 0)

        workflow['nodes'] = self.nodes
        workflow['connections'] = self.connections
        return workflow

    def export_workflow(self, workflow: Dict[str, Any], output_path: str):
        """
        Export workflow configuration to file.

        Args:
            workflow: Workflow configuration
            output_path: Output file path
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(workflow, f, indent=2)

        print(f"Exported workflow to {output_path}")

    def _next_node_id(self) -> int:
        """Get next node ID."""
        self.node_counter += 1
        return self.node_counter

    def _get_loader_script(self, category: str) -> str:
        """Get Python script for data loading."""
        return f'''# Lloyd's Regulatory Reporting Data Loader
# Category: {category.upper()}

import pandas as pd
import numpy as np
import sys

# Add integrations path
sys.path.insert(0, '/path/to/Lloyds_Reporting_Dev')

try:
    from integrations.knime import KNIMEConnector
    connector = KNIMEConnector()
    datasets = connector.generate_all_datasets(['{category}'])

    # Get first dataset as output
    dataset_names = list(datasets.keys())
    if dataset_names:
        output_table = datasets[dataset_names[0]]
    else:
        output_table = pd.DataFrame()
except Exception as e:
    print(f"Error: {{e}}")
    output_table = pd.DataFrame({{'Error': [str(e)]}})
'''

    def generate_readme(self) -> str:
        """Generate README for KNIME workflows."""
        return """# KNIME Workflows for Lloyd's Regulatory Reporting

## Available Workflows

### 1. RRA Analysis Workflow
Analyzes Reserving Return Annual data with statistics and export capabilities.

### 2. Solvency II Reporting Workflow
Combines QSR and ASB data for comprehensive Solvency II analysis.

### 3. Capital Analysis Workflow
Analyzes LCR and Liquidity data for capital management.

## Setup Instructions

1. **Install KNIME Analytics Platform** (version 5.2 or later)
2. **Install Required Extensions:**
   - KNIME Python Integration
   - KNIME Excel Support
   - KNIME Statistics

3. **Configure Python Environment:**
   ```bash
   pip install pandas numpy openpyxl
   ```

4. **Set Python Path in KNIME:**
   - File > Preferences > KNIME > Python
   - Set path to Python executable

5. **Import Workflow:**
   - File > Import KNIME Workflow
   - Select the workflow JSON file

## Data Categories

| Category | Description | Tables |
|----------|-------------|--------|
| RRA | Reserving Return Annual | 8 |
| RRQ | Reserving Return Quarterly | 4 |
| QSR | Quarterly Solvency Return | 6 |
| ASB | Annual Solvency Balance Sheet | 5 |
| LCR | Lloyd's Capital Return | 6 |
| SBF | Syndicate Business Forecast | 4 |
| QMA | Quarterly Monitoring | 4 |
| FSCS | Financial Services Compensation | 2 |
| Liquidity | Stress Testing | 4 |
| Claims | Claims Analysis | 4 |

## Usage Notes

- All data is synthetic for testing purposes
- Random seed is set to 42 for reproducibility
- Output tables are pandas DataFrames

## Support

For issues, please contact the Lloyd's Development Team.
"""
