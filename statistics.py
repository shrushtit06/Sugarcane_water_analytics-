"""Phase 2: Descriptive statistics."""
import numpy as np
import pandas as pd
from scipy import stats
from scipy.spatial.distance import cdist

STAT_COLS = ["Farm_Size_acres", "Water_Usage_L", "Rainfall_mm"]


def count_outliers(s):
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return int(((s < low) | (s > high)).sum())


def summary_table(df):
    rows = {}
    for col in STAT_COLS:
        s = df[col]
        rows[col] = {
            "Mean": s.mean(),
            "Median": s.median(),
            "Mode": s.mode()[0],
            "Range": s.max() - s.min(),
            "Variance": s.var(),
            "Std Dev": s.std(),
            "CV (%)": s.std() / s.mean() * 100,
            "Skewness": stats.skew(s),
            "Kurtosis": stats.kurtosis(s),
            "IQR": s.quantile(0.75) - s.quantile(0.25),
            "Outliers (IQR rule)": count_outliers(s),
        }
    return pd.DataFrame(rows).round(2)


def weighted_mean_water(df):
    """Mean water usage, using farm size as the weight."""
    return np.average(df["Water_Usage_L"], weights=df["Farm_Size_acres"])


def grouped_mean(s, bins=10):
    """Mean estimated from grouped (binned) data: sum(midpoint * freq) / n."""
    groups = pd.cut(s, bins=bins)
    freq = groups.value_counts().sort_index()
    mid = np.array([iv.mid for iv in freq.index])
    table = pd.DataFrame({"Class": freq.index.astype(str),
                          "Midpoint": mid, "Frequency": freq.values})
    mean = (mid * freq.values).sum() / freq.values.sum()
    return mean, table


def sample_farms(df, n=4, seed=7):
    """Pick one farm per irrigation type so the comparison is interesting."""
    types = [t for t in ["Drip", "Borewell", "Canal", "Sprinkler"]
             if t in df["Irrigation_Type"].values]
    if len(types) < 2:
        return df.sample(min(n, len(df)), random_state=seed)
    parts = [df[df["Irrigation_Type"] == t].sample(1, random_state=seed) for t in types]
    return pd.concat(parts)


def distance_matrices(farms):
    """Euclidean and Manhattan distance on Min-Max scaled numeric columns."""
    cols = ["Farm_Size_acres", "Water_Usage_L", "Rainfall_mm",
            "Soil_Moisture_%", "Temperature_C"]
    x = farms[cols]
    x = (x - x.min()) / (x.max() - x.min())  # scale so no column dominates
    names = farms["Record_ID"].values
    euc = pd.DataFrame(cdist(x, x, "euclidean"), index=names, columns=names)
    man = pd.DataFrame(cdist(x, x, "cityblock"), index=names, columns=names)
    return euc.round(3), man.round(3)


def binary_similarity(farms):
    """Jaccard and SMC between farms using yes/no columns."""
    cols = ["Uses_Drip", "Uses_Borewell", "Red_Soil", "Low_Rainfall"]
    names = farms["Record_ID"].values
    data = farms[cols].values
    n = len(names)
    jac = np.zeros((n, n))
    smc = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            a, b = data[i], data[j]
            both1 = np.sum((a == 1) & (b == 1))
            both0 = np.sum((a == 0) & (b == 0))
            diff = np.sum(a != b)
            jac[i, j] = both1 / (both1 + diff) if (both1 + diff) > 0 else 1
            smc[i, j] = (both1 + both0) / len(a)
    return (pd.DataFrame(jac, index=names, columns=names).round(2),
            pd.DataFrame(smc, index=names, columns=names).round(2))
