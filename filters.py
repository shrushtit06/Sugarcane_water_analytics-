"""Sidebar filters: State, District, Irrigation Type."""
import streamlit as st


def apply_filters(df):
    sb = st.sidebar
    sb.markdown('<div class="side-title">⚙️ Filters</div>', unsafe_allow_html=True)

    state = sb.selectbox("State", ["All States"] + sorted(df["State"].unique()))
    data = df if state == "All States" else df[df["State"] == state]

    district = sb.selectbox("District", ["All Districts"] + sorted(data["District"].unique()))
    if district != "All Districts":
        data = data[data["District"] == district]

    irrigation = sb.selectbox("Irrigation Type", ["All Types"] + sorted(df["Irrigation_Type"].unique()))
    if irrigation != "All Types":
        data = data[data["Irrigation_Type"] == irrigation]
    return data
