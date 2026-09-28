#!/usr/bin/env python3
"""Validate and copy the committed employee-level Tableau source."""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_COLUMNS = [
    "Age", "Attrition", "BusinessTravel", "DailyRate", "Department",
    "DistanceFromHome", "Education", "EducationField", "EmployeeCount",
    "EmployeeNumber", "EnvironmentSatisfaction", "Gender", "HourlyRate",
    "JobInvolvement", "JobLevel", "JobRole", "JobSatisfaction",
    "MaritalStatus", "MonthlyIncome", "MonthlyRate", "NumCompaniesWorked",
    "Over18", "OverTime", "PercentSalaryHike", "PerformanceRating",
    "RelationshipSatisfaction", "StandardHours", "StockOptionLevel",
    "TotalWorkingYears", "TrainingTimesLastYear", "WorkLifeBalance",
    "YearsAtCompany", "YearsInCurrentRole", "YearsSinceLastPromotion",
    "YearsWithCurrManager",
]
DERIVED_COLUMNS = ["Attrition Flag", "Age Band", "Tenure Band", "Income Band"]
EXPECTED_ROWS = 1_470
EXPECTED_ATTRITIONS = 237
EXPECTED_SHA256 = "988ab632ae57bb334d70763035823f938e181d3724868dcd78da68b7da29f7a7"
EXPECTED_OVERTIME_RATES = {"Yes": 30.53, "No": 10.44}


def age_band(age: int) -> str:
    if age < 25:
        return "Under 25"
    if age < 35:
        return "25-34"
    if age < 45:
        return "35-44"
    if age < 55:
        return "45-54"
    return "55+"


def tenure_band(years: int) -> str:
    if years <= 1:
        return "0-1"
    if years <= 4:
        return "2-4"
    if years <= 9:
        return "5-9"
    if years <= 19:
        return "10-19"
    return "20+"


def income_band(income: int) -> str:
    if income < 3_000:
        return "Under 3000"
    if income < 6_000:
        return "3000-5999"
    if income < 10_000:
        return "6000-9999"
    return "10000+"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate(path: Path) -> tuple[int, int, float, float, dict[str, float]]:
    rows = attritions = tenure_total = income_total = 0
    employee_numbers: set[int] = set()
    overtime = {"Yes": [0, 0], "No": [0, 0]}

    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        expected_columns = SOURCE_COLUMNS + DERIVED_COLUMNS
        if reader.fieldnames != expected_columns:
            raise ValueError(
                "Tableau source columns do not match the documented schema.\n"
                f"Expected: {expected_columns}\nReceived: {reader.fieldnames}"
            )

        for line_number, row in enumerate(reader, start=2):
            try:
                employee_number = int(row["EmployeeNumber"])
                age = int(row["Age"])
                tenure = int(row["YearsAtCompany"])
                income = int(row["MonthlyIncome"])
                attrition_flag = int(row["Attrition Flag"])
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid numeric value on CSV line {line_number}."
                ) from exc

            if employee_number in employee_numbers:
                raise ValueError(f"Duplicate EmployeeNumber: {employee_number}")
            employee_numbers.add(employee_number)

            expected_attrition = int(row["Attrition"] == "Yes")
            if row["Attrition"] not in {"Yes", "No"} or attrition_flag != expected_attrition:
                raise ValueError(f"Attrition Flag mismatch on CSV line {line_number}.")
            if row["Age Band"] != age_band(age):
                raise ValueError(f"Age Band mismatch on CSV line {line_number}.")
            if row["Tenure Band"] != tenure_band(tenure):
                raise ValueError(f"Tenure Band mismatch on CSV line {line_number}.")
            if row["Income Band"] != income_band(income):
                raise ValueError(f"Income Band mismatch on CSV line {line_number}.")

            over_time = row["OverTime"]
            if over_time not in overtime:
                raise ValueError(f"Unexpected OverTime value on CSV line {line_number}.")
            overtime[over_time][0] += 1
            overtime[over_time][1] += attrition_flag
            rows += 1
            attritions += attrition_flag
            tenure_total += tenure
            income_total += income

    if rows == 0:
        raise ValueError("Tableau source contains no employee rows.")
    average_tenure = round(tenure_total / rows, 2)
    average_income = round(income_total / rows, 2)
    overtime_rates = {
        value: round(100 * counts[1] / counts[0], 2)
        for value, counts in overtime.items()
    }
    checks = {
        "employees": (rows, EXPECTED_ROWS),
        "unique employee numbers": (len(employee_numbers), EXPECTED_ROWS),
        "attritions": (attritions, EXPECTED_ATTRITIONS),
        "attrition rate": (round(100 * attritions / rows, 2), 16.12),
        "average tenure": (average_tenure, 7.01),
        "average monthly income": (average_income, 6_502.93),
        "overtime attrition rate": (overtime_rates["Yes"], EXPECTED_OVERTIME_RATES["Yes"]),
        "non-overtime attrition rate": (overtime_rates["No"], EXPECTED_OVERTIME_RATES["No"]),
    }
    failures = [
        f"{name}: expected {expected}, got {actual}"
        for name, (actual, expected) in checks.items()
        if actual != expected
    ]
    if failures:
        raise ValueError("Validation failed:\n- " + "\n- ".join(failures))
    return rows, attritions, average_tenure, average_income, overtime_rates


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate and copy the employee-level Tableau source."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=ROOT / "data" / "hr_attrition_clean.csv",
        help="committed clean CSV (default: data/hr_attrition_clean.csv)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "tableau" / "hr_attrition_tableau.csv",
        help="validated Tableau CSV (default: tableau/hr_attrition_tableau.csv)",
    )
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output.resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Tableau source not found: {source}")
    if source == output:
        raise ValueError("Source and output paths must be different.")

    digest = sha256(source)
    if digest != EXPECTED_SHA256:
        raise ValueError(
            f"SHA-256 mismatch: expected {EXPECTED_SHA256}, got {digest}"
        )
    rows, attritions, average_tenure, average_income, overtime_rates = validate(source)

    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix="hr-tableau-", suffix=".csv", dir=output.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        shutil.copyfile(source, temporary)
        copied_digest = sha256(temporary)
        if copied_digest != EXPECTED_SHA256:
            raise ValueError(
                f"Copied SHA-256 mismatch: expected {EXPECTED_SHA256}, got {copied_digest}"
            )
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)

    print(f"Prepared {rows:,} Tableau employee rows in {output}.")
    print(f"Attritions: {attritions:,}")
    print(f"Average tenure: {average_tenure:.2f} years")
    print(f"Average monthly income: ${average_income:,.2f}")
    print(f"Overtime attrition: {overtime_rates['Yes']:.2f}%")
    print(f"Non-overtime attrition: {overtime_rates['No']:.2f}%")
    print(f"SHA-256: {digest}")


if __name__ == "__main__":
    main()
