# 🌿 Sri Lanka Climate Change Dashboard

An interactive Streamlit dashboard exploring Sri Lanka's climate change indicators from 1960 to 2024, built using World Bank data sourced from the Humanitarian Data Exchange (HDX).

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)
![Pandas](https://img.shields.io/badge/Pandas-2.x-green)
![Plotly](https://img.shields.io/badge/Plotly-5.x-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🔗 Live Dashboard
👉 [Click here to view the live dashboard](https://rt6ecubcyvrxuyjzcgva62.streamlit.app)

---

## 📊 Dataset
- **Source:** [Humanitarian Data Exchange (HDX)](https://data.humdata.org/dataset/world-bank-climate-change-indicators-for-sri-lanka)
- **Provider:** World Bank
- **Country:** Sri Lanka 🇱🇰
- **Period:** 1960 – 2024
- **Records:** 1,534 rows
- **Indicators:** 48 climate indicators including energy, agriculture, land use, population, and environment

---

## ✨ Features

| Feature | Description |
|---|---|
| 📂 Category Filter | Filter indicators by Agriculture, Energy, Climate, Population, Water |
| 📈 Trend Analysis | Line chart with optional 5-year moving average |
| 📊 Year Breakdown | Bar chart with colour scale by value |
| 🔍 Compare Indicators | Compare multiple indicators with normalize toggle |
| 🕐 Decade Overview | Decade bar chart, donut chart, and heatmap |
| 📋 Data Explorer | Searchable data table with CSV download |
| 💡 Auto Insights | Automatic insight text showing % change over time |
| 🎨 Chart Themes | Switch between Greens, Blues, Viridis, Plasma, Turbo |

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/maleesha05/climate-dashboard-.git
cd climate-dashboard-
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Open in browser
```
http://localhost:8501
```

---

## 📁 Project Structure

```
climate-dashboard/
├── app.py                          # Main Streamlit dashboard
├── clean_data.py                   # Data cleaning script
├── sri_lanka_climate_cleaned.xlsx  # Cleaned dataset
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

---

## 📦 Dependencies

```
streamlit
pandas
plotly
openpyxl
```

---

## 📚 Module Information

- **Module:** 5DATA004C Data Science Project Lifecycle
- **University:** University of Westminster
- **Academic Year:** 2025/2026

---

## 📝 License

This project is for academic purposes only. Data sourced from the World Bank via HDX.
