import streamlit as st
import pandas as pd
import plotly.express as px

from analytics.gpa import calculate_gpa
from analytics.ai_insights import generate_ai_insight

from utils.firebase_config import db


def show_admin_dashboard():

    st.subheader("Admin Analytics Dashboard")

    docs = db.collection("marks").stream()

    data_list = []

    for doc in docs:
        data_list.append(doc.to_dict())

    if len(data_list) == 0:
        st.warning("No marks data found.")
        return

    df = pd.DataFrame(data_list)

    st.subheader("Analytics Filters")

    selected_subject = st.selectbox(
        "Select Subject",
        df["subject"].unique()
    )

    filtered_df = df[
        df["subject"] == selected_subject
    ]

    marks = filtered_df["mark"].tolist()

    overall_gpa = calculate_gpa(marks)

    passed = len([m for m in marks if m >= 50])

    failed = len(marks) - passed

    pass_percentage = round(
        (passed / len(marks)) * 100,
        2
    )

    insight = generate_ai_insight(
        pass_percentage
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Students",
        len(filtered_df)
    )

    c2.metric(
        "Pass Percentage",
        f"{pass_percentage}%"
    )

    c3.metric(
        "Failed Students",
        failed
    )

    c4.metric(
        "Overall GPA",
        overall_gpa
    )

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "Overview",
        "Analytics",
        "Reports",
        "AI Insights"
    ])

    with tab1:

        st.subheader("Institutional Overview")

        fig1 = px.bar(
            filtered_df,
            x="student_name",
            y="mark",
            color="subject",
            title="Student Performance"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with tab2:

        st.subheader("Advanced Analytics")

        fig2 = px.histogram(
            filtered_df,
            x="mark",
            nbins=10,
            title="Marks Distribution"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        fig3 = px.pie(
            filtered_df,
            names="student_name",
            values="mark",
            title="Marks Contribution"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    with tab3:

        st.subheader("Download Reports")

        st.dataframe(filtered_df)

        csv = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Institutional Report",
            data=csv,
            file_name="admin_report.csv",
            mime="text/csv"
        )

    with tab4:

        st.subheader("AI Institutional Insight")

        st.info(insight)