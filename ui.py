"""Look and feel: CSS, page header, white cards, HTML tables."""
import streamlit as st

PAGES = ["📊  Dashboard", "🧹  Phase 1: Preprocessing", "📈  Phase 2: Statistics",
         "📉  Phase 3: Charts", "📖  Phase 4: Story"]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="st-"], .stMarkdown {font-family:'Inter',sans-serif;}
#MainMenu, footer {visibility:hidden;}
header[data-testid="stHeader"] {background:transparent;}
.block-container {padding-top:1.2rem; max-width:1500px;}
/* sidebar */
section[data-testid="stSidebar"] {background:linear-gradient(180deg,#0b3d3a 0%,#08302f 100%);}
section[data-testid="stSidebar"] > div {padding-top:0.5rem;}
.brand {display:flex; gap:10px; align-items:center; color:#fff; font-weight:700; font-size:17px; line-height:1.2; margin:6px 0 18px 0;}
.brand-icon {background:#17a673; border-radius:10px; width:38px; height:38px; display:flex; align-items:center; justify-content:center; font-size:20px;}
.side-title {color:#fff; font-weight:600; font-size:15px; margin:22px 0 6px 0; border-top:1px solid rgba(255,255,255,.15); padding-top:16px;}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {color:#9fd3c7; font-weight:600; font-size:13px;}
[data-testid="stSidebar"] div[role="radiogroup"] {gap:4px;}
[data-testid="stSidebar"] div[role="radiogroup"] label {padding:10px 14px; border-radius:10px; width:100%; cursor:pointer;}
[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {display:none;}
[data-testid="stSidebar"] div[role="radiogroup"] label p {color:#cfe8e3 !important; font-size:14px;}
[data-testid="stSidebar"] div[role="radiogroup"] label:hover {background:rgba(255,255,255,.08);}
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {background:#17a673;}
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {color:#fff !important; font-weight:600;}
/* header */
.hdr {display:flex; justify-content:space-between; align-items:center; padding:6px 4px 14px 4px;}
.hdr h1 {font-size:26px; font-weight:700; color:#0b3d3a; margin:0; padding:0;}
.hdr p {color:#1b7f6b; margin:2px 0 0 0; font-size:14px;}
.banner {background:linear-gradient(90deg,#ffffff 0%,#eaf7f0 55%,#a9d8bd 100%); border-radius:14px; padding:18px 24px; margin-bottom:6px; border:1px solid #e1ebe8;}
.deco {font-size:54px; letter-spacing:4px; opacity:.85;}
/* cards */
[class*="st-key-card_"] {background:#fff; border:1px solid #e1ebe8; border-radius:14px; padding:14px 16px; box-shadow:0 1px 4px rgba(11,61,58,.06);}
.card-title {font-weight:600; color:#0b3d3a; font-size:15px; margin-bottom:2px;}
.card-sub {font-weight:400; color:#6b8a85; font-size:12px; margin-left:8px;}
/* KPI */
.kpi {background:#fff; border:1px solid #e1ebe8; border-radius:14px; padding:16px; display:flex; gap:14px; align-items:center; box-shadow:0 1px 4px rgba(11,61,58,.06);}
.kpi-icon {width:52px; height:52px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:26px;}
.kpi-label {color:#6b8a85; font-size:13px;}
.kpi-value {color:#0b3d3a; font-size:24px; font-weight:700; line-height:1.2;}
.kpi-sub {color:#8aa39e; font-size:12px;}
/* tabs */
.stTabs [data-baseweb="tab-list"] {gap:8px; border-bottom:none;}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {display:none;}
.stTabs button[role="tab"] {background:#fff; border:1px solid #e1ebe8; border-radius:8px; padding:6px 18px; height:auto;}
.stTabs button[role="tab"][aria-selected="true"] {background:#17a673; border-color:#17a673;}
.stTabs button[role="tab"][aria-selected="true"] p {color:#fff; font-weight:600;}
/* tables */
.tbl-wrap {overflow:auto; max-height:330px; margin-top:6px;}
table.tbl {width:100%; border-collapse:collapse; font-size:12.5px;}
table.tbl th {background:#e8f5f1; color:#0b3d3a; padding:7px 10px; text-align:right !important; position:sticky; top:0;}
table.tbl td {padding:6px 10px; border-bottom:1px solid #edf3f1; text-align:right; color:#17302e;}
table.tbl th:first-child, table.tbl td:first-child {text-align:left !important;}
/* tinted boxes and big numbers */
.tint {border-radius:12px; padding:10px 12px;}
.tint-title {font-weight:600; font-size:13px; margin-bottom:4px;}
.tint-green {background:#eaf7f1; color:#0f7a5a;}
.tint-blue {background:#eaf2fd; color:#1f5fbf;}
.tint-orange {background:#fdf1e6; color:#c26a0a;}
.bignum {background:#eaf7f1; border-radius:12px; padding:10px 14px; margin-bottom:8px;}
.bn-label {font-size:12px; color:#0f7a5a; font-weight:600;}
.bn-val {font-size:24px; font-weight:700; color:#0b3d3a;}
.good {color:#0f7a5a; font-weight:600;}
/* story */
.insight {display:flex; gap:12px; align-items:flex-start; padding:9px 0; border-bottom:1px solid #edf3f1; font-size:13.5px; color:#17302e;}
.ins-icon {min-width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:18px;}
.impact {border-radius:12px; padding:14px; border:1px solid #e1ebe8; background:#fff;}
.impact-val {font-size:28px; font-weight:700;}
.impact-label {font-size:13px; color:#17302e; font-weight:600;}
.impact-sub {font-size:12px; color:#6b8a85;}
.closing {background:linear-gradient(90deg,#0b3d3a,#17805f); color:#fff; border-radius:14px; padding:22px 26px; font-size:17px; font-weight:600; margin-top:12px;}
"""

_count = [0]


def inject_css():
    _count[0] = 0  # card keys restart on every run
    st.markdown("<style>" + CSS + "</style>", unsafe_allow_html=True)


def sidebar_nav():
    st.sidebar.markdown(
        '<div class="brand"><div class="brand-icon">🌾</div>'
        '<div>Sugarcane<br>Water Analytics</div></div>', unsafe_allow_html=True)
    return st.sidebar.radio("Navigation", PAGES, label_visibility="collapsed")


def header(title, subtitle, banner=False):
    cls = "hdr banner" if banner else "hdr"
    deco = '<div class="deco">🌾🌾🌾</div>' if banner else ""
    st.markdown(f'<div class="{cls}"><div><h1>{title}</h1><p>{subtitle}</p></div>{deco}</div>',
                unsafe_allow_html=True)


def card(title=None, sub=None):
    """White rounded card. Use as:  with ui.card('Title'): ..."""
    _count[0] += 1
    box = st.container(key=f"card_{_count[0]}")
    if title:
        s = f'<span class="card-sub">{sub}</span>' if sub else ""
        box.markdown(f'<div class="card-title">{title}{s}</div>', unsafe_allow_html=True)
    return box


def _fmt(v):
    if isinstance(v, float):
        return f"{v:,.0f}" if abs(v) >= 1000 else f"{v:,.2f}"
    return v


def table_html(df, index=True):
    df = df.copy()
    df.index.name = None
    html = df.to_html(classes="tbl", border=0, index=index, float_format=_fmt,
                      formatters={c: _fmt for c in df.columns if df[c].dtype.kind == "f"})
    return '<div class="tbl-wrap">' + html.replace("\n", "") + "</div>"


def table(df, index=True):
    st.markdown(table_html(df, index), unsafe_allow_html=True)


def tint(title, series_or_df, color):
    """Small coloured box with a table inside (used for binning)."""
    return (f'<div class="tint tint-{color}"><div class="tint-title">{title}</div>'
            + table_html(series_or_df) + "</div>")


def bignum(label, value):
    return f'<div class="bignum"><div class="bn-label">{label}</div><div class="bn-val">{value}</div></div>'


def pd_frame(d):
    import pandas as pd
    return pd.DataFrame(d if isinstance(d, dict) and all(isinstance(v, list) for v in d.values())
                        else {k: [v] for k, v in d.items()})
