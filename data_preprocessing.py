"""Phase 1: Preprocessing (quality check, normalization, binning)."""
import numpy as np
import pandas as pd

NUMERIC_COLS = ["Farm_Size_acres", "Water_Usage_L", "Rainfall_mm",
                "Soil_Moisture_%", "Temperature_C"]


def load_data(path="data/sugarcane.csv"):
    return pd.read_csv(path)


def quality_check(df):
    """Returns missing values per column and number of duplicate rows."""
    missing = df.isnull().sum()
    duplicates = df.duplicated().sum()
    return missing, duplicates


def imputation_demo(df, n_blank=20, seed=1):
    """Blank a few values in a COPY, then fill them with the median."""
    demo = df[["Farm_Size_acres"]].copy()
    rng = np.random.default_rng(seed)
    rows = rng.choice(demo.index, n_blank, replace=False)
    demo.loc[rows, "Farm_Size_acres"] = np.nan
    before = int(demo["Farm_Size_acres"].isnull().sum())
    median = demo["Farm_Size_acres"].median()
    demo["Farm_Size_acres"] = demo["Farm_Size_acres"].fillna(median)
    after = int(demo["Farm_Size_acres"].isnull().sum())
    return before, median, after


def add_derived_columns(df):
    """Adds water per acre and a few yes/no columns."""
    df = df.copy()
    df["Water_per_acre"] = df["Water_Usage_L"] / df["Farm_Size_acres"]
    df["Uses_Drip"] = (df["Irrigation_Type"] == "Drip").astype(int)
    df["Red_Soil"] = (df["Soil_Type"] == "Red").astype(int)
    df["Uses_Borewell"] = (df["Irrigation_Type"] == "Borewell").astype(int)
    df["Low_Rainfall"] = (df["Rainfall_mm"] < 700).astype(int)
    return df


def normalize(df):
    """Min-Max on Water_Usage_L and Farm_Size_acres, Z-score on Rainfall_mm."""
    df = df.copy()
    for col in ["Water_Usage_L", "Farm_Size_acres"]:
        df[col + "_minmax"] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    df["Rainfall_zscore"] = (df["Rainfall_mm"] - df["Rainfall_mm"].mean()) / df["Rainfall_mm"].std()
    return df


def add_bins(df):
    """Farm size: equal-frequency, Age: equal-width, Rainfall: Low/Medium/High."""
    df = df.copy()
    df["Farm_Size_Category"] = pd.qcut(df["Farm_Size_acres"], 3,
                                       labels=["Small", "Medium", "Large"])
    df["Age_Group"] = pd.cut(df["Farmer_Age"], bins=4)
    df["Age_Group"] = df["Age_Group"].astype(str)
    df["Rainfall_Category"] = pd.cut(df["Rainfall_mm"], bins=3,
                                     labels=["Low", "Medium", "High"])
    return df


def preprocess(df):
    df = add_derived_columns(df)
    df = normalize(df)
    df = add_bins(df)
    return df
