
import streamlit as st
import pandas as pd
from PIL import Image

# ===== LOGO =====
logo = Image.open("logo.png")

st.set_page_config(
    page_title="Student Result Analysis System",
    page_icon=logo,
    layout="wide"
)

# Session Storage
if "classes" not in st.session_state:
    st.session_state.classes = {}
if "students" not in st.session_state:
    st.session_state.students = []

# Header
st.image(logo, width=120)
st.title("MONNET DAV PUBLIC SCHOOL")
st.subheader("Student Result Analysis & Management System")
st.caption("Created By: Aastha Dansena | Class XII (Science)")

tab1, tab2, tab3 = st.tabs(["Class Setup", "Student Entry", "Analysis"])

with tab1:
    st.header("Create / Edit Class")

    cname = st.text_input("Class Name")
    nsub = st.number_input("Number of Subjects", min_value=1, value=5)

    subjects = []

    for i in range(int(nsub)):
        c1, c2 = st.columns(2)

        sname = c1.text_input(f"Subject {i+1} Name", key=f"s{i}")
        smax = c2.number_input(
            f"Maximum Marks {i+1}",
            min_value=1,
            value=100,
            key=f"m{i}"
        )

        if sname:
            subjects.append(
                {"name": sname, "max": smax}
            )

    if st.button("Save Class"):
        if cname and subjects:
            st.session_state.classes[cname] = subjects
            st.success("Class Saved Successfully")

with tab2:

    st.header("Student Entry")

    if st.session_state.classes:

        selected_class = st.selectbox(
            "Select Class",
            list(st.session_state.classes.keys())
        )

        cls_subjects = st.session_state.classes[selected_class]

        name = st.text_input("Student Name")
        father = st.text_input("Father Name")
        mother = st.text_input("Mother Name")
        roll = st.text_input("Roll Number")
        section = st.text_input("Section")

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        st.subheader("Enter Marks")

        marks = {}
        total_obt = 0
        total_max = 0

        for sub in cls_subjects:

            m = st.number_input(
                f"{sub['name']} (Max {sub['max']})",
                min_value=0.0,
                max_value=float(sub['max']),
                value=0.0,
                key=f"{roll}_{sub['name']}"
            )

            marks[sub["name"]] = m

            total_obt += m
            total_max += sub["max"]

        if st.button("Save Student"):

            percentage = round(
                (total_obt / total_max) * 100,
                2
            )

            result = "Pass" if percentage >= 33 else "Fail"

            st.session_state.students.append({
                "Class": selected_class,
                "Name": name,
                "Father": father,
                "Mother": mother,
                "RollNo": roll,
                "Section": section,
                "Gender": gender,
                "Total": total_obt,
                "MaxTotal": total_max,
                "Percentage": percentage,
                "Result": result,
                **marks
            })

            st.success("Student Saved Successfully")

    else:
        st.warning("Please Create a Class First")

with tab3:

    st.header("Analysis Dashboard")

    if st.session_state.students:

        df = pd.DataFrame(st.session_state.students)

        df["Rank"] = df["Percentage"].rank(
            method="dense",
            ascending=False
        ).astype(int)

        st.dataframe(df)

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Students", len(df))

        c2.metric(
            "Average Percentage",
            round(df["Percentage"].mean(), 2)
        )

        c3.metric(
            "Pass Percentage",
            round(
                (df["Result"] == "Pass").mean() * 100,
                2
            )
        )

        c4.metric(
            "Highest Percentage",
            round(df["Percentage"].max(), 2)
        )

        st.subheader("Top 10 Merit List")

        st.dataframe(
            df.sort_values(
                "Percentage",
                ascending=False
            ).head(10)
        )

        st.subheader("Class Wise Average")

        st.bar_chart(
            df.groupby("Class")["Percentage"].mean()
        )

        st.subheader("Pass / Fail Distribution")

        st.bar_chart(
            df["Result"].value_counts()
        )

        student = st.selectbox(
            "Select Student Report Card",
            df["Name"].tolist()
        )

        rec = df[df["Name"] == student].iloc[0]

        st.subheader("Student Report Card")

        st.write("Name :", rec["Name"])
        st.write("Father :", rec["Father"])
        st.write("Class :", rec["Class"])
        st.write("Roll No :", rec["RollNo"])
        st.write("Percentage :", rec["Percentage"])
        st.write("Rank :", rec["Rank"])
        st.write("Result :", rec["Result"])

        csv = df.to_csv(index=False)

        st.download_button(
            "Download Full Result",
            csv,
            "school_result.csv",
            "text/csv"
        )

    else:
        st.info("No Student Data Available")
