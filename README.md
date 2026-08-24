# HR Analytics – Attrition & Workforce Insights

> **Status:** Validated data and executable SQLite analysis complete · Tableau dashboard in progress

## Overview

This project explores workforce composition and attrition patterns using IBM’s fictional HR Analytics sample. It identifies organisation-level areas for further investigation while avoiding inappropriate individual prediction or employment decisions.

**Dataset:** [IBM HR Analytics Employee Attrition & Performance](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)

## Key KPIs

| Metric | Result |
|---|---:|
| Employees | 1,470 |
| Attritions | 237 |
| Attrition rate | 16.12% |
| Average tenure | 7.01 years |
| Average monthly income | $6,502.93 |

## Analysis completed

- Confirmed one unique employee number per record.
- Converted Attrition to a binary Attrition Flag.
- Validated age, income, tenure and satisfaction ranges.
- Created age, tenure and income bands.
- Reconciled workforce and attrition totals across each segment.
- Compared job role, department, overtime, tenure, age, income and business travel.

## Repository contents

- [`data/`](data/) — cleaned data with source and validation notes
- [`sql/`](sql/) — executable SQLite schema, aggregate workforce views and run guide
- [`scripts/build_database.py`](scripts/build_database.py) — standard-library loader that rebuilds and validates `project.db`
- [`tableau/`](tableau/) — build guide; workbook and screenshots are still pending

## Tableau dashboard — in progress

Planned views:

- Attrition rate and employee count by job role
- Overtime and department comparisons
- Tenure-band attrition curve
- Business-travel comparison
- Age- and income-band views
- Interactive workforce filters

## Key insights

- Overall attrition was **16.12%**.
- Overtime employees had **30.53% attrition**, compared with **10.44%** without overtime.
- Sales Representative had the highest observed job-role rate.
- Sales had the highest observed department rate.

## Repository roadmap

- [x] Business problem and KPI definition
- [x] Cleaning and feature-engineering approach
- [x] SQL analysis documented
- [x] Responsible-use boundaries documented
- [x] Add cleaned data with source and validation notes
- [x] Add reproducible SQLite database loader
- [ ] Add reproducible preparation code
- [x] Add complete SQL schema and analysis views
- [ ] Build and publish Tableau dashboard
- [ ] Add dashboard screenshots and Tableau Public link

## Responsible interpretation

This is fictional sample data. Results are descriptive associations, not causal findings, and must not be used for individual hiring, promotion, performance or termination decisions.
