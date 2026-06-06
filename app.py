import streamlit as st
import pandas as pd

st.title("Student Result Analysis System")

file = st.file_uploader(
    "Upload Student CSV File",
    type=["csv"]
)

if file is not None:

    df = pd.read_csv(file)

    subjects = ["Maths","Physics","Chemistry","English","Computer"]

    df["Total"] = df[subjects].sum(axis=1)

    df["Percentage"] = round(
        (df["Total"] / 500) * 100, 2
    )

    def grade(p):
        if p >= 90:
            return "A+"
        elif p >= 75:
            return "A"
        elif p >= 60:
            return "B"
        elif p >= 40:
            return "C"
        else:
            return "F"

    df["Grade"] = df["Percentage"].apply(grade)

    df["Result"] = df["Percentage"].apply(
        lambda x: "Pass" if x >= 33 else "Fail"
    )

    st.subheader("Student Result Table")
    st.dataframe(df)

    st.subheader("Topper")

    topper = df.loc[df["Percentage"].idxmax()]

    st.success(
        f"{topper['Name']} ({topper['Percentage']}%)"
    )

    st.subheader("Statistics")

    st.write(
        "Average Percentage:",
        round(df["Percentage"].mean(),2)
    )

    st.write(
        "Pass Students:",
        len(df[df["Result"]=="Pass"])
    )

    st.write(
        "Fail Students:",
        len(df[df["Result"]=="Fail"])
    )

    st.subheader("Subject Average")

    st.bar_chart(df[subjects].mean())

    st.subheader("Percentage Comparison")

    chart_data = df.set_index("Name")["Percentage"]

    st.bar_chart(chart_data)
