"""Prepare the original long-format Tax Burden on Tobacco export."""
import numpy as np
import pandas as pd

MEASURES = {
    "Cigarette Consumption (Pack Sales Per Capita)": "Y",
    "State Tax per pack": "state_tax",
    "Federal and State Tax per pack": "total_tax",
    "Federal and State tax as a Percentage of Retail Price": "reported_total_tax_pct",
    "Average Cost per pack": "Avg Cost Per Pack",
    "Gross Cigarette Tax Revenue": "Gross Cigarette Tax Revenue",
}


def load_data(path):
    raw = pd.read_csv(path)
    required = {"LocationAbbr", "Year", "SubMeasureDesc", "Data_Value"}
    if not required.issubset(raw.columns):
        raise ValueError(f"Missing raw CSV columns: {sorted(required - set(raw.columns))}")
    raw = raw.loc[raw["SubMeasureDesc"].isin(MEASURES)].copy()
    raw["Year"] = pd.to_numeric(raw["Year"], errors="raise")
    if not np.isfinite(raw["Year"]).all() or (raw["Year"] % 1 != 0).any():
        raise ValueError("Year must contain finite whole years")
    raw = raw.loc[raw["Year"].between(1990, 2019)].copy()
    if raw.empty:
        raise ValueError("No observations in 1990-2019")
    raw["Data_Value"] = pd.to_numeric(raw["Data_Value"], errors="raise")
    if not np.isfinite(raw["Data_Value"]).all():
        raise ValueError("Data_Value must be finite")
    if raw.duplicated(["LocationAbbr", "Year", "SubMeasureDesc"]).any():
        raise ValueError("Duplicate state-year-measure records")
    df = raw.pivot(index=["LocationAbbr", "Year"], columns="SubMeasureDesc", values="Data_Value").rename(columns=MEASURES)
    if not set(MEASURES.values()).issubset(df.columns) or df.isna().any().any():
        raise ValueError("Missing measures for one or more state-years")
    df = df.reset_index().rename(columns={"LocationAbbr": "state"})
    if (df["Avg Cost Per Pack"] <= 0).any() or (df[["Y", "state_tax", "total_tax"]] < 0).any().any():
        raise ValueError("Prices must be positive and sales/taxes nonnegative")
    if (df["total_tax"] < df["state_tax"]).any():
        raise ValueError("Combined tax cannot be below state tax")
    df["state_tax_pct"] = df["state_tax"] / df["Avg Cost Per Pack"]
    df["federal_tax_pct"] = (df["total_tax"] - df["state_tax"]) / df["Avg Cost Per Pack"]
    df["total_tax_pct"] = df["total_tax"] / df["Avg Cost Per Pack"]
    df["Year"] = df["Year"].astype(int)
    df.columns.name = None
    return df.sort_values(["state", "Year"]).reset_index(drop=True)
