"""
utils/data_loader.py

Data loading, validation, and preprocessing utility functions for the Student Analytics Dashboard.
"""

import os
from typing import Optional, List, Tuple
import pandas as pd
import streamlit as st


@st.cache_data
def load_default_data() -> pd.DataFrame:
    """Loads the default students.csv dataset from disk with caching.

    Returns:
        pd.DataFrame: Loaded student dataset.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_csv_path = os.path.join(base_dir, "data", "students.csv")

    if not os.path.exists(default_csv_path):
        st.error(f"Default dataset not found at {default_csv_path}. Please run data/generate_data.py first.")
        return pd.DataFrame()

    df = pd.read_csv(default_csv_path)
    return df


def calculate_grades_and_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Ensures total, percentage, and grade columns exist if subject columns are present.

    Args:
        df (pd.DataFrame): Raw uploaded or loaded dataframe.

    Returns:
        pd.DataFrame: DataFrame with percentage and grade attributes.
    """
    df = df.copy()

    # Identify numeric score columns if standard ones are present
    standard_subjects = ["Maths", "Python", "DBMS", "Data Structures", "Java"]
    present_subjects = [col for col in standard_subjects if col in df.columns]

    if present_subjects and ("percentage" not in df.columns or "total" not in df.columns):
        if "total" not in df.columns:
            df["total"] = df[present_subjects].sum(axis=1)
        if "percentage" not in df.columns:
            df["percentage"] = (df["total"] / (len(present_subjects) * 100)) * 100
            df["percentage"] = df["percentage"].round(2)

    if "percentage" in df.columns and "grade" not in df.columns:
        def assign_grade(pct: float) -> str:
            if pct >= 85:
                return "A+"
            elif pct >= 75:
                return "A"
            elif pct >= 65:
                return "B"
            elif pct >= 50:
                return "C"
            elif pct >= 40:
                return "D"
            else:
                return "F"

        df["grade"] = df["percentage"].apply(assign_grade)

    return df


def load_user_data(uploaded_file) -> Tuple[pd.DataFrame, bool]:
    """Loads dataset from uploaded CSV file or default CSV.

    Args:
        uploaded_file: Streamlit UploadedFile instance or None.

    Returns:
        Tuple[pd.DataFrame, bool]: (DataFrame, is_custom_dataset_flag)
    """
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df = calculate_grades_and_metrics(df)
            return df, True
        except Exception as e:
            st.error(f"Error reading uploaded CSV file: {str(e)}")
            st.info("Falling back to default student dataset.")
            return load_default_data(), False
    else:
        return load_default_data(), False


def detect_column_types(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """Separates dataframe columns into numeric and categorical lists.

    Args:
        df (pd.DataFrame): Input dataframe.

    Returns:
        Tuple[List[str], List[str]]: (numeric_cols, categorical_cols)
    """
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    return numeric_cols, categorical_cols
