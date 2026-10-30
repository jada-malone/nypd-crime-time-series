
# Time Series Analysis by Offense Type

import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the dataset
df = pd.read_csv("NYPD_Cleaned 1(in).csv")

# 2. Check the data
print(df.head())
print(df.columns)

# 3. Make sure month and year are numeric
df["OCC_MONTH"] = pd.to_numeric(df["OCC_MONTH"], errors="coerce")
df["OCC_YEAR"] = pd.to_numeric(df["OCC_YEAR"], errors="coerce")

# 4. Filter for 2024 only
df_2024 = df[df["OCC_YEAR"] == 2024].copy()

# 5. Find the top 5 offense types
top_5_offenses = df_2024["OFNS_DESC"].value_counts().head(5).index

print("Top 5 Offense Types:")
print(top_5_offenses)

# 6. Keep only the top 5 offense types
df_top5 = df_2024[df_2024["OFNS_DESC"].isin(top_5_offenses)].copy()

# 7. Group by month and offense type
monthly_counts = (
    df_top5
    .groupby(["OCC_MONTH", "OFNS_DESC"])
    .size()
    .reset_index(name="COUNT")
)

print(monthly_counts.head())

# 8. Create pivot table for time series format
pivot_table = monthly_counts.pivot(
    index="OCC_MONTH",
    columns="OFNS_DESC",
    values="COUNT"
).fillna(0)

# 9. Sort by month
pivot_table = pivot_table.sort_index()

# 10. Display the table
print(pivot_table)

# 11. Plot the time series line chart
plt.figure(figsize=(12, 6))

for offense in pivot_table.columns:
    plt.plot(
        pivot_table.index,
        pivot_table[offense],
        marker="o",
        label=offense
    )

plt.title("Monthly Offense Type Trends in 2024")
plt.xlabel("Month")
plt.ylabel("Number of Offenses")
plt.xticks(range(1, 13))
plt.legend(title="Offense Type", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.tight_layout()
plt.show()

# 12. Find the peak month for each offense type
peak_summary = pd.DataFrame({
    "Peak Month": pivot_table.idxmax(),
    "Peak Count": pivot_table.max()
})

print("Peak Month and Count by Offense Type:")
print(peak_summary)

# 13. Optional: Convert month numbers to names for easier reading
month_names = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

peak_summary["Peak Month Name"] = peak_summary["Peak Month"].map(month_names)

print("Readable Peak Summary:")
print(peak_summary)