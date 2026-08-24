# Data

## File

`hr_attrition_clean.csv` contains 1,470 fictional employee records and 39 columns.

## Source

- Dataset: IBM HR Analytics Employee Attrition & Performance
- URL: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
- Original file: `WA_Fn-UseC_-HR-Employee-Attrition.csv`
- Content: fictional data created by IBM data scientists

## Preparation

The original 35 fields were retained. `Attrition Flag`, `Age Band`, `Tenure Band` and `Income Band` were added for aggregate analysis. Employee Number remains an anonymous source identifier and must not be exposed in dashboard detail.

## Validation

| Check | Result |
|---|---:|
| Employees | 1,470 |
| Attritions | 237 |
| Attrition rate | 16.12% |
| Average tenure | 7.01 years |
| Average monthly income | $6,502.93 |

SHA-256: `988ab632ae57bb334d70763035823f938e181d3724868dcd78da68b7da29f7a7`
