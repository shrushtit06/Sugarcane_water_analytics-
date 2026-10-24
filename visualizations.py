"""Phase 3: Charts. Each function returns a matplotlib figure (styled like the mockup)."""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats

sns.set_theme(style="whitegrid", rc={"font.size": 9, "grid.color": "#e8efed",
                                     "axes.edgecolor": "#cfdcd9", "axes.labelcolor": "#17302e"})

GREEN, BLUE, ORANGE, PURPLE = "#1b9e77", "#3b82f6", "#f59e0b", "#8b5cf6"
PALETTE = {"Drip": GREEN, "Sprinkler": BLUE, "Borewell": ORANGE, "Canal": PURPLE, "Rainfed": "#94a3b8"}


def _types(df):
    return [t for t in PALETTE if t in df["Irrigation_Type"].unique()]


def _done(fig, ax, xlabel=None, ylabel=None):
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    sns.despine(ax=ax)
    fig.tight_layout()
    return fig


def histogram(df, col, color=GREEN, w=5, h=3.2):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.hist(df[col], bins=35, color=color, edgecolor="white")
    return _done(fig, ax, col, "Frequency")


def frequency_polygon(df, col="Rainfall_mm", bins=25, w=5, h=3.2):
    counts, edges = np.histogram(df[col], bins=bins)
    mids = (edges[:-1] + edges[1:]) / 2
    fig, ax = plt.subplots(figsize=(w, h))
    ax.plot(mids, counts, marker="o", ms=3, color=BLUE)
    ax.fill_between(mids, counts, alpha=0.15, color=BLUE)
    return _done(fig, ax, "Rainfall (mm)", "Frequency")


def ogive(df, col="Water_Usage_L", bins=30, w=5, h=3.2):
    counts, edges = np.histogram(df[col], bins=bins)
    fig, ax = plt.subplots(figsize=(w, h))
    ax.plot(edges[1:], np.cumsum(counts) / counts.sum() * 100, color=PURPLE, lw=2)
    return _done(fig, ax, "Water usage (L), upper class limit", "Cumulative %")


def boxplot_by_irrigation(df, col="Water_Usage_L", w=5, h=3.2):
    fig, ax = plt.subplots(figsize=(w, h))
    sns.boxplot(data=df, x="Irrigation_Type", y=col, order=_types(df), hue="Irrigation_Type",
                hue_order=_types(df), palette=PALETTE, legend=False, fliersize=2, linewidth=1, ax=ax)
    return _done(fig, ax, "", "Water Usage (L)")


def qq_plot(df, col, w=5, h=3.2):
    fig, ax = plt.subplots(figsize=(w, h))
    stats.probplot(df[col], dist="norm", plot=ax)
    ax.set_title("")
    ax.get_lines()[0].set_color(GREEN)
    ax.get_lines()[0].set_markersize(3)
    ax.get_lines()[1].set_color(ORANGE)
    return _done(fig, ax)


def scatter(df, x, y, hue=None, sample=4000, w=5, h=3.2):
    data = df.sample(min(sample, len(df)), random_state=1)
    fig, ax = plt.subplots(figsize=(w, h))
    if hue:
        sns.scatterplot(data=data, x=x, y=y, hue=hue, hue_order=_types(data), palette=PALETTE,
                        alpha=0.6, s=10, ax=ax)
        ax.legend(title=None, fontsize=8, markerscale=1.4, frameon=False)
    else:
        sns.scatterplot(data=data, x=x, y=y, color=BLUE, alpha=0.5, s=10, ax=ax)
    return _done(fig, ax)


def pair_plot(df, sample=1000):
    cols = ["Farm_Size_acres", "Water_Usage_L", "Rainfall_mm", "Soil_Moisture_%",
            "Temperature_C", "Irrigation_Type"]
    data = df[cols].sample(min(sample, len(df)), random_state=1)
    grid = sns.pairplot(data, hue="Irrigation_Type", hue_order=_types(data), palette=PALETTE,
                        corner=True, height=1.8, plot_kws={"s": 8, "alpha": 0.5})
    return grid.figure


def water_per_acre_bar(df, w=5, h=3.2):
    order = df.groupby("Irrigation_Type")["Water_per_acre"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(w, h))
    ax.barh(order.index, order.values, color=[PALETTE[t] for t in order.index])
    for i, v in enumerate(order.values):
        ax.text(v, i, f" {v:,.0f}", va="center", fontsize=8)
    return _done(fig, ax, "Litres per acre", "")


def water_per_acre_by_state(df, w=5, h=3.2):
    s = df.groupby("State")["Water_per_acre"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(w, h))
    ax.bar(s.index, s.values, color=GREEN)
    ax.tick_params(axis="x", rotation=25, labelsize=8)
    return _done(fig, ax, "", "Water (L/acre)")


def rainfall_by_state_bar(df, w=5, h=3.2):
    s = df.groupby("State")["Rainfall_mm"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(w, h))
    ax.bar(s.index, s.values, color=BLUE)
    ax.tick_params(axis="x", rotation=25, labelsize=8)
    return _done(fig, ax, "", "Rainfall (mm)")


def correlation_heatmap(df, w=5, h=3.8):
    cols = ["Farm_Size_acres", "Water_Usage_L", "Rainfall_mm", "Soil_Moisture_%", "Temperature_C", "Soil_pH"]
    fig, ax = plt.subplots(figsize=(w, h))
    sns.heatmap(df[cols].corr(), annot=True, fmt=".2f", cmap="YlGnBu", annot_kws={"size": 7}, ax=ax)
    ax.tick_params(labelsize=7)
    fig.tight_layout()
    return fig
