import streamlit as st
import firebase_admin

from firebase_admin import (
    credentials,
    firestore
)

# ==========================================
# FIREBASE INITIALIZATION
# ==========================================

if not firebase_admin._apps:

    firebase_credentials = dict(
        st.secrets["firebase"]
    )

    cred = credentials.Certificate(
        firebase_credentials
    )

    firebase_admin.initialize_app(
        cred
    )

db = firestore.client()