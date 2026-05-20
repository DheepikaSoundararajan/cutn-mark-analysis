import streamlit as st
import pandas as pd
import plotly.express as px

from utils.firebase_config import db

from analytics.attendance_marks import (
    calculate_attendance_mark
)


def show_student_dashboard(register_number):

    st.subheader(
        f"🎓 Student Dashboard"
    )

    # ==================================================
    # FETCH STUDENT DATA
    # ==================================================

    docs = db.collection(
        "marks"
    ).stream()

    data_list = []

    for doc in docs:

        data = doc.to_dict()

        if (
            data["register_number"]
            == register_number
        ):

            data_list.append(data)

    if len(data_list) == 0:

        st.warning(
            "No student data found."
        )

        return

    df = pd.DataFrame(data_list)

    # ==================================================
    # ATTENDANCE MARK
    # ==================================================

    df["attendance_mark"] = (

        df["attendance"]

        .apply(
            calculate_attendance_mark
        )

    )

    # ==================================================
    # GPA CALCULATION
    # ==================================================

    average_mark = round(

        df["mark"].mean(),

        2

    )

    gpa = round(

        (average_mark / 10),

        2

    )

    attendance_avg = round(

        df["attendance"].mean(),

        2

    )

    weak_subjects = df[
        df["mark"] < 50
    ]["subject"].tolist()

    # ==================================================
    # KPI CARDS
    # ==================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "GPA",
        gpa
    )

    c2.metric(
        "Average Mark",
        average_mark
    )

    c3.metric(
        "Attendance %",
        f"{attendance_avg}%"
    )

    c4.metric(
        "Weak Subjects",
        len(weak_subjects)
    )

    st.divider()

    # ==================================================
    # SUBJECT OVERVIEW TABLE
    # ==================================================

    st.subheader(
        "📘 Semester Subject Overview"
    )

    overview_df = df[[

        "subject",
        "mark",
        "attendance",
        "attendance_mark"

    ]]

    st.dataframe(
        overview_df,
        use_container_width=True
    )

    # ==================================================
    # TABS
    # ==================================================

    tab1, tab2, tab3, tab4 = st.tabs([

        "📊 Performance",

        "📈 Attendance",

        "🎯 CO Analytics",

        "⚠️ Weak Areas"

    ])

    # ==================================================
    # PERFORMANCE TAB
    # ==================================================

    with tab1:

        st.subheader(
            "📊 Subject Performance"
        )

        fig1 = px.bar(

            df,

            x="subject",

            y="mark",

            color="mark",

            text="mark",

            title="Subject Wise Marks"

        )

        st.plotly_chart(

            fig1,

            use_container_width=True

        )

        st.subheader(
            "📈 Mark Trend"
        )

        fig2 = px.line(

            df,

            x="subject",

            y="mark",

            markers=True,

            title="Performance Trend"

        )

        st.plotly_chart(

            fig2,

            use_container_width=True

        )

    # ==================================================
    # ATTENDANCE TAB
    # ==================================================

    with tab2:

        st.subheader(
            "📈 Attendance Analysis"
        )

        fig3 = px.pie(

            df,

            names="subject",

            values="attendance",

            title="Attendance Distribution"

        )

        st.plotly_chart(

            fig3,

            use_container_width=True

        )

        st.subheader(
            "🎯 Attendance Marks"
        )

        fig4 = px.bar(

            df,

            x="subject",

            y="attendance_mark",

            color="attendance_mark",

            text="attendance_mark",

            title="Attendance Internal Marks"

        )

        st.plotly_chart(

            fig4,

            use_container_width=True

        )

    # ==================================================
    # CO ANALYTICS TAB
    # ==================================================

    with tab3:

        st.subheader(
            "🎯 CO Attainment Analysis"
        )

        co_docs = db.collection(
            "co_mapping"
        ).stream()

        co_list = []

        for doc in co_docs:

            co_list.append(
                doc.to_dict()
            )

        co_df = pd.DataFrame(
            co_list
        )

        co_analysis = []

        for _, row in df.iterrows():

            subject = row["subject"]

            subject_co = co_df[
                co_df["subject"]
                == subject
            ]

            for _, co_row in subject_co.iterrows():

                co_number = (
                    co_row["co_number"]
                    .lower()
                )

                score = row.get(
                    co_number,
                    0
                )

                status = "Strong"

                if score < 10:

                    status = "Weak"

                elif score < 15:

                    status = "Average"

                co_analysis.append({

                    "Subject":
                    subject,

                    "CO Description":
                    co_row[
                        "co_statement"
                    ],

                    "Score":
                    score,

                    "Target":
                    co_row[
                        "target_percentage"
                    ],

                    "Status":
                    status

                })

        co_analysis_df = pd.DataFrame(
            co_analysis
        )

        st.dataframe(

            co_analysis_df,

            use_container_width=True

        )

        fig5 = px.bar(

            co_analysis_df,

            x="CO Description",

            y="Score",

            color="Status",

            title="CO Performance Analysis"

        )

        st.plotly_chart(

            fig5,

            use_container_width=True

        )

    # ==================================================
    # WEAK AREAS TAB
    # ==================================================

    with tab4:

        st.subheader(
            "⚠️ Weak Subject Detection"
        )

        weak_df = df[

            df["mark"] < 50

        ][[

            "subject",

            "mark",

            "attendance"

        ]]

        if len(weak_df) == 0:

            st.success(
                "No weak subjects detected!"
            )

        else:

            st.dataframe(
                weak_df
            )

        st.subheader(
            "📉 Weak CO Areas"
        )

        weak_co = co_analysis_df[

            co_analysis_df["Status"]
            == "Weak"

        ]

        if len(weak_co) == 0:

            st.success(
                "No weak CO areas detected!"
            )

        else:

            st.dataframe(
                weak_co
            )

    # ==================================================
    # DOWNLOAD REPORT
    # ==================================================

    st.divider()

    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        label="📄 Download Student Report",

        data=csv,

        file_name=f"{register_number}_report.csv",

        mime="text/csv"

    )