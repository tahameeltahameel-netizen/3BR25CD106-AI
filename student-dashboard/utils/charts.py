"""
utils/charts.py

Plotly chart generation helper functions for the Student Analytics Dashboard.
Clean, modular, and styled with consistent dark-blue palette.
"""

from typing import List, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Custom color palette matching dark-blue dashboard theme
PRIMARY_COLOR = "#2563eb"
SECONDARY_COLOR = "#3b82f6"
ACCENT_COLOR = "#10b981"
DARK_BG = "rgba(0,0,0,0)"

SUBJECT_COLUMNS = ["Maths", "Python", "DBMS", "Data Structures", "Java"]


def create_subject_bar_chart(df: pd.DataFrame) -> go.Figure:
    """Bar chart showing average marks across subjects.

    Args:
        df (pd.DataFrame): Filtered student dataset.

    Returns:
        go.Figure: Plotly bar chart figure.
    """
    subjects_present = [col for col in SUBJECT_COLUMNS if col in df.columns]
    if not subjects_present:
        # Fallback to numeric columns
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        subjects_present = [c for c in numeric_cols if c not in ["student_id", "semester", "total", "percentage", "attendance_percent"]][:5]

    if not subjects_present or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No subject data available", showarrow=False, font=dict(size=16))
        return fig

    avg_marks = df[subjects_present].mean().reset_index()
    avg_marks.columns = ["Subject", "Average Marks"]
    avg_marks["Average Marks"] = avg_marks["Average Marks"].round(2)

    fig = px.bar(
        avg_marks,
        x="Subject",
        y="Average Marks",
        text="Average Marks",
        color="Average Marks",
        color_continuous_scale="Blues",
        title="Average Marks per Subject"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title="Subject",
        yaxis_title="Average Marks (out of 100)",
        yaxis=dict(range=[0, 105]),
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig


def create_percentage_histogram(df: pd.DataFrame, col_name: str = "percentage") -> go.Figure:
    """Histogram showing distribution of student percentages.

    Args:
        df (pd.DataFrame): Filtered student dataset.
        col_name (str): Column name for percentage values.

    Returns:
        go.Figure: Plotly histogram figure.
    """
    if col_name not in df.columns or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Percentage column unavailable", showarrow=False, font=dict(size=16))
        return fig

    fig = px.histogram(
        df,
        x=col_name,
        nbins=15,
        title="Distribution of Student Percentages",
        color_discrete_sequence=["#3b82f6"],
        marginal="box"
    )
    fig.update_layout(
        xaxis_title="Percentage (%)",
        yaxis_title="Count of Students",
        bargap=0.05,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig


def create_grade_donut_chart(df: pd.DataFrame, col_name: str = "grade") -> go.Figure:
    """Donut chart depicting student grade distribution.

    Args:
        df (pd.DataFrame): Filtered student dataset.
        col_name (str): Column name for grades.

    Returns:
        go.Figure: Plotly donut pie chart figure.
    """
    if col_name not in df.columns or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Grade column unavailable", showarrow=False, font=dict(size=16))
        return fig

    grade_counts = df[col_name].value_counts().reset_index()
    grade_counts.columns = ["Grade", "Count"]

    # Defined color map for grades
    color_map = {
        "A+": "#10b981",
        "A": "#3b82f6",
        "B": "#6366f1",
        "C": "#f59e0b",
        "D": "#f97316",
        "F": "#ef4444"
    }

    fig = px.pie(
        grade_counts,
        names="Grade",
        values="Count",
        hole=0.45,
        title="Grade Distribution",
        color="Grade",
        color_discrete_map=color_map
    )
    fig.update_traces(textinfo="percent+label", hoverinfo="label+value+percent")
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig


def create_department_box_plot(df: pd.DataFrame) -> go.Figure:
    """Box plot of overall percentage across departments.

    Args:
        df (pd.DataFrame): Filtered student dataset.

    Returns:
        go.Figure: Plotly box plot figure.
    """
    if "department" not in df.columns or "percentage" not in df.columns or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Department / Percentage data unavailable", showarrow=False, font=dict(size=16))
        return fig

    fig = px.box(
        df,
        x="department",
        y="percentage",
        color="department",
        title="Percentage Distribution by Department",
        points="all"
    )
    fig.update_layout(
        xaxis_title="Department",
        yaxis_title="Percentage (%)",
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig


def create_attendance_scatter_plot(df: pd.DataFrame) -> go.Figure:
    """Scatter plot showing relationship between Attendance and Percentage.

    Args:
        df (pd.DataFrame): Filtered student dataset.

    Returns:
        go.Figure: Plotly scatter plot figure with trendline.
    """
    if "attendance_percent" not in df.columns or "percentage" not in df.columns or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Attendance / Percentage data unavailable", showarrow=False, font=dict(size=16))
        return fig

    try:
        fig = px.scatter(
            df,
            x="attendance_percent",
            y="percentage",
            color="department" if "department" in df.columns else None,
            hover_data=["name"] if "name" in df.columns else None,
            title="Attendance % vs Overall Percentage",
            trendline="ols" if len(df) > 2 else None
        )
    except Exception:
        fig = px.scatter(
            df,
            x="attendance_percent",
            y="percentage",
            title="Attendance % vs Overall Percentage"
        )

    fig.update_layout(
        xaxis_title="Attendance (%)",
        yaxis_title="Overall Percentage (%)",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig


def create_subject_correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    """Correlation heatmap across subjects and attendance.

    Args:
        df (pd.DataFrame): Filtered student dataset.

    Returns:
        go.Figure: Plotly correlation heatmap figure.
    """
    cols_to_check = [col for col in SUBJECT_COLUMNS if col in df.columns]
    if "attendance_percent" in df.columns:
        cols_to_check.append("attendance_percent")
    if "percentage" in df.columns:
        cols_to_check.append("percentage")

    if len(cols_to_check) < 2 or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Insufficient numeric columns for correlation", showarrow=False, font=dict(size=16))
        return fig

    corr_matrix = df[cols_to_check].corr().round(2)

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Subject & Metric Correlation Heatmap",
        color_continuous_scale="RdBu_r"
    )
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig


def create_semester_line_chart(df: pd.DataFrame) -> go.Figure:
    """Line chart showing average percentage trend across semesters.

    Args:
        df (pd.DataFrame): Filtered student dataset.

    Returns:
        go.Figure: Plotly line chart figure.
    """
    if "semester" not in df.columns or "percentage" not in df.columns or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Semester / Percentage data unavailable", showarrow=False, font=dict(size=16))
        return fig

    sem_avg = df.groupby("semester")["percentage"].mean().reset_index()
    sem_avg["percentage"] = sem_avg["percentage"].round(2)
    sem_avg["semester"] = "Semester " + sem_avg["semester"].astype(str)

    fig = px.line(
        sem_avg,
        x="semester",
        y="percentage",
        markers=True,
        title="Average Percentage by Semester",
        color_discrete_sequence=["#10b981"]
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    fig.update_layout(
        xaxis_title="Semester",
        yaxis_title="Average Percentage (%)",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig
