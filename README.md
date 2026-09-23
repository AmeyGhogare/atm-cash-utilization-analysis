# 🏧 ATM Cash Utilization & Downtime Analysis

## 📌 Project Overview

**ATM Cash Utilization & Downtime Analysis** is an end-to-end Data Analytics project focused on analyzing ATM cash utilization, withdrawal patterns, cash demand, operational factors, and potential cash-availability risks.

The project uses Python for data cleaning and exploratory data analysis, MySQL for structured data storage and SQL-based analysis, and Microsoft Power BI for interactive dashboard development.

The objective is to transform raw ATM transaction and operational data into meaningful business insights that can help identify high-demand ATMs, understand cash utilization patterns, analyze location and time-based behavior, and identify records associated with potential cash-availability risk.

> **Important:** The provided dataset does not contain an actual ATM downtime/outage column. Therefore, this project does **not** measure actual ATM downtime. Instead, it uses a `Cash_Risk` indicator to identify records that may represent potential cash-availability risk.

---

# 🎯 Business Problem

ATMs need to maintain sufficient cash availability to meet customer demand.

Insufficient cash can potentially result in:

- Cash shortages
- Increased operational risk
- Poor customer experience
- Emergency cash replenishment
- Inefficient cash management
- Higher operational costs

At the same time, keeping excessive cash inside ATMs can also result in inefficient utilization of available funds.

This project analyzes historical ATM data to answer questions such as:

- Which ATMs have the highest withdrawal activity?
- Which locations experience higher cash demand?
- How does cash demand change over time?
- Which time periods generate the most ATM activity?
- How does previous-day cash level relate to next-day demand?
- Which ATMs or records show higher potential cash-availability risk?
- How does cash utilization vary across ATM locations?
- How do holidays, special events, weather, and competitors affect ATM activity?

---

# 🎯 Project Objectives

The major objectives of the project are:

1. Clean and prepare ATM data for analysis.
2. Perform Exploratory Data Analysis using Python.
3. Analyze withdrawal and deposit patterns.
4. Analyze ATM activity by location and time.
5. Analyze monthly and yearly cash-demand trends.
6. Study the relationship between previous-day cash level and next-day demand.
7. Identify high-demand ATM records.
8. Identify potential cash-availability risk.
9. Store and analyze the cleaned data using MySQL.
10. Perform SQL-based business analysis.
11. Build interactive Power BI dashboards.
12. Generate analytical reports.
13. Study relevant research papers related to ATM cash management and Power BI analytics.

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data cleaning, analysis and visualization |
| Pandas | Data manipulation and EDA |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| MySQL | Database storage and SQL analysis |
| MySQL Workbench | Database management |
| Power BI | Interactive dashboard development |
| DAX | Power BI calculations |
| ReportLab | Automated PDF report generation |
| Jupyter Notebook | EDA and analysis |
| VS Code | Project development |
| Git & GitHub | Version control and project hosting |

---

# 📂 Project Structure

```text
ATM_CASH_UTILIZATION_DOWNTIME_ANALYSIS/
│
├── .env
├── .gitignore
├── README.md
│
├── data/
│   ├── raw/
│   │   └── original_dataset.csv
│   │
│   └── processed/
│       └── atm_cleaned.csv
│
├── notebooks/
│   └── ATM_Cash_Utilization_Downtime_Analysis.ipynb
│
├── outputs/
│   ├── charts/
│   │   └── generated_visualizations
│   │
│   └── reports/
│       ├── ATM_Project_Report.pdf
│       ├── Business_Insights.pdf
│       └── Executive_Summary.pdf
│
├── powerbi/
│   └── ATM_Cash_Utilization_Analytics.pbix
│
├── researchers_papers/
│   ├── Research_Paper_1_ATM_Cash_Management_Summary.pdf
│   └── Research_Paper_2_PowerBI_Analytics_Summary.pdf
│
├── sql/
│   └── atm_analysis.sql
│
└── src/
    ├── data_cleaning.py
    ├── visualization.py
    ├── database.py
    └── report.py
