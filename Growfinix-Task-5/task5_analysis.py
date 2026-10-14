
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Set up project folders
BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "hospital_admissions.csv"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 2. Check the dataset
if not CSV_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {CSV_FILE}"
    )

# 3. Load the data
df = pd.read_csv(CSV_FILE, encoding="utf-8-sig")

# Standardize column names
df.columns = (
    df.columns.str.strip()
    .str.replace(" ", "_")
)

required_columns = [
    "Admission_ID",
    "Admission_Date",
    "Discharge_Date",
    "Department"
]

missing = [
    column for column in required_columns
    if column not in df.columns
]

if missing:
    raise ValueError(
        f"Missing columns: {missing}. "
        f"Columns found: {list(df.columns)}"
    )

# 4. Clean and prepare data
df["Admission_Date"] = pd.to_datetime(
    df["Admission_Date"], errors="coerce"
)

df["Discharge_Date"] = pd.to_datetime(
    df["Discharge_Date"], errors="coerce"
)

df["Department"] = df["Department"].astype("string").str.strip()

df = df.dropna(subset=required_columns)
df = df.drop_duplicates(subset=["Admission_ID"])

# Calculate length of stay in days
df["Length_of_Stay"] = (
    df["Discharge_Date"] - df["Admission_Date"]
).dt.days

# Remove impossible negative stays
df = df[df["Length_of_Stay"] >= 0].copy()

if df.empty:
    raise ValueError(
        "No valid records remain after cleaning."
    )

# 5. Analyze monthly admissions
df["Admission_Month"] = (
    df["Admission_Date"].dt.to_period("M").astype(str)
)

monthly_admissions = (
    df.groupby("Admission_Month")
    .size()
    .reset_index(name="Admission_Count")
)

monthly_admissions.to_csv(
    OUTPUT_DIR / "monthly_admissions.csv",
    index=False
)

# 6. Average length of stay by department
department_summary = (
    df.groupby("Department")["Length_of_Stay"]
    .agg(["count", "mean", "median"])
    .reset_index()
)

department_summary.columns = [
    "Department",
    "Admission_Count",
    "Average_Length_of_Stay",
    "Median_Length_of_Stay"
]

department_summary.to_csv(
    OUTPUT_DIR / "department_stay_summary.csv",
    index=False
)

# 7. Detect outliers using the IQR method
q1 = df["Length_of_Stay"].quantile(0.25)
q3 = df["Length_of_Stay"].quantile(0.75)
iqr = q3 - q1

lower_bound = max(0, q1 - 1.5 * iqr)
upper_bound = q3 + 1.5 * iqr

outliers = df[
    (df["Length_of_Stay"] < lower_bound)
    | (df["Length_of_Stay"] > upper_bound)
].copy()

outliers.to_csv(
    OUTPUT_DIR / "length_of_stay_outliers.csv",
    index=False
)

# Create a dataset with outliers excluded for comparison
df_without_outliers = df[
    (df["Length_of_Stay"] >= lower_bound)
    & (df["Length_of_Stay"] <= upper_bound)
].copy()

df.to_csv(
    OUTPUT_DIR / "cleaned_hospital_admissions.csv",
    index=False
)

df_without_outliers.to_csv(
    OUTPUT_DIR / "admissions_without_outliers.csv",
    index=False
)

# 8. Chart: monthly admission trends
sns.set_theme(style="whitegrid")

plt.figure(figsize=(12, 6))
sns.lineplot(
    data=monthly_admissions,
    x="Admission_Month",
    y="Admission_Count",
    marker="o"
)
plt.title("Monthly Hospital Admission Trends")
plt.xlabel("Admission Month")
plt.ylabel("Number of Admissions")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "monthly_admission_trends.png",
    dpi=300
)
plt.close()

# 9. Chart: average stay by department
plt.figure(figsize=(9, 5))
sns.barplot(
    data=department_summary,
    x="Department",
    y="Average_Length_of_Stay"
)
plt.title("Average Length of Stay by Department")
plt.xlabel("Department")
plt.ylabel("Average Stay (Days)")
plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "department_average_stay.png",
    dpi=300
)
plt.close()

# 10. Chart: length-of-stay outliers
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Length_of_Stay")
plt.title("Length of Stay — Outlier Detection")
plt.xlabel("Length of Stay (Days)")
plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "length_of_stay_boxplot.png",
    dpi=300
)
plt.close()

# 11. Print the results
print("\nTASK 5 ANALYSIS COMPLETED")
print("-" * 40)

print("Valid admissions:", len(df))
print("Outliers detected:", len(outliers))
print("IQR lower bound:", lower_bound)
print("IQR upper bound:", upper_bound)

print("\nMonthly admission trends:")
print(monthly_admissions.to_string(index=False))

print("\nAverage length of stay by department:")
print(department_summary.to_string(index=False))

print("\nOutput files saved in:", OUTPUT_DIR)
