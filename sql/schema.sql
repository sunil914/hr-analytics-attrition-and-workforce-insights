DROP TABLE IF EXISTS hr_employees;

CREATE TABLE hr_employees (
    age INTEGER, attrition TEXT, business_travel TEXT, daily_rate INTEGER,
    department TEXT, distance_from_home INTEGER, education INTEGER,
    education_field TEXT, employee_count INTEGER, employee_number INTEGER,
    environment_satisfaction INTEGER, gender TEXT, hourly_rate INTEGER,
    job_involvement INTEGER, job_level INTEGER, job_role TEXT,
    job_satisfaction INTEGER, marital_status TEXT, monthly_income INTEGER,
    monthly_rate INTEGER, num_companies_worked INTEGER, over18 TEXT,
    over_time TEXT, percent_salary_hike INTEGER, performance_rating INTEGER,
    relationship_satisfaction INTEGER, standard_hours INTEGER,
    stock_option_level INTEGER, total_working_years INTEGER,
    training_times_last_year INTEGER, work_life_balance INTEGER,
    years_at_company INTEGER, years_in_current_role INTEGER,
    years_since_last_promotion INTEGER, years_with_curr_manager INTEGER,
    attrition_flag INTEGER, age_band TEXT, tenure_band TEXT, income_band TEXT
);

CREATE INDEX idx_hr_department ON hr_employees (department);
CREATE INDEX idx_hr_role ON hr_employees (job_role);

