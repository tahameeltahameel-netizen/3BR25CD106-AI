"""
app.py

Student Performance Analytics Dashboard built with Streamlit, Pandas, and Plotly.
Clean, well-commented, beginner-friendly code designed for data science portfolios.
"""

import streamlit as st
import pandas as pd
import numpy as np

from utils.data_loader import (
    load_user_data,
    detect_column_types
)
from utils.charts import (
    create_subject_bar_chart,
    create_percentage_histogram,
    create_grade_donut_chart,
    create_department_box_plot,
    create_attendance_scatter_plot,
    create_subject_correlation_heatmap,
    create_semester_line_chart
)

# 1. Page Configuration
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark-Blue Clean Layout
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stMetric {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #334155;
    }
    .metric-card {
        background-color: #1e293b;
        border-radius: 10px;
        border: 1px solid #334155;
        padding: 1.2rem;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #3b82f6;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        font-weight: 600;
    }
    .insight-box {
        background-color: #1e293b;
        border-left: 4px solid #3b82f6;
        padding: 1rem 1.2rem;
        border-radius: 6px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def generate_key_insights(df: pd.DataFrame) -> list[str]:
    """Auto-generates 3-4 text insights from the filtered dataset.

    Args:
        df (pd.DataFrame): Filtered student dataset.

    Returns:
        list[str]: Bulleted key insight strings.
    """
    if df.empty:
        return ["No data available to generate insights."]

    insights = []

    # Insight 1: Lowest Scoring Subject
    subjects = ["Maths", "Python", "DBMS", "Data Structures", "Java"]
    present_subs = [s for s in subjects if s in df.columns]
    if present_subs:
        avg_scores = df[present_subs].mean()
        lowest_sub = avg_scores.idxmin()
        lowest_val = avg_scores.min()
        highest_sub = avg_scores.idxmax()
        highest_val = avg_scores.max()
        insights.append(
            f"**Subject Performance**: Students achieved the highest average score in **{highest_sub}** ({highest_val:.1f}), while **{lowest_sub}** was the lowest performing subject ({lowest_val:.1f})."
        )

    # Insight 2: Attendance Correlation
    if "attendance_percent" in df.columns and "percentage" in df.columns and len(df) > 1:
        corr = df["attendance_percent"].corr(df["percentage"])
        if corr > 0.4:
            corr_desc = "a strong positive correlation"
        elif corr > 0.1:
            corr_desc = "a moderate positive correlation"
        else:
            corr_desc = "a weak correlation"
        insights.append(
            f"**Attendance Impact**: There is {corr_desc} (r = {corr:.2f}) between student attendance and overall marks percentage."
        )

    # Insight 3: Pass Rate / Top Grade Proportions
    if "grade" in df.columns:
        pass_students = df[df["grade"] != "F"]
        pass_rate = (len(pass_students) / len(df)) * 100
        a_plus_count = len(df[df["grade"] == "A+"])
        insights.append(
            f"**Academic Success Rate**: **{pass_rate:.1f}%** of students passed their coursework, with **{a_plus_count}** students obtaining top 'A+' grades."
        )

    # Insight 4: Department / Semester Comparison
    if "department" in df.columns and "percentage" in df.columns:
        dept_avg = df.groupby("department")["percentage"].mean()
        if not dept_avg.empty:
            top_dept = dept_avg.idxmax()
            top_dept_val = dept_avg.max()
            insights.append(
                f"**Top Department**: The **{top_dept}** department leads performance with an average score of **{top_dept_val:.1f}%**."
            )

    return insights


def main():
    # Header Section
    st.title("🎓 Student Performance Analytics Dashboard")
    st.caption("Interactive data science portfolio dashboard built with Streamlit, Pandas, and Plotly.")

    # Sidebar: Dataset Upload & Controls
    st.sidebar.header("📁 Dataset Settings")
    uploaded_file = st.sidebar.file_uploader("Upload Custom Student CSV", type=["csv"])

    # Load Dataset
    df_raw, is_custom = load_user_data(uploaded_file)

    if df_raw.empty:
        st.error("No dataset available. Please upload a valid CSV file.")
        return

    if is_custom:
        st.sidebar.success("Custom CSV dataset loaded successfully!")
    else:
        st.sidebar.info("Using default sample dataset (data/students.csv).")

    # Detect Available Columns for Flexible Filtering
    numeric_cols, categorical_cols = detect_column_types(df_raw)

    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filter Dataset")

    # Dynamic Filter 1: Department
    selected_depts = "All"
    if "department" in df_raw.columns:
        depts = ["All"] + sorted(df_raw["department"].dropna().unique().tolist())
        selected_depts = st.sidebar.selectbox("Select Department", depts)

    # Dynamic Filter 2: Semester
    selected_sem = "All"
    if "semester" in df_raw.columns:
        sems = ["All"] + sorted(df_raw["semester"].dropna().unique().tolist())
        selected_sem = st.sidebar.selectbox("Select Semester", sems)

    # Dynamic Filter 3: Gender
    selected_gender = "All"
    if "gender" in df_raw.columns:
        genders = ["All"] + sorted(df_raw["gender"].dropna().unique().tolist())
        selected_gender = st.sidebar.selectbox("Select Gender", genders)

    # Dynamic Filter 4: Percentage Range Slider
    min_pct, max_pct = 0.0, 100.0
    if "percentage" in df_raw.columns:
        data_min = float(df_raw["percentage"].min())
        data_max = float(df_raw["percentage"].max())
        min_pct, max_pct = st.sidebar.slider(
            "Filter Percentage Range (%)",
            min_value=0.0,
            max_value=100.0,
            value=(data_min, data_max),
            step=1.0
        )

    # Apply Filtering
    df_filtered = df_raw.copy()

    if selected_depts != "All" and "department" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["department"] == selected_depts]

    if selected_sem != "All" and "semester" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["semester"] == selected_sem]

    if selected_gender != "All" and "gender" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["gender"] == selected_gender]

    if "percentage" in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered["percentage"] >= min_pct) & (df_filtered["percentage"] <= max_pct)
        ]

    # Handle Empty Filter Results
    if df_filtered.empty:
        st.warning("⚠️ No student records match the selected filter criteria. Please broaden your filters in the sidebar.")
        return

    # Top KPI Cards
    st.subheader("📌 Key Performance Indicators")
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

    total_students = len(df_filtered)
    avg_percentage = df_filtered["percentage"].mean() if "percentage" in df_filtered.columns else 0.0
    highest_score = df_filtered["percentage"].max() if "percentage" in df_filtered.columns else 0.0
    pass_pct = (
        (len(df_filtered[df_filtered["grade"] != "F"]) / total_students) * 100
        if "grade" in df_filtered.columns else 0.0
    )
    avg_attendance = (
        df_filtered["attendance_percent"].mean()
        if "attendance_percent" in df_filtered.columns else 0.0
    )

    with kpi_col1:
        st.metric("Total Students", f"{total_students}")
    with kpi_col2:
        st.metric("Average Score", f"{avg_percentage:.1f}%")
    with kpi_col3:
        st.metric("Highest Score", f"{highest_score:.1f}%")
    with kpi_col4:
        st.metric("Pass Rate", f"{pass_pct:.1f}%")
    with kpi_col5:
        st.metric("Avg Attendance", f"{avg_attendance:.1f}%")

    st.markdown("---")

    # Key Insights Section
    st.subheader("💡 Dynamic Key Insights")
    insights_list = generate_key_insights(df_filtered)
    for insight in insights_list:
        st.markdown(f"<div class='insight-box'>• {insight}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Analytics Charts Layout
    st.subheader("📊 Interactive Visualizations")

    chart_row1_col1, chart_row1_col2 = st.columns(2)
    with chart_row1_col1:
        st.plotly_chart(create_subject_bar_chart(df_filtered), use_container_width=True)
    with chart_row1_col2:
        st.plotly_chart(create_percentage_histogram(df_filtered), use_container_width=True)

    chart_row2_col1, chart_row2_col2 = st.columns(2)
    with chart_row2_col1:
        st.plotly_chart(create_grade_donut_chart(df_filtered), use_container_width=True)
    with chart_row2_col2:
        st.plotly_chart(create_department_box_plot(df_filtered), use_container_width=True)

    chart_row3_col1, chart_row3_col2 = st.columns(2)
    with chart_row3_col1:
        st.plotly_chart(create_attendance_scatter_plot(df_filtered), use_container_width=True)
    with chart_row3_col2:
        st.plotly_chart(create_semester_line_chart(df_filtered), use_container_width=True)

    st.plotly_chart(create_subject_correlation_heatmap(df_filtered), use_container_width=True)

    st.markdown("---")

    # Summary Statistics Table
    st.subheader("📈 Statistical Summary (df.describe())")
    st.dataframe(df_filtered.describe().round(2), use_container_width=True)

    # Top & Bottom Performers Tables
    st.markdown("---")
    st.subheader("🏆 Leaderboards: Top & Bottom Performers")

    top_col, bottom_col = st.columns(2)

    if "percentage" in df_filtered.columns:
        display_cols = [c for c in ["student_id", "name", "department", "attendance_percent", "percentage", "grade"] if c in df_filtered.columns]

        with top_col:
            st.markdown("#### 🥇 Top 10 Performers")
            top_10 = df_filtered.sort_values(by="percentage", ascending=False).head(10)[display_cols]
            st.dataframe(top_10, use_container_width=True, hide_index=True)

        with bottom_col:
            st.markdown("#### ⚠️ Bottom 10 Performers (Needs Support)")
            bottom_10 = df_filtered.sort_values(by="percentage", ascending=True).head(10)[display_cols]
            st.dataframe(bottom_10, use_container_width=True, hide_index=True)

    # Filtered Data Table & Download Option
    st.markdown("---")
    st.subheader("📋 Searchable Filtered Data Table")

    search_term = st.text_input("🔍 Search by Student Name or ID:")
    df_search = df_filtered.copy()

    if search_term:
        name_mask = df_search["name"].astype(str).str.contains(search_term, case=False, na=False) if "name" in df_search.columns else False
        id_mask = df_search["student_id"].astype(str).str.contains(search_term, case=False, na=False) if "student_id" in df_search.columns else False
        df_search = df_search[name_mask | id_mask]

    st.dataframe(df_search, use_container_width=True, hide_index=True)

    # CSV Download Button
    csv_data = df_search.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_student_data.csv",
        mime="text/csv"
    )


if __name__ == "__main__":
    main()
