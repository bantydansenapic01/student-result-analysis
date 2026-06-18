import streamlit as st
import pandas as pd
from PIL import Image

# ---------------- PAGE SETUP ----------------

try:
    logo = Image.open("logo.png")

    st.set_page_config(
        page_title="Student Result Analysis System",
        page_icon=logo,
        layout="wide"
    )

except:

    st.set_page_config(
        page_title="Student Result Analysis System",
        page_icon="🎓",
        layout="wide"
    )

# ---------------- SESSION STORAGE ----------------

if "classes" not in st.session_state:
    st.session_state.classes = {}

if "students" not in st.session_state:
    st.session_state.students = []

# ---------------- HEADER ----------------

try:
    st.image(logo, width=120)
except:
    pass

st.title("MONNET DAV PUBLIC SCHOOL")

st.subheader(
    "STUDENT RESULT ANALYSIS & MANAGEMENT SYSTEM"
)

st.markdown("""
### Developed By

- Aastha Dansena
- Khushboo Patel

**Class XII (Science)**

**Academic Session 2026–27**
""")

# ---------------- TABS ----------------

tab1, tab2, tab3 = st.tabs([
    "Class Management",
    "Student Management",
    "Analysis"
])

# ==================================================
# CLASS MANAGEMENT
# ==================================================

with tab1:

    st.header("Create New Class")

    class_name = st.text_input(
        "Class Name"
    )

    n_subjects = st.number_input(
        "Number of Subjects",
        min_value=1,
        max_value=20,
        value=5
    )

    subjects = []

    for i in range(int(n_subjects)):

        c1, c2 = st.columns(2)

        subject_name = c1.text_input(
            f"Subject {i+1}"
        )

        max_marks = c2.number_input(
            f"Max Marks {i+1}",
            min_value=1,
            value=100
        )

        if subject_name:

            subjects.append({
                "name": subject_name,
                "max": max_marks
            })

    if st.button("Save Class"):

        if class_name and subjects:

            st.session_state.classes[
                class_name
            ] = subjects

            st.success(
                "Class Saved Successfully"
            )

    st.markdown("---")

    st.subheader("Delete Class")

    if st.session_state.classes:

        delete_class = st.selectbox(
            "Select Class To Delete",
            list(
                st.session_state.classes.keys()
            )
        )

        if st.button("Delete Selected Class"):

            del st.session_state.classes[
                delete_class
            ]

            st.success(
                "Class Deleted Successfully"
            )

    st.markdown("---")

    st.subheader("Reset Complete System")

    if st.button("Delete All Data"):

        st.session_state.classes = {}
        st.session_state.students = []

        st.success(
            "All Data Deleted Successfully"
        )
# ==================================================
# STUDENT MANAGEMENT
# ==================================================

with tab2:

    st.header("Student Entry")

    if not st.session_state.classes:

        st.warning(
            "Please Create A Class First"
        )

    else:

        selected_class = st.selectbox(
            "Select Class",
            list(
                st.session_state.classes.keys()
            )
        )

        class_subjects = (
            st.session_state.classes[
                selected_class
            ]
        )

        name = st.text_input(
            "Student Name"
        )

        father = st.text_input(
            "Father Name"
        )

        mother = st.text_input(
            "Mother Name"
        )

        roll = st.text_input(
            "Roll Number"
        )

        section = st.text_input(
            "Section"
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female",
                "Other"
            ]
        )

        st.subheader(
            "Enter Subject Marks"
        )

        marks = {}

        total_obt = 0
        total_max = 0

        for sub in class_subjects:

            mark = st.number_input(
                f"{sub['name']} (Max {sub['max']})",
                min_value=0.0,
                max_value=float(
                    sub["max"]
                ),
                value=0.0,
                key=f"{roll}_{sub['name']}"
            )

            marks[
                sub["name"]
            ] = mark

            total_obt += mark
            total_max += sub["max"]

        if st.button(
            "Save Student"
        ):

            duplicate = False

            for s in st.session_state.students:

                if s["RollNo"] == roll:

                    duplicate = True
                    break

            if duplicate:

                st.error(
                    "Roll Number Already Exists"
                )

            else:

                percentage = round(
                    (
                        total_obt
                        /
                        total_max
                    )
                    * 100,
                    2
                )

                if percentage >= 90:
                    grade = "A+"

                elif percentage >= 75:
                    grade = "A"

                elif percentage >= 60:
                    grade = "B"

                elif percentage >= 45:
                    grade = "C"

                elif percentage >= 33:
                    grade = "D"

                else:
                    grade = "F"

                result = (
                    "Pass"
                    if percentage >= 33
                    else "Fail"
                )

                st.session_state.students.append({

                    "Class":
                    selected_class,

                    "Name":
                    name,

                    "Father":
                    father,

                    "Mother":
                    mother,

                    "RollNo":
                    roll,

                    "Section":
                    section,

                    "Gender":
                    gender,

                    "Total":
                    total_obt,

                    "MaxTotal":
                    total_max,

                    "Percentage":
                    percentage,

                    "Grade":
                    grade,

                    "Result":
                    result,

                    **marks
                })

                st.success(
                    "Student Saved Successfully"
                )

    st.markdown("---")

    st.subheader(
        "Search Student"
    )

    search_text = st.text_input(
        "Search By Name Or Roll Number"
    )

    if (
        search_text
        and
        st.session_state.students
    ):

        temp_df = pd.DataFrame(
            st.session_state.students
        )

        result = temp_df[
            temp_df.astype(str)
            .apply(
                lambda x:
                x.str.contains(
                    search_text,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

        st.dataframe(result)

    st.markdown("---")

    st.subheader(
        "Delete Student"
    )

    if st.session_state.students:

        delete_roll = st.selectbox(
            "Select Roll Number",
            [
                s["RollNo"]
                for s in
                st.session_state.students
            ],
            key="delete_student"
        )

        if st.button(
            "Delete Student"
        ):

            st.session_state.students = [

                s
                for s in
                st.session_state.students

                if s["RollNo"]
                != delete_roll
            ]

            st.success(
                "Student Deleted"
            )
# ==================================================
# ANALYSIS DASHBOARD (PART 3)
# ==================================================

with tab3:

    st.header("Analysis Dashboard")

    if not st.session_state.students:

        st.info(
            "No Student Data Available"
        )

    else:

        df = pd.DataFrame(
            st.session_state.students
        )

        # -----------------------
        # OVERALL RANK
        # -----------------------

        df["Overall Rank"] = (
            df["Percentage"]
            .rank(
                ascending=False,
                method="dense"
            )
            .astype(int)
        )

        # -----------------------
        # CLASS WISE RANK
        # -----------------------

        df["Class Rank"] = (
            df.groupby("Class")
            ["Percentage"]
            .rank(
                ascending=False,
                method="dense"
            )
            .astype(int)
        )

        st.subheader(
            "All Student Records"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        # -----------------------
        # TOPPER
        # -----------------------

        topper = df.loc[
            df["Percentage"].idxmax()
        ]

        lowest = df.loc[
            df["Percentage"].idxmin()
        ]

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Students",
            len(df)
        )

        c2.metric(
            "Average %",
            round(
                df["Percentage"]
                .mean(),
                2
            )
        )

        c3.metric(
            "Highest %",
            round(
                df["Percentage"]
                .max(),
                2
            )
        )

        c4.metric(
            "Pass %",
            round(
                (
                    len(
                        df[
                            df["Result"]
                            ==
                            "Pass"
                        ]
                    )
                    /
                    len(df)
                ) * 100,
                2
            )
        )

        st.success(
            f"Overall Topper : "
            f"{topper['Name']} "
            f"({topper['Percentage']}%)"
        )

        st.warning(
            f"Lowest Scorer : "
            f"{lowest['Name']} "
            f"({lowest['Percentage']}%)"
        )

        # -----------------------
        # TOP 10 MERIT
        # -----------------------

        st.subheader(
            "Top 10 Merit List"
        )

        merit = df.sort_values(
            by="Percentage",
            ascending=False
        )

        st.dataframe(
            merit.head(10),
            use_container_width=True
        )

        # -----------------------
        # CLASS WISE MERIT
        # -----------------------

        st.subheader(
            "Class Wise Merit List"
        )

        selected_class = st.selectbox(
            "Select Class",
            sorted(
                df["Class"]
                .unique()
            ),
            key="class merit"
        )

        class_df = df[
            df["Class"]
            ==
            selected_class
        ]

        class_df = class_df.sort_values(
            by="Percentage",
            ascending=False
        )

        st.dataframe(
            class_df,
            use_container_width=True
        )

        # -----------------------
        # EDIT STUDENT
        # -----------------------

        st.markdown("---")

        st.subheader(
            "Edit Student"
        )

        edit_roll = st.selectbox(
            "Select Roll No To Edit",
            df["RollNo"]
            .tolist()
        )

        student_index = None

        for i, s in enumerate(
            st.session_state.students
        ):

            if (
                s["RollNo"]
                ==
                edit_roll
            ):

                student_index = i
                break

        if student_index is not None:

            student = (
                st.session_state.students[
                    student_index
                ]
            )

            new_name = st.text_input(
                "Name",
                value=student["Name"]
            )

            new_father = st.text_input(
                "Father Name",
                value=student["Father"]
            )

            new_section = st.text_input(
                "Section",
                value=student["Section"]
            )

            if st.button(
                "Update Student"
            ):

                st.session_state.students[
                    student_index
                ]["Name"] = new_name

                st.session_state.students[
                    student_index
                ]["Father"] = new_father

                st.session_state.students[
                    student_index
                ]["Section"] = new_section

                st.success(
                    "Student Updated"
                )
        # -----------------------
        # SUBJECT ANALYSIS
        # -----------------------

        subject_columns = [

            c for c in df.columns

            if c not in [

                "Class",
                "Name",
                "Father",
                "Mother",
                "RollNo",
                "Section",
                "Gender",

                "Total",
                "MaxTotal",

                "Percentage",
                "Grade",
                "Result",

                "Overall Rank",
                "Class Rank"
            ]
        ]

        if subject_columns:

            st.markdown("---")

            st.subheader(
                "Subject Wise Average"
            )

            st.bar_chart(
                df[subject_columns]
                .mean()
            )

            subject_analysis = []

            for sub in subject_columns:

                topper_name = df.loc[
                    df[sub].idxmax(),
                    "Name"
                ]

                subject_analysis.append({

                    "Subject":
                    sub,

                    "Average":
                    round(
                        df[sub].mean(),
                        2
                    ),

                    "Highest":
                    round(
                        df[sub].max(),
                        2
                    ),

                    "Lowest":
                    round(
                        df[sub].min(),
                        2
                    ),

                    "Topper":
                    topper_name
                })

            st.subheader(
                "Subject Analysis Table"
            )

            st.dataframe(
                pd.DataFrame(
                    subject_analysis
                ),
                use_container_width=True
            )

        # -----------------------
        # CLASS WISE AVERAGE
        # -----------------------

        st.markdown("---")

        st.subheader(
            "Class Wise Average"
        )

        class_avg = (
            df.groupby("Class")
            ["Percentage"]
            .mean()
        )

        st.bar_chart(
            class_avg
        )

        # -----------------------
        # PASS FAIL CHART
        # -----------------------

        st.markdown("---")

        st.subheader(
            "Pass / Fail Distribution"
        )

        pass_fail = (
            df["Result"]
            .value_counts()
        )

        st.bar_chart(
            pass_fail
        )

        # -----------------------
        # GRADE DISTRIBUTION
        # -----------------------

        st.markdown("---")

        st.subheader(
            "Grade Distribution"
        )

        grade_chart = (
            df["Grade"]
            .value_counts()
        )

        st.bar_chart(
            grade_chart
        )

        # -----------------------
        # STUDENT PERFORMANCE
        # -----------------------

        st.markdown("---")

        st.subheader(
            "Student Performance"
        )

        chart_df = (
            df.set_index("Name")
        )

        st.bar_chart(
            chart_df[
                "Percentage"
            ]
        )
        # -----------------------
        # CLASS TOPPERS
        # -----------------------

        st.markdown("---")

        st.subheader(
            "Class Toppers"
        )

        for cls in sorted(
            df["Class"].unique()
        ):

            temp = df[
                df["Class"] == cls
            ]

            topper = temp.loc[
                temp["Percentage"].idxmax()
            ]

            st.success(
                f"{cls} : "
                f"{topper['Name']} "
                f"({topper['Percentage']}%)"
            )

        # -----------------------
        # REPORT CARD
        # -----------------------

        st.markdown("---")

        st.subheader(
            "Student Report Card"
        )

        report_roll = st.selectbox(
            "Select Student",
            df["RollNo"].tolist(),
            key="report_card"
        )

        report_df = df[
            df["RollNo"] == report_roll
        ]

        if not report_df.empty:

            student = report_df.iloc[0]

            st.markdown(
                "# MONNET DAV PUBLIC SCHOOL"
            )

            st.markdown(
                "## REPORT CARD"
            )

            st.write(
                "Name:",
                student["Name"]
            )

            st.write(
                "Father:",
                student["Father"]
            )

            st.write(
                "Class:",
                student["Class"]
            )

            st.write(
                "Roll No:",
                student["RollNo"]
            )

            st.write(
                "Section:",
                student["Section"]
            )

            st.write(
                "Percentage:",
                student["Percentage"]
            )

            st.write(
                "Grade:",
                student["Grade"]
            )

            st.write(
                "Result:",
                student["Result"]
            )

            st.write(
                "Class Rank:",
                student["Class Rank"]
            )

            subject_columns = [

                c for c in df.columns

                if c not in [

                    "Class",
                    "Name",
                    "Father",
                    "Mother",
                    "RollNo",
                    "Section",
                    "Gender",

                    "Total",
                    "MaxTotal",

                    "Percentage",
                    "Grade",
                    "Result",

                    "Overall Rank",
                    "Class Rank"
                ]
            ]

            marks_table = pd.DataFrame({

                "Subject":
                subject_columns,

                "Marks":
                [
                    student[s]
                    for s in
                    subject_columns
                ]
            })

            st.dataframe(
                marks_table,
                use_container_width=True
            )

        # -----------------------
        # CSV EXPORT
        # -----------------------

        st.markdown("---")

        st.subheader(
            "Export Data"
        )

        csv = df.to_csv(
            index=False
        )

        st.download_button(

            label=
            "Download Full Result CSV",

            data=csv,

            file_name=
            "school_result.csv",

            mime="text/csv"
        )

        # -----------------------
        # DELETE ALL STUDENTS
        # -----------------------

        st.markdown("---")

        st.subheader(
            "Danger Zone"
        )

        if st.button(
            "Delete All Students"
        ):

            st.session_state.students = []

            st.success(
                "All Student Data Deleted"
            )
