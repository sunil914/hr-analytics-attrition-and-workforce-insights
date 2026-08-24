DROP VIEW IF EXISTS v_project_kpis;
DROP VIEW IF EXISTS v_department_attrition;
DROP VIEW IF EXISTS v_role_attrition;
DROP VIEW IF EXISTS v_overtime_attrition;
DROP VIEW IF EXISTS v_tenure_attrition;
DROP VIEW IF EXISTS v_travel_attrition;

CREATE VIEW v_project_kpis AS
SELECT
    COUNT(*) AS employees,
    SUM(attrition_flag) AS attritions,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct,
    ROUND(AVG(years_at_company), 2) AS average_tenure_years,
    ROUND(AVG(monthly_income), 2) AS average_monthly_income
FROM hr_employees;

CREATE VIEW v_department_attrition AS
SELECT department, COUNT(*) AS employees, SUM(attrition_flag) AS attritions,
       ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employees GROUP BY department;

CREATE VIEW v_role_attrition AS
SELECT job_role, COUNT(*) AS employees, SUM(attrition_flag) AS attritions,
       ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employees GROUP BY job_role HAVING COUNT(*) >= 10;

CREATE VIEW v_overtime_attrition AS
SELECT over_time, COUNT(*) AS employees, SUM(attrition_flag) AS attritions,
       ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employees GROUP BY over_time;

CREATE VIEW v_tenure_attrition AS
SELECT tenure_band, COUNT(*) AS employees, SUM(attrition_flag) AS attritions,
       ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employees GROUP BY tenure_band;

CREATE VIEW v_travel_attrition AS
SELECT business_travel, COUNT(*) AS employees, SUM(attrition_flag) AS attritions,
       ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employees GROUP BY business_travel;

