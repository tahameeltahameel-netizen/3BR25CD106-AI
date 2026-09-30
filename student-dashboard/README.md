# 🎓 Student Performance Analytics Dashboard

An interactive, beginner-friendly Data Visualization & Analytics Dashboard built with Python, Streamlit, Pandas, and Plotly. Designed for computer science and data science student portfolios.

![Dashboard Screenshot](screenshot_placeholder.png)

## 📌 Project Overview

This application allows educators and academic administrators to explore, analyze, and visualize student performance metrics. Users can filter student datasets dynamically by department, semester, gender, and percentage range, inspect key performance metrics, view interactive Plotly visualizations, read auto-generated key analytical insights, and export filtered results.

---

## ✨ Features

1. **Custom Data Upload & Synthetic Data Generation**:
   - Includes a standalone data generator (`data/generate_data.py`) creating 200 realistic student records.
   - Allows users to upload custom CSV files with dynamic column detection.
2. **Interactive Sidebar Filters**:
   - Filter records by Department, Semester, Gender, and Percentage Score range.
3. **Key Performance Indicator (KPI) Cards**:
   - Total Students, Average Score %, Highest Score, Pass Rate %, and Average Attendance %.
4. **Interactive Visualizations (Plotly Express)**:
   - **Bar Chart**: Average marks across subjects (Maths, Python, DBMS, Data Structures, Java).
   - **Histogram**: Distribution of student percentage scores.
   - **Donut Chart**: Grade distribution (`A+`, `A`, `B`, `C`, `D`, `F`).
   - **Box Plot**: Percentage score distribution across departments.
   - **Scatter Plot**: Attendance % vs. Overall Percentage with trendline.
   - **Heatmap**: Subject and metric correlation matrix.
   - **Line Chart**: Average performance trend across semesters.
5. **Statistical Summary & Leaderboards**:
   - Comprehensive `df.describe()` table.
   - Top 10 High Performers & Bottom 10 Performers requiring academic support.
6. **Search & Data Export**:
   - Live name/ID search bar and CSV download button for filtered dataset views.
7. **Auto-Generated Key Insights**:
   - 3-4 bulleted analytical takeaways synthesized dynamically from active filter selections.

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Dashboard Framework**: Streamlit
- **Data Manipulation**: Pandas, NumPy
- **Interactive Visualizations**: Plotly Express, Statsmodels
- **Data Export**: CSV

---

## 📁 Directory Structure

```text
student-dashboard/
│
├── app.py                   # Main Streamlit application entry point
├── data/
│   ├── generate_data.py      # Standalone synthetic dataset generator script
│   └── students.csv          # Generated default student dataset
├── utils/
│   ├── data_loader.py        # Cached data loading & preprocessing helpers
│   └── charts.py             # Plotly chart creation helper functions
├── requirements.txt         # Project Python dependencies
├── README.md                # Project documentation
└── .gitignore               # Git ignore rules
```

---

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/student-dashboard.git
cd student-dashboard
```

### 2. Set Up Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate Dataset (Optional)
```bash
python data/generate_data.py
```

### 5. Launch Streamlit App
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your web browser.

---

## 🧠 What I Learned

- Building interactive web analytical interfaces using **Streamlit**.
- Utilizing `@st.cache_data` to optimize data loading performance and avoid redundant re-computations.
- Designing modular Python software using function type hints and docstrings across utility modules (`utils/data_loader.py` and `utils/charts.py`).
- Transforming raw datasets into compelling, customizable data visualizations with **Plotly Express**.
- Implementing dynamic, rule-based text synthesis for automated data insights generation.
