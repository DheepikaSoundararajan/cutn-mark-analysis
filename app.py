import os
import streamlit as st

from utils.firebase_config import db

from dashboards.admin_dashboard import (
    show_admin_dashboard
)

from dashboards.staff_dashboard import (
    show_staff_dashboard
)

from dashboards.student_dashboard import (
    show_student_dashboard
)

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Academic Analytics Portal",
    layout="wide"
)

# ==================================================
# LOAD CSS
# ==================================================

def load_css():

    css_path = os.path.join(
        "styles",
        "style.css"
    )

    with open(css_path) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# ==================================================
# SESSION STATE
# ==================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "name" not in st.session_state:
    st.session_state.name = ""

if "register_number" not in st.session_state:
    st.session_state.register_number = ""

if "subject" not in st.session_state:
    st.session_state.subject = ""

# ==================================================
# LOGIN PAGE
# ==================================================

if not st.session_state.logged_in:

    # HEADER

    col_logo, col_title = st.columns([1,5])

    with col_logo:

        st.image(
            "assets/logo.png",
            width=120
        )

    with col_title:

        st.title(
            "Central University of Tamil Nadu"
        )

        st.subheader(
            "Academic Analytics Portal"
        )

        st.caption(
            "Outcome Based Education System"
        )

    st.divider()

    # MAIN LAYOUT

    left, right = st.columns([3,2])

    # LEFT IMAGE

    with left:

        st.image(
            "assets/university.jpg",
            use_container_width=True
        )

    # LOGIN CARD

    with right:

        st.markdown("## 🔐 Login Portal")

        role = st.selectbox(
            "Select Role",
            ["Admin", "Staff", "Student"]
        )

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password (DOB)",
            type="password"
        )

        login_button = st.button(
            "Login",
            use_container_width=True
        )

        # LOGIN LOGIC

        if login_button:

            login_success = False

            # ADMIN LOGIN

            if role == "Admin":

                users = db.collection(
                    "admin"
                ).stream()

                for user in users:

                    data = user.to_dict()

                    if (
                        data["username"] == username
                        and
                        data["dob"] == password
                    ):

                        login_success = True

                        st.session_state.logged_in = True
                        st.session_state.role = role
                        st.session_state.name = data["name"]

                        st.rerun()

            # STAFF LOGIN

            elif role == "Staff":

                users = db.collection(
                    "staff"
                ).stream()

                for user in users:

                    data = user.to_dict()

                    if (
                        data["username"] == username
                        and
                        data["dob"] == password
                    ):

                        login_success = True

                        st.session_state.logged_in = True
                        st.session_state.role = role
                        st.session_state.name = data["name"]

                        st.session_state.subject = (
                            data["subject"]
                        )

                        st.rerun()

            # STUDENT LOGIN

            elif role == "Student":

                student_doc = db.collection(
                    "student"
                ).document(
                    username
                ).get()

                if student_doc.exists:

                    data = student_doc.to_dict()

                    if data["dob"] == password:

                        login_success = True

                        st.session_state.logged_in = True

                        st.session_state.role = role

                        st.session_state.name = (
                            data.get(
                                "student_name",
                                "Student"
                            )
                        )

                        st.session_state.register_number = (
                            data.get(
                                "register_number",
                                username
                            )
                        )

                        st.rerun()

            if not login_success:

                st.error(
                    "Invalid Username or Password"
                )

# ==================================================
# DASHBOARD
# ==================================================

else:

    col1, col2 = st.columns([8,1])

    with col1:

        st.title(
            f"{st.session_state.role} Dashboard"
        )

    with col2:

        if st.button("Logout"):

            st.session_state.logged_in = False
            st.session_state.role = ""
            st.session_state.name = ""
            st.session_state.register_number = ""
            st.session_state.subject = ""

            st.rerun()

    st.success(
        f"Welcome {st.session_state.name}"
    )

    st.markdown("---")

    # ROLE DASHBOARD

    if st.session_state.role == "Admin":

        show_admin_dashboard()

    elif st.session_state.role == "Staff":

        show_staff_dashboard(
            st.session_state.subject
        )

    elif st.session_state.role == "Student":

        show_student_dashboard(
            st.session_state.register_number
        )