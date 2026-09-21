# ATM Cash Utilization & Downtime Analysis

## Project Overview
Analyze ATM cash withdrawal patterns and downtime events to understand
cash utilization efficiency, predict cash-out risk, and identify the
main drivers of ATM downtime across regions and location types.

## Dataset
`atm_cash_utilization_downtime.csv` — a synthetic dataset covering:
- 40 ATMs across 5 regions and 8 cities
- 365 days (2025), 14,600 total records
- Daily transaction count, cash withdrawn, cash remaining, cash capacity
- Status (Active/Down), downtime duration, and downtime reason
- Weekday/weekend and seasonal demand patterns (salary days, festive season)

Regenerate or customize it with `generate_atm_dataset.py` (edit the
constants at the top: number of ATMs, date range, downtime-rate tuning).

## Planned Analysis
- **SQL**: cash utilization by region/location type, downtime frequency
  and duration by ATM, cash-out risk patterns, high-downtime ATM ranking
- **Pandas**: cleaning, feature engineering, cash-out risk classification,
  correlation between utilization and downtime, time-series trends
- **Power BI / Dashboard**: KPI cards (uptime %, total cash dispensed,
  downtime hours), downtime-reason breakdown, regional heatmaps

## Project Structure
```
.
├── atm_cash_utilization_downtime.csv   # dataset
├── generate_atm_dataset.py             # dataset generator (synthetic data)
└── README.md
```

## Status
🚧 In progress — dataset generated, analysis scripts coming next.
