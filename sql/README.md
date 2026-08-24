# SQLite analysis

Run `python3 scripts/build_database.py` to load and validate the 1,470-row fictional IBM HR sample, then create `project.db` and aggregate analysis views.

Expected reconciliation: **1,470 employees**, **237 attritions**, **16.12% attrition**, **7.01 years average tenure** and **$6,502.93 average monthly income**. Views compare departments, roles, overtime, tenure and travel using aggregate counts and rates; they are descriptive and are not intended for individual employment decisions.

Open `project.db` in DB Browser for SQLite to inspect the views or export Tableau-ready aggregates.

