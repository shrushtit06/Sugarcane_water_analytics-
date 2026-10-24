"""Phase 4: Story. Key insights, recommendations and impact (numbers come from the data)."""
import streamlit as st
from modules import ui


def _insight(icon, bg, text):
    return (f'<div class="insight"><div class="ins-icon" style="background:{bg}">{icon}</div>'
            f'<div>{text}</div></div>')


def _impact(value, label, sub, color):
    return (f'<div class="impact"><div class="impact-val" style="color:{color}">{value}</div>'
            f'<div class="impact-label">{label}</div><div class="impact-sub">{sub}</div></div>')


def show_story(df):
    corr = df["Farm_Size_acres"].corr(df["Water_Usage_L"])
    wpa = df.groupby("Irrigation_Type")["Water_per_acre"].mean()
    rain = df.groupby("State")["Rainfall_mm"].mean().sort_values()
    skew = df[["Farm_Size_acres", "Water_Usage_L", "Rainfall_mm"]].skew()

    drip, bore, canal = wpa.get("Drip"), wpa.get("Borewell"), wpa.get("Canal")
    have_both = drip is not None and bore is not None
    saving = (1 - drip / bore) * 100 if have_both else None
    dry = list(rain.index[:2])

    # ---- Key insights (What / Why / Domain value) ----
    ins = [
        _insight("📈", "#dff5e9", f"<b>What:</b> water usage rises with farm size (correlation {corr:.2f}), "
                 "so farms should be compared by <b>water per acre</b>."),
        _insight("📊", "#e0f0fe", f"Rainfall is almost symmetric (skewness {skew['Rainfall_mm']:.2f}) while farm size "
                 f"({skew['Farm_Size_acres']:.2f}) and water usage ({skew['Water_Usage_L']:.2f}) are right-skewed with many outliers."),
    ]
    if have_both:
        extra = f" and {canal:,.0f} L for canal" if canal else ""
        ins.append(_insight("💧", "#fdeedd", f"<b>Why:</b> drip uses about {drip:,.0f} L per acre against "
                            f"{bore:,.0f} L for borewell{extra}. Drip delivers water to the roots, "
                            "while borewell and canal flood the field."))
    else:
        ins.append(_insight("💧", "#fdeedd", "Select <b>All Types</b> in the Irrigation filter to compare drip with borewell."))
    ins.append(_insight("🌍", "#f0e6fd", f"<b>Domain value:</b> agriculture and water conservation. The driest state here is "
                        f"<b>{rain.index[0]}</b> (about {rain.iloc[0]:,.0f} mm of rain)."))

    recs = [
        _insight("💧", "#e0f0fe", "<b>Promote drip and sprinkler irrigation</b> to reduce water use and improve efficiency."),
        _insight("🌧️", "#dff5e9", f"<b>Focus on low-rainfall states</b> ({', '.join(dry)})."),
        _insight("📏", "#fdeedd", "<b>Track water per acre</b> instead of total water, so small and large farms compare fairly."),
        _insight("🌱", "#f0e6fd", "<b>Monitor soil moisture</b> to schedule irrigation better."),
    ]

    a, b = st.columns(2)
    with a:
        with ui.card("Key Insights"):
            st.markdown("".join(ins), unsafe_allow_html=True)
    with b:
        with ui.card("Recommendations"):
            st.markdown("".join(recs), unsafe_allow_html=True)

    # ---- Impact (calculated from the dataset) ----
    st.markdown('<div class="card-title" style="margin-top:14px">Business Impact (from this data)</div>',
                unsafe_allow_html=True)
    flood = df["Irrigation_Type"].isin(["Borewell", "Canal"]).mean() * 100
    tiles = [
        _impact(f"{saving:.0f}%" if have_both else "n/a", "Lower water use", "drip vs borewell, per acre", "#0f7a5a"),
        _impact(f"{bore - drip:,.0f} L" if have_both else "n/a", "Water saved per acre", "if borewell moves to drip", "#1f5fbf"),
        _impact(f"{df['Uses_Drip'].mean() * 100:.1f}%", "Drip adoption", "of farms in selection", "#7c3aed"),
        _impact(f"{flood:.1f}%", "Flood-style irrigation", "borewell + canal farms", "#c26a0a"),
    ]
    cols = st.columns(4)
    for c, t in zip(cols, tiles):
        c.markdown(t, unsafe_allow_html=True)

    st.markdown('<div class="closing">🌾 Efficient water use today ensures a sustainable sugarcane tomorrow.</div>',
                unsafe_allow_html=True)
