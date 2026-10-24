"""KPI cards shown at the top of the dashboard."""
import streamlit as st


def _card(icon, bg, label, value, sub):
    return (f'<div class="kpi"><div class="kpi-icon" style="background:{bg}">{icon}</div><div>'
            f'<div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>'
            f'<div class="kpi-sub">{sub}</div></div></div>')


def show_kpis(df):
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(_card("🌱", "#dff5e9", "Total Farms", f"{len(df):,}", "in selected filters"),
                unsafe_allow_html=True)
    c2.markdown(_card("💧", "#e0f0fe", "Avg. Water Usage", f"{df['Water_Usage_L'].mean():,.0f} L", "per farm"),
                unsafe_allow_html=True)
    c3.markdown(_card("📐", "#f0e6fd", "Avg. Farm Size", f"{df['Farm_Size_acres'].mean():.1f} acres", "per farm"),
                unsafe_allow_html=True)
    c4.markdown(_card("🌧️", "#fdeedd", "Avg. Rainfall", f"{df['Rainfall_mm'].mean():,.0f} mm", "per farm"),
                unsafe_allow_html=True)
