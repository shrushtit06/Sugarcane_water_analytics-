"""Water Usage & Irrigation Analysis of Sugarcane Farms in India
Run with:  streamlit run app.py
"""
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Sugarcane Water Analytics", page_icon="🌾", layout="wide")

from modules import data_preprocessing as pre
from modules import filters, kpi_scoreboard, recommendations, ui
from modules import statistics as stat
from modules import visualizations as viz


@st.cache_data
def get_data():
    raw = pre.load_data("data/sugarcane.csv")
    return raw, pre.preprocess(raw)


def show(fig):
    st.pyplot(fig)
    plt.close(fig)


def chart_grid(items, n=3):
    """items = [(title, function that returns a figure), ...] shown in cards, n per row."""
    for i in range(0, len(items), n):
        for col, (title, make) in zip(st.columns(n), items[i:i + n]):
            with col:
                with ui.card(title):
                    show(make())


# ---------------------------------------------------------------- pages
def page_dashboard(data):
    ui.header("Water Usage & Irrigation Analysis of Sugarcane Farms in India",
              "Insights into water usage, irrigation patterns and farm characteristics", banner=True)
    kpi_scoreboard.show_kpis(data)
    chart_grid([
        ("Water Usage per Acre", lambda: viz.water_per_acre_by_state(data, 6, 3.2)),
        ("Rainfall by State", lambda: viz.rainfall_by_state_bar(data, 6, 3.2)),
        ("Water Usage by Irrigation Type", lambda: viz.boxplot_by_irrigation(data, w=6)),
        ("Farm Size vs Water Usage", lambda: viz.scatter(data, "Farm_Size_acres", "Water_Usage_L",
                                                         hue="Irrigation_Type", w=6)),
    ], n=2)


def page_preprocessing(raw, data):
    ui.header("Phase 1: Preprocessing", "Data quality, transformations and feature engineering")
    t1, t2, t3, t4 = st.tabs(["1. Quality Check", "2. Columns Used", "3. Normalization", "4. Binning"])

    with t1:
        missing, dups = pre.quality_check(raw)
        before, median, after = pre.imputation_demo(raw)
        a, b, c = st.columns([1.2, 1, 1.2])
        with a:
            with ui.card("Missing Values", "isnull().sum()"):
                ui.table(missing.rename("Missing Count").rename_axis("Column").reset_index(), index=False)
        with b:
            with ui.card("Duplicate Rows", "duplicated().sum()"):
                st.markdown(ui.bignum("duplicate rows", int(dups)), unsafe_allow_html=True)
                if missing.sum() == 0 and dups == 0:
                    st.markdown('<div class="tint tint-green"><div class="tint-title">✅ The data is clean</div>'
                                'No missing values and no duplicates.</div>', unsafe_allow_html=True)
        with c:
            with ui.card("Imputation Demo", "Farm_Size_acres, on a copy"):
                ui.table(ui.pd_frame({"Missing before": before, "Median used": f"{median:.2f} acres",
                                      "Missing after": after}), index=False)

    with t2:
        with ui.card("Columns Used"):
            ui.table(ui.pd_frame({
                "Column Group": ["Nominal", "Ratio, discrete", "Ratio / interval, continuous", "Interval, continuous"],
                "Columns": ["Record_ID, State, District, Soil_Type, Irrigation_Type, Seed_Variety",
                            "Farmer_Age, Water_Usage_L",
                            "Farm_Size_acres, Soil_Moisture_%, Soil_pH, Rainfall_mm, Temperature_C",
                            "Latitude, Longitude"]}), index=False)

    with t3:
        with ui.card("Normalization (sample)", "Min-Max on water and farm size, Z-score on rainfall"):
            sample = data[["Water_Usage_L", "Water_Usage_L_minmax", "Farm_Size_acres",
                           "Farm_Size_acres_minmax", "Rainfall_mm", "Rainfall_zscore"]].head(10)
            sample.columns = ["Water_Usage_L", "Water (min-max)", "Farm_Size_acres",
                              "Farm size (min-max)", "Rainfall_mm", "Rainfall (z-score)"]
            ui.table(sample.round(3), index=False)

    with t4:
        a, b, c = st.columns(3)
        with a:
            with ui.card("Binning"):
                st.markdown(ui.tint("Farm Size (equal-frequency)",
                                    data["Farm_Size_Category"].value_counts().sort_index().rename("Farms").to_frame(),
                                    "green"), unsafe_allow_html=True)
        with b:
            with ui.card("Binning"):
                st.markdown(ui.tint("Farmer Age (equal-width)",
                                    data["Age_Group"].value_counts().sort_index().rename("Farmers").to_frame(),
                                    "blue"), unsafe_allow_html=True)
        with c:
            with ui.card("Binning"):
                st.markdown(ui.tint("Rainfall (Low / Medium / High)",
                                    data["Rainfall_Category"].value_counts().sort_index().rename("Farms").to_frame(),
                                    "orange"), unsafe_allow_html=True)


def page_statistics(data):
    ui.header("Phase 2: Statistics", "Descriptive and distance / similarity measures")
    a, b = st.columns([2, 1])
    with a:
        with ui.card("Summary Statistics"):
            ui.table(stat.summary_table(data).T)
            st.caption("Farm size and water usage are right-skewed (skew about 2) with many outliers. "
                       "Rainfall is almost symmetric (skew about 0).")
    with b:
        with ui.card("Weighted & Grouped Mean"):
            gm, table = stat.grouped_mean(data["Water_Usage_L"], bins=10)
            st.markdown(ui.bignum("Weighted Mean (weight = farm size)", f"{stat.weighted_mean_water(data):,.0f} L")
                        + ui.bignum("Grouped Mean (10 bins)", f"{gm:,.0f} L")
                        + ui.bignum("Ordinary Mean", f"{data['Water_Usage_L'].mean():,.0f} L"),
                        unsafe_allow_html=True)

    with ui.card("Distance Between Sample Farms", "one farm per irrigation type"):
        seed = st.number_input("Random seed", value=7, step=1)
        farms = stat.sample_farms(data, n=4, seed=int(seed))
        ui.table(farms[["Record_ID", "State", "Irrigation_Type", "Soil_Type",
                        "Farm_Size_acres", "Water_Usage_L", "Rainfall_mm"]], index=False)
    euc, man = stat.distance_matrices(farms)
    jac, smc = stat.binary_similarity(farms)
    cols = st.columns(4)
    for col, (title, m) in zip(cols, [("Euclidean Distance", euc), ("Manhattan Distance", man),
                                      ("Jaccard Similarity", jac), ("SMC", smc)]):
        with col:
            with ui.card(title):
                ui.table(m)


def page_charts(data):
    ui.header("Phase 3: Charts", "Visual exploration of data patterns and relationships")
    t1, t2, t3, t4 = st.tabs(["Distribution", "Relationship", "Correlation", "Advanced"])
    sm = dict(w=4.4, h=3)
    with t1:
        chart_grid([
            ("Histogram: Farm Size", lambda: viz.histogram(data, "Farm_Size_acres", **sm)),
            ("Histogram: Water Usage", lambda: viz.histogram(data, "Water_Usage_L", viz.ORANGE, **sm)),
            ("Frequency Polygon: Rainfall", lambda: viz.frequency_polygon(data, **sm)),
            ("Ogive: Water Usage", lambda: viz.ogive(data, **sm)),
            ("Boxplot by Irrigation", lambda: viz.boxplot_by_irrigation(data, **sm)),
            ("Water per Acre by Irrigation", lambda: viz.water_per_acre_bar(data, **sm)),
        ])
    with t2:
        chart_grid([
            ("Scatter: Farm Size vs Water Usage",
             lambda: viz.scatter(data, "Farm_Size_acres", "Water_Usage_L", hue="Irrigation_Type", w=6)),
            ("Scatter: Rainfall vs Soil Moisture",
             lambda: viz.scatter(data, "Rainfall_mm", "Soil_Moisture_%", w=6)),
        ], n=2)
    with t3:
        a, b = st.columns(2)
        with a:
            with ui.card("Correlation Heatmap"):
                show(viz.correlation_heatmap(data, w=6))
        with b:
            with ui.card("Key Correlations"):
                pairs = [("Farm size vs Water usage", "Farm_Size_acres", "Water_Usage_L"),
                         ("Rainfall vs Soil moisture", "Rainfall_mm", "Soil_Moisture_%"),
                         ("Rainfall vs Water usage", "Rainfall_mm", "Water_Usage_L"),
                         ("Temperature vs Water usage", "Temperature_C", "Water_Usage_L")]
                rows = {"Pair": [p[0] for p in pairs],
                        "Correlation (r)": [round(data[p[1]].corr(data[p[2]]), 3) for p in pairs]}
                ui.table(ui.pd_frame(rows), index=False)
    with t4:
        chart_grid([
            ("Q-Q Plot: Rainfall (close to normal)", lambda: viz.qq_plot(data, "Rainfall_mm", w=6)),
            ("Q-Q Plot: Water Usage (not normal)", lambda: viz.qq_plot(data, "Water_Usage_L", w=6)),
        ], n=2)
        with ui.card("Pair Plot", "random sample of 1,000 farms"):
            show(viz.pair_plot(data))


# ---------------------------------------------------------------- main
ui.inject_css()
raw, df = get_data()
page = ui.sidebar_nav()
data = filters.apply_filters(df)

if data.empty:
    st.warning("No farms match these filters. Try 'All Types' or 'All Districts'.")
    st.stop()

if page == ui.PAGES[0]:
    page_dashboard(data)
elif page == ui.PAGES[1]:
    page_preprocessing(raw, data)
elif page == ui.PAGES[2]:
    page_statistics(data)
elif page == ui.PAGES[3]:
    page_charts(data)
else:
    ui.header("Phase 4: Story", "Key insights, recommendations and business impact")
    recommendations.show_story(data)
