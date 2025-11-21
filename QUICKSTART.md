# 🚀 Quick Start Guide
## Lloyd's RRA Premium Processing

Get up and running with RRA premium processing in **5 minutes**!

---

## ⚡ Super Quick Start (Python)

### 1. Install Dependencies
```bash
pip install pandas numpy openpyxl
```

### 2. Test with Synthetic Data
```bash
cd Lloyds_Reporting_Dev
python python_scripts/rra_premium_processing.py
```

**Expected Output:**
- 7 RRA output tables generated
- Excel file created: `synthetic_data/rra_premium_outputs.xlsx`
- Console summary showing data statistics

✅ **If this works, you're ready to use your own data!**

---

## 📊 Use in Power BI (Python - 3 Steps)

### Step 1: Configure Python
1. Open Power BI Desktop
2. **File** → **Options** → **Python scripting**
3. Set Python home directory (e.g., `C:\Python39`)
4. Click **OK**

### Step 2: Load Data
1. **Get Data** → **Text/CSV**
2. Select your premium data CSV
3. Load

### Step 3: Create Visual
1. Add **Python visual** to report
2. Drag these fields to the visual:
   - Syndicate Number
   - YOA
   - Gross Annual Premium in Period
3. Paste this code:
```python
import matplotlib.pyplot as plt

summary = dataset.groupby(['Syndicate Number', 'YOA'])['Gross Annual Premium in Period'].sum().reset_index()

plt.figure(figsize=(10, 6))
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

**Done!** 🎉

---

## 📈 Use in Power BI (R - 3 Steps)

### Step 1: Configure R
1. Install R from [r-project.org](https://www.r-project.org/)
2. Open R console and run:
```r
install.packages(c("dplyr", "ggplot2", "readr"))
```
3. In Power BI: **File** → **Options** → **R scripting** → Set R home directory

### Step 2: Load Data
1. **Get Data** → **Text/CSV**
2. Select your premium data CSV
3. Load

### Step 3: Create Visual
1. Add **R visual** to report
2. Drag fields to the visual (same as Python)
3. Paste this code:
```r
library(ggplot2)
library(dplyr)

summary_data <- dataset %>%
  group_by(`Syndicate Number`, YOA) %>%
  summarise(Total_Premium = sum(`Gross Annual Premium in Period`), .groups = 'drop')

ggplot(summary_data, aes(x = YOA, y = Total_Premium, color = factor(`Syndicate Number`))) +
  geom_line(size = 1.2) +
  geom_point(size = 3) +
  labs(title = "Premium Trends by Syndicate", x = "Year of Account", y = "Total Premium (£)", color = "Syndicate") +
  theme_minimal()
```

**Done!** 🎉

---

## 🎯 Using Your Own Data

### Required Columns
Your CSV/Excel must have these columns:
```
Syndicate Number
UMR
Insured Country
Risk Location
Insured Name
Insured - Policyholder Type
Risk Code
Risk / Certificate Reference
Original Currency
Sum Insured
Gross Annual Premium in Period
YOA
Part VII Indicator
Original Signing Number
Original Signing Date
```

### Quick Test
```python
import pandas as pd
from rra_premium_processing import RRAPremiumProcessor

# Load your data
data = pd.read_csv('your_data.csv')

# Process
processor = RRAPremiumProcessor(data)
outputs = processor.generate_all_outputs()

# Export
processor.export_to_excel('my_rra_outputs.xlsx')
```

---

## 📁 What You Get

After processing, you'll have **7 output tables**:

| Table | Description | Use Case |
|-------|-------------|----------|
| **Premium Summary By Syndicate** | Aggregated totals by syndicate & year | Executive KPIs |
| **Premium By Risk Code** | Breakdown by risk classification | Risk analysis |
| **Geographic Analysis** | Country-level breakdown with market share | Geographic exposure |
| **Policyholder Type Analysis** | Retail vs Business segmentation | Customer segmentation |
| **Currency Analysis** | Currency exposure breakdown | FX risk |
| **Part VII Analysis** | Part VII transfer tracking | Regulatory reporting |
| **Detailed Risk Register** | Full risk-level data with calculations | Detailed analysis |

---

## 🎨 Quick Visualizations

### Python - Premium Heatmap
```python
import seaborn as sns
import matplotlib.pyplot as plt

pivot = dataset.pivot_table(
    values='Gross Annual Premium in Period',
    index='Risk Code',
    columns='YOA',
    aggfunc='sum'
)

plt.figure(figsize=(10, 8))
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd')
plt.title('Premium Heatmap: Risk Code vs Year')
plt.show()
```

### R - Interactive Plot
```r
library(ggplot2)

ggplot(dataset, aes(x = YOA, y = `Gross Annual Premium in Period`, fill = `Insured - Policyholder Type`)) +
  geom_bar(stat = 'identity') +
  facet_wrap(~ `Syndicate Number`) +
  theme_minimal() +
  labs(title = 'Premium by Policyholder Type', x = 'Year', y = 'Premium', fill = 'Type')
```

---

## 🐛 Troubleshooting

### "Python script error"
**Fix:** Check Python path in Power BI Options → Python scripting

### "Module pandas not found"
**Fix:** Run `pip install pandas` in command prompt

### "Cannot find file"
**Fix:** Use absolute paths:
- ❌ `data/file.csv`
- ✅ `C:/Users/YourName/Documents/data/file.csv`

### Script runs but no visual appears
**Fix:** Add `plt.show()` at the end of Python scripts

### "Object dataset not found"
**Fix:** Don't rename the `dataset` variable in Python/R visuals

---

## 📚 Next Steps

1. ✅ **Test with synthetic data** (you are here)
2. 📊 **Load your own data**
3. 🎨 **Create basic visuals**
4. 📈 **Build complete dashboard** (see POWER_BI_GUIDE.md)
5. 🚀 **Deploy to production**

---

## 💡 Pro Tips

### Tip 1: Use Parameters
Create parameters in Power BI for file paths - easy to switch between dev/prod

### Tip 2: Test Scripts Outside Power BI First
Run Python/R scripts standalone before using in Power BI - faster debugging

### Tip 3: Start Simple
Begin with one visual, then add complexity

### Tip 4: Use Filters
Apply filters in Power Query before Python/R scripts - better performance

### Tip 5: Save Often
Power BI can crash with bad Python/R code - save your work!

---

## 🎓 Common Use Cases

### Case 1: Monthly Premium Report
```python
processor = RRAPremiumProcessor(dataset)
summary = processor.create_premium_summary_by_syndicate()
# Filter for current month
current_month = summary[summary['YOA'] == 2024]
```

### Case 2: Risk Concentration Analysis
```python
risk_analysis = processor.create_premium_by_risk_code()
top_risks = risk_analysis.nlargest(10, 'Total Premium')
```

### Case 3: Geographic Exposure
```python
geo = processor.create_geographic_analysis()
# Focus on top 5 countries
top_countries = geo.nlargest(5, 'Total Premium')
```

---

## ✅ Validation Checklist

Before using in production:

- [ ] Script runs successfully with synthetic data
- [ ] All required columns present in your data
- [ ] Output tables contain expected data
- [ ] Visuals render correctly
- [ ] No error messages
- [ ] Performance is acceptable
- [ ] Numbers match expected totals

---

## 🆘 Need Help?

1. **Check** README.md for detailed documentation
2. **Read** POWER_BI_GUIDE.md for step-by-step Power BI instructions
3. **Review** error messages - they usually tell you what's wrong
4. **Test** scripts standalone before Power BI integration

---

## 🎯 Success Metrics

After setup, you should be able to:

✅ Generate 7 RRA output tables in **< 5 seconds**
✅ Create visuals in Power BI in **< 2 minutes**
✅ Process **1,000+ premium records** without errors
✅ Refresh reports **automatically** on schedule

---

**You're ready to go!** 🚀

For detailed documentation, see:
- **README.md** - Full documentation
- **POWER_BI_GUIDE.md** - Power BI integration guide

---

**Questions?** Check the Troubleshooting section above or review the full documentation.
