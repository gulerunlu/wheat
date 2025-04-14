# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 21:22:44 2025

@author: Gandalf The Grey
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("prices.csv")

# Convert 'Date' column to datetime using correct format
df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y", errors="coerce")
df = df.dropna(subset=["Date"])

# Reshape to long format
df_long = df.melt(id_vars=["Date"], var_name="Country", value_name="Price")

# Drop missing or zero prices
df_long = df_long.dropna(subset=["Price"])
df_long = df_long[df_long["Price"] > 0]

# Label each row as Pre-War or Post-War based on cutoff
cutoff_date = pd.Timestamp("2022-02-24")
df_long["Period"] = df_long["Date"].apply(lambda x: "Pre-War" if x < cutoff_date else "Post-War")

# Create a balanced subset: 3 years before and 3 years after the war
trimmed_pre_war = df_long[(df_long["Period"] == "Pre-War") & (df_long["Date"] >= "2019-03-01")]
post_war = df_long[df_long["Period"] == "Post-War"]
balanced_df = pd.concat([trimmed_pre_war, post_war])

# Compute median prices
medians = balanced_df.groupby(["Country", "Period"])["Price"].median().reset_index()

# Plot boxplot with median annotations
plt.figure(figsize=(14, 6))
sns.set(style="whitegrid")

ax = sns.boxplot(
    data=balanced_df,
    x="Country",
    y="Price",
    hue="Period",
    palette="Set2"
)

plt.title("Boxplot with Median Values: Wheat Prices (Balanced 3-Year Periods)")
plt.xticks(rotation=45)

# Determine x-axis positions for annotation offsets
positions = {}
for i, country in enumerate(balanced_df["Country"].unique()):
    positions[country] = i

# Add annotations for medians
for index, row in medians.iterrows():
    x_offset = -0.2 if row["Period"] == "Pre-War" else 0.2
    x = positions[row["Country"]] + x_offset
    y = row["Price"]
    label = f"{y:.1f}"
    plt.text(x, y + 1, label, ha='center', va='bottom', fontsize=8, color='black')

plt.tight_layout()

# Save figure
plt.savefig("prices.png", dpi=300)