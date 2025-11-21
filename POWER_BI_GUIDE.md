# Power BI Integration Guide
## RRA Premium Processing Scripts

This guide provides step-by-step instructions for integrating the Python and R scripts into Power BI for Lloyd's RRA reporting.

---

## 🎯 Quick Start

### Option 1: Python (Recommended)
Best for: Fast processing, easy installation, wide compatibility

### Option 2: R
Best for: Advanced statistical analysis, ggplot2 visualizations

---

## 📥 Data Import Methods

### Method A: Direct CSV Import
1. Open Power BI Desktop
2. Get Data → Text/CSV
3. Select `synthetic_lloyds_premium_data.csv`
4. Load data

### Method B: Excel Import
1. Get Data → Excel
2. Select `synthetic_lloyds_premium_data.xlsx`
3. Choose "Premium Data" sheet
4. Load data

### Method C: Database Connection
1. Get Data → SQL Server / Other database
2. Connect to your Lloyd's data warehouse
3. Write query to extract premium data with required columns

---

## 🐍 Python Integration - Detailed Steps

### Step 1: Enable Python in Power BI

1. **Install Python**
   ```bash
   # Windows
   Download from https://www.python.org/downloads/
   During installation, check "Add Python to PATH"

   # Verify installation
   python --version
   ```

2. **Install Required Packages**
   ```bash
   pip install pandas numpy openpyxl
   ```

3. **Configure Power BI**
   - Open Power BI Desktop
   - File → Options and settings → Options
   - Python scripting
   - Set "Python home directory" to your Python installation
   - Set "Python IDE" (optional) to your preferred IDE

### Step 2: Import Data with Python Script

1. **Get Data → More → Python script**

2. **Enter the following script:**
   ```python
   import pandas as pd

   # Load your premium data
   premium_data = pd.read_csv(r'C:\path\to\synthetic_lloyds_premium_data.csv')

   # Display for Power BI to import
   print(premium_data.head())
   ```

3. **Click OK** - Power BI will detect the `premium_data` table

4. **Select the table** and click Load

### Step 3: Transform Data with Python

1. **Transform Data** → Enter Power Query Editor

2. **Add Column → Run Python Script**

3. **Use the RRA processing script:**
   ```python
   import sys
   sys.path.append(r'C:\path\to\Lloyds_Reporting_Dev\python_scripts')

   from rra_premium_processing import RRAPremiumProcessor

   # Process the data
   processor = RRAPremiumProcessor(dataset)

   # Generate outputs (choose one or more)
   Premium_Summary = processor.create_premium_summary_by_syndicate()
   Geographic_Analysis = processor.create_geographic_analysis()
   Risk_Code_Analysis = processor.create_premium_by_risk_code()
   Policyholder_Analysis = processor.create_policyholder_type_analysis()
   ```

4. **Expand the output tables** by clicking the expand icon

5. **Close & Apply**

### Step 4: Create Python Visuals

1. **Add Python Visual** to your report page

2. **Add fields** to the Python visual (drag from Fields pane)

3. **Enter visualization script:**
   ```python
   import matplotlib.pyplot as plt
   import pandas as pd

   # dataset is automatically provided by Power BI
   # Aggregate data
   summary = dataset.groupby(['Syndicate Number', 'YOA'])['Gross Annual Premium in Period'].sum().reset_index()

   # Create visualization
   plt.figure(figsize=(12, 6))
   for syndicate in summary['Syndicate Number'].unique():
       data = summary[summary['Syndicate Number'] == syndicate]
       plt.plot(data['YOA'], data['Gross Annual Premium in Period'], marker='o', label=f'Syndicate {syndicate}')

   plt.xlabel('Year of Account')
   plt.ylabel('Total Premium (£)')
   plt.title('Premium Trends by Syndicate')
   plt.legend()
   plt.grid(True, alpha=0.3)
   plt.show()
   ```

4. **Run** - The visual will display

### Step 5: Advanced - Create Custom Functions

1. **Transform Data** → New Source → Blank Query

2. **Advanced Editor** → Paste:
   ```
   let
       ProcessPremiumData = (InputData as table) =>
       let
           Script = "
   import sys
   sys.path.append(r'C:\path\to\python_scripts')
   from rra_premium_processing import RRAPremiumProcessor

   processor = RRAPremiumProcessor(dataset)
   result = processor.create_premium_summary_by_syndicate()
   ",
           Result = Python.Execute(Script, [dataset = InputData])
       in
           Result
   in
       ProcessPremiumData
   ```

3. **Invoke this function** on any premium data table

---

## 📊 R Integration - Detailed Steps

### Step 1: Enable R in Power BI

1. **Install R**
   ```bash
   # Download from https://cran.r-project.org/
   # Windows: Download and run the installer
   # Mac: Download .pkg file

   # Verify installation
   R --version
   ```

2. **Install Required Packages**
   ```r
   install.packages(c("dplyr", "tidyr", "readr", "writexl", "lubridate", "ggplot2"))
   ```

3. **Configure Power BI**
   - File → Options and settings → Options
   - R scripting
   - Set "R home directory" (usually auto-detected)
   - Set "R IDE" to RStudio if installed

### Step 2: Import Data with R Script

1. **Get Data → More → R script**

2. **Enter the following script:**
   ```r
   library(readr)

   # Load premium data
   premium_data <- read_csv('C:/path/to/synthetic_lloyds_premium_data.csv')
   ```

3. **Click OK** - Power BI will detect the table

4. **Select the table** and click Load

### Step 3: Transform Data with R

1. **Transform Data** → Enter Power Query Editor

2. **Transform → Run R Script**

3. **Use the RRA processing script:**
   ```r
   source('C:/path/to/Lloyds_Reporting_Dev/r_scripts/rra_premium_processing.R')

   # Generate outputs
   Premium_Summary <- create_premium_summary_by_syndicate(dataset)
   Geographic_Analysis <- create_geographic_analysis(dataset)
   Risk_Code_Analysis <- create_premium_by_risk_code(dataset)
   ```

4. **Expand the output tables**

5. **Close & Apply**

### Step 4: Create R Visuals

1. **Add R Visual** to your report page

2. **Add fields** to the R visual

3. **Enter visualization script:**
   ```r
   library(ggplot2)
   library(dplyr)

   # Aggregate data
   summary_data <- dataset %>%
     group_by(`Syndicate Number`, YOA) %>%
     summarise(Total_Premium = sum(`Gross Annual Premium in Period`), .groups = 'drop')

   # Create visualization
   ggplot(summary_data, aes(x = YOA, y = Total_Premium, color = factor(`Syndicate Number`))) +
     geom_line(size = 1.2) +
     geom_point(size = 3) +
     scale_y_continuous(labels = scales::comma) +
     labs(
       title = "Premium Trends by Syndicate",
       x = "Year of Account",
       y = "Total Premium (£)",
       color = "Syndicate"
     ) +
     theme_minimal() +
     theme(plot.title = element_text(hjust = 0.5, size = 14, face = "bold"))
   ```

4. **Run** - The visual will display

---

## 📋 Pre-built Dashboard Templates

### Template 1: Executive Summary Dashboard

**Visuals to Create:**

1. **KPI Cards**
   - Total Premium (current year)
   - Number of Policies
   - Number of Syndicates
   - Average Premium

2. **Premium Trend Line Chart** (Python/R visual)
   - X-axis: YOA
   - Y-axis: Total Premium
   - Legend: Syndicate Number

3. **Geographic Heat Map**
   - Use Power BI Map visual
   - Location: Insured Country
   - Size: Total Premium

4. **Risk Code Distribution** (Donut Chart)
   - Legend: Risk Code
   - Values: Count of policies

5. **Policyholder Type Breakdown** (Stacked Bar)
   - Axis: Policyholder Type
   - Values: Total Premium
   - Legend: YOA

### Template 2: Risk Analysis Dashboard

**Python Visual Example:**
```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Risk concentration analysis
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Premium by Risk Code
ax1 = axes[0, 0]
risk_premium = dataset.groupby('Risk Code')['Gross Annual Premium in Period'].sum().sort_values(ascending=False).head(10)
risk_premium.plot(kind='barh', ax=ax1, color='steelblue')
ax1.set_title('Top 10 Risk Codes by Premium')
ax1.set_xlabel('Total Premium (£)')

# 2. Geographic Concentration
ax2 = axes[0, 1]
geo_premium = dataset.groupby('Insured Country')['Gross Annual Premium in Period'].sum().sort_values(ascending=False).head(10)
geo_premium.plot(kind='bar', ax=ax2, color='coral')
ax2.set_title('Top 10 Countries by Premium')
ax2.set_ylabel('Total Premium (£)')
ax2.tick_params(axis='x', rotation=45)

# 3. Premium Distribution
ax3 = axes[1, 0]
dataset['Gross Annual Premium in Period'].hist(bins=50, ax=ax3, color='lightgreen', edgecolor='black')
ax3.set_title('Premium Distribution')
ax3.set_xlabel('Premium Amount (£)')
ax3.set_ylabel('Frequency')

# 4. Currency Exposure
ax4 = axes[1, 1]
currency_counts = dataset['Original Currency'].value_counts()
ax4.pie(currency_counts, labels=currency_counts.index, autopct='%1.1f%%', startangle=90)
ax4.set_title('Currency Exposure')

plt.tight_layout()
plt.show()
```

### Template 3: Syndicate Performance Dashboard

**R Visual Example:**
```r
library(ggplot2)
library(dplyr)
library(gridExtra)

# Prepare data
syndicate_summary <- dataset %>%
  group_by(`Syndicate Number`, YOA) %>%
  summarise(
    Total_Premium = sum(`Gross Annual Premium in Period`),
    Avg_Premium = mean(`Gross Annual Premium in Period`),
    Policy_Count = n(),
    .groups = 'drop'
  )

# 1. Premium Growth
p1 <- ggplot(syndicate_summary, aes(x = YOA, y = Total_Premium, fill = factor(`Syndicate Number`))) +
  geom_bar(stat = 'identity', position = 'dodge') +
  scale_fill_brewer(palette = 'Set3') +
  labs(title = 'Premium by Syndicate and Year', x = 'Year', y = 'Total Premium', fill = 'Syndicate') +
  theme_minimal()

# 2. Policy Count Trend
p2 <- ggplot(syndicate_summary, aes(x = YOA, y = Policy_Count, color = factor(`Syndicate Number`))) +
  geom_line(size = 1) +
  geom_point(size = 2) +
  labs(title = 'Policy Count Trends', x = 'Year', y = 'Number of Policies', color = 'Syndicate') +
  theme_minimal()

# Display
grid.arrange(p1, p2, ncol = 1)
```

---

## 🔄 Scheduled Refresh Setup

### For Python Scripts

1. **Save your PBIX file**

2. **Publish to Power BI Service**
   - File → Publish → Select workspace

3. **Configure Data Source Credentials**
   - In Power BI Service, go to Settings → Datasets
   - Edit credentials for Python data source
   - Enter path to Python executable

4. **Schedule Refresh**
   - Settings → Schedule refresh
   - Set frequency (daily/weekly)
   - Set time

**Note**: Python scripts in Power BI Service require:
- Power BI Premium
- Python packages installed on the gateway machine

### For R Scripts

Same process as Python, but:
- Configure R home directory in gateway
- Ensure R packages are installed on gateway machine

---

## 🎨 Visualization Best Practices

### 1. Color Scheme
Use Lloyd's brand colors:
- Primary: Navy Blue (#003057)
- Secondary: Green (#00A758)
- Accent: Gold (#FFB81C)

```python
# Python color palette
lloyds_colors = ['#003057', '#00A758', '#FFB81C', '#8B8C89', '#E87722']
```

```r
# R color palette
lloyds_colors <- c("#003057", "#00A758", "#FFB81C", "#8B8C89", "#E87722")
```

### 2. Number Formatting

**Python:**
```python
# Format as currency
dataset['Formatted Premium'] = dataset['Gross Annual Premium in Period'].apply(lambda x: f'£{x:,.2f}')

# Format as percentage
dataset['Premium Share %'] = (dataset['Premium'] / dataset['Premium'].sum() * 100).round(2)
```

**R:**
```r
# Format as currency
library(scales)
dataset$`Formatted Premium` <- dollar(dataset$`Gross Annual Premium in Period`, prefix = "£")

# Format as percentage
dataset$`Premium Share %` <- percent(dataset$Premium / sum(dataset$Premium), accuracy = 0.01)
```

### 3. Responsive Design
- Use bookmarks for different views
- Create mobile layouts
- Use drill-through for detailed analysis

---

## 🐛 Troubleshooting

### Python Issues

**Error: "Python script execution error"**
- Solution: Check Python path in Options → Python scripting
- Verify packages are installed: `pip list`

**Error: "Module not found"**
- Solution: Ensure script path is correct in `sys.path.append()`
- Use absolute paths, not relative

**Error: "Dataset variable not found"**
- Solution: In Power BI Python scripts, the input is always called `dataset`
- Don't rename this variable

### R Issues

**Error: "R script execution error"**
- Solution: Check R home directory in Options → R scripting
- Verify packages: `installed.packages()`

**Error: "Cannot find function"**
- Solution: Source the RRA script before using functions
- Check that script path is correct

**Error: "Object 'dataset' not found"**
- Solution: Use `dataset` as the input variable name in R visuals

### Performance Issues

**Slow refresh times:**
- Reduce data volume with filters
- Use data aggregation in Power Query
- Consider DirectQuery instead of Import

**Python/R script timeout:**
- Optimize scripts for performance
- Process data in chunks
- Use Power Query for heavy transformations

---

## 📊 Sample DAX Measures

Enhance your reports with these DAX measures:

```dax
// Total Premium
Total Premium = SUM('Premium Data'[Gross Annual Premium in Period])

// Premium Growth YoY
Premium Growth % =
VAR CurrentYearPremium = [Total Premium]
VAR PreviousYearPremium = CALCULATE([Total Premium], DATEADD('Date'[Date], -1, YEAR))
RETURN
DIVIDE(CurrentYearPremium - PreviousYearPremium, PreviousYearPremium, 0)

// Average Premium per Policy
Avg Premium = AVERAGE('Premium Data'[Gross Annual Premium in Period])

// Policy Count
Policy Count = COUNTROWS('Premium Data')

// Large Risk Count
Large Risks = COUNTROWS(FILTER('Premium Data', 'Premium Data'[Gross Annual Premium in Period] > 500000))

// Market Share by Syndicate
Syndicate Market Share =
DIVIDE(
    [Total Premium],
    CALCULATE([Total Premium], ALLSELECTED('Premium Data'[Syndicate Number])),
    0
)
```

---

## 📈 Performance Optimization Tips

1. **Use Query Folding**
   - Apply filters in Power Query before Python/R scripts
   - Reduces data volume processed by scripts

2. **Aggregate Early**
   - Summarize data before complex calculations
   - Use Power Query aggregation when possible

3. **Limit Visual Refreshes**
   - Use bookmarks to control which visuals refresh
   - Disable auto-refresh during development

4. **Optimize Scripts**
   - Use vectorized operations (pandas/dplyr)
   - Avoid loops when possible
   - Cache intermediate results

5. **Use Parameters**
   - Create parameters for file paths
   - Easy to switch between dev/prod environments

---

## 🎓 Learning Resources

### Power BI with Python
- [Microsoft: Python in Power BI](https://docs.microsoft.com/power-bi/connect-data/desktop-python-scripts)
- [Python Visualizations in Power BI](https://docs.microsoft.com/power-bi/create-reports/desktop-python-visuals)

### Power BI with R
- [Microsoft: R in Power BI](https://docs.microsoft.com/power-bi/connect-data/service-r-packages-support)
- [R Visualizations in Power BI](https://docs.microsoft.com/power-bi/create-reports/desktop-r-visuals)

### Lloyd's Reporting
- Lloyd's Performance Management Portal
- Solvency II Reporting Guidelines
- Lloyd's Market Reporting Documentation

---

## ✅ Checklist for Production Deployment

- [ ] Python/R environment configured in Power BI
- [ ] All required packages installed
- [ ] Scripts tested with sample data
- [ ] File paths updated for production
- [ ] Data source credentials configured
- [ ] Scheduled refresh tested
- [ ] Visuals rendering correctly
- [ ] Performance acceptable (<30s refresh)
- [ ] Error handling implemented
- [ ] Documentation updated
- [ ] User training completed

---

## 📞 Support

For technical issues:
1. Check this guide first
2. Review error messages carefully
3. Test scripts standalone before Power BI integration
4. Consult Power BI community forums

For Lloyd's reporting questions:
- Contact your managing agent
- Refer to Lloyd's Market Reporting team

---

**Last Updated**: November 2025
**Compatible with**: Power BI Desktop (Latest version)
