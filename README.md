# Water Usage & Irrigation Analysis of Sugarcane Farms in India

A Streamlit dashboard built on 50,000 sugarcane farm records (6 states, 30 districts).

## Run
```
pip install -r requirements.txt
streamlit run app.py
```

## Structure
| File | Purpose |
| --- | --- |
| `app.py` | Main dashboard (KPI cards, State filter, 5 tabs) |
| `data/sugarcane.csv` | Dataset |
| `modules/data_preprocessing.py` | Phase 1: quality check, normalization, binning |
| `modules/filters.py` | Sidebar filters (State, Irrigation, Soil) |
| `modules/statistics.py` | Phase 2: central tendency, dispersion, skew, outliers, distances |
| `modules/visualizations.py` | Phase 3: histogram, polygon, ogive, boxplot, Q-Q, scatter, pair-plot |
| `modules/kpi_scoreboard.py` | KPI cards |
| `modules/recommendations.py` | Phase 4: What / Why / Domain value / Recommendation |

## Story
- Water usage depends mainly on farm size (correlation about 0.92), so compare water per acre.
- Drip uses about 4,800 L/acre against about 7,300 L/acre for borewell.
- Gujarat is the driest state (about 700 mm rainfall).
- Recommendation: promote drip and sprinkler irrigation in low-rainfall states.
