import streamlit as st


def apply_custom_css():

    theme = st.session_state.get(
        "theme",
        "Light",
    )

    if theme == "Dark":

        st.markdown(
            """
            <style>

            /* =================================================
               DARK THEME
            ================================================= */

            .stApp {
                background-color: #111827;
                color: #e5e7eb;
            }

            .main .block-container {
                color: #e5e7eb;
            }

            h1,
            h2,
            h3 {
                color: #f3f4f6 !important;
            }

            p,
            .stCaption {
                color: #9ca3af !important;
            }


            /* Sidebar */

            section[data-testid="stSidebar"] {
                background-color: #0f172a;
                border-right: 1px solid #273244;
            }

            section[data-testid="stSidebar"] a {
                color: #d1d5db !important;
            }

            section[data-testid="stSidebar"] a:hover {
                background-color: #1e293b;
            }


            /* Buttons */

            .stButton > button {
                background-color: #1f2937;
                color: #e5e7eb;
                border-color: #374151;
            }

            .stButton > button:hover {
                background-color: #374151;
                border-color: #4b5563;
            }

            .stButton > button[kind="primary"] {
                background-color: #315fce;
                border-color: #315fce;
                color: white;
            }


            /* Inputs */

            .stTextInput input,
            .stNumberInput input,
            .stDateInput input {
                background-color: #1f2937;
                color: #f3f4f6;
                border-color: #374151;
            }

            .stTextInput input:focus,
            .stNumberInput input:focus,
            .stDateInput input:focus {
                border-color: #6d8fe5;
            }


            /* Selectboxes */

            .stSelectbox [data-baseweb="select"] > div,
            .stMultiSelect [data-baseweb="select"] > div {
                background-color: #1f2937;
                color: #f3f4f6;
                border-color: #374151;
            }


            /* Metrics */

            [data-testid="stMetric"] {
                background-color: #1f2937;
                border-color: #374151;
            }


            /* Tables */

            [data-testid="stDataFrame"] {
                background-color: #1f2937;
                border-color: #374151;
            }


            /* Expanders */

            [data-testid="stExpander"] {
                background-color: #1f2937;
                border-color: #374151;
            }


            /* Dividers */

            hr {
                border-color: #374151;
            }


            /* Alerts */

            [data-testid="stAlert"] {
                background-color: #1f2937;
                border-color: #374151;
            }

            </style>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
            <style>

            /* =================================================
               LIGHT THEME
            ================================================= */

            .stApp {
                background-color: #f7f8fc;
                color: #20242d;
            }

            .main .block-container {
                color: #20242d;
            }

            h1 {
                color: #20242d !important;
            }

            h2 {
                color: #252a34 !important;
            }

            h3 {
                color: #303642 !important;
            }

            p,
            .stCaption {
                color: #555c69 !important;
            }


            /* Sidebar */

            section[data-testid="stSidebar"] {
                background-color: #ffffff;
                border-right: 1px solid #e5e7ed;
            }


            /* Buttons */

            .stButton > button {
                background-color: #ffffff;
                color: #303642;
                border-color: #d4d9e2;
            }

            .stButton > button:hover {
                background-color: #f3f5f8;
                border-color: #9ba4b3;
            }

            .stButton > button[kind="primary"] {
                background-color: #315fce;
                border-color: #315fce;
                color: #ffffff;
            }


            /* Inputs */

            .stTextInput input,
            .stNumberInput input,
            .stDateInput input {
                background-color: #ffffff;
                color: #20242d;
                border-color: #d9dde6;
            }


            /* Selectboxes */

            .stSelectbox [data-baseweb="select"] > div,
            .stMultiSelect [data-baseweb="select"] > div {
                background-color: #ffffff;
                color: #20242d;
                border-color: #d4d9e2;
            }


            /* Expanders */

            [data-testid="stExpander"] {
                background-color: #ffffff;
                border-color: #e2e5eb;
            }


            /* Dividers */

            hr {
                border-color: #e5e7ed;
            }

            </style>
            """,
            unsafe_allow_html=True,
        )
