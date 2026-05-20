import streamlit as st
import pandas as pd
import plotly.express as px

from analytics.pass_fail import (
    pass_fail_analysis
)

from analytics.weak_students import (
    weak_students
)

from analytics.attendance_marks import (
    calculate_attendance_mark
)

from utils.firebase_config import db


def show_staff_dashboard(staff_subject):

    st.subheader(
        f"👨‍🏫 {staff_subject} Faculty Dashboard"
    )

    # ==================================================
    # MARKS FILE FORMAT
    # ==================================================

    st.info(
        f"""
        ONLY {staff_subject} subject uploads allowed.

        CSV FORMAT:

        register_number,
        student_name,
        gender,
        dob,
        department,
        semester,
        subject,
        co1,
        co2,
        co3,
        co4,
        co5,
        mark,
        attendance
        """
    )

    # ==================================================
    # MARKS FILE UPLOAD
    # ==================================================

    marks_file = st.file_uploader(

        "Upload Subject Marks CSV",

        type=["csv"]

    )

    if marks_file is not None:

        marks_df = pd.read_csv(
            marks_file
        )

        required_columns = [

            "register_number",
            "student_name",
            "gender",
            "dob",
            "department",
            "semester",
            "subject",
            "co1",
            "co2",
            "co3",
            "co4",
            "co5",
            "mark",
            "attendance"

        ]

        if (

            list(marks_df.columns)

            != required_columns

        ):

            st.error(
                "Invalid CSV Format!"
            )

            st.stop()

        uploaded_subject = (
            marks_df["subject"]
            .iloc[0]
        )

        if uploaded_subject != staff_subject:

            st.error(

                f"""
                You can upload only
                {staff_subject} subject.
                """

            )

            st.stop()

        st.success(
            "Correct Subject Uploaded!"
        )

        st.dataframe(marks_df)

        # ==============================================
        # ATTENDANCE MARK
        # ==============================================

        marks_df["attendance_mark"] = (

            marks_df["attendance"]

            .apply(
                calculate_attendance_mark
            )

        )

        # ==============================================
        # STORE FIREBASE
        # ==============================================

        for _, row in marks_df.iterrows():

            data = row.to_dict()

            doc_id = (

                str(data["register_number"])

                + "_"

                + str(data["subject"])

            )

            db.collection("marks").document(
                doc_id
            ).set(data)

        st.success(
            "Marks Uploaded Successfully!"
        )

    # ==================================================
    # CO FILE FORMAT
    # ==================================================

    st.info(
        f"""
        Upload ONLY {staff_subject} CO file.

        CO FORMAT:

        subject,
        co_number,
        co_statement,
        max_mark,
        target_percentage
        """
    )

    # ==================================================
    # CO FILE UPLOAD
    # ==================================================

    co_file = st.file_uploader(

        "Upload CO Mapping CSV",

        type=["csv"]

    )

    if co_file is not None:

        co_df = pd.read_csv(
            co_file
        )

        required_co_columns = [

            "subject",
            "co_number",
            "co_statement",
            "max_mark",
            "target_percentage"

        ]

        if (

            list(co_df.columns)

            != required_co_columns

        ):

            st.error(
                "Invalid CO CSV Format!"
            )

            st.stop()

        uploaded_subject = (
            co_df["subject"]
            .iloc[0]
        )

        if uploaded_subject != staff_subject:

            st.error(

                f"""
                Upload only
                {staff_subject} CO file.
                """

            )

            st.stop()

        st.success(
            "Correct CO File Uploaded!"
        )

        st.dataframe(co_df)

        # ==============================================
        # STORE CO
        # ==============================================

        for _, row in co_df.iterrows():

            data = row.to_dict()

            doc_id = (

                str(data["subject"])

                + "_"

                + str(data["co_number"])

            )

            db.collection(
                "co_mapping"
            ).document(
                doc_id
            ).set(data)

        st.success(
            "CO Mapping Uploaded!"
        )

    # ==================================================
    # FETCH SUBJECT DATA ONLY
    # ==================================================

    docs = db.collection(
        "marks"
    ).stream()

    data_list = []

    for doc in docs:

        data = doc.to_dict()

        if data["subject"] == staff_subject:

            data_list.append(data)

    if len(data_list) == 0:

        st.warning(
            "No subject data found."
        )

        return

    df = pd.DataFrame(data_list)

    # ==================================================
    # FILTERS
    # ==================================================

    col1, col2 = st.columns(2)

    with col1:

        department_filter = st.selectbox(

            "Department",

            sorted(
                df["department"].unique()
            )

        )

    with col2:

        semester_filter = st.selectbox(

            "Semester",

            sorted(
                df["semester"].unique()
            )

        )

    filtered_df = df[

        (df["department"]
         == department_filter)

        &

        (df["semester"]
         == semester_filter)

    ]

    st.dataframe(filtered_df)

    # ==================================================
    # ANALYTICS
    # ==================================================

    marks = filtered_df[
        "mark"
    ].tolist()

    students_data = []

    for _, row in filtered_df.iterrows():

        students_data.append({

            "name":
            row["student_name"],

            "mark":
            row["mark"]

        })

    passed, failed = (
        pass_fail_analysis(marks)
    )

    pass_percentage = round(

        (passed / len(marks)) * 100,

        2

    )

    weak = weak_students(
        students_data
    )

    # ==================================================
    # KPI
    # ==================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Students",
        len(filtered_df)
    )

    c2.metric(
        "Pass %",
        f"{pass_percentage}%"
    )

    c3.metric(
        "Passed",
        passed
    )

    c4.metric(
        "Weak Students",
        len(weak)
    )

    st.divider()

    # ==================================================
    # TABS
    # ==================================================

    tab1, tab2, tab3, tab4 = st.tabs([

        "📈 Performance",

        "📊 Attendance",

        "📄 Reports",

        "⚠️ Weak Students"

    ])

    # ==================================================
    # PERFORMANCE TAB
    # ==================================================

    with tab1:

        fig = px.bar(

            filtered_df,

            x="student_name",

            y="mark",

            color="mark",

            title=f"{staff_subject} Performance"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # ==================================================
    # ATTENDANCE TAB
    # ==================================================

    with tab2:

        st.subheader(
            "📊 Attendance Analytics"
        )

        attendance_fig = px.bar(

            filtered_df,

            x="student_name",

            y="attendance_mark",

            color="attendance_mark",

            title="Attendance Mark Analysis"

        )

        st.plotly_chart(

            attendance_fig,

            use_container_width=True

        )

        st.dataframe(

            filtered_df[[

                "student_name",

                "attendance",

                "attendance_mark"

            ]]

        )

    # ==================================================
    # REPORTS TAB
    # ==================================================

    with tab3:

        csv = filtered_df.to_csv(

            index=False

        ).encode("utf-8")

        st.download_button(

            label="Download Report",

            data=csv,

            file_name=f"{staff_subject}_report.csv",

            mime="text/csv"

        )

    # ==================================================
    # WEAK STUDENTS TAB
    # ==================================================

    with tab4:

        weak_df = pd.DataFrame(
            weak
        )

        st.dataframe(weak_df)