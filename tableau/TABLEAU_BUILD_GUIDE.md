# Tableau Dashboard Build Guide

> **Status:** Build specification only. The Tableau workbook, screenshots and Tableau Public link are not yet published.

## Purpose

Build an organisation-level dashboard that helps an HR audience explore where attrition is concentrated in IBM's fictional employee sample. The dashboard must present descriptive patterns, not predict an individual's behaviour or recommend employment actions.

## Source and required fields

Use the cleaned one-row-per-employee dataset described in the project README. The prepared source should include:

- `Employee Number` — unique employee identifier
- `Attrition Flag` — 1 for attrition and 0 otherwise
- `Age`, `Monthly Income` and `Years at Company`
- `Department`, `Job Role`, `Gender`, `Overtime` and `Business Travel`
- `Age Band`, `Income Band` and `Tenure Band`

Keep the dashboard at aggregate level. Do not expose employee identifiers in worksheets, tooltips or downloadable detail.

## Validation gate

Before designing charts, reproduce these README checkpoints in Tableau:

| Check | Expected value |
|---|---:|
| Distinct employees | 1,470 |
| Attritions | 237 |
| Attrition rate | 16.12% |
| Average tenure | 7.01 years |
| Average monthly income | $6,502.93 |
| Overtime attrition rate | 30.53% |
| Non-overtime attrition rate | 10.44% |

Stop and reconcile the prepared data if any value differs. Common causes are duplicated employees, null identifiers, an incorrectly mapped attrition flag or filters applied before validation.

## Calculated fields

Adjust field names only if the cleaned source uses a different naming convention.

### Employees

```text
COUNTD([Employee Number])
```

### Attritions

```text
SUM([Attrition Flag])
```

### Attrition Rate

```text
IF COUNTD([Employee Number]) = 0 THEN 0
ELSE SUM([Attrition Flag]) / COUNTD([Employee Number])
END
```

Format as a percentage with two decimal places.

### Minimum group size

Create an integer parameter named `Minimum Group Size` with a default value of 10. Then create:

```text
COUNTD([Employee Number]) >= [Minimum Group Size]
```

Place this Boolean field on Filters and keep `True` for segmented views. This avoids presenting unstable rates for very small groups; retain the employee-count mark so viewers can judge context.

## Worksheets

### 1. KPI summary

Show Employees, Attritions, Attrition Rate, average Years at Company and average Monthly Income. Use concise labels and include a subtitle stating that the data is a fictional IBM sample.

### 2. Attrition by job role

- Rows: `Job Role`
- Columns: `Attrition Rate`
- Label: `Employees`
- Filter: minimum group size
- Sort: descending attrition rate

Use a reference line for the overall 16.12% rate. The employee count should remain visible so a high percentage is not interpreted without its denominator.

### 3. Overtime comparison

- Columns: `Overtime`
- Rows: `Attrition Rate`
- Label: attrition rate and employees
- Expected validation: 30.53% for overtime and 10.44% without overtime

Describe this as an association. Do not state that overtime caused attrition.

### 4. Department comparison

Show attrition rate and employee count by `Department`, sorted by rate. Add the overall-rate reference line and minimum-group-size filter.

### 5. Tenure pattern

- Columns: ordered `Tenure Band`
- Rows: `Attrition Rate`
- Label or tooltip: employees and attritions
- Mark: line with visible points

Use the explicit band order from the prepared data rather than alphabetical sorting.

### 6. Business travel

Compare attrition rate and employee count by `Business Travel`. Keep category labels fully visible and avoid abbreviations that may be unclear.

### 7. Workforce profile

Use separate age-band and income-band views. Display the rate together with employee count, and apply the same minimum-size rule used elsewhere.

## Dashboard layout

Use a desktop canvas around 1200 × 850 pixels:

1. Title, fictional-data note and last-updated text
2. KPI row
3. Job-role view as the primary chart
4. Overtime and department comparisons
5. Tenure and business-travel views
6. Age- and income-band views
7. Filter panel and responsible-use note

Recommended filters are Department, Job Role, Age Band, Gender, Overtime, Business Travel and Tenure Band. Apply filters to all relevant worksheets using the same data source. Include a visible reset control.

## Interaction and tooltip rules

- Selecting a category should highlight related marks without revealing row-level records.
- Tooltips should state the segment, employees, attritions and attrition rate.
- Avoid causal language such as "driver" or "reason."
- Do not rank or label individual employees.
- Make clear when the minimum group-size rule hides a category.

## Accessibility

- Use a colour-blind-safe palette and do not encode attrition rate by colour alone.
- Maintain strong text/background contrast.
- Pair every percentage with a text label or axis.
- Use descriptive worksheet titles and Tableau alt text.
- Keep keyboard reading order aligned with the visual layout.
- Test the published view at common laptop width without horizontal scrolling.

## Publishing checklist

- [ ] All seven KPI checkpoints reconcile with the README
- [ ] Filters update the intended worksheets consistently
- [ ] Small groups are suppressed using the visible threshold
- [ ] No employee identifier or row-level record is exposed
- [ ] Tooltips include both rate and denominator
- [ ] Overall-rate reference lines remain correct under the chosen filter behaviour
- [ ] Fictional-data and non-causal interpretation notes are visible
- [ ] Titles, contrast, alt text and reading order are checked
- [ ] Dashboard screenshot is added to the repository
- [ ] Tableau Public link is added only after the published workbook is verified

## Responsible-use boundary

This dashboard is suitable for portfolio demonstration and aggregate workforce exploration only. The dataset is fictional, and its associations must not be used to make or justify decisions about hiring, promotion, performance management or termination. Any real HR deployment would require privacy, fairness, governance and legal review.
