# Tableau Validation Checklist

> **Status:** Publication gate only. The Tableau workbook, screenshots and Tableau Public link remain pending.

Use this checklist after generating `tableau/hr_attrition_tableau.csv` and building the worksheets in `TABLEAU_BUILD_GUIDE.md`. Do not mark the dashboard complete until every required item passes and the evidence is committed.

## 1. Source and model integrity

- [ ] Run `python3 scripts/prepare_tableau_data.py` successfully before opening Tableau.
- [ ] Connect only to `tableau/hr_attrition_tableau.csv`.
- [ ] Confirm the source contains 1,470 rows, 1,470 distinct `EmployeeNumber` values and 39 columns.
- [ ] Confirm the source checksum is `988ab632ae57bb334d70763035823f938e181d3724868dcd78da68b7da29f7a7`.
- [ ] Do not join SQLite aggregate views to the employee-level source; use them only for independent reconciliation.
- [ ] Confirm `Attrition Flag`, `Age Band`, `Tenure Band` and `Income Band` match the prepared source.

## 2. Opening reconciliation

Clear all filters and reconcile the workbook to these repository-validated checkpoints:

| Check | Expected |
|---|---:|
| Distinct employees | 1,470 |
| Attritions | 237 |
| Attrition rate | 16.12% |
| Average tenure | 7.01 years |
| Average monthly income | $6,502.93 |
| Overtime attrition rate | 30.53% |
| Non-overtime attrition rate | 10.44% |

- [ ] Employee count uses `COUNTD([Employee Number])`, not row count.
- [ ] Attritions use `SUM([Attrition Flag])`.
- [ ] Attrition rate divides attritions by distinct employees and handles an empty denominator.
- [ ] Currency and percentages use consistent precision across cards, labels and tooltips.
- [ ] Any mismatch blocks publication until the source, calculation or filter state is reconciled.

## 3. Filter and interaction tests

Test Department, Job Role, Age Band, Gender, Overtime, Business Travel and Tenure Band individually and in combination.

- [ ] Every KPI card updates to the selected population.
- [ ] Employees equal the sum of visible segment counts when categories are mutually exclusive.
- [ ] Attritions never exceed employees, and attrition rate remains between 0% and 100%.
- [ ] Empty selections show a clear no-data state rather than stale values or division errors.
- [ ] Reset returns all seven opening checkpoints exactly.
- [ ] Highlight actions do not silently change KPI denominators.
- [ ] Overall-rate reference lines use the documented filter behaviour and are labelled clearly.
- [ ] Ordered bands remain chronological or numeric, not alphabetical.

Record at least one single-filter and one combined-filter test with expected and observed employees, attritions and attrition rate.

## 4. Minimum-group and privacy tests

- [ ] The `Minimum Group Size` parameter defaults to 10.
- [ ] Segmented views suppress categories below the threshold.
- [ ] A visible note explains that suppression protects privacy and avoids unstable rates.
- [ ] Suppressed values cannot be recovered through tooltips, labels, drill-down, downloadable crosstabs or underlying-data views.
- [ ] `EmployeeNumber` is absent from worksheets, tooltips, dashboard text and downloads.
- [ ] No row-level employee table, identifiable profile or individual risk score is published.
- [ ] Cross-filter combinations are tested to ensure they cannot expose a group smaller than the threshold.

## 5. Responsible interpretation

- [ ] The dashboard states that the data is IBM's fictional sample.
- [ ] Overtime, role, department and demographic patterns are described as associations, not causes.
- [ ] Titles and annotations avoid language such as “driver,” “reason,” “high-risk employee” or “prediction.”
- [ ] Age and gender views include employee counts and are not framed as grounds for employment decisions.
- [ ] Recommendations focus on organisation-level investigation, workload design and anonymous qualitative evidence.
- [ ] A visible note prohibits use for hiring, promotion, performance or termination decisions.

## 6. Accessibility and layout

- [ ] Colour is not the only way attrition rate or selection state is communicated.
- [ ] Text and marks have sufficient contrast in the published theme.
- [ ] Every percentage is paired with a label, axis or tooltip.
- [ ] Worksheet titles and Tableau alt text state the measure and population.
- [ ] Keyboard reading order follows title, KPI cards, primary comparisons, supporting views, filters and notes.
- [ ] Desktop layout works near 1200 × 850 without horizontal scrolling.
- [ ] Phone layout preserves KPI context, reset control, suppression note and responsible-use note.
- [ ] Tooltips remain readable at 200% zoom and do not reveal employee-level detail.

## 7. Publication evidence

- [ ] Capture an unfiltered desktop screenshot showing the reconciled KPI cards.
- [ ] Capture a filtered screenshot demonstrating consistent KPIs and visible denominators.
- [ ] Capture a phone-layout screenshot.
- [ ] Save the workbook in `tableau/` only after all checks pass.
- [ ] Add screenshots to the repository with descriptive filenames and alt text in the README.
- [ ] Open the Tableau Public URL in a signed-out browser and repeat the privacy, filter and accessibility checks.
- [ ] Add the verified public link to the README, GitHub portfolio and Notion only after publication succeeds.

## Sign-off

Record the workbook version, validation date, source checksum and any accepted limitations alongside the screenshots. If any required item is unchecked, keep the project and both portfolio surfaces marked **Tableau pending**.
