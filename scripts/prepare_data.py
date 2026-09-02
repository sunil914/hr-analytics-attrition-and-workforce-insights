#!/usr/bin/env python3
"""Rebuild the cleaned IBM HR Analytics dataset from its original CSV."""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import tempfile
from pathlib import Path


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


def prepare_row(source: dict[str, str]) -> dict[str, str | int]:
    row = {column: source[column].strip() for column in SOURCE_COLUMNS}
    if row["Attrition"] not in {"Yes", "No"}:
        raise ValueError(f"Unexpected Attrition value: {row['Attrition']!r}")
    row.update(
        {
            "Attrition Flag": int(row["Attrition"] == "Yes"),
            "Age Band": age_band(int(row["Age"])),
            "Tenure Band": tenure_band(int(row["YearsAtCompany"])),
            "Income Band": income_band(int(row["MonthlyIncome"])),
        }
    )
    return row


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source", type=Path, help="Path to WA_Fn-UseC_-HR-Employee-Attrition.csv"
    )
    parser.add_argument(
        "--output", type=Path, default=Path("data/hr_attrition_clean.csv")
    )
    args = parser.parse_args()

    if args.source.resolve() == args.output.resolve():
        raise ValueError("Source and output paths must be different.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = tempfile.NamedTemporaryFile(
        prefix="hr-clean-", suffix=".csv", dir=args.output.parent, delete=False
    )
    temporary_path = Path(temporary.name)
    temporary.close()

    rows = attritions = tenure_total = income_total = 0
    employee_numbers: set[int] = set()
    try:
        with args.source.open(encoding="utf-8-sig", newline="") as source_stream:
            reader = csv.DictReader(source_stream)
            if reader.fieldnames != SOURCE_COLUMNS:
                raise ValueError(
                    "Source columns do not match the IBM HR Analytics CSV.\n"
                    f"Expected: {SOURCE_COLUMNS}\nReceived: {reader.fieldnames}"
                )

            with temporary_path.open("w", encoding="utf-8", newline="") as output_stream:
                writer = csv.DictWriter(
                    output_stream,
                    fieldnames=SOURCE_COLUMNS + DERIVED_COLUMNS,
                    lineterminator="\n",
                )
                writer.writeheader()
                for source_row in reader:
                    row = prepare_row(source_row)
                    employee_number = int(row["EmployeeNumber"])
                    if employee_number in employee_numbers:
                        raise ValueError(f"Duplicate EmployeeNumber: {employee_number}")
                    employee_numbers.add(employee_number)
                    writer.writerow(row)
                    rows += 1
                    attritions += int(row["Attrition Flag"])
                    tenure_total += int(row["YearsAtCompany"])
                    income_total += int(row["MonthlyIncome"])

        checks = {
            "employees": (rows, EXPECTED_ROWS),
            "unique employee numbers": (len(employee_numbers), EXPECTED_ROWS),
            "attritions": (attritions, EXPECTED_ATTRITIONS),
            "attrition rate": (round(100 * attritions / rows, 2), 16.12),
            "average tenure": (round(tenure_total / rows, 2), 7.01),
            "average monthly income": (round(income_total / rows, 2), 6_502.93),
        }
        failures = [
            f"{name}: {actual} != {expected}"
            for name, (actual, expected) in checks.items()
            if actual != expected
        ]
        digest = file_sha256(temporary_path)
        if digest != EXPECTED_SHA256:
            failures.append(f"SHA-256: {digest} != {EXPECTED_SHA256}")
        if failures:
            raise ValueError("Validation failed:\n- " + "\n- ".join(failures))

        os.replace(temporary_path, args.output)
        print(f"Prepared {rows:,} employees with {attritions:,} attritions.")
        print(f"SHA-256: {digest}")
        print(f"Wrote {args.output}.")
    finally:
        temporary_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
