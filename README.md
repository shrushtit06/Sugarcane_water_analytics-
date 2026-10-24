# 🌾 Sugarcane Water Usage & Irrigation Analytics Dashboard

An interactive data analytics dashboard built using **Python and Streamlit** to explore water consumption, irrigation patterns, rainfall, and farm characteristics across sugarcane farms in India.

The project applies data preprocessing, descriptive statistics, statistical visualizations, and data-driven recommendations to understand agricultural water usage and support more efficient irrigation practices.

## 📌 Project Overview

Water management is an important challenge in sugarcane cultivation. This project analyses farm-level data to explore the relationship between farm size, water consumption, rainfall, and irrigation methods.

The dashboard presents key statistics and visual insights in an interactive interface, helping users compare irrigation methods and identify opportunities for water conservation.

## ✨ Features

- **Interactive Dashboard:** View important agricultural metrics through KPI cards and visualizations.
- **Data Preprocessing:** Examine missing values, duplicate records, imputation, normalization, and binning.
- **Statistical Analysis:** Explore mean, median, dispersion, skewness, outliers, grouped statistics, and distance measures.
- **Data Visualization:** Analyse distributions, box plots, scatter plots, Q-Q plots, histograms, and other statistical charts.
- **Filtering:** Explore data by state, irrigation type, and soil type.
- **Irrigation Comparison:** Compare water usage across different irrigation methods.
- **Key Performance Indicators (KPIs):** Monitor total farms, average water usage, average farm size, and average rainfall.
- **Data-Driven Recommendations:** View insights related to drip irrigation, rainfall, water efficiency, and soil moisture.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive dashboard and frontend |
| Pandas | Data manipulation and preprocessing |
| NumPy | Numerical operations |
| SciPy | Statistical computations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| OpenPyXL | Spreadsheet file support |

## 📂 Project Structure

```text
sugarcane-water-analytics-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   └── sugarcane.csv
│
├── modules/
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── filters.py
│   ├── statistics.py
│   ├── visualizations.py
│   ├── kpi_scoreboard.py
│   ├── recommendations.py
│   └── ui.py
│
└── .streamlit/
    └── config.toml
```

## 📊 Key Analytical Areas

### 1. Data Preprocessing
- Identify missing values and duplicate records.
- Demonstrate median-based imputation.
- Apply Min-Max normalization and Z-score standardization.
- Group continuous variables into meaningful categories using binning.

### 2. Statistical Analysis
- Calculate descriptive statistics and measures of central tendency.
- Study dispersion, skewness, and outliers.
- Compare weighted, grouped, and ordinary means.
- Explore distances and similarities between sample farms.

### 3. Visual Analytics
- Water usage per acre by state.
- Rainfall comparisons across states.
- Water consumption across irrigation types.
- Relationship between farm size and total water usage.
- Distribution and statistical diagnostic plots.

### 4. Insights and Recommendations
The dashboard uses the dataset to highlight patterns in water usage, compare irrigation methods, identify low-rainfall states, and present recommendations for efficient irrigation and water conservation.

## 🚀 Getting Started

Follow these steps to run the project locally.

### Prerequisites

- Python 3.10 or later
- pip package manager
- Git (optional, for cloning the repository)

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/sugarcane-water-analytics-dashboard.git
```

### Step 2: Navigate to the project folder

```bash
cd sugarcane-water-analytics-dashboard
```

### Step 3: Create a virtual environment (recommended)

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the dashboard

```bash
streamlit run app.py
```

The dashboard should open in your browser. If it does not, open the local URL displayed in the terminal, usually `http://localhost:8501`.

## 📈 Expected Outcome

The project provides an interactive way to investigate agricultural water consumption, understand the influence of farm characteristics, compare irrigation methods, and communicate statistical findings through visualizations and recommendations.

## 🎯 Learning Outcomes

Through this project, I explored:

- Data cleaning and preprocessing using Pandas.
- Statistical analysis and descriptive measures.
- Data visualization and interpretation.
- Building interactive dashboards using Streamlit.
- Modular Python programming.
- Translating analytical findings into actionable recommendations.

## 🔮 Future Improvements

- Add downloadable reports and filtered datasets.
- Include more agricultural and environmental datasets.
- Add predictive models for estimating irrigation requirements.
- Improve comparisons across seasons and regions.
- Deploy the dashboard online for easier access.

## 👩‍💻 Author
Shrushti Trivedi
---

⭐ If you find this project interesting, consider giving the repository a star!

*Built with Python, Streamlit, and data analytics.*
