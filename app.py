import streamlit as st
import pandas as pd
from PIL import Image

# Logo
logo = Image.open("logo.png")

# Page Settings
st.set_page_config(
    page_title="Student Result Analysis System",
    page_icon=logo,
    layout="wide"
)

# Header
st.image(logo, width=150)
st.title("🎓 Student Result Analysis System")
st.markdown("### Analyze Student Results Easily")

# File Upload
file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if file is not None:

    df = pd.read_csv(file)

    if len(df.columns) < 3:
        st.error("Minimum columns required: RollNo, Name and at least one Subject")
        st.stop()

    # Subjects = all columns after RollNo and Name
    subjects = list(df.columns[2:])

    # Total Marks
    df["Total"] = df[subjects].sum(axis=1)

    # Percentage
    max_marks = len(subjects) * 100
    df["Percentage"] = round(
        (df["Total"] / max_marks) * 100,
        2
    )

    # Pass / Fail
    df["Result"] = df["Percentage"].apply(
        lambda x: "Pass" if x >= 33 else "Fail"
    )

    # Grade System
    def grade(p):
        if p >= 90:
            return "A+"
        elif p >= 75:
            return "A"
        elif p >= 60:
            return "B"
        elif p >= 45:
            return "C"
        elif p >= 33:
            return "D"
        else:
            return "F"

    df["Grade"] = df["Percentage"].apply(grade)

    # Student Table
    st.subheader("📋 Student Records")
    st.dataframe(df)

    # Search Student
    st.subheader("🔍 Search Student")

    search = st.text_input(
        "Enter Roll Number or Name"
    )

    if search:
        result = df[
            df.astype(str)
            .apply(
                lambda x: x.str.contains(
                    search,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

        st.dataframe(result)

    # Statistics
    st.subheader("📊 Overall Statistics")

    topper = df.loc[df["Percentage"].idxmax()]
    lowest = df.loc[df["Percentage"].idxmin()]

    pass_percent = round(
        (
            len(df[df["Result"] == "Pass"])
            / len(df)
        ) * 100,
        2
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Topper",
        topper["Name"]
    )

    col2.metric(
        "Highest %",
        f"{topper['Percentage']}%"
    )

    col3.metric(
        "Average %",
        round(df["Percentage"].mean(), 2)
    )

    col4.metric(
        "Pass %",
        f"{pass_percent}%"
    )

    st.info(
        f"Lowest Scorer: {lowest['Name']} ({lowest['Percentage']}%)"
    )

    # Subject Wise Average
    st.subheader("📈 Subject Wise Average")
    st.bar_chart(df[subjects].mean())

    # Student Performance
    st.subheader("🏆 Student Performance")
    chart_df = df.set_index("Name")
    st.bar_chart(chart_df["Percentage"])

    # Result Distribution
    st.subheader("✅ Pass / ❌ Fail Distribution")
    result_counts = df["Result"].value_counts()
    st.bar_chart(result_counts)

    # Top 5 Students
    st.subheader("🥇 Top 5 Students")

    top5 = df.sort_values(
        by="Percentage",
        ascending=False
    ).head(5)

    st.dataframe(
        top5[
            [
                "RollNo",
                "Name",
                "Percentage",
                "Grade"
            ]
        ]
    )

    # Download Result
    csv = df.to_csv(index=False)

    st.download_button(
        label="⬇ Download Analyzed Result",
        data=csv,
        file_name="result_analysis.csv",
        mime="text/csv"
    )
