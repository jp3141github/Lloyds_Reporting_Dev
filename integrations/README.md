# Lloyd's Reporting Integrations

Integration modules for connecting Lloyd's regulatory reporting data with external BI and analytics platforms.

## Supported Platforms

| Platform | Directory | Description |
|----------|-----------|-------------|
| Power BI | `powerbi/` | Microsoft Power BI Desktop and Service |
| KNIME | `knime/` | KNIME Analytics Platform |
| Shared | `shared/` | Common utilities for all integrations |

## Quick Start

### Power BI Integration

```python
from integrations.powerbi import PowerBIConnector

# Create connector
connector = PowerBIConnector()

# Generate all datasets
datasets = connector.generate_all_datasets()

# Export for Power BI
connector.export_for_powerbi('output/powerbi/')

# Generate standalone Python script for Power BI
from integrations.powerbi import ScriptBuilder
builder = ScriptBuilder()
script = builder.generate_full_script(['rra', 'qsr', 'lcr'])
```

### KNIME Integration

```python
from integrations.knime import KNIMEConnector, WorkflowBuilder, PythonNodeScripts

# Create connector
connector = KNIMEConnector()

# Generate datasets
datasets = connector.generate_all_datasets()

# Export for KNIME (ARFF format)
connector.export_for_knime('output/knime/')

# Build workflow configuration
workflow = WorkflowBuilder()
rra_workflow = workflow.build_rra_workflow()
workflow.export_workflow(rra_workflow, 'workflows/rra_analysis.json')

# Get Python scripts for KNIME nodes
scripts = PythonNodeScripts()
loader_script = scripts.get_data_loader_script('rra')
```

## Data Categories

Both integrations support all Lloyd's regulatory data categories:

| Category | Description | Tables |
|----------|-------------|--------|
| `rra` | Reserving Return Annual | 8 |
| `rrq` | Reserving Return Quarterly | 4 |
| `qsr` | Quarterly Solvency Return | 6 |
| `asb` | Annual Solvency Balance Sheet | 5 |
| `lcr` | Lloyd's Capital Return | 6 |
| `sbf` | Syndicate Business Forecast | 4 |
| `qma` | Quarterly Monitoring | 4 |
| `fscs` | Financial Services Compensation | 2 |
| `liquidity` | Liquidity Stress Testing | 4 |
| `claims` | Claims Development Analysis | 4 |

## Power BI Setup

### Method 1: Python Script Data Source

1. Open Power BI Desktop
2. Get Data > Python script
3. Paste the generated Python script
4. Click OK to import data

### Method 2: File Import

1. Run export: `connector.export_for_powerbi('output/')`
2. In Power BI: Get Data > Text/CSV
3. Select exported CSV files
4. Create relationships between tables

### Power BI Requirements

- Power BI Desktop (latest version)
- Python 3.9+ configured in Power BI
- Required packages: `pandas`, `numpy`, `openpyxl`

## KNIME Setup

### Method 1: Python Script Node

1. Open KNIME Analytics Platform
2. Add Python Script node to workflow
3. Configure Python environment
4. Paste script from `PythonNodeScripts`
5. Execute node

### Method 2: File Import

1. Run export: `connector.export_for_knime('output/')`
2. Use ARFF Reader or CSV Reader node
3. Connect to analysis nodes

### Method 3: Workflow Import

1. Generate workflow: `workflow.export_workflow(...)`
2. File > Import KNIME Workflow
3. Select generated JSON file

### KNIME Requirements

- KNIME Analytics Platform 5.2+
- KNIME Python Integration extension
- Python 3.9+ with pandas, numpy

## Shared Utilities

### DataConnector

Base class for data connections:

```python
from integrations.shared import DataConnector

connector = DataConnector(config={'random_seed': 42})
syndicates = connector.generate_syndicates(10)
years = connector.generate_years_of_account(5)
```

### DataValidator

Validate data quality:

```python
from integrations.shared import DataValidator

validator = DataValidator()
results = validator.validate(df, data_type='claims_data')

if validator.has_errors():
    print("Validation errors found!")
    print(validator.get_summary())
```

### ExportManager

Multi-format exports:

```python
from integrations.shared import ExportManager

exporter = ExportManager('output/')

# Single format
exporter.export_csv(df, 'claims_data')
exporter.export_excel(df, 'claims_data', format_header=True)

# Multiple formats
exporter.export_all_formats(df, 'claims_data', ['csv', 'excel', 'json'])

# Multi-sheet Excel
exporter.export_multi_sheet_excel(tables, 'regulatory_report')

# Platform-specific
exporter.export_for_powerbi(tables)
exporter.export_for_knime(tables)
```

## File Structure

```
integrations/
├── __init__.py
├── README.md
├── powerbi/
│   ├── __init__.py
│   ├── connector.py        # PowerBIConnector class
│   ├── dataset_generator.py # DatasetGenerator class
│   └── script_builder.py   # ScriptBuilder class
├── knime/
│   ├── __init__.py
│   ├── connector.py        # KNIMEConnector class
│   ├── workflow_builder.py # WorkflowBuilder class
│   └── python_nodes.py     # PythonNodeScripts class
└── shared/
    ├── __init__.py
    ├── data_connector.py   # DataConnector base class
    ├── validator.py        # DataValidator class
    └── export_manager.py   # ExportManager class
```

## Configuration

### Random Seed

All data generation uses seed 42 by default for reproducibility:

```python
connector = PowerBIConnector(config={'random_seed': 123})
```

### Custom Syndicates

```python
config = {
    'syndicates': [2987, 33, 1183],
    'base_year': 2024,
    'years_of_history': 10
}
connector = KNIMEConnector(config=config)
```

## Troubleshooting

### Import Errors

Ensure the repository root is in Python path:

```python
import sys
sys.path.insert(0, '/path/to/Lloyds_Reporting_Dev')
```

### Missing Dependencies

```bash
pip install pandas numpy openpyxl
```

### Power BI Python Path

1. File > Options and settings > Options
2. Python scripting
3. Set Python home directory to your Python installation

### KNIME Python Configuration

1. File > Preferences > KNIME > Python
2. Select Python 3 environment
3. Ensure pandas and numpy are installed
